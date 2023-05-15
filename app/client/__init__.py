import logging
import grpc
import time
import threading
import random

from queue import Queue
from enum import Enum

import app.grpc.schema_pb2 as schema_pb2
import app.grpc.schema_pb2_grpc as schema_pb2_grpc

from app.definitions import ALL_PLAYERS_CONNECTED, BOT_NAMES
from app.client.heartbeat import HeartBeat
from app.client.notifier import Notifier


class Commands(Enum):
    Exit = "exit"
    Name = "name"
    ConnectRoom = "connect"
    DisconnectRoom = "disconnect"
    CreateRoom = "create"
    SetPlayersNumber = "players"


class MafiaClient:
    def __init__(self, server_address="172.17.0.1:50051", auto=False):
        self.auto = auto
        if auto:
            self.name = BOT_NAMES[random.randint(1, len(BOT_NAMES)) - 1]
            logging.info(self.name)
        else:
            self.name = input("Enter player name: ")

        if self.auto:
            time.sleep(random.randint(1, 2000) / 100)

        self.channel = grpc.insecure_channel(server_address)
        self.stub = schema_pb2_grpc.MafiaStub(self.channel)

        self.player_id = self._get_player_id()

        self.heartbeat = HeartBeat(self.stub, self.player_id)
        self.notifier = Notifier(self.stub, self.player_id)

    def _get_player_id(self):
        player_id_request = schema_pb2.PlayerIdRequest(name=self.name)
        return self.stub.PlayerId(player_id_request).player_id

    def _connect(self):
        while True:
            notification = self.notifier.next()
            print(notification)
            if notification == ALL_PLAYERS_CONNECTED:
                break

    def run(self):
        self._connect()

        alive = random.randint(1, 2000) / 100
        start = time.time()

        while True:
            if self.auto:
                continue
            else:
                command = input("Enter command(one of [list, disconnect]): ")

            if command == "list":
                response: schema_pb2.ListPlayersResponse = self.stub.ListPlayers(
                    schema_pb2.ListPlayersRequest(player_id=self.player_id)
                )
                print("\n".join(list(response.name)))
            elif command == "disconnect":
                break

        while True:
            notification = self.notifier.next_no_wait(default=None)
            if notification:
                logging.info(notification)

        self.notifier.stop()
        self.heartbeat.stop()
