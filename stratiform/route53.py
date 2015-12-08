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
from stratiform.common import DomainName, IpAddress
from stratiform.utils import ListWrapper, Wrapper, snake_case
from stratiform.resources import Resource, Tags

################################ Custom Types ################################
class ContinentCode(Wrapper):
    pass

class CountryCode(Wrapper):
    pass

class SubdivisionCode(Wrapper):
    pass

class HostedZoneVPCs(ListWrapper):
    pass

################################ AWS Property Types ################################
class AliasTarget(AWSObject):
    @staticmethod
    def props():
        return [prop('DNSName', DomainName),
                prop('EvaluateTargetHealth', bool),
                prop('HostedZoneId', HostedZone)]

class RecordSetGeoLocation(AWSObject):
    @staticmethod
    def props():
        return [prop('ContinentCode', ContinentCode),
                prop('CountryCode', CountryCode),
                prop('SubdivisionCode', SubdivisionCode)]

class HealthCheckConfig(AWSObject):
    @staticmethod
    def props():
        return [prop('FailureThreshold'),
                prop('FullyQualifiedDomainName', DomainName),
                prop('IPAddress', IpAddress),
                prop('Port'),
                prop('RequestInterval'),
                prop('ResourcePath'),
                prop('SearchString'),
                prop('Type')]

class HostedZoneConfig(AWSObject):
    @staticmethod
    def props():
        return [prop('Comment')]

class HostedZoneVPC(AWSObject):
    @staticmethod
    def props():
        return [prop('VPCId', basestring),
                prop('VPCRegion', basestring)]

################################ AWS Resource Types ################################
class HealthCheck(Resource):
    resource_type = 'AWS::Route53::HealthCheck'

    @staticmethod
    def props():
        return [prop('HealthCheckConfig', HealthCheckConfig)]

class HostedZone(Resource):
    resource_type = 'AWS::Route53::HostedZone'

    @staticmethod
    def props():
        return [prop('Name', DomainName),
                prop('VPCs', HostedZoneVPCs, attr='vpcs'),
                prop('HostedZoneConfig', HostedZoneConfig),
                prop('HostedZoneTags', Tags)]

class RecordSet(Resource):
    resource_type = 'AWS::Route53::RecordSet'

    @staticmethod
    def props():
        return [prop('AliasTarget', AliasTarget),
                prop('Comment'),
                prop('Failover'),
                prop('GeoLocation', RecordSetGeoLocation),
                prop('HealthCheckId', HealthCheck),
                prop('HostedZoneId', HostedZone),
                prop('HostedZoneName', DomainName),
                prop('Name'),
                prop('Region'),
                prop('ResourceRecords'),
                prop('SetIdentifier'),
                prop('TTL'),
                prop('Type'),
                prop('Weight')]

class RecordSetGroup(Resource):
    resource_type = 'AWS::Route53::RecordSetGroup'

    @staticmethod
    def props():
        return [prop('HostedZoneId', HostedZone),
                prop('HosedZoneName', DomainName),
                prop('RecordsSets'),
                prop('Comment')]

#### Public API ####
# Generate functional snake_cased form of constructors for public API
def __is_resource(obj):
    return issubclass(type(obj), type) and issubclass(obj, Resource)
constructors = {snake_case(name): obj for (name, obj) in globals().items() if __is_resource(obj)}
globals().update(constructors)

continent_code   = ContinentCode
country_code     = CountryCode
subdivision_code = SubdivisionCode

hosted_zone_vpc  = HostedZoneVPC
hosted_zone_vpcs = HostedZoneVPCs

alias_target = AliasTarget
record_set_geo_location = RecordSetGeoLocation
health_check_config = HealthCheckConfig
hosted_zone_config = HostedZoneConfig

__all__ = sorted(['continent_code', 'country_code',
                  'subdivision_code', 'alias_target',
                  'record_set_geo_location',
                  'health_check_config',
                  'hosted_zone_config'] + \
                 constructors.keys())
