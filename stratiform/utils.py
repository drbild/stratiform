# Copyright 2015 David R. Bild
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import copy, json, re

class JSONEncoder(json.JSONEncoder):
    """A JSONEncoder that calls the __json__() method, if it exists, to
       obtain a serializable form of the object.

    """
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return super(JSONEncoder, self).default(obj)

class Wrapper(object):
    """Base class for wrapping a single object. This is used to refine
    the type of a wrapped object, while proxying the __str__() and
    __json__() through to the wrapped object.

    """
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __str__(self):
        return str(self.wrapped)

    def __json__(self):
        return self.wrapped

class ListWrapper(Wrapper):
    """Base class for wrapping a list of objects. This is used to refine
    the type of the list, while proxying the __str__() and
    __json__() through to the wrapped list.

    If multiple arguments are supplied to the constructor, they are
    merged into a single wrapped list.

    """
    def __init__(self, *args):
        wrapped = []
        if len(args) == 1 and isinstance(args[0], list):
            wrapped += args[0]
        else:
            wrapped = args
        super(ListWrapper, self).__init__(wrapped)

def class_name(obj):
    """Returns the class name of the specified object.

    """
    return obj.__class__.__name__

def snake_case(string):
    """Returns the snake_cased form of the specified string.

    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def camel_case(string):
    """Returns the CamelCased form of the specified string.

    """
    components = string.split('_')
    return "".join(x.title() for x in components)

def shallow_copy(obj):
    """Returns a standard shallow copy of the object.
    """
    cls = obj.__class__
    result = cls.__new__(cls)
    result.__dict__.update(obj.__dict__)
    return result

def super_copy(klass, obj):
    """Returns a copy of obj by invoking __copy__ on the super class, if
    it is defined. Otherwise, returns a standard shallow copy.

    """
    sup = super(klass, obj)
    if hasattr(sup, '__copy__'):
        return sup.__copy__()
    else:
        return shallow_copy(obj)

def shallow_copy_attr(instance, attr):
    if hasattr(instance, attr):
        orig = getattr(instance, attr)
        setattr(instance, attr, copy.copy(orig))

# API

__all__ = ['JSONEncoder, Wrapper, ListWrapper', 'class_name',
           'snake_case', 'camel_case', 'shallow_copy', 'super_copy',
           'shallow_copy_attr']
