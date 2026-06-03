# NSX Edge Failure / BGP Down

<div class="kb-summary">
NSX edge nodes carry all north-south traffic in and out of the datacenter. When an edge node fails
or its BGP session to the upstream router drops, every VM using that T0 gateway loses external
connectivity. This scenario covers identifying the failure layer — NSX edge, TEP tunnels, or
the physical network — and restoring connectivity with minimal downtime.
</div>

```text
┌───────────────────────────── NSX Edge Failure / BGP Down — Investigation Flow ─────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: External connectivity lost for VMs — north-south traffic not reaching upstream network      ││
│   └────────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                        ┌───────────────────────┼───────────────────────┐                              │
│                        ▼                       ▼                       ▼                              │
│   ┌─────────────────────────────┐  ┌─────────────────────────┐  ┌────────────────────────────┐        │
│   │  All VMs lose external      │  │  Only specific VMs      │  │  Specific destinations     │        │
│   │  connectivity               │  │  affected               │  │  unreachable only          │        │
│   │  → T0 gateway / edge issue  │  │  → Check DFW or T1      │  │  → BGP prefix / route leak │        │
│   └──────────────┬──────────────┘  └────────────┬────────────┘  └────────────┬───────────────┘        │
│                  │                               │                             │                      │
│                  └───────────────────────────────┼─────────────────────────────┘                      │
│                                                  ▼                                                    │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Check edge cluster health in NSX Manager → Check BGP neighbor state on T0 → SSH to edge node      ││
│   └────────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                   ┌────────────────────────────┼────────────────────────────┐                         │
│                   ▼                            ▼                            ▼                         │
│   ┌───────────────────────────┐   ┌───────────────────────────┐  ┌───────────────────────────┐        │
│   │  Edge node degraded       │   │  BGP idle / not estab.    │  │  Edge healthy, BGP estab. │        │
│   │  → check edge VM in       │   │  → check TEP tunnels and  │  │  → problem is upstream    │        │
│   │    vCenter, power state   │   │    upstream switch config │  │    switch or routing      │        │
│   └───────────────────────────┘   └───────────────────────────┘  └───────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

The scope of the outage determines where to start:

| Symptom | Likely layer | First check |
|---|---|---|
| All VMs on the datacenter lose external connectivity | T0 gateway or edge cluster | NSX Manager → edge nodes |
| Only VMs in one tenant segment lose connectivity | T1 gateway or DFW rule | NSX → T1 routing, DFW |
| Specific IP destinations unreachable | BGP prefix advertisement | T0 → BGP neighbor → received routes |
| Intermittent external connectivity | Active-standby edge failover loop | Edge node stability in NSX |

If the outage is global (all external traffic), proceed to Step 2. For partial outages, check the
T1 gateway for that tenant and the relevant DFW rules first.

---

## 2. Check Edge Cluster Health in NSX Manager

NSX Manager → **System** → **Fabric** → **Nodes** → **Edge Transport Nodes**.

Each edge node has a status indicator. Green means healthy. If one node is **Degraded** or
**Down**: the other node in an active-standby pair should have taken over. Confirm which node is
currently active on the T0 gateway.

```bash
# NSX Manager REST API — list all edge nodes and their status
curl -sk -u admin:<password> \
  "https://nsx-manager.domain.local/api/v1/transport-nodes?node_type=EdgeNode" \
  | python3 -m json.tool | grep -E '"display_name"|"status"'
```

---

## 3. Check BGP Neighbor State on the T0 Gateway

NSX Manager → **Networking** → **Tier-0 Gateways** → select the T0 → **BGP** → **Neighbors**.

Each BGP neighbor (upstream router) should show state **Established**. If the state is **Idle**,
**Active**, or **Connect**: the BGP session is down and routes are not being exchanged.

| BGP state | Meaning |
|---|---|
| Established | Healthy — routes are being exchanged |
| Idle | BGP is not attempting to connect — check edge node health first |
| Active | BGP is attempting to connect but not succeeding — check network reachability |
| Connect | TCP connection initiated but not yet acknowledged — usually a transient state |

---

## 4. SSH to the Edge Node — Check BGP and Routes

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

A healthy BGP summary shows the upstream router IP, state **Established**, and a non-zero
count under **PfxRcd** (prefixes received from the upstream router).

```bash
# Ping the upstream router from the edge node uplink interface
ping <upstream-router-ip> interface <uplink-interface-name>

# Check interface status on the edge node
get interfaces
```

---

## 5. Check TEP Connectivity — Edge to ESXi Host Tunnels

Edge nodes communicate with ESXi hosts via GENEVE tunnels over their TEP (Tunnel Endpoint)
VMkernel interfaces. If TEP tunnels are down, overlay traffic cannot reach VMs even if the
edge node itself is up and BGP is established.

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

If TEP pings fail between the ESXi hosts and the edge node, the underlay network (VLAN carrying
TEP traffic) has a problem. Check the physical switch port carrying the TEP VLAN.

---

## 6. Check the Edge VM in vCenter

Edge nodes run as VMs on ESXi hosts. If the edge VM is powered off, suspended, or on a host
that is itself degraded, the edge node goes down entirely.

In vCenter: navigate to the edge VM (typically named `edge-<uuid>`). Verify:

- Power state: should be **Powered On**
- Host: which ESXi host is running the edge VM? Is that host healthy?
- Network adapter: are the edge VM's vNICs connected to the correct port groups?

```powershell
# PowerCLI — find edge VMs and their host placement
Get-VM | Where-Object {$_.Name -like "edge-*"} | Select-Object Name, PowerState, VMHost
```

If the edge VM is on a host that has failed or been put into maintenance mode, vSphere HA will
restart the edge VM on another host. Wait for HA to complete, then recheck BGP state.

---

## 7. Verify Failover — Active-Standby Edge Pair

NSX edge clusters default to **active-standby** for T0 gateways. When the active edge node
fails, the standby takes over in approximately 1 second. BGP reconverges with the upstream router
shortly after (BFD-assisted convergence if BFD is configured).

Check which node is currently active:

NSX Manager → **Networking** → **Tier-0 Gateways** → select T0 → **Configuration** →
**Edge Cluster Member** column shows which edge node is **Active** for each service router.

If failover did not occur (standby did not take over): check the edge cluster configuration and
confirm BFD is enabled on the uplink interfaces.

---

## 8. Physical Switch — Upstream BGP Peer

If both edge nodes report BGP in a non-Established state and the edge VMs and TEPs are healthy,
the problem is the upstream physical switch or router.

Check on the ToR switch:
- BGP neighbor state for the NSX T0 uplink IPs
- Port state for the ports connecting to the edge VM uplinks (trunk VLAN)
- MTU — NSX GENEVE requires MTU 1600 or higher on the underlay; mismatched MTU causes intermittent
  tunnel failures that can destabilise BGP

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

## Related Scenarios

- [Aria Ops Alert Storm](../aria-ops-alert-storm/index.md) — An NSX edge failure generates a cascade of east-west latency alerts across all VMs that transit the edge, producing a classic alert storm.
- [NSX Connectivity Broken](../nsx-connectivity-broken/index.md) — Broader NSX connectivity troubleshooting covering DFW, T1 routing, and overlay fabric.
- [VM Performance Degraded](../vm-performance-degraded/index.md) — VM performance issues caused by network congestion are investigated via Aria Networks path traces that traverse edge nodes.
