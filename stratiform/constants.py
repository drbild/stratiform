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

from stratiform.types import cidr, protocol, port, ports, availability_zone

# common CIDR constants
all_cidr = cidr("0.0.0.0/0")

# common IP protocol constants
icmp = protocol(1)
tcp  = protocol(6)
udp  = protocol(17)

# common TCP port numbers
all_ports             = ports("0-65535")
all_ephemeral_ports   = ports("1024-65535")
elb_ephemeral_ports   = ports("1024-65535")
linux_ephemeral_ports = ports("32768-61000")

ssh   = port(22)
smtp  = port(25)
dns   = port(53)
http  = port(80)
pop3  = port(110)
imap  = port(143)
ldap  = port(389)
https = port(443)
smtps = port(465)
imaps = port(993)
pop3s = port(995)
mssql = port(1433)
mysql = port(3306)
rdp   = port(3389)

# availability zones
us_west_2a = availability_zone("us-west-2a")
