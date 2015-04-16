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

import copy, json
from collections import OrderedDict as odict

from stratiform.utils import JSONEncoder, Wrapper, class_name, super_copy
from stratiform.base import AWSObject, prop

from stratiform.parameters import Parameter
from stratiform.mappings   import Mapping
from stratiform.conditions import Condition
from stratiform.resources  import Resource
from stratiform.outputs    import Output

class Version(Wrapper):
    pass
Version.DEFAULT = Version("2010-09-09")

class Template(AWSObject):
    @staticmethod
    def props():
        return [prop('Description', basestring),
                prop('AWSTemplateFormatVersion', Version, default=Version.DEFAULT),
                prop('Parameters', odict),
                prop('Mappings',   odict),
                prop('Conditions', odict),
                prop('Resources',  odict),
                prop('Outputs',    odict)]

    __collections = ['parameters', 'mappings', 'conditions',
                     'resources', 'outputs']

    def __init__(self, *args, **kwargs):
        for attr in Template.__collections:
            kwargs.setdefault(attr, odict())
        super(Template, self).__init__(*args, **kwargs)

    def __copy__(self):
        result = super_copy(Template, self)
        for attr in Template.__collections:
            orig = getattr(result, attr)
            setattr(result, attr, copy.copy(orig))
        return result

    def __str__(self):
        return self.to_json()

    def __setattr__(self, k, v):
        try:
            v = v(k)
            self.add(v)
        except TypeError as e:
            pass
        super(Template, self).__setattr__(k, v)

    def add(self, *items):
        self.__add(*items)

    def __add(self, *items):
        for item in items:
            coll = self.__collection_for(item)
            coll[item.object_name] = item
            self.__add(*item.siblings())

    def __collection_for(self, item):
        if isinstance(item, Parameter):
            return self.parameters
        elif isinstance(item, Mapping):
            return self.mappings
        elif isinstance(item, Condition):
            return self.conditions
        elif isinstance(item, Resource):
            return self.resources
        elif isinstance(item, Output):
            return self.outputs
        else:
            msg = "Argument of type '%s' is valid in template"
            raise TypeError(msg%type(item))

    def resource(self, resource, name=None):
        self._resource(resource, name)
        for resource in siblings(resource):
            self._resource(resource)

    def _resource(self, resource, name=None):
        name = name or resource.object_name
        self._ensure_present('resources')
        self.resources[name] = resource

    def output(self, output, name=None):
        name = name or output.object_name
        self._ensure_present('outputs')
        self.outputs[name] = output

    def to_json(self, indent=2):
        return json.dumps(self, cls=JSONEncoder, indent=indent, separators=(',', ': '))

#### Public API ####
template = Template
version  = Version

__all__ = ['template', 'version']
