from common import *

######################## Template ########################
t = template("VPC stack - VPC, Subnets, and Routing Rules")

######################## Parameters ########################
t.Deployment = deployment_parameter

t.VpcDomainName = string_parameter(description="The domain name for DHCP clients")

######################## Python Constants ########################

TagsBase = tags_base(t.Deployment)

# Tags
TagsPublic       = TagsBase + tag(Network="public")
TagsPrivate      = TagsBase + tag(Network="private")
TagsPublicNamed  = TagsPublic + tag(Name=fn.join('-', [StackName, 'public']))
TagsPrivateNamed = TagsPrivate + tag(Name=fn.join('-', [StackName, 'private']))

######################## Resources ########################
# VPC
t.DhcpOptions      = ec2.dhcp_options(ec2.aws_provided_dns, TagsBase + nametag(StackName), domain_name=t.VpcDomainName)
t.Vpc              = ec2.vpc_with_dns(CIDR_VPC, t.DhcpOptions, TagsBase + nametag(StackName))
t.InternetGateway = ec2.internet_gateway(t.Vpc, TagsPublicNamed)

# Public Subnet
t.PublicSubnet     = ec2.subnet(t.Vpc, ZONE, CIDR_PUBLIC, TagsPublicNamed)
t.PublicRouteTable = ec2.route_table("PublicRouteTable", t.Vpc, t.PublicSubnet, TagsPublicNamed) \
                        .route("PublicRoute", cidr_all, t.InternetGateway)

t.PublicNetworkAcl = ec2.network_acl("PublicNetworkAcl", t.Vpc, TagsPublicNamed)            \
                        .allow_ingress("HTTP",      100, tcp, cidr_all,     http)           \
                        .allow_ingress("HTTPS",     110, tcp, cidr_all,     https)          \
                        .allow_ingress("SSH",       120, tcp, CIDR_EXT,     ssh)            \
                        .allow_ingress("Ephemeral", 140, tcp, cidr_all,     ephemeral_elb)  \
                        .allow_ingress("NTP",       150, udp, cidr_all,     ntp)            \
                        .allow_ingress("SMTP",      160, tcp, CIDR_PRIVATE, port(587))      \
                        .allow_egress("HTTP",       100, tcp, cidr_all,     http)           \
                        .allow_egress("HTTPS",      110, tcp, cidr_all,     https)          \
                        .allow_egress("SSH",        120, tcp, CIDR_PRIVATE, ssh)            \
                        .allow_egress("Postgres",   130, tcp, CIDR_PRIVATE, postgresql)     \
                        .allow_egress("Ephemeral",  140, tcp, cidr_all,     ephemeral)      \
                        .allow_egress("NTP",        150, udp, cidr_all,     ntp)            \
                        .allow_egress("SMTP",       160, tcp, cidr_all,     port(587))

t.PublicNetworkAclAssociation = ec2.subnet_network_acl_association(t.PublicSubnet,
                                                                   t.PublicNetworkAcl)

### Private Subnets
t.PrivateSubnet     = ec2.subnet(t.Vpc, ZONE, CIDR_PRIVATE_PRIMARY, TagsPrivateNamed)
t.PrivateRouteTable = ec2.route_table(t.Vpc, t.PrivateSubnet, TagsPrivateNamed)

t.PrivateSubnetBackup     = ec2.subnet(t.Vpc, ZONE_BACKUP, CIDR_PRIVATE_BACKUP, TagsPrivateNamed)
t.PrivateRouteTableBackup = ec2.route_table(t.Vpc, t.PrivateSubnetBackup, TagsPrivateNamed)

t.PrivateNetworkAcl = ec2.network_acl("PrivateNetworkAcl", t.Vpc, TagsPrivateNamed)                     \
                         .allow_ingress("AllPrivate",  50, protocol_all, CIDR_PRIVATE, ports_all)       \
                         .allow_ingress("HTTP",       100, tcp,          CIDR_PUBLIC,  http)            \
                         .allow_ingress("SSH",        120, tcp,          CIDR_PUBLIC,  ssh)             \
                         .allow_ingress("Postgres",   130, tcp,          CIDR_PUBLIC,  postgresql)      \
                         .allow_ingress("Ephemeral",  140, tcp,          cidr_all,     ephemeral_linux) \
                         .allow_ingress("NTP",        150, udp,          cidr_all,     ntp)             \
                         .allow_egress("AllPrivate",   50, protocol_all, CIDR_PRIVATE, ports_all)       \
                         .allow_egress("HTTP",        100, tcp,          cidr_all,     http)            \
                         .allow_egress("HTTPS",       110, tcp,          cidr_all,     https)           \
                         .allow_egress("Ephemeral",   140, tcp,          CIDR_PUBLIC,  ephemeral_elb)   \
                         .allow_egress("NTP",         150, udp,          cidr_all,     ntp)             \
                         .allow_egress("SMTP",        160, tcp,          cidr_all,     port(587))

t.PrivateNetworkAclAssociation = ec2.subnet_network_acl_association(t.PrivateSubnet,
                                                                    t.PrivateNetworkAcl)
t.PrivateNetworkAclAssociationBackup = ec2.subnet_network_acl_association(t.PrivateSubnetBackup,
                                                                          t.PrivateNetworkAcl)

######################## Outputs ########################
t.VpcId                     = output(value = t.Vpc)
t.PublicSubnetId            = output(value = t.PublicSubnet)
t.PrivateSubnetId           = output(value = t.PrivateSubnet)
t.PublicRouteTableId        = output(value = t.PublicRouteTable)
t.PrivateRouteTableId       = output(value = t.PrivateRouteTable)
t.PrivateSubnetBackupId     = output(value = t.PrivateSubnetBackup)
t.PrivateRouteTableBackupId = output(value = t.PrivateRouteTableBackup)

if __name__ == "__main__":
    print t.to_json()
