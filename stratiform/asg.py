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
from stratiform.common import AvailabilityZone, CIDR, DomainName, PortRange, IpAddress, IpProtocol
from stratiform.utils import Wrapper, ListWrapper, snake_case, super_copy
from stratiform.resources import Resource, merge

from stratiform import ec2

################################ Custom Types ################################
class AdjustmentType(Wrapper):
    pass
AdjustmentType.change_in_capacity = AdjustmentType('ChangeInCapacity')
AdjustmentType.exact_capacity = AdjustmentType('ExactCapacity')
AdjustmentType.percent_change_in_capacity = AdjustmentType('PercentChangeInCapacity')

class HealthCheckType(Wrapper):
    pass
HealthCheckType.ec2 = HealthCheckType('EC2')
HealthCheckType.elb = HealthCheckType('ELB')

class MetricAggregationType(Wrapper):
    pass
MetricAggregationType.minimum = MetricAggregationType('Minimum')
MetricAggregationType.maximum = MetricAggregationType('Maximum')
MetricAggregationType.average = MetricAggregationType('Average')

class PolicyType(Wrapper):
    pass
PolicyType.simple_scaling = PolicyType('SimpleScaling')
PolicyType.step_scaling = PolicyType('StepScaling')

################################ AWS Property Types ################################
class BlockDeviceMapping(AWSObject):
    @staticmethod
    def props():
        return [prop('DeviceName', basestring),
                prop('Ebs', EbsBlockDevice),
                prop('NoDevice', bool),
                prop('VirtualName', basestring)]

class EbsBlockDevice(AWSObject):
    @staticmethod
    def props():
        return [prop('DeleteOnTermination', bool),
                prop('Encrypted', bool),
                prop('Iops', int),
                prop('SnapshotId', basestring),
                prop('VolumeSize', int),
                prop('VolumeType', int)]

class MetricsCollection(AWSObject):
    @staticmethod
    def props():
        return [prop('Granularity', basestring),
                prop('Metrics')]

class NotificationConfigurations(AWSObject):
    @staticmethod
    def props():
        return [prop('NotificationTypes'),
                prop('TopicARN', basestring)]

class ScalingPolicyStepAdjustments(AWSObject):
    @staticmethod
    def props():
        return [prop('MetricIntervalLowerBound', float),
                prop('MetricIntervalUpperBound', float),
                prop('ScalingAdjustment', int)]

class AutoScalingTag(AWSObject):
    @staticmethod
    def props():
        return [prop('Key', basestring),
                prop('Value', basestring),
                prop('PropagateAtLaunch', bool)]

    @staticmethod
    def from_tag(tag, propagate_at_launch=False):
        return AutoScalingTag(key=tag.key, value=tag.value, propagate_at_launch=propagate_at_launch)

class AutoScalingTags(object):
    def __init__(self, *tags, **kwtags):
        kwtags = [AutoScalingTag(key=k,value=v,propagate_at_launch=p) for k, v, p in kwtags.iteritems()]
        self.tags = merge(tags, kwtags)

    def __add_(self, rhs):
        if rhs is None:
            return self
        if not isinstance(rhs, AutoScalingTags):
            raise TypeError("cannot merge 'AutoScalingTags' and '%s' objects"%class_name(rhs))
        return AutoScalingTags(*(self.tags + rhs.tags))

    def __json__(self):
        return self.tags

    @staticmethod
    def from_tags(tags, propagate_at_launch=False):
        mapped = [AutoScalingTag.from_tag(t, propagate_at_launch) for t in tags.tags]
        return AutoScalingTags(*mapped)

################################ AWS Resource Types ################################
class AutoScalingGroup(Resource):
    resource_type = 'AWS::AutoScaling::AutoScalingGroup'

    @staticmethod
    def props():
        return [prop('AvailabilityZones'),
                prop('Cooldown', basestring),
                prop('DesiredCapacity', basestring),
                prop('HealthCheckGracePeriod', int),
                prop('HealthCheckType', HealthCheckType),
                prop('InstanceId', ec2.Instance),
                prop('LaunchConfigurationName', LaunchConfiguration),
                prop('LoadBalancerNames'),
                prop('MaxSize', basestring),
                prop('MetricsCollection', MetricsCollection),
                prop('MinSize', basestring),
                prop('NotificationConfigurations', NotificationConfigurations),
                prop('PlacementGroup'),
                prop('Tags', AutoScalingTags),
                prop('TerminationPolicies'),
                prop('VPCZoneIdentifier')]

