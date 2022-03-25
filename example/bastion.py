from common import *

######################## Template ########################
t = template("Bastion stack - EC2 Host")

######################## Parameters ########################
t.Deployment = deployment_parameter
t.Key        = key_parameter

t.BastionInstanceType   = instance_type_parameter
t.BastionSpotPrice      = spot_price_parameter
t.BastionAmi            = ami_parameter
t.BastionSubnet         = subnet_parameter
t.BastionSecurityGroups = security_groups_parameter

######################## Python Constants ########################

# Tags
TagsBastion = tags_base(t.Deployment) + tag(Name=fn.join('-', [StackName, 'bastion']))

######################## Resources ########################
t.BastionLaunchConfig = asg.launch_configuration(associate_public_ip_address = True,
                                                 instance_type               = t.BastionInstanceType,
                                                 image_id                    = t.BastionAmi,
                                                 security_groups             = t.BastionSecurityGroups,
                                                 instance_monitoring         = False,
                                                 key_name                    = t.Key,
                                                 spot_price                  = t.BastionSpotPrice)

t.BastionAsg          = asg.auto_scaling_group(t.BastionLaunchConfig,
                                               vpc_zone_identifier = [ref(t.BastionSubnet)],
                                               desired_capacity    = 1,
                                               min_size            = 1,
                                               max_size            = 1,
                                               tags                = asg.from_tags(TagsBastion, True))

######################## Outputs ########################
t.BastionAsgId = output(value = t.BastionAsg)


if __name__ == "__main__":
    print t.to_json()
