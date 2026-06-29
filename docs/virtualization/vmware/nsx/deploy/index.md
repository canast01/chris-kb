---
tags:
  - deployment
  - nsx
  - nsx-4
  - vmware
search:
  boost: 2
---
# NSX — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware NSX network virtualisation. Phases 1–2 establish prerequisites and the NSX Manager cluster; Phases 3–4 prepare transport zones, TEP profiles, and ESXi host transport nodes; Phases 5–6 deploy Edge nodes, configure T0/T1 gateways and overlay segments, then validate the full data path.

*Applies to: NSX-T 3.x / NSX 4.x*
</div>

![NSX Deploy Stages](../../../../assets/nsx-deploy-stages.svg)

![NSX Deploy Topology](../../../../assets/nsx-deploy-topology.svg)

---

```d2
direction: right

plan: "Plan" {shape: oval}
phase_1_prerequisites: "Phase 1 — Prerequisites" {shape: rectangle}
phase_2_nsx_manager_cluster: "Phase 2 — NSX Manager Cluster" {shape: rectangle}
phase_3_transport_zones_and_profiles: "Phase 3 — Transport Zones and Profiles" {shape: rectangle}
phase_4_host_transport_node_preparat: "Phase 4 — Host Transport Node Preparation" {shape: rectangle}
phase_5_edge_cluster_and_t0_gateway: "Phase 5 — Edge Cluster and T0 Gateway" {shape: rectangle}
phase_6_logical_networking_and_valid: "Phase 6 — Logical Networking and Validation" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> phase_1_prerequisites
phase_1_prerequisites -> phase_2_nsx_manager_cluster
phase_2_nsx_manager_cluster -> phase_3_transport_zones_and_profiles
phase_3_transport_zones_and_profiles -> phase_4_host_transport_node_preparat
phase_4_host_transport_node_preparat -> phase_5_edge_cluster_and_t0_gateway
phase_5_edge_cluster_and_t0_gateway -> phase_6_logical_networking_and_valid
phase_6_logical_networking_and_valid -> validate
```

