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

from stratiform.base import AWSObject, prop
from stratiform.utils import Wrapper, snake_case
from stratiform.resources import Resource

################################ Custom Types ################################
class KeyStatus(Wrapper):
    pass
KeyStatus.active = KeyStatus('Active')
KeyStatus.inactive = KeyStatus('Inactive')

################################ AWS Property Types ################################
class Policies(AWSObject):
    @staticmethod
    def props():
        return [prop('PolicyDocument'),
                prop('PolicyCode')]

class LoginProfile(AWSObject):
    @staticmethod
    def props():
        return [prop('Password', basestring)]

################################ AWS Resource Types ################################
class AccessKey(Resource):
    resource_type = 'AWS::IAM::AccessKey'
    
    @staticmethod
    def props():
        return [prop('Serial', int),
                prop('Status', KeyStatus),
                prop('UserName')]

class Group(Resource):
    resource_type = 'AWS::IAM::Group'
    
    @staticmethod
    def props():
        return [prop('Path', basestring),
                prop('Policies')]

class InstanceProfile(Resource):
    resource_type = 'AWS::IAM::InstanceProfile'

    @staticmethod
    def props():
        return [prop('Path', basestring),
                prop('Roles')]

class Policy(Resource):
    resource_type = 'AWS::IAM::Policy'

    @staticmethod
    def props():
        return [prop('Groups'),
                prop('PolicyDocument'),
                prop('PolicyName'),
                prop('Roles'),
                prop('Users')]

class Role(Resource):
    resource_type = 'AWS::IAM::Role'

    @staticmethod
    def props():
        return [prop('AssumeRolePolicyDocument'),
                prop('Path'),
                prop('Policies')]

class User(Resource):
    resource_type = 'AWS::IAM::User'
    
    @staticmethod
    def props():
        return [prop('Path'),
                prop('Groups'),
                prop('LoginProfile', LoginProfile),
                prop('Policies')]

class UserToGroupAddition(Resource):
    resource_type = 'AWS::IAM::UserToGroupAddition'
    
    @staticmethod
    def props():
        return [prop('GroupName'),
                prop('Users')]

#### Public API ####
# Generate functional snake_cased form of constructors for public API
def __is_resource(obj):
    return issubclass(type(obj), type) and issubclass(obj, Resource)
constructors = {snake_case(name): obj for (name, obj) in globals().items() if __is_resource(obj)}
globals().update(constructors)

key_status   = KeyStatus
key_active   = KeyStatus.active
key_inactive = KeyStatus.inactive

policies      = Policies
login_profile = LoginProfile

__all__ = sorted(['key_status', 'key_active', 'key_inactive',
                  'policies', 'login_profile'] + \
                 constructors.keys())
