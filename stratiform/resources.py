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

from copy import copy
from collections import OrderedDict as odict

from stratiform.base import AWSObject, NameableAWSObject, prop
from stratiform.conditions import Condition, Conditionable
from stratiform.utils import class_name, super_copy, Wrapper

def merge(*seqs):
    return [item for seq in seqs for item in seq]

class Resource(Conditionable, NameableAWSObject):
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)

    def __attrs__(self):
        sattrs = super(Resource, self).__attrs__()
        return sattrs + ['deletion_policy']

    def arg_names(self):
        snames = super(Resource, self).arg_names()
        return snames + ['deletion_policy']

    def arg_types(self):
        stypes = super(Resource, self).arg_types()
        return stypes + [DeletionPolicy]

    def __json__(self):
        data = odict([
            ('Type', self.resource_type),
            ('Properties', NameableAWSObject.__json__(self))
        ])
        data.update(Conditionable.__json__(self))
        if hasattr(self, 'deletion_policy'):
            data['DeletionPolicy'] = self.deletion_policy
        return data

class Tag(AWSObject):
    @staticmethod
    def props():
        return [prop('Key'),
                prop('Value')]

    def __repr__(self):
        return "Tag(%s='%s')"%(self.key, self.value)

class Tags(object):
    def __init__(self, *tags, **kwtags):
        kwtags = [Tag(key=k,value=v) for k, v in kwtags.iteritems()]
        self.tags = merge(tags, kwtags)

    def __add__(self, rhs):
        if rhs is None:
            return self
        if not isinstance(rhs, Tags):
            raise TypeError("cannot merge 'Tags' and '%s' objects"%class_name(rhs))
        return Tags(*(self.tags + rhs.tags))

    def __json__(self):
        return self.tags

class DeletionPolicy(Wrapper):
    pass
DeletionPolicy.DELETE   = DeletionPolicy("Delete")
DeletionPolicy.RETAIN   = DeletionPolicy("Retain")
DeletionPolicy.SNAPSHOT = DeletionPolicy("Snapshot")

#### Public API ####
tag = tags = Tags
deletion_policy = DeletionPolicy

__all__ = ['tag', 'tags', 'deletion_policy']
