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

from stratiform.base import AWSObject, prop
from stratiform.utils import Wrapper, ListWrapper

class AvailabilityZone(Wrapper):
    pass

class CIDR(Wrapper):
    pass
CIDR.all = CIDR("0.0.0.0/0")

class DomainName(Wrapper):
    pass

class IpProtocol(Wrapper):
    pass
IpProtocol.icmp = IpProtocol(1)
IpProtocol.tcp  = IpProtocol(6)
IpProtocol.udp  = IpProtocol(17)

class IpAddress(Wrapper):
    pass
IpAddress.localhost = IpAddress('127.0.0.1')

class PortRange(AWSObject):
    @staticmethod
    def props():
        return [prop('From', attr='from_port'),
                prop('To', attr='to_port')]

    def __init__(self, ports):
        match = re.compile(r'^(\d+)(?:-+(\d+))?$').match(str(ports))
        from_port = match.groups()[0]
        to_port   = match.groups()[1] or from_port
        super(PortRange, self).__init__(from_port=from_port, to_port=to_port)

    def from_port(self):
        return self.from_port

    def to_port(self):
        return self.to_port

PortRange.all             = PortRange("0-65535")
PortRange.ephemeral       = PortRange("1024-65535")
PortRange.ephemeral_elb   = PortRange("1024-65535")
PortRange.ephemeral_linux = PortRange("32768-61000")

PortRange.ssh   = PortRange(22)
PortRange.smtp  = PortRange(25)
PortRange.dns   = PortRange(53)
PortRange.http  = PortRange(80)
PortRange.pop3  = PortRange(110)
PortRange.imap  = PortRange(143)
PortRange.ldap  = PortRange(389)
PortRange.https = PortRange(443)
PortRange.smtps = PortRange(465)
PortRange.imaps = PortRange(993)
PortRange.pop3s = PortRange(995)
PortRange.mssql = PortRange(1433)
PortRange.mysql = PortRange(3306)
PortRange.rdp   = PortRange(3389)

#### Public API ####
az              = availability_zone = AvailabilityZone

address         = IpAddress
ip_localhost    = IpAddress.localhost

cidr            = CIDR
cidr_all        = CIDR.all

domain_name     = DomainName

port            = ports = port_range = PortRange
ports_all       = PortRange.all
ephemeral       = PortRange.ephemeral
ephemeral_elb   = PortRange.ephemeral_elb
ephemeral_linux = PortRange.ephemeral_linux
ssh             = PortRange.ssh   
smtp            = PortRange.smtp 
dns             = PortRange.dns   
http            = PortRange.http 
pop3            = PortRange.pop3 
imap            = PortRange.imap 
ldap            = PortRange.ldap 
https           = PortRange.https
smtps           = PortRange.smtps
imaps           = PortRange.imaps
pop3s           = PortRange.pop3s
mssql           = PortRange.mssql
mysql           = PortRange.mysql
rdp             = PortRange.rdp

protocol        = IpProtocol
icmp            = IpProtocol.icmp
tcp             = IpProtocol.tcp
udp             = IpProtocol.udp

__all__ = ['az', 'availability_zone', 'address', 'ip_localhost',
           'cidr', 'cidr_all', 'domain_name', 'port', 'ports',
           'port_range', 'ports_all', 'ephemeral', 'ephemeral_elb',
           'ephemeral_linux', 'ssh', 'smtp', 'dns', 'http', 'pop3',
           'imap', 'ldap', 'https', 'smtps', 'pop3s', 'mssql',
           'mysql', 'rdp', 'protocol', 'icmp', 'tcp', 'udp']
