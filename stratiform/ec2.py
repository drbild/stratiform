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

from stratiform.resources import Resource, Tags

################################ Custom Types ################################
class AclAction(Wrapper):
    pass
AclAction.allow = AclAction('allow')
AclAction.deny  = AclAction('deny')

class DomainNameServers(ListWrapper):
    pass
DomainNameServers.aws_provided_dns = DomainNameServers(['AmazonProvidedDns'])

class ImageId(Wrapper):
    pass

################################ AWS Property Types ################################
class ICMPProperty(AWSObject):
    @staticmethod
    def props():
        return [prop('Code', int),
                prop('Type', int)]

class MountPoint(AWSObject):
    @staticmethod
    def props():
        return [prop('Device', basestring),
                prop('VolumeId', Volume)]

class NetworkInterfaceProperty(AWSObject):
    @staticmethod
    def props():
        return [prop('AssociatePublicIpAddress'),
                prop('DeleteOnTermination'),
                prop('Description'),
                prop('DeviceIndex'),
                prop('GroupSet'),
                prop('NetworkInterfaceId'),
                prop('PrivateIpAddress', IpAddress),
                prop('PrivateIpAddresses'),
                prop('SecondaryPrivateIpAddressCount'),
                prop('SubnetId', Subnet)]

class NetworkInterfaceAssociation(AWSObject):
    @staticmethod
    def props():
        return [prop('AttachmentId', NetworkInterfaceAttachment),
                prop('InstanceId', Instance),
                prop('PublicIp', IpAddress),
                prop('IpOwnerId')]

class NetworkInterfaceAttachmentProperty(AWSObject):
    @staticmethod
    def props():
        return [prop('AttachmentId', NetworkInterfaceAttachment),
                prop('InstanceId', Instance)]

class NetworkInterfaceGroupItem(AWSObject):
    @staticmethod
    def props():
        return [prop('GroupId'),
                prop('GroupName')]

class NetworkInterfacePrivateIpSpecification(AWSObject):
    @staticmethod
    def props():
        return [prop('PrivateIpAddress'),
                prop('Primary')]

class SecurityGroupRuleIngress(AWSObject):
    @staticmethod
    def props():
        return [prop('CidrIp', CIDR),
                prop('FromPort', PortRange, 'port_range', PortRange.from_port),
                prop('ToPort', PortRange, 'port_range', PortRange.to_port),
                prop('IpProtocol', IpProtocol),
                prop('SourceSecurityGroupId', SecurityGroup),
                prop('SourceSecurityGroupName'),
                prop('SourceSecurityGroupOwnerId')]

class SecurityGroupRuleEgress(AWSObject):
    @staticmethod
    def props():
        return [prop('CidrIp', CIDR),
                prop('FromPort', PortRange, 'port_range', PortRange.from_port),
                prop('ToPort', PortRange, 'port_range', PortRange.to_port),
                prop('IpProtocol', IpProtocol),
                prop('DestinationSecurityGroupId', SecurityGroup)]

