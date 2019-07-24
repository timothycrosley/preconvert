Preconvert
===================

[![PyPI version](https://badge.fury.io/py/preconvert.svg)](http://badge.fury.io/py/preconvert)

A Library to enable preconversion of any Python type into one that is easily serializable.

Preconvert provides a way to define conversions from more complex objects and datastructures into the base
types before serialization happens. This happens in a way that is independant of the eventual form of serialization,
allowing you to easily then serialize into multiple formats.

# Why?

Have you ever tried to `json.dumps` a data structure, only to be surprised when your DataClass throws an exception, or your namedtuple outputs as a list?
Preconvert was created to solve this problem across common serialization formats.


Before Preconvert:

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


my_store_inventory = [InventoryItem("beer", unit_price=0.0, quantity_on_hand=sys.maxsize),  InventoryItem("bacon", unit_price=2.5, quantity_on_hand=3)]
json.dumps(my_store_inventory)

>>> '[{"name": "beer", "unit_price": 0.0, "quantity_on_hand": 9223372036854775807}, {"name": "bacon", "unit_price": 2.5, "quantity_on_hand": 3}]'

:D
```

## Design goals:

- Enable conversion from complex to simple types independant of desired output format
- Provide built in conversion for common types that are not universally supported (dataclasses, namedtuple, etc...)
- Provide a way to build custom preconverts or override built-in preconverts
- Ability to build preconverts that are dependent on the destination format
- Easy utilization from existing projects
- Minimal overhead when utilized with common serialization formats

# How do I use this?

1. Download

`pip3 install preconvert`

2. Utilize

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

# How do I extend this?

Want to add preconversion to your own custom types? For OOP projects, one easy way to do this is to add a `__jsonifiable__` method to your object:

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
