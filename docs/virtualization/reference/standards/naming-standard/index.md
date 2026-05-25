# Naming Standard

> Part of the [Standards](../index.md) reference.

---

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Naming Convention Patterns                         │
├──────────────────┬──────────────────────────────────────────────────────┤
│  Object          │  Pattern                      │  Example             │
├──────────────────┼───────────────────────────────┼──────────────────────┤
│ Virtual Machine  │ <env>-<app>-<##>              │ prod-sqldb-01        │
│ ESXi Host        │ esx-<site>-<##>               │ esx-syd-01           │
│ Cluster          │ <site>-<env>-cluster-<##>     │ syd-prod-cluster-01  │
│ Datastore        │ ds-<env>-<storage>-<proto>-<##>│ ds-prod-powermax-fc-01│
│ Port Group       │ pg-<vlan>-<description>       │ pg-1001-prod-vm      │
│ Distributed vSwitch│ vds-<site>-<cluster>-<##>  │ vds-syd-compute-01    │
│ Template         │ tmpl-<os>-<version>-<date>    │ tmpl-win2022-std-20260101│
│ iDRAC/iLO        │ idrac-esx-<site>-<##>         │ idrac-esx-syd-01     │
└──────────────────┴───────────────────────────────┴──────────────────────┘
  Tokens: env=prod/dev/test/uat/dr/mgmt │ site=syd/mel/etc.
```
## Overview

Consistent naming across the VMware environment reduces confusion during incidents, simplifies inventory queries, and supports automation. All new objects must follow this standard. Exceptions require a documented justification.

## Virtual Machines

Pattern: `<env>-<app>-<##>`

| Token | Values | Description |
|---|---|---|
| `<env>` | `prod`, `dev`, `test`, `uat`, `dr`, `mgmt` | Environment |
| `<app>` | Short application or service name | e.g. `sqldb`, `webfront`, `vcsa`, `nsx` |
| `<##>` | Two-digit zero-padded number | e.g. `01`, `02` |

Examples:
- `prod-sqldb-01`
- `dev-webfront-02`
- `mgmt-vcsa-01`
- `dr-sqldb-01`

## Clusters

Pattern: `<site>-<env>-cluster-<##>`

| Token | Values |
|---|---|
| `<site>` | `syd` (Sydney), `mel` (Melbourne), etc. |
| `<env>` | `prod`, `mgmt`, `edge`, `dr` |
| `<##>` | Zero-padded sequence number |

Examples:
- `syd-prod-cluster-01`
- `syd-mgmt-cluster-01`
- `mel-dr-cluster-01`

## ESXi Hosts

Pattern: `esx-<site>-<##>`

Examples:
- `esx-syd-01`
- `esx-mel-01`

For out-of-band management (iDRAC/iLO): `idrac-esx-<site>-<##>` or `ilo-esx-<site>-<##>`

## Datastores

Pattern: `ds-<env>-<storage>-<protocol>-<##>`

| Token | Values |
|---|---|
| `<env>` | `prod`, `dev`, `mgmt`, `dr` |
| `<storage>` | `powermax`, `flasharray`, `netapp`, `vsan` |
| `<protocol>` | `fc`, `iscsi`, `nfs`, `vsan` |

Examples:
- `ds-prod-powermax-fc-01`
- `ds-prod-flasharray-fc-01`
- `ds-mgmt-netapp-nfs-01`

## Port Groups

Pattern: `pg-<vlan>-<description>`

| Token | Description |
|---|---|
| `<vlan>` | 4-digit VLAN number |
| `<description>` | Short, lowercase description with hyphens |

Examples:
- `pg-1001-prod-vm`
- `pg-1002-vmotion`
- `pg-1003-vsan`
- `pg-1004-mgmt`

## Distributed Switches (vDS)

Pattern: `vds-<site>-<cluster_or_use>-<##>`

Examples:
- `vds-syd-compute-01`
- `vds-syd-edge-01`
- `vds-syd-mgmt-01`

## Folders

Pattern: `<env>-<purpose>` or match the cluster/application grouping.

Examples:
- `prod-compute-vms`
- `mgmt-tools`
- `dr-vms`

## vSAN Disk Groups

Disk groups are named automatically by vSAN based on device identifiers. Do not rename them.

## Templates

Pattern: `tmpl-<os>-<version>-<date>`

Examples:
- `tmpl-win2022-std-20260101`
- `tmpl-rhel9-20260101`

## Tags and Categories

| Category | Tag Examples |
|---|---|
| Environment | `prod`, `dev`, `test`, `uat`, `dr` |
| Backup Tier | `backup-gold`, `backup-silver`, `backup-none` |
| Application | Application or service name |
| Owner | Team or individual owner |

## Exceptions

Any object that cannot follow this standard must be documented with:
- The object name
- The reason for the exception
- Approval from the team lead
