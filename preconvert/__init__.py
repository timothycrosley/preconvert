"""A Library to enable preconversion of any Python type into one that is easily serializable"""
import pkg_resources

from preconvert import convert, exceptions, output
from preconvert.convert import default_serializer
from preconvert.register import bson, converter, json, msgpack

for plugin in pkg_resources.iter_entry_points("preconvert.converters"):
    plugin.load()

__version__ = "0.0.3"
__all__ = [
    "converter",
    "json",
    "bson",
    "msgpack",
    "exceptions",
    "convert",
    "output",
    "unserializable",
    "__version__",
]
