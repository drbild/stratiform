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

from stratiform.common import snake_case
from stratiform.copyutils import super_copy

from stratiform.common import prop, required_prop as req_prop, optional_prop as opt_prop
from stratiform.resources import Resource, Tags

class CustomerGateway(Resource):
    resource_type = 'AWS::EC2::CustomerGateway'
    props = [req_prop('BgpAsn', int),
             req_prop('IpAddress', basestring),
             req_prop('Type', basestring),
             opt_prop('Tags', Tags)]

class DHCPOptions(Resource):
    resource_type = 'AWS::EC2::DHCPOptions'
    props = [opt_prop('DomainName', basestring),
             opt_prop('DomainNameServers', list),
             opt_prop('NetbiosNameServers', list),
             opt_prop('NetbiosNodeType', int),
             opt_prop('NtpServers', basestring),
             opt_prop('Tags', Tags)]

class EIP(Resource):
    resource_type = 'AWS::EC2::EIP'
    props = [opt_prop('Domain', basestring),
             opt_prop('InstanceId', basestring)]

class EIPAssociation(Resource):
    resource_type = 'AWS::EC2::EIPAssociation'
    props = [opt_prop('AllocationId', basestring),
             opt_prop('EIP', basestring),
             opt_prop('InstanceId', basestring),
             opt_prop('NetworkInterfaceId', basestring),
             opt_prop('PrivateIpAdress', basestring)]

class Instance(Resource):
    resource_type = 'AWS::EC2::Instance'
    props = [opt_prop('AvailabilityZone', basestring),
             opt_prop('BlockDeviceMappings', list),
             opt_prop('DisableApiTermination', bool),
             opt_prop('EbsOptimized', bool),
             opt_prop('IamInstanceProfile', basestring),
             req_prop('ImageId', basestring),
             opt_prop('InstanceInitiatedShutdownBehavior', basestring),
             opt_prop('InstanceType', basestring),
             opt_prop('KernelId', basestring),
             opt_prop('KeyName', basestring),
             opt_prop('Monitoring', bool),
             opt_prop('NetworkInterfaces', list),
             opt_prop('PlacementGroupName', basestring),
             opt_prop('PrivateIpAdress', basestring),
             opt_prop('RamdiskId', basestring),
             opt_prop('SecurityGroupIds', list),
             opt_prop('SecurityGroups', list),
             opt_prop('SourceDestCheck', bool),
             opt_prop('SubnetId', basestring),
             opt_prop('Tags', Tags),
             opt_prop('UserData', basestring),
             opt_prop('Volumes', list)]

class InternetGateway(Resource):
    resource_type = 'AWS::EC2::InternetGateway'
    props = [opt_prop('Tags', Tags)]

class NetworkAcl(Resource):
    resource_type = 'AWS::EC2::NetworkAcl'
    props = [req_prop('VpcId', basestring),
             opt_prop('Tags', Tags)]

    def entry(self, *args, **kwargs):
        result = copy(self)
        kwargs['network_acl_id'] = self
        result.siblings.append(network_acl_entry(*args, **kwargs))
        return result

    def ingress(self, *args, **kwargs):
        kwargs['egress'] = False
        return self.entry(*args, **kwargs)

    def egress(self, *args, **kwargs):
        kwargs['egress'] = True
        return self.entry(*args, **kwargs)

class NetworkAclEntry(Resource):
    resource_type = 'AWS::EC2::NetworkAclEntry'
    props = [req_prop('CidrBlock', basestring),
             req_prop('Egress', bool),
             opt_prop('Icmp', dict),
             req_prop('NetworkAclId', basestring),
             req_prop('PortRange', object),
             req_prop('Protocol', int),
             req_prop('RuleAction', object),
             req_prop('RuleNumber', int)]

class NetworkInterface(Resource):
    resource_type = 'AWS::EC2::NetworkInterface'
    props = [opt_prop('Description', basestring),
             opt_prop('GroupSet', list),
             opt_prop('PrivateIpAddress', basestring),
             opt_prop('PrivateIpAddresses', list),
             opt_prop('SecondaryPrivateIpAddressCount', int),
             opt_prop('SourceDestCheck', bool),
             req_prop('SubnetId', basestring),
             opt_prop('Tags', Tags)]

class NetworkInterfaceAttachment(Resource):
    resource_type = 'AWS::EC2::NetworkInterfaceAttachment'
    props = [opt_prop('DeleteOnTermination', bool),
             req_prop('DeviceIndex', int),
             req_prop('InstanceId', basestring),
             req_prop('NetworkInterfaceId', basestring)]

class Route(Resource):
    resource_type = 'AWS::EC2::Route'
    props = [req_prop('DestinationCidrBlock', basestring),
             opt_prop('GatewayId', basestring),
             opt_prop('InstanceId', basestring),
             opt_prop('NetworkInterfaceId', basestring),
             opt_prop('RouteTableId', basestring),
             opt_prop('VpcPeeringConnectionId', basestring)]

rroute = Route

class RouteTable(Resource):
    resource_type = 'AWS::EC2::RouteTable' 
    props = [req_prop('VpcId', basestring),
             opt_prop('Tags', Tags)]

    def __attrs__(self):
        sattrs = super(RouteTable, self).__attrs__()
        return sattrs + ['subnet']

    def __siblings__(self):
        siblings = super(RouteTable, self).__siblings__()
        siblings += self._subnet_siblings()
        return siblings

    @property
    def subnet(self):
        return self._subnet
    
    @subnet.setter
    def subnet(self, value):
        self._subnet = value

    def _subnet_siblings(self):
        if not hasattr(self, 'subnet'):
            return []
        association_name = ''.join([self._subnet.name, self.name, "Association"])
        association = SubnetRouteTableAssociation(association_name, subnet_id=self._subnet,
                                                  route_table_id=self)
        return [association]

    def route(self, *args, **kwargs):
        result = copy(self)
        kwargs['route_table_id'] = self
        result.siblings.append(rroute(*args, **kwargs))
        return result

