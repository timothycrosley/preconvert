import msgpack
from msgpack import *

from preconvert import convert
from preconvert.converters import convert_namedtuple


def pack(content, *args, default=convert.msgpack, **kwargs):  # type: ignore
    """Msgpacks with preconversion for common unserializable types in place"""
    if isinstance(content, tuple):
        content = convert_namedtuple(content)
    return msgpack.pack(content, default=default, *args, **kwargs)


def packb(content, *args, default=convert.msgpack, **kwargs):  # type: ignore
    """Msgpacks with preconversion for common unserializable types in place"""
    if isinstance(content, tuple):
        content = convert_namedtuple(content)
    return msgpack.packb(content, default=default, *args, **kwargs)


def dump(content, *args, default=convert.msgpack, **kwargs):  # type: ignore
    """Msgpack dump with preconversion for common unserializable types in place"""
    if isinstance(content, tuple):
        content = convert_namedtuple(content)
    return msgpack.dump(content, default=default, *args, **kwargs)


def dumps(content, *args, default=convert.msgpack, **kwargs):  # type: ignore
    """Msgpacks dump with preconversion for common unserializable types in place"""
    if isinstance(content, tuple):
        content = convert_namedtuple(content)
    return msgpack.dumps(content, default=default, *args, **kwargs)
