import sys
from common import *

######################## Template ########################
t = template("RDS stack - RDS Host")

######################## Parameters ########################
t.Deployment = deployment_parameter

t.RdsInstanceType = db_instance_type_parameter
t.RdsVolumeSize   = volume_size_parameter
t.RdsSubnets      = subnets_parameter
t.RdsSecurityGroups = security_groups_parameter
t.RdsHostedZone     = hosted_zone_parameter
t.RdsFqdn    = fqdn_parameter

t.RdsMasterUsername = string_parameter(description="Username for RDS master user.")
t.RdsMasterPassword = string_parameter(description="Password for RDS master user.")

######################## Python Constants ########################

# Constants
ENGINE = "postgres"
ENGINE_VERSION = "9.4.1"
STORAGE_TYPE = "gp2"

# Tags
TagsRds = tags_base(t.Deployment) + tag(Name=fn.join('-', [StackName, 'rds']))

######################## Resources ########################
t.RdsSubnetGroup = rds.db_subnet_group(db_subnet_group_description = "subnet group for RDS",
                                       subnet_ids = t.RdsSubnets,
                                       tags = TagsRds)

t.RdsHost = rds.db_instance(allocated_storage = t.RdsVolumeSize,
                            allow_major_version_upgrade = False,
                            auto_minor_version_upgrade = True,
                            backup_retention_period = 35, #days
                            db_instance_class = t.RdsInstanceType,
                            db_subnet_group_name = t.RdsSubnetGroup,
                            engine = ENGINE,
                            engine_version = ENGINE_VERSION,
                            master_username = t.RdsMasterUsername,
                            master_user_password = t.RdsMasterPassword,
                            port = postgresql.from_port,
                            publicly_accessible = False,
                            storage_encrypted = True,
                            storage_type = STORAGE_TYPE,
                            vpc_security_groups = ref(t.RdsSecurityGroups),
                            tags = TagsRds)

t.RdsHostRecordSet = route53.record_set(hosted_zone_id   = t.RdsHostedZone,
                                        name             = t.RdsFqdn,
                                        type             = 'CNAME',
                                        ttl              = 60,
                                        resource_records = [fn.get_att(t.RdsHost, 'Endpoint.Address')])

######################## Outputs ########################
t.RdsAddress = output(value = fn.get_att(t.RdsHost, 'Endpoint.Address'))
t.RdsPort    = output(value = fn.get_att(t.RdsHost, 'Endpoint.Port'))

if __name__ == "__main__":
    print t.to_json()
