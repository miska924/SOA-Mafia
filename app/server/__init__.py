from concurrent import futures
from typing import List
import logging
import uuid
import time

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
)


class Mafia(schema_grpc.MafiaServicer):
    def __init__(self, **kwargs):
        super().__init__()
        self.players_lock = threading.Lock()
        self.players = {}

    def PlayerId(self, request, context):
        player_id = str(uuid.uuid1())

        # notify all players about new connection
        with self.players_lock:
            self.players[player_id] = {NOTIFICATIONS_KEY: []}

            all_players_connected = False
            if len(self.players) == NEEDED_PLAYERS_FOR_GAME:
                all_players_connected = True
                self.players[player_id][NOTIFICATIONS_KEY].append(ALL_PLAYERS_CONNECTED)

            for other_player_id in self.players:
                self.players[other_player_id][NOTIFICATIONS_KEY].append(
                    NEW_PLAYER_CONNECTED.format(player_id=player_id)
                )

                self.players[player_id][NOTIFICATIONS_KEY].append(
                    PLAYER_IS_GREATING_YOU.format(player_id=other_player_id)
                )

                if all_players_connected:
                    self.players[other_player_id][NOTIFICATIONS_KEY].append(
                        ALL_PLAYERS_CONNECTED
                    )

        return schema.PlayerIdResponse(player_id=player_id)

    def Notifications(self, request, context):
        player_id = request.player_id

        with self.players_lock:
            if player_id not in self.players:
                return schema.NotificationResponse(message=EMPTY)

        with self.players_lock:
            players_count = len(self.players)

        # logging.info(".")
        try:
            while True:
                with self.players_lock:
                    if player_id in self.players and len(
                        self.players[player_id][NOTIFICATIONS_KEY]
                    ):
                        yield schema.NotificationResponse(
                            message=self.players[player_id][NOTIFICATIONS_KEY][0]
                        )
                        self.players[player_id][NOTIFICATIONS_KEY] = self.players[
                            player_id
                        ][NOTIFICATIONS_KEY][1:]

                    players_count = len(self.players)
                time.sleep(0.1)
        except Exception:
            pass
        return

    def Connected(self, request_iterator, context):
        player_id = None
        try:
            for request in request_iterator:
                player_id = request.player_id
                if request.connected:
                    yield schema.ConnectionResponse(message=CONNECTED_OK)
                else:
                    break
        except Exception:
            pass

        # logging.info(PLAYER_DISCONNECTED.format(player_id=player_id))
        with self.players_lock:
            del self.players[player_id]

            for another_player_id in self.players:
                self.players[another_player_id][NOTIFICATIONS_KEY].append(
                    PLAYER_DISCONNECTED.format(player_id=player_id)
                )
        return schema.ConnectionResponse(message=EMPTY)


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schema_grpc.add_MafiaServicer_to_server(Mafia(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info("Server started, listening on " + port)
    server.wait_for_termination()
