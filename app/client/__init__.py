import logging
import grpc

import app.grpc.schema_pb2 as schema_pb2
import app.grpc.schema_pb2_grpc as schema_pb2_grpc


def run(server_address="172.17.0.1:50051"):
    logging.info("Will try to greet world ...")
    with grpc.insecure_channel(server_address) as channel:
        stub = schema_pb2_grpc.GreeterStub(channel)
        response = stub.Ping(schema_pb2.PingRequest(message="ahahahahah"))
    logging.info("Greeter client received: %s", response.message)
