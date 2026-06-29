---
tags:
  - nsx
  - nsx-4
  - scenarios
  - vmware
---
# NSX Connectivity Broken

<div class="kb-summary">
A VM or workload loses network connectivity on an NSX-T overlay network. This scenario establishes a
scoping method to determine whether the problem is a single VM (DFW rule), a segment (overlay binding),
inter-segment routing (T1 gateway), or north-south external traffic (T0/edge BGP), then provides the
exact commands and UI paths to isolate and resolve each layer.

*Applies to: vSphere 7.x / 8.x*
</div>

## Products Involved

| Product | Role in This Scenario |
|---|---|
| NSX Manager | DFW rules; T0/T1 gateways; segment config; edge nodes; TEP |
| Aria Operations for Networks | Path analysis (path trace); flow analysis; DFW rule ID lookup |
| vCenter | Host transport node state; edge VM power state |
| ESXi | NSX kernel modules (VIBs); TEP VMkernel connectivity |

---

## 1. Scope the Problem Before Touching Anything

Determine the blast radius first — scope tells you which layer to investigate.

| Scope | Most Likely Cause | First Check |
|---|---|---|
| One VM, one direction | DFW rule blocking specific traffic | Aria Networks path trace |
| All VMs on one segment | Segment not bound to transport node | NSX → Networking → Segments |
| All east-west across segments | T1 gateway issue or T1→T0 uplink down | T1 route table |
| North-south broken only | T0 BGP session down or edge node degraded | T0 BGP neighbor summary |
| All VMs on one ESXi host | TEP connectivity lost or NSX VIB not loaded | vmkping from TEP vmk; esxcli vib list |

---

## 2. Aria Networks Path Trace — First Tool to Use

Run a path trace before touching any DFW rules or routing config — it pinpoints the exact hop and rule ID causing the drop.

Navigate to **Aria Networks → Path Analysis → enter source IP and destination IP → Run**.

```text
Path trace output shows each hop:
  VM NIC → DFW (per vNIC) → Logical Switch → T1 Gateway → T0 Gateway → Physical

If the path shows "Blocked by DFW Rule ID: XXXX":
  Note the rule ID — go to NSX Manager → Security → Distributed Firewall
  Search for that rule ID to see the exact source, destination, service, and action.

If the path shows "Segment not found" or "MAC not in forwarding table":
  The VM's MAC has not been learned on the logical switch.
  Check segment binding and transport node status.
```

---

## 3. DFW Rule Investigation

DFW evaluates rules top-to-bottom within each category — a correct allow rule lower in the list can be shadowed by a deny rule above it.

Navigate to **NSX Manager → Security → Distributed Firewall** and search by the rule ID from path trace.

```text
DFW Rule Evaluation Order (top to bottom within each category):
  ┌────────────────────────────────────────────────── ┬ ──────────────────────────────────────────────────┐
  │ Category        │ Typical Use                                            │
  ├─────────────────┼────────────────────────────────────────────────────────┤
  │ Emergency       │ Breakglass allow/deny; applied first globally          │
  │ Infrastructure  │ DC infrastructure: DNS (53), NTP (123), vCenter (443) │
  │ Environment     │ Environment-level segment isolation rules              │
  │ Application     │ Microsegmentation — app-tier allow rules               │
  │ Default         │ Implicit drop if no rule above matches                 │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```bash
# From ESXi host where the affected VM runs — dump all DFW rules applied to the VM's vNIC
# Get the VM world ID first
esxcli vm process list | grep -A5 "<vm-name>"
# Note the WorldID

# Dump DFW rules for that VM (requires knowing vNIC slot, typically 0)
vsipioctl getrules -f /<world-id>/0

# Count total rules applied to this VM's vNIC (high count = performance overhead)
vsipioctl getrules -f /<world-id>/0 | grep -c "rule"
```


```text title="Expected output"
UUID: 564d3e8a-1234-5678-90ab-cdef12345678
Display Name: prod-web-vm-01
World ID: 2147483648
Config File: /vmfs/volumes/datastore1/prod-web-vm-01/prod-web-vm-01.vmx
Memory: 8192 MB
CPU Count: 4
World ID: 2147483648

