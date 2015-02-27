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

from stratiform.base import named_as_ref

# Circular import
import stratiform.conditions

class Fn(object):
    """Base class for AWS intrinsic functions
    """
    pass

class Base64(Fn):
    """This intrinsic function returns the Base64 representation of the
    input string.

    """
    def __init__(self, value):
        self.value = value

    def __json__(self):
        return {'Fn::Base64': named_as_ref(self.value)}

class FindInMap(Fn):
    """This intrinsic function returns the value corresponding to key in
    a two-level map that is declared in the Mappings section.

    """
    def __init__(self, map_name, top_level_key, second_level_key):
        self.map_name         = map_name
        self.top_level_key    = top_level_key
        self.second_level_key = second_level_key

    def __json__(self):
        params = [self.map_name,
                  named_as_ref(self.top_level_key),
                  named_as_ref(self.second_level_key)]
        return {'Fn::FindInMap' : params}

class GetAtt(Fn):
    """This intrinsic function returns the value of an attribute from a
    resource in the template.

    """
    def __init__(self, resource, attribute):
        self.resource  = resource
        self.attribute = attribute

    def __json__(self):
        params = [self.resource, named_as_ref(self.attribute)]
        return {'Fn::GetAtt' : params}

class GetAZs(Fn):
    """This intrinsic function returns an array that lists Availability
    Zones for a specified region.

    """
    def __init__(self, region):
        self.region = region

    def __json__(self):
        return {'Fn::GetAZs' : named_as_ref(self.region)}

class Join(Fn):
    """This intrinsic function appends a set of values into a single
    value, separated by the specified delimiter.

    """
    def __init__(self, delimiter, values):
        self.delimiter = delimiter
        self.values    = values

    def __json__(self):
        params = [named_as_ref(self.delimiter),
                  [named_as_ref(v) for v in self.values]]
        return {'Fn::Join' : params}

class Select(Fn):
    """This intrinsic function returns a single object from a list of
    objects by index.

    """
    def __init__(self, index, objects):
        self.index = index
        self.objects = objects

    def __json__(self):
        params = [named_as_ref(self.index),
                  [named_as_ref(v) for v in self.values]]
        return {'Fn::Select' : params}

class ConditionFn(Fn):
    """Base class for condition functions
    """
    pass

def nacor(obj):
    return stratiform.conditions.named_as_cond(named_as_ref(obj))

class And(ConditionFn):
    """Returns true if all the specified conditions evaluate to true, or
    returns false if any one of the conditions evaluates to true.

    """
    def __init__(self, *conditions):
        self.conditions = conditions

    def __json__(self):
        params = [nacor(c) for c in self.conditions]
        return {'Fn::And' : params}

class Equals(ConditionFn):
    """Returns true if the two values are equal and false if they aren't.

    """
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __json__(self):
        params = [named_as_ref(self.lhs), named_as_ref(self.rhs)]
        return {'Fn::Equals' : params}

class If(ConditionFn):
    """Returns one value if the specified condition evaluates to true and
    another value if the specified condition evaluates to false.

    """
    def __init__(self, condition, true_value, false_value):
        self.condition = condition
        self.true_value = true_value
        self.false_value = false_value

    def __json__(self):
        name = self.condition.object_name
        params = [name,
                  named_as_ref(self.true_value),
                  named_as_ref(self.false_value)]
        return {'Fn::If' : params}

class Not(ConditionFn):
    """Returns true for a condition that evaluates to false and vice
    versa.

    """
    def __init__(self, condition):
        self.condition = condition

    def __json__(self):
        return {'Fn::Not' : [nacor(self.condition)]}

class Or(ConditionFn):
    """Returns true if any one of the specified conditions evalutes to
    true, or return false if all of the conditions evaluate to false.

    """
    def __init__(self, *conditions):
        self.conditions = conditions

    def __json__(self):
        params = [nacor(c) for c in self.conditions]
        return {'Fn::Or' : params}

#### Public API ####
base64      = Base64
find_in_map = FindInMap
get_att     = GetAtt
get_azs     = GetAZs
join        = Join
select      = Select
fn_and         = And
fn_equals      = Equals
fn_if          = If
fn_not         = Not
fn_or          = Or

__all__ = ['base64', 'find_in_map', 'get_att', 'get_azs', 'join',
           'select', 'fn_and', 'fn_equals', 'fn_if', 'fn_not',
           'fn_or']
