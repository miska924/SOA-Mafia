from concurrent import futures
import logging

import grpc
import app.grpc.schema_pb2 as schema
import app.grpc.schema_pb2_grpc as schema_grpc


class Greeter(schema_grpc.GreeterServicer):
    def Ping(self, request, context):
        logging.info(request.message)
        return schema.PingReply(message=request.message)


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schema_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info("Server started, listening on " + port)
    server.wait_for_termination()
