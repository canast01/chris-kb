# vSphere Replication — Integrations


<div class="kb-summary">
Integrations reference covering vCenter Integration, SRM Integration, Network Requirements, Cross-vCenter Replication, Multi-Target Replication (Fan-Out) and 1 more sections.
</div>

## vCenter Integration

The VRA registers itself as a vCenter extension (plugin) during initial setup. This registration installs the vSphere Replication plugin in the vCenter UI (Site Recovery section) and grants the VRA API access to vCenter objects (VMs, datastores, hosts, clusters).

Both the source-site VRA and the target-site VRA must register with their respective vCenter instances. After registration, the two VRAs are paired via TCP 44046 to establish the management channel between sites.

### Registration Architecture

```text
Source Site                          Target Site
-----------                          -----------
Source vCenter ◄──── VRA-src         Target vCenter ◄──── VRA-tgt
  (plugin installed)   (registered)    (plugin installed)   (registered)
                          |                                      |
                          └──────── TCP 44046 ────────────────────┘
                                (VRA pairing / management)
```

Replication configuration is stored in the vCenter database on the source side. The target vCenter holds the target-side registration and manages target datastore access.

### vCenter Extension Details

- Extension key: `com.vmware.vcHms` (HMS extension) and `com.vmware.vcDr` (VRMS/Site Recovery extension)
- Both extensions are installed on the vCenter where VRA registers
- The Site Recovery UI in vCenter (`Menu → Site Recovery`) is the primary management interface for VR
- VR does not require vCenter Enhanced Linked Mode — cross-vCenter replication works with any pairing

```bash
# Verify VRA extension registration via vCenter API
curl -k -u administrator@vsphere.local:<pass> \
  https://<vCenter-FQDN>/sdk/vimService \
  -H "Content-Type: text/xml" \
  --data '<Envelope>...' | grep -i 'HmsMain\|vcDr'

# Check extension registration from VRA side
curl -k -u admin:<pass> \
  https://<VRA-FQDN>:8043/api/config/site \
  | python3 -m json.tool
```

---

## SRM Integration

Site Recovery Manager uses vSphere Replication as its replication provider for VM-level (non-array-based) protection. The integration is configured from the SRM side after VR appliances are deployed and paired.

### Integration Model

1. Deploy and pair VR appliances (described in install/upgrade page)
2. Configure per-VM replication via VR UI (source → target site, datastore, RPO)
3. In SRM: create a Protection Group using "vSphere Replication" type
4. Add replicated VMs to the SRM Protection Group
5. Create or update SRM Recovery Plan to include this Protection Group
6. Recovery Plan handles failover sequence, IP customization, VM boot order

SRM communicates with VR exclusively via the VRA REST API on port 8043. SRM does not interact with ESXi hbrsvc directly.

### SRM Protection Group Requirements

- All VMs in the group must be actively replicating (green status in VR)
- VMs must be in the same source vCenter and target vCenter as the site pair
- VMs cannot be in both an array-based protection group and a VR protection group simultaneously
- SRM service account needs "vSphere Replication → Manage Replication" privilege on all VMs

### Recovery Flow (SRM-Orchestrated)

```text
SRM triggers recovery plan
         |
SRM calls VR API: promote recovery point for each VM
         |
VRA promotes replica VMDK at target site
  (unmounts snapshot chain, makes disk R/W)
         |
SRM registers promoted VM in target vCenter
         |
SRM applies IP customization (if configured)
         |
SRM powers on VM according to boot order/dependencies
         |
SRM monitors VM startup (heartbeat/VMware Tools)
```

---

## Network Requirements

### Firewall Rules Summary

| Source | Destination | Port | Protocol | Purpose |
|---|---|---|---|---|
| Source ESXi hosts | Target VRA IP | 31031 | TCP | Replication data |
| Source VRA | Target VRA | 44046 | TCP | VRA management/pairing |
| Target VRA | Target VRA | 44046 | TCP | VRA self (loopback not needed — between VRAs) |
| VRA (both) | vCenter (both) | 443 | HTTPS | vCenter API / registration |
| vCenter (both) | VRA (both) | 8043 | HTTPS | Site Recovery plugin → VRA API |
| Admin workstation | VRA | 5480 | HTTPS | VAMI management UI |
| Admin workstation | VRA | 22 | TCP | SSH CLI access |
| Source ESXi hosts | Target VRS (if deployed) | 31031 | TCP | Replication data to scale-out server |

