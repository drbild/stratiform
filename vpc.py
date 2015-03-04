from stratiform.constants import *
from stratiform.types import *

from stratiform.templates import template
from stratiform.outputs import output
from stratiform.parameters import string_parameter, StackName
from stratiform.resources import tag, tags

from stratiform.functions import join

import stratiform.ec2 as ec2

# Constants
cidr_vpc    = cidr("10.20.0.0/16")
cidr_public = cidr("10.20.10.0/24")
cidr_ext    = cidr("98.206.146.32/32")

# Parameters
deployment  = string_parameter("Deployment", "The environment to which this stack is deployed",
                               allowed_values = ['dev', 'stage', 'prod'],
                               constraint_description = "Must be one of the following environments - dev | stage | prod")
domain_name = string_parameter("DomainName", "The domain name to provide to DHCP clients in this VPC")

# Common tags
tags_base = tags(Environment=deployment, Stack=StackName)
tags_public = tags_base + tag(Network="public")
tags_public_named = tags_public + tag(Name=join('-', [StackName, 'public']))

# Resources
dhcp_options     = ec2.dhcp_options("DHCPOptions", tags_base + tag(Name=StackName), domain_name=domain_name)
vpc              = ec2.vpc_with_dns("VPC", cidr_vpc, dhcp_options, tags_base + tag(Name=StackName))

internet_gateway   = ec2.internet_gateway("InternetGateway", vpc, tags_public_named)
public_subnet      = ec2.subnet("PublicSubnet", vpc, us_west_2a, cidr_public, tags_public_named)
public_route_table = ec2.route_table("PublicRouteTable", vpc, public_subnet, tags_public_named) \
                        .route("PublicRoute", all_cidr, internet_gateway)

public_network_acl = ec2.network_acl("PublicNetworkAcl", vpc, tags_public_named) \
                        .ingress("InboundHTTPS",     110, allow, cidr_ext, tcp, https) \
                        .ingress("InboundSSH",       120, allow, cidr_ext, tcp, ssh) \
                        .ingress("InboundEphemeral", 140, allow, all_cidr, tcp, all_ephemeral_ports) \
                        .egress("OutboundHTTP",      100, allow, all_cidr, tcp, http) \
                        .egress("OutboundHTTPS",     110, allow, all_cidr, tcp, https) \
                        .egress("OutboundEphemeral", 140, allow, all_cidr, tcp, linux_ephemeral_ports)

# Outputs
vpc_id                = output("VpcId", vpc)
public_subnet_id      = output("PublicSubnetId", public_subnet)
public_route_table_id = output("PublicRouteTableId", public_route_table)

# Create template
t = template("VPC stack for bigsky docker registry")
t = t.add(deployment,
          domain_name,
          vpc,
          dhcp_options,
          internet_gateway,
          public_subnet,
          public_route_table,
          public_network_acl,
          vpc_id,
          public_subnet_id,
          public_route_table_id)
print t