################################ AWS Resource Types ################################
class CustomerGateway(Resource):
    resource_type = 'AWS::EC2::CustomerGateway'

    @staticmethod
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
                prop('DomainNameServers', DomainNameServers,
                     default=DomainNameServers.aws_provided_dns),
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
        return [prop('AvailabilityZone', AvailabilityZone),
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
                prop('PrivateIpAddress', IpAddress),
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

    def siblings(self):
        siblings = super(InternetGateway, self).siblings()
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
        attachment_name = ''.join([self.object_name, self._vpc.object_name, "Attachment"])
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
        result._siblings.append(network_acl_entry(*args, **kwargs))
        return result

    def ingress(self, *args, **kwargs):
        kwargs['egress'] = False
        return self.entry(*args, **kwargs)

    def allow_ingress(self, *args, **kwargs):
        kwargs['rule_action'] = AclAction.allow
        args = self.prefix_name_arg("Allow", "Ingress", args)
        return self.ingress(*args, **kwargs)

    def deny_ingress(self, *args, **kwargs):
        kwargs['rule_action'] = AclAction.deny
        args = self.prefix_name_arg("Deny", "Ingress", args)
        return self.ingress(*args, **kwargs)

    def egress(self, *args, **kwargs):
        kwargs['egress'] = True
        return self.entry(*args, **kwargs)

    def allow_egress(self, *args, **kwargs):
        kwargs['rule_action'] = AclAction.allow
        args = self.prefix_name_arg("Allow", "Egress", args)
        return self.egress(*args, **kwargs)

    def deny_egress(self, *args, **kwargs):
        kwargs['rule_action'] = AclAction.deny
        args = self.prefix_name_arg("Deny", "Egress", args)
        return self.egress(*args, **kwargs)

    def prefix_name_arg(self, action, kind, args):
        '''Adds a prefix consisting of the ACL name, the action, and the
        direction to the name argument.

        '''
        if len(args) < 1 or not isinstance(args[0], basestring):
            return args
        args = list(args)
        args[0] = self.object_name + action.title() + kind.title() + args[0]
        return args

class NetworkAclEntry(Resource):
    resource_type = 'AWS::EC2::NetworkAclEntry'

    @staticmethod
    def props():
        return [prop('CidrBlock', CIDR),
                prop('Egress', bool),
                prop('Icmp', ICMPProperty),
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

    def siblings(self):
        siblings = super(RouteTable, self).siblings()
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
        association_name = ''.join([self._subnet.object_name, self.object_name, "Association"])
        association = SubnetRouteTableAssociation(association_name, subnet_id=self._subnet,
                                                  route_table_id=self)
        return [association]

    def route(self, *args, **kwargs):
        result = copy(self)
        kwargs['route_table_id'] = self
        result._siblings.append(Route(*args, **kwargs))
        return result

class SecurityGroup(Resource):
    resource_type = 'AWS::EC2::SecurityGroup'

    @staticmethod
    def props():
        return [prop('VpcId', VPC),
                prop('GroupDescription', basestring),
                prop('SecurityGroupEgress', default=[]),
                prop('SecurityGroupIngress', default=[]),
                prop('Tags', Tags)]

    def egress(self, *args, **kwargs):
        result = copy(self)
        args = self.prefix_name_arg("Outbound", args)
        args, kwargs = SecurityGroup.name_sg_arg('destination_security_group_id', args, kwargs)
        kwargs['group_id'] = self
        result._siblings.append(security_group_egress(*args, **kwargs))
        return result

    def ingress(self, *args, **kwargs):
        result = copy(self)
        args = self.prefix_name_arg("Inbound", args)
        args, kwargs = SecurityGroup.name_sg_arg('source_security_group_id', args, kwargs)
        kwargs['group_id'] = self
        result._siblings.append(security_group_ingress(*args, **kwargs))
        return result

    def prefix_name_arg(self, kind, args):
        '''Adds a prefix consisting of the group name and the direction to the
        name argument.

        '''
        if len(args) < 1 or not isinstance(args[0], basestring):
            return args
        args = list(args)
        args[0] = self.object_name + kind.title() + args[0]
        return args

    @staticmethod
    def name_sg_arg(kw, args, kwargs):
        '''Replaces a positional argument of type SecurityGroup by keyword
        arguments of the specified name.

        '''
        sg = None
        for arg in args:
            if isinstance(arg, SecurityGroup):
                sg = arg
                break
        if sg:
            kwargs[kw] = sg
            args.remove(sg)
        return args, kwargs

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
    resource_type = 'AWS::EC2::SecurityGroupIngress'

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
        return [prop('AvailabilityZone', AvailabilityZone),
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
                prop('VolumeId', Volume)]

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

    def siblings(self):
        siblings = super(VPC, self).siblings()
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
        association_name = ''.join([self.object_name, self._dhcp_options.object_name, "Association"])
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

class VPNConnection(Resource):
    resource_type = 'AWS::EC2::VPNConnection'
    
    @staticmethod
    def props():
        return [prop('Type'),
                prop('CustomerGatewayId', CustomerGateway),
                prop('StaticRoutesOnly'),
                prop('Tags', Tags),
                prop('VpnGatewayId', VPNGateway)]

class VPNConnectionRoute(Resource):
    resource_type = 'AWS::EC2::VPNConnectionRoute'
    
    @staticmethod
    def props():
        return [prop('DestinationCidrBlock', CIDR),
                prop('VPnConnectionId', VPNConnection)]

class VPNGateway(Resource):
    resource_type = 'AWS::EC2::VPNGateway'
    
    @staticmethod
    def props():
        return [prop('Type'),
                prop('Tags', Tags)]

class VPNGatewayRoutePropagation(Resource):
    resource_type = 'AWS::EC2::VPNGatewayRoutePropagation'
    
    @staticmethod
    def props():
        return [prop('RouteTableIds'),
                prop('VpnGatewayId', VPNGateway)]

#### Public API ####
# Generate functional snake_cased form of constructors for public API
def __is_resource(obj):
    return issubclass(type(obj), type) and issubclass(obj, Resource)
constructors = {snake_case(name): obj for (name, obj) in globals().items() if __is_resource(obj)}
globals().update(constructors)

acl_action          = AclAction
allow               = AclAction.allow
deny                = AclAction.deny
domain_name_servers = DomainNameServers
aws_provided_dns    = DomainNameServers.aws_provided_dns
image_id            = ImageId

icmp_property                              = ICMPProperty
mount_point                                = MountPoint
network_interface_property                 = NetworkInterfaceProperty
network_interface_association              = NetworkInterfaceAssociation
network_interface_attachment_property      = NetworkInterfaceAttachmentProperty
network_interface_group_item               = NetworkInterfaceGroupItem
network_interface_private_ip_specification = NetworkInterfacePrivateIpSpecification
port_range                                 = PortRange
security_group_rule_ingress                = SecurityGroupRuleIngress
security_group_rule_egress                 = SecurityGroupRuleEgress

def vpc_with_dns(*args, **kwargs):
    """Creates a VPC resource with enable_dns_support and
    enable_dns_hostnames both set to True.

    """
    kwargs['enable_dns_support'] = True
    kwargs['enable_dns_hostnames'] = True
    return vpc(*args, **kwargs)

__all__ = sorted(['acl_action', 'allow', 'deny',
                  'domain_name_servers', 'aws_provided_dns',
                  'vpc_with_dns', 'icmp_property', 'mount_point',
                  'network_interface_property',
                  'network_interface_association',
                  'network_interface_attachment_property',
                  'network_interface_group_item',
                  'network_interface_private_ip_specification',
                  'port_range', 'security_group_rule_ingress',
                  'security_group_rule_egress'] + \
                 constructors.keys())
