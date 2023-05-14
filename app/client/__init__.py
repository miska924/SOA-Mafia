import logging
import grpc
import time
import random
import threading

from queue import Queue
from enum import Enum

import app.grpc.schema_pb2 as schema_pb2
import app.grpc.schema_pb2_grpc as schema_pb2_grpc

from app.definitions import ALL_PLAYERS_CONNECTED, BOT_NAMES


class Commands(Enum):
    Exit = "exit"
    Name = "name"
    ConnectRoom = "connect"
    DisconnectRoom = "disconnect"
    CreateRoom = "create"
    SetPlayersNumber = "players"


def send_connection_events(stub, player_id, stop):
    responses = stub.Connected(generate_connection_events(player_id, stop))

    for response in responses:
        pass


def generate_connection_events(player_id, stop):
    while not stop():
        yield schema_pb2.ConnectionRequest(player_id=player_id, connected=True)
        time.sleep(0.1)


def run_heartbeat_thread(stub, player_id):
    stop = [False]
    connection_events_thread = threading.Thread(
        target=send_connection_events, args=(stub, player_id, lambda: stop[0])
    )

    connection_events_thread.start()
    return connection_events_thread, stop


def get_player_id(stub):
    player_id_request = schema_pb2.PlayerIdRequest(old_player_id="")
    return stub.PlayerId(player_id_request).player_id


def get_notifications(stub, player_id):
    notifications_request = schema_pb2.NotificationRequest(player_id=player_id)
    for response in stub.Notifications(notifications_request):
        yield response.message


def generator_thread_func(stub, player_id, q: Queue):
    for value in get_notifications(stub, player_id):
        q.put(value)


def run(server_address="172.17.0.1:50051"):
    with grpc.insecure_channel(server_address) as channel:
        stub = schema_pb2_grpc.MafiaStub(channel)

        player_id = get_player_id(stub)

        heartbeat_thread, stop = run_heartbeat_thread(stub, player_id)

        notifications = Queue()
        generator_thread = threading.Thread(
            target=generator_thread_func,
            args=(stub, player_id, notifications),
        )
        generator_thread.start()

        while generator_thread.is_alive() or not notifications.empty():
            message = notifications.get()
            logging.info(message)
            if message == ALL_PLAYERS_CONNECTED:
                break

        alive = random.randint(1, 1000) / 100
        start = time.time()

        while (
            generator_thread.is_alive() or not notifications.empty()
        ) and time.time() - start < alive:
            if not notifications.empty():
                logging.info(notifications.get())

        stop[0] = True
        heartbeat_thread.join()
        generator_thread.join()