Rule ID: 1001 | Direction: IN | Protocol: TCP | Port: 443 | Action: ALLOW | Source: 10.0.0.0/8
Rule ID: 1002 | Direction: IN | Protocol: TCP | Port: 80 | Action: ALLOW | Source: 10.0.0.0/8
Rule ID: 1003 | Direction: OUT | Protocol: TCP | Port: 3306 | Action: ALLOW | Dest: 10.50.1.0/24
Rule ID: 1004 | Direction: IN | Protocol: ICMP | Action: ALLOW | Source: 10.0.0.0/8
Rule ID: 1005 | Direction: OUT | Protocol: DNS | Port: 53 | Action: ALLOW | Dest: 8.8.8.8
Rule ID: 1006 | Direction: IN | Protocol: TCP | Port: 22 | Action: DENY | Source: 0.0.0.0/0
...
247
```

!!! warning "Common errors"
    **`vsipioctl: command not found`** — Verify you are running this command directly on the ESXi host (not vCenter) and that DFW is enabled on the cluster.
    **`No such file or directory: /<world-id>/0`** — Replace `<world-id>` with the actual numeric World ID from the `esxcli vm process list` output (e.g., `/2147483648/0`).
    **`Permission denied`** — Run the command as root or with appropriate ESXi host privileges; use `su -` to elevate if needed.
```bash
# Get hit count for a specific DFW rule — confirms if rule is actively matching traffic
curl -sk -u admin:<password> \
  "https://<nsx-manager>/api/v1/firewall/stats/rules/<rule-id>" \
  | python3 -m json.tool
```


```text title="Expected output"
{
  "rule_id": "1001",
  "rule_name": "Allow-Web-Traffic",
  "hit_count": 47283,
  "byte_count": 5847392,
  "packet_count": 12456,
  "last_hit_timestamp": 1699564823000,
  "enabled": true,
  "direction": "IN_OUT",
  "statistics": {
    "total_matches": 47283,
    "denied_packets": 0,
    "allowed_packets": 47283
  }
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present; if still failing, verify NSX Manager hostname matches certificate CN).
    **`curl: (7) Failed to connect to <nsx-manager>: Name or service not known`** — Confirm NSX Manager hostname/IP is correct and resolvable from your network location.
    **`{"error_code": 401, "error_message": "Unauthorized"}`** — Verify admin credentials are correct and the user has API access permissions in NSX Manager.
Look for: a high-hit-count deny rule in a higher category (Emergency/Infrastructure) that matches the source or destination — this shadows any allow rule lower in the list.

---

## 4. Segment and Transport Node Check

If Aria Networks shows the segment unreachable or the VM's MAC is unknown, verify the segment is bound to the affected host.

```bash
# NSX Manager REST API — check transport node status for the segment (logical switch)
# First get the logical switch ID from NSX Manager UI → Networking → Segments

curl -sk -u admin:<password> \
  "https://<nsx-manager>/api/v1/logical-switches/<ls-id>/transport-node-status" \
  | python3 -m json.tool | grep -E "status|transport_node_id|display_name"

# Expected: all transport nodes for the segment show "UP"
```


```text title="Expected output"
{
  "display_name": "segment-prod-web-01",
  "status": "UP",
  "transport_node_id": "tn-001-esx-01.lab.local"
}
{
  "display_name": "segment-prod-web-01",
  "status": "UP",
  "transport_node_id": "tn-002-esx-02.lab.local"
}
{
  "display_name": "segment-prod-web-01",
  "status": "UP",
  "transport_node_id": "tn-003-esx-03.lab.local"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag (already in the command above) or import the NSX Manager CA certificate into your system trust store.
    **`curl: (401) Unauthorized`** — Verify the admin password is correct and the user has API access permissions in NSX Manager.
    **`jq: command not found`** — Replace `python3 -m json.tool` with `jq '.'` if jq is installed, or ensure python3 is available on your system.
From vCenter, go to **NSX → System → Fabric → Nodes → Host Transport Nodes** and check configuration state. If the host shows "Failed" or "Pending":

```bash
# Check NSX VIBs installed on the host — all should match the same version
esxcli software vib list | grep -i nsx
```


```text title="Expected output"
Name                           Version                Install Date
nsx-common                     4.1.0.0-21589934       2024-01-15
nsx-esx                        4.1.0.0-21589934       2024-01-15
nsx-vdrportset                 4.1.0.0-21589934       2024-01-15
nsx-vxlan                      4.1.0.0-21589934       2024-01-15
nsx-vsipfe                     4.1.0.0-21589934       2024-01-15
```

!!! warning "Common errors"
    **`Connect to localhost failed. Error: Unable to connect to the local hostd agent.`** — Ensure the ESXi host is in maintenance mode or restart the hostd service with `services.sh restart`.
    **`grep: (standard input): Permission denied`** — Run the command with root privileges using `sudo` or execute it directly in an ESXi SSH session where you already have elevated permissions.
Look for: any NSX VIB at a different version than the rest indicates a partial upgrade or failed re-apply — re-apply the transport node profile from NSX Manager.

---

## 5. T1/T0 Routing Check

For inter-segment routing failures, check the T1 route table and T1→T0 uplink from the edge node CLI.

Navigate to **NSX Manager → Networking → Tier-1 Gateways → select T1 → Route Table**, or SSH to the edge node:

```bash
# SSH to the NSX edge node (via vCenter console or direct SSH)
# List logical routers on the edge node
get logical-routers

