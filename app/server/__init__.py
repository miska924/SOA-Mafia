from concurrent import futures
from typing import List
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
)


class Mafia(schema_grpc.MafiaServicer):
    def __init__(self, **kwargs):
        super().__init__()
        self.lock = threading.Lock()
        self.players = []
        self.names = {}
        self.notifications = {}

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

        self._notify_about_disconnect(player_id)

    def _player_exists(self, player_id):
        with self.lock:
            return player_id in self.players

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
        logging.info(player_id)
        response = schema.ListPlayersResponse()
        for player_id in self.players:
            name = self.names[player_id]
            response.name.append(name)

        return response


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    schema_grpc.add_MafiaServicer_to_server(Mafia(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info("Server started, listening on " + port)
    server.wait_for_termination()
