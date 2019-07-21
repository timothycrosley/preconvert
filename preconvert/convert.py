from collections import ChainMap
from enum import Enum
from functools import partial
from typing import Any, Callable, Dict, Sequence, Text, Union

from preconvert.exceptions import Unconvertable
from preconvert.register import converters


class PreconversionSource(Enum):
    """All globally available conversion sources"""

    ALL_PACKAGES = 1
    PRECONVERT = 2


def unserializable(
    item: Any,
    namespace: Text = "base",
    base_namespace: Text = "base",
    using: Union[Sequence[Text], PreconversionSource] = PreconversionSource.ALL_PACKAGES,
    store: Dict[Text, Dict[Text, Dict[Any, Callable]]] = converters,
):
    if hasattr(item, "__native_types__"):
        return item.__native_types__()

    if using == PreconversionSource.ALL_PACKAGES:
        package_stores = store.values()
    elif using == PreconversionSource.PRECONVERT:
        package_stores = (store["preconvert"],)
    else:
        package_stores = tuple(store[use_package] for use_package in using)

    if base_namespace and namespace != base_namespace:
        preconverters = ChainMap(
            ChainMap(package_store.get(namespace, {}), package_store["base"])
            for package_store in package_stores
        ).items()
    else:
        preconverters = ChainMap(store[base_namespace] for package_store in package_stores).items()

    for kind, transformer in reversed(tuple(preconverters)):
        if isinstance(item, kind):
            return transformer(item)

    if hasattr(item, "__iter__"):
        return list(item)

    raise Unconvertable(item)


json = partial(unserializable, namespace="json")
bson = partial(unserializable, namespace="bson")
msgpack = partial(unserializable, namespace="msgpack")
