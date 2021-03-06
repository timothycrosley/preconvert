"""A Library to enable preconversion of any Python type into one that is easily serializable"""
import pkg_resources

from preconvert import exceptions, output
from preconvert.output.convert import default_serializer
from preconvert.register import bson, converter, json, msgpack

for plugin in pkg_resources.iter_entry_points("preconvert.converters"):
    plugin.load()

__version__ = "0.0.6"
__all__ = [
    "converter",
    "json",
    "bson",
    "msgpack",
    "exceptions",
    "output",
    "default_serializer",
    "__version__",
]
