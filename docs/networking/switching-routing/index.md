---
tags:
  - networking
---
# Networking — Switching & Routing

```bash
show vlan brief
show vlan id <id>
show interfaces trunk
show interface <int> status
```


```text title="Expected output"
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/1, Fa0/2, Fa0/3, Fa0/4
10   Management                       active    Fa0/5, Fa0/6
20   Production                       active    Fa0/7, Fa0/8, Fa0/9, Fa0/10
30   Guest                            suspended Fa0/11
100  DMZ                              active    Fa0/12, Gi0/1

VLAN ID  Name                             Status    Ports
-------- -------------------------------- --------- -------------------------------
20       Production                       active    Fa0/7, Fa0/8, Fa0/9, Fa0/10

Port        Mode             Encapsulation  Status        Native vlan
Fa0/1       on               802.1q         trunking      1
Fa0/2       on               802.1q         trunking      1
Gi0/1       on               802.1q         trunking      1

Interface      Status       Protocol
Fa0/1          connected    up
Fa0/2          notconnect   down
Fa0/3          connected    up
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the exact command syntax for your switch model; some platforms use `show vlan brief` while others require `show vlan`.
    **`% Incomplete command`** — Provide the complete VLAN ID number after `show vlan id` (e.g., `show vlan id 20`).
```bash
interface <int>
  switchport mode trunk
  switchport trunk allowed vlan <id1>,<id2>
  switchport trunk native vlan <native_id>
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in interface configuration mode by running `configure terminal` then `interface <int>` before entering switchport commands.
    **`% Incomplete command`** — Ensure all VLAN IDs are numeric and comma-separated without spaces (e.g., `switchport trunk allowed vlan 10,20,30`).
```bash
switchport trunk allowed vlan add <id>
switchport trunk allowed vlan remove <id>
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in interface configuration mode with `configure terminal` and `interface <port>` before running switchport commands.
    **`% Incomplete command`** — Replace `<id>` with an actual VLAN ID number (e.g., `switchport trunk allowed vlan add 100`).
```bash
# Confirm VLAN exists
show vlan brief | include <id>

# Confirm port is in correct VLAN
show interface <int> status

# Confirm VLAN crosses trunk
show interfaces trunk | include <id>

# End-to-end test
ping <ip_on_same_vlan>
```

```text title="Expected output"
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
100  Production-VLAN                  active    Fa0/1, Fa0/2, Fa0/3, Fa0/24

Name                         Status       Vlan
FastEthernet0/1              connected    trunk
FastEthernet0/2              connected    100
FastEthernet0/3              connected    100

Port        Vlans allowed on trunk
Fa0/1       1,100,200,300,1002-1005
Fa0/2       1-4094

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.100.45, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/4 ms
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the VLAN ID syntax matches your device OS (Cisco IOS uses `show vlan id <number>`, not `include`).
    **`Destination Host Unreachable.`** — Confirm the target IP is actually on the same VLAN and the device is powered on and reachable.
    **`% Ambiguous command: "show interfaces trunk"`** — Use the exact command syntax for your platform; some devices require `show trunk` or `show spanning-tree vlan`.
```bash
configure terminal
vlan <id>
  name <vlan_name>
exit
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Ensure you are in privileged EXEC mode (enable) before entering configure terminal.
    **`% VLAN <id> does not exist`** — Create the VLAN first with the global config command `vlan <id>` before attempting to name it.
```bash
interface <int>
  switchport mode access
  switchport access vlan <id>
  description <description>
  no shutdown
exit
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify that `<int>`, `<id>`, and `<description>` are replaced with actual values (e.g., `interface GigabitEthernet0/0/1`) and that no angle brackets remain in the command.
    **`% Interface does not exist.`** — Confirm the interface name matches your device's nomenclature by running `show interfaces` to list available interfaces.
```bash
interface <int>
  switchport mode trunk
  switchport trunk encapsulation dot1q    # if required by platform
  switchport trunk native vlan <native_id>
  switchport trunk allowed vlan <id1>,<id2>,<id3>
  no shutdown
exit
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify you are in interface configuration mode (use `configure terminal` then `interface <int>`) before entering switchport commands.
    **`% Incomplete command`** — Ensure all VLAN IDs in the `allowed vlan` list are valid integers separated by commas with no spaces (e.g., `1,10,20` not `1, 10, 20`).
    **`% Invalid input detected`** — Confirm the native VLAN ID exists and is not already assigned to another interface; use `show vlan` to verify available VLANs.
```bash
interface <int>
  switchport trunk allowed vlan add <id>
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the interface name syntax matches your device model (e.g., `GigabitEthernet0/0/1` or `Ethernet1/1`) and that you are in interface configuration mode.
    **`% VLAN <id> does not exist.`** — Create the VLAN first using `vlan <id>` in global configuration mode before adding it to the trunk.
