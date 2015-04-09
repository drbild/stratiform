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

from stratiform.base import NameableAWSObject, prop
from stratiform.utils import Wrapper

class Parameter(NameableAWSObject):

    class Type(Wrapper):
        pass

    Type.String             = Type('String')
    Type.Number             = Type('Number')
    Type.ListNumber         = Type('List<Number>')
    Type.CommaDelimitedList = Type('CommaDelimitedList')
    Type.KeyPair            = Type('AWS::EC2::KeyPair::KeyName')
    Type.SecurityGroup      = Type('AWS::EC2::SecurityGroup::Id')
    Type.Subnet             = Type('AWS::EC2::Subnet::Id')
    Type.Vpc                = Type('AWS::EC2::VPC::Id')
    Type.ListSecurityGroup  = Type('List<AWS::EC2::SecurityGroup::Id>')
    Type.ListSubnet         = Type('List<AWS::EC2::Subnet::Id>')
    Type.ListVpc            = Type('List<AWS::EC2::VPC::Id>')

    @staticmethod
    def props():
        return [prop('Type', Parameter.Type),
                prop('Description', basestring),
                prop('Default'),
                prop('AllowedValues'),
                prop('AllowedPattern'),
                prop('ConstraintDescription'),
                prop('MaxLength'),
                prop('MinLength'),
                prop('MaxValue'),
                prop('MinValue'),
                prop('NoEcho')]

def bind_type(type):
    def f(*args, **kwargs):
        return Parameter(*args, type=type, **kwargs)
    return f

class PseudoParameter(NameableAWSObject):
    @staticmethod
    def props():
        return []

#### Public API ####
parameter = Parameter

string_parameter               = bind_type(Parameter.Type.String)
number_parameter               = bind_type(Parameter.Type.Number)
list_number_parameter          = bind_type(Parameter.Type.ListNumber)
comma_delimited_list_parameter = bind_type(Parameter.Type.CommaDelimitedList)
key_pair_parameter             = bind_type(Parameter.Type.KeyPair)
security_group_parameter       = bind_type(Parameter.Type.SecurityGroup)
subnet_parameter               = bind_type(Parameter.Type.Subnet)
vpc_parameter                  = bind_type(Parameter.Type.Vpc)
list_security_group_parameter  = bind_type(Parameter.Type.ListSecurityGroup)
list_subnet_parameter          = bind_type(Parameter.Type.ListSubnet)
list_vpc_parameter             = bind_type(Parameter.Type.ListVpc)

AccountId        = PseudoParameter('AWS::AccountId')
NotificationArns = PseudoParameter('AWS::NotificationARNs')
NoValue          = PseudoParameter('AWS::NoValue')
Region           = PseudoParameter('AWS::Region')
StackId          = PseudoParameter('AWS::StackId')
StackName        = PseudoParameter('AWS::StackName')

__all__ = ['parameter'] + \
          ['string_parameter', 'number_parameter',
           'list_number_parameter', 'comma_delimited_list_parameter',
           'key_pair_parameter', 'security_group_parameter',
           'subnet_parameter', 'vpc_parameter',
           'list_security_group_parameter', 'list_subnet_parameter',
           'list_vpc_parameter'] + \
          ['AccountId', 'NotificationArns', 'NoValue', 'Region',
           'StackId', 'StackName']
