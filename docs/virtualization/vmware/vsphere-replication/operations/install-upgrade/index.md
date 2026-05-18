# vSphere Replication — Install and Upgrade

```
  VR Deployment and Upgrade Workflow
┌──────────────────────────────────────────────────────────────┐
│  Deploy VRA OVA ──► Register with vCenter ──► Pair sites    │
│  (both sites)        (VAMI port 5480)         (accept certs) │
│       │                                            │         │
│       ▼                                            ▼         │
│  ┌─────────────────────┐              ┌────────────────────┐  │
│  │ Configure per-VM    │              │ Add VRS if >500    │  │
│  │ replication:        │              │ VMs (same OVA,     │  │
│  │  RPO, target DS,    │              │ deploy as VRS)     │  │
│  │  quiesce, encrypt   │              └────────────────────┘  │
│  └─────────────────────┘                                     │
│                                                              │
│  Upgrade: redeploy from new OVA with same IP                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Snapshot ──► redeploy ──► re-register ──► verify     │    │
│  │ Replications resume from last sync — no data loss    │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

| Requirement | Detail |
|---|---|
| vCenter | Supported version (check interopmatrix.vmware.com) |
| DNS | FQDN for VRA resolvable from both sites |
| Network | TCP 31031 (source ESXi → target VRA), TCP 44046 (VRA-to-VRA), TCP 443 (VRA → vCenter) |
| NTP | VRA and vCenter time synchronized (±5 seconds) |
| Storage | Sufficient datastore space at target site for replica VMDKs |
| License | vSphere Replication included with vSphere Essentials Plus and higher |

---

## VRA OVA Deployment

Deploy a VRA at each site (protected site and recovery site):

```
vCenter → Deploy OVF Template
  Source: VMware-vSphere-Replication-<version>.ovf

  Step 1: Name and folder
    Name: vra-london
    Folder: Infrastructure VMs

  Step 2: Compute resource
    Select: host or cluster for VRA VM

  Step 3: Storage
    Storage policy: default (VRA needs minimal disk)
    Datastore: management datastore

  Step 4: Network
    Network: Management portgroup

  Step 5: Customize template
    IP Address: 10.10.10.50 (static)
    Subnet Mask: 255.255.255.0
    Gateway: 10.10.10.1
    DNS: 10.10.10.10
    NTP: ntp.corp.local
    Admin password: <set strong password>
    Root password: <set strong password>

  → Deploy (takes ~5 minutes)
```

---

## Register VRA with vCenter

After deployment, register VRA with vCenter:

```
VRA VAMI UI: https://vra-london.corp.local:5480
  Configuration → vCenter Server
    vCenter Address: vcenter-london.corp.local
    Username: administrator@vsphere.local
    Password: <password>
    Accept certificate
    → Register
```

After registration, VRA appears in vCenter → Site Recovery as a Replication Appliance.

---

## Deploy VRS (Scale-Out Server)

For environments with >500 replicated VMs, deploy additional VRS appliances:

```
vCenter → Site Recovery → vSphere Replication → Replication Servers → Deploy

  Same OVF as VRA, but select: Deploy as Replication Server
  Configure: same network settings
  After deploy: it auto-registers with the VRA
```

---

## Pair Sites

```
vCenter (Protected Site) → Site Recovery → New Site Pair
  Remote vCenter: vcenter-amsterdam.corp.local
  SSO credentials for remote vCenter: administrator@vsphere.local
  Remote VRA: vra-amsterdam.corp.local
  Accept certificate thumbprints for both VRA appliances
  → Pair
```

After pairing, configure replications on individual VMs:
```
vCenter → [VM] → right-click → Configure Replication
```

---

## Upgrade Process

Upgrade VRA by redeploying from new OVA (not in-place):

1. **Take a snapshot of the existing VRA VM** before starting
2. **Redeploy from new OVA** with same IP configuration
3. VRA re-registers with vCenter automatically (if same IP)
4. Existing replications resume without data loss — only the appliance is replaced

> Upgrade Protected Site VRA first (or either order — VRA upgrades are non-disruptive to replications)

```bash
# After redeployment, verify service is up:
ssh admin@vra-london.corp.local
systemctl status hms
```

Check Site Recovery → Sites → both sites still Connected after upgrade.

---

## Version Compatibility

Check the Interoperability Matrix before upgrading:
- https://interopmatrix.vmware.com
- Key dependencies: VR version ↔ vSphere version ↔ SRM version (if paired with SRM)
- VRA must be same version on both sites before pairing

---

## Post-Install Verification

```bash
# Verify VRA health
curl -sk https://vra-london.corp.local/api/rest/vr/health

# Configure a test VM replication:
# vCenter → [any test VM] → Configure Replication
#   Target site: amsterdam, RPO: 1 hour
#   Verify initial sync starts (status: Syncing)
#   Wait for initial sync to complete (status: OK)
```
