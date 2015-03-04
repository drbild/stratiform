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

from stratiform.common import named_as_ref

class Join(object):
    """This intrinsic function appends a set of values into a single
    value, separated by the specified delimiter.

    """
    def __init__(self, delimiter, values):
        self.delimiter = delimiter
        self.values    = values

    def __json__(self):
        params = [
            named_as_ref(self.delimiter),
            [named_as_ref(v) for v in self.values]
        ]
        return {'Fn::Join' : params}

#### Public API ####
join        = Join

__all__ = ['ref']
