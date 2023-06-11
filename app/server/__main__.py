import logging

from . import serve

if __name__ == "__main__":
    logging.basicConfig()
    serve(port="50051")
