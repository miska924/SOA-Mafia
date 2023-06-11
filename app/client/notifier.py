import logging
import threading
import time

from queue import Queue

import app.grpc.schema_pb2 as schema_pb2
from app.definitions import EMPTY


def _notifications_thread(stub, player_id, notifications: Queue, stop):
    for response in stub.Notifications(
        _generate_notifications_requests(player_id, stop)
    ):
        if response.message == EMPTY:
            continue

        notifications.put(response.message)


def _generate_notifications_requests(player_id, stop):
    while not stop():
        yield schema_pb2.NotificationRequest(
            player_id=player_id, timestamp=int(time.time())
        )
        time.sleep(1)


class Notifier:
    def __init__(self, stub, player_id) -> None:
        self.stub = stub
        self.player_id = player_id

        self.notifications = Queue()
        self._stop = [False]

        self.notifier_thread = threading.Thread(
            target=_notifications_thread,
            args=(self.stub, self.player_id, self.notifications, lambda: self._stop[0]),
        )
        self.notifier_thread.start()

    def next(self):
        return self.notifications.get()

    def next_no_wait(self, default=None):
        if self.notifications.empty():
            return default

        return self.notifications.get()

    def stop(self) -> None:
        self._stop[0] = True
        self.notifier_thread.join()
