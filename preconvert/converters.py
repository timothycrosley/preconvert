import base64
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum
from types import GeneratorType
from typing import Any, Collection, Dict, Mapping, NamedTuple, Union
from uuid import UUID

from preconvert import register
from preconvert.exceptions import Unconvertable

try:
    import dataclasses

    dataclasses_loaded = True
except ImportError:
    dataclasses_loaded = False

if dataclasses_loaded:

    @register.converter(object)
    def convert_data_class(instance):
        if dataclasses.is_dataclass(instance):
            return dataclasses.asdict(instance)
        else:
            raise Unconvertable(instance)


register.converter(Collection)(list)
register.converter(GeneratorType)(tuple)
register.converter(Mapping)(dict)
register.converter(Decimal, UUID)(str)


@register.converter(date, datetime)
def datetime_converter(item):
    return item.isoformat()


@register.converter(timedelta)
def time_delta_converter(item):
    return item.total_seconds()


@register.converter(Enum)
def use_value_attribute(item):
    return item.value


@register.converter(NamedTuple)
def convert_namedtuple(instance: Any) -> Union[Dict, tuple]:
    """Converts a tuple of type namedtuple to a dict.
       This isn't registered as injecting this via registration won't work because it will never be
       falling through to as tuples convert to list.

       if the tuple isn't a named one, it will return the tuple unchanged
    """
    if hasattr(instance, "_asdict"):
        return instance._asdict()

    return instance


@register.converter(bytes)
def byte_converter(item):
    try:
        return item.decode("utf8")
    except UnicodeDecodeError:
        return base64.b64encode(item)
