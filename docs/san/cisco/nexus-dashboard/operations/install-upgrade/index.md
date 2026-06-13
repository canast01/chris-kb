---
tags:
  - operations
  - san
---
# Cisco Nexus Dashboard — Operations Install & Upgrade

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

## Upgrade Overview

Nexus Dashboard supports rolling upgrades — the cluster upgrades one node at a time to maintain service availability throughout the process. Services (NDFC, NDI) are upgraded separately from the base ND platform.

**Always check compatibility before upgrading.**

## Compatibility Matrix

Before any upgrade, validate all component versions using the [Cisco Nexus Dashboard Compatibility Matrix](https://www.cisco.com/c/en/us/support/data-center-analytics/nexus-dashboard/products-device-support-tables-list.html).

Check compatibility between:
- Nexus Dashboard base platform version
- NDFC version
- NDI version
- ACI APIC firmware version
- NX-OS fabric switch firmware version

A version mismatch between ND and its managed fabrics can result in loss of management connectivity.

## Pre-Upgrade Checklist

```text
┌─────────────────────────────── Nexus Dashboard — Lifecycle Management ────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                    Deploy                    │  │                   Upgrade                   │   │
│   │              Bootstrap 3 nodes               │  │             Check release notes             │   │
│   │            Assign mgmt + data IPs            │  │             Backup config first             │   │
│   │             Form cluster via UI              │  │              acs upgrade apply              │   │
│   │            Install apps (NDI etc)            │  │             Rolling node upgrade            │   │
│   │               Onboard fabrics                │  │               Verify apps post              │   │
│   │              Configure ITSM out              │  │               Rollback if fail              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  3 physical or VM nodes · Cisco ISO install · upgrade via acs CLI or ND UI                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Bootstrap = Initial ND node setup: assign hostname, IPs, NTP, DNS via console                        │
│  Cluster form = Joining 3 nodes into quorum cluster via ND web UI                                     │
│  App install = Installing NDI, NDFC, NDO as apps from ND admin > Apps                                 │
│  Fabric onboard = Adding APIC or NX-OS fabric to ND with credentials                                  │
│  acs upgrade = CLI command to apply upgrade image to cluster                                          │
│  Rolling upgrade = Upgrading nodes sequentially to maintain quorum                                    │
│  Backup = acs backup create before upgrade; stored externally                                         │
│  Rollback = Restoring from backup if upgrade causes data loss                                         │
│  Release notes = Cisco release notes; check for breaking changes before upgrade                       │
│  Verify apps = Post-upgrade check: NDI collecting, NDFC managing, NDO syncing                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
### Replacing a Failed Node
```

1. Remove the failed node: Admin > Cluster Configuration > [Node] > Delete
2. Deploy a new ND node (OVA or physical) with identical network configuration
3. Join the new node: Admin > Cluster Configuration > Add Node
4. Verify cluster returns to full quorum

## Backup and Restore

### Automated Backup Schedule

Admin > Backup and Restore > Scheduled Backup
- Destination: SFTP (sftp://<backup-host>/nexus-dashboard/)
- Schedule: weekly, Sunday 02:00
- Retention: keep 4 most recent

### Manual Backup

Admin > Backup and Restore > Backup Now
- Backs up: cluster configuration, NDFC policies, NDI baselines, user accounts
- Note: does not back up NDI telemetry history (that data is ephemeral)

### Restore

Admin > Backup and Restore > Restore
- Upload backup file
- Select what to restore (full cluster or specific services)
- Confirm — cluster will be restored to the backup state

## EOL Tracking

- Cisco EOL/EOS notices: [cisco.com/go/eos](https://cisco.com/go/eos)
- Search for "Nexus Dashboard" to find current EOS announcements
- Review quarterly and plan upgrades to stay on supported versions
- Upgrade packages: [software.cisco.com](https://software.cisco.com)

## Version Cadence

Cisco releases ND major versions approximately annually and maintenance releases (bug fixes) every 2–3 months. Target staying within 1–2 minor versions of the current release. Older versions typically see EOS announced 18–24 months after release.
