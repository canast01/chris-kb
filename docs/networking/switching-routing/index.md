# Switching & Routing

<div class="kb-summary">
Switching and routing knowledge base covering VLANs, inter-VLAN routing, BGP, OSPF, subnetting, and TCP/IP fundamentals.
</div>

## VLANs

VLANs segment network traffic into logical broadcast domains. In an enterprise infrastructure, separate VLANs are standard practice for management, storage (iSCSI, NFS), replication, vMotion, backup, SAN, and production traffic.

### View VLANs (Cisco IOS/NX-OS)

```bash
show vlan brief
show vlan id <id>
show interfaces trunk
show interface <int> status
```
```
┌────────────────────────────────── Networking — Switching & Routing ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       VLANs segment broadcast domains; trunk ports carry multiple VLANs between switches      │   │
│   │       Routing: OSPF for internal; BGP for DC fabric and WAN; static for management paths      │   │
│   │          Subnetting: plan IP space per VLAN; document in IPAM; leave growth headroom          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Switching                   │  │                   Routing                   │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │            VLAN: show vlan brief             │  │           OSPF: show ip ospf neigh          │   │
│   │            Trunk: show int trunk             │  │            BGP: show bgp summary            │   │
│   │             STP: show span brief             │  │          Route table: show ip route         │   │
│   │           LACP: show etherchannel            │  │           Ping + traceroute verify          │   │
│   │           MAC table: show mac addr           │  │          MTU: ping with df-bit set          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       VLAN       │       Name       │       Subnet      │     Gateway      │     Purpose      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │        10        │    Management    │    10.0.10.0/24   │    10.0.10.1     │    OOB / IPMI    │   │
│   │        20        │     vMotion      │    10.0.20.0/24   │    10.0.20.1     │  VMware vMotion  │   │
│   │        30        │     Storage      │    10.0.30.0/24   │    10.0.30.1     │   iSCSI / NFS    │   │
│   │       100        │    Production    │    10.1.0.0/22    │     10.1.0.1     │   VM workloads   │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Trunk port   = Switch port carrying multiple VLANs with 802.1Q tagging                             │
│    Native VLAN  = Untagged VLAN on a trunk; must match both sides; mismatch causes loops              │
│    SVI          = Switched Virtual Interface; L3 gateway for a VLAN on a layer-3 switch               │
│    ECMP         = Equal-Cost Multi-Path; multiple routes to destination; load balanced                │
│    IPAM         = IP Address Management; tracks allocations; prevents duplicate IPs                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

### Configure a Trunk Port

```bash
interface <int>
  switchport mode trunk
  switchport trunk allowed vlan <id1>,<id2>
  switchport trunk native vlan <native_id>
```

### Add / Remove VLANs on a Trunk

```bash
switchport trunk allowed vlan add <id>
switchport trunk allowed vlan remove <id>
```

### VLAN Validation

After creating or modifying VLANs:

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

### Common VLAN Use Cases

| VLAN | Traffic Type | Notes |
|---|---|---|
| Management | OOB switch/server management | Strictly controlled access |
| Storage | iSCSI, NFS | Jumbo frames (MTU 9000) required |
| vMotion | VMware live migration | Dedicated, no other traffic |
| Replication | SRDF, SnapMirror, vSphere replication | May share with storage |
| Backup | Backup agents and media servers | High-bandwidth bursts |
| Production | Application traffic | Standard MTU (1500) |

### Common Issues

| Issue | Check | Action |
|---|---|---|
| Host unreachable | VLAN on trunk? | `show interfaces trunk` |
| VLAN not in FLOGI / iSCSI | Wrong VLAN on port | Check access or trunk assignment |
| Native VLAN mismatch | CDP/LLDP log | Match native VLAN on both trunk ends |
| VLAN not propagated | VTP or manual config | Check VTP domain or add VLAN manually |

## VLAN Configuration

Step-by-step procedures for creating and assigning VLANs on Cisco IOS/NX-OS switches.

### Create a VLAN

```bash
configure terminal
vlan <id>
  name <vlan_name>
exit
```

### Assign an Access Port

```bash
interface <int>
  switchport mode access
  switchport access vlan <id>
  description <description>
  no shutdown
exit
```

### Configure a Trunk Port

```bash
interface <int>
  switchport mode trunk
  switchport trunk encapsulation dot1q    # if required by platform
  switchport trunk native vlan <native_id>
  switchport trunk allowed vlan <id1>,<id2>,<id3>
  no shutdown
exit
```

### Add a VLAN to an Existing Trunk

```bash
interface <int>
  switchport trunk allowed vlan add <id>
```

### Remove a VLAN from a Trunk

```bash
interface <int>
  switchport trunk allowed vlan remove <id>
