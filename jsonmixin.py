#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
to_json() for all your objects!

>>> class CustomDescriptor(object):
...     def __get__(self, obj, _):
...         return obj.a
...     def __set__(self, obj, value):
...         obj.a = value

>>> class Titi(JsonMixin):
...     __slots__ = ['a', 'b', 'c']
...     clsvars = 'test'
...     def __init__(self, a, b):
...         self.a = a
...         self.b = b
...     def method(self):
...         return self.a
...     @property
...     def prop(self):
...         return self.b
...     @prop.setter
...     def prop(self, b):
...         self.b = b
...     custom_desc = CustomDescriptor()
...     @classmethod
...     def clsmethod(cls):
...         pass
...     @staticmethod
...     def static():
...         pass

>>> l = Titi(a=1, b='2')
>>> l.a
1
>>> l.b
'2'
>>> l.method()
1
>>> l.prop
'2'
>>> l.prop = 'g'
>>> l.prop
'g'
>>> l.custom_desc
1
>>> l.custom_desc = 2
>>> l.clsmethod()
>>> Titi.static()
>>>
>>> from pprint import pprint
>>> pprint(l.to_json())
{'a': 2, 'b': 'g'}

"""

import inspect
import sys
PY3 = sys.version_info[0] >= 3


def _find_attrs(obj):
    """Iterate over all attributes of objects."""
    visited = set()

    if hasattr(obj, '__dict__'):
        for attr in obj.__dict__:
            if attr not in visited:
                yield attr
                visited.add(attr)

    for cls in reversed(inspect.getmro(obj.__class__)):
        if hasattr(cls, '__slots__'):
            for attr in cls.__slots__:
                if hasattr(obj, attr):
                    if attr not in visited:
                        yield attr
                        visited.add(attr)


def _to_json(obj):
    if not PY3 and isinstance(obj, unicode):
        return obj.encode('utf8')
    if isinstance(obj, (str, int, float, complex, bool, type(None))):
        return obj
    if isinstance(obj, (set, frozenset, list, tuple)):
        return [_to_json(e) for e in obj]
    if isinstance(obj, dict):
        return dict((k, _to_json(obj[k])) for k in obj)

    return dict((attr, _to_json(getattr(obj, attr)))
                for attr in _find_attrs(obj)
                if not attr.startswith('_'))


class JsonMixin(object):
    __slots__ = []

    def to_json(self):
        return _to_json(self)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
