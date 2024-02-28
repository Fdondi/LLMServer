from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TYPE_PLAIN: _ClassVar[Type]
    TYPE_DICTIONARY: _ClassVar[Type]
TYPE_PLAIN: Type
TYPE_DICTIONARY: Type

class Request(_message.Message):
    __slots__ = ("query", "type", "max_tokens", "id")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    query: str
    type: Type
    max_tokens: int
    id: int
    def __init__(self, query: _Optional[str] = ..., type: _Optional[_Union[Type, str]] = ..., max_tokens: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("id", "query", "response")
    ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    id: int
    query: str
    response: str
    def __init__(self, id: _Optional[int] = ..., query: _Optional[str] = ..., response: _Optional[str] = ...) -> None: ...
