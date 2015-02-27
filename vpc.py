from stratiform.outputs import output
from stratiform.parameters import *
from stratiform.resources import tag, tags
from stratiform.templates import template

import stratiform.ec2 as ec2

from stratiform.constants import cidr, ALL_CIDR, TCP, ALL_EPHEMERAL_PORTS, LINUX_EPHEMERAL_PORTS, ALLOW, SSH, HTTP, HTTPS

# Constants
cidr_vpc = cidr("10.20.0.0/16")
cidr_ext = cidr("98.0.0.0/31")

domain_name  = "example.com"

# Parameters
deployment = parameter("Deployment",
                       description="The environment to which this stack is deployed",
                       type='String',
                       allowed_values=['dev', 'stage', 'prod'],
                       constraint_description="Must be one of the following environments - dev | stage | prod")

domain_name = parameter("DomainName",
                        description="The domain name to provide to DHCP clients in this VPC",
                        type='String')

# Common tags
tags_base = tags(Environment=deployment, Stack=STACK_NAME)
tags_public = tags_base + tag(Network="public")

# Resources
dhcp_options     = ec2.dhcp_options("DHCPOptions", domain_name=domain_name, domain_name_servers=['AmazonProvidedDNS'], tags=tags_base)
vpc              = ec2.vpc("VPC", cidr_block=cidr_vpc, enable_dns_support=True, enable_dns_hostnames=True, dhcp_options=dhcp_options, tags=tags_public)

public_subnet      = ec2.subnet("PublicSubnet", "us-west-2a", ALL_CIDR, vpc, tags=tags_public)
internet_gateway   = ec2.internet_gateway("InternetGateway", tags=tags_public)
public_route_table = ec2.route_table("PublicRouteTable", vpc_id=vpc, subnet=public_subnet, tags=tags_public) \
                        .route("PublicRoute", ALL_CIDR, gateway_id=internet_gateway)

public_network_acl = ec2.network_acl("PublicNetworkAcl", vpc, tags=tags_public) \
    .ingress("InboundHTTPS",     rule_number=110, cidr_block=cidr_ext, protocol=TCP, rule_action=ALLOW, port_range=HTTPS) \
    .ingress("InboundSSH",       rule_number=120, cidr_block=cidr_ext, protocol=TCP, rule_action=ALLOW, port_range=SSH) \
    .ingress("InboundEphemeral", rule_number=140, cidr_block=ALL_CIDR, protocol=TCP, rule_action=ALLOW, port_range=ALL_EPHEMERAL_PORTS) \
    .egress("OutboundHTTP",      rule_number=100, cidr_block=ALL_CIDR, protocol=TCP, rule_action=ALLOW, port_range=HTTP) \
    .egress("OutboundHTTPS",     rule_number=110, cidr_block=ALL_CIDR, protocol=TCP, rule_action=ALLOW, port_range=HTTPS) \
    .egress("OutboundEphemeral", rule_number=140, cidr_block=ALL_CIDR, protocol=TCP, rule_action=ALLOW, port_range=LINUX_EPHEMERAL_PORTS)

# Outputs
vpc_id                = output("VpcId", vpc, "Id of the VPC")
public_subnet_id      = output("PublicSubnetId", public_subnet)
public_route_table_id = output("PublicRouteTableId", public_route_table)

# Create template
t = template("VPC stack for bigsky docker registry")

t = t.parameter(deployment)
t = t.parameter(domain_name)

t = t.resource(vpc)
t = t.resource(dhcp_options)
t = t.resource(internet_gateway)
t = t.resource(public_subnet)
t = t.resource(public_route_table)
t = t.resource(public_network_acl)

t = t.output(vpc_id)
t = t.output(public_subnet_id)
t = t.output(public_route_table_id)

print t.to_json()
