# NSX — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering Version Support Matrix, Initial NSX Manager Deployment, Prepare ESXi Hosts as Transport Nodes, NSX Manager Upgrade, Rollback Considerations and 1 more sections.
</div>

## Version Support Matrix

| NSX-T Version | ESXi Minimum | vCenter Minimum | General Support End |
|---|---|---|---|
| NSX 4.2.x | ESXi 7.0 U3 | vCenter 7.0 U3 | ~2027 |
| NSX 4.1.x | ESXi 7.0 U2 | vCenter 7.0 U2 | ~2026 |
| NSX 4.0.x | ESXi 7.0 U1 | vCenter 7.0 | Ended |
| NSX 3.2.x | ESXi 7.0 | vCenter 7.0 | 2026-05 |
| NSX 3.1.x | ESXi 6.7 U3 | vCenter 6.7 U3 | Ended |

Check the [VMware Product Lifecycle](https://support.broadcom.com/group/ecx/productlifecycle) and [Interoperability Matrix](https://interopmatrix.broadcom.com) before every upgrade.

---

## Initial NSX Manager Deployment

### Pre-Deployment Requirements

- [ ] vCenter registered and accessible
- [ ] DNS forward/reverse records created for all three NSX Manager nodes and the VIP
- [ ] NTP servers configured and reachable
- [ ] Three static IPs available in the management network (one per node) plus one VIP
- [ ] Deployment size determined (see sizing table in Components page)
- [ ] SFTP/SCP server available for backup configuration

### OVA Deployment

Deploy via vCenter UI: **Actions → Deploy OVF Template**

1. Select the NSX Manager OVA from the downloaded bundle
2. Configure compute resources: target cluster, host placement (avoid same host for all three)
3. Set disk provisioning to **Thin** for lab; **Thick Eager-Zeroed** for production
4. Configure networking:
   - Network 0 → Management portgroup
5. Customise template:
   - Hostname, IPv4 address, netmask, gateway
   - DNS server(s)
   - NTP server(s)
   - Admin password (20+ characters, meets complexity)
   - Audit password
   - Root password

Repeat for nodes 2 and 3. The first node deployed becomes the primary.

### Form the NSX Manager Cluster

After deploying all three nodes, join nodes 2 and 3 to the cluster:

```bash
# SSH to node 2
nsxcli

# Join to the cluster (provide node 1's IP and certificate thumbprint)
join management-plane <node1-ip> username admin thumbprint <node1-thumbprint>

# Get node 1's thumbprint from node 1 CLI:
get certificate api thumbprint
```
```
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

DNS for the NSX Manager FQDN (e.g., `nsx-manager.example.local`) must point to this VIP.

### Register vCenter Compute Manager

**System → Fabric → Compute Managers → Add**

Provide vCenter FQDN, username, and password. Verify the SSL thumbprint when prompted. Status should show `Registered` within a few minutes.

### Configure Backup

**System → Backup & Restore → Configure**

| Field | Recommended Value |
|---|---|
| Protocol | SFTP |
| Host | backup-server.example.local |
| Port | 22 |
| Directory | /backups/nsx/ |
| Username | nsx-backup |
| Passphrase | Unique encryption passphrase (store securely) |
| Schedule | Daily at 02:00 |
| Retain | 14 backup copies |

Test the connection before saving. The passphrase encrypts the backup bundle — losing it means the backup is unrestorable.

---

## Prepare ESXi Hosts as Transport Nodes

### Create Transport Zones

**System → Fabric → Transport Zones → Add**

| Name | Type | N-VDS or vDS |
|---|---|---|
| tz-overlay-compute | Overlay | Select target vDS |
| tz-vlan-edge | VLAN | Select edge vDS |

### Create TEP IP Pool

**Networking → IP Management → IP Address Pools → Add**

Configure one pool per subnet:

```yaml
Name: pool-tep-compute
Subnet: 192.168.200.0/24
Gateway: 192.168.200.1
IP Ranges: 192.168.200.10–192.168.200.254
```

### Create Host Transport Node Profile

**System → Fabric → Profiles → Host Transport Node Profiles → Add**

The profile captures:
- Which vDS to use for NSX
- Which uplinks carry TEP traffic
- Which Transport Zones to include
- Which IP pool to use for TEP allocation

### Apply Profile to vSphere Cluster

**System → Fabric → Hosts → Configure NSX**

Select the vCenter cluster and attach the Transport Node Profile. NSX prepares all hosts in the cluster. Monitor progress in the **Configuration** column — each host transitions through `In Progress` → `Success`.

```bash
# Verify from Manager CLI after preparation
nsxcli
get transport-nodes
get transport-node-status
# All hosts should show "UP"
```

---

## NSX Manager Upgrade

### Pre-Upgrade Checklist

- [ ] NSX backup completed and verified on SFTP server (take a manual backup before starting)
- [ ] vCenter and ESXi version compatibility confirmed for target NSX version
- [ ] HCL checked for Edge node hardware (bare metal Edge only)
- [ ] All transport nodes in UP state: `GET /api/v1/transport-nodes/status`
- [ ] No open CRITICAL alarms: `GET /api/v1/alarms?status=OPEN&severity=CRITICAL`
- [ ] All BGP sessions established on all T0 gateways
- [ ] Change window approved; networking team notified (BGP reconvergence during Edge upgrade)
- [ ] Rollback plan documented (restore from backup to prior version)

### Download and Upload the Bundle

1. Download the NSX upgrade bundle (`.mub` file) from Broadcom Support Portal
2. Upload via NSX Manager UI: **System → Upgrade → Upload Bundle**
3. Wait for upload and pre-check validation to complete

### Upgrade Order (Critical)

NSX components must be upgraded in this sequence:

```text
1. NSX Manager (all 3 nodes) — control plane first
2. Edge Nodes — north-south gateway impact; BGP reconverges
3. ESXi Transport Nodes (host-by-host) — data plane impact; rolling
```

**Never upgrade Edge nodes before NSX Manager.** The upgrade coordinator in the UI enforces this order.

### Upgrading NSX Manager Nodes

The upgrade coordinator upgrades one Manager node at a time. The cluster VIP migrates to an available node during each node's upgrade:

```text
Upgrade node 1 → node 1 reboots (cluster VIP on node 2 or 3)
Upgrade node 2 → node 2 reboots
Upgrade node 3 → node 3 reboots
```

Monitor via UI **System → Upgrade → Upgrade Coordinator** or via API:

```bash
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/upgrade/status-summary"
```

### Upgrading Edge Nodes

Edge node upgrade causes BGP reconvergence. For ACTIVE_STANDBY T0 gateways:

1. Standby Edge upgrades first and reboots
2. Active Edge upgrades — T0 failover to (now upgraded) Standby
3. Both Edges return to service
4. BGP reconverges (typically < 30 seconds with BFD)

Verify after Edge upgrade:

```bash
# On Edge node CLI
get version
get bgp neighbor summary
# All peers should be Established
```

### Upgrading ESXi Transport Nodes

ESXi transport node upgrade applies NSX VIB updates to each host. The host does not need to reboot for VIB updates in most patch releases, but major version upgrades require a reboot.

The upgrade coordinator uses vCenter to put each host into maintenance mode, apply the update, and exit maintenance mode. DRS must be enabled to allow automatic VM migration.

Monitor per-host progress in the upgrade coordinator. Do not manually put hosts in maintenance mode during NSX-managed upgrade.

---

## Rollback Considerations

NSX does not support in-place version downgrade. If a post-upgrade issue requires rollback:

1. Stop the upgrade if still in progress (Edge or host phase)
2. Restore NSX Manager from the pre-upgrade backup
3. The restored NSX Manager controls the pre-upgrade state
4. Edge and host VIBs may need manual rollback — contact VMware Support

Backup restore procedure: **System → Backup & Restore → Restore** — the restore wipes the current NSX Manager cluster and replaces it with the backup state.

```bash
# Verify backup is restorable before the upgrade window
# Check backup files are present on SFTP server
# Confirm the passphrase is stored and accessible
```

---

## Post-Upgrade Validation

Run these checks after each upgrade phase completes:

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
