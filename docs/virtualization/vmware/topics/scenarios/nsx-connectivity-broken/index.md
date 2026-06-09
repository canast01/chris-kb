# NSX Connectivity Broken

<div class="kb-summary">
A VM or workload loses network connectivity on an NSX-T overlay network. This scenario establishes a
scoping method to determine whether the problem is a single VM (DFW rule), a segment (overlay binding),
inter-segment routing (T1 gateway), or north-south external traffic (T0/edge BGP), then provides the
exact commands and UI paths to isolate and resolve each layer.
</div>

```text
┌──────────────────────────── NSX Connectivity Broken — Investigation Flow ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: Connectivity complaint — determine scope before touching any config                        ││
│   └──────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                              │                                                        │
│   ┌──────────────┬───────────────────────────┼────────────────────────────┬───────────────┐           │
│   ▼              ▼                           ▼                            ▼               ▼           │
│  ┌──────────┐  ┌──────────┐           ┌──────────────┐           ┌──────────────┐  ┌──────────┐       │
│  │ 1 VM     │  │ 1 Segment│           │ All east-west│           │ North-south  │  │ All VMs  │       │
│  │ affected │  │ affected │           │ across segs  │           │ external     │  │ on host  │       │
│  └────┬─────┘  └────┬─────┘           └──────┬───────┘           └──────┬───────┘  └────┬─────┘       │
│       │             │                        │                          │               │             │
│       ▼             ▼                        ▼                          ▼               ▼             │
│  ┌──────────┐  ┌──────────┐           ┌──────────────┐           ┌──────────────┐  ┌──────────┐       │
│  │ DFW rule │  │ Segment  │           │ T1 gateway   │           │ T0/edge BGP  │  │ TEP/     │       │
│  │ blocking?│  │ binding / │          │ route table  │           │ neighbor     │  │ transport│       │
│  │ Aria path│  │ transport │          │ T1→T0 uplink │           │ state        │  │ node VIB │       │
│  │ trace    │  │ node      │          │              │           │              │  │ issue    │       │
│  └────┬─────┘  └────┬─────┘           └──────┬───────┘           └──────┬───────┘  └────┬─────┘       │
│       │             │                        │                          │               │             │
│       └─────────────┴────────────────────────┴──────────────────────────┴───────────────┘             │
│                                              │                                                        │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  CLOSE: Aria Networks path trace shows clean path · DFW shows Allow · BGP established            ││
│   └───────────────────────────────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

```bash
# Get hit count for a specific DFW rule — confirms if rule is actively matching traffic
curl -sk -u admin:<password> \
  "https://<nsx-manager>/api/v1/firewall/stats/rules/<rule-id>" \
  | python3 -m json.tool
```

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

From vCenter, go to **NSX → System → Fabric → Nodes → Host Transport Nodes** and check configuration state. If the host shows "Failed" or "Pending":

```bash
# Check NSX VIBs installed on the host — all should match the same version
esxcli software vib list | grep -i nsx
```

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

```bash
# If edge TEP has a stale ARP entry after a recent migration or network event:
clear arp
# Then re-test BGP and TEP connectivity
```

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

- [VM Performance Degraded](../vm-performance-degraded/index.md) — DFW rule overhead on east-west traffic is a common but overlooked cause of VM network latency and dropped packets.
- [vMotion Failing](../vmotion-failing/index.md) — NSX TEP and segment availability issues cause vMotion failures; the vMotion scenario covers TEP vmkping in context.
- [VM Inaccessible / HA Failover](../vm-inaccessible-ha-failover/index.md) — After HA restarts a VM on a new host, NSX transport node state on that host must be healthy for connectivity to restore.
