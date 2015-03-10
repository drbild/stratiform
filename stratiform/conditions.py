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

from stratiform.dispatchers import typed_dispatch
from stratiform.functions import ConditionFn

def named_as_cond(obj):
    if isinstance(obj, Condition) and hasattr(obj, 'object_name'):
        return {'Condition' : obj.object_name}
    else:
        return obj

class Condition(object):
    @typed_dispatch
    def __init__(self, object_name, func):
        self.object_name = object_name
        self.func = func

    @staticmethod
    def arg_names():
        return ('object_name', 'func')

    @staticmethod
    def arg_types():
        return (basestring, ConditionFn)

    def siblings(self):
        return []

    def __json__(self):
        return self.func

class Conditionable(object):
    """Mixin for AWSObject types that can accept a condition parameter.

    """
    def __attrs__(self):
        sattrs = super(Conditionable, self).__attrs__()
        return sattrs + ['condition']

    def arg_names(self):
        snames = super(Conditionable, self).arg_names()
        return snames + ['condition']

    def arg_types(self):
        stypes = super(Conditionable, self).arg_types()
        return stypes + [Condition]

    def __json__(self):
        if hasattr(self, 'condition'):
            return {'Condition' : self.condition.object_name}
        else:
            return {}

#### Public API ####
condition = Condition

__all__ = ['condition']