```bash
interface <int>
  switchport trunk allowed vlan remove <id>
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the interface name syntax matches your device model (e.g., `GigabitEthernet0/0/1` or `Ethernet1/1`) and that you are in interface configuration mode.
    **`% VLAN <id> is not in the allowed list for this trunk.`** — Confirm the VLAN ID exists in the current allowed list using `show interface <int> trunk` before attempting removal.
```bash
copy running-config startup-config
# or (NX-OS)
copy running-config startup-config vdc-all
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command`** — Ensure you are in privileged EXEC mode (enable) before running copy commands.
    **`% Error opening destination file`** — Verify the startup-config file system has write permissions and sufficient space available.
```bash
# Confirm VLAN exists
show vlan brief | include <id>

# Confirm port VLAN assignment
show interface <int> status

# Confirm trunk carries VLAN
show interfaces trunk | include <id>

# Confirm VLAN on both sides of a trunk
# (Run on both switches)
```

```text title="Expected output"
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
10   Management                       active    Gi0/1, Gi0/2, Gi0/3
20   Sales                            active    Gi0/5, Gi0/6
30   Engineering                      active    Gi0/7, Gi0/8, Gi0/9
40   Guest                            suspended Gi0/10

Interface            Status       Protocol
Gi0/5                connected    up
Gi0/6                notconnect   down
Gi0/7                connected    up

Port        Mode             Encapsulation  Status        Native vlan
Gi0/24      on               802.1q         trunking      1
Gi0/48      on               802.1q         trunking      1

VLAN ID  10
  Port Gi0/24 (trunking)
  Port Gi0/48 (trunking)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the exact command syntax for your switch model (Cisco IOS uses `show vlan id <id>` instead of `include`).
    **`% Incomplete command`** — Replace `<int>` and `<id>` with actual interface names (e.g., `Gi0/5`) and VLAN numbers (e.g., `10`).
    **`VLAN <id> does not exist`** — Create the VLAN first using `vlan <id>` in global configuration mode before checking trunk membership.
```bash
ip route show
ip route get <destination_ip>    # show which route would be used
```
```cmd
route print
```
```bash
show ip route
show ip route <destination>
show ip route summary
```

```text title="Expected output"
Codes: K - kernel route, C - connected, S - static, R - RIP, B - BGP
       O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - nssa-external, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is 10.0.0.1 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 10.0.0.1, 00:15:32, GigabitEthernet0/0/0
C     10.0.0.0/24 is directly connected, GigabitEthernet0/0/0
L     10.0.0.5/32 is directly connected, GigabitEthernet0/0/0
O     192.168.1.0/24 [110/65] via 10.0.0.1, 00:12:45, GigabitEthernet0/0/0
O     192.168.2.0/24 [110/130] via 10.0.0.1, 00:12:40, GigabitEthernet0/0/0
B     172.16.0.0/16 [20/0] via 10.0.0.2, 00:08:19, GigabitEthernet0/0/1

Route Summary for VRF "default" (1 OSPF process):
*OSPF process 1, distance 110
  Intra-area: 2 routes, Intra-area summary: 0 routes
  Inter-area: 0 routes, Inter-area summary: 0 routes
  External type 1: 0 routes, External type 2: 1 routes
  NSSA External type 1: 0 routes, NSSA External type 2: 0 routes
  Redistributed: 0 routes
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the destination IP address format is valid (e.g., `show ip route 192.168.1.0`).
    **`% Incomplete command.`** — Complete the command with a valid destination address or use `show ip route` without parameters to display all routes.
```bash
# Linux — confirm default route
ip route show default

# Windows
route print 0.0.0.0
```

```text title="Expected output"
# Linux output:
default via 192.168.1.1 dev eth0 proto dhcp metric 100

# Windows output:
===========================================================================
Interface List
  1...00 1a 2b 3c 4d 5e ......Intel(R) Ethernet Connection (2) I219-LM
  2...00 1a 2b 3c 4d 5f ......Realtek PCIe GbE Family Controller
