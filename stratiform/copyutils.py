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
        setattr(instance, attr, copy(orig))
