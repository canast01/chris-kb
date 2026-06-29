---
tags:
  - networking
  - troubleshooting
search:
  boost: 1.5
---
# Network Connectivity Troubleshooting

<div class="kb-summary">
Network Connectivity Troubleshooting reference covering Overview, Failure Classification by OSI Layer, Diagnostic Flowchart, VLAN and Trunk Verification, Routing Table Verification and 6 more sections.
</div>

## Before you begin

- **Access:** Network admin credentials; console or SSH to devices
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Overview

Network failures must be diagnosed by layer — jumping straight to firewall rules wastes time when the issue is a downed physical link or a misconfigured VLAN. This guide follows the OSI model from physical through application, with enterprise tools for Linux, Windows, Cisco, and VMware ESXi environments.

---

## Failure Classification by OSI Layer

| Layer | Common Failure | First Symptom | Diagnostic Tool |
|---|---|---|---|
| L1 — Physical | Cable/SFP down | Link down LED; interface counters 0 | `ethtool eth0`; switch port light |
| L2 — Data Link | VLAN misconfiguration | Ping fails on same subnet | `ip link`; `show interfaces trunk` |
| L2 — Data Link | Spanning tree loop | Broadcast storm; high CPU on switch | `show spanning-tree` |
| L3 — Network | Routing missing | Can ping gateway, not remote host | `ip route`; `traceroute` |
| L3 — Network | ACL blocking | Traceroute shows *; ping fails | `show ip access-lists` |
| L4 — Transport | Firewall blocking port | TCP connect timeout | `nc -zv host port`; `telnet` |
| L4 — Transport | MTU mismatch | Large transfers fail; small ping ok | `ping -M do -s 8972` |
| L7 — Application | TLS certificate failure | HTTPS connection refused | `openssl s_client` |
| L7 — Application | DNS failure | Name not resolved | `dig`; `nslookup` |

---

## Diagnostic Flowchart

```d2
direction: right

A: "Connectivity Failure Reported" {shape: rectangle}
B: "Can you ping the default gateway?" {shape: rectangle}
C: "Check local interface: ip link / ip addr" {shape: rectangle}
E: "Check cable / SFP\nethtool eth0 — link detected?" {shape: rectangle}
F: "Check IP address assigned\nARP for gateway: arping -I eth0 GW" {shape: rectangle}
H: "VLAN issue\nCheck switch port VLAN assignment" {shape: rectangle}
I: "Firewall or routing on gateway" {shape: rectangle}
J: "Can you ping destination IP?" {shape: rectangle}
K: "traceroute / mtr to destination" {shape: rectangle}
M: "Check routing table: ip route\nDefault route present?" {shape: rectangle}
N: "Routing or ACL issue in transit\nEngage network team with hop IP" {shape: rectangle}
O: "Host firewall / service not listening\nnc -zv dst port" {shape: rectangle}
P: "Name resolution issue?\ndig / nslookup hostname" {shape: rectangle}
R: "See DNS Resolution guide" {shape: rectangle}
S: "Application-layer issue\nCheck service on destination\nopenssl s_client / curl -v" {shape: rectangle}

A -> B
```

---

## VLAN and Trunk Verification

### Cisco

```text
! Show all trunk ports and allowed VLANs
show interfaces trunk

! Example output:
! Port        Mode         Encapsulation  Status        Native vlan
! Gi0/1       on           802.1q         trunking      1
! Port        Vlans allowed on trunk
! Gi0/1       1-4094
! Port        Vlans allowed and active in management domain
! Gi0/1       1,10,20,100,200,300

! Check specific port VLAN assignment (access port)
show interfaces GigabitEthernet0/2 switchport

! Expected for access port:
! Administrative Mode: static access
! Access Mode VLAN: 100

! Verify VLAN exists in database
show vlan id 100
```

### Linux (802.1Q VLAN interface)

```bash
# Check VLAN interfaces defined on host
cat /proc/net/vlan/config
# VLAN Dev name    | VLAN ID
# eth0.100         | 100  | eth0
# eth0.200         | 200  | eth0

# Check VLAN interface stats
ip -d link show eth0.100
```


