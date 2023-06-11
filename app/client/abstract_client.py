import logging
import grpc
import time
import random

from enum import Enum

import app.grpc.schema_pb2 as schema_pb2
import app.grpc.schema_pb2_grpc as schema_pb2_grpc

from app.definitions import ALL_PLAYERS_CONNECTED, Commands, Role, Time
from app.client.heartbeat import HeartBeat
from app.client.notifier import Notifier


class MafiaAbstractClient:
    def __init__(self, server_address="172.17.0.1:50051"):
        time.sleep(1)
        self.name = self.get_name()

        self.channel = grpc.insecure_channel(server_address)
        self.stub = schema_pb2_grpc.MafiaStub(self.channel)

        self.player_id = self._get_player_id()

        self.heartbeat = HeartBeat(self.stub, self.player_id)
        self.notifier = Notifier(self.stub, self.player_id)

    def get_name(self):
        raise NotImplementedError()

    def get_avaliable_commands(self):
        commands = [Commands.LIST]
        if self.time == Time.DAY:
            commands.append(Commands.VOTE)
        elif self.time == Time.NIGHT:
            if self.role == Role.MAFIA:
                commands.append(Commands.KILL)

            elif self.role == Role.POLICE:
                commands.append(Commands.CHECK)

            else:
                commands.append(Commands.PROCEED)

        return commands

    def get_command(self):
        raise NotImplementedError()

    def _get_player_id(self):
        player_id_request = schema_pb2.PlayerIdRequest(name=self.name)
        return self.stub.PlayerId(player_id_request).player_id

    def _connect(self):
        while True:
            notification = self.notifier.next()
            print(notification)
            if notification == ALL_PLAYERS_CONNECTED:
                break
        response: schema_pb2.RoleResponse = self.stub.Role(
            schema_pb2.RoleRequest(player_id=self.player_id)
        )
        self.role = Role(response.role)
        print(f"ROLE: {self.role.value}")

        self.time = Time.DAY

    def is_alive(self):
        response: schema_pb2.IsAliveResponse = self.stub.IsAlive(
            schema_pb2.IsAliveRequest(player_id=self.player_id)
        )
        return response.is_alive

    def round(self):
        while True:
            command = self.get_command()
            args = " ".join(command[1:])

            if Commands(command[0]) == Commands.LIST:
                response: schema_pb2.ListPlayersResponse = self.stub.ListPlayers(
                    schema_pb2.ListPlayersRequest(player_id=self.player_id)
                )
                logging.info("\n".join(list(response.name)))
                ("\n".join(list(response.name)))

            elif Commands(command[0]) == Commands.VOTE:
                response: schema_pb2.VoteResponse = self.stub.Vote(
                    schema_pb2.VoteRequest(player_id=self.player_id, name=args)
                )
                while "Ok" not in response.message:
                    logging.error(response.message)
                    response = self.stub.Vote(
                        schema_pb2.VoteRequest(player_id=self.player_id, name=args)
                    )
                logging.info(response.message)
                return True

            elif Commands(command[0]) == Commands.KILL:
                response: schema_pb2.KillResponse = self.stub.Kill(
                    schema_pb2.KillRequest(player_id=self.player_id, name=args)
                )
                while "Ok" not in response.message:
                    logging.error(response.message)
                    response = self.stub.Kill(
                        schema_pb2.KillRequest(player_id=self.player_id, name=args)
                    )
                logging.info(response.message)
                return True
            elif Commands(command[0]) == Commands.CHECK:
                response: schema_pb2.CheckResponse = self.stub.Check(
                    schema_pb2.CheckRequest(name=args)
                )
                while "Ok" not in response.message:
                    logging.error(response.message)
                    response = self.stub.Check(schema_pb2.CheckRequest(name=args))
                logging.info(response.message)
                return True
            elif Commands(command[0]) == Commands.PROCEED:
                logging.info("Ok")
                return True

    def run(self):
        self._connect()

        while True:
            if self.is_alive():
                self.round()
                response: schema_pb2.TurnResponsee = self.stub.Turn(
                    schema_pb2.TurnRequest(player_id=self.player_id)
                )
                if "Congrats!" in response.message:
                    logging.info(response.message)
                    break
            else:
                logging.info("You are killed")
                break
            self.time = Time.NIGHT if self.time == Time.DAY else Time.DAY

        # while listen():
        #     notification = self.notifier.next_no_wait(default=None)
        #     if notification:
        #         logging.info(notification)

        self.notifier.stop()
        self.heartbeat.stop()
