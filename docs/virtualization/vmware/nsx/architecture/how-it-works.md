---
tags:
  - architecture
  - nsx
  - nsx-4
  - vmware
---
# NSX — How It Works

<div class="kb-summary">
How It Works reference covering API Surfaces, Transport Nodes, Geneve Encapsulation, Transport Zones, Gateway Architecture — T0 and T1 and 7 more sections.

*Applies to: NSX-T 3.x · NSX 4.x*
</div>
![NSX — How It Works](../../../../assets/virtualization-vmware-nsx-architecture-how-it-works.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Admin" as ADM
participant "NSX Manager\n(policy API)" as MGR
participant "NSX Controller\n(cluster)" as CTL
participant "ESXi Transport Node\n(TEP + N-VDS)" as ESX
participant "Edge Node\n(Tier-0 / Tier-1 GW)" as EDGE
participant "Physical Fabric\n(BGP peer)" as FABRIC

ADM -> MGR: Define segment / DFW policy
MGR -> CTL: Distribute intent
CTL -> ESX: Push TEP config + DFW rules
CTL -> EDGE: Push routing config
EDGE -> FABRIC: BGP advertise prefixes
FABRIC --> EDGE: BGP ack
ESX --> CTL: Config applied
CTL --> MGR: Realisation complete
MGR --> ADM: Policy enforced
@enduml
```

## Control and Data Plane

### NSX 3-Plane Architecture

```mermaid
graph TB
    subgraph MGMT["Management Plane — NSX Manager Cluster"]
        MGR1["NSX Manager 1<br/>Policy API · REST · UI"]
        MGR2["NSX Manager 2<br/>Policy API · REST · UI"]
        MGR3["NSX Manager 3<br/>Policy API · REST · UI"]
        MGR1 <--> MGR2
        MGR2 <--> MGR3
        MGR1 <--> MGR3
    end

    subgraph CTRL["Control Plane — Central Control Plane (CCP)"]
        CCP["Central Control Plane<br/>Embedded in NSX Manager<br/>Computes forwarding tables<br/>Pushes config via RPC/messaging"]
    end

    subgraph DATA["Data Plane — Transport Nodes"]
        HOST1["ESXi Host 1<br/>VMkernel NSX module<br/>DLR · DFW · TEP vmknic"]
        HOST2["ESXi Host 2<br/>VMkernel NSX module<br/>DLR · DFW · TEP vmknic"]
        EDGE["Edge VM / Bare-Metal<br/>Service Router<br/>BGP · NAT · LB · VPN"]
    end

    subgraph TUNNEL["GENEVE Overlay Tunnels"]
        GEN["GENEVE UDP 6081<br/>VNI-tagged frames<br/>TEP-to-TEP encapsulation"]
    end

    MGMT -->|"Config sync — Policy API"| CTRL
    CTRL -->|"State push via RPC<br/>forwarding tables · segment state<br/>DFW rules · TEP assignments"| HOST1
    CTRL -->|"State push via RPC<br/>forwarding tables · segment state<br/>DFW rules · TEP assignments"| HOST2
    CTRL -->|"State push via RPC<br/>routing config · gateway state"| EDGE
    HOST1 <-->|"GENEVE tunnel<br/>E-W overlay traffic"| GEN
    HOST2 <-->|"GENEVE tunnel<br/>E-W overlay traffic"| GEN

    classDef mgmtStyle fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef ctrlStyle fill:#15803d,stroke:#166534,color:#fff
    classDef dataStyle fill:#b45309,stroke:#92400e,color:#fff
    classDef tunnelStyle fill:#7c3aed,stroke:#6d28d9,color:#fff

    class MGR1,MGR2,MGR3 mgmtStyle
    class CCP ctrlStyle
    class HOST1,HOST2,EDGE dataStyle
    class GEN tunnelStyle
```

### Edge Node Transport Nodes

Edge nodes are NSX-deployed VMs or bare-metal appliances hosting north-south gateway functions.

| Interface | Name | Purpose |
|---|---|---|
| Management | eth0 | SSH, NSX Manager communication |
| Uplink 0 | fp-eth0 | Physical router-facing (BGP peer) |
| Uplink 1 | fp-eth1 | Second physical path (HA or ECMP) |
| Overlay | nsx-geneve | Geneve encap for overlay within Edge |

```bash
# SSH to Edge node
get interfaces
get service dataplane   # Confirm dataplane is running
get service router      # Confirm routing engine is running
```

---

## Geneve Encapsulation

NSX uses Geneve (port 6081) — not VXLAN. The VNI identifies which logical segment a packet belongs to.

```text
[Outer ETH][Outer IP: TEP-src → TEP-dst][UDP 6081][Geneve VNI=5001][Inner ETH][Inner IP: VM-src → VM-dst][Payload]
```

Geneve carries extensible metadata (security group tags, service chain IDs) inline — not possible with VXLAN.

```bash
# Verify tunnel health from NSX Manager CLI
nsxcli
get tunnel status
get tunnel status <remote-tep-ip>
```

---

## Transport Zones

Transport Zones define which transport nodes can host VMs on a given segment.

| Zone Type | Encapsulation | Hosts |
|---|---|---|
| Overlay TZ | Geneve (VNI-based) | ESXi hosts + Edge nodes |
| VLAN TZ | 802.1Q VLAN tagging | Edge nodes (uplinks to physical routers) |

A transport node can participate in multiple zones. ESXi hosts typically join one overlay TZ; Edge nodes join both overlay and VLAN TZs.

---

## Gateway Architecture — T0 and T1

### Tier-1 Gateway (Distributed Routing)

T1 gateways perform routing at the ESXi host level — east-west traffic between subnets on the same T1 never leaves the host.

- Runs as a logical router instance on every ESXi transport node
- Connects to segments via downlink interfaces (default gateway for VMs)
- Connects upward to T0 via an auto-created internal transit link

Route advertisement from T1 to T0 (configure in T1 settings):

| Route Type | Advertises |
|---|---|
| `TIER1_CONNECTED` | Subnets of directly connected segments |
| `TIER1_STATIC` | Static routes on the T1 |
| `TIER1_LB_VIP` | Load balancer VIP addresses |
| `TIER1_NAT` | NAT'ed addresses |

### Tier-0 Gateway (North-South Routing)

T0 gateways run on Edge nodes and peer with physical routers via BGP or static routes.

| HA Mode | Behaviour |
|---|---|
| Active/Standby | One Edge node active; other is hot standby |
| Active/Active | ECMP across all Edge nodes; requires equal-cost uplinks |

```bash
# Check HA state from Edge node
get edge-cluster status
set edge-cluster failover   # Force failover from active Edge
```

### Routing Flow — VM to External

```text
VM → vNIC → DFW filter → T1 distributed instance (same ESXi host)
  → T0 Service Router (Edge node) → Physical router (BGP peer) → Internet
```

---

## Edge Cluster

Edge clusters group Edge nodes for HA and gateway service assignment. Any T0 or T1 with services (NAT, LB, VPN) must reference an Edge cluster.

| Size | vCPU | Memory | Throughput | Use |
|---|---|---|---|---|
| Small | 2 | 8 GB | ~5 Gbps | Lab only |
| Medium | 4 | 16 GB | ~40 Gbps | Dev/test |
| Large | 8 | 32 GB | ~100 Gbps | Production |
| Bare Metal | Physical | 256 GB | Line rate | High-throughput edge |

Edge VMs must be deployed on hosts **separate** from compute workload hosts.

---

## Distributed Firewall (DFW)

The DFW runs as a kernel-level stateful firewall at every VM vNIC on every ESXi host. Traffic is intercepted before it enters or leaves the vNIC — even between two VMs on the same host.

### DFW Categories (evaluated top to bottom)

| Category | Priority | Typical Use |
|---|---|---|
| Ethernet | 1 | L2 / MAC-based rules |
| Emergency | 2 | Break-glass blocks |
| Infrastructure | 3 | Management, backup, monitoring allow rules |
| Environment | 4 | Inter-zone segmentation (prod/dev, PCI boundary) |
| Application | 5 | Application-specific micro-segmentation |

Default rule (65535): **DROP** — do not change.

### DFW Inspection on ESXi Host

```bash
# List all DFW filters (one per VM vNIC)
summarize-dvfilter

# Show rules applied to a vNIC filter
vsipioctl getrules -f nic-12345-eth0-vmware-sfw.2

# Show rule hit counts
vsipioctl getstats -f nic-12345-eth0-vmware-sfw.2

# Show security groups (address sets) in use
vsipioctl getaddrsets -f nic-12345-eth0-vmware-sfw.2
```

---

## Segments

Segments are NSX Layer 2 logical networks. VMs on the same segment communicate without crossing a gateway, regardless of physical host.

| Type | Backing | Use Case |
|---|---|---|
| Overlay | Geneve (VNI) | VM workload networking |
| VLAN-backed | Physical VLAN | Management networks, Edge uplinks |

```bash
# Find the VNI of a segment
nsxcli
get logical-switch <segment-id> | grep VNI
```

---

## IPAM and DHCP

NSX includes built-in IPAM for IP pool management and a distributed DHCP server running on ESXi hosts — no dedicated DHCP VM required.

```bash
# List IP pools
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/pools/ip-pools"

# Check pool allocations
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/pools/ip-pools/<pool-id>/ip-allocations"
```

---

## VPN Services

NSX supports IPsec site-to-site VPN and L2 VPN on Edge nodes (T0 or T1 with Edge cluster).

```bash
# Check IPsec sessions from Edge CLI
get vpn ipsec session list

# Check L2 VPN sessions
get vpn l2vpn session list
```

| IKE Setting | Recommended Value |
|---|---|
| IKE Version | IKEv2 |
| Encryption | AES-256 |
| Digest | SHA-256 |
| DH Group | Group 14 or Group 20 |

---

## NSX-T vs NSX-V

| Feature | NSX-T (current) | NSX-V (end-of-life) |
|---|---|---|
| Overlay protocol | Geneve | VXLAN |
| Control plane | Embedded in Manager cluster | Separate Controller VMs |
| Multi-hypervisor | Yes (ESXi, KVM) | ESXi only |
| VDS requirement | vDS 7.0+ | vDS 6.x |
| EoL status | Supported | **End-of-life — no security patches** |

NSX-V migrations are critical — NSX-V receives no patches.

---

## Ports and Logs

| Use | Protocol | Port |
|---|---|---|
| NSX Manager UI / API | HTTPS | 443 |
| Geneve overlay encapsulation | UDP | 6081 |
| BFD (path failure detection) | UDP | 3784 |
| BGP (T0 to physical router) | TCP | 179 |
| NSX Manager SSH | TCP | 22 |
| Syslog (TLS) | TCP | 6514 |

**Key log paths (NSX Manager):**

- `/var/log/vmware/nsx-manager/` — manager and policy service logs
- `/var/log/vmware/nsx-manager/audit.log` — admin actions, role changes
- `/var/log/vmware/nsx-controller/` — control plane logs

**Edge node logs (SSH):**

```bash
get log-file syslog follow   # live tail
get log-file auth.log        # authentication events
```

## See also

- [NSX — Design Standards](design-standards/)
- [NSX — Deploy](../deploy/)
- [NSX — Integrations](integrations/)
