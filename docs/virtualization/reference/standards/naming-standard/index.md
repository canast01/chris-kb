# Naming Standard


<div class="kb-summary">
Naming Standard reference covering Overview, Virtual Machines, Clusters, ESXi Hosts, Datastores and 7 more sections.
</div>

```
┌────────────────────────────────────── vSphere — Naming Standard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Consistent naming conventions for all vSphere objects — enables automation and auditing    │   │
│   │     Pattern: {prefix}-{env}-{function}-{site}-{nn} — lowercase, hyphens, no spaces or dots    │   │
│   │         Environment codes: prod / nprod / dev / dr; site codes: 3-letter DC identifier        │   │
│   │      Enforced via vCenter tags and automated naming check in CI/CD provisioning pipelines     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Consistent names drive automation, CMDB population, and audit traceability                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Infrastructure       │  │          Networking         │  │           Storage           │   │
│   │        Cluster: cl-*        │  │        VDS: vds-{env}       │  │        DS: ds-{type}        │   │
│   │       Host: esx-{site}      │  │       PG-{vlan}-{func}      │  │        ds-vsan-{site}       │   │
│   │       VM: {app}-{env}       │  │        NSX seg: seg-*       │  │        ds-nfs-{site}        │   │
│   │       Template: tmpl-*      │  │      Tier-0: t0-{site}      │  │        ds-vmfs-{site}       │   │
│   │       vCenter: vcsa-*       │  │      Tier-1: t1-{func}      │  │      Policy: pol-{tier}     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Non-compliant names flagged by naming lint script in provisioning pipeline                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Object      │     Pattern      │      Example      │     Max len      │      Notes       │   │
│   │     Cluster      │cl-{env}-{fn}-{nn}│ cl-prod-compute-01│        32        │    Lowercase     │   │
│   │    ESXi host     │ esx-{site}-{nn}  │     esx-lon-01    │        15        │    FQDN used     │   │
│   │        VM        │ {app}-{env}-{nn} │    app1-prod-01   │        15        │    FQDN match    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: server naming aligned with iDRAC hostname and rack label for traceability                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Prefix        = Object type identifier: cl (cluster), esx (host), ds (datastore), pg (portgroup)   │
│    Environment   = prod / nprod / dev / dr — applied to clusters, VMs, and datastores                 │
│    Site code     = 3-letter datacenter ID (lon, ams, nyc); embedded in host and DS names              │
│    Function      = Role identifier in cluster/VDS name: compute, edge, mgmt, vdi, db                  │
│    Sequential nn = Zero-padded two-digit counter per site/env: -01, -02, -03                          │
│    FQDN          = Fully Qualified Domain Name; VM hostname must match FQDN in DNS                    │
│    NSX segment   = seg-{function}-{vlan}: seg-web-100, seg-db-200, seg-app-300                        │
│    Port group    = PG-{VLAN ID}-{purpose}: PG-10-Mgmt, PG-20-vMotion, PG-30-vSAN                      │
│    Template      = tmpl-{os}-{version}: tmpl-rhel9-2024q4, tmpl-win2022-2024q4                        │
│    Policy name   = pol-{tier}: pol-gold, pol-silver, pol-bronze for storage SPBM                      │
│    Lint script   = CI/CD pre-provisioning check that validates names against naming regex             │
│    CMDB populate = Automated CMDB entry creation triggered by consistent naming pattern               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── vSphere — Naming Standard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Consistent naming conventions for all vSphere objects — enables automation and auditing    │   │
│   │     Pattern: {prefix}-{env}-{function}-{site}-{nn} — lowercase, hyphens, no spaces or dots    │   │
│   │         Environment codes: prod / nprod / dev / dr; site codes: 3-letter DC identifier        │   │
│   │      Enforced via vCenter tags and automated naming check in CI/CD provisioning pipelines     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Consistent names drive automation, CMDB population, and audit traceability                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Infrastructure       │  │          Networking         │  │           Storage           │   │
│   │        Cluster: cl-*        │  │        VDS: vds-{env}       │  │        DS: ds-{type}        │   │
│   │       Host: esx-{site}      │  │       PG-{vlan}-{func}      │  │        ds-vsan-{site}       │   │
│   │       VM: {app}-{env}       │  │        NSX seg: seg-*       │  │        ds-nfs-{site}        │   │
│   │       Template: tmpl-*      │  │      Tier-0: t0-{site}      │  │        ds-vmfs-{site}       │   │
│   │       vCenter: vcsa-*       │  │      Tier-1: t1-{func}      │  │      Policy: pol-{tier}     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Non-compliant names flagged by naming lint script in provisioning pipeline                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Object      │     Pattern      │      Example      │     Max len      │      Notes       │   │
│   │     Cluster      │cl-{env}-{fn}-{nn}│ cl-prod-compute-01│        32        │    Lowercase     │   │
│   │    ESXi host     │ esx-{site}-{nn}  │     esx-lon-01    │        15        │    FQDN used     │   │
│   │        VM        │ {app}-{env}-{nn} │    app1-prod-01   │        15        │    FQDN match    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: server naming aligned with iDRAC hostname and rack label for traceability                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Prefix        = Object type identifier: cl (cluster), esx (host), ds (datastore), pg (portgroup)   │
│    Environment   = prod / nprod / dev / dr — applied to clusters, VMs, and datastores                 │
│    Site code     = 3-letter datacenter ID (lon, ams, nyc); embedded in host and DS names              │
│    Function      = Role identifier in cluster/VDS name: compute, edge, mgmt, vdi, db                  │
│    Sequential nn = Zero-padded two-digit counter per site/env: -01, -02, -03                          │
│    FQDN          = Fully Qualified Domain Name; VM hostname must match FQDN in DNS                    │
│    NSX segment   = seg-{function}-{vlan}: seg-web-100, seg-db-200, seg-app-300                        │
│    Port group    = PG-{VLAN ID}-{purpose}: PG-10-Mgmt, PG-20-vMotion, PG-30-vSAN                      │
│    Template      = tmpl-{os}-{version}: tmpl-rhel9-2024q4, tmpl-win2022-2024q4                        │
│    Policy name   = pol-{tier}: pol-gold, pol-silver, pol-bronze for storage SPBM                      │
│    Lint script   = CI/CD pre-provisioning check that validates names against naming regex             │
│    CMDB populate = Automated CMDB entry creation triggered by consistent naming pattern               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Standards](../index.md) reference.

---

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
