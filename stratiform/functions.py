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

from collections import OrderedDict as odict
from copy import copy
from copyutils import super_copy
from dispatchers import named_args

#### Helper functions ####
def ref_or_raw(obj):
    if hasattr(obj, 'name'):
        return ref(obj)
    else:
        return obj

#### AWS intrinsic functions ####
class Ref(object):
    """This intrinsic function returns the value of the specified
    parameter or resource.

    """
    def __init__(self, obj):
        self.obj  = obj

    def __json__(self):
        return {'Ref' : self.obj.name}

class Base64(object):
    """This intrinsic function returns the Base64 representation of the
    input string.

    """
    def __init__(self, string):
        self.string = string

    def __json__(self):
        return {'Fn::Base64' : self.string}

class FindInMap(object):
    """This intrinsic function returns the value corresponding to keys in
    a two-level map that is declared in the Mappings section.

    """
    def __init__(self, mapping, top_level_key, second_level_key):
        self.mapping = mapping
        self.top_level_key = top_level_key
        self.second_level_key = second_level_key

    def __json__(self):
        params = [
            self.mapping.name,
            ref_or_raw(self.top_level_key),
            ref_or_raw(self.second_level_key)
        ]
        return {'Fn::FindInMap' : params}

class GetAtt(object):
    """This intrinsic function returns the value of an attribute from a
    resource in the template.

    """
    def __init__(self, obj, attribute):
        self.obj = obj
        self.attribute = attribute

    def __json__(self):
        params = [
            self.obj.name,
            self.attribute
        ]
        return {'Fn::GetAtt' : params}

class GetAZs(object):
    """This intrinsic function returns an array that lists Availability
    Zones for a specified region.

    """
    def __init__(self, region):
        self.region = region

    def __json__(self):
        return {'Fn::GetAZs' : ref_or_raw(self.region)}

class Join(object):
    """This intrinsic function appends a set of values into a single
    value, separated by the specified delimiter.

    """
    def __init__(self, delimiter, values):
        self.delimiter = delimiter
        self.values    = values

    def __json__(self):
        params = [
            ref_or_raw(self.delimiter),
            [ref_or_raw(v) for v in self.values]
        ]
        return {'Fn::Join' : params}

#### Public API ####
ref         = Ref
base64      = Base64
find_in_map = FindInMap
get_att     = GetAtt
get_azs     = GetAZs
join        = Join

__all__ = [ref, base64, find_in_map, get_att, get_azs, join]
