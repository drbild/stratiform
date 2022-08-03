# stratiform

[DEPRECATED] This library is deprecated. Use something Hashicorp
Terraform instead (although the limited expressiveness of declarative
HCL is a significant step backwards).

Stratiform is a Python library for concisely creating AWS
CloudFormation JSON templates.  Python's expressiveness leads to
simpler and easier-to-read templates than a purley declarative
approach like JSON (or HCL), significantly reducing the number of
accidental misconfigurations.


## Install

```pip install stratiform```


## Usage

A Stratiform template is simply a python script that defines the AWS
resources as Stratiform objects and then prints corresponding
CloudFormation JSON to stdout.

``` python
from stratiform import *
import stratiform.ec2 as ec2

# Create a template
t = template("VPC stack - VPC, Subnets, and Routing Rules")
Tags = tags(Deployment=t.Deployment, Stack=StackName)

# Define constants
CIDR_VPC    = cidr("10.20.0.0/16")
CIDR_PUBLIC = cidr("10.20.10.0/24")
ZONE        = az('us-west-2a')

# Define parameters, resources, outputs, etc., in the template
t.Deployment = string_parameter(description="Environment containing this stack.",
                                allowed_values=['dev', 'stage', 'prod'])

t.Vpc              = ec2.vpc(CIDR_VPC, Tags)
t.InternetGateway  = ec2.internet_gateway(t.Vpc, Tags)
t.PublicSubnet     = ec2.subnet(t.Vpc, ZONE, CIDR_PUBLIC, Tags)
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

# Define outputs
t.VpcId                     = output(value = t.Vpc)
t.PublicSubnetId            = output(value = t.PublicSubnet)
t.PrivateSubnetId           = output(value = t.PrivateSubnet)
t.PublicRouteTableId        = output(value = t.PublicRouteTable)

# Print the JSON
if __name__ == "__main__":
    print t.to_json()
```

## Example
For a larger example with multiple CloudFormation stacks and
additional resource types (RDS, EC2, S3, etc.), see the `example/`
directory.

## Authors
**David R. Bild**

+ [https://www.davidbild.org](https://www.davidbild.org)
+ [https://github.com/drbild](https://github.com/drbild)

## License
Copyright 2015 David R. Bild

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License from the LICENSE.txt file or at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
