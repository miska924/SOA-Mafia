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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x61pp/grpc/schema.proto\x12\x05mafia\"&\n\x11\x43onnectionRequest\x12\x11\n\tplayer_id\x18\x01 \x01(\t\"%\n\x12\x43onnectionResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\";\n\x13NotificationRequest\x12\x11\n\tplayer_id\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\"\'\n\x14NotificationResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1f\n\x0fPlayerIdRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"%\n\x10PlayerIdResponse\x12\x11\n\tplayer_id\x18\x01 \x01(\t\"\'\n\x12ListPlayersRequest\x12\x11\n\tplayer_id\x18\x01 \x01(\t\"#\n\x13ListPlayersResponse\x12\x0c\n\x04name\x18\x01 \x03(\t2\xa6\x02\n\x05Mafia\x12=\n\x08PlayerId\x12\x16.mafia.PlayerIdRequest\x1a\x17.mafia.PlayerIdResponse\"\x00\x12N\n\rNotifications\x12\x1a.mafia.NotificationRequest\x1a\x1b.mafia.NotificationResponse\"\x00(\x01\x30\x01\x12\x46\n\tConnected\x12\x18.mafia.ConnectionRequest\x1a\x19.mafia.ConnectionResponse\"\x00(\x01\x30\x01\x12\x46\n\x0bListPlayers\x12\x19.mafia.ListPlayersRequest\x1a\x1a.mafia.ListPlayersResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'app.grpc.schema_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CONNECTIONREQUEST._serialized_start=32
  _CONNECTIONREQUEST._serialized_end=70
  _CONNECTIONRESPONSE._serialized_start=72
  _CONNECTIONRESPONSE._serialized_end=109
  _NOTIFICATIONREQUEST._serialized_start=111
  _NOTIFICATIONREQUEST._serialized_end=170
  _NOTIFICATIONRESPONSE._serialized_start=172
  _NOTIFICATIONRESPONSE._serialized_end=211
  _PLAYERIDREQUEST._serialized_start=213
  _PLAYERIDREQUEST._serialized_end=244
  _PLAYERIDRESPONSE._serialized_start=246
  _PLAYERIDRESPONSE._serialized_end=283
  _LISTPLAYERSREQUEST._serialized_start=285
  _LISTPLAYERSREQUEST._serialized_end=324
  _LISTPLAYERSRESPONSE._serialized_start=326
  _LISTPLAYERSRESPONSE._serialized_end=361
  _MAFIA._serialized_start=364
  _MAFIA._serialized_end=658
# @@protoc_insertion_point(module_scope)