===========================================================================

IPv4 Route Table
===========================================================================
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0      192.168.1.1    192.168.1.100    25
===========================================================================
```

!!! warning "Common errors"
    **`RTNETLINK answers: Operation not permitted`** — Run the command with `sudo` or as root user.
    **`The system cannot find the file specified.`** — On Windows, ensure you're running Command Prompt or PowerShell with administrator privileges.
```bash
# Check OSPF neighbor state
show ip ospf neighbor

# Verify OSPF routes
show ip route ospf

# OSPF interface status
show ip ospf interface brief
```

```text title="Expected output"
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.0.0.1        1     FULL/DR         00:00:32    192.168.1.1     GigabitEthernet0/0/0
10.0.0.2        1     FULL/BDR        00:00:35    192.168.1.2     GigabitEthernet0/0/1
10.0.0.3        0     INIT/DROTHER    00:00:38    192.168.2.1     GigabitEthernet0/0/2

O       10.1.0.0/24 [110/65] via 192.168.1.1, 00:12:45, GigabitEthernet0/0/0
O       10.2.0.0/24 [110/128] via 192.168.1.2, 00:08:22, GigabitEthernet0/0/1
O       10.3.0.0/24 [110/192] via 192.168.1.1, 00:05:10, GigabitEthernet0/0/0

Interface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C
Gi0/0/0      1     0.0.0.0         192.168.1.254/24   1     DR    2/2
Gi0/0/1      1     0.0.0.0         192.168.1.253/24   1     BDR   1/1
Gi0/0/2      1     0.0.0.1         192.168.2.254/24   10    DR    0/0
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the device is in privileged EXEC mode (use `enable` command) and the OSPF process is configured.
    **`% OSPF process not running`** — Enable OSPF routing with `router ospf <process-id>` and configure at least one network statement.
    **`Neighbor ID     Pri   State           Dead Time   Address         Interface`** (header only, no neighbors listed) — Verify OSPF is enabled on interfaces with `ip ospf <process-id> area <area-id>` and check physical link status with `show interface`.
```bash
# BGP summary (neighbor states)
show bgp summary
show bgp neighbors <ip>

# BGP routes
show bgp
show bgp routes
```

```text title="Expected output"
BGP router identifier 192.168.1.1, local AS number 65001

Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
10.0.1.254      4 65002    1247    1251       42    0    0 00:45:23       1205
10.0.2.254      4 65003     892     895       42    0    0 00:32:15        847
10.1.1.1        4 65004    2156    2159       42    0    0 02:18:47       3421
10.1.2.1        4 65005     445     448       42    0    0 00:15:32 Idle (Admin)

BGP table version is 42, main routing table version 42
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal
Origin codes: i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.0/24      10.0.1.254               0             0 65002 i
*> 10.1.0.0/24      10.0.2.254             100             0 65003 65004 i
*> 172.16.0.0/16    10.1.1.1                50             0 65004 i
*> 192.168.0.0/16   10.1.2.1               200             0 65005 i
...
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the exact command syntax for your device OS (Cisco IOS uses `show ip bgp`, Juniper uses `show route protocol bgp`).
    **`% BGP not enabled`** — Enable BGP with `router bgp <AS-number>` in configuration mode before running show commands.
```bash
# Linux — add a static route
ip route add <network>/<prefix> via <gateway>

# Persist (add to /etc/network/interfaces or nmcli)
nmcli connection modify <conn> +ipv4.routes "<network>/<prefix> <gateway>"
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: unknown or ambiguous command 'route'.`** — Ensure you're using `ip route` (not just `route`) and that the iproute2 package is installed.
    **`Error: connection '<conn>' not found.`** — Replace `<conn>` with an actual connection name from `nmcli connection show` output.
```bash
traceroute <destination>    # Linux
tracert <destination>       # Windows
```

```text title="Expected output"
traceroute to example.com (93.184.216.34), 30 hops max, 60 byte packets
 1  gateway.local (192.168.1.1)  2.341 ms  2.156 ms  2.089 ms
 2  isp-router.net (10.0.0.1)  8.923 ms  9.104 ms  8.756 ms
 3  core-backbone-01.isp.net (203.0.113.45)  15.234 ms  15.678 ms  15.412 ms
 4  transit-peer-02.net (198.51.100.22)  22.891 ms  23.145 ms  22.567 ms
 5  example.com (93.184.216.34)  28.734 ms  28.456 ms  28.912 ms