# Output shows VRF IDs:
#   VRF 0 — management plane
#   VRF 1 — T0 uplink (SR — service router)
#   VRF 2 — T1 DR (distributed router)

# Enter the T1 VRF
vrf <t1-vrf-id>

# Check route table on the T1
get route

# If the connected subnet for the source or destination segment is missing:
# the T1 is not connected to that segment — verify segment is attached to this T1
```


```text title="Expected output"
NSX Edge Node CLI
edge-node-01> get logical-routers
Logical Router ID          VRF    Type              Status
lr-mgmt-001                0      Management        up
lr-t0-uplink-prod          1      Service Router    up
lr-t1-distributed-web      2      Distributed       up
lr-t1-distributed-db       3      Distributed       up

edge-node-01> vrf 2
Entering VRF 2 (lr-t1-distributed-web)
edge-node-01(vrf-2)> get route
Destination          Next Hop         Metric  Type
192.168.10.0/24      Connected        0       Direct
192.168.20.0/24      192.168.10.1     10      Static
10.0.0.0/8           192.168.10.254   20      BGP
169.254.1.0/24       Kernel           0       Kernel
```

!!! warning "Common errors"
    **`vrf: invalid VRF ID`** — Verify the VRF ID from `get logical-routers` output matches your T1 router and use the correct numeric ID.
    **`get route: command not found`** — Ensure you are in the correct VRF context using `vrf <id>` before running route commands.
Check the T1 → T0 uplink and BGP state:

```bash
# Enter the T0 VRF
vrf <t0-vrf-id>

# Check BGP neighbor state (for external/north-south connectivity)
get bgp neighbor summary

# Fields to check:
#   State    — Established (healthy) vs Active/Connect (session down)
#   Up/Down  — time since BGP session last changed state

# If BGP is down with upstream router: check IP reachability from edge to router
ping <upstream-router-ip> source <t0-uplink-ip>
```


```text title="Expected output"
vrf t0-vrf-001
(no output — command completes silently)

get bgp neighbor summary
Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
10.200.1.1      4 65001    4521    4518   128456    0    0 5w2d14h Established
10.200.1.5      4 65001    4512    4515   128456    0    0 5w2d14h Established
10.200.2.1      4 65002    3847    3851   128456    0    0 2d18h   Established
10.200.2.5      4 65002      12      14       0    0    0 00:02:34 Active

ping 10.200.1.1 source 10.100.0.5
PING 10.200.1.1 (10.200.1.1) from 10.100.0.5: 56 data bytes
64 bytes from 10.200.1.1: icmp_seq=0 ttl=64 time=2.341 ms
64 bytes from 10.200.1.1: icmp_seq=1 ttl=64 time=2.287 ms
64 bytes from 10.200.1.1: icmp_seq=2 ttl=64 time=2.305 ms
--- 10.200.1.1 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max/stddev = 2.287/2.311/2.341/0.022 ms
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the correct VRF ID syntax for your NSX-T or vSphere environment (use `show vrf` to list available VRFs).
    **`Neighbor 10.200.1.5: connect to peer failed (Connection refused)`** — Check that BGP is enabled on the upstream router and that the neighbor relationship is configured with matching AS numbers and timers.
    **`PING: sendto: No route to host`** — Verify the source IP address is assigned to an active interface on the T0 uplink and that a route exists to the upstream router IP.
Look for: `State = Active` or `Connect` on any BGP neighbor means the session is down — check IP reachability and AS/password configuration on both sides.

---

## 6. Edge Node Health Check

If north-south traffic is broken and T0 BGP is down, verify the edge VM itself is healthy and its TEP connectivity is intact.

In vCenter, confirm the edge VM is powered on: **NSX → Fabric → Nodes → Edge Transport Nodes**.

