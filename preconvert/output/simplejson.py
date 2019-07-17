import simplejson
from funtools import partial
from preconvert import convert
from simplejson import *

dumps = partial(simplejson.dumps, default=convert.json)  # type: ignore
dump = partial(simplejson.dump, default=convert.json)  # type: ignore