```

!!! warning "Common errors"
    **`traceroute: command not found`** — Install traceroute using `apt-get install traceroute` (Debian/Ubuntu) or `yum install traceroute` (RHEL/CentOS).
    **`traceroute: getaddrinfo: Name or service not known`** — Verify the destination hostname or IP address is correct and that DNS resolution is working with `nslookup <destination>`.
    **`* * *` (all hops timing out)** — Check firewall rules blocking ICMP packets; the destination or intermediate routers may be configured to drop traceroute probes.
```bash
# Capture current route table
ip route show > /tmp/routes-before.txt

# Capture traceroute to critical destinations
traceroute <production_host> >> /tmp/routes-before.txt
traceroute <storage_vip> >> /tmp/routes-before.txt
traceroute <replication_peer> >> /tmp/routes-before.txt
```

```text title="Expected output"
default via 192.168.1.1 dev eth0 proto kernel scope link src 192.168.1.45
10.0.0.0/8 via 10.20.30.1 dev eth1 proto static
172.16.0.0/12 via 10.20.30.2 dev eth1 proto static
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.45
traceroute to prod-app-01.internal (10.50.100.42), 30 hops max, 60 byte packets
 1  gateway.local (192.168.1.1)  2.145 ms  1.987 ms  2.034 ms
 2  core-router-01.dc1 (10.20.30.1)  8.432 ms  8.521 ms  8.389 ms
 3  prod-app-01.internal (10.50.100.42)  12.654 ms  12.701 ms  12.589 ms
traceroute to storage-vip.internal (10.60.50.100), 30 hops max, 60 byte packets
 1  gateway.local (192.168.1.1)  1.876 ms  1.923 ms  1.945 ms
 2  core-router-01.dc1 (10.20.30.1)  7.234 ms  7.189 ms  7.301 ms
 3  storage-vip.internal (10.60.50.100)  15.432 ms  15.501 ms  15.378 ms
traceroute to repl-peer-02.internal (10.70.20.55), 30 hops max, 60 byte packets
 1  gateway.local (192.168.1.1)  2.012 ms  1.998 ms  2.045 ms
 2  core-router-01.dc1 (10.20.30.1)  8.876 ms  8.923 ms  8.801 ms
 3  repl-peer-02.internal (10.70.20.55)  18.234 ms  18.156 ms  18.301 ms
```

!!! warning "Common errors"
    **`bash: traceroute: command not found`** — Install traceroute with `apt-get install traceroute` (Debian/Ubuntu) or `yum install traceroute` (RHEL/CentOS).
    **`traceroute: sendto: Operation not permitted`** — Run the script with `sudo` or ensure the user has CAP_NET_RAW capability.
    **`Cannot open /tmp/routes-before.txt: Permission denied`** — Verify /tmp is writable with `ls -ld /tmp` and check disk space with `df /tmp`.
```bash
# Compare route tables
ip route show > /tmp/routes-after.txt
diff /tmp/routes-before.txt /tmp/routes-after.txt

# Confirm specific routes still present
ip route get <destination>

# Trace paths to critical systems
traceroute <production_host>
traceroute <storage_vip>
```

```text title="Expected output"
1c1
< default via 192.168.1.1 dev eth0 proto dhcp metric 100
---
> default via 192.168.1.1 dev eth0 proto static metric 100
3a4
> 10.50.0.0/16 via 192.168.2.254 dev eth1 metric 50
10.0.0.0/8 via 192.168.1.254 dev eth0 proto kernel scope link src 10.0.5.42

10.20.30.0/24 dev eth0 proto kernel scope link src 10.20.30.15 metric 256

traceroute to prod-db-01.internal (10.50.12.88), 30 hops max, 60 byte packets
 1  gateway.local (192.168.1.1)  2.145 ms  2.089 ms  2.156 ms
 2  core-switch-01.internal (10.0.0.1)  5.234 ms  5.198 ms  5.267 ms
 3  prod-db-01.internal (10.50.12.88)  12.456 ms  12.389 ms  12.521 ms

traceroute to storage-vip.internal (10.50.100.5), 30 hops max, 60 byte packets
 1  gateway.local (192.168.1.1)  1.987 ms  1.945 ms  2.012 ms
 2  core-switch-01.internal (10.0.0.1)  4.156 ms  4.123 ms  4.189 ms
 3  storage-vip.internal (10.50.100.5)  8.734 ms  8.701 ms  8.789 ms
