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

## Design goals:

- Enable conversion from complex to simple types independant of desired output format
- Provide built in conversion for common types that are not universally supported (dataclasses, namedtuple, etc...)
- Provide a way to build custom preconverters or override built-in preconverters
- Ability to build preconverters that are dependent on the destination format
- Easy utilization from existing projects

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

my_serializer.dumps(default=preconvert.unserializable)
```

# How do I extend this?

Want to add preconversion to your own custom types? For OOP projects, one easy way to do this is to add a `__native_types__` method to your object:

```python
class MyCustomClass(object):
    def __init__(self, first_name, children=()):
        self.first_name = first_name
        self.children = children

    def __native_types__(self)
        return {'first': self.first_name, 'children': children}
```

For other entities, such as objects you do not control, you can register a new preconverter using the `preconverter.converter` decorator:

```python
import preconverter


@preconverter.converter(SomeFrameworkObject)
def convert_framework_object(instance):
    return {'name': instance.name}
```

You can also, optionally, specify preconversions per an intended serialization format:

```python
import preconverter


@preconverter.json(SomeFrameworkObject)
def convert_framework_object(instance):
    return {'json': {'name': instance.name}}


@preconverter.msgpack(SomeFrameworkObject)
def convert_framework_object(instance):
    return ['name', instance.name]
```
