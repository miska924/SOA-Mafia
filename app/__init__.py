from enum import Enum

from app.client import MafiaClient
from app.server import serve as run_server


class Role(Enum):
    Server = "server"
    Client = "client"


def main(args):
    if Role(args.role) == Role.Server:
        run_server(port=args.port)
    elif args.bot:
        MafiaClient(server_address=args.server_address, auto=True).run()
    else:
        MafiaClient(server_address=args.server_address).run()