class SecurityGroup(Resource):
    resource_type = 'AWS::EC2::SecurityGroup'
    props = [opt_prop('VpcId', basestring),
             req_prop('GroupDescription', basestring),
             opt_prop('SecurityGroupEgress', list),
             opt_prop('SecurityGroupIngress', list),
             opt_prop('Tags', Tags)]

    def __init__(self, *args, **kwargs):
        super(SecurityGroup, self).__init__(*args, **kwargs)
        self.rules = []

    def __copy__(self):
        result = super_copy(NetworkAcl, self)
        result = copy(result.rules)
        return result

    def egress(self, *args, **kwargs):
        result = copy(self)
        kwargs['group_id'] = self
        result.rules.append(security_group_egress(*args, **kwargs))
        return result

    def ingress(self, *args, **kwargs):
        result = copy(self)
        kwargs['group_id'] = self
        result.rules.append(security_group_ingress(*args, **kwargs))
        return result

class SecurityGroupEgress(Resource):
    resource_type = 'AWS::EC2::SecurityGroupEgress'
    props = [opt_prop('CidrIp', basestring),
             opt_prop('DestinationSecurityGroupId', basestring),
             req_prop('IpProtocol', basestring),
             req_prop('FromPort', int),
             req_prop('ToPort', int),
             req_prop('GroupId', basestring)]

class SecurityGroupIngress(Resource):
    resource_type = 'AWS::EC2::SecurityGroupIgress'
    props = [opt_prop('CidrIp', basestring),
             opt_prop('SourceSecurityGroupId', basestring),
             opt_prop('SourceSecurityGroupName', basestring),
             opt_prop('SourceSecurityGroupOwnerId', basestring),
             req_prop('IpProtocol', basestring),
             req_prop('FromPort', int),
             req_prop('ToPort', int),
             req_prop('GroupId', basestring),
             req_prop('GroupName', basestring)]

class Subnet(Resource):
    resource_type = 'AWS::EC2::Subnet'
    props = [opt_prop('AvailabilityZone', basestring),
             req_prop('CidrBlock', basestring),
             req_prop('VpcId', basestring),
             opt_prop('Tags', Tags)]

class SubnetNetworkAclAssociation(Resource):
    resource_type = 'AWS::EC2::SubnetNetworkAclAssociation'
    props = [req_prop('SubnetId', basestring),
             req_prop('NetworkAclId', basestring)]

class SubnetRouteTableAssociation(Resource):
    resource_type = 'AWS::EC2::SubnetRouteTableAssociation'
    props = [req_prop('RouteTableId', basestring),
             req_prop('SubnetId', basestring)]

class Volume(Resource):
    resource_type = 'AWS::EC2::Volume'
    props = [req_prop('AvailabilityZone', basestring),
             opt_prop('Encrypted', bool),
             opt_prop('Iops', int),
             opt_prop('Size', basestring),
             opt_prop('SnapshotId', basestring),
             opt_prop('Tags', Tags),
             opt_prop('VolumeType', basestring)]

class VolumeAttachment(Resource):
    resource_type = 'AWS::EC2::VolumeAttachment'
    props = [req_prop('Device', basestring),
             req_prop('InstanceId', basestring),
             req_prop('VolumeId', basestring)]

class VPC(Resource):
    resource_type = 'AWS::EC2::VPC'
    props = [req_prop('CidrBlock', basestring),
             opt_prop('EnableDnsSupport', bool),
             opt_prop('EnableDnsHostnames', bool),
             opt_prop('InstanceTenancy', basestring),
             opt_prop('Tags', Tags)]

    def __attrs__(self):
        sattrs = super(VPC, self).__attrs__()
        return sattrs + ['dhcp_options']

    def __siblings__(self):
        siblings = super(VPC, self).__siblings__()
        siblings += self._dhcp_options_association()
        return siblings

    @property
    def dhcp_options(self):
        return self._dhcp_options
    
    @dhcp_options.setter
    def dhcp_options(self, value):
        self._dhcp_options = value

    def _dhcp_options_association(self):
        if not hasattr(self, 'dhcp_options'):
            return []
        association_name = ''.join([self.name, self._dhcp_options.name, "Association"])
        association = VPCDHCPOptionsAssociation(association_name, vpc_id=self,
                                                dhcp_options_id=self._dhcp_options)
        return [association]

class VPCDHCPOptionsAssociation(Resource):
    resource_type = 'AWS::EC2::VPCDHCPOptionsAssociation'
    props = [req_prop('DhcpOptionsId', basestring),
             req_prop('VpcId', basestring)]

class VPCGatewayAttachment(Resource):
    resource_type = 'AWS::EC2::VPCGatewayAttachment'
    props = [req_prop('VpcId', basestring),
             opt_prop('InternetGatewayId', basestring),
             opt_prop('VpnGatewayId', basestring)]

class VPCPeeringConnection(Resource):
    resource_type = 'AWS::EC2::VPCPeeringConnection'
    props = [req_prop('PeerVpcId', basestring),
             req_prop('VpcId', basestring),
             opt_prop('Tags', Tags)]

# TODO: Add VPN* resource types

#### Public API ####

# Generate functional snake_cased form of constructors for public API
def __is_resource(obj):
    return type(obj) is type and issubclass(obj, Resource)
constructors = {snake_case(name): obj for (name, obj) in globals().items() if __is_resource(obj)}
globals().update(constructors)

__all__ = sorted([] + constructors.keys())
