"""This module handles the registration of preconverters"""
from collections import OrderedDict
from enum import Enum
from functools import partial
from typing import Any, Callable, Dict, Text, Union

from preconvert.exceptions import ExistingConverter

converters: Dict[Text, Dict[Text, Dict[Text, Callable]]] = {"preconvert": {"base": OrderedDict()}}


class AutoPackage(Enum):
    """Provides options for the automatic determination of a package name"""

    FUNCTION = 1
    PRECONVERT = 2
    FUNCTION_OR_PRECONVERT = 3


def converter(
    *kinds: Any,
    scope: Text = "base",
    store: Dict[Text, Dict[Text, Dict[Text, Callable]]] = converters,
    override: bool = False,
    package: Union[Text, AutoPackage] = AutoPackage.FUNCTION_OR_PRECONVERT,
) -> Callable:
    """A decorator that registers the wrapped function as a pre-converter for the provided types
       in the provided `store` data structure or a default global one.

       Returns the decorated function unchanged.
    """

    def register_converter(function):
        nonlocal package
        nonlocal scope

        if package == AutoPackage.FUNCTION_OR_PRECONVERT:
            package = getattr(function, "__package__", None) or "preconvert"
        if package == AutoPackage.FUNCTION:
            package = function.__package__
        elif package == AutoPackage.PRECONVERT:
            package = "preconvert"

        package = store.setdefault(package, {})
        scope = package.setdefault(scope, OrderedDict())

        if not override:
            for kind in kinds:
                if kind in scope:
                    raise ExistingConverter(kind, scope, function)

        for kind in kinds:  # we redo this loop simply to guard against partial application
            scope[kind] = function

        return function

    return register_converter


json = partial(converter, scope="json")
bson = partial(converter, scope="bson")
msgpack = partial(converter, scope="msgpack")
