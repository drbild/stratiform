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

from common import NameableAWSObject
from common import required_prop as req_prop, optional_prop as opt_prop

class Parameter(NameableAWSObject):
    props = [req_prop('Type'),
             opt_prop('Description'),
             opt_prop('Default'),
             opt_prop('AllowedValues'),
             opt_prop('AllowedPattern'),
             opt_prop('ConstraintDescription'),
             opt_prop('MaxLength'),
             opt_prop('MinLength'),
             opt_prop('MaxValue'),
             opt_prop('MinValue'),
             opt_prop('NoEcho')]

class PseudoParameter(NameableAWSObject):
    props = []

#### Public API ####
parameter = Parameter

ACCOUNT_ID        = PseudoParameter('AWS::AccountId')
NOTIFICATION_ARNS = PseudoParameter('AWS::NotificationARNs')
NO_VALUE          = PseudoParameter('AWS::NoValue')
REGION            = PseudoParameter('AWS::Region')
STACK_ID          = PseudoParameter('AWS::StackId')
STACK_NAME        = PseudoParameter('AWS::StackName')

__all__ = ['parameter', 'ACCOUNT_ID', 'NOTIFICATION_ARNS', 'NO_VALUE',
           'REGION', 'STACK_ID', 'STACK_NAME']
