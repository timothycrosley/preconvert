import bson
from bson import *

from preconvert import convert
from preconvert.converters import convert_namedtuple


def dumps(content, *args, on_unknown=convert.bson, **kwargs):  # type: ignore
    """BSON dumps with preconversion for common unserializable types in place"""
    if isinstance(content, tuple):
        content = convert_namedtuple(content)
    return bson.dumps(content, on_unknown=on_unknown, *args, **kwargs)


def dump(content, *args, on_unknown=convert.bson, **kwargs):  # type: ignore
    """BSON dump with preconversion for common unserializable types in place"""
    if isinstance(content, tuple):
        content = convert_namedtuple(content)
    return bson.dump(content, on_unknown=on_unknown, *args, **kwargs)