```text title="Expected output"
VLAN Dev name    | VLAN ID
eth0.100         | 100  | eth0
eth0.200         | 200  | eth0

2: eth0.100@eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 08:00:27:a4:2b:19 brd ff:ff:ff:ff:ff:ff promiscuity 0
    vlan protocol 802.1Q id 100 <REORDER_HDR>
    RX: bytes  packets  errors  dropped overrun mcast
    1245680    8934     0       12      0       0
    TX: bytes  packets  errors  dropped carrier collsns
    987543     7821     0       0       0       0
```

!!! warning "Common errors"
    **`cat: /proc/net/vlan/config: No such file or directory`** — Load the 8021q kernel module with `sudo modprobe 8021q`.
    **`Device "eth0.100" does not exist.`** — Create the VLAN interface first using `sudo ip link add link eth0 name eth0.100 type vlan id 100`.
---

## Routing Table Verification

### Linux

```bash
# Show full routing table
ip route show

# Example:
# default via 10.10.1.1 dev eth0 proto static metric 100
# 10.10.1.0/24 dev eth0 proto kernel scope link src 10.10.1.55
# 10.20.0.0/16 via 10.10.1.254 dev eth0 proto static   ← storage network route

# Find route for a specific destination
ip route get 10.20.5.100

# Expected:
# 10.20.5.100 via 10.10.1.254 dev eth0 src 10.10.1.55
#    cache

# Missing route → add static route (temporary)
ip route add 10.20.0.0/16 via 10.10.1.254 dev eth0
```


```text title="Expected output"
default via 10.10.1.1 dev eth0 proto static metric 100
10.10.1.0/24 dev eth0 proto kernel scope link src 10.10.1.55
10.20.0.0/16 via 10.10.1.254 dev eth0 proto static
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
10.20.5.100 via 10.10.1.254 dev eth0 src 10.10.1.55
    cache
(no output — command completes silently)
```

!!! warning "Common errors"
    **`RTNETLINK answers: File exists`** — The route already exists in the routing table; use `ip route replace` instead of `ip route add` to overwrite it.
    **`RTNETLINK answers: No such device`** — The interface name (e.g., eth0) does not exist; verify the correct interface name with `ip link show`.
    **`RTNETLINK answers: Network is unreachable`** — The gateway IP (10.10.1.254) is not reachable on the specified interface; confirm the gateway is on the same subnet or check ARP with `arp -n`.
### Cisco

```text
! Show full routing table
show ip route

! Show route for specific destination
show ip route 10.20.5.100

! Check OSPF neighbours (dynamic routing)
show ip ospf neighbor

! Check BGP peers (if in use)
show bgp summary
```

---

## Firewall Rule Testing

```bash
# Test TCP port reachability (nc = netcat)
nc -zv 10.10.5.20 443
# Connection to 10.10.5.20 443 port [tcp/https] succeeded!

# Test UDP port
nc -zuv 10.10.1.10 53

# Test multiple ports in range
for port in 2500 2501 2502 3300; do
    nc -zv 10.20.1.50 $port 2>&1 | grep -E "succeeded|refused|timed out"
done

# Test with timeout (avoid long hangs)
nc -zv -w 3 10.10.5.20 8080

# Windows equivalent
Test-NetConnection -ComputerName 10.10.5.20 -Port 443

# Curl for HTTP/HTTPS with full header details
curl -v --connect-timeout 10 https://app01.corp.example.com/health

# OpenSSL TLS test
openssl s_client -connect app01.corp.example.com:443 -servername app01.corp.example.com
```


```text title="Expected output"
Connection to 10.10.5.20 443 port [tcp/https] succeeded!
Connection to 10.10.1.10 53 port [udp/domain] succeeded!
Connection to 10.20.1.50 2500 port [tcp/icl-tls] succeeded!
Connection to 10.20.1.50 2501 port [tcp/nessus] refused!
Connection to 10.20.1.50 2502 port [tcp/nessus-alt] timed out
Connection to 10.20.1.50 3300 port [tcp/unknown] succeeded!
Connection to 10.10.5.20 8080 port [http-alt] succeeded!

ComputerName     : 10.10.5.20
RemoteAddress    : 10.10.5.20
RemotePort       : 443
InterfaceAlias   : Ethernet
SourceAddress    : 10.10.2.15
TcpTestSucceeded : True

*   Trying 10.10.5.20:443...
* Connected to app01.corp.example.com (10.10.5.20) port 443 (#0)
> GET /health HTTP/1.1
< HTTP/1.1 200 OK
< Content-Type: application/json
< Content-Length: 42
{"status":"healthy","uptime":"72h15m"}
* Connection #0 to host app01.corp.example.com left intact

CONNECTED(00000003)
depth=0 OU = IT Operations, O = Corp Inc, C = US
verify return:1
---
Certificate chain
 0 s:/CN=app01.corp.example.com
   i:/CN=Corp Root CA
---
Server certificate
subject=/CN=app01.corp.example.com
issuer=/CN=Corp Root CA
---
```

