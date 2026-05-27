# NSX — CLI Reference

Commonly used NSX-T Manager and Edge CLI commands for managing overlays, routing, and distributed firewall. NSX-T is VMware's software-defined networking platform — it creates virtual networks (segments), virtual routers (gateways), and enforces firewall rules at the hypervisor level.

> NSX Manager and Edge Node CLIs are accessed via SSH. Log in as `admin`. Run `nsxcli` on the Manager to enter the NSX management shell.

---

## System

### Cluster and Manager Health

```bash
nsxcli

# NSX Manager cluster members and status
get managers
get clusters
get cluster status

# Service status on this node
get services

# Specific service status
get service http
get service manager
get service controller
```
┌───────────────────────────────────────── NSX — CLI Reference ─────────────────────────────────────────┐
│                                                                                                       │
│  NSX Manager CLI, Edge Node CLI, and REST API commands for operations.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               NSX Manager CLI                │  │                Edge Node CLI                │   │
│   │              get cluster status              │  │             get logical-routers             │   │
│   │             get management-plane             │  │           get bgp neighbor summary          │   │
│   │               get certificate                │  │               get route table               │   │
│   │             start service <svc>              │  │              ping <IP> vrf <n>              │   │
│   │                get node-uuid                 │  │               traceroute <IP>               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Manager CLI for cluster health; Edge CLI for routing/BGP/path checks.                                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             NSX Policy REST API              │  │             Useful curl Examples            │   │
│   │           GET /policy/api/v1/infra           │  │           curl -k -u admin:pass \           │   │
│   │          GET /api/v1/cluster/status          │  │            -X GET https://mgr/...           │   │
│   │          POST /policy/api/v1/infra/          │  │             jq .results[].status            │   │
│   │         GET /api/v1/transport-nodes          │  │           Token auth: Bearer token          │   │
│   │          DELETE /policy/api/v1/...           │  │            Postman collection NSX           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NSX Manager cluster VMs, Edge VMs on ESXi, management network, vCenter                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NSX Manager CLI = SSH to manager appliance; admin account access                                     │
│  Edge CLI      = SSH to edge node; routing, BGP, NAT diagnostics                                      │
│  Policy API    = NSX REST API /policy/api/v1; primary config interface                                │
│  Management API= NSX REST API /api/v1; legacy + infra ops endpoints                                   │
│  Transport node= ESXi or Edge with N-VDS installed; dataplane element                                 │
│  BGP neighbor  = Edge peers; get bgp shows session state + prefixes                                   │
│  VRF           = Virtual Routing and Forwarding; per-router context                                   │
│  cluster status= manager API; shows CCP/MP health of all 3 nodes                                      │
│  Bearer token  = JWT token for NSX API auth; alternative to Basic auth                                │
│  jq            = JSON query tool; parses NSX API responses in shell                                   │
│  logical-router= Edge data structure; mapped to T0/T1 gateway object                                  │
│  node-uuid     = unique ID of NSX appliance; used in API paths                                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Appliance Configuration

```bash
# Add a static route on the appliance (out-of-band management)
set appliance gw-route <prefix>/<mask> <gateway_ip>

# Check current appliance routes
get appliance routes

# Start or stop the NSX Manager UI
set appliance ui start
set appliance ui stop

# Set hostname
set appliance hostname <new_hostname>
```

### NTP and Time

```bash
# Check NTP status
get service ntp
get ntp servers

# Set NTP server
set service ntp server <ntp_ip>
```

### Certificates

```bash
# List installed certificates
get certificate api
get certificate cluster

# Thumbprint of the API cert (used for trust verification)
get certificate api thumbprint
```

### Syslog

```bash
# Show configured syslog exporters
get service syslog exporters

# Add a syslog target
set service syslog exporter <name> level info protocol UDP server <syslog_ip> port 514

# Remove an exporter
del service syslog exporter <name>
```

### Backup Status

```bash
# View backup configuration
get service manager backup

# Trigger a manual backup (NSX Manager UI is preferred)
# API: POST /api/v1/node/backups/create
```

### Quick Reference

