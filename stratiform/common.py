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
from functools import partial

from stratiform.copyutils import super_copy
from stratiform.dispatchers import named_args

def class_name(obj):
    return obj.__class__.__name__

def named_as_ref(obj):
    if isinstance(obj, NameableAWSObject) and hasattr(obj, 'name'):
        return Ref(obj)
    else:
        return obj

def snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return super(JSONEncoder, self).default(obj)

class Property(object):
    def __init__(self, name, type=object, required=False, attr=None):
        self.name = name
        self.type = type
        self.required = required
        self.attr = attr or snake_case(name)

class AWSObject(object):
    """Super class for all AWS objects that can be expressed in a
    template.
    """

    @named_args
    def __init__(self, **kwargs):
        self.__set_attrs__(**kwargs)

    @named_args
    def __call__(self, **kwargs):
        result = copy(self)
        result.__set_attrs__(**kwargs)
        return result

    def __set_attrs__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if k not in self.__attrs__():
                err_msg = "%s() got unexpected keyword argument '%s'"
                raise TypeError(err_msg%(class_name(self), k))
            setattr(self, k, v)
 
    def __attrs__(self):
        return [p.attr for p in self.__props__()]

    def __named_args__(self):
        return self.__attrs__()

    def __props__(self):
        return self.props

    def __json__(self):
        data = odict()
        for p in self.__props__():
            if hasattr(self, p.attr):
                v = getattr(self, p.attr)
                data[p.name] = named_as_ref(v)
        return data

class NameableAWSObject(AWSObject):
    """Super class for all AWS objects that can be assigned a name.

    """
    def __attrs__(self):
        sattrs = super(NameableAWSObject, self).__attrs__()
        return ['name'] + sattrs

class Ref(AWSObject):
    props = [Property('referent', NameableAWSObject)]

    def __json__(self):
        return {'Ref' : self.referent.name}



#### Public API ####
ref  = Ref

prop = Property
required_prop = partial(prop, required=True)
optional_prop = partial(prop, required=False)

__all__ = ['ref', 'prop', 'required_prop', 'optional_prop']
