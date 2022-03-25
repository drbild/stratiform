import sys
from common import *

def strip_suffix(s, suffix):
    import re
    return re.sub(re.escape(suffix) + '$', '', s)

######################## Template ########################
t = template("API stack - Security Groups")

######################## Parameters ########################
t.Deployment = deployment_parameter

t.Vpc        = vpc_parameter

######################## Python Constants ########################

# Read parameters from command line
deployment = sys.argv[1]
assert deployment in ('dev', 'stage', 'prod')

is_prod = deployment == 'prod'
is_stage = deployment == 'stage'

def nametag(name):
    return tags_base(t.Deployment) + tag(Name=fn.join('-', [StackName, name]))

def make_sg(name, description):
    tag = name.lower()
    return ec2.security_group(name, description, vpc_id=t.Vpc, tags=nametag(tag))

######################## Resources ########################
### first create all security groups, so they can be referenced in rules
t.CommonSg   = make_sg("common",   "Security group common to all hosts")
t.NatSg      = make_sg("nat",      "Security group for all NAT hosts")
t.BastionSg  = make_sg("bastion",  "Security group for all bastion hosts")
t.RegistrySg = make_sg("registry", "Security group for Docker registry hosts")
t.ElkSg      = make_sg("elk",      "Security group for all ELK hosts")
t.RdsSg      = make_sg("rds",      "Security group for the RDS hosts")
t.ApiSg      = make_sg("api",      "Security group for API hosts")
t.ApiElbSg   = make_sg("elb-api",  "Security group for API ELB instances")

### then add all rules, allowing cross-references
t.CommonSg   = t.CommonSg.ingress("SSH",     tcp, ssh,      t.BastionSg) \
                         .egress("HTTP",     tcp, http,     cidr_all)    \
                         .egress("HTTPS",    tcp, https,    cidr_all)    \
                         .egress("NTP",      udp, ntp,      cidr_all)    \
                         .egress("Logstash", tcp, logstash, t.ElkSg)

t.NatSg      = t.NatSg.ingress("HTTP",  tcp, http,      CIDR_PRIVATE) \
                      .ingress("HTTPS", tcp, https,     CIDR_PRIVATE) \
                      .ingress("SMTP",  tcp, port(587), CIDR_PRIVATE) \
                      .egress("HTTP",   tcp, http,      cidr_all)     \
                      .egress("HTTPS",  tcp, https,     cidr_all)     \
                      .egress("SMTP",   tcp, port(587), cidr_all)

t.BastionSg  = t.BastionSg.ingress("SSH",       tcp, ssh,        CIDR_EXT)   \
                          .egress("SSH",        tcp, ssh,        t.CommonSg) \
                          .egress("PostgreSQL", tcp, postgresql, t.RdsSg)

t.RegistrySg = t.RegistrySg.ingress("HTTP",  tcp, http,  t.CommonSg)

t.ElkSg      = t.ElkSg.ingress("Logstash",      tcp, logstash,      t.CommonSg) \
                      .ingress("Elasticsearch", tcp, elasticsearch, t.ElkSg)    \
                      .egress("Elasticsearch",  tcp, elasticsearch, t.ElkSg)

t.RdsSg      = t.RdsSg.ingress("PostgreSQLAPI",     tcp, postgresql, t.ApiSg) \
                      .ingress("PostgresQLBastion", tcp, postgresql, t.BastionSg)

t.ApiSg      = t.ApiSg.ingress("ELB",       tcp, http,       t.ApiElbSg) \
                      .egress("PostgreSQL", tcp, postgresql, t.RdsSg)    \
                      .egress("SMTP",       tcp, port(587),  cidr_all)

t.ApiElbSg   = t.ApiElbSg.ingress("HTTPS", tcp, https, cidr_all if is_prod else CIDR_EXT) \
                         .egress("HTTP",   tcp, http,  t.ApiSg)

######################## Outputs ########################
t.CommonSgId   = output(value = t.CommonSg)
t.NatSgId      = output(value = t.NatSg)
t.BastionSgId  = output(value = t.BastionSg)
t.RegistrySgId = output(value = t.RegistrySg)
t.ElkSgId      = output(value = t.ElkSg)
t.RdsSgId      = output(value = t.RdsSg)
t.ApiSgId      = output(value = t.ApiSg)
t.ApiElbSgId   = output(value = t.ApiElbSg)

if __name__ == "__main__":
    print t.to_json()