```

!!! warning "Common errors"
    **`diff: /tmp/routes-before.txt: No such file or directory`** — Run `ip route show > /tmp/routes-before.txt` before making network changes to capture the baseline state.
    **`traceroute: command not found`** — Install traceroute with `apt install traceroute` (Debian/Ubuntu) or `yum install traceroute` (RHEL/CentOS).
    **`ICMP Host Unreachable`** — Verify the destination IP is correct and that firewall rules permit ICMP traffic to the target host.
```bash
ip route show default
ping <gateway_ip>
```

```text title="Expected output"
default via 192.168.1.1 dev eth0 proto static metric 100
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=1.89 ms
64 bytes from 192.168.1.1: icmp_seq=3 ttl=64 time=2.12 ms
^C
--- 192.168.1.1 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/stddev = 1.89/2.11/2.34/0.18 ms
```

!!! warning "Common errors"
    **`ping: connect: Network is unreachable`** — Verify the default route exists with `ip route show` and check that the network interface is up with `ip link show`.
    **`ping: Name or service not known`** — Replace `<gateway_ip>` with an actual IP address (e.g., `192.168.1.1`) instead of a placeholder variable.
    **`PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.` followed by no responses and timeout** — Check gateway connectivity with `ip neighbor show` and verify the interface has a valid IP address using `ip addr show`.
```bash
show ip ospf neighbor            # all neighbors in FULL state
show ip ospf neighbor <id>       # specific neighbor detail
show ip route ospf               # routes learned via OSPF
```

```text title="Expected output"
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.0.0.1         1   FULL/DR         00:00:38    192.168.1.1     GigabitEthernet0/0
10.0.0.2         1   FULL/BDR        00:00:35    192.168.1.2     GigabitEthernet0/1
10.0.0.3         0   FULL/DROTHER    00:00:39    192.168.1.3     GigabitEthernet0/2
10.0.0.5         1   2WAY/DROTHER    00:00:37    192.168.1.5     GigabitEthernet0/3

Neighbor 10.0.0.1, interface address 192.168.1.1
    In the area 0.0.0.0 via interface GigabitEthernet0/0
    Neighbor priority is 1, State is FULL, 6 state changes
    DR is 10.0.0.1 BDR is 10.0.0.2
    Options is 0x12 *|E|-
    Dead timer due in 00:00:38
    Neighbor is up for 02:14:52

O       10.2.0.0/24 [110/65] via 192.168.1.1, 00:45:23, GigabitEthernet0/0
O       10.3.0.0/24 [110/130] via 192.168.1.2, 00:32:15, GigabitEthernet0/1
O       10.4.0.0/24 [110/195] via 192.168.1.3, 01:12:08, GigabitEthernet0/2
O IA    172.16.0.0/16 [110/256] via 192.168.1.1, 00:28:44, GigabitEthernet0/0
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the command syntax matches your IOS version; some devices use `show ip ospf neighbor detail` instead of `show ip ospf neighbor <id>`.
    **`% Incomplete command.`** — Ensure OSPF is enabled with `router ospf <process-id>` and at least one network is configured in the OSPF process.
```bash
show bgp summary                  # peer state: Established
show bgp neighbors <ip> routes    # routes received from peer
```

