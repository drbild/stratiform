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

from stratiform.utils import Wrapper
from stratiform.utils import snake_case, super_copy

from stratiform.common import NameableAWSObject
from stratiform.constants import aws_provided_dns
from stratiform.types import *

from stratiform.common import prop
from stratiform.resources import Resource, Tags

class CustomerGateway(Resource):
    resource_type = 'AWS::EC2::CustomerGateway'

    def props():
        return [prop('BgpAsn'),
                prop('IpAddress', IpAddress),
                prop('Type'),
                prop('Tags', Tags)]

class DHCPOptions(Resource):
    resource_type = 'AWS::EC2::DHCPOptions'

    @staticmethod
    def props():
        return [prop('DomainName', DomainName),
                prop('DomainNameServers', DomainNameServers, default=aws_provided_dns),
                prop('NetbiosNameServers'),
                prop('NetbiosNodeType'),
                prop('NtpServers'),
                prop('Tags', Tags)]

class EIP(Resource):
    resource_type = 'AWS::EC2::EIP'

    @staticmethod
    def props():
        return [prop('Domain'),
                prop('InstanceId', Instance)]

class EIPAssociation(Resource):
    resource_type = 'AWS::EC2::EIPAssociation'

    @staticmethod
    def props():
        return [prop('AllocationId'),
                prop('EIP', EIP),
                prop('InstanceId', Instance),
                prop('NetworkInterfaceId', NetworkInterface),
                prop('PrivateIpAddress', IpAddress)]

class Instance(Resource):
    resource_type = 'AWS::EC2::Instance'

    @staticmethod
    def props():
        return [prop('AvailabilityZone', AvailiabilityZone),
                prop('BlockDeviceMappings'),
                prop('DisableApiTermination'),
                prop('EbsOptimized'),
                prop('IamInstanceProfile'),
                prop('ImageId', ImageId),
                prop('InstanceInitiatedShutdownBehavior'),
                prop('InstanceType'),
                prop('KernelId'),
                prop('KeyName'),
                prop('Monitoring'),
                prop('NetworkInterfaces'),
                prop('PlacementGroupName'),
                prop('PrivateIpAdress', IpAddress),
                prop('RamdiskId'),
                prop('SecurityGroupIds'),
                prop('SecurityGroups'),
                prop('SourceDestCheck'),
                prop('SubnetId', Subnet),
                prop('Tags', Tags),
                prop('UserData'),
                prop('Volumes')]

class InternetGateway(Resource):
    resource_type = 'AWS::EC2::InternetGateway'

    @staticmethod
    def props():
        return [prop('Tags', Tags)]

    def __attrs__(self):
        sattrs = super(InternetGateway, self).__attrs__()
        return sattrs + ['vpc']

    def arg_names(self):
        sarg_names = super(InternetGateway, self).arg_names()
        return sarg_names + ['vpc']

    def arg_types(self):
        sarg_types = super(InternetGateway, self).arg_types()
        return sarg_types + [VPC]

    def __siblings__(self):
        siblings = super(InternetGateway, self).__siblings__()
        siblings += self._vpc_attachment()
        return siblings

    @property
    def vpc(self):
        return self._vpc
    
    @vpc.setter
    def vpc(self, value):
        self._vpc = value

    def _vpc_attachment(self):
        if not hasattr(self, 'vpc'):
            return []
        attachment_name = ''.join([self.name, self._vpc.name, "Attachment"])
        attachment = VPCGatewayAttachment(attachment_name, self._vpc, self)
        return [attachment]

class NetworkAcl(Resource):
    resource_type = 'AWS::EC2::NetworkAcl'

    @staticmethod
    def props():
        return [prop('VpcId', VPC),
                prop('Tags', Tags)]

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

    @staticmethod
    def props():
        return [prop('CidrBlock', CIDR),
                prop('Egress', bool),
                prop('Icmp'),
                prop('NetworkAclId', NetworkAcl),
                prop('PortRange', PortRange),
                prop('Protocol', IpProtocol),
                prop('RuleAction', AclAction),
                prop('RuleNumber', int)]

class NetworkInterface(Resource):
    resource_type = 'AWS::EC2::NetworkInterface'

    @staticmethod
    def props():
        return [prop('Description'),
                prop('GroupSet'),
                prop('PrivateIpAddress', IpAddress),
                prop('PrivateIpAddresses'),
                prop('SecondaryPrivateIpAddressCount'),
                prop('SourceDestCheck', bool),
                prop('SubnetId', Subnet),
                prop('Tags', Tags)]

class NetworkInterfaceAttachment(Resource):
    resource_type = 'AWS::EC2::NetworkInterfaceAttachment'

    @staticmethod
    def props():
        return [prop('DeleteOnTermination', bool),
                prop('DeviceIndex', int),
                prop('InstanceId', Instance),
                prop('NetworkInterfaceId', NetworkInterface)]

class Route(Resource):
    resource_type = 'AWS::EC2::Route'

    @staticmethod
    def props():
        return [prop('DestinationCidrBlock', CIDR),
                prop('GatewayId', InternetGateway),
                prop('InstanceId', Instance),
                prop('NetworkInterfaceId', NetworkInterface),
                prop('RouteTableId', RouteTable),
                prop('VpcPeeringConnectionId', VPCPeeringConnection)]