| Task | Command |
|---|---|
| Cluster health | `get cluster status` |
| All services up? | `get services` |
| NSX version | `get version` |
| Node IPs | `get node interfaces` |
| BGP peer state | `vrf <id>` → `get bgp neighbor summary` |
| Corfu DB health | `get corfu-cluster status` |
| Syslog targets | `get service syslog exporters` |

---

## Transport Nodes

Transport nodes are the ESXi hosts and Edge nodes that participate in the NSX overlay network. TEPs (Tunnel Endpoints) are the VMkernel IPs that ESXi hosts use to encapsulate traffic in Geneve tunnels.

### Transport Nodes (NSX Manager CLI)

```bash
nsxcli

# List all transport nodes (ESXi hosts + Edge nodes)
get transport-nodes

# Detail for a specific transport node
get transport-node <id>

# Operational status (UP/DOWN/DEGRADED)
get transport-node <id> status

# Summary status for all nodes
get transport-node-status
```

### Transport Zones

```bash
# List transport zones (overlay and VLAN backed)
get transport-zone

# Detail for a specific zone
get transport-zone <name>

# Which transport nodes are in a zone
get transport-nodes | grep <zone_name>
```

### Tunnel Endpoints (TEPs)

```bash
# List all TEP IPs and associated hosts
get tunnel endpoints

# Tunnel status between all TEP pairs
get tunnel status

# Tunnel to a specific remote TEP
get tunnel status <remote_tep_ip>
```

### ESXi Host Fabric Verification

SSH to the ESXi host:

```bash
# NSX VIBs installed
esxcli software vib list | grep -i nsx

# VDS and NSX Port ID mapping
net-vdl2 -M all -s 0

# TEP VMkernel IP and state
esxcli network ip interface ipv4 get | grep -A2 vmk

# TEP uplink binding
esxcli network ip interface list | grep -i nsx
```

### Edge Node Fabric Status

SSH to Edge node:

```bash
# Edge interfaces (uplinks + overlay)
get interfaces

# Geneve overlay interface
get interface nsx-geneve

# Uplink state
get interface fp-eth0
get interface fp-eth1
```

### Common Issues

| Symptom | Check |
|---|---|
| Transport node status DEGRADED | `get transport-node <id> status` — check VIB version mismatch |
| Tunnel DOWN between two hosts | `get tunnel status` — check TEP IP reachability and MTU ≥ 1600 |
| ESXi host not joining fabric | `esxcli software vib list | grep nsx` — VIB may have failed install |
| BFD session flapping | Underlay MTU or path instability — check physical switch |
| Segment VMs can't communicate | `get logical-switch <id> status` + `get tunnel status` between both host TEPs |

### Maintenance Mode Workflow

```bash
# Before putting ESXi host in maintenance mode:
# 1. Check no active vSAN resync
esxcli vsan debug resync list

# 2. Verify NSX DFW is not the sole enforcement point for a segment
nsxcli
get transport-node <id> status

# 3. After host in maintenance mode — confirm tunnels reconverged
get tunnel status
```

---

## Segments

Segments are NSX's virtual Layer 2 networks. Each segment has a VNI (VXLAN Network Identifier) and uses Geneve encapsulation to carry traffic between ESXi hosts over the physical underlay.

### Segments (NSX Manager CLI)

```bash
nsxcli

# List all logical switches / segments
get logical-switches

# Detail for a specific segment (VNI, replication mode, transport zone)
get logical-switch <id>

# Operational status (UP/DOWN)
get logical-switch <id> status

# Traffic statistics for a segment
get logical-switch <id> stats
```

### Logical Ports (VMs connected to a segment)

```bash
# List all logical ports
get logical-ports

# Detail for a specific port
get logical-port <id>

# Port operational state
get logical-port <id> status

# Traffic stats on a specific port
get logical-port <id> stats
```

### Geneve Tunnels (Overlay)

Segments use Geneve encapsulation over the underlay. Verify tunnel health from NSX Manager CLI:

```bash
# List tunnel endpoints (TEPs) — shows VTEP IPs and state
get tunnel endpoints

# Tunnel status between all TEP pairs
get tunnel status

# Tunnel for a specific remote TEP
get tunnel status <remote_tep_ip>
```

