import random
import logging
import time

from faker import Faker

from app.client.abstract_client import MafiaAbstractClient
from app.definitions import BOT_WAIT_MAX_MILLIS, MAGIC_SEED, Commands


def _bot_wait():
    time.sleep(random.randint(1, BOT_WAIT_MAX_MILLIS) / 1000)


class MafiaBotClient(MafiaAbstractClient):
    def get_name(self):
        fake = Faker()
        fake.random.seed(MAGIC_SEED)

        name = " ".join([fake.first_name(), fake.last_name()])
        logging.info(name)
        return name

    def get_command(self):
        command = random.choice(self.get_avaliable_commands())
        while command == Commands.LIST:
            command = random.choice(self.get_avaliable_commands())

        name = ""
        _bot_wait()
        logging.info(command)
        return command, name
