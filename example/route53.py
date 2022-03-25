from common import *

######################## Template ########################
t = template("Route53 stack - Hosted Zones")

######################## Parameters ########################
t.Deployment             = deployment_parameter
t.Vpc                    = vpc_parameter
t.VpcRegion              = vpc_region_parameter
t.InternalHostedZoneName = hosted_zone_name_parameter

######################## Python Constants ########################
# Tags
TagsRoute53 = tags_base(t.Deployment) + tag(Name=fn.join('-', [StackName, 'route53']))

######################## Resources ########################
zone_vpc             = route53.hosted_zone_vpc(vpc_id     = t.Vpc,
                                               vpc_region = t.VpcRegion)

internal_zone_config = route53.hosted_zone_config(comment = fn.join(' | ',
                                                                    [t.Deployment, "private internal DNS"]))

t.InternalHostedZone = route53.hosted_zone(name               = t.InternalHostedZoneName,
                                           vpcs               = [zone_vpc],
                                           hosted_zone_config = internal_zone_config,
                                           hosted_zone_tags   = TagsRoute53)

######################## Outputs ########################
t.InternalHostedZoneId = output(t.InternalHostedZone)

if __name__ == "__main__":
    print t.to_json()
