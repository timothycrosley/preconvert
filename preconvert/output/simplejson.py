from functools import partial

import simplejson
from simplejson import *

from preconvert import convert

dumps = partial(simplejson.dumps, default=convert.json)  # type: ignore
dump = partial(simplejson.dump, default=convert.json)  # type: ignore
