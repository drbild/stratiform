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

@wrapt.decorator
def named_args(func, self, args, kwargs):
    """A decorator that converts positional args to keyword args before
    dispatching the method. Positional args are paired with the
    supplied names in order.

    """
    names = self.__named_args__()
    if len(args) > len(names):
        err_msg = "%s() takes at most %d argument(s) (%d given)"
        raise TypeError(err_msg%(func.__name__, len(names), len(args)))
    for k, v in zip(names, args):
        if k in kwargs:
            err_msg = "%s() got multiple values for keyword argument '%s'"
            raise TypeError(err_msg%(func.__name__, k))
        kwargs[k] = v
    return func(**kwargs)