class LaunchConfiguration(Resource):
    resource_type = 'AWS::AutoScaling::LaunchConfiguration'
    
    @staticmethod
    def props():
        return [prop('AssociatePublicIpAddress', bool),
                prop('BlockDeviceMappings'),
                prop('ClassicLinkVPCId', ec2.VPC),
                prop('ClassicLinkVPCSecurityGroups'),
                prop('EbsOptimized', bool),
                prop('IamInstanceProfile'),
                prop('ImageId', ec2.ImageId),
                prop('InstanceId', ec2.Instance),
                prop('InstanceMonitoring', bool),
                prop('InstanceType'),
                prop('KernelId'),
                prop('KeyName'),
                prop('PlacementTenancy'),
                prop('RamDiskId'),
                prop('SecurityGroups'),
                prop('SpotPrice'),
                prop('UserData', basestring)]

class LifecycleHook(Resource):
    resource_type = 'AWS::AutoScaling::LifecycleHook'
    
    @staticmethod
    def props():
        return [prop('AutoScalingGroupName', AutoScalingGroup),
                prop('DefaultResult', basestring),
                prop('HeartbeatTimeout', int),
                prop('LifecycleTransititon', basestring),
                prop('NotificationMetadata', basestring),
                prop('NotificationTargetARN', basestring),
                prop('RoleARN', basestring)]

class ScalingPolicy(Resource):
    resource_type = 'AWS::AutoScaling::ScalingPolicy'
    
    @staticmethod
    def props():
        return [prop('AdjustmentType', AdjustmentType),
                prop('AutoScalingGroupName', AutoScalingGroup),
                prop('Cooldown', basestring),
                prop('EstimatedInstanceWarmup', int),
                prop('MetricAggregationType', MetricAggregationType),
                prop('MinAdjustmentMagnitude', int),
                prop('PolicyType', PolicyType),
                prop('ScalingAdjustment', int),
                prop('StepAdjustments')]

class ScheduledAction(Resource):
    resource_type = 'AWS::AWS::AutoScaling::ScheduleAction'
    
    @staticmethod
    def props():
        return [prop('AutoScalingGroupName', AutoScalingGroup),
                prop('DesiredCapacity', int),
                prop('EndTime'),
                prop('MaxSize', int),
                prop('MinSize', int),
                prop('Recurrence'),
                prop('StartTime')]

#### Public API ####
# Generate functional snake_cased form of constructors for public API
def __is_resource(obj):
    return issubclass(type(obj), type) and issubclass(obj, Resource)
constructors = {snake_case(name): obj for (name, obj) in globals().items() if __is_resource(obj)}
globals().update(constructors)

adjustment_type            = AdjustmentType
change_in_capacity         = AdjustmentType.change_in_capacity
exact_capacity             = AdjustmentType.exact_capacity
percent_change_in_capacity = AdjustmentType.percent_change_in_capacity


health_check_type = HealthCheckType
ec2_health_check  = HealthCheckType.ec2
elb_health_check  = HealthCheckType.elb

metric_aggregatin_type = MetricAggregationType
minimum                = MetricAggregationType.minimum
maximum                = MetricAggregationType.maximum
average                = MetricAggregationType.average

policy_type    = PolicyType
simple_scaling = PolicyType.simple_scaling
step_scaling   = PolicyType.step_scaling

block_device_mapping           = BlockDeviceMapping
ebs_block_device               = EbsBlockDevice
metrics_collection             = MetricsCollection
notification_configuration     = NotificationConfigurations
scaling_policy_step_adjustment = ScalingPolicyStepAdjustments
auto_scaling_tag               = AutoScalingTag
auto_scaling_tags              = AutoScalingTags
from_tag                       = AutoScalingTag.from_tag
from_tags                      = AutoScalingTags.from_tags

__all__ = sorted(['adjustment_type', 'change_in_capacity', 'exact_capacity', 'percent_change_in_capacity',
                  'health_check_type', 'ec2', 'elb',
                  'metric_aggregation_type', 'ec2', 'elb',
                  'policy_type', 'simple_scaling', 'step_scaling',
                  'block_device_mapping',
                  'ebs_block_device',
                  'metrics_collection',
                  'notification_configuration',
                  'scaling_policy_step_adjustment',
                  'auto_scaling_tag', 'auto_scaling_tags', 'from_tag', 'from_tags'] + \
                 constructors.keys())