### DNS Requirements

All VRA FQDNs must resolve from both sites:
- Source VRA FQDN resolves at both source and target
- Target VRA FQDN resolves at both source and target
- VRS FQDNs resolve at both sites if deployed

Replication traffic uses the IP address configured on the VRA network interface — ensure the FQDN resolves to the correct replication-path IP if VRA has multiple NICs.

### Network Design Recommendations

```text
Site A                                 Site B
------                                 ------
Management Network (VLAN 10)           Management Network (VLAN 10)
  └─ vCenter-A                           └─ vCenter-B
  └─ VRA-A mgmt NIC                      └─ VRA-B mgmt NIC

Replication Network (VLAN 20)          Replication Network (VLAN 20)
  └─ ESXi vmk (replication vmk)          └─ VRA-B replication NIC
  └─ VRA-A replication NIC (opt.)

WAN/DCI Link
  └─ VLAN 20 extended or routed
     between sites
```

If VRA has only one NIC, all traffic (management, data, VAMI) shares that interface. Dual-NIC VRA deployment allows separation of management (443/8043/5480) from replication data (31031/44046).

---

## Cross-vCenter Replication

vSphere Replication supports replication between VMs managed by different vCenter instances, including vCenters in different SSO domains. This is the standard configuration for physical DR sites with independent management stacks.

### Requirements

- Both vCenters must be running a compatible version (see version compatibility table in install/upgrade page)
- Both VRAs must be deployed and registered with their respective vCenter
- VRAs must be paired (TCP 44046 connectivity between VRA-A and VRA-B)
- DNS resolution of both VRA FQDNs from both sites
- vCenter SSO domains do not need to be linked (cross-vCenter Enhanced Linked Mode is NOT required for VR)

### Cross-vCenter Replication Gotcha

When vCenter instances are in different SSO domains, the vSphere Replication UI at the source site shows the target site datastores, but the user must authenticate to the target vCenter separately during site pairing. After pairing is complete, the source-site UI manages replication transparently.

---

## Multi-Target Replication (Fan-Out)

A single VM can be replicated to multiple target sites simultaneously. Each replication is configured independently and has its own RPO, target datastore, and recovery point instance count.

### Fan-Out Behavior

- Source ESXi hbrsvc maintains separate TCP 31031 connections for each target VRA
- Changed blocks are read once from the source datastore and sent to each target independently
- Each target site has independent recovery point instances — no shared state
- RPO compliance is tracked per-target independently
- Bandwidth requirement is multiplied by the number of targets

```text
Source VM
    |
    ├──[TCP 31031]──► VRA at DR Site A (RPO 15 min, 3 instances)
    |
    └──[TCP 31031]──► VRA at DR Site B (RPO 1 hour, 5 instances)
```

Maximum fan-out targets: 3 (VMware supported limit for VR fan-out)

---

## Storage Compatibility

vSphere Replication is storage-agnostic at both source and target. The source and target datastores can be of different types.

### Supported Source Datastore Types

| Type | Supported | Notes |
|---|---|---|
| VMFS (5, 6, 8) | Yes | All block storage backends (FC, iSCSI, local) |
| NFS (3, 4.1) | Yes | Standard NFS datastores |
| vSAN | Yes | ESA and OSA |
| VVols | Yes | Requires VVol-compatible VASA provider |
| RDM (physical mode) | No | Raw Device Mappings in physical compatibility mode are not replicable |
| RDM (virtual mode) | Yes | Virtual mode RDMs are treated as VMDKs |

### Source/Target Datastore Pairing Examples

| Source | Target | Supported |
|---|---|---|
| vSAN | NFS | Yes |
| VMFS (FC) | vSAN | Yes |
| NFS | VMFS (iSCSI) | Yes |
| vSAN | vSAN | Yes |
| VVols | VMFS | Yes |
| Physical RDM | Any | No |

Target datastore must be accessible (mounted) on at least one ESXi host in the target cluster. vSphere Replication does not require the target datastore type to match the source — this is a key advantage over array-based replication.

### vSAN-Specific Notes

When replicating to vSAN at the target site, storage policies are NOT transferred with the replication. The replica VM at the target site uses the default vSAN storage policy (or the policy assigned at replication configuration time). After failover, review and apply the appropriate vSAN policy to the recovered VM.

When replicating FROM vSAN (source), replication works normally — the hbr module tracks writes at the virtual disk level, independent of the vSAN distributed storage layer.
