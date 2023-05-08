from enum import Enum

from app.client import run as run_client
from app.server import serve as run_server


class Role(Enum):
    Server = "server"
    Client = "client"


def main(args):
    if Role(args.role) == Role.Server:
        run_server(port=args.port)
    else:
        run_client()