### Segment Troubleshooting

```bash
# Is the segment UP?
get logical-switch <id> status

# Find the VNI of a segment (needed for packet analysis)
get logical-switch <id> | grep VNI

# Which hosts have TEPs in this transport zone?
get transport-nodes

# Is the Geneve tunnel UP between two hosts?
get tunnel status <remote_tep_ip>

# On the ESXi host — confirm Geneve encap
esxcli network ip interface ipv4 get | grep vmk
esxcli network ip route ipv4 list | grep <tep_subnet>
```

### Replication Modes

| Mode | Use Case |
|---|---|
| `MTEP` (Head-End Replication) | BUM traffic replicated by ingress TEP — simpler, higher bandwidth |
| `HIERARCHICAL_TWO_TIER` | Uses designated replicator — better for large environments |

```bash
# Check replication mode for a segment
get logical-switch <id> | grep -i replication
```

---

## Gateways

NSX uses Tier-0 gateways for north-south routing (in/out of the data center) and Tier-1 gateways for east-west routing (between segments). Tier-0 connects to physical routers via BGP or static routes. All gateway CLI inspection runs on the Edge node.

### List Gateways (NSX Manager)

```bash
nsxcli
get logical-routers
# Output includes: UUID, VRF ID, type (TIER0 / TIER1), and Edge cluster
```

### Enter Gateway Context on Edge Node

SSH to the Edge node, then:

```bash
# List all router VRFs on this Edge
get logical-routers

# Enter a specific router's VRF
vrf <vrf_id>

# Exit VRF context
exit
```

### Routing

```bash
# Show routing table (all protocols)
vrf <vrf_id>
get route

# Detailed route table (next-hop, preference, metric)
get route detail

# Filter for a specific prefix
get route <prefix>/<mask>

# Forwarding information base (FIB)
get forwarding
```

### BGP

```bash
# BGP neighbor summary (all peers, state, prefixes)
get bgp neighbor summary

# Detailed view of a specific neighbor
get bgp neighbor <neighbor_ip>

# Routes received from a neighbor
get bgp neighbor <neighbor_ip> routes

# Routes advertised to a neighbor
get bgp neighbor <neighbor_ip> advertised-routes

# BGP configuration summary
get bgp config
```

### Static Routes

```bash
# Static routes on this gateway
get route static
```

### Interfaces

```bash
# All interfaces (uplinks, downlinks, loopback)
get interfaces

# Specific interface detail
get interface <name>

# Interface counters (tx/rx bytes, drops)
get interface <name> counters
```

### HA and Failover

```bash
# HA state (Active/Standby)
get edge-cluster status

# Force failover to standby (Active→Standby)
# Only run on Active Edge node
set edge-cluster failover

# Edge high availability info
get high-availability channels
get high-availability status
```

### Gateway Quick Reference

| Task | Command |
|---|---|
| Find gateway VRF ID | `get logical-routers` |
| Check BGP sessions | `vrf <id>` → `get bgp neighbor summary` |
| Verify route exists | `vrf <id>` → `get route <prefix>` |
| Check interface status | `vrf <id>` → `get interfaces` |
| Check HA state | `get edge-cluster status` |
| Force failover | `set edge-cluster failover` |

---

## Edge Nodes

Edge nodes are dedicated VMs or bare-metal appliances that host Tier-0 and Tier-1 gateway functions. They handle north-south traffic, NAT, load balancing, and BGP peering with physical routers.

```bash
# Connect to Edge Node via SSH (admin) and run:

# Services running on this edge
get services
get service dataplane
get service router

# System resources
get node
get node cpu-usage
get node memory

# Uplinks and overlay interfaces
get interfaces
get interface fp-eth0

# Routing (in gateway VRF context)
vrf <lr_id>
get route
get forwarding
get bgp neighbor summary

# Connectivity tests from Edge
ping <ip>
traceroute <ip>
curl http://<ip>
```

---

## Distributed Firewall (DFW)

The NSX Distributed Firewall enforces rules at the virtual NIC of each VM. Rules are applied at the hypervisor level, so traffic is inspected even between VMs on the same host, before it hits the physical network.

