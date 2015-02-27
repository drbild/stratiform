from stratiform import *

import stratiform.functions as fn
import stratiform.ec2 as ec2

# Constants
cidr_vpc    = cidr("10.20.0.0/16")
cidr_public = cidr("10.20.10.0/24")
cidr_ext    = cidr("98.206.146.32/32")

zone        = az('us-west-2a')

# Parameters
deployment  = string_parameter("Deployment", "The environment to which this stack is deployed",
                               allowed_values = ['dev', 'stage', 'prod'],
                               constraint_description = "Must be one of the following environments - dev | stage | prod")
domain_name = string_parameter("DomainName", "The domain name to provide to DHCP clients in this VPC")

# Common tags
tags_base = tags(Environment=deployment, Stack=StackName)
tags_public = tags_base + tag(Network="public")
tags_public_named = tags_public + tag(Name=fn.join('-', [StackName, 'public']))

# Resources
dhcp_options     = ec2.dhcp_options("DHCPOptions", tags_base + tag(Name=StackName), domain_name=domain_name)
vpc              = ec2.vpc_with_dns("VPC", cidr_vpc, dhcp_options, tags_base + tag(Name=StackName))

internet_gateway   = ec2.internet_gateway("InternetGateway", vpc, tags_public_named)
public_subnet      = ec2.subnet("PublicSubnet", vpc, zone, cidr_public, tags_public_named)
public_route_table = ec2.route_table("PublicRouteTable", vpc, public_subnet, tags_public_named) \
                        .route("PublicRoute", cidr_all, internet_gateway)

public_network_acl = ec2.network_acl("PublicNetworkAcl", vpc, tags_public_named) \
                        .allow_ingress("InboundHTTPS",     110, tcp, cidr_ext, https) \
                        .allow_ingress("InboundSSH",       120, tcp, cidr_ext, ssh) \
                        .allow_ingress("InboundEphemeral", 140, tcp, cidr_all, ephemeral) \
                        .allow_egress("OutboundHTTP",      100, tcp, cidr_all, http) \
                        .allow_egress("OutboundHTTPS",     110, tcp, cidr_all, https) \
                        .allow_egress("OutboundEphemeral", 140, tcp, cidr_all, ephemeral_linux)

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