```bash
# From edge node CLI — check overall system status
get system health status

# Check interfaces on the edge
get interfaces

# Verify TEP connectivity from the edge node to ESXi host TEPs
get tunnel-port interface
ping <esxi-tep-ip> source <edge-tep-ip>
```


```text title="Expected output"
System Health Status:
  Overall Status: HEALTHY
  CPU Usage: 34%
  Memory Usage: 62%
  Disk Usage: 48%
  Last Updated: 2024-01-15 14:32:18 UTC

Interface Summary:
  eth0: UP (10.45.12.88/24) — MTU 1500
  eth1: UP (192.168.100.45/24) — MTU 1500
  eth2: DOWN
  bond0: UP (172.16.50.10/25) — MTU 9000

Tunnel Port Interface:
  TEP Interface: vmk10
  IP Address: 10.50.1.45/24
  Status: CONNECTED
  MTU: 1500

PING 10.50.1.88 from 10.50.1.45: 56 data bytes
64 bytes from 10.50.1.88: icmp_seq=0 ttl=64 time=2.34 ms
64 bytes from 10.50.1.88: icmp_seq=1 ttl=64 time=2.18 ms
64 bytes from 10.50.1.88: icmp_seq=2 ttl=64 time=2.41 ms
--- 10.50.1.88 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
```

!!! warning "Common errors"
    **`Error: Unable to resolve TEP interface — tunnel port not configured`** — Configure the tunnel endpoint (TEP) on the edge node using the appropriate network configuration command before attempting connectivity checks.
    **`PING: sendto: No route to host`** — Verify that the ESXi host TEP IP is reachable and that routing/firewall rules permit traffic between the edge TEP subnet and ESXi TEP subnet.
    **`Error: Command 'get tunnel-port interface' not found`** — Ensure you are running this command from the NSX edge node CLI context, not a standard ESXi or Linux shell.
```bash
# If edge TEP has a stale ARP entry after a recent migration or network event:
clear arp
# Then re-test BGP and TEP connectivity
```


```text title="Expected output"
Clearing ARP cache on edge TEP node-42.prod.local...
ARP cache cleared successfully.
Flushing neighbor table for all interfaces...
  eth0: 127 entries removed
  eth1: 89 entries removed
  eth2: 0 entries removed
Waiting 5 seconds for ARP table to stabilize...
BGP session status check:
  Neighbor 10.240.1.1: Established (uptime: 2d 14h)
  Neighbor 10.240.1.2: Established (uptime: 1d 3h)
TEP connectivity test:
  TEP IP 192.168.100.42 → 192.168.100.41: OK (RTT: 2.3ms)
  TEP IP 192.168.100.42 → 192.168.100.43: OK (RTT: 2.1ms)
All connectivity checks passed.
```

!!! warning "Common errors"
    **`command not found: clear arp`** — Use `ip neigh flush all` or `arp -d -a` depending on your OS, or consult your hypervisor's CLI documentation for the correct ARP flush command.
    **`RTNETLINK answers: Operation not permitted`** — Run the command with sudo or as root, since ARP cache manipulation requires elevated privileges.
    **`BGP session down: Neighbor 10.240.1.1 not responding`** — Verify network connectivity to the BGP neighbor and check that the BGP daemon is running with `systemctl status bgpd` or equivalent.
---

## 7. TEP (Tunnel Endpoint) Connectivity from ESXi

GENEVE tunnels between ESXi hosts use TEP VMkernel interfaces — if TEP is unreachable, all overlay traffic between affected hosts is broken.

```bash
# Identify the TEP VMkernel IP on the source host
esxcli network ip interface list | grep -i vmk10

# Test GENEVE tunnel path to a remote TEP IP (use 1572-byte payload: GENEVE overhead ~50 bytes)
vmkping -I vmk10 <remote-tep-ip> -d -s 1572

# If this fails: check that the physical underlay (VLAN, MTU, routing) allows
# UDP port 6081 (GENEVE) between hosts

# Confirm GENEVE firewall rule is enabled on both hosts
esxcli network firewall ruleset list | grep -i geneve
```


```text title="Expected output"
Name  Port Group      IP Address      Netmask         Broadcast       MAC Address        MTU     TSO MSS Status VMotion Vsan Management
vmk10 TEP-Network    192.168.100.45  255.255.255.0   192.168.100.255 00:50:56:c0:00:0a 1600    65535  up      false    false   false

PING 192.168.100.67 (192.168.100.67): 1572 data bytes
1580 bytes from 192.168.100.67: icmp_seq=0 time=2.341 ms
1580 bytes from 192.168.100.67: icmp_seq=1 time=2.156 ms
1580 bytes from 192.168.100.67: icmp_seq=2 time=2.289 ms
1580 bytes from 192.168.100.67: icmp_seq=3 time=2.401 ms
--- 192.168.100.67 statistics ---
4 packets transmitted, 4 packets received, 0% packet loss

Name                    Enabled
vsan                    true
vMotion                 true
NFC                     true
geneveClient            true
...
```

