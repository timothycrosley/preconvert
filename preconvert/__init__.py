"""A Library to enable preconversion of any Python type into one that is easily serializable"""
__version__ = "0.0.1"

from preconvert import convert, exceptions, output
from preconvert.register import bson, converter, json, msgpack
from preconvert.convert import unserializable

__all__ = ["converter", "json", "bson", "msgpack", "exceptions", "convert", "output", "unserializable"]
