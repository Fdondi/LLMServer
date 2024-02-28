from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Id(_message.Message):
    __slots__ = ("conversation", "message")
    CONVERSATION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    conversation: int
    message: int
    def __init__(self, conversation: _Optional[int] = ..., message: _Optional[int] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ("id", "query", "max_tokens")
    ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    id: Id
    query: str
    max_tokens: int
    def __init__(self, id: _Optional[_Union[Id, _Mapping]] = ..., query: _Optional[str] = ..., max_tokens: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("id", "query", "response")
    ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    id: Id
    query: str
    response: str
    def __init__(self, id: _Optional[_Union[Id, _Mapping]] = ..., query: _Optional[str] = ..., response: _Optional[str] = ...) -> None: ...
