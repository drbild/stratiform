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

from stratiform.base import AWSObject, prop
from stratiform.common import AvailabilityZone
from stratiform.utils import snake_case

from stratiform.resources import Resource, Tags

################################ AWS Property Types ################################
class Attribute(AWSObject):
    @staticmethod
    def props():
        return [prop('Name', basestring),
                prop('Value', basestring)]

class AccessLoggingPolicy(AWSObject):
    @staticmethod
    def props():
        return [prop('EmitInterval', int),
                prop('Enabled', bool),
                prop('S3BucketName', basestring),
                prop('S3BucketPrefix', basestring)]

class AppCookieStickinessPolicy(AWSObject):
    @staticmethod
    def props():
        return [prop('CookieName', basestring),
                prop('PolicyName', basestring)]

class ConnectionDrainingPolicy(AWSObject):
    @staticmethod
    def props():
        return [prop('Enabled', boolean),
                prop('Timeout', int)]

class ConnectionSettings(AWSObject):
    @staticmethod
    def props():
        return [prop('IdleTimeout', int)]

class HealthCheck(AWSObject):
    @staticmethod
    def props():
        return [prop('HealthyThreshold', basestring),
                prop('Interval', basestring),
                prop('Target', basestring),
                prop('Timeout', basestring),
                prop('UnhealthyThreshold', basestring)]

class LBCookieStickinessPolicy(AWSObject):
    @staticmethod
    def props():
        return [prop('CookieExpirationPeriod', basestring),
                prop('PolicyName', basestring)]

class Listener(AWSObject):
    @staticmethod
    def props():
        return [prop('InstancePort', basestring),
                prop('InstanceProtocol', basestring),
                prop('LoadBalancerPort', basestring),
                prop('PolicyNames', basestring),
                prop('Protocol', basestring),
                prop('SSLCertificateId', basestring)]

class Policy(AWSObject):
    @staticmethod
    def props():
        return [prop('Attributes'),
                prop('InstancePorts'),
                prop('LoadBalancerPorts'),
                prop('PolicyName', basestring),
                prop('PolicyType', basestring)]

################################ AWS Resource Types ################################
class LoadBalancer(Resource):
    resource_type = 'AWS::ElasticLoadBalancing::LoadBalancer'
    
    @staticmethod
    def props():
        return [prop('AccessLoggingPolicy', AccessLoggingPolicy),
                prop('AppCookieStickinessPolicy', AppCookieStickinessPolicy),
                prop('AvailabilityZone', AvailabilityZone),
                prop('ConnectionDrainingPolicy', ConnectionDrainingPolicy),
                prop('ConnectionSettings', ConnectionSettings),
                prop('CrossZone'),
                prop('HealthCheck', HealthCheck),
                prop('Instances'),
                prop('LBCookieStickinessPolicy', LBCookieStickinessPolicy),
                prop('LoadBalancerName'),
                prop('Listeners'),
                prop('Policies'),
                prop('Scheme'),
                prop('SecurityGroups'),
                prop('Subnets'),
                prop('Tags', Tags)]

#### Public API ####
# Generate functional snake_cased form of constructors for public API
def __is_resource(obj):
    return issubclass(type(obj), type) and issubclass(obj, Resource)
constructors = {snake_case(name): obj for (name, obj) in globals().items() if __is_resource(obj)}
globals().update(constructors)

def ssl_attribute(name):
    return Attribute(name=name, value='true')

__all__ = sorted([ssl_attribute] + constructors.keys())