## Before you begin

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: How to Deploy and Create a VMware NSX-T Management Cluster](https://www.youtube.com/watch?v=RNrzwpiR-Zs){ .md-button }
<!-- /video-link -->

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

!!! warning "DFW enforcement change"
    Deploying or reconfiguring NSX affects distributed firewall policy across all hosts. Validate in monitor mode before enforcing. A misconfigured rule can block application traffic immediately.

## Phase 1 — Prerequisites

**Exit criterion:** DNS, NTP, MTU, and vCenter connectivity confirmed on all hosts; IP allocation plan documented.

### Infrastructure Readiness

| Check | Required Value | Notes |
|---|---|---|
| DNS forward + reverse | Resolves for all 3 Manager FQDNs + VIP | Required before OVA deploy |
| NTP | Same source as vCenter, drift < 500 ms | `esxcli system ntp get` |
| MTU on ToR switches | 9000 (all ports carrying TEP traffic) | Geneve encapsulation overhead |
| vCenter version | 7.0 U2+ for NSX 4.x | Verify interop matrix |
| Host NIC firmware | On NSX HCL | Check Broadcom HCL portal |

### IP Allocation Plan

Reserve before deployment (document in runbook):

```text
NSX Manager node 1:  10.10.0.11/24   nsx-mgr01.example.local
NSX Manager node 2:  10.10.0.12/24   nsx-mgr02.example.local
NSX Manager node 3:  10.10.0.13/24   nsx-mgr03.example.local
NSX Manager VIP:     10.10.0.10/24   nsx-manager.example.local  (DNS A-record → VIP)

TEP subnet (compute): 192.168.100.0/24   pool: .10–.254
TEP subnet (edge):    192.168.101.0/24   pool: .10–.30
Edge uplink 1:        10.10.10.1/30
Edge uplink 2:        10.10.10.5/30
BGP ASN (NSX):        65100
BGP ASN (ToR):        65200
```

### MTU Verification (Pre-Deploy)

```bash
# From each ESXi host — confirm jumbo frames to the ToR before NSX install
vmkping -I vmk0 -d -s 8972 <tor-switch-ip>
# 0% loss = MTU 9000 path confirmed
# Any loss = fix switch port MTU before proceeding
```


```text title="Expected output"
PING 10.20.30.1 (10.20.30.1): 8972 data bytes
8980 bytes from 10.20.30.1: icmp_seq=0 time=2.341 ms
8980 bytes from 10.20.30.1: icmp_seq=1 time=2.156 ms
8980 bytes from 10.20.30.1: icmp_seq=2 time=2.289 ms
8980 bytes from 10.20.30.1: icmp_seq=3 time=2.401 ms
8980 bytes from 10.20.30.1: icmp_seq=4 time=2.178 ms

--- 10.20.30.1 statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 2.156/2.273/2.401 ms
```

!!! warning "Common errors"
    **`PING 10.20.30.1 (10.20.30.1): 8972 data bytes — Packet size 9000 is too large for interface`** — Verify the ESXi vmk0 interface MTU is set to 9000 with `esxcli network ip interface list`.
    **`100% packet loss`** — Confirm the ToR switch port connected to this ESXi host has MTU 9000 enabled and is not in an error-disabled state.
    **`Unknown host 10.20.30.1`** — Replace `<tor-switch-ip>` with the actual IP address of your ToR switch management interface.
---

## Phase 2 — NSX Manager Cluster

**Exit criterion:** Three NSX Manager nodes deployed, clustered, VIP configured, and vCenter registered as compute manager.

### Deploy NSX Manager Node 1

In vCenter: **Actions → Deploy OVF Template**, select the NSX Manager OVA:

```text
Deployment size: Medium (production) — 4 vCPU / 16 GB RAM / 200 GB disk
Thick Eager-Zeroed provisioning for production
Network: Management portgroup

Customise template:
  Hostname:       nsx-mgr01.example.local
  IPv4 address:   10.10.0.11
  Netmask:        255.255.255.0
  Gateway:        10.10.0.1
  DNS:            10.10.0.5, 10.10.0.6
  NTP:            ntp1.example.local, ntp2.example.local
  Admin password: <20+ char, upper+lower+special+digit>
  Audit password: <separate audit account password>
```

Repeat for nodes 2 and 3 (10.10.0.12, 10.10.0.13).

### Form the Cluster

```bash
# SSH to node 2, join to node 1
nsxcli

# Get node 1's API certificate thumbprint from node 1 first
get certificate api thumbprint
# Copy the thumbprint string

# On node 2
join management-plane 10.10.0.11 username admin thumbprint <node1-thumbprint>

# Repeat on node 3
join management-plane 10.10.0.11 username admin thumbprint <node1-thumbprint>

# Verify cluster health from any node
get cluster status
# Expected: "STABLE" with 3 members
```


```text title="Expected output"
NSX CLI (Build 21.0.1.0.0.17483745)
Type "help" for command reference.

nsx> get certificate api thumbprint
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAKp8Z7x9mK2jMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
-----END CERTIFICATE-----
Thumbprint: 8F:A4:2E:D1:9C:7B:E5:3A:F2:C1:B8:6D:9E:4A:7F:C3:2B:E8:D5:91

nsx> join management-plane 10.10.0.11 username admin thumbprint 8F:A4:2E:D1:9C:7B:E5:3A:F2:C1:B8:6D:9E:4A:7F:C3:2B:E8:D5:91
Joining management cluster... 
Node joined successfully. Cluster formation in progress.

nsx> join management-plane 10.10.0.11 username admin thumbprint 8F:A4:2E:D1:9C:7B:E5:3A:F2:C1:B8:6D:9E:4A:7F:C3:2B:E8:D5:91
Joining management cluster...
Node joined successfully. Cluster formation in progress.

nsx> get cluster status
Cluster Status: STABLE
Node Count: 3
Node 1 (10.10.0.10): UP - Role: PRIMARY
Node 2 (10.10.0.11): UP - Role: SECONDARY
Node 3 (10.10.0.12): UP - Role: SECONDARY
Last Heartbeat: 2 seconds ago
```

!!! warning "Common errors"
    **`join management-plane: Certificate thumbprint mismatch`** — Verify the thumbprint was copied correctly from node 1 and matches exactly, including colons and case.
    **`join management-plane: Connection refused to 10.10.0.11:443`** — Ensure node 1 is reachable and the NSX management service is running with `get service nsxd status`.
    **`get cluster status: Cluster not yet formed`** — Wait 30-60 seconds for cluster consensus to establish after the final node joins, then retry the command.
### Configure the Cluster VIP

```bash
# From NSX Manager UI: System → Appliances → Set Virtual IP
# Or via API:
curl -sk -u 'admin:<password>' -X PUT \
  "https://10.10.0.11/api/v1/cluster/api-virtual-ip?action=set_virtual_ip&ip_address=10.10.0.10"

# Verify VIP is reachable
ping 10.10.0.10
# UI accessible at https://nsx-manager.example.local
```


```text title="Expected output"
% Total    % Received % Xferd  Average Speed   Time    Current
                                 Dload  Upload   Speed
100   156  100   156    0     0    892      0 --:--:-- --:-- --:--:--   0
{"resource_type":"ClusterVirtualIp","ip_address":"10.10.0.10","status":"success"}

PING 10.10.0.10 (10.10.0.10) 56(84) bytes of data.
64 bytes from 10.10.0.10: icmp_seq=1 ttl=64 time=2.14 ms
64 bytes from 10.10.0.10: icmp_seq=2 ttl=64 time=1.89 ms
64 bytes from 10.10.0.10: icmp_seq=3 ttl=64 time=2.03 ms
--- 10.10.0.10 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 1.89/2.02/2.14/0.10 ms
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in example, but ensure it's included if removed).
    **`{"error_code":400,"error_message":"Invalid IP address format or IP already in use"}`** — Verify the IP address is valid, not already assigned to another node, and within the correct subnet for your NSX cluster.
    **`No route to host`** — Ensure the VIP subnet is routable from your management network and that network connectivity exists between the NSX Manager nodes and the VIP address.
### Register vCenter as Compute Manager

**System → Fabric → Compute Managers → Add**

```text
Display name:  vCenter-Prod
FQDN:          vcenter.example.local
Username:      administrator@vsphere.local
Password:      <password>
Accept SSL thumbprint when prompted
```

Status must reach `Registered` before proceeding.

### Configure SFTP Backup

**System → Backup & Restore → Configure**

```text
Protocol:    SFTP
Host:        backup-server.example.local
Port:        22
Directory:   /backups/nsx/
Username:    nsx-backup
Passphrase:  <encrypt passphrase — store in vault>
Schedule:    Daily 02:00
Retain:      14 copies
```

Test the connection before saving.

---

## Phase 3 — Transport Zones and Profiles

**Exit criterion:** Overlay and VLAN transport zones created; uplink profile and TEP IP pools configured.

### Create Transport Zones

**System → Fabric → Transport Zones → Add**

| Name | Type | Purpose |
|---|---|---|
| `tz-overlay-compute` | Overlay (Geneve) | Compute workload segments |
| `tz-vlan-edge` | VLAN | Edge node uplinks to physical routers |

### Create TEP IP Pools

**Networking → IP Management → IP Address Pools → Add**

```yaml
# Compute TEP pool
Name:    pool-tep-compute
Subnet:  192.168.100.0/24
Gateway: 192.168.100.1
Ranges:  192.168.100.10–192.168.100.254

# Edge TEP pool
Name:    pool-tep-edge
Subnet:  192.168.101.0/24
Gateway: 192.168.101.1
Ranges:  192.168.101.10–192.168.101.30
```

### Create Uplink Profile

**System → Fabric → Profiles → Uplink Profiles → Add**

```text
Name:             uplink-profile-compute
Active uplinks:   uplink-1, uplink-2
Standby uplinks:  (empty — use active/active teaming or LACP)
Transport VLAN:   <TEP VLAN ID — e.g. 100>
MTU:              9000
```

### Create Host Transport Node Profile

**System → Fabric → Profiles → Host Transport Node Profiles → Add**

```text
Name:             tn-profile-compute
vDS:              select production vDS
Transport zones:  tz-overlay-compute
Uplink profile:   uplink-profile-compute
IP pool:          pool-tep-compute
Uplink mapping:   uplink-1 → vmnic2, uplink-2 → vmnic3
```

---

## Phase 4 — Host Transport Node Preparation

**Exit criterion:** All ESXi hosts in the cluster show `Success` in the transport node config state; TEP-to-TEP pings pass between all hosts.

### Apply Transport Node Profile to Cluster

**System → Fabric → Hosts → [cluster] → Configure NSX**

```text
Select: tn-profile-compute
Apply to entire cluster
Monitor: Configuration column — each host progresses from "In Progress" → "Success"
```

### Verify Transport Nodes

```bash
# From NSX Manager CLI
nsxcli
get transport-nodes
get transport-node-status
# All hosts: state = UP

# Verify TEP IP assignment
get logical-switch port
```


```text title="Expected output"
NSX CLI (build 17.0.1.0.0.17964471)
Connected to NSX Manager 192.168.1.10

nsxcli> get transport-nodes
Transport Node ID                          Host Name              IP Address       State
tn-esx01-uuid-a1b2c3d4                     esx01.lab.local        10.0.1.51        UP
tn-esx02-uuid-e5f6g7h8                     esx02.lab.local        10.0.1.52        UP
tn-esx03-uuid-i9j0k1l2                     esx03.lab.local        10.0.1.53        UP

nsxcli> get transport-node-status
Transport Node ID                          State    TEP IP           Tunnel Status
tn-esx01-uuid-a1b2c3d4                     UP       172.16.10.101    UP
tn-esx02-uuid-e5f6g7h8                     UP       172.16.10.102    UP
tn-esx03-uuid-i9j0k1l2                     UP       172.16.10.103    UP

nsxcli> get logical-switch port
Logical Switch                             Port ID              MAC Address          TEP IP
ls-prod-web                                lsp-uuid-001         00:50:56:a1:2b:3c    172.16.10.101
ls-prod-web                                lsp-uuid-002         00:50:56:a1:4d:5e    172.16.10.102
ls-prod-db                                 lsp-uuid-003         00:50:56:a1:6f:7g    172.16.10.103
ls-mgmt                                    lsp-uuid-004         00:50:56:a1:8h:9i    172.16.10.101
```

!!! warning "Common errors"
    **`Error: Unable to connect to NSX Manager`** — Verify NSX Manager IP/hostname is reachable and nsxcli is configured with correct credentials via `set api-server` command.
    **`Transport Node State: DOWN`** — Check host connectivity to NSX Manager, verify vxlan kernel module is loaded with `vmkload_mod -l | grep vxlan`, and confirm TEP network is routable.
    **`No logical-switch port entries returned`** — Ensure logical switches have been created in NSX Manager UI and at least one VM is connected to the logical switch.
### TEP-to-TEP Connectivity Test

```bash
# SSH to each ESXi host — ping all other TEP IPs
# TEP vmkernel is typically vmk10 after NSX preparation
vmkping -I vmk10 -d -s 1500 192.168.100.11
vmkping -I vmk10 -d -s 1500 192.168.100.12
vmkping -I vmk10 -d -s 1500 192.168.100.13
# 0% loss required on all tests
# If loss: check TEP VLAN tagging on uplink profile and switch trunk config
```


```text title="Expected output"
PING 192.168.100.11 (192.168.100.11): 56 data bytes
64 bytes from 192.168.100.11: icmp_seq=0. time=2.341 ms
64 bytes from 192.168.100.11: icmp_seq=1. time=2.156 ms
64 bytes from 192.168.100.11: icmp_seq=2. time=2.289 ms
64 bytes from 192.168.100.11: icmp_seq=3. time=2.401 ms
64 bytes from 192.168.100.11: icmp_seq=4. time=2.178 ms
--- 192.168.100.11 statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max/stddev = 2.156/2.273/2.401/0.099 ms

PING 192.168.100.12 (192.168.100.12): 56 data bytes
64 bytes from 192.168.100.12: icmp_seq=0. time=1.987 ms
64 bytes from 192.168.100.12: icmp_seq=1. time=2.045 ms
64 bytes from 192.168.100.12: icmp_seq=2. time=2.134 ms
64 bytes from 192.168.100.12: icmp_seq=3. time=2.089 ms
64 bytes from 192.168.100.12: icmp_seq=4. time=2.156 ms
--- 192.168.100.12 statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max/stddev = 1.987/2.082/2.156/0.061 ms

PING 192.168.100.13 (192.168.100.13): 56 data bytes
64 bytes from 192.168.100.13: icmp_seq=0. time=2.412 ms
64 bytes from 192.168.100.13: icmp_seq=1. time=2.267 ms
64 bytes from 192.168.100.13: icmp_seq=2. time=2.501 ms
64 bytes from 192.168.100.13: icmp_seq=3. time=2.334 ms
64 bytes from 192.168.100.13: icmp_seq=4. time=2.289 ms
--- 192.168.100.13 statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max/stddev = 2.267/2.361/2.501/0.089 ms
```

!!! warning "Common errors"
    **`PING 192.168.100.11 (192.168.100.11): 56 data bytes — No response from host`** — Verify the TEP VLAN is tagged on the physical switch uplink port and that the vmk10 interface is assigned to the correct VLAN ID in the NSX uplink profile.
    **`Unable to locate vmkernel interface vmk10`** — Confirm NSX Host Preparation has completed successfully on the ESXi host by
---

## Phase 5 — Edge Cluster and T0 Gateway

**Exit criterion:** Edge cluster deployed, T0 BGP sessions established with ToR switches, routes advertised.

### Deploy Edge Transport Nodes

Deploy Edge VMs via **System → Fabric → Edge Transport Nodes → Add**:

```text
Name:           edge-node-01
Form factor:    Large (8 vCPU / 32 GB — production)
Host:           dedicated-edge-esxi-host-01  (NOT on compute hosts)
Management IP:  10.10.0.21/24
DNS:            10.10.0.5
NTP:            ntp1.example.local

Transport configuration:
  Overlay TZ:  tz-overlay-compute
  VLAN TZ:     tz-vlan-edge
  Uplink profile: uplink-profile-edge
  TEP pool:    pool-tep-edge
  fp-eth0 → edge-uplink portgroup 1 (ToR VLAN)
  fp-eth1 → edge-uplink portgroup 2 (ToR VLAN — second path)
```

Repeat for edge-node-02 on a different host.

```bash
# Verify Edge transport node status
nsxcli
get transport-nodes | grep edge
# Both Edge nodes: state = UP
```


```text title="Expected output"
NSX CLI (Build 20.0.3.1)
Connected to: nsx-manager-01.lab.local (192.168.1.50)

transport-node-0 (edge-01.lab.local):
  state: UP
  status: READY
  host-switch-mode: VDS
  
transport-node-1 (edge-02.lab.local):
  state: UP
  status: READY
  host-switch-mode: VDS

2 edge transport nodes found, all UP
```

!!! warning "Common errors"
    **`nsxcli: command not found`** — Ensure NSX CLI is installed and the PATH includes the NSX installation directory, or run with the full path `/opt/vmware/nsx-cli/bin/nsxcli`.
    **`Connection refused: Unable to connect to nsx-manager-01.lab.local:443`** — Verify the NSX Manager is reachable and running, and check network connectivity with `ping` and `curl -k https://<nsx-manager-ip>`.
    **`transport-node-0: state = DOWN`** — Check the Edge VM's vNIC connectivity, verify host-switch configuration, and review NSX Manager logs for transport node registration failures.
### Create Edge Cluster

**System → Fabric → Edge Clusters → Add**

```text
Name:          edge-cluster-prod
Edge nodes:    edge-node-01, edge-node-02
BFD:           enabled (fast failure detection, 300 ms)
```

### Create T0 Gateway

**Networking → Tier-0 Gateways → Add**

```text
Name:          T0-Prod
HA Mode:       Active/Standby
Edge cluster:  edge-cluster-prod

Interfaces → Add:
  Type:         External
  Name:         T0-uplink-edge01
  IP:           10.10.10.2/30
  Connected to: edge-node-01 / fp-eth0 (VLAN-backed segment)

  Type:         External
  Name:         T0-uplink-edge02
  IP:           10.10.10.6/30
  Connected to: edge-node-02 / fp-eth0
```

### Configure BGP on T0

```text
Networking → T0-Prod → Routing → BGP
  Local AS:     65100
  Graceful restart: Enabled

BGP Neighbor 1:
  Neighbor IP:  10.10.10.1   (ToR 1)
  Remote AS:    65200
  BFD:          Enabled

BGP Neighbor 2:
  Neighbor IP:  10.10.10.5   (ToR 2)
  Remote AS:    65200
  BFD:          Enabled
```

```bash
# Verify BGP from Edge node CLI
get bgp neighbor summary
# Both neighbors: State = Established

# Verify routes received from physical fabric
get route
# Physical fabric prefixes should appear in routing table
```


```text title="Expected output"
NSX-Edge> get bgp neighbor summary
Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
10.100.1.1      4 65000    1247    1251        0    0    0 5d12h23m Established
10.100.1.2      4 65000    1248    1252        0    0    0 5d12h22m Established

NSX-Edge> get route
Codes: K - kernel, C - connected, S - static, R - RIP, B - BGP
       O - OSPF, IA - OSPF inter area, E1 - OSPF external type 1
       E2 - OSPF external type 2, i - IS-IS, L1 - IS-IS level-1
       L2 - IS-IS level-2, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       + - replicated route, % - next hop override

B   10.50.0.0/16 [200/0] via 10.100.1.1, 0d02h14m
B   10.51.0.0/16 [200/0] via 10.100.1.2, 0d02h14m
B   172.16.0.0/12 [200/0] via 10.100.1.1, 0d02h14m
C   192.168.1.0/24 is directly connected, eth0
S   0.0.0.0/0 [1/0] via 10.100.1.1, 0d05h22m
```

!!! warning "Common errors"
    **`% Unknown command`** — Verify the exact command syntax for your NSX version; use `?` to list available commands.
    **`BGP neighbor 10.100.1.1 not established (State = Idle)`** — Check physical network connectivity between Edge and BGP peer, verify AS numbers match, and confirm firewall allows BGP port 179.
---

## Phase 6 — Logical Networking and Validation

**Exit criterion:** T1 gateway, overlay segment, and DFW baseline policy in place; east-west and north-south traffic tested.

### Create T1 Gateway

**Networking → Tier-1 Gateways → Add**

```text
Name:          T1-Tenant-01
Linked T0:     T0-Prod
Edge cluster:  edge-cluster-prod  (required for stateful services: NAT, LB)

Route advertisement:
  Connected segments: Enabled
  Static routes:      Enabled (if applicable)
```

### Create Overlay Segment

**Networking → Segments → Add**

```text
Name:          seg-web-tier
Transport zone: tz-overlay-compute
Connected gateway: T1-Tenant-01 / routed
Subnets:       192.168.50.1/24
```

Attach test VMs to `seg-web-tier` and verify:

```bash
# From a VM on seg-web-tier — verify gateway reachability
ping 192.168.50.1

# From NSX Manager — check segment VNI assignment
nsxcli
get logical-switch seg-web-tier | grep VNI
```


```text title="Expected output"
PING 192.168.50.1 (192.168.50.1) 56(84) bytes of data.
64 bytes from 192.168.50.1: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 192.168.50.1: icmp_seq=2 ttl=64 time=1.89 ms
64 bytes from 192.168.50.1: icmp_seq=3 ttl=64 time=2.12 ms
^C
--- 192.168.50.1 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/stddev = 1.89/2.11/2.34/0.19 ms

nsxcli> get logical-switch seg-web-tier | grep VNI
VNI: 5001
```

!!! warning "Common errors"
    **`PING: sendto: No route to host`** — Verify the NSX edge node has a route to the gateway IP and that the logical router is properly configured on the segment.
    **`nsxcli: command not found`** — SSH directly to the NSX Manager appliance (not a managed host) and ensure you have admin credentials to access the CLI.
    **`No logical switch named 'seg-web-tier' found`** — Confirm the segment name matches exactly in NSX Manager; use `get logical-switches` to list all available segments.
### DFW Baseline Policy

**Security → Distributed Firewall → Add Policy**

```text
Category:  Infrastructure
Policy name: Allow-Management

Rules:
  1. Allow SSH from mgmt subnet (10.10.0.0/24) → ANY, port 22
  2. Allow monitoring from monitoring subnet → ANY, ICMP + ports 161, 9100
  3. Allow backup traffic → backup subnet, port 22
  4. Deny ALL (default rule 65535 — do not modify, remains DROP)
```

```bash
# Verify DFW rules pushed to hosts
# SSH to any ESXi host
summarize-dvfilter
# Each VM vNIC should have a vmware-sfw filter listed

vsipioctl getrules -f <filter-name>
# Infrastructure allow rules should appear
```


```text title="Expected output"
Filter Summary
==============
VM Name                    vNIC  Filter Name                    Status
web-prod-01                eth0  dvfilter-generic-fw-0          ACTIVE
web-prod-01                eth1  dvfilter-generic-fw-1          ACTIVE
db-backup-02               eth0  dvfilter-generic-fw-0          ACTIVE
app-cache-03               eth0  dvfilter-generic-fw-0          ACTIVE
app-cache-03               eth1  dvfilter-generic-fw-1          ACTIVE
...
Total VMs with filters: 47

Rules for dvfilter-generic-fw-0:
==================================
Rule ID  Direction  Protocol  Source         Destination    Port   Action
1001     INBOUND    TCP       10.20.0.0/16   10.30.0.0/16   443    ALLOW
1002     INBOUND    TCP       10.20.0.0/16   10.30.0.0/16   8443   ALLOW
1003     INBOUND    TCP       ANY            10.30.50.0/24  22     DENY
1004     OUTBOUND   TCP       10.30.0.0/16   8.8.8.8        53     ALLOW
1005     OUTBOUND   TCP       10.30.0.0/16   ANY            443    ALLOW
```

!!! warning "Common errors"
    **`summarize-dvfilter: command not found`** — Run the command from the ESXi host shell (SSH directly to the host, not vCenter), or verify the NSX agent is installed with `esxcli software vib list | grep nsx`.
    **`vsipioctl: command not found`** — Ensure you are running this command on an ESXi host where NSX is installed; this tool is not available on vCenter or management workstations.
    **`Error: Filter '<filter-name>' not found in kernel`** — Verify the filter name is correct by running `summarize-dvfilter` first to list active filters, then use the exact filter name from the output.
### End-to-End Validation

```bash
# East-West: VM on seg-web-tier pings VM on a second segment via T1
ping <vm2-ip>

# North-South: VM reaches external IP via T0 BGP path
ping 8.8.8.8

# NSX Manager route table
nsxcli
get route
# Default route via T0 uplinks should be present

# BGP summary from both Edge nodes
get bgp neighbor summary
# All peers: Established, Prefixes Received > 0
```


```text title="Expected output"
PING 192.168.20.15 (192.168.20.15) 56(84) bytes of data.
64 bytes from 192.168.20.15: icmp_seq=1 ttl=64 time=2.341 ms
64 bytes from 192.168.20.15: icmp_seq=2 ttl=64 time=1.987 ms
64 bytes from 192.168.20.15: icmp_seq=3 ttl=64 time=2.156 ms
--- 192.168.20.15 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/stddev = 1.987/2.161/2.341/0.149 ms

PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=18.742 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=118 time=19.156 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=118 time=18.923 ms
--- 8.8.8.8 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 3004ms
rtt min/avg/max/stddev = 18.742/18.940/19.156/0.187 ms

NSX Manager CLI
nsx> get route
Flags: [U]p, [G]ateway, [R]ejected, [B]lackhole, [D]ynamic, [A]cive
Destination        Gateway          Flags  Metric  Interface
0.0.0.0/0          10.100.1.1       UG     0       eth0
10.0.0.0/8         0.0.0.0          U      0       eth1
192.168.0.0/16     0.0.0.0          U      0       eth2
169.254.0.0/16     0.0.0.0          U      256     eth0

nsx> get bgp neighbor summary
BGP router identifier 10.50.0.1, local AS number 65001
Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
10.100.1.1      4 65000    1247    1251        0    0    0 2d14h23m Established/847
10.100.1.2      4 65000    1248    1250        0    0    0 2d14h22m Established/851
---OUTPUT---
```

!!! warning "Common errors"
    **`ping: sendmsg: Operation not permitted`** — Verify the VM has network connectivity to the segment and check NSX firewall rules are not blocking ICMP traffic.
    **`get bgp neighbor summary: command not found`** — Ensure you are in the NSX Edge CLI context (not NSX Manager); SSH directly to the Edge node IP and retry.
    **`0.0.0.0/0 route missing
### Post-Deployment Checklist

| Check | Command / Location | Pass Criterion |
|---|---|---|
| NSX Manager cluster | `get cluster status` | STABLE — 3 members |
| vCenter compute manager | System → Fabric → Compute Managers | Status: Registered |
| All transport nodes UP | `get transport-node-status` | All hosts: UP |
| TEP connectivity | `vmkping -I vmk10 -d -s 1500 <peer-TEP>` | 0% loss |
| Edge cluster health | `get edge-cluster status` | Active/Standby confirmed |
| BGP sessions | `get bgp neighbor summary` (Edge CLI) | All peers: Established |
| T0 route table | `get route` (Edge CLI) | Default + fabric routes present |
| T1 route advertisement | Networking → T1 → Route Advertisement | Connected segments: Enabled |
| Overlay segment | VM ping to T1 gateway IP | Reachable |
| DFW rule push | `summarize-dvfilter` (ESXi host) | vmware-sfw filter on all vNICs |
| NSX backup | System → Backup & Restore | Last backup: successful |

---

## See also

- [NSX — How It Works](../architecture/how-it-works/)
- [NSX — Health Checks](../operations/health-checks/)
- [NSX — Common Issues](../troubleshooting/common-issues/)

## Verify

- **Manager cluster:** NSX UI → System → Overview — all nodes Active, cluster Stable
- **Transport nodes:** Fabric → Nodes → Host Transport Nodes — all nodes Configured/Success
- **Edge cluster:** Fabric → Nodes → Edge Transport Nodes — all edges Up
- **Connectivity test:** NSX UI → Tools → Traceflow — send a packet between two VMs on different segments
