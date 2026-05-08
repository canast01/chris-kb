# NSX — Components

## NSX Manager Cluster

The NSX Manager cluster is the control and management plane for the entire NSX environment. It is deployed as three identical VMs that form an active-active cluster with a shared virtual IP (VIP) for management access.

### Manager Roles

| Role | Function |
|---|---|
| Management plane | Hosts the UI and northbound REST API |
| Control plane | Distributes logical network state to transport nodes |
| Policy plane | Processes policy-based configuration (intent-based API) |

All three roles run on each node. The cluster uses Raft consensus (Corfu DB) for state replication — a majority of nodes (2/3) must be healthy for the cluster to accept write operations.

### Cluster Health Verification

```bash
# SSH to any NSX Manager node
nsxcli

# Overall cluster status
get cluster status
# Expected output: Management Cluster Status: STABLE, Control Cluster Status: STABLE

# Individual node reachability
get managers

# Corfu (Raft DB) cluster status
get corfu-cluster status

# Services on this node
get services
```

### NSX Manager API

The REST API is the primary automation interface. NSX-T has two API surfaces:

| API | Base URL | Use |
|---|---|---|
| Management Plane API (MP API) | `/api/v1/` | Direct object manipulation; legacy |
| Policy API | `/policy/api/v1/infra/` | Intent-based; preferred for new automation |

Authenticate with HTTP Basic Auth or session token:

```bash
# Basic auth example
curl -sk -u 'admin:Password123!' \
  -H "Accept: application/json" \
  "https://nsx-manager.corp.local/api/v1/cluster/status"

# Session-based auth (get a token)
curl -sk -u 'admin:Password123!' \
  -X POST \
  "https://nsx-manager.corp.local/api/v1/aaa/session" \
  -c /tmp/nsx-session.txt

# Reuse session
curl -sk -b /tmp/nsx-session.txt \
  "https://nsx-manager.corp.local/api/v1/cluster/status"
```

---

## Transport Nodes

Transport nodes are the data plane participants in the NSX overlay. Every ESXi host and every Edge node that participates in overlay networking is a transport node.

### ESXi Host Transport Nodes

When a vSphere cluster is prepared for NSX (via a Transport Node Profile), NSX installs VIBs on each ESXi host and creates a VMkernel adapter for TEP traffic.

| Component | Purpose |
|---|---|
| NSX VIBs | NSX kernel modules installed on ESXi |
| TEP VMkernel (vmkX) | The IP used for Geneve encapsulation |
| N-VDS or vDS | Virtual switch that carries TEP and overlay port groups |

```bash
# Verify NSX VIBs on an ESXi host
esxcli software vib list | grep -i nsx

# Expected VIBs (NSX 4.x):
# nsx-exporter, nsx-netx, nsx-platform-client, nsx-aggservice, etc.

# Verify TEP vmkernel IP is assigned
esxcli network ip interface ipv4 get | grep -A3 vmk

# Confirm TEP reachability
vmkping -I vmk<n> <remote-tep-ip>
```

### Edge Node Transport Nodes

Edge nodes are NSX-deployed VMs or bare-metal appliances that host the north-south gateway functions. They are transport nodes configured with both overlay (TEP) and uplink (physical-facing) interfaces.

| Interface | Name | Purpose |
|---|---|---|
| Management | eth0 | SSH, NSX Manager communication |
| Uplink 0 | fp-eth0 | Physical router-facing (BGP peer) |
| Uplink 1 | fp-eth1 | Second physical path (HA or ECMP) |
| Overlay | nsx-geneve | Geneve encap for overlay within Edge |

```bash
# SSH to Edge node
get interfaces

# Sample output:
# fp-eth0  UP  10.0.0.2/30  mtu 1500
# fp-eth1  UP  10.0.0.6/30  mtu 1500
# nsx-geneve  UP  192.168.201.10/24  mtu 9000

get service dataplane   # Confirm dataplane is running
get service router      # Confirm routing engine is running
```

---

## Tunnel Endpoints (TEPs)

Every transport node has one or more TEP IPs. These are the source and destination addresses used in the outer Geneve header when encapsulating VM-to-VM traffic across the physical underlay.

### Geneve Encapsulation

