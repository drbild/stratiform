from common import *

######################## Template ########################
t = template("NAT Route stack - Route")

######################## Parameters ########################
t.Deployment        = deployment_parameter

t.NatHost           = string_parameter(description="Id of the NAT EC2 instance")
t.NatRouteTable     = route_table_parameter

######################## Python Constants ########################
# Tags
TagsNat = tags_base(t.Deployment) + tag(Name=fn.join('-', [StackName, 'nat']))

######################## Resources ########################
t.NatRoute = ec2.route(cidr_all,
                       instance_id = t.NatHost,
                       route_table_id = t.NatRouteTable)

if __name__ == "__main__":
    print t.to_json()
