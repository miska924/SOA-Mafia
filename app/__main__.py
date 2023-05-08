import logging
import argparse

from . import Role, main

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--role",
        type=str,
        choices=[item.value for item in Role],
        default=Role.Server.value,
    )
    parser.add_argument("--port", "-p", type=str, default="50051")

    args = parser.parse_args()

    main(args)
