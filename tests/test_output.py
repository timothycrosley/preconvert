import os
from datetime import datetime, timedelta

import pytest

import preconvert
from preconvert import converters
from collections import namedtuple
from decimal import Decimal
from .constants import BASE_DIRECTORY


def test_json():
    """Tests outputting a variety of Python data types to JSON using preconvert"""
    now = datetime.now()
    one_day = timedelta(days=1)
    test_data = {"text": "text", "datetime": now, "bytes": b"bytes", "delta": one_day}
    output = preconvert.output.json.dumps(test_data)
    assert "text" in output
    assert "bytes" in output
    assert str(one_day.total_seconds()) in output
    assert now.isoformat() in output

    class NewObject(object):
        pass

    test_data["non_serializable"] = NewObject()
    with pytest.raises(preconvert.exceptions.Unconvertable):
        preconvert.output.json.dumps(test_data)

    class NamedTupleObject(namedtuple("BaseTuple", ("name", "value"))):
        pass

    data = NamedTupleObject("name", "value")
    converted = preconvert.output.json.loads(preconvert.output.json.dumps(data))
    assert converted == {"name": "name", "value": "value"}

    data = set((1, 2, 3, 3))
    assert preconvert.output.json.loads(preconvert.output.json.dumps(data)) == [1, 2, 3]

    data = (number for number in range(1, 4))
    assert preconvert.output.json.loads(preconvert.output.json.dumps(data)) == [1, 2, 3]

    data = [Decimal(1.5), Decimal("155.23"), Decimal("1234.25")]
    assert preconvert.output.json.loads(preconvert.output.json.dumps(data)) == [
        "1.5",
        "155.23",
        "1234.25",
    ]

    assert preconvert.output.json.loads(preconvert.output.json.dumps(b"a")) == "a"

    class MyCrazyObject(object):
        pass

    @preconvert.converter(MyCrazyObject)
    def convert(instance):
        return "Like anyone could convert this"

    crazy_object_json = preconvert.output.json.loads(preconvert.output.json.dumps(MyCrazyObject()))
    assert crazy_object_json == "Like anyone could convert this"
    assert preconvert.output.json.loads(
        preconvert.output.json.dumps({"data": ["Τη γλώσσα μου έδωσαν ελληνική"]})
    ) == {"data": ["Τη γλώσσα μου έδωσαν ελληνική"]}