!!! warning "Common errors"
    **`nc: connect to 10.10.5.20 port 443 (tcp) failed: Connection refused`** — Verify the target service is running and listening on that port with `netstat -tlnp | grep 443` or `ss -tlnp | grep 443`.
    **`curl: (7) Failed to connect to app01.corp.example.com port 443: Connection timed out`** — Check network connectivity to the host with `ping app01.corp.example.com` and verify firewall rules allow outbound HTTPS traffic.
    **`openssl: error:0A000410:SSL routines:ssl3_get_record:sslv3 alert handshake failure`** — Confirm the server certificate is valid and the SNI hostname matches; test with `openssl s_client -connect <ip>:443 -servername <hostname>`.
---

## MTU and Jumbo Frame Issues

MTU mismatches cause large packet failures while small pings succeed — common in storage networks (iSCSI, NFS over 10GbE with jumbo frames).

```bash
# Test if path supports jumbo frames (9000 byte MTU — payload 8972 = 9000 - 28)
ping -M do -s 8972 10.20.1.50
# If MTU mismatch: "From 10.10.1.1 icmp_seq=1 Frag needed and DF set (mtu = 1500)"
# If path OK: normal ping reply

# Progressive MTU test (binary search)
for size in 8972 4096 2048 1472; do
    result=$(ping -M do -s $size -c 1 -W 2 10.20.1.50 2>&1)
    echo "Size $size: $(echo $result | grep -o 'Frag needed\|1 received\|timeout')"
done

# Check MTU on interface
ip link show eth0 | grep mtu
# 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9000 ...

# Set MTU (temporary)
ip link set eth0 mtu 9000

# VMware ESXi: check vSwitch MTU
esxcli network vswitch standard list | grep -i mtu
```


```text title="Expected output"
PING 10.20.1.50 (10.20.1.50) 8972(9000) bytes of data.
From 10.10.1.1 icmp_seq=1 Frag needed and DF set (mtu = 1500)

--- 10.20.1.50 statistics ---
1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 2031ms

Size 8972: Frag needed
Size 4096: 1 received
Size 2048: 1 received
Size 1472: 1 received

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9000

(no output — command completes silently)

vSwitch Name: vSwitch0
  MTU: 1500
vSwitch Name: vSwitch1
  MTU: 9000
```

!!! warning "Common errors"
    **`ping: -M do: unknown option`** — Use `ping -M do` on Linux; on macOS use `ping -D` instead.
    **`RTNETLINK answers: Operation not permitted`** — Run `ip link set` commands with `sudo` or as root.
    **`esxcli: command not found`** — SSH into the ESXi host directly; esxcli is not available on vCenter or standard Linux systems.
---

## ARP Table and MAC Address Checks

```bash
# Show ARP table — verify gateway MAC is present
ip neigh show

# Example:
# 10.10.1.1 dev eth0 lladdr 00:50:56:ab:cd:ef REACHABLE  ← good
# 10.10.1.100 dev eth0  FAILED                            ← host unreachable / no ARP reply

# Send ARP request manually
arping -I eth0 10.10.1.100

# Flush ARP cache for a specific entry (force re-ARP)
ip neigh del 10.10.1.100 dev eth0

# Show MAC address table on Cisco switch (find which port a MAC is on)
# show mac address-table address 00:50:56:ab:cd:ef
! Vlan    Mac Address       Type        Ports
! 100    0050.56ab.cdef    DYNAMIC     Gi0/5
```


