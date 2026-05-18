# Version Inventory

> Part of the [Inventory](../) reference.

---

```
┌──────────────────────┬─────────────┬─────────────┬────────────┬──────────────┐
│   Component          │   Current   │   Target    │  EOL Date  │  Priority    │
├──────────────────────┼─────────────┼─────────────┼────────────┼──────────────┤
│ vCenter Server       │  8.0 U3     │     —       │ Oct 2027   │  Low         │
│ ESXi (prod)          │  8.0 U3     │     —       │ Oct 2027   │  Low         │
│ ESXi (mgmt)          │  8.0 U2b    │  8.0 U3     │ Oct 2027   │  Medium ⚠   │
│ vSAN                 │  8.0 U3     │     —       │ Oct 2027   │  Low         │
│ NSX-T                │  4.1.2      │  4.2.x      │ Oct 2027   │  Medium ⚠   │
├──────────────────────┼─────────────┼─────────────┼────────────┼──────────────┤
│ VxRail Manager       │  8.0.300    │  8.0.310    │     —      │  Planned     │
│ Aria Operations      │  8.16       │     —       │     —      │  Low         │
│ Veeam B&R            │  12.1.2     │     —       │     —      │  Low         │
└──────────────────────┴─────────────┴─────────────┴────────────┴──────────────┘
  Rule: vCenter ≥ ESXi version at all times │ VxRail: always use LCM
```
## Overview

Track current and target versions across all VMware components. Use this page for upgrade planning, compliance reporting, and support case reference. Update after every upgrade.

## Core Platform Versions

| Component | Current Version | Target Version | EOL Date | Upgrade Priority | Last Updated | Notes |
|---|---|---|---|---|---|---|
| vCenter Server | 8.0 U3 | — | Oct 2027 | Low | 2026-03-10 | On current approved baseline |
| ESXi (prod cluster) | 8.0 U3 | — | Oct 2027 | Low | 2026-03-10 | All hosts aligned |
| ESXi (mgmt cluster) | 8.0 U2b | 8.0 U3 | Oct 2027 | Medium | 2025-11-01 | Upgrade scheduled Q3 2026 |
| vSAN | 8.0 U3 | — | Oct 2027 | Low | 2026-03-10 | Embedded in ESXi |
| NSX-T | 4.1.2 | 4.2.x | Oct 2027 | Medium | 2025-10-15 | Target upgrade H2 2026 |

## VxRail

| Component | Current Version | Target Version | EOL Date | Notes |
|---|---|---|---|---|
| VxRail Manager | 8.0.300 | 8.0.310 | — | Quarterly VxRail LCM planned |
| VxRail Firmware Bundle | 8.0.300-xxx | 8.0.310-xxx | — | Applied via VxRail LCM |
| Dell iDRAC (firmware) | 7.10.xx | 7.10.xx | — | Current approved baseline |

## Aria Suite

| Component | Current Version | Target Version | Notes |
|---|---|---|---|
| Aria Suite Lifecycle | 8.16 | — | Manages all Aria upgrades |
| Aria Operations | 8.16 | — | |
| Aria Automation | 8.16 | — | |
| Aria Operations for Logs | 8.16 | — | |

## Data Protection

| Component | Current Version | Target Version | Notes |
|---|---|---|---|
| Veeam Backup & Replication | 12.1.2 | — | Annual upgrade cycle |
| Veeam ONE | 12.1 | — | |

## Version Compliance Policy

| Policy | Requirement |
|---|---|
| ESXi version skew | All hosts in a cluster must be on the same ESXi build |
| vCenter / ESXi alignment | vCenter must be equal to or newer than all managed ESXi hosts |
| NSX / vCenter compatibility | Verify NSX–vCenter compatibility matrix before any upgrade |
| VxRail LCM | All VxRail upgrades must use VxRail LCM — never upgrade ESXi manually on VxRail |
| Upgrade approval | All upgrades require a change record and pre/post validation |

## Upgrade Planning Notes

| Component | Planned Upgrade Date | Change Reference | Owner | Status |
|---|---|---|---|---|
| ESXi mgmt cluster → 8.0 U3 | 2026-Q3 | CHG-1042 | C. Anastasiadis | Planned |
| NSX 4.1.2 → 4.2.x | 2026-H2 | TBD | Network/Infra Team | Under review |

## How to Check Versions

### vCenter and ESXi

```
vCenter UI → Administration → Deployment → System Configuration → Nodes
vCenter UI → Hosts and Clusters → Host → Summary tab (ESXi version)
```

### PowerCLI

```powershell
# ESXi version for all hosts in a cluster
Get-Cluster "cl-prod-compute-01" | Get-VMHost | Select Name, Version, Build | Sort Name
```

### NSX

```
NSX UI → System → Lifecycle Management → About NSX
```
