import os, yaml

from string import Template

from stratiform import *
import stratiform.functions as fn
import stratiform.asg as asg
import stratiform.ec2 as ec2
import stratiform.elb as elb
import stratiform.iam as iam
import stratiform.rds as rds
import stratiform.route53 as route53

################ Constants ################
CIDR_VPC             = cidr("10.20.0.0/16")
CIDR_PUBLIC          = cidr("10.20.10.0/24")
CIDR_PRIVATE         = cidr("10.20.20.0/23")
CIDR_PRIVATE_PRIMARY = cidr("10.20.20.0/24")
CIDR_PRIVATE_BACKUP  = cidr("10.20.21.0/24")
CIDR_EXT             = cidr("73.72.178.72/32") # Our external IP block

ZONE          = az('us-west-2a')
ZONE_BACKUP   = az('us-west-2b')

elasticsearch = port(9300)
logstash      = port(5000)

################ Common Parameters ################
ami_parameter              = string_parameter(description="An AMI id.")

db_instance_type_parameter = string_parameter(description="A RDS instance type.",
                                              allowed_values = ['db.t2.micro', 'db.t2.small',
                                                                'db.t2.medium', 'db.m3.medium'])

deployment_parameter       = string_parameter(description="Environment containing this stack.",
                                             allowed_values=['dev', 'stage', 'prod'])

fqdn_parameter             = string_parameter(description="A fully-qualified domain name.")

hosted_zone_parameter      = string_parameter(description="A route53 hosted zone id.")

hosted_zone_name_parameter = string_parameter(description="A domain name.")

instance_type_parameter    = string_parameter(description="An EC2 instance type.",
                                             allowed_values = ['t1.micro',
                                                               't2.micro', 't2.small', 't2.medium', 't2.large',
                                                               'm1.small', 'm1.large',
                                                               'm3.medium'])

spot_price_parameter       = string_parameter(description="Bid for EC2 spot instances")

key_parameter              = string_parameter(description="Name of a key pair.")

route_table_parameter      = string_parameter(description="A route table id.")

security_groups_parameter  = list_security_group_parameter(description="List of security group ids")

subnet_parameter           = string_parameter(description="A subnet id.")

subnets_parameter          = list_subnet_parameter(description="List of subnet ids.")

volume_parameter           = string_parameter(description="An EBS volume id.")

volume_size_parameter      = number_parameter(description="Size of an EBS volume in GiB.")

volume_device_parameter    = string_parameter(description="The path at which to expose a volume.")

vpc_parameter              = string_parameter(description="A VPC id.")

vpc_region_parameter       = string_parameter(description="A region containing a VPC.")

################ Common Tags ################
def tags_base(deployment_parameter):
    return tags(Deployment=deployment_parameter, Stack=StackName)

################ Common ELB Policy  ################
ssl_protocols_strict = ['Protocol-TLSv1.2']

ssl_ciphers_strict = ['ECDHE-ECDSA-AES128-GCM-SHA256',
                      'ECDHE-RSA-AES128-GCM-SHA256',
                      'ECDHE-ECDSA-AES128-SHA256',
                      'ECDHE-RSA-AES128-SHA256',
                      'ECDHE-ECDSA-AES128-SHA',
                      'ECDHE-RSA-AES128-SHA',
                      'DHE-RSA-AES128-SHA',
                      'ECDHE-ECDSA-AES256-GCM-SHA384',
                      'ECDHE-RSA-AES256-GCM-SHA384',
                      'ECDHE-ECDSA-AES256-SHA384',
                      'ECDHE-RSA-AES256-SHA384',
                      'ECDHE-RSA-AES256-SHA',
                      'ECDHE-ECDSA-AES256-SHA',
                      'AES128-GCM-SHA256',
                      'AES256-GCM-SHA384']

elb_ssl_negotiation_policy_strict = elb.Policy(policy_name = "common-ssl-negotiation-policy-strict",
                                               policy_type = "SSLNegotiationPolicyType",
                                               attributes  = [elb.ssl_attribute(x) for x in ['Server-Defined-Cipher-Order'] + ssl_protocols_strict + ssl_ciphers_strict])

################ Helper Functions ################
# Helper function to create Tag(Name=...)
def nametag(name):
    return tag(Name=name)

# Functions to load yaml policy documents
def load_policy(name, mapping={}):
    base = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(base, "policies", name)) as stream:
        raw = stream.read()
        template = Template(raw)
        return yaml.load(template.substitute(mapping))
