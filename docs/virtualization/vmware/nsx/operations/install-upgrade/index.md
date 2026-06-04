# NSX — Install and Upgrade

```bash
# SSH to node 2
nsxcli

# Join to the cluster (provide node 1's IP and certificate thumbprint)
join management-plane <node1-ip> username admin thumbprint <node1-thumbprint>

# Get node 1's thumbprint from node 1 CLI:
get certificate api thumbprint
```text
┌────────────────────────────────────── NSX — Install and Upgrade ──────────────────────────────────────┐
│                                                                                                       │
│  NSX Manager OVA deployment, transport node prep, and in-place upgrade flow.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Fresh Deployment               │  │              Upgrade Procedure              │   │
│   │            Deploy Manager OVA x3             │  │           Download upgrade bundle           │   │
│   │          Form cluster (join nodes)           │  │            Upload to NSX Manager            │   │
│   │           Register compute manager           │  │           Run pre-check validation          │   │
│   │         Deploy edge transport nodes          │  │           Upgrade MP → CCP → hosts          │   │
│   │          Prepare ESXi hosts (N-VDS)          │  │         Verify each tier before next        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Deploy manager cluster → compute manager → edges → ESXi transport nodes.                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Prerequisites                 │  │            Version Compatibility            │   │
│   │           vCenter registered first           │  │             NSX 4.x — current GA            │   │
│   │          IP pool for TEP addresses           │  │            vCenter 7.0+ required            │   │
│   │         Uplink/overlay profiles set          │  │            ESXi 7.0+ for N-VDS 2            │   │
│   │           MTU 1600+ on fabric NICs           │  │             Interop matrix check            │   │
│   │         BGP ASN planned with NetEng          │  │            VCF: use SDDC Mgr LCM            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ESXi hosts, vCenter, physical ToR with BGP, SFTP server, management network                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OVA         = Open Virtualisation Appliance; NSX Manager deploy format                               │
│  Compute Mgr = vCenter registered in NSX; source of host inventory                                    │
│  Transport node = ESXi or Edge with N-VDS installed for overlay                                       │
│  N-VDS       = NSX managed vSwitch replacing dvSwitch on host                                         │
│  TEP         = Tunnel Endpoint; source IP for GENEVE overlay traffic                                  │
│  Uplink profile= defines LAG, teaming, VLAN for TEP traffic                                           │
│  IP pool     = range of IPs assigned to TEPs during host prep                                         │
│  MP          = Management Plane; upgraded first in NSX upgrade sequence                               │
│  CCP         = Central Control Plane; upgraded second after MP                                        │
│  SDDC Mgr    = VCF lifecycle mgr; handles NSX upgrades in VCF context                                 │
│  Pre-check   = NSX upgrade validator; runs before bundle apply                                        │
│  Interop     = VMware Product Interoperability Matrix for version support                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```yaml
Name: pool-tep-compute
Subnet: 192.168.200.0/24
Gateway: 192.168.200.1
IP Ranges: 192.168.200.10–192.168.200.254
```
```bash
# Verify from Manager CLI after preparation
nsxcli
get transport-nodes
get transport-node-status
# All hosts should show "UP"
```
```text
1. NSX Manager (all 3 nodes) — control plane first
2. Edge Nodes — north-south gateway impact; BGP reconverges
3. ESXi Transport Nodes (host-by-host) — data plane impact; rolling
```
```text
Upgrade node 1 → node 1 reboots (cluster VIP on node 2 or 3)
Upgrade node 2 → node 2 reboots
Upgrade node 3 → node 3 reboots
```
```bash
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/upgrade/status-summary"
```
```bash
# On Edge node CLI
get version
get bgp neighbor summary
# All peers should be Established
```
```bash
# Verify backup is restorable before the upgrade window
# Check backup files are present on SFTP server
# Confirm the passphrase is stored and accessible
```
```bash
# NSX Manager cluster health
nsxcli
get cluster status
get managers
get services

# Transport node health
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/transport-nodes/status"
# Check: up_count equals total_count

# Edge cluster health and BGP
# SSH to each Edge node
get version                    # Confirm new version
get bgp neighbor summary        # All peers Established
get edge-cluster status         # Active/Standby state confirmed

# Open alarms
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=CRITICAL"
# Should return result_count: 0

# DFW rule push
# Verify a test VM can still communicate as expected after upgrade
```
