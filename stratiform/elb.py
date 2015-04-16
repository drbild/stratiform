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

################################ AWS Resource Types ################################
class LoadBalancer(Resource):
    resource_type = 'AWS::ElasticLoadBalancing::LoadBalancer'
    
    @staticmethod
    def props():
        return [prop('AccessLoggingPolicy'),
                prop('AppCookieStickinessPolicy'),
                prop('AvailabilityZone', AvailabilityZone),
                prop('ConnectionDrainingPolicy'),
                prop('ConnectionSettings'),
                prop('CrossZone'),
                prop('HealthCheck'),
                prop('Instances'),
                prop('LBCookieStickinessPolicy'),
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

__all__ = sorted(constructors.keys())
