# Nexus Dashboard Lifecycle

<div class="kb-summary">
Nexus Dashboard Lifecycle reference covering Upgrade Overview, Compatibility Matrix, Pre-Upgrade Checklist, Node Management, Backup and Restore and 2 more sections.
</div>

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
1. Check the Cisco Nexus Dashboard Compatibility Matrix for target version compatibility
2. Verify ACI APIC and NX-OS firmware are compatible with the target ND version
3. Take a cluster backup: Admin > Backup and Restore > Backup Now (to SFTP/NFS)
4. Take VM snapshots of all ND nodes (for VMware deployments)
5. Note current cluster health: Admin > Cluster Configuration — all nodes Online
6. Download the ND upgrade image from software.cisco.com
7. Notify network operations team — brief service interruptions may occur per node during rolling upgrade
8. Schedule the upgrade in the change management system
```
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

Upgrade services after the base ND platform upgrade is complete and all nodes are healthy.

## Node Management

### Adding a Node

Expanding from 3 to 5 nodes requires the same ND version across all nodes.

```text
Admin > Cluster Configuration > Add Node
- Enter the new node's management IP and credentials
- ND orchestrates node join and cluster rebalancing
- Wait for the new node to reach Online status (10–20 minutes)
```

### Replacing a Failed Node

```text
1. Remove the failed node: Admin > Cluster Configuration > [Node] > Delete
2. Deploy a new ND node (OVA or physical) with identical network configuration
3. Join the new node: Admin > Cluster Configuration > Add Node
4. Verify cluster returns to full quorum
```

## Backup and Restore

### Automated Backup Schedule

```text
Admin > Backup and Restore > Scheduled Backup
- Destination: SFTP (sftp://<backup-host>/nexus-dashboard/)
- Schedule: weekly, Sunday 02:00
- Retention: keep 4 most recent
```

### Manual Backup

```text
Admin > Backup and Restore > Backup Now
- Backs up: cluster configuration, NDFC policies, NDI baselines, user accounts
- Note: does not back up NDI telemetry history (that data is ephemeral)
```

### Restore

```text
Admin > Backup and Restore > Restore
- Upload backup file
- Select what to restore (full cluster or specific services)
- Confirm — cluster will be restored to the backup state
```

## EOL Tracking

- Cisco EOL/EOS notices: [cisco.com/go/eos](https://cisco.com/go/eos)
- Search for "Nexus Dashboard" to find current EOS announcements
- Review quarterly and plan upgrades to stay on supported versions
- Upgrade packages: [software.cisco.com](https://software.cisco.com)

## Version Cadence

Cisco releases ND major versions approximately annually and maintenance releases (bug fixes) every 2–3 months. Target staying within 1–2 minor versions of the current release. Older versions typically see EOS announced 18–24 months after release.
