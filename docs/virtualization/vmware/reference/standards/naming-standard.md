---
tags:
  - reference
description: "Naming Standard reference covering Overview, Virtual Machines, Clusters, ESXi Hosts, Datastores and 7 more sections."
---
# Naming Standard

<div class="kb-summary">
Naming Standard reference covering Overview, Virtual Machines, Clusters, ESXi Hosts, Datastores and 7 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

> Part of the [Standards](index.md) reference.

---

```d2
direction: down

virtual_machines: "Virtual Machines" {shape: rectangle}
clusters: "Clusters" {shape: rectangle}
esxi_hosts: "ESXi Hosts" {shape: rectangle}
datastores: "Datastores" {shape: rectangle}
port_groups: "Port Groups" {shape: rectangle}
distributed_switches_vds: "Distributed Switches (vDS)" {shape: rectangle}

virtual_machines -> clusters: hardens
clusters -> esxi_hosts: hardens
esxi_hosts -> datastores: hardens
datastores -> port_groups: hardens
port_groups -> distributed_switches_vds: hardens
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
