from concurrent import futures
from typing import List
from random import shuffle, choice
import logging
import uuid
import time
from queue import Queue

import grpc
import app.grpc.schema_pb2 as schema
import app.grpc.schema_pb2_grpc as schema_grpc

import threading

from app.definitions import (
    NEEDED_PLAYERS_FOR_GAME,
    NOTIFICATIONS_KEY,
    CONNECTED_OK,
    EMPTY,
    NEW_PLAYER_CONNECTED,
    PLAYER_IS_GREATING_YOU,
    ALL_PLAYERS_CONNECTED,
    PLAYER_DISCONNECTED,
    STREAM_RESPONSE_TIME_THREASHOLD,
    ROLES,
    Role,
)


class Mafia(schema_grpc.MafiaServicer):
    def __init__(self, **kwargs):
        super().__init__()
        self.lock = threading.Lock()
        self.players = []
        self.names = {}
        self.player_by_name = {}
        self.roles = {}
        self.alive = {}
        self.notifications = {}
        self.votes = {}
        self.turn = set()
        self.alive_players_count = 0
        self.to_kill_player_id = None

        self.roles_left = ROLES.copy()
        shuffle(self.roles_left)

    def _players_count(self):
        with self.lock:
            return len(self.players)

    def _full(self):
        return self._players_count() == NEEDED_PLAYERS_FOR_GAME

    def _notify_about_full(self):
        for player_id in self.players:
            with self.lock:
                queue = self.notifications[player_id]

            queue.put(ALL_PLAYERS_CONNECTED)

    def _notify_about_join(self, joined_player_id):
        for player_id in self.players:
            if player_id == joined_player_id:
                continue

            with self.lock:
                queue = self.notifications[player_id]
                name = self.names[joined_player_id]

            queue.put(NEW_PLAYER_CONNECTED.format(name=name))

        if self._full():
            self._notify_about_full()

    def _join(self, player_id, name):
        if self._player_exists(player_id):
            logging.error("exists %s", player_id)
            return None

        with self.lock:
            self.players.append(player_id)
            self.notifications[player_id] = Queue()
            self.names[player_id] = name
            self.player_by_name[name] = player_id

            self.alive[player_id] = True

            self.roles[player_id] = self.roles_left[-1]
            self.roles_left = self.roles_left[:-1]
            self.votes[player_id] = 0
            self.alive_players_count += 1

        return player_id

    def _get_notifications(self, player_id):
        if not self._player_exists(player_id):
            return Queue()

        with self.lock:
            return self.notifications[player_id]

    def _notify_about_disconnect(self, disconnected_player_id):
        for player_id in self.players:
            if player_id == disconnected_player_id:
                continue

            with self.lock:
                queue = self.notifications[player_id]
                name = self.names[disconnected_player_id]

            queue.put(PLAYER_DISCONNECTED.format(name=name))

    def _disconnect(self, player_id):
        if not self._player_exists(player_id):
            return

        with self.lock:
            self.players.remove(player_id)
            del self.notifications[player_id]
            del self.player_by_name[self.names[player_id]]
            del self.names[player_id]
            del self.alive[player_id]
            del self.votes[player_id]
            self.alive_players_count -= 1

            self.roles_left.append(self.roles[player_id])
            del self.roles[player_id]

        self._notify_about_disconnect(player_id)

    def _player_exists(self, player_id):
        with self.lock:
            return player_id in self.players

    def _mafia_alive(self):
        for player_id in self.alive:
            if self.roles[player_id] == Role.MAFIA.value:
                return self.alive[player_id]
        return False

    def PlayerId(self, request, context):
        player_id = str(uuid.uuid4())

        if not self._join(player_id, request.name):
            return schema.PlayerIdResponse(player_id=EMPTY)

        self._notify_about_join(player_id)
        return schema.PlayerIdResponse(player_id=player_id)

    def Notifications(self, request_iterator, context):
        for request in request_iterator:
            # if request.timestamp - time.time() > STREAM_RESPONSE_TIME_THREASHOLD:
            #     continue
            notifications = self._get_notifications(request.player_id)

            if notifications.empty():
                yield schema.NotificationResponse(message=EMPTY)

            message = notifications.get()
            logging.info(message)
            yield schema.NotificationResponse(message=message)

    def Connected(self, request_iterator, context):
        player_id = None
        try:
            for request in request_iterator:
                player_id = request.player_id
                yield schema.ConnectionResponse(message=CONNECTED_OK)
        except Exception:
            pass

        self._disconnect(player_id)

    def ListPlayers(self, request, context):
        player_id = request.player_id
        response = schema.ListPlayersResponse()
        for player_id in self.players:
            if self.alive[player_id]:
                name = self.names[player_id]
                response.name.append(name)

        return response

    def Role(self, request, context):
        player_id = request.player_id
        response = schema.RoleResponse()
        response.role = self.roles[player_id]
        return response

    def Kill(self, request, context):
        response = schema.KillResponse()
        if not request.name:
            player_id = choice(self.players)
        elif request.name not in self.player_by_name:
            response.message = "No such player"
            return response
        else:
            player_id = self.player_by_name[request.name]

        if not self.alive[player_id]:
            response.message = "Player is not alive"
            return response

        if request.player_id == player_id:
            response.message = "You cannot suicide"
            return response

        with self.lock:
            self.alive[player_id] = False
            self.to_kill_player_id = player_id
        response.message = f"Ok. {self.names[player_id]} killed."
        return response

    def _count_votes(self):
        votes_sum = 0
        with self.lock:
            for player_id in self.votes:
                votes_sum += self.votes[player_id]
        return votes_sum

    def _clear_votes(self):
        with self.lock:
            for player_id in self.votes:
                self.votes[player_id] = 0

    def _max_voted_player_id(self):
        max_player_id = None
        with self.lock:
            for player_id in self.votes:
                if (
                    max_player_id is None
                    or self.votes[player_id] > self.votes[max_player_id]
                ):
                    max_player_id = player_id
        return max_player_id

    def Vote(self, request, context):
        response = schema.VoteResponse()
        if not request.name:
            player_id = choice(self.players)
        elif request.name not in self.player_by_name:
            response.message = "No such player"
            return response
        else:
            player_id = self.player_by_name[request.name]

        if not self.alive[player_id]:
            response.message = "Player is not alive"
            return response

        if request.player_id == player_id:
            response.message = "You cannot vote for yourself"
            return response

        with self.lock:
            self.votes[player_id] += 1
        response.message = f"Ok. Vote for {self.names[player_id]}."

        if self._count_votes() == self.alive_players_count:
            self.to_kill_player_id = self._max_voted_player_id()
            self.alive[self.to_kill_player_id] = False
            self._clear_votes()

        return response

    def IsAlive(self, request, context):
        player_id = request.player_id
        response = schema.IsAliveResponse()
        response.is_alive = self.alive[player_id]
        return response

    def Turn(self, request, context):
        with self.lock:
            self.turn.add(request.player_id)

        while len(self.turn) != self.alive_players_count:
            time.sleep(0.1)

        time.sleep(0.5)
        self.turn.remove(request.player_id)

        response = schema.TurnResponse()
        if self._mafia_alive():
            if self.alive_players_count - bool(self.to_kill_player_id) == 1:
                response.message = "Congrats! Mafia wins"
        else:
            response.message = "Congrats! Citizens win"

        with self.lock:
            if self.to_kill_player_id == request.player_id:
                self.to_kill_player_id = None
                self.alive_players_count -= 1

        return response

    def Check(self, request, context):
        # logging.info("Check called")
        response = schema.CheckResponse()
        if not request.name:
            player_id = choice(self.players)
        elif request.name not in self.player_by_name:
            response.message = "No such player"
            # logging.info(response.message)
            return response
        else:
            player_id = self.player_by_name[request.name]

        response.is_mafia = self.roles[player_id] == Role.MAFIA.value
        response.message = f"Ok. {self.names[player_id]} {'is' if response.is_mafia else 'is not'} mafia."
        # logging.info(response.message)
        return response


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    schema_grpc.add_MafiaServicer_to_server(Mafia(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info("Server started, listening on " + port)
    server.wait_for_termination()
