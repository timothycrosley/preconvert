import json
from json import *

from preconvert import convert
from preconvert.converters import convert_namedtuple


def dumps(content, *args, default=convert.json, **kwargs):  # type: ignore
    """JSON dumps with preconversion for common unserializable types in place"""
    if isinstance(content, tuple):
        content = convert_namedtuple(content)
    return json.dumps(content, default=default, *args, **kwargs)


def dump(content, *args, default=convert.json, **kwargs):  # type: ignore
    """JSON dump with preconversion for common unserializable types in place"""
    if isinstance(content, tuple):
        content = convert_namedtuple(content)
    return json.dump(content, default=default, *args, **kwargs)