```text title="Expected output"
10.10.1.1 dev eth0 lladdr 00:50:56:ab:cd:ef REACHABLE
10.10.1.50 dev eth0 lladdr 00:50:56:12:34:56 REACHABLE
10.10.1.100 dev eth0  FAILED
10.10.1.200 dev eth0 lladdr 00:50:56:78:9a:bc STALE
fe80::1 dev eth0 lladdr 00:50:56:ff:ff:01 REACHABLE

ARPING 10.10.1.100 from 10.10.1.50 eth0
Unicast reply from 10.10.1.100 [00:50:56:99:88:77]  0.645ms
Sent 1 probes (1 broadcast(s))
Received 1 response(s)

(no output — command completes silently)
```

!!! warning "Common errors"
    **`ARPING: Device eth0 not found`** — Verify the interface name with `ip link show` and replace eth0 with the correct interface.
    **`RTNETLINK answers: No such process`** — The ARP entry does not exist; remove the `dev eth0` parameter or verify the IP address is in the neighbor table first.
---

## Common Failure Patterns

| Scenario | Symptom | Root Cause | Fix |
|---|---|---|---|
| Storage network unreachable | iSCSI/NFS timeouts; VM disk I/O errors | Missing static route to storage VLAN | Add route to storage network on hosts |
| vMotion fails | "A general system error occurred" in vCenter | vMotion VMkernel NIC not in correct VLAN | Verify vmk1 VLAN and MTU (9000) |
| Backup timeouts | Veeam job fails after 30 min; network error | Jumbo frames misconfigured on backup NIC | Match MTU between proxy and repo |
| Cross-site connectivity fails | Traceroute stops at WAN router | BGP/OSPF peering down | Check routing protocol peering |
| New VM cannot reach gateway | Ping to GW fails | Wrong port group / VLAN assigned in vCenter | Fix VM network adapter port group |
| Intermittent packet loss | 1–5% loss detected by mtr | Duplex mismatch or bad SFP | Check ethtool duplex; replace SFP |
| SMTP relay fails | Mail not delivered; NDR with connection error | Port 25 blocked at perimeter firewall | Request firewall rule for relay IP |
| Application cluster split-brain | Both nodes think the other is down | NIC bonding failover bug or heartbeat VLAN down | Check bond status; restore heartbeat VLAN |

---

## mtr Analysis and Output Interpretation

```bash
# Run mtr in report mode (12 cycles)
mtr --report --report-cycles 12 10.10.5.20

# Example output:
# HOST: app01.corp.example.com     Loss%   Snt   Last   Avg  Best  Wrst StDev
#   1.|-- 10.10.1.1                 0.0%    12    0.3   0.4   0.3   0.6   0.1
#   2.|-- 10.10.0.1                 0.0%    12    0.8   0.9   0.7   1.2   0.1
#   3.|-- 10.10.5.20                0.0%    12    1.1   1.2   1.0   1.5   0.1

# Interpretation:
# Loss% at hop N but not hop N+1 = router ICMP rate-limiting (not real loss)
# Loss% at final hop = real packet loss to destination
# Wrst >> Avg at a hop = intermittent congestion or flapping link
```


```text title="Expected output"
HOST: app01.corp.example.com     Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- 10.10.1.1                 0.0%    12    0.3   0.4   0.3   0.6   0.1
  2.|-- 10.10.0.1                 0.0%    12    0.8   0.9   0.7   1.2   0.1
  3.|-- 10.10.5.20                0.0%    12    1.1   1.2   1.0   1.5   0.1
```

!!! warning "Common errors"
    **`mtr: command not found`** — Install mtr with `apt-get install mtr` (Debian/Ubuntu) or `yum install mtr` (RHEL/CentOS).
    **`Cannot open raw socket: Operation not permitted`** — Run the command with `sudo` or as root user.
---

## Escalation Criteria

Escalate to network or data centre team when:

- Physical link is down and requires hands-on cabling or SFP replacement
- Spanning tree topology change is causing broadcast storms
- Routing protocol (OSPF/BGP) peering is down between core routers
- ACL changes are required on perimeter or core firewall
- VLAN misconfiguration requires switch configuration change (change management)
- Packet loss >1% is sustained across a core link (SLA breach)
- Storage network is unreachable — iSCSI or NFS failures causing active VM I/O errors
- WAN circuit outage — engage carrier via NOC

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [DNS Resolution Troubleshooting](../dns-resolution/)
- [Networking — Known Issues](../known-issues.md)
- [Networking — Troubleshooting Overview](../)