### DFW Statistics — NSX Manager

```bash
nsxcli

# Firewall rule statistics (hit counts, bytes)
get firewall stats

# DFW summary across all transport nodes
get dfw stats
```

### DFW Inspection on ESXi Host

All commands run as root on the ESXi host:

```bash
# List all DFW filters attached to VMs on this host
summarize-dvfilter

# Output format shows: vmname -> vnic -> filter_name
# Example filter name: nic-12345-eth0-vmware-sfw.2
```

```bash
# Get DFW rules applied to a specific filter
vsipioctl getrules -f <filter_name>

# Show address sets (IP groups, security groups) used in rules
vsipioctl getaddrsets -f <filter_name>

# Per-rule hit statistics for a filter
vsipioctl getstats -f <filter_name>

# Show service / port-protocol objects
vsipioctl getservices -f <filter_name>
```

### Identifying a VM's Filter Name

```bash
# Step 1 — find the VM's world ID
esxcli vm process list | grep -A5 <vm_name>

# Step 2 — list filters and match to VM
summarize-dvfilter | grep -A3 <vm_name>

# Step 3 — inspect rules for that filter
vsipioctl getrules -f <filter_name_from_step2>
```

### Rule Output Interpretation

```text
# Sample getrules output:
ruleset domain-c12:500  {
  rule 1234 at 1 inout protocol any from any to any accept;
  rule 1235 at 2 inout protocol tcp from addrset sg-web to addrset sg-db port {3306} accept;
  rule 65535 at 99 inout protocol any from any to any drop;
}
```

| Field | Meaning |
|---|---|
| `rule <id>` | NSX DFW rule ID — matches Policy > Security > Rules |
| `inout` | Applies to both ingress and egress |
| `addrset` | References a security group or IP set |
| `drop` | Packet silently dropped |
| `reject` | TCP RST / ICMP unreachable sent |
| `accept` | Traffic permitted |

### DFW Troubleshooting

```bash
# Confirm DFW is enforced on a VM (filter count > 0)
summarize-dvfilter | grep -c <vm_name>

# Check if a rule is being hit (non-zero pkt count)
vsipioctl getstats -f <filter_name> | grep -v " 0 pkts"

# Add VM to DFW exclusion list (NSX Manager only, not CLI)
# System → Fabric → Nodes → Host Transport Nodes → DFW Exclusion List
```

---

## NAT & Load Balancing

NAT translates IP addresses at the gateway — typically used to let VMs with private IPs reach the internet (SNAT) or to expose a service externally via a public IP (DNAT). The NSX load balancer distributes traffic across a pool of backend VMs.

### NAT (on Edge Node in gateway VRF)

```bash
vrf <lr_id>

# List all NAT rules
get nat rules

# NAT rule hit statistics
get nat rule stats

# SNAT translations active
get nat translations
```

### NAT Rule Output Fields

| Field | Meaning |
|---|---|
| Rule ID | Matches NSX Manager policy NAT rule ID |
| Type | `SNAT`, `DNAT`, `REFLEXIVE`, `NO_NAT` |
| Match Source | Source IP/prefix triggering this rule |
| Match Destination | Destination IP/prefix |
| Translated Address | Address substituted in the packet |
| Action | `SNAT` = rewrite source; `DNAT` = rewrite destination |

### Troubleshooting NAT

```bash
# Confirm rule exists for expected source
get nat rules | grep <source_ip>

# Check translation table for active SNAT flows
get nat translations | grep <internal_ip>

# Verify interface has correct uplink for NAT
get interfaces
```

### Load Balancer (on Edge Node)

NSX-T load balancer runs on the Edge node. All commands below run in the Edge CLI (not VRF context).

```bash
# Overall load balancer status
get load-balancer status

# List virtual servers (VIPs)
get load-balancer virtual-servers

# Server pools and member state
get load-balancer pools

# Specific pool detail (member health)
get load-balancer pool <pool_id>

# Active connections per virtual server
get load-balancer virtual-server <vs_id> stats
```

### Load Balancer Status Values

