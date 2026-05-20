# Naming Standards

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
Clear naming makes troubleshooting easier.

| Object | Example |
|---|---|
| vCenter | vcsa-prod-01 |
| Cluster | cl-prod-compute-01 |
| ESXi Host | esx-prod-01 |
| Datastore | ds-prod-vsan-01 |
| Port Group | pg-prod-app-vlan100 |
| VM | appname-prod-01 |
| Template | tmpl-win2022-standard |
| Folder | Prod / Dev / Test / Infra |
