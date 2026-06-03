# Cisco DCNM — Standards


<div class="kb-summary">
> Part of the [Cisco DCNM](../../index.md) reference.
</div>

---

## Overview

This page defines design standards, naming conventions, and configuration baselines for Cisco DCNM 11.x deployments managing MDS SAN fabrics.

---

## Appliance Naming

| Object | Convention | Example |
|---|---|---|
| DCNM appliance VM | `dcnm-<site>-<number>` | `dcnm-dc1-01` |
| DCNM HA VIP DNS | `dcnm-<site>.corp.example.com` | `dcnm-dc1.corp.example.com` |
| DCNM HA active node | `dcnm-<site>-active.corp.example.com` | |
| DCNM HA standby node | `dcnm-<site>-standby.corp.example.com` | |

---

## Fabric and VSAN Naming Conventions

| Object | Convention | Example |
|---|---|---|
| DCNM fabric | `<SITE>-FABRIC-<A or B>` | `DC1-FABRIC-A` |
| VSAN | `<site>-VSAN-<number>` (display name) | `DC1-VSAN-10` |
| VSAN ID | Production: 10–99, Management: 100–109, Test: 200–299 | VSAN 10 |

Avoid VSAN 1 for production traffic. VSAN 1 is the default and carries unintended ports if port-to-VSAN assignment is not carefully managed.

---

## Device Alias Standards

Device aliases are fabric-wide identifiers for FC ports (host HBAs and storage ports). Maintain these naming conventions for all aliases:

| Port Type | Convention | Example |
|---|---|---|
| Host HBA (primary) | `<hostname>-hba0` | `esxi01-hba0` |
| Host HBA (secondary) | `<hostname>-hba1` | `esxi01-hba1` |
| Storage array port | `<array-name>-<controller>-<port>` | `purestor01-ct0-fc0` |
| Tape library port | `<library-name>-<port>` | `lib01-fc0` |

Maintain device aliases via DCNM's Device Alias editor (**SAN > Device Alias**) rather than per-switch configuration, so that CFS distribution keeps all switches in sync.

---

## Zoning Standards

### Zone Naming

| Zone Type | Convention | Example |
|---|---|---|
| Host-to-storage zone | `HOST-<hostname>-<array>-<array-port>` | `HOST-esxi01-purestor01-ct0fc0` |
| Test zone | `TEST-<hostname>-<date>` | `TEST-esxi01-20260506` |
| Maintenance zone | `MAINT-<hostname>-<date>` | `MAINT-esxi01-20260506` |

### Zone Set Naming

| Convention | Example |
|---|---|
| `<site>-<fabric>-ZONESET` | `DC1-FABRIC-A-ZONESET` |

### Zoning Rules

- **Single-initiator zoning only** — each zone contains exactly one host HBA and one or more storage targets. Never zone multiple initiators together.
- **WWN-based zoning preferred** — use device aliases (which map to WWNs) rather than FC ID (domain/area/port) zoning. FC IDs are not stable across fabric rebuilds.
- **No default zone** — ensure the default zone policy is `deny` on all VSANs:

```bash
# On each MDS switch (NX-OS CLI)
zone default-zone permit vsan 10
# Expected after setting deny:
no zone default-zone permit vsan 10
# Verify:
show zone status vsan 10
# Mode: Basic, Default-zone: deny
```text
┌──────────────────────────────────── Cisco DCNM — Design Standards ────────────────────────────────────┐
│                                                                                                       │
│  DCNM design: HA deployment, management VLAN, RBAC, TLS, backup, and scale limits.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Deployment Standards             │  │              Security Standards             │   │
│   │          HA pair: primary + standby          │  │            TLS 1.2+ for all HTTPS           │   │
│   │          Dedicated management VLAN           │  │          TACACS+ via ISE mandatory          │   │
│   │          8 vCPU / 32 GB RAM (large)          │  │          RBAC: operator = read-only         │   │
│   │            NTP for all timestamps            │  │         SNMPv3 only; disable v1/v2c         │   │
│   │          Dedicated DNS entries mgmt          │  │           IP whitelist API access           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  HA and dedicated management VLAN are baseline; ISE + TLS are security minimums.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Operational Standards             │  │            Scalability Guidelines           │   │
│   │         Backup: nightly NFS; 30-day          │  │          Max 2,000 switches / node          │   │
│   │        Alert review: daily SNMP check        │  │           Max 200,000 ports / node          │   │
│   │         Zone changes: change ticket          │  │          Separate SAN vs LAN domain         │   │
│   │            Firmware via DCNM only            │  │           Scale-out: multi-cluster          │   │
│   │            Quarterly DCNM upgrade            │  │          2 TB storage perf history          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere host · 2 TB datastore · management Ethernet · NFS backup share                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HA pair         = DCNM primary + standby VMs; database replication between them                      │
│  Management VLAN = isolated VLAN for OOB switch management and DCNM traffic                           │
│  ISE             = Cisco Identity Services Engine; provides TACACS+ for DCNM                          │
│  TLS 1.2+        = minimum TLS version for DCNM HTTPS GUI and REST API                                │
│  RBAC            = Role-Based Access Control; network-admin/operator/read-only                        │
│  SNMPv3          = SNMP version 3; auth + privacy mode; disable v1/v2c in DCNM                        │
│  IP whitelist    = restrict REST API source IPs to automation host subnet                             │
│  NFS backup      = nightly DCNM config and database export to NFS mount                               │
│  2,000 switches  = Cisco-recommended maximum MDS/Nexus per DCNM instance                              │
│  SAN vs LAN      = DCNM manages both; separate logical domains per best practice                      │
│  Multi-cluster   = multiple DCNM instances federated; each manages a subset                           │
│  Change ticket   = ITSM requirement; all zone and config changes pre-approved                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Performance Monitoring Standards

| Metric | Warning Threshold | Critical Threshold | Action |
|---|---|---|---|
| ISL utilization | 70% sustained 5 min | 90% sustained 1 min | Capacity review |
| Port error rate (CRC) | > 0 per 15 min | > 10 per 5 min | Physical layer investigation |
| Port LOS count | > 0 per hour | > 5 per hour | SFP/cable check |
| F_Port link down | Any unexpected | Any | Escalate to host/storage team |

---

## Upgrade Standards

- Stay within two minor versions of the current Cisco recommended DCNM release.
- Always test upgrades in a non-production DCNM instance (if available) before production.
- Perform DCNM upgrade in a scheduled maintenance window; the appliance is unavailable for 20–40 minutes during upgrade.
- DCNM upgrade does not affect managed switch operation — switches continue to forward I/O while DCNM is offline.
