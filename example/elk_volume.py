import sys
from common import *

######################## Template ########################
t = template("ELK stack - Data Volume")

######################## Parameters ########################
t.Deployment = deployment_parameter

t.ElkHost         = string_parameter(description="ID of the ELK EC2 instance")
t.ElkVolumeDevice = volume_device_parameter
t.ElkVolumeSize   = volume_size_parameter # Used only in dev and stage
t.ElkVolume       = volume_parameter      # Used only in prod

######################## Python Constants ########################
# Read parameters from command line
deployment = sys.argv[1]
assert deployment in ('dev', 'stage', 'prod')

is_prod = deployment == 'prod'

# Tags
TagsElk = tags_base(t.Deployment) + tag(Name=fn.join('-', [StackName, 'elk']))

######################## Resources ########################
if not is_prod:
    # in dev/stage, we create a volume inside the stack
    # so that it is always deleted with the stack
    t.ElkVolumeInternal = ec2.volume(ZONE,
                             volume_type = 'gp2',
                             size = t.ElkVolumeSize,
                             tags = TagsElk)

# Volume Attachment
elk_volume = t.ElkVolume if is_prod else t.ElkVolumeInternal

t.ElkVolumeAttachment = ec2.volume_attachment(instance_id = t.ElkHost,
                                              volume_id   = elk_volume,
                                              device      = t.ElkVolumeDevice)

if __name__ == "__main__":
    print t.to_json()
