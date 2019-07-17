from collections import ChainMap
from functools import partial
from typing import Any, Callable, Dict, Text

from preconvert.exceptions import Unconvertable
from preconvert.register import converters


def unserializable(
    item: Any,
    namespace: Text = "base",
    base_namespace: Text = "base",
    store: Dict[Text, Dict[Any, Callable]] = converters,
):
    if hasattr(item, "__native_types__"):
        return item.__native_types__()

    if base_namespace and namespace != base_namespace:
        preconverters = ChainMap(store.get(namespace, {}), store["base"]).items()
    else:
        preconverters = store[base_namespace].items()

    for kind, transformer in reversed(tuple(preconverters)):
        if isinstance(item, kind):
            return transformer(item)

    if hasattr(item, "__iter__"):
        return list(item)

    raise Unconvertable(item)


json = partial(unserializable, namespace="json")
bson = partial(unserializable, namespace="bson")
msgpack = partial(unserializable, namespace="msgpack")
