# JsonMixin

Automatic `to_json()` on your Python objects!

Note that class attributes, class methods, static methods, instance methods and properties will not appear in the `json` representation, only instance attributes.
This also works whether `slots` are defined or not.

```python
>>> from jsonmixin import JsonMixin
>>>
>>> class Titi(JsonMixin):
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
...     @classmethod
...     def clsmethod(cls):
...         pass
...     @staticmethod
...     def static():
...         pass

>>> l = Titi(1, '2')
>>>
>>> from pprint import pprint
>>> pprint(l.to_json())
{'a': 1, 'b': '2'}

```

