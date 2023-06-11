from enum import Enum

from app.client.user_client import MafiaUserClient
from app.client.bot_client import MafiaBotClient
from app.server import serve as run_server


class Role(Enum):
    Server = "server"
    Client = "client"


def main(args):
    if Role(args.role) == Role.Server:
        run_server(port=args.port)
    elif args.bot:
        MafiaBotClient(server_address=args.server_address).run()
    else:
        MafiaUserClient(server_address=args.server_address).run()
