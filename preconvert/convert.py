from itertools import chain
from enum import Enum
from functools import partial
from typing import Any, Callable, Dict, Iterable, Text, Union

from preconvert.exceptions import Unconvertable
from preconvert.register import converters


class PreconversionSource(Enum):
    """All globally available conversion sources"""

    ALL_PACKAGES = 1
    PRECONVERT = 2


def default_serializer(
    item: Any,
    namespace: Text = "base",
    base_namespace: Text = "base",
    using: Union[Iterable[Text], PreconversionSource] = PreconversionSource.ALL_PACKAGES,
    store: Dict[Text, Dict[Text, Dict[Any, Callable]]] = converters,
):
    if hasattr(item, "__jsonifiable__"):
        return item.__jsonifiable__()

    package_stores: Any
    if using == PreconversionSource.ALL_PACKAGES:
        package_stores = store.values()
    elif using == PreconversionSource.PRECONVERT:
        package_stores = (store["preconvert"],)
    elif isinstance(using, Iterable):
        package_stores = tuple(store[use_package] for use_package in using)

    if base_namespace and namespace != base_namespace:
        preconverters = chain(
            *(
                chain(package_store.get(namespace, {}).items(),
                      package_store["base"].items())
                for package_store in package_stores
            )
        )
    else:
        preconverters = chain(
            *(store[base_namespace].items() for package_store in package_stores)
        )

    for kind, transformer in reversed(tuple(preconverters)):
        if isinstance(item, kind):
            return transformer(item)

    if hasattr(item, "__iter__"):
        return list(item)

    raise Unconvertable(item)


json = partial(default_serializer, namespace="json")
bson = partial(default_serializer, namespace="bson")
msgpack = partial(default_serializer, namespace="msgpack")
