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

class Mapping(object):
    @typed_dispatch
    def __init__(self, name, mapping):
        self.name    = name
        self.mapping = mapping

    @staticmethod
    def arg_names():
        return ('name', 'mapping')

    @staticmethod
    def arg_types():
        return (basestring, dict)

    def __json__(self):
        return {self.name : self.mapping}

#### Public API ####
mapping = Mapping

__all__ = ['mapping']