class RouteTable(Resource):
    resource_type = 'AWS::EC2::RouteTable'

    @staticmethod
    def props():
        return [prop('VpcId', VPC),
                prop('Tags', Tags)]

    def __attrs__(self):
        sattrs = super(RouteTable, self).__attrs__()
        return sattrs + ['subnet']

    def arg_names(self):
        sarg_names = super(RouteTable, self).arg_names()
        return sarg_names + ['subnet']

    def arg_types(self):
        sarg_types = super(RouteTable, self).arg_types()
        return sarg_types + [Subnet]

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
        result.siblings.append(Route(*args, **kwargs))
        return result

class SecurityGroup(Resource):
    resource_type = 'AWS::EC2::SecurityGroup'

    @staticmethod
    def props():
        return [prop('VpcId', Vpc),
                prop('GroupDescription'),
                prop('SecurityGroupEgress'),
                prop('SecurityGroupIngress'),
                prop('Tags', Tags)]

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

    @staticmethod
    def props():
        return [prop('CidrIp', CIDR),
                prop('DestinationSecurityGroupId'),
                prop('IpProtocol', IpProtocol),
                prop('FromPort', PortRange, 'port_range', PortRange.from_port),
                prop('ToPort', PortRange, 'port_range', PortRange.to_port),
                prop('GroupId')]

class SecurityGroupIngress(Resource):
    resource_type = 'AWS::EC2::SecurityGroupIgress'

    @staticmethod
    def props():
        return [prop('CidrIp', CIDR),
                prop('SourceSecurityGroupId'),
                prop('SourceSecurityGroupName'),
                prop('SourceSecurityGroupOwnerId'),
                prop('IpProtocol', IpProtocol),
                prop('FromPort', PortRange, 'port_range', PortRange.from_port),
                prop('ToPort', PortRange, 'port_range', PortRange.to_port),
                prop('GroupId'),
                prop('GroupName')]

class Subnet(Resource):
    resource_type = 'AWS::EC2::Subnet'

    @staticmethod
    def props():
        return [prop('AvailabilityZone', AvailabilityZone),
                prop('CidrBlock', CIDR),
                prop('VpcId', VPC),
                prop('Tags', Tags)]

class SubnetNetworkAclAssociation(Resource):
    resource_type = 'AWS::EC2::SubnetNetworkAclAssociation'

    @staticmethod
    def props():
        return [prop('SubnetId', Subnet),
                prop('NetworkAclId', NetworkAcl)]

class SubnetRouteTableAssociation(Resource):
    resource_type = 'AWS::EC2::SubnetRouteTableAssociation'

    @staticmethod
    def props():
        return [prop('RouteTableId', RouteTable),
                prop('SubnetId', Subnet)]

class Volume(Resource):
    resource_type = 'AWS::EC2::Volume'

    @staticmethod
    def props():
        [prop('AvailabilityZone', AvailabilityZone),
         prop('Encrypted'),
         prop('Iops'),
         prop('Size'),
         prop('SnapshotId'),
         prop('Tags', Tags),
         prop('VolumeType')]

class VolumeAttachment(Resource):
    resource_type = 'AWS::EC2::VolumeAttachment'

    @staticmethod
    def props():
        return [prop('Device'),
                prop('InstanceId', Instance),
                prop('VolumeId', Volumne)]

class VPC(Resource):
    resource_type = 'AWS::EC2::VPC'

    class Tenancy(Wrapper):
        pass
    Tenancy.DEFAULT   = Tenancy('default')
    Tenancy.DEDICATED = Tenancy('dedicated')

    @staticmethod
    def props():
        return [prop('CidrBlock', CIDR),
                prop('EnableDnsSupport'),
                prop('EnableDnsHostnames'),
                prop('InstanceTenancy', VPC.Tenancy),
                prop('Tags', Tags)]

    def __attrs__(self):
        sattrs = super(VPC, self).__attrs__()
        return sattrs + ['dhcp_options']

    def arg_names(self):
        sarg_names = super(VPC, self).arg_names()
        return sarg_names + ['dhcp_options']

    def arg_types(self):
        sarg_types = super(VPC, self).arg_types()
        return sarg_types + [DHCPOptions]

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

    @staticmethod
    def props():
        return [prop('DhcpOptionsId', DHCPOptions),
                prop('VpcId', VPC)]

class VPCGatewayAttachment(Resource):
    resource_type = 'AWS::EC2::VPCGatewayAttachment'

    @staticmethod
    def props():
        return [prop('VpcId', VPC),
                prop('InternetGatewayId', InternetGateway),
                prop('VpnGatewayId')]

class VPCPeeringConnection(Resource):
    resource_type = 'AWS::EC2::VPCPeeringConnection'

    @staticmethod
    def props():
        return [prop('PeerVpcId'),
                prop('VpcId'),
                prop('Tags', Tags)]

# TODO: Add VPN* resource types

#### Public API ####

# Generate functional snake_cased form of constructors for public API
def __is_resource(obj):
    return issubclass(type(obj), type) and issubclass(obj, Resource)
constructors = {snake_case(name): obj for (name, obj) in globals().items() if __is_resource(obj)}
globals().update(constructors)

def vpc_with_dns(*args, **kwargs):
    kwargs['enable_dns_support'] = True
    kwargs['enable_dns_hostnames'] = True
    return vpc(*args, **kwargs)

__all__ = sorted(['vpc_with_dns'] + constructors.keys())
