import sys
from common import *

######################## Template ########################
t = template("Registry stack - EC2 Host")

######################## Parameters ########################
t.Deployment   = deployment_parameter
t.Vpc          = vpc_parameter
t.VpcRegion    = vpc_region_parameter
t.Key          = key_parameter

t.RegistryInstanceType   = instance_type_parameter
t.RegistrySpotPrice      = spot_price_parameter
t.RegistryAmi            = ami_parameter
t.RegistrySubnet         = subnet_parameter
t.RegistrySecurityGroups = security_groups_parameter

# The split-horizon DNS routes internal requests to the
# registry.example.com domain to the internal registry host.
t.RegistrySplitHorizonHostedZoneName = hosted_zone_name_parameter

######################## Python Constants ########################

# Tags
TagsRegistry = tags_base(t.Deployment) + tag(Name=fn.join('-', [StackName, 'registry']))

# Constants
PATH = fn.join('/', ["", t.Deployment, 'internal', 'registry', 'example', 'ec2', ""])


######################## Resources ########################
# Split Hosted Zone
zone_vpc                   = route53.hosted_zone_vpc(vpc_id     = t.Vpc,
                                            vpc_region = t.VpcRegion)
registry_split_zone_config = route53.hosted_zone_config(
    comment = fn.join(' | ', [t.Deployment, "internal split-horizon DNS for registry"])
)

t.RegistrySplitHorizonHostedZone = route53.hosted_zone(name               = t.RegistrySplitHorizonHostedZoneName,
                                                       vpcs               = [zone_vpc],
                                                       hosted_zone_config = registry_split_zone_config,
                                                       hosted_zone_tags   = TagsRegistry)

# Instance Profile
t.RegistryRole             = iam.role(assume_role_policy_document=load_policy('role_registry.yml'),
                                      path = PATH)

t.ReadDockerRegistryPolicy = iam.policy(policy_name="read-docker-registry",
                                        policy_document=load_policy('read_docker_registry.yml'),
                                        roles=[ref(t.RegistryRole)])

t.RegistryInstanceProfile  = iam.instance_profile(path=PATH,
                                                  roles=[ref(t.RegistryRole)])

# Autoscaling Group
t.RegistryLaunchConfig = asg.launch_configuration(instance_type               = t.RegistryInstanceType,
                                                  image_id                    = t.RegistryAmi,
                                                  iam_instance_profile        = t.RegistryInstanceProfile,
                                                  security_groups             = t.RegistrySecurityGroups,
                                                  instance_monitoring         = False,
                                                  key_name                    = t.Key,
                                                  spot_price                  = t.RegistrySpotPrice)

t.RegistryAsg          = asg.auto_scaling_group(t.RegistryLaunchConfig,
                                                vpc_zone_identifier = [ref(t.RegistrySubnet)],
                                                desired_capacity    = 1,
                                                min_size            = 1,
                                                max_size            = 1,
                                                tags                = asg.from_tags(TagsRegistry, True))

######################## Outputs ########################
t.RegistryAsgId                    = output(value = t.RegistryAsg)
t.RegistrySplitHorizonHostedZoneId = output(value = t.RegistrySplitHorizonHostedZone)

if __name__ == "__main__":
    print t.to_json()
