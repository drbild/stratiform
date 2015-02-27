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

import json, re

from collections import OrderedDict as odict
from copy import copy

from stratiform.utils import class_name, snake_case, super_copy
from stratiform.dispatchers import typed_dispatch

def named_as_ref(obj):
    if isinstance(obj, NameableAWSObject) and hasattr(obj, 'object_name'):
        return Ref(obj)
    else:
        return obj

def unique_attr(seq, attr):
    """Filters out objects with a duplicate attribute value
    """
    result = []
    seen = set()
    for s in seq:
        a = getattr(s, attr)
        if a not in seen:
            seen.add(a)
            result.append(s)
    return result

class Property(object):
    def __init__(self, name, type=None, attr=None, func=None, default=None):
        self.name = name
        self.type = type
        self.attr = attr or snake_case(name)
        self.func = func or (lambda x: x)
        self.default= default

    def __repr__(self):
        return "Property(%s, %r, %r, %r"%(self.name, self.type, self.attr, self.func)

class AWSObjectType(type):
    def __getattr__(cls, key):
        for p in cls.props():
            if key == p.type.__name__:
                return p.type
        raise AttributeError(key)

class AWSObject(object):
    """Super class for all AWS objects that can be expressed in a
    template.
    """

    __metaclass__ = AWSObjectType

    @typed_dispatch
    def __init__(self, **kwargs):
        self.__set_attrs__(**kwargs)
        self._siblings = []

    @typed_dispatch
    def __call__(self, **kwargs):
        result = copy(self)
        result.__set_attrs__(**kwargs)
        return result

    def __copy__(self):
        result = super_copy(AWSObject, self)
        result._siblings = copy(result._siblings)
        return result

    def __set_attrs__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if k not in self.__attrs__():
                err_msg = "%s() got unexpected keyword argument '%s'"
                raise TypeError(err_msg%(class_name(self), k))
            setattr(self, k, v)
 
    def __attrs__(self):
        unique = unique_attr(self.__props__(), 'attr')
        return [u.attr for u in unique]

    def arg_names(self):
        unique = unique_attr(self.__props__(), 'attr')
        unique = filter(lambda p: p.type != None, unique)
        return [u.attr for u in unique]

    def arg_types(self):
        unique = unique_attr(self.__props__(), 'attr')
        unique = filter(lambda p: p.type != None, unique)
        return [u.type for u in unique]

    def siblings(self):
        return self._siblings

    def __props__(self):
        return self.props()

    def __json__(self):
        data = odict()
        for p in self.__props__():
            if hasattr(self, p.attr):
                v = p.func(getattr(self, p.attr))
                data[p.name] = named_as_ref(v)
            elif p.default is not None:
                v = p.default
                data[p.name] = named_as_ref(p.default)
        return data

class NameableAWSObject(AWSObject):
    """Super class for all AWS objects that can be assigned a name.

    """
    def __init__(self, *args, **kwargs):
        object_name, args = NameableAWSObject.__parse_args(args)
        super(NameableAWSObject, self).__init__(*args, **kwargs)
        if object_name:
            self.object_name = object_name

    def __call__(self, *args, **kwargs):
        object_name, args = NameableAWSObject.__parse_args(args)
        result = super(NameableAWSObject, self).__call__(*args, **kwargs)
        if object_name:
            result.object_name = object_name
        return result
    
    @staticmethod
    def __parse_args(args):
        object_name = None
        if len(args) >= 1 and isinstance(args[0], basestring):
            object_name, args = args[0], args[1:]
        return object_name, args

    def __attrs__(self):
        sattrs = super(NameableAWSObject, self).__attrs__()
        return ['object_name'] + sattrs

class Ref(AWSObject):
    @staticmethod
    def props():
        return [Property('Ref', NameableAWSObject, func='object_name')]

    def __json__(self):
        return {'Ref' : self.ref.object_name}

#### Public API ####
ref  = Ref
prop = Property

__all__ = ['ref', 'prop']
