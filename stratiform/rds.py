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
from stratiform.common import AvailabilityZone, CIDR
from stratiform.utils import snake_case

from stratiform.resources import Resource, Tags

################################ AWS Property Types ################################
class RDSSecurityGroupRule(AWSObject):
    @staticmethod
    def props():
        return [prop('CIDRIP', CIDR),
                prop('EC2SecurityGroupId', SecurityGroup),
                prop('EC2SecurityGroupName', basestring),
                prop('EC2SecurityGroupOwnerId', basestring)]

################################ AWS Resource Types ################################
class DBInstance(Resource):
    resource_type = 'AWS::RDS::DBInstance'

    @staticmethod
    def props():
        return [prop('AllocatedStorage', int),
                prop('AllowMajorVersionUpgrade', bool),
                prop('AutoMinorVersionUpgrade', bool),
                prop('AvailabilityZone', AvailabilityZone),
                prop('BackupRetentionPeriod', int),
                prop('CharacterSetName'),
                prop('DBClusterIdentifier'),
                prop('DBInstanceClass'),
                prop('DBInstanceIdentifier'),
                prop('DBName'),
                prop('DBParameterGroupName'),
                prop('DBSecurityGroups'),
                prop('DBSnapshotIdentifier'),
                prop('DBSubnetGroupName',),
                prop('Engine'),
                prop('EngineVersion'),
                prop('Iops', int),
                prop('KmsKeyId'),
                prop('LicenseModel'),
                prop('MasterUsername'),
                prop('MasterUserPassword'),
                prop('MultiAZ', bool),
                prop('OptionGroupName'),
                prop('Port', int),
                prop('PreferredBackupWindow'),
                prop('PreferredMaintenanceWindow'),
                prop('PubliclyAccessible', bool),
                prop('SourceDBInstanceIdentifier'),
                prop('StorageEncrypted', bool),
                prop('StorageType'),
                prop('Tags', Tags),
                prop('VPCSecurityGroups')]

class DBParameterGroup(Resource):
    resource_type = 'AWS::RDS::DBParameterGroup'
    
    @staticmethod
    def props():
        return [prop('Description', basestring),
                prop('Family', basestring),
                prop('Parameters', dict),
                prop('Tags', Tags)]

class DBSubnetGroup(Resource):
    resource_type = 'AWS::RDS::DBSubnetGroup'
    
    @staticmethod
    def props():
        return [prop('DBSubnetGroupDescription', basestring),
                prop('SubnetIds'),
                prop('Tags', Tags)]

class DBSecurityGroup(Resource):
    resource_type = 'AWS::RDS::DBSecurityGroup'

    @staticmethod
    def props():
        return [prop('EC2VpcId', VPC),
                prop('DBSecurityGroupIngress', RDSSecurityGroupRule),
                prop('GroupDescription', basestring),
                prop('Tags', Tags)]

class DBSecurityGroupIngress(Resource):
    resource_type = 'AWS::RDS::DBSecurityGroupIngress'

    @staticmethod
    def props():
        return [prop('CIDRIP', CIDR),
                prop('DBSecurityGroupName', basestring),
                prop('EC2SecurityGroupId', SecurityGroup),
                prop('EC2SecurityGroupName', basestring),
                prop('EC2SecurityGroupOwnerId', basestring)]

#### Public API ####
# Generate functional snake_cased form of constructors for public API
def __is_resource(obj):
    return issubclass(type(obj), type) and issubclass(obj, Resource)
constructors = {snake_case(name): obj for (name, obj) in globals().items() if __is_resource(obj)}
globals().update(constructors)

rds_security_group_rule = RDSSecurityGroupRule

__all__ = sorted(['rds_security_group_rule'] + \
                 constructors.keys())
