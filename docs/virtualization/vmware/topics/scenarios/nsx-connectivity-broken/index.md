# NSX Connectivity Broken

<div class="kb-summary">
A VM or workload loses network connectivity on an NSX-T overlay network. This scenario establishes a
scoping method to determine whether the problem is a single VM (DFW rule), a segment (overlay binding),
inter-segment routing (T1 gateway), or north-south external traffic (T0/edge BGP), then provides the
exact commands and UI paths to isolate and resolve each layer.
</div>

```text
┌──────────────────────────────────── NSX Connectivity Broken — Investigation Flow ─────────────────────────┐
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
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

Determine the blast radius first. The scope tells you where to look:

| Scope | Most Likely Cause | First Check |
|---|---|---|
| One VM, one direction | DFW rule blocking specific traffic | Aria Networks path trace |
| All VMs on one segment | Segment not bound to transport node | NSX → Networking → Segments |
| All east-west across segments | T1 gateway issue or T1→T0 uplink down | T1 route table |
| North-south broken only | T0 BGP session down or edge node degraded | T0 BGP neighbor summary |
| All VMs on one ESXi host | TEP connectivity lost or NSX VIB not loaded | vmkping from TEP vmk; esxcli vib list |

---

## 2. Aria Networks Path Trace — First Tool to Use

Do not guess at DFW rules manually. Use Aria Operations for Networks to run a path trace.

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

DFW rules are evaluated top-to-bottom within each category. First match wins. A correct rule lower in the list can be shadowed by a deny rule above it.

Navigate to **NSX Manager → Security → Distributed Firewall**. Search by rule ID found in path trace.

```text
DFW Rule Evaluation Order (top to bottom within each category):
  ┌─────────────────┬────────────────────────────────────────────────────────┐
  │ Category        │ Typical Use                                            │
  ├─────────────────┼────────────────────────────────────────────────────────┤
  │ Emergency       │ Breakglass allow/deny; applied first globally          │
  │ Infrastructure  │ DC infrastructure: DNS (53), NTP (123), vCenter (443) │
  │ Environment     │ Environment-level segment isolation rules              │
  │ Application     │ Microsegmentation — app-tier allow rules               │
  │ Default         │ Implicit drop if no rule above matches                 │
  └─────────────────┴────────────────────────────────────────────────────────┘
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

Check DFW rule statistics from NSX Manager REST API:

```bash
# Get hit count for a specific DFW rule — confirms if rule is actively matching traffic
curl -sk -u admin:<password> \
  "https://<nsx-manager>/api/v1/firewall/stats/rules/<rule-id>" \
  | python3 -m json.tool
```

---

## 4. Segment and Transport Node Check

If Aria Networks shows the segment is unreachable or the VM's MAC is unknown:

```bash
# NSX Manager REST API — check transport node status for the segment (logical switch)
# First get the logical switch ID from NSX Manager UI → Networking → Segments

curl -sk -u admin:<password> \
  "https://<nsx-manager>/api/v1/logical-switches/<ls-id>/transport-node-status" \
  | python3 -m json.tool | grep -E "status|transport_node_id|display_name"

# Expected: all transport nodes for the segment show "UP"
```

From vCenter, go to **NSX → System → Fabric → Nodes → Host Transport Nodes**. The ESXi host should show "Success" configuration state. If it shows "Failed" or "Pending":

1. Check NSX VIBs installed on the host:

```bash
esxcli software vib list | grep -i nsx
# All NSX VIBs should show the same version
```

2. Re-apply the transport node profile from NSX Manager if VIBs are missing or version-mismatched.

---

## 5. T1/T0 Routing Check

For inter-segment routing failures, check the T1 gateway route table.

Navigate to **NSX Manager → Networking → Tier-1 Gateways → select T1 → Route Table** (or use the CLI from edge node).

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

Check the T1 → T0 uplink:

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

---

## 6. Edge Node Health Check

If north-south traffic is broken and T0 BGP is down, check the edge node itself.

In vCenter, verify the edge VM is powered on: **NSX → Fabric → Nodes → Edge Transport Nodes**.

```bash
# From edge node CLI — check overall system status
get system health status

# Check interfaces on the edge
get interfaces

# Verify TEP connectivity from the edge node to ESXi host TEPs
get tunnel-port interface
ping <esxi-tep-ip> source <edge-tep-ip>
```

If the edge node VM was recently migrated or the host it runs on had a network event, the TEP may have a stale ARP or VTEP entry:

```bash
# Clear ARP on the edge node
clear arp
# Then re-test BGP and TEP connectivity
```

---

## 7. TEP (Tunnel Endpoint) Connectivity from ESXi

GENEVE tunnels between ESXi hosts use TEP VMkernel interfaces (typically vmk10). If TEP is unreachable, all overlay traffic between affected hosts is broken.

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
