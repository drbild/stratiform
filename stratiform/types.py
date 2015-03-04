# Copyright 2015 David R. Bild
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import re

from stratiform.common import AWSObject, prop

class Wrap(object):
    def __init__(self, wrap):
        self.wrap = wrap

    def __str__(self):
        return str(self.wrap)

    def __json__(self):
        return self.wrap

class WrapList(object):
    def __init__(self, *args):
        wrap = []
        if len(args) == 1 and isinstance(wrap, list):
            wrap += args
        else:
            wrap = args
        super(WrapList, self).__init__(wrap)

class Version(Wrap):
    pass

class BgpAsn(Wrap):
    pass

class CIDR(Wrap):
    pass

class IpProtocol(Wrap):
    pass

class IpAddress(Wrap):
    pass

class PortRange(AWSObject):
    @staticmethod
    def props():
        return [prop('From', attr='from_port'),
                prop('To', attr='to_port')]

    def __init__(self, ports):
        ports = str(ports)
        match = re.compile(r'^(\d+)(?:-+(\d+))?$').match(ports)
        from_port = match.groups()[0]
        to_port   = match.groups()[1] or from_port
        super(PortRange, self).__init__(from_port=from_port, to_port=to_port)

    def from_port(self):
        return self.from_port

    def to_port(self):
        return self.to_port

class AclAction(Wrap):
    pass

class DomainName(Wrap):
    pass

class DomainNameServers(WrapList):
    pass

class VPCConnectionType(Wrap):
    pass

class AvailabilityZone(Wrap):
    pass

version = Version
cidr = CIDR
protocol = ip_protocol = IpProtocol
port = ports = port_range = PortRange
acl_action = AclAction
domain_name = DomainName
domain_name_servers = DomainNameServers
availability_zone = AvailabilityZone
