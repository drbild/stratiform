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
from collections import OrderedDict as odict

class CIDR(object):
    def __init__(self, cidr):
        self.cidr = cidr

    def __json__(self):
        return self.cidr

class Protocol(object):
    def __init__(self, protocol):
        self.protocol = str(protocol)

    def __json__(self):
        return self.protocol

class AclPorts(object):
    def __init__(self, ports):
        ports = str(ports)
        match = re.compile(r'^(\d+)(?:-+(\d+))?$').match(ports)
        from_port = match.groups()[0]
        to_port   = match.groups()[1] or from_port
        self.port_range = odict([
            ('From', from_port),
            ('To', to_port)
        ])

    def __json__(self):
        return self.port_range

class AclAction(object):
    def __init__(self, action):
        self.action = action

    def __json__(self):
        return self.action

class Tenancy(object):
    def __init__(self, tenency):
        self.tenency = tenency

    def __json__(self):
        return self.tenency

def cidr(cidr):
    return CIDR(cidr)

def protocol(protocol):
    return Protocol(protocol)

def ports(ports):
    return AclPorts(ports)
port = ports

def acl_action(action):
    return AclAction(action)

def tenancy(tenancy):
    return Tenancy(tenancy)

# common CIDR constants
ALL_CIDR = cidr("0.0.0.0/0")

# common IP protocol constants
ICMP = protocol(1)
TCP  = protocol(6)
UDP  = protocol(17)

# common TCP port numbers
ALL_PORTS             = ports("0-65535")
ALL_EPHEMERAL_PORTS   = ports("1024-65535")
ELB_EPHEMERAL_PORTS   = ports("1024-65535")
LINUX_EPHEMERAL_PORTS = ports("32768-61000")

SSH   = port(22)
SMTP  = port(25)
DNS   = port(53)
HTTP  = port(80)
POP3  = port(110)
IMAP  = port(143)
LDAP  = port(389)
HTTPS = port(443)
SMTPS = port(465)
IMAPS = port(993)
POP3S = port(995)
MSSQL = port(1433)
MYSQL = port(3306)
RDP   = port(3389)

# ACL action constants
ALLOW = acl_action("allow")
DENY  = acl_action("deny")

# Instance tenancy constants
DEFAULT = tenancy("default")
DEDICATED = tenancy("dedicated")
