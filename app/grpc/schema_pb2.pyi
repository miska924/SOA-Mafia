from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectionRequest(_message.Message):
    __slots__ = ["player_id"]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: str
    def __init__(self, player_id: _Optional[str] = ...) -> None: ...

class ConnectionResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class ListPlayersRequest(_message.Message):
    __slots__ = ["player_id"]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: str
    def __init__(self, player_id: _Optional[str] = ...) -> None: ...

class ListPlayersResponse(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[_Iterable[str]] = ...) -> None: ...

class NotificationRequest(_message.Message):
    __slots__ = ["player_id", "timestamp"]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    player_id: str
    timestamp: int
    def __init__(self, player_id: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class NotificationResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class PlayerIdRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class PlayerIdResponse(_message.Message):
    __slots__ = ["player_id"]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: str
    def __init__(self, player_id: _Optional[str] = ...) -> None: ...