```

### Save Configuration

```bash
copy running-config startup-config
# or (NX-OS)
copy running-config startup-config vdc-all
```

### Validation Checklist

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

After VLAN config:
- [ ] VLAN visible in `show vlan brief` on all relevant switches
- [ ] Trunk carries VLAN — `show interfaces trunk`
- [ ] End-host reachable — `ping <host_on_vlan>`
- [ ] Storage / application traffic flowing

### Common Issues

| Issue | Check | Action |
|---|---|---|
| VLAN not passing | Trunk allowed list | `switchport trunk allowed vlan add` |
| Host not on VLAN | Access port assignment | `switchport access vlan <id>` |
| Native VLAN mismatch | CDP/LLDP warnings | Match native VLAN on both trunk ends |
| VLAN pruned by VTP | VTP mode | Set to transparent or manually add VLAN |

## Routing

Routing determines how traffic moves between subnets. All storage replication, backup traffic, vMotion, and cloud connectivity depend on correct routing.

### View Route Table

**Linux:**
```bash
ip route show
ip route get <destination_ip>    # show which route would be used
```

**Windows:**
```cmd
route print
```

**Cisco IOS / NX-OS:**
```bash
show ip route
show ip route <destination>
show ip route summary
```

### Default Gateway

```bash
# Linux — confirm default route
ip route show default

# Windows
route print 0.0.0.0
```

### OSPF

```bash
# Check OSPF neighbor state
show ip ospf neighbor

# Verify OSPF routes
show ip route ospf

# OSPF interface status
show ip ospf interface brief
```

All OSPF neighbors should be in `FULL` state. `EXSTART`, `EXCHANGE`, or stuck `2WAY` indicates an adjacency issue.

### BGP

```bash
# BGP summary (neighbor states)
show bgp summary
show bgp neighbors <ip>

# BGP routes
show bgp
show bgp routes
```

### Static Routes

```bash
# Linux — add a static route
ip route add <network>/<prefix> via <gateway>

# Persist (add to /etc/network/interfaces or nmcli)
nmcli connection modify <conn> +ipv4.routes "<network>/<prefix> <gateway>"
```

### Path Tracing

```bash
traceroute <destination>    # Linux
tracert <destination>       # Windows
```

### Common Issues

| Issue | Check | Action |
|---|---|---|
| No route to host | `ip route get <dest>` | Add missing static route or fix OSPF |
| OSPF neighbor stuck | MTU mismatch or auth | Match MTU and OSPF auth config |
| Default gateway unreachable | Physical link and ARP | Check interface and ARP table |
| Asymmetric routing | `traceroute` both directions | Review route policy |

## Routing Validation

Verify routing paths are correct before and after network changes.

### Pre-Change Baseline

```bash
# Capture current route table
ip route show > /tmp/routes-before.txt

# Capture traceroute to critical destinations
traceroute <production_host> >> /tmp/routes-before.txt
traceroute <storage_vip> >> /tmp/routes-before.txt
traceroute <replication_peer> >> /tmp/routes-before.txt
```

### Post-Change Validation

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

### Validate Default Gateway

```bash
ip route show default
ping <gateway_ip>
```

### OSPF Neighbor Validation

```bash
show ip ospf neighbor            # all neighbors in FULL state
show ip ospf neighbor <id>       # specific neighbor detail
show ip route ospf               # routes learned via OSPF
```

### BGP Route Validation

```bash
show bgp summary                  # peer state: Established
show bgp neighbors <ip> routes    # routes received from peer
```

### Test Application-Level Connectivity

```bash
# Confirm key services reachable after routing change
nc -zv <storage_vip> 443    # storage management
nc -zv <vcenter_fqdn> 443   # vCenter
curl -k https://<app_vip>/  # application VIP
```

### Validation Checklist

- [ ] Route table contains all expected routes
- [ ] Default gateway reachable
- [ ] OSPF/BGP neighbors in expected state
- [ ] Traceroute paths unchanged (or correctly changed)
- [ ] Storage, backup, and replication traffic routing correctly
- [ ] Application connectivity confirmed

### Common Issues

| Issue | Check | Action |
|---|---|---|
| Route missing post-change | Route table diff | Restore static route or fix dynamic routing |
| OSPF adjacency lost | MTU, auth, hello timers | Match config on both ends |
| BGP peer down | Peer state | Check ACLs, peer address, ASN |
| Traffic taking wrong path | Metric or admin distance | Adjust metric or route preference |

## Subnetting

### CIDR Notation Reference

| CIDR | Subnet Mask | Hosts | Use Case |
|---|---|---|---|
| /30 | 255.255.255.252 | 2 | Point-to-point links |
| /29 | 255.255.255.248 | 6 | Small management segments |
| /28 | 255.255.255.240 | 14 | DMZ / small service zones |
| /27 | 255.255.255.224 | 30 | Medium service segments |
| /26 | 255.255.255.192 | 62 | Storage or server subnets |
| /25 | 255.255.255.128 | 126 | Mid-size server segments |
| /24 | 255.255.255.0 | 254 | Standard server / VLAN |
| /23 | 255.255.254.0 | 510 | Larger server segments |
| /22 | 255.255.252.0 | 1022 | Campus / large server zones |

### Calculate a Subnet

```bash
# Linux — ipcalc
ipcalc 10.10.10.0/24