Geneve (Generic Network Virtualization Encapsulation) is the overlay protocol used by NSX-T (not VXLAN). Packets are encapsulated with:

- Outer Ethernet header (TEP-to-TEP)
- Outer IP header (TEP source → TEP destination)
- UDP header (destination port 6081)
- Geneve header (includes VNI — Virtual Network Identifier)
- Inner Ethernet + IP + payload

```
[Outer ETH][Outer IP: TEP-src → TEP-dst][UDP 6081][Geneve VNI=5001][Inner ETH][Inner IP: VM-src → VM-dst][Payload]
```

### Verify Tunnel Health

```bash
# From NSX Manager CLI
nsxcli
get tunnel status
# Shows state: UP or DOWN for each TEP pair

# From ESXi host — verify Geneve encap interface
esxcli network ip interface list | grep -i geneve

# Tunnel to a specific remote TEP
get tunnel status 192.168.200.12
```

---

## Distributed Firewall (DFW)

The Distributed Firewall is NSX's micro-segmentation engine. Rules execute as kernel-level filters in the vNIC of every VM, enforced by the ESXi hypervisor before the packet enters or leaves the vNIC.

### DFW Architecture

```
VM vNIC → [DFW filter] → vDS port → physical uplink
```

The DFW filter is stateful (connection tracking per TCP/UDP flow). Rules are pushed from the NSX Manager control plane to every ESXi transport node and applied locally — no traffic hairpins to a central firewall.

### Policy Structure

```
Security Policy (ordered)
└── Rules (ordered within policy)
    ├── Rule 1: Allow Web (80/443) from LB to App group
    ├── Rule 2: Allow DB (3306) from App group to DB group
    └── Rule 3: Default deny (applied-to: this policy's groups)
```

DFW Categories (evaluated top to bottom):

| Category | Priority | Typical Use |
|---|---|---|
| Ethernet | 1 | L2 rules, MAC-based |
| Emergency | 2 | Break-glass blocks; highest priority IP rules |
| Infrastructure | 3 | Management traffic: vCenter, backup, monitoring |
| Environment | 4 | Inter-zone segmentation (prod/dev, PCI boundary) |
| Application | 5 | Application-specific micro-segmentation |

### DFW Inspection on ESXi Host

```bash
# List all DFW filters (one per VM vNIC)
summarize-dvfilter

# Output shows: VM name → vNIC → filter name
# Example: my-vm-01.eth0 -> nic-12345-eth0-vmware-sfw.2

# Show rules applied to a VM vNIC filter
vsipioctl getrules -f nic-12345-eth0-vmware-sfw.2

# Show rule hit counts (non-zero = traffic matched this rule)
vsipioctl getstats -f nic-12345-eth0-vmware-sfw.2

# Show security groups (address sets) in use
vsipioctl getaddrsets -f nic-12345-eth0-vmware-sfw.2
```

### DFW Rule Hit Count Verification

After a policy change, confirm the new rules are receiving hits:

```bash
# Continuous stats — run on ESXi host
watch -n 5 'vsipioctl getstats -f <filter-name>'
```

If a deny rule has non-zero hits when you expect traffic to be allowed, the rule is actively blocking. Check the rule ordering or the group membership of the source/destination VMs.

---

## Segments (Logical Switches)

Segments are NSX's Layer 2 logical networks. VMs connected to the same segment can communicate without crossing a gateway, regardless of which physical host they run on.

### Segment Types

| Type | Backing | Use Case |
|---|---|---|
| Overlay | Geneve (VNI) | VM workload networking |
| VLAN-backed | Physical VLAN | Management networks, Edge uplinks |

### Segment VNI

Each overlay segment has a unique VNI (Virtual Network Identifier) assigned from the VNI pool. The VNI appears in the Geneve header to identify which logical segment a packet belongs to.

```bash
# Find the VNI of a segment
nsxcli
get logical-switch <segment-id> | grep VNI

# Or via API
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/logical-switches?display_name=seg-prod-web"
```

### Segment Connectivity

A segment gains routed connectivity by connecting it to a Tier-1 gateway's downlink port. The T1 becomes the default gateway for VMs on that segment.

---

## Tier-0 and Tier-1 Gateways

### Tier-0 Gateway

The T0 gateway is the north-south boundary. It peers with physical routers via BGP or static routes. T0 runs exclusively on Edge nodes.

