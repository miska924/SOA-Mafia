import logging
import threading
import time

import app.grpc.schema_pb2 as schema_pb2


def _send_connection_events(stub, player_id, stop):
    responses = stub.Connected(_generate_connection_events(player_id, stop))

    for _ in responses:
        pass


def _generate_connection_events(player_id, stop):
    while not stop():
        yield schema_pb2.ConnectionRequest(player_id=player_id)
        time.sleep(1)


class HeartBeat:
    def __init__(self, stub, player_id):
        self.stub = stub
        self.player_id = player_id

        self._stop = [False]
        self.heartbeat_thread = threading.Thread(
            target=_send_connection_events,
            args=(
                self.stub,
                self.player_id,
                lambda: self._stop[0],
            ),
        )
        self.heartbeat_thread.start()

    def stop(self) -> None:
        self._stop[0] = True
        self.heartbeat_thread.join()