```text title="Expected output"
BGP router identifier 10.0.1.1, local AS number 65001

Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
10.20.30.40     4 65002    1247    1251       89    0    0 00:42:15       156
10.20.30.41     4 65002    1089    1092       89    0    0 00:38:22       142
10.50.60.70     4 65003     892     895       89    0    0 00:31:08   Idle (Admin)

Total number of neighbors 3

For address family: IPv4 Unicast
Neighbor        Prefix Received Sent  Best Paths
10.20.30.40          156      0    156
10.20.30.41          142      0    142
10.50.60.70            0      0      0
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the correct syntax for your router OS (Cisco IOS uses `show ip bgp summary`, Juniper uses `show bgp summary`).
    **`% Neighbor not found`** — Confirm the neighbor IP address is configured and the BGP session is established before querying its routes.
    **`Connection refused` or `% Connection timeout`** — Ensure the management interface is reachable and SSH/Telnet access is enabled on the router.
```bash
# Confirm key services reachable after routing change
nc -zv <storage_vip> 443    # storage management
nc -zv <vcenter_fqdn> 443   # vCenter
curl -k https://<app_vip>/  # application VIP
```

```text title="Expected output"
Connection to 192.168.50.45 443 port [tcp/https] succeeded!
Connection to vcenter.prod.local 443 port [tcp/https] succeeded!
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   1247  100   1247    0     0   2840      0 --:--:-- --:--:-- --:--:-- --:--:--
<!DOCTYPE html>
<html>
<head><title>Application Portal</title></head>
<body>Welcome to App VIP</body>
</html>
```

!!! warning "Common errors"
    **`nc: connect to 192.168.50.45 port 443 (tcp) failed: Connection timed out`** — Verify the storage VIP is reachable by checking routing table (`ip route show`) and confirming firewall rules allow port 443 from your management network.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to curl (already present) or import the application's CA certificate into your system trust store if certificate validation is required.
    **`nc: getaddrinfo for host "vcenter.prod.local" failed: Name or service not known`** — Confirm DNS resolution is working by testing `nslookup vcenter.prod.local` and verify your `/etc/resolv.conf` points to the correct nameserver.
```bash
# Linux — ipcalc
ipcalc 10.10.10.0/24

# Python one-liner
python3 -c "import ipaddress; n = ipaddress.ip_network('10.10.10.0/24'); print(n.network_address, n.broadcast_address, n.num_addresses)"
```

```text title="Expected output"
Address:   10.10.10.0
Netmask:   255.255.255.0
Broadcast: 10.10.10.255
Hostmin:   10.10.10.1
Hostmax:   10.10.10.254
Hosts/Net: 254

10.10.10.0 10.10.10.255 256
```

!!! warning "Common errors"
    **`command not found: ipcalc`** — Install ipcalc with `apt-get install ipcalc` (Debian/Ubuntu) or `yum install ipcalc` (RHEL/CentOS).
    **`ModuleNotFoundError: No module named 'ipaddress'`** — Upgrade to Python 3.3+ or install the backport with `pip install ipaddress`.
```bash
ipcalc 10.10.10.45/24
# Returns: network, broadcast, first/last usable host
```

```text title="Expected output"
Address:   10.10.10.45
Netmask:   255.255.255.0 = 24
Wildcard:  0.0.0.255
Network:   10.10.10.0/24
HostMin:   10.10.10.1
HostMax:   10.10.10.254
Broadcast: 10.10.10.255
Hosts/Net: 254
```

!!! warning "Common errors"
    **`ipcalc: command not found`** — Install ipcalc with `apt-get install ipcalc` (Debian/Ubuntu) or `yum install ipcalc` (RHEL/CentOS).
    **`ipcalc: invalid address 10.10.10.45/24`** — Verify the CIDR notation is correct; use a valid IP address and prefix length (e.g., `ipcalc 10.10.10.45/24`).
```bash
python3 -c "
import ipaddress
a = ipaddress.ip_address('10.10.10.45')
b = ipaddress.ip_address('10.10.10.200')
net = ipaddress.ip_network('10.10.10.0/24')
print(a in net, b in net)
"
```

```text title="Expected output"
True False
```

!!! warning "Common errors"
    **`ModuleNotFoundError: No module named 'ipaddress'`** — Install Python 3.3+ or use `python3 -m pip install ipaddress` on older Python versions (ipaddress is built-in for Python 3.3+, so verify your Python version with `python3 --version`).
    **`SyntaxError: invalid syntax`** — Ensure you're using `python3` not `python` (which may point to Python 2), or check that the multi-line string is properly quoted with matching single or double quotes.
```bash
# Linux — show all routes
ip route show

# Check for overlap manually or with ipcalc
ipcalc <new_network>/<prefix>
```

```text title="Expected output"
default via 192.168.1.1 dev eth0 proto dhcp metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.50 metric 100
10.0.0.0/8 via 192.168.1.254 dev eth0 metric 50
172.16.0.0/12 dev tun0 proto none scope link metric 1000
fe80::/64 dev eth0 proto kernel metric 256 pref medium

