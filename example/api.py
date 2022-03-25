import sys
from common import *

######################## Template ########################
t = template("API stack - ELB and EC2 Host")

######################## Parameters ########################
t.Deployment   = deployment_parameter
t.Key          = key_parameter

t.ApiInstanceType   = instance_type_parameter
t.ApiAmi            = ami_parameter
t.ApiSubnet         = subnet_parameter
t.ApiSecurityGroups = security_groups_parameter
t.ApiHostedZone     = hosted_zone_parameter
t.ApiFqdn           = fqdn_parameter

t.ElbSubnets        = subnets_parameter
t.ElbSecurityGroups = security_groups_parameter
t.ElbFqdn           = fqdn_parameter

t.SslCertArn        = string_parameter(description="ARN for SSL cert for API")

######################## Python Constants ########################

# Read parameters from command line
deployment = sys.argv[1]
assert deployment in ('dev', 'stage', 'prod')

# Constants
ELB_HOSTED_ZONE = "example.com."
PATH = fn.join('/', ["", t.Deployment, 'internal', 'example', 'ec2', ""])

# Tags
TagsApi = tags_base(t.Deployment) + tag(Name=fn.join('-', [StackName, 'api']))

######################## Resources ########################
# Host resource
t.ApiRole              = iam.role(assume_role_policy_document = load_policy('role_api.yml'),
                                  path                        = PATH)

t.ReadApiSecretsPolicy = iam.policy(policy_name     = "read-api-secrets",
                                    policy_document = load_policy('read_api_secrets.yml', {'deployment' : deployment}),
                                    roles           = [ref(t.ApiRole)])

t.ApiInstanceProfile   = iam.instance_profile(path  = PATH,
                                              roles = [ref(t.ApiRole)])

api_host_iface = ec2.network_interface_property(device_index          = 0,
                                                delete_on_termination = True,
                                                subnet_id             = t.ApiSubnet,
                                                group_set             = ref(t.ApiSecurityGroups))

t.ApiHost = ec2.instance(instance_type        = t.ApiInstanceType,
                         image_id             = t.ApiAmi,
                         key_name             = t.Key,
                         iam_instance_profile = t.ApiInstanceProfile,
                         network_interfaces   = [api_host_iface],
                         tags                 = TagsApi)

# ELB resources
listener = elb.Listener(instance_port = 80,
                        instance_protocol = "HTTP",
                        load_balancer_port = 443,
                        protocol = "HTTPS",
                        policy_names = ['common-ssl-negotiation-policy-strict'],
                        ssl_certificate_id = ref(t.SslCertArn))

healthcheck = elb.HealthCheck(healthy_threshold = 2,
                              interval = 10,
                              target = "HTTP:80/",
                              timeout = 5,
                              unhealthy_threshold = 10)

t.Elb      = elb.LoadBalancer(instances = [ref(t.ApiHost)],
                              listeners = [listener],
                              health_check = healthcheck,
                              policies = [elb_ssl_negotiation_policy_strict],
                              security_groups = ref(t.ElbSecurityGroups),
                              subnets = t.ElbSubnets,
                              tags = TagsApi)

# Route53 resources
t.ApiHostRecordSet = route53.record_set(hosted_zone_id   = t.ApiHostedZone,
                                        name             = t.ApiFqdn,
                                        type             = 'A',
                                        ttl              = 60,
                                        resource_records = [fn.get_att(t.ApiHost, 'PrivateIp')])

t.ElbRecordSet     = route53.record_set(hosted_zone_name  = ELB_HOSTED_ZONE,
                                        name              = t.ElbFqdn,
                                        type              = 'CNAME',
                                        ttl               = 60,
                                        resource_records  = [fn.get_att(t.Elb, 'DNSName')])

######################## Outputs ########################
t.ApiInstanceId = output(value = t.ApiHost)
t.ElbId         = output(value = t.Elb)
t.ElbDnsName    = output(value = fn.get_att(t.Elb, 'DNSName'))

if __name__ == "__main__":
    print t.to_json()
