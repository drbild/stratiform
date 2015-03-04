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

import json
from collections import OrderedDict as odict

from copy import copy
from stratiform.copyutils import super_copy, shallow_copy_attr

from stratiform.common import class_name, prop
from stratiform.common import AWSObject, JSONEncoder

from stratiform.types import *

from stratiform.outputs import Output
from stratiform.parameters import Parameter
from stratiform.resources import Resource, siblings

class Template(AWSObject):
    @staticmethod
    def props():
        return [prop('Description', basestring),
                prop('AWSTemplateFormatVersion', Version),
                prop('Parameters', list),
                prop('Mappings',   list),
                prop('Conditions', list),
                prop('Resources',  list),
                prop('Outputs',    list)]

    DEFAULT_VERSION = version("2010-09-09")

    def __init__(self, *args, **kwargs):
        super(Template, self).__init__(*args, **kwargs)

        if not hasattr(self, 'aws_template_format_version'):
            self.aws_template_format_version = Template.DEFAULT_VERSION

        self._ensure_odict_if_present('parameters')
        self._ensure_odict_if_present('mappings')
        self._ensure_odict_if_present('conditions')
        self._ensure_odict_if_present('resources')
        self._ensure_odict_if_present('outputs')

    def _ensure_odict_if_present(self, attr):
        """If the specified attribute is present, converts it to an
        OrderedDictionary.

        """
        if hasattr(self, attr):
            safe = odict(getattr(self, attr))
            setattr(self, attr, safe)

    def _ensure_present(self, attr):
        if not hasattr(self, attr):
            setattr(self, attr, odict())

    def __copy__(self):
        result = super_copy(Template, self)
        shallow_copy_attr(result, 'parameters')
        shallow_copy_attr(result, 'mappings')
        shallow_copy_attr(result, 'conditions')
        shallow_copy_attr(result, 'resources')
        shallow_copy_attr(result, 'outputs')
        return result

    def __str__(self):
        return self.to_json()

    def add_all(self, items):
        result = self
        for item in items:
            result = result.add(item, strict=False)
        return result

    def add(self, obj, name=None, strict=True):
        if isinstance(obj, Parameter):
            return self.parameter(obj, name)
#        if isinstance(obj, Mapping):
#            return self.mapping(obj, name)
#        if isinstance(obj, Condition):
#            return self.condition(obj, name)
        if isinstance(obj, Resource):
            return self.resource(obj, name)
        if isinstance(obj, Output):
            return self.output(obj, name)
        if strict:
            raise TypeError("Cannot object of type '%s' to template"%class_name(obj))
        else:
            return self

    def parameter(self, parameter, name=None):
        name = name or parameter.name
        result = copy(self)
        result._ensure_present('parameters')
        result.parameters[name] = parameter
        return result

    def mapping(self, mapping, name=None):
        name = name or mapping.name
        result = copy(self)
        result._ensure_present('mappings')
        result.mappings[name] = mapping
        return result

    def condition(self, condition, name=None):
        name = name or condition.name
        result = copy(self)
        result._ensure_present('conditions')
        result.conditions[name] = condition
        return result

    def resource(self, resource, name=None):
        result = copy(self)
        result._resource(resource, name)
        for resource in siblings(resource):
            result._resource(resource)
        return result

    def _resource(self, resource, name=None):
        name = name or resource.name
        self._ensure_present('resources')
        self.resources[name] = resource

    def output(self, output, name=None):
        name = name or output.name
        result = copy(self)
        result._ensure_present('outputs')
        result.outputs[name] = output
        return result

    def to_json(self):
        return json.dumps(self, cls=JSONEncoder,
                          indent=4, separators=(',', ': '))

#### Public API ####
template = Template

__all__ = ['template']
