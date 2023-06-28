import argparse
import redis
import threading
import time
from faker import Faker


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--chat",
        type=str,
        default="trash",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6379,
    )

    fake = Faker()
    fake.random.seed(int(time.time() * 1000))

    parser.add_argument(
        "--username",
        type=str,
        default="".join((fake.first_name(), fake.last_name())),
    )

    return parser.parse_args()


def listen(pubsub):
    while True:
        message = pubsub.get_message()
        if message and message["type"] == "message":
            print(str(message["data"], "utf-8"))
        time.sleep(0.01)


def main(args):
    r = redis.Redis(host=args.host, port=args.port, db=0)

    p = r.pubsub()
    p.subscribe(args.chat)

    listening_thread = threading.Thread(
        target=listen,
        args=(p,),
    )
    listening_thread.start()

    while True:
        message = input()
        r.publish(args.chat, " > ".join((args.username, message)))
