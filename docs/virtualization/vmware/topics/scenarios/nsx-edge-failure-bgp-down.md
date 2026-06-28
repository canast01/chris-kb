---
tags:
  - nsx
  - nsx-4
  - scenarios
  - vmware
---
# NSX Edge Failure / BGP Down

<div class="kb-summary">
NSX edge nodes carry all north-south traffic in and out of the datacenter. When an edge node fails
or its BGP session to the upstream router drops, every VM using that T0 gateway loses external
connectivity. This scenario covers identifying the failure layer — NSX edge, TEP tunnels, or
the physical network — and restoring connectivity with minimal downtime.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_determine_scope_all_vms_or_specifi: "1. Determine Scope — All VMs or Specific VMs" {shape: rectangle}
2_check_edge_cluster_health_in_nsx_m: "2. Check Edge Cluster Health in NSX Manager" {shape: rectangle}
3_check_bgp_neighbor_state_on_the_t0: "3. Check BGP Neighbor State on the T0 Gateway" {shape: rectangle}
4_ssh_to_the_edge_node_check_bgp_and: "4. SSH to the Edge Node — Check BGP and Routes" {shape: rectangle}
5_check_tep_connectivity_edge_to_esx: "5. Check TEP Connectivity — Edge to ESXi Host Tunnels" {shape: rectangle}

products_involved -> 1_determine_scope_all_vms_or_specifi: uses
1_determine_scope_all_vms_or_specifi -> 2_check_edge_cluster_health_in_nsx_m: uses
2_check_edge_cluster_health_in_nsx_m -> 3_check_bgp_neighbor_state_on_the_t0: uses
3_check_bgp_neighbor_state_on_the_t0 -> 4_ssh_to_the_edge_node_check_bgp_and: uses
4_ssh_to_the_edge_node_check_bgp_and -> 5_check_tep_connectivity_edge_to_esx: uses
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| NSX Manager | Edge cluster health, T0 gateway BGP state, TEP configuration |
| vCenter | Edge VM power state and host placement; ESXi host health for the edge VM |
| Aria Operations for Networks | North-south topology view, path trace from VM to upstream router |
| Physical switches (ToR) | BGP peer for the NSX T0 uplink; source of physical network failures |

---

## 1. Determine Scope — All VMs or Specific VMs

Use the symptom to identify the failure layer before diving deeper:

| Symptom | Likely layer | First check |
|---|---|---|
| All VMs on the datacenter lose external connectivity | T0 gateway or edge cluster | NSX Manager → edge nodes |
| Only VMs in one tenant segment lose connectivity | T1 gateway or DFW rule | NSX → T1 routing, DFW |
| Specific IP destinations unreachable | BGP prefix advertisement | T0 → BGP neighbor → received routes |
| Intermittent external connectivity | Active-standby edge failover loop | Edge node stability in NSX |

Look for: global outage → proceed to Step 2; partial outage → check the T1 gateway for that tenant and the relevant DFW rules first.

---

## 2. Check Edge Cluster Health in NSX Manager

Navigate to NSX Manager → **System** → **Fabric** → **Nodes** → **Edge Transport Nodes** and check each node's status indicator.

Look for: any node showing **Degraded** or **Down** — the standby should have taken over; confirm which node is currently active on the T0 gateway.

```bash
# NSX Manager REST API — list all edge nodes and their status
curl -sk -u admin:<password> \
  "https://nsx-manager.domain.local/api/v1/transport-nodes?node_type=EdgeNode" \
  | python3 -m json.tool | grep -E '"display_name"|"status"'
```

---

## 3. Check BGP Neighbor State on the T0 Gateway

Navigate to NSX Manager → **Networking** → **Tier-0 Gateways** → select T0 → **BGP** → **Neighbors**.

Look for: each upstream router peer showing **Established**; any other state means the BGP session is down and routes are not being exchanged.

| BGP state | Meaning |
|---|---|
| Established | Healthy — routes are being exchanged |
| Idle | BGP is not attempting to connect — check edge node health first |
| Active | BGP is attempting to connect but not succeeding — check network reachability |
| Connect | TCP connection initiated but not yet acknowledged — usually a transient state |

---

## 4. SSH to the Edge Node — Check BGP and Routes

SSH to the edge node and run the BGP and route commands in sequence:

```bash
# From NSX edge node CLI — list logical routers (VRFs)
get logical-routers

# Switch to the uplink VRF (note the UUID from the output above)
vrf <uplink-vrf-uuid>

# Check BGP neighbor summary — look for State = Established
get bgp neighbor summary

# Check the route table for default route (0.0.0.0/0) and uplink prefixes
get route
```

Look for: **Established** state and a non-zero **PfxRcd** (prefixes received from upstream router).

```bash
# Ping the upstream router from the edge node uplink interface
ping <upstream-router-ip> interface <uplink-interface-name>

# Check interface status on the edge node
get interfaces
```

---

## 5. Check TEP Connectivity — Edge to ESXi Host Tunnels

TEP tunnels carry overlay traffic between edge nodes and ESXi hosts via GENEVE; broken TEPs mean VMs cannot be reached even if the edge node and BGP are healthy.

```bash
# From edge node — list all tunnel ports and their state
get tunnel-ports

# Check GENEVE tunnel state to each ESXi host TEP
# Look for tunnel state: UP
get logical-switch port <port-id>
```

