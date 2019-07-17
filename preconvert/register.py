"""This module handles the registration of preconverters"""
from functools import partial
from typing import Any, Callable, Dict, Text

from preconvert.exceptions import ExistingConverter

converters: Dict[Text, Dict[Text, Callable]] = {"base": {}}


def converter(
    *kinds: Any,
    scope: Text = "base",
    store: Dict[Text, Dict[Text, Callable]] = converters,
    override: bool = False
) -> Callable:
    """A decorator that registers the wrapped function as a pre-converter for the provided types
       in the provided `store` data structure or a default global one.

       Returns the decorated function unchanged.
    """

    def register_converter(function):
        if not override:
            for kind in kinds:
                if kind in store[scope]:
                    raise ExistingConverter(kind, store[scope], function)

        for kind in kinds:  # we redo this loop simply to guard against partial application
            store[scope][kind] = function

        return function

    return register_converter


json = partial(converter, scope="json")
bson = partial(converter, scope="bson")
msgpack = partial(converter, scope="msgpack")