| Status | Meaning |
|---|---|
| `UP` | All pool members healthy |
| `PARTIALLY_UP` | At least one member healthy |
| `DOWN` | No healthy members |
| `DISABLED` | Administratively disabled |
| `DETACHED` | Edge cluster assignment missing |

### Troubleshooting Load Balancer

```bash
# Are pool members passing health checks?
get load-balancer pools

# Member is DOWN — check:
# 1. Security group / DFW allows health check port
# 2. Application listening on expected port
# 3. Pool monitor type matches application (HTTP vs TCP)

# Check Edge CPU — LB is Edge-hosted, CPU bound under high load
get service dataplane stats
```

---

## Diagnostics

These tools help you trace packets, capture traffic, analyse logs, and diagnose BGP or tunnel issues.

### Central CLI (NSX Manager)

```bash
# Interactive CLI
nsxcli

# Or single command
nsxcli -c "get managers"
```

### Traceflow

Traceflow injects a probe packet to trace its path through the logical network:

```bash
# List active traceflows
get traceflows

# Traceflow is primarily launched from NSX Manager UI:
# Plan & Troubleshoot → Traceflow
# Or via API: POST /api/v1/traceflows
```

### Packet Capture on Edge Node

SSH to the Edge node, then:

```bash
# Capture on uplink (physical interface)
debug packet capture interface fp-eth0 count 500

# Capture on Geneve overlay interface
debug packet capture interface nsx-geneve count 500

# Capture with filter (BPF syntax)
debug packet capture interface fp-eth0 filter "host 10.0.0.1" count 200

# Write to file for Wireshark analysis
debug packet capture interface fp-eth0 file /tmp/cap.pcap count 1000
```

### Log Management

```bash
# View recent logs
get logs

# Follow logs in real time
get log manager follow

# Set log level (Edge or Manager node)
set service manager logging-level debug
set service manager logging-level info      # reset after troubleshooting

# NSX log file locations (SSH to node)
ls /var/log/vmware/nsx-*/
tail -f /var/log/vmware/nsx-manager/manager.log
tail -f /var/log/vmware/nsx-edge/edge.log
```

### Connectivity Tests

```bash
# Ping from NSX Manager node
vrf <lr_id>
ping <destination_ip>
ping <destination_ip> repeat 100 size 1400

# Traceroute through overlay
traceroute <destination_ip>

# Test DNS resolution from Edge
nslookup <hostname>
```

### BGP and Routing Diagnostics

```bash
# Check BGP session state (run on Edge in gateway VRF)
vrf <lr_id>
get bgp neighbor summary

# BGP route counts per neighbor
get bgp neighbor <neighbor_ip>

# Advertised routes to a peer
get bgp neighbor <neighbor_ip> advertised-routes

# Received routes from a peer
get bgp neighbor <neighbor_ip> routes

# Full forwarding table
get forwarding

# Check for route to a specific prefix
get route <prefix>/<mask>
```

### Health and Cluster Status

```bash
# NSX Manager cluster health
get managers
get clusters
get cluster status

# Corfu DB (control plane) status
get corfu-cluster status

# Individual service status
get service manager
get service http
get service controller

# Transport node connectivity
get transport-nodes
get transport-node-status
```

### Common Diagnostic Scenarios

| Symptom | Commands |
|---|---|
| VM can't reach gateway | `vsipioctl getrules` on source ESXi host — check DFW drop |
| BGP session down | `vrf <id>` → `get bgp neighbor summary` on Edge |
| Tunnel flapping | `get tunnel status` — check underlay MTU (needs ≥ 1600 for Geneve) |
| Segment not reachable | `get logical-switch <id> status` — check replication mode |
| High CPU on Edge | `get service dataplane stats` — check connection table |
| Manager UI unreachable | `get service http` + `get cluster status` on Manager node |

---

## IPAM, Certificates & Backup

IP pool management for TEP address allocation, certificate management for API trust, and backup configuration.

### IP Pools

```bash
get ip-pools
get ip-pool <id>
get ip-pool <id> allocations
```

### Certificates

```bash
get certificates
get certificate <id>
get trust-objects
```

### Backup & Restore

```bash
get backup status
set backup schedule daily time 02:00
backup manual
get backup history
```
