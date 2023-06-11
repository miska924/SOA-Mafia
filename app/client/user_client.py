import random
import logging
import time

from app.client.abstract_client import MafiaAbstractClient
from app.definitions import Commands


class MafiaUserClient(MafiaAbstractClient):
    def get_name(self):
        name = input("Name: ")
        logging.info(name)
        return name

    def get_command(self):
        print(
            f"Avaliable commands: {' '.join([item.value for item in self.get_avaliable_commands()])}"
        )
        while True:
            try:
                command = input("Command: ").split()
                logging.info(command)
                return command
            except Exception as e:
                continue
