from common import *

######################## Template ########################
t = template("NAT stack - EC2 ASG")

######################## Parameters ########################
t.Deployment        = deployment_parameter
t.Key               = key_parameter

t.NatInstanceType   = instance_type_parameter
t.NatSpotPrice      = spot_price_parameter
t.NatAmi            = ami_parameter
t.NatSubnet         = subnet_parameter
t.NatSecurityGroups = security_groups_parameter

######################## Python Constants ########################
# Tags
TagsNat = tags_base(t.Deployment) + tag(Name=fn.join('-', [StackName, 'nat']))

######################## Resources ########################
# Must set sourceDestCheck to False after the instance has launched.
# Our Ansible scripts should do this.
t.NatLaunchConfig = asg.launch_configuration(associate_public_ip_address = True,
                                             instance_type = t.NatInstanceType,
                                             image_id = t.NatAmi,
                                             security_groups = t.NatSecurityGroups,
                                             instance_monitoring = False,
                                             key_name = t.Key,
                                             spot_price = t.NatSpotPrice)

t.NatAsg = asg.auto_scaling_group(t.NatLaunchConfig,
                                  vpc_zone_identifier = [ref(t.NatSubnet)],
                                  desired_capacity = 1,
                                  min_size = 1,
                                  max_size = 1,
                                  tags = asg.from_tags(TagsNat, True))

######################## Outputs ########################
t.NatAsgId = output(value = t.NatAsg)

if __name__ == "__main__":
    print t.to_json()
