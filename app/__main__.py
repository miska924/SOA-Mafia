import logging
import argparse

from . import Role, main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--role",
        type=str,
        choices=[item.value for item in Role],
        default=Role.Server.value,
    )
    parser.add_argument("--port", "-p", type=str, default="50051")
    parser.add_argument("--server-address", type=str, default="172.17.0.1:50051")
    parser.add_argument("--bot", action="store_true")

    args = parser.parse_args()

    main(args)
