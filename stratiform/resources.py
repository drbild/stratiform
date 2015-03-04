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
from stratiform.utils import class_name, super_copy

def merge(*seqs):
    return [item for seq in seqs for item in seq]

class Resource(NameableAWSObject):
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)

    def __json__(self):
        return odict([
            ('Type', self.resource_type),
            ('Properties', super(Resource, self).__json__())
        ])

class Tag(AWSObject):
    @staticmethod
    def props():
        return [prop('Key'),
                prop('Value')]

    def __repr__(self):
        print ''
        print self.__dict__.keys()
        print ''
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

#### Public API ####
tag = tags = Tags

__all__ = ['tag', 'tags']