| HA Mode | Behaviour | Use Case |
|---|---|---|
| Active/Standby | One Edge node active; other is hot standby | Most deployments; simpler failover |
| Active/Active | ECMP across multiple Edge nodes | High-throughput requirements |

T0 failure modes:

```bash
# Check HA state from Edge node
get edge-cluster status
# Shows: Active or Standby for this Edge

# Force failover (run on Active Edge)
set edge-cluster failover
```

### Tier-1 Gateway

T1 gateways provide distributed routing — the routing function runs on every ESXi transport node that hosts VMs connected to its segments. T1 does not require an Edge node unless services (NAT, LB, VPN) are configured.

T1-to-T0 link: When you connect a T1 to a T0, NSX creates an internal transit link (/31 subnet) between them. No manual route configuration is needed.

Route advertisement from T1 to T0 (configure in T1 settings):

| Route Type | Advertises |
|---|---|
| `TIER1_CONNECTED` | Subnets of directly connected segments |
| `TIER1_STATIC` | Static routes configured on the T1 |
| `TIER1_LB_VIP` | Load balancer VIP addresses |
| `TIER1_NAT` | NAT'ed addresses |

---

## Edge Cluster

Edge clusters group Edge nodes for HA and for assigning gateway services. A T0 or T1 with services (NAT, LB, VPN) must reference an Edge cluster.

```bash
# List Edge clusters and members
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/edge-clusters" | python3 -m json.tool

# Health of a specific Edge cluster
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/edge-clusters/<cluster-id>/status"
```

### Edge Node Sizing

| Size | vCPU | Memory | Throughput | Typical Use |
|---|---|---|---|---|
| Small | 2 | 8 GB | ~5 Gbps | Lab only |
| Medium | 4 | 16 GB | ~40 Gbps | Dev/test |
| Large | 8 | 32 GB | ~100 Gbps | Production |
| Bare Metal | Physical | 256 GB | Line rate | High-traffic edge |

Production Edge nodes must be deployed on hosts **separate** from compute workload hosts to prevent resource contention.

---

## IPAM and DHCP

NSX includes built-in IPAM for IP pool management and a distributed DHCP server that runs on ESXi hosts (no dedicated DHCP VM required).

### IP Pools (for TEP allocation)

```bash
# List IP pools
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/pools/ip-pools"

# Check allocations from a pool
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/pools/ip-pools/<pool-id>/ip-allocations"
```

### Segment DHCP

NSX can serve DHCP for VM workloads directly from the segment configuration. The DHCP server runs distributed on ESXi hosts — each host serves DHCP to local VMs.

Configure via Policy API:

```bash
curl -sk -u 'admin:password' \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "dhcp_config": {
      "resource_type": "SegmentDhcpV4Config",
      "server_address": "10.0.1.1/24",
      "dns_servers": ["10.0.0.53"],
      "lease_time": 86400,
      "options": {
        "option121": {
          "static_routes": [
            {"network": "0.0.0.0/0", "next_hop": "10.0.1.1"}
          ]
        }
      }
    }
  }' \
  "https://<nsx-manager>/policy/api/v1/infra/segments/seg-prod-web"
```

---

## VPN Services

NSX-T supports IPsec site-to-site VPN and L2 VPN for extending Layer 2 segments to remote sites. Both run on Edge nodes.

### IPsec VPN

IPsec VPN runs on the T0 or T1 gateway (with services on an Edge cluster). Configure via Policy API or UI: **Networking → VPN → IPsec Sessions**.

```bash
# Check IPsec session status from Edge CLI
get vpn ipsec session list
# Shows: Session ID, Peer, Status, Bytes In/Out
```

| IKE Profile | Recommended Settings |
|---|---|
| IKE Version | IKEv2 |
| Encryption | AES-256 |
| Digest | SHA-256 |
| DH Group | Group 14 (2048-bit) or Group 20 (ECP384) |
| SA Lifetime | 28800 seconds |

### L2 VPN

L2 VPN extends a segment across sites over an IPsec tunnel. The remote site requires an L2 VPN client (autonomous edge appliance or another NSX Manager).

```bash
# Check L2 VPN session from Edge CLI
get vpn l2vpn session list
get vpn l2vpn session <session-id>
```