# Python one-liner
python3 -c "import ipaddress; n = ipaddress.ip_network('10.10.10.0/24'); print(n.network_address, n.broadcast_address, n.num_addresses)"
```

### Find Subnet of a Given IP

```bash
ipcalc 10.10.10.45/24
# Returns: network, broadcast, first/last usable host
```

### Check if Two IPs Are in the Same Subnet

```bash
python3 -c "
import ipaddress
a = ipaddress.ip_address('10.10.10.45')
b = ipaddress.ip_address('10.10.10.200')
net = ipaddress.ip_network('10.10.10.0/24')
print(a in net, b in net)
"
```

### Reserved Addresses in Each Subnet

- **Network address** — first IP (e.g., 10.10.10.0)
- **Broadcast address** — last IP (e.g., 10.10.10.255)
- **Gateway** — typically .1 or .254 (convention, not mandatory)

### Common Infrastructure Subnets

| Network | Purpose | Notes |
|---|---|---|
| 10.x.x.0/24 | Server / production | Standard for most enterprise server VLANs |
| 10.x.x.0/24 | Storage (iSCSI/NFS) | Often on dedicated VLAN with jumbo frames |
| 10.x.x.0/24 | vMotion | Dedicated VLAN, high bandwidth |
| 10.x.x.0/24 | Backup | Often large subnet for media server access |
| 10.x.x.0/30 | Replication uplinks | Point-to-point between sites |

### Overlap Check

Before assigning a new subnet, verify it doesn't overlap with existing routes:

```bash
# Linux — show all routes
ip route show

# Check for overlap manually or with ipcalc
ipcalc <new_network>/<prefix>
```

## TCP/IP Reference

### IP Configuration

**Linux:**
```bash
ip addr show
ip addr show <interface>
ip addr add <ip>/<prefix> dev <interface>
ip route add default via <gateway>
```

**Windows:**
```powershell
Get-NetIPAddress
Get-NetIPConfiguration
ipconfig /all
```

### TCP Connection Testing

```bash
# Test TCP port reachability
nc -zv <host> <port>
telnet <host> <port>

# PowerShell
Test-NetConnection <host> -Port <port>
```

### Active Connections

```bash
# Linux
ss -tnp         # TCP connections with process info
ss -tnlp        # listening ports
netstat -tnp    # legacy equivalent

# Windows
netstat -ano
Get-NetTCPConnection
```

### MTU and Fragmentation

Default Ethernet MTU is 1500 bytes. Storage networks (iSCSI, NFS) typically use jumbo frames (9000 bytes). Mismatches cause fragmentation or dropped packets.

```bash
# Check interface MTU
ip link show <interface>

# Test path MTU (don't-fragment bit)
ping -M do -s 1472 <destination>    # 1500 MTU test
ping -M do -s 8972 <destination>    # 9000 MTU test

# Windows
ping /f /l 1472 <destination>
```

### TCP States

| State | Meaning |
|---|---|
| ESTABLISHED | Active connection |
| TIME_WAIT | Connection closing; waiting for delayed packets |
| CLOSE_WAIT | Remote side closed; local app hasn't closed yet |
| SYN_SENT | TCP handshake in progress |
| LISTEN | Port open and listening |

### Common Protocol Ports

| Protocol | Port |
|---|---|
| SSH | 22 |
| HTTPS | 443 |
| iSCSI | 3260 |
| NFS | 2049 |
| SMB/CIFS | 445 |
| DNS | 53 (UDP/TCP) |
| LDAP | 389 |
| LDAPS | 636 |
| NTP | 123 (UDP) |
| SNMP | 161/162 (UDP) |

### Common Issues

| Issue | Check | Action |
|---|---|---|
| Can't reach port | Firewall, service down | `nc -zv`; check firewall and service |
| High TIME_WAIT count | Short connection pattern | Tune `net.ipv4.tcp_tw_reuse` |
| MTU causing drops | Path MTU | Lower MTU or fix network |
| Intermittent loss | Duplex mismatch | Force full duplex on NIC and switch |
