[![preconvert - Supercharge Your Serializers](https://raw.github.com/timothycrosley/preconvert/master/art/logo_large.png)](https://timothycrosley.github.io/preconvert/)
===================

[![PyPI version](https://badge.fury.io/py/preconvert.svg)](http://badge.fury.io/py/preconvert)
[![Build Status](https://travis-ci.org/timothycrosley/preconvert.svg?branch=master)](https://travis-ci.org/timothycrosley/preconvert)
[![codecov](https://codecov.io/gh/timothycrosley/preconvert/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/preconvert)
[![Gitter](https://badges.gitter.im/preconvert/community.svg)](https://gitter.im/preconvert/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/hug/)
[![Downloads](https://pepy.tech/badge/preconvert)](https://pepy.tech/project/preconvert)

_________________

[Read Latest Documentation](https://timothycrosley.github.io/preconvert/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/preconvert/)
_________________

Preconvert is a library that extends existing serializiers (json, simplejson, bson, msgpack, ..) to be capable of converting *all* the types you use.
It accomplishes this by efficiently preconverting just the types the serializers aren't aware of (things like dataclasses and namedtuples) into basic built-in types that all
serializers can understand. It then provides a mechanism for you to build custom preconverters, and preconvert_plugins that automatically take effect when installed via pip.

## Quickstart

1. Install preconvert using pip:

        pip3 install preconvert

2. Replace existing json (or other serialization library) with preconvert equivalent:

        from preconvert.output import simplejson as json

        ...

        json.dumps(MY_COMPLEX_OBJECT_WITH_DATA_CLASSSES)

4. Define preconverters for any custom types, even if they aren't under your control:

        import numpy
        from preconvert import json


        class Employee:

            def __init__(self, first_name, last_name):
                self.first_name = first_name
                self.last_name = last_name

            def __preconvert__(self):
                return {'name': {'first': self.first_name, 'last': self.last_name}}


        @preconvert.converter(numpy.integer)
        def numpy_integer_to_python_int(numpy_int):
            return int(numpy_int)


        json.dumps({
            'employee': Employee('Timothy', 'Crosley'),
            'height_inches': numpy.int_(73)
        })

3. Enjoy a more comprehensive and configurable serializer!

## Why?

Have you ever tried to `json.dumps` a data structure, only to be surprised when your DataClass throws an exception, or your namedtuple outputs as a list?
Preconvert was created to solve this problem across common serialization formats.


Before preconvert:

```python
import sys
import json
from dataclasses import dataclass


@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand


my_store_inventory = [InventoryItem("beer", unit_price=0.0, quantity_on_hand=sys.maxsize),  InventoryItem("bacon", unit_price=2.5, quantity_on_hand=3)]
json.dumps(my_store_inventory)

output >>>

    177
    178
--> 179         raise TypeError(f'Object of type {o.__class__.__name__} '
    180                         f'is not JSON serializable')
    181

TypeError: Object of type InventoryItem is not JSON serializable

D:
```

After preconvert:

```python
import sys
import json
from preconvert.output import json


@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand


my_store_inventory = [
    InventoryItem("beer", unit_price=0.0, quantity_on_hand=sys.maxsize),
    InventoryItem("bacon", unit_price=2.5, quantity_on_hand=3)
]
json.dumps(my_store_inventory)

>>> [
        {
            "name": "beer",
            "unit_price": 0.0,
            "quantity_on_hand": 9223372036854775807
        },
        {
            "name": "bacon",
            "unit_price": 2.5,
            "quantity_on_hand": 3
        }
    ]

:D
```

## Design goals:

<<<<<<< HEAD
- Easy utilization from existing projects
- Enable conversion from complex to simple types independant of desired output format
- Provide built in conversion for common types that are not universally supported (dataclasses, namedtuple, etc...)
=======
- Enable conversion from complex to simple types independent of desired output format
- Provide built-in conversion for common types that are not universally supported (dataclasses, namedtuple, etc...)
>>>>>>> 31e62dbf18a895e72e201ca4c80a701e81d66dbf
- Provide a way to build custom preconverts or override built-in preconverts
- Ability to build preconverts that are dependent on the destination format
- Minimal overhead when utilized with common serialization formats

## How do I use this?

If your project uses one of our built-in supported serializers (json, msgpak, bson)
you can simply replace your existing serializer import with a preconvert one:

`from preconvert.outputs import json`

OR

`from preconvert.outputs import simplejson as json`

OR

`from preconvert.outputs import msgpack`

OR

`from preconvert.outputs import bson`

If not you can inject preconvert before usage of any other serializers, often by setting a `default` or `on_onknown` parameter:

```
import preconvert
import my_serializer

my_serializer.dumps(default=preconvert.default_serializable)
```

## How do I extend this?

Want to add preconversion to your own custom types? For OOP projects, one easy way to do this is to add a `__preconvert__` method to your object:

```python
class MyCustomClass(object):
    def __init__(self, first_name, children=()):
        self.first_name = first_name
        self.children = children

    def __jsonifiable__(self)
        return {'first': self.first_name, 'children': children}
```

For other entities, such as objects you do not control, you can register a new preconvert using the `preconvert.converter` decorator:

```python
import preconvert


@preconvert.converter(SomeFrameworkObject)
def convert_framework_object(instance):
    return {'name': instance.name}
```

You can also, optionally, specify preconversions per an intended serialization format:

```python
import preconvert


@preconvert.json(SomeFrameworkObject)
def convert_framework_object(instance):
    return {'json': {'name': instance.name}}


@preconvert.msgpack(SomeFrameworkObject)
def convert_framework_object(instance):
    return ['name', instance.name]
```

Finally, you can resister any modules that contain converters to package 'preconvert.converters' entrypoints, and they will take effect automatically as long as the package that contains them is installed.
See the [preconvert_numpy](https://github.com/timothycrosley/preconvert_numpy/blob/master/pyproject.toml#L28) for an example of how this works.