Address:   10.20.30.0
Netmask:   255.255.255.0
Broadcast: 10.20.30.255
Network:   10.20.30.0/24
HostMin:   10.20.30.1
HostMax:   10.20.30.254
Hosts/Net: 254
```

!!! warning "Common errors"
    **`command not found: ipcalc`** — Install ipcalc with `apt install ipcalc` (Debian/Ubuntu) or `yum install ipcalc` (RHEL/CentOS).
    **`CIDR <new_network>/<prefix>: Invalid CIDR address`** — Verify the network address is valid (e.g., `10.20.30.0/24` not `10.20.30.5/24`).
```bash
ip addr show
ip addr show <interface>
ip addr add <ip>/<prefix> dev <interface>
ip route add default via <gateway>
```
```powershell
Get-NetIPAddress
Get-NetIPConfiguration
ipconfig /all
```
```bash
# Test TCP port reachability
nc -zv <host> <port>
telnet <host> <port>

# PowerShell
Test-NetConnection <host> -Port <port>
```

```text title="Expected output"
Connection to 192.168.1.42 22 port [tcp/ssh] succeeded!
Trying 192.168.1.42...
Connected to 192.168.1.42.
Escape character is '^]'.
SSH-2.0-OpenSSH_7.4

TNComputerName   : db-server-01.corp.local
RemoteAddress    : 192.168.1.42
RemotePort       : 22
InterfaceAlias   : Ethernet
SourceAddress    : 192.168.1.100
TcpTestSucceeded : True
```

!!! warning "Common errors"
    **`nc: getaddrinfo: Name or service not known`** — Verify the hostname is correct and resolvable with `nslookup <host>` or check DNS configuration.
    **`Connection refused`** — Confirm the service is running on the target port with `ss -tlnp | grep <port>` on the remote host.
    **`No route to host`** — Check network connectivity and firewall rules with `ping <host>` and verify the route exists using `ip route show`.
```bash
# Linux
ss -tnp         # TCP connections with process info
ss -tnlp        # listening ports
netstat -tnp    # legacy equivalent

# Windows
netstat -ano
Get-NetTCPConnection
```

```text title="Expected output"
# Linux output from ss -tnp
State      Recv-Q Send-Q Local Address:Port       Peer Address:Port Process
ESTAB      0      0      192.168.1.45:22         203.0.113.12:54321 users:(("sshd",pid=2847,fd=3))
ESTAB      0      0      192.168.1.45:443        198.51.100.8:49152 users:(("nginx",pid=1203,fd=12))
LISTEN     0      128    0.0.0.0:22              0.0.0.0:*        users:(("sshd",pid=891,fd=4))
LISTEN     0      511    127.0.0.1:5432          0.0.0.0:*        users:(("postgres",pid=3421,fd=5))

# Linux output from ss -tnlp
State      Recv-Q Send-Q Local Address:Port       Peer Address:Port Process
LISTEN     0      128    0.0.0.0:22              0.0.0.0:*        users:(("sshd",pid=891,fd=4))
LISTEN     0      511    127.0.0.1:5432          0.0.0.0:*        users:(("postgres",pid=3421,fd=5))
LISTEN     0      128    0.0.0.0:80              0.0.0.0:*        users:(("nginx",pid=1203,fd=8))

# Windows output from netstat -ano
Proto  Local Address          Foreign Address        State           PID
TCP    0.0.0.0:22             0.0.0.0:0              LISTENING       2847
TCP    192.168.1.100:443      203.0.113.12:54321     ESTABLISHED     1203
TCP    127.0.0.1:5432         0.0.0.0:0              LISTENING       3421
TCP    0.0.0.0:80             0.0.0.0:0              LISTENING       891

# Windows output from Get-NetTCPConnection
LocalAddress      LocalPort RemoteAddress RemotePort State       OwningProcess
0.0.0.0           22        0.0.0.0       0          Listen      2847
192.168.1.100     443       203.0.113.12  54321      Established 1203
127.0.0.1         5432      0.0.0.0       0          Listen      3421
```

!!! warning "Common errors"
    **`ss: No such file or directory`** — Install iproute2 package with `apt install iproute2` (Debian/Ubuntu) or `yum install iproute2` (RHEL/CentOS).
    **`netstat: command not found`** — Install net-tools with `apt install net-tools` or use `ss` instead, which is the modern replacement.
    **`Access denied` (Windows)** — Run PowerShell or Command Prompt as Administrator to view all process information.
```bash
# Check interface MTU
ip link show <interface>

# Test path MTU (don't-fragment bit)
ping -M do -s 1472 <destination>    # 1500 MTU test
ping -M do -s 8972 <destination>    # 9000 MTU test

# Windows
ping /f /l 1472 <destination>
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