!!! warning "Common errors"
    **`vmkping: Unknown host 192.168.100.67`** — Verify the remote TEP IP address is correct and reachable on the underlay network.
    **`100% packet loss`** — Check that MTU is set to at least 1600 on vmk10 and the physical switch allows UDP 6081; verify GENEVE firewall rule is enabled with `esxcli network firewall ruleset set -r geneveClient -e true`.
Look for: `vmkping -I vmk10 -d -s 1572` success to all remote TEPs confirms the GENEVE underlay is healthy; failure points to VLAN, MTU, or routing issues in the physical network.

---

## Key Terms

| Term | Definition |
|---|---|
| DFW (Distributed Firewall) | NSX kernel-level stateful firewall enforced per vNIC on every ESXi host; rules follow the VM at vMotion; evaluated top-to-bottom by category with first-match-wins logic |
| T0 (Tier-0 Gateway) | The NSX north-south router that connects the overlay network to the physical underlay; runs BGP with upstream physical routers; deployed on edge nodes |
| T1 (Tier-1 Gateway) | The NSX inter-segment router that connects logical segments to each other and uplinks to the T0; can be distributed (runs on ESXi hosts) or centralized (runs on edge nodes) |
| TEP | Tunnel Endpoint — VMkernel interface (typically vmk10 on ESXi, vmk0 on edge nodes) used to originate and terminate GENEVE overlay tunnels between transport nodes |
| GENEVE | Generic Network Virtualization Encapsulation — UDP-based tunnel protocol (port 6081) used by NSX-T to carry overlay traffic between TEPs; requires MTU ~1600 in the underlay |
| BGP | Border Gateway Protocol — routing protocol used between NSX T0 gateways and physical routers to advertise VM subnet prefixes north-south; session state is key to external connectivity |
| Segment | An NSX logical Layer-2 network backed by GENEVE tunnels; VMs on the same segment communicate without routing; must be bound to each host transport node that runs its VMs |
| Transport node | An ESXi host or NSX edge node that has been configured with NSX VIBs and TEP VMkernel interfaces; only transport nodes can carry overlay traffic |
| Path analysis | Aria Networks feature that traces the forwarding path between two IPs hop-by-hop through DFW, logical switches, T1, and T0; returns the exact rule ID causing a block |
| Aria Networks | VMware network observability product (formerly vRealize Network Insight); used here for path trace, flow analysis, and DFW rule lookup |
| Edge node | Dedicated NSX VM or bare-metal appliance that hosts the T0 and T1 service router (SR) components; required for stateful north-south services and BGP peering |
| Rule priority | The position of a DFW rule within its category; lower position = evaluated first; a high-priority deny in Emergency or Infrastructure shadows allow rules in Application |

---

## Common Mistakes

- **Assuming the firewall is the problem without running path trace first.** A routing issue at T1 or T0 looks identical to a DFW drop from the VM's perspective. Path trace distinguishes them in seconds.
- **Not checking rule order.** A correct allow rule in the Application category may be shadowed by an overly broad deny rule in the Infrastructure or Environment category. Always look at what comes above the matched rule.
- **Forgetting that DFW follows the VM, not the host.** After a vMotion, DFW rules are re-enforced on the destination host's vNIC. If the destination host's transport node is in a bad state, DFW enforcement may fail silently.
- **Clearing ARP or BGP state on a production edge without checking both T0s.** In an active-standby T0 pair, the standby takes over when the active is disrupted. Clearing state on the active without checking failover impact can cause an unnecessary cutover.

---

## Related Scenarios

- [VM Performance Degraded](vm-performance-degraded.md) — DFW rule overhead on east-west traffic is a common but overlooked cause of VM network latency and dropped packets.
- [vMotion Failing](vmotion-failing.md) — NSX TEP and segment availability issues cause vMotion failures; the vMotion scenario covers TEP vmkping in context.
- [VM Inaccessible / HA Failover](vm-inaccessible-ha-failover.md) — After HA restarts a VM on a new host, NSX transport node state on that host must be healthy for connectivity to restore.
