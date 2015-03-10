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

import wrapt

from stratiform.utils import class_name

@wrapt.decorator
def named_args(func, self, args, kwargs):
    """A decorator that converts positional args to keyword args before
    dispatching the method. Positional args are paired with the
    supplied names in order.

    """
    names = self.__named_args__()
    if len(args) > len(names):
        msg = "%s() takes at most %d argument(s) (%d given)"
        raise TypeError(msg%(func.__name__, len(names), len(args)))
    for k, v in zip(names, args):
        if k in kwargs:
            msg = "%s() got multiple values for keyword argument '%s'"
            raise TypeError(msg%(func.__name__, k))
        kwargs[k] = v
    return func(**kwargs)

@wrapt.decorator
def typed_dispatch(func, self, args, kwargs):
    """A decorator that converts positional args to keyword args before
    dispatching the method. Positional args are assigned to names
    based on their types, not their positions.  Types and names are
    retrieved from the passed instance via the _arg_types(self) and
    _arg_names(self) instance methods.

    """
    types = self.arg_types()
    names = self.arg_names()
    if len(types) != len(names):
        msg = "%s must declare same number of types (%d given) and names (%d given) for dispatch"
        raise TypeError(msg%(class_name(self), len(types), len(names)))
    if len(args) > len(types):
        msg = "%s.%s() takes at most %d arguments(s) (%d given)"
        raise TypeError(msg%(class_name(func.im_self), func.__name__, len(types), len(args)))
    posargs = []
    for v in args:
        found_key = None
        for k, t in zip(names, types):
            if isinstance(v, t):
                if found_key != None:
                    msg = "%s() got ambigious argument. Matches both '%s' and '%s'"
                    raise TypeError(msg%(func.__name__, found_key, k))
                if k in kwargs:
                    msg = "%s() got multiple values for keyword argument '%s'"
                    raise TypeError(msg%(func.__name__, k))
                found_key = k
                kwargs[k] = v
        if found_key == None:
            msg = "%s.%s() got argument of unexpected type '%s'"
            raise TypeError(msg%(class_name(func.im_self), func.__name__, class_name(v)))
    return func(*posargs, **kwargs)
