# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: app/grpc/schema.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x61pp/grpc/schema.proto\x12\x05mafia\"\x1e\n\x0bPingRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1c\n\tPingReply\x12\x0f\n\x07message\x18\x01 \x01(\t2q\n\x07Greeter\x12.\n\x04Ping\x12\x12.mafia.PingRequest\x1a\x10.mafia.PingReply\"\x00\x12\x36\n\nStreamPing\x12\x12.mafia.PingRequest\x1a\x10.mafia.PingReply\"\x00\x30\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'app.grpc.schema_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PINGREQUEST._serialized_start=32
  _PINGREQUEST._serialized_end=62
  _PINGREPLY._serialized_start=64
  _PINGREPLY._serialized_end=92
  _GREETER._serialized_start=94
  _GREETER._serialized_end=207
# @@protoc_insertion_point(module_scope)
