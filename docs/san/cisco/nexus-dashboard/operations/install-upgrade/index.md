# Nexus Dashboard — Install & Upgrade


<div class="kb-summary">
> Part of the [Nexus Dashboard](../../index.md) reference.
</div>

---

## Overview

Nexus Dashboard is deployed as a 3-node or 5-node cluster. This page covers fresh installation (OVA on VMware) and in-place cluster upgrades. Application upgrades (NDFC, NDI) are a separate step performed after the ND platform upgrade.

---

## Pre-Installation Requirements

### Per Node (3-Node Cluster, OVA)

| Requirement | Value |
|---|---|
| Hypervisor | VMware ESXi 7.0+ or 8.x |
| vCPU | 16 (24 for NDFC + NDI) |
| RAM | 64 GB (128 GB for NDFC + NDI) |
| Storage | 500 GB thick provisioned (1 TB for NDFC + NDI) |
| NICs | 3 vNICs on separate port groups (mgmt, data, app) |
| NTP | All 3 nodes must reach the same NTP servers |
| DNS | Forward and reverse DNS for each node's mgmt IP |

### Network Prerequisites

- Management network: routed from client workstations; TCP 443 and SSH 22 reachable
- Data network: routed to switch management IPs and APIC/NDFC-managed fabric
- App/cluster network: L2 adjacency between all nodes (low-latency; < 5ms RTT)

Download the ND OVA from Cisco Software Download Center. Verify SHA-512 checksum before deployment.

---

## Fresh Installation — VMware OVA (3-Node Cluster)

### Step 1: Deploy Three OVAs

Deploy three identical OVA instances. In vCenter for each node:

1. **Actions > Deploy OVF Template**
2. Select the ND OVA file
3. VM name: `nd-dc1-1`, `nd-dc1-2`, `nd-dc1-3`
4. Select datastore with sufficient space (thick provisioning)
5. Map OVA networks to your port groups:
   - `mgmt` → Management VLAN port group
   - `data` → SAN/Fabric data port group
   - `app` → Cluster internal port group
6. On **Customize Template**, set for each node:
   - Management IP / mask / gateway
   - Data IP / mask
   - App IP / mask
   - DNS servers
   - NTP servers
   - Hostname (e.g. `nd-dc1-1.corp.example.com`)
   - Initial admin password
7. Do not power on yet.

### Step 2: Power On and Initialize Cluster

Power on all three nodes. Wait 10 minutes for initial startup.

```bash
# SSH to node 1 (the designated primary)
ssh ndadmin@nd-dc1-1.corp.example.com

# Initialize the cluster from node 1
acs cluster init \
  --name nd-dc1 \
  --primary-ip 10.10.5.21 \
  --node-ips 10.10.5.22,10.10.5.23 \
  --app-ips 192.168.100.1,192.168.100.2,192.168.100.3

# Monitor cluster formation (takes 10-20 minutes)
acs health
# Wait until all nodes show Healthy
```
```text
┌──────────────────────── Cisco Nexus Dashboard — Operations Install & Upgrade ─────────────────────────┐
│                                                                                                       │
│  ND cluster initial build and rolling upgrade process with pre/post validation steps.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Initial Install                │  │                Prerequisites                │   │
│   │          Deploy OVA/ISO: 3 node min          │  │          Hardware: 16 vCPU/64GB RAM         │   │
│   │         Bootstrap: node 1 as primary         │  │         Storage: 500GB min per node         │   │
│   │          Join: nodes 2+3 to cluster          │  │          Network: OOB + data VLANs          │   │
│   │           Configure: IP, NTP, DNS            │  │          NTP: synced before install         │   │
│   │          Install apps: NDFC/NDI/NDO          │  │          Cisco CCO: download images         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Bootstrap node 1 first; other nodes join via cluster join token; apps installed last                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Process                │  │           Post-Upgrade Validation           │   │
│   │            Backup: before upgrade            │  │         acs health: all nodes green         │   │
│   │           Upload image: UI or CLI            │  │             Apps: verify running            │   │
│   │         Rolling: one node at a time          │  │             Sites: all connected            │   │
│   │            Duration: ~45 min/node            │  │          Telemetry: flowing to NDI          │   │
│   │        Apps auto-upgrade post-cluster        │  │           Rollback: restore backup          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND nodes (UCS/VM) · management switch · NTP/DNS server · CCO download server                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OVA            = Open Virtualization Appliance; VMware VM image format for ND                        │
│  ISO            = Disk image for bare-metal ND node installation                                      │
│  Bootstrap      = First-node initialization creating the cluster with initial config                  │
│  Cluster join token= One-time secret additional nodes use to securely join cluster                    │
│  Rolling upgrade= ND upgrades one node at a time; cluster stays available throughout                  │
│  CCO            = Cisco Connection Online; software download portal                                   │
│  App auto-upgrade= After cluster upgrade, apps detect new platform and self-upgrade                   │
│  OOB VLAN       = Management VLAN on dedicated out-of-band network                                    │
│  Data VLAN      = In-band network VLAN used for site-to-ND app communication                          │
│  NTP pre-sync   = NTP must be configured and synced before cluster forms                              │
│  acs health     = Validates all nodes report green status after upgrade completes                     │
│  Rollback       = Only via backup restore; no in-place cluster downgrade supported                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

After a 48-hour validation window with no issues: delete the VM snapshots taken before the upgrade.

---

## Upgrade Applications (NDFC, NDI)

After the ND platform upgrade is confirmed healthy, upgrade installed applications:

1. Navigate to **Admin Console > Apps**.
2. Select the application (NDFC or NDI).
3. Click **Upgrade**.
4. Upload the new application image.
5. Click **Start Upgrade**. The application is briefly unavailable during the upgrade.
6. After upgrade: confirm app version and validate core functionality.

Upgrade NDFC before NDI. Validate NDFC functionality (fabric discovery, zone operations) before proceeding to NDI upgrade.

---

## Rollback

If a ND platform upgrade causes a cluster-breaking issue:

1. Power off all three ND VMs in vCenter.
2. Revert all three VMs to the pre-upgrade snapshot simultaneously.
3. Power on all three VMs.
4. Verify cluster reforms: `acs health` (takes 5-10 minutes).
5. Confirm NDFC and NDI are running.

**Note:** Snapshot revert restores the full VM state including the database. Any zone changes made after the snapshot (before rollback) will be lost. Ensure pre-upgrade zone exports are available to re-apply if needed.

---

## Adding a Node to an Existing Cluster

To scale a 3-node cluster to 5 nodes:

```bash
# Deploy two additional OVA nodes as per Step 1 above
# Configure their IPs but do not initialize them

# From the primary node, add the new nodes
acs cluster add-node --node-ip 10.10.5.24 --app-ip 192.168.100.4
acs cluster add-node --node-ip 10.10.5.25 --app-ip 192.168.100.5

# Monitor cluster expansion (takes 20-40 minutes)
acs health
acs nodes list
```

---

## Decommission

To decommission a Nexus Dashboard cluster:

1. Export all NDFC zone databases and device alias databases.
2. Take a final full backup.
3. Remove all registered sites and managed fabrics from NDFC to clean up switch-side references:
   - Remove NDFC service accounts from managed switches
   - Remove NDFC as SNMP trap destination on managed switches
4. Power off all three ND cluster VMs.
5. Delete VMs from vCenter.
6. Remove DNS entries.