```bash
# From an ESXi host — verify TEP reachability to the edge node TEP IP
vmkping -I vmk10 <edge-tep-ip> -d -s 8972
# vmk10 = TEP VMkernel interface (check your environment for the correct vmk)
```

Look for: failed large-packet pings between ESXi hosts and the edge node TEP IPs — this points to the underlay VLAN carrying TEP traffic; check the physical switch port.

---

## 6. Check the Edge VM in vCenter

Edge nodes run as VMs; a powered-off or mis-placed edge VM takes down the node entirely.

In vCenter navigate to the edge VM (typically named `edge-<uuid>`) and verify power state, host placement, and vNIC port group assignments.

```powershell
# PowerCLI — find edge VMs and their host placement
Get-VM | Where-Object {$_.Name -like "edge-*"} | Select-Object Name, PowerState, VMHost
```

Look for: edge VM on a failed or maintenance-mode host — vSphere HA will restart it elsewhere; wait for HA to complete, then recheck BGP state.

---

## 7. Verify Failover — Active-Standby Edge Pair

When the active edge node fails, the standby should take over in ~1 second with BFD-assisted BGP reconvergence.

Check which node is active: NSX Manager → **Networking** → **Tier-0 Gateways** → T0 → **Configuration** → **Edge Cluster Member** column.

Look for: if failover did not occur, verify BFD is enabled on the T0 uplink interfaces and the edge cluster configuration is correct.

---

## 8. Physical Switch — Upstream BGP Peer

If both edge nodes show non-Established BGP and TEPs and edge VMs are healthy, the problem is the upstream physical switch or router.

Check on the ToR switch: BGP neighbor state for the NSX T0 uplink IPs, port state for edge uplink ports, and MTU (GENEVE requires MTU 1600 or higher — mismatched MTU causes intermittent tunnel failures that destabilise BGP).

```bash
# On Cisco Nexus — check BGP summary for NSX edge peers
show bgp ipv4 unicast summary | grep <edge-uplink-ip>

# Check port state for edge-connected ports
show interface eth1/10 status
```

---

## Common Mistakes

- **Restarting both edge nodes simultaneously.** In an active-standby pair, this causes a complete
  north-south outage. Always restart one edge at a time and confirm the standby has taken over
  before touching the second node.
- **Not checking TEP connectivity.** An edge node can show green in NSX Manager while TEP tunnels
  to ESXi hosts are broken. Overlay traffic cannot reach VMs without working TEPs.
- **Ignoring the upstream physical switch.** The NSX edge may be perfectly healthy while the ToR
  switch BGP peer is misconfigured or has flapped. Always verify the physical layer before
  concluding it is an NSX problem.
- **Forgetting BFD configuration.** Without BFD, BGP failover after an edge failure can take 30–90
  seconds (standard BGP keepalive timer). With BFD, convergence is sub-second. If failover is slow,
  check whether BFD is enabled on the T0 uplinks.

---

## Key Terms

| Term | Definition |
|---|---|
| Edge node | An NSX-T VM that provides gateway services — routing, NAT, load balancing, and VPN — at the boundary between the NSX overlay and the physical network |
| Edge cluster | A logical group of one or more edge nodes; T0 gateways are bound to an edge cluster and use active-standby failover between its members |
| T0 (Tier-0 Gateway) | The NSX gateway that connects the overlay network to the physical network; runs eBGP with upstream routers and handles all north-south traffic |
| BGP (Border Gateway Protocol) | The routing protocol used between the NSX T0 gateway and the upstream physical router to exchange reachable prefixes; session state must be Established for traffic to flow |
| TEP (Tunnel Endpoint) | VMkernel IP address on each ESXi host and edge node used to originate and terminate GENEVE overlay tunnels; TEP reachability is required for overlay traffic |
| GENEVE | Generic Network Virtualization Encapsulation — the overlay protocol used by NSX to carry VM traffic over the physical underlay between TEPs (replaces VXLAN) |
| Active-standby | NSX edge cluster failover mode where one edge node handles all traffic; the standby takes over in ~1 second when the active node fails |
| VRF (Virtual Routing and Forwarding) | A separate routing table instance on the edge node; each T0 uplink uses a dedicated VRF — use `vrf <uuid>` on the edge CLI to switch context |
| eBGP | External BGP — the BGP session type between the NSX T0 gateway and the upstream physical router; used because they are in different autonomous systems |
| BGP neighbor | A router peer configured to exchange routes via BGP; in this scenario the T0 gateway's BGP neighbors are the upstream ToR switches |
| Uplink | The edge node network interface that connects the NSX overlay to the physical network; carries BGP and routed north-south traffic to the ToR switch |
| North-south traffic | Traffic between VMs inside the NSX overlay and destinations outside the datacenter (internet, WAN, or other networks); all flows through the T0 gateway edge node |

---

## Related Scenarios

- [Aria Ops Alert Storm](aria-ops-alert-storm/index.md) — An NSX edge failure generates a cascade of east-west latency alerts across all VMs that transit the edge, producing a classic alert storm.
- [NSX Connectivity Broken](nsx-connectivity-broken/index.md) — Broader NSX connectivity troubleshooting covering DFW, T1 routing, and overlay fabric.
- [VM Performance Degraded](vm-performance-degraded/index.md) — VM performance issues caused by network congestion are investigated via Aria Networks path traces that traverse edge nodes.
