"""Exposes all output formatters that have built-in support for preconversion

Note: the interesting try: catch: pattern is done as their isn't a guarantee that the user has
any of the given output formatters installed, which is required for preconvert to plug-in
it's preconversion.
"""
try:
    from preconvert.output import json
except ImportError:
    pass

try:
    from preconvert.output import bson
except ImportError:
    pass

try:
    from preconvert.output import msgpack
except ImportError:
    pass

try:
    from preconvert.output import simplejson
except ImportError:
    pass
