import sys
from common import *

######################## Template ########################
t = template("ELK stack - ASG")

######################## Parameters ########################
t.Deployment = deployment_parameter
t.Key        = key_parameter

t.ElkInstanceType   = instance_type_parameter
t.ElkSpotPrice      = spot_price_parameter
t.ElkAmi            = ami_parameter
t.ElkSubnet         = subnet_parameter
t.ElkSecurityGroups = security_groups_parameter

######################## Python Constants ########################
# Read parameters from command line
deployment = sys.argv[1]
assert deployment in ('dev', 'stage', 'prod')

# Constants
PATH = fn.join('/', ["", t.Deployment, 'internal', 'example', 'ec2', ""])

# Tags
TagsElk = tags_base(t.Deployment) + tag(Name=fn.join('-', [StackName, 'elk']))

######################## Resources ########################
# Instance Profile
t.ElkRole            = iam.role(assume_role_policy_document = load_policy('role_elk.yml'),
                                path                        = PATH)

t.ReadElkSslPolicy   = iam.policy(policy_name     = "read-elk-ssl",
                                  policy_document = load_policy('read_elk_ssl.yml', {'deployment' : deployment}),
                                  roles           = [ref(t.ElkRole)])

t.ElkInstanceProfile = iam.instance_profile(path  = PATH,
                                            roles = [ref(t.ElkRole)])

# Autoscaling Group
t.ElkLaunchConfig    = asg.launch_configuration(instance_type        = t.ElkInstanceType,
                                                image_id             = t.ElkAmi,
                                                iam_instance_profile = t.ElkInstanceProfile,
                                                security_groups      = t.ElkSecurityGroups,
                                                instance_monitoring  = False,
                                                key_name             = t.Key,
                                                spot_price           = t.ElkSpotPrice)

t.ElkAsg             = asg.auto_scaling_group(t.ElkLaunchConfig,
                                              vpc_zone_identifier = [ref(t.ElkSubnet)],
                                              desired_capacity    = 1,
                                              min_size            = 1,
                                              max_size            = 1,
                                              tags                = asg.from_tags(TagsElk, True))

######################## Outputs ########################
t.ElkAsgId = output(value = t.ElkAsg)

if __name__ == "__main__":
    print t.to_json()
