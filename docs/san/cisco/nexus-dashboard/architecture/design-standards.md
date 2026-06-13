---
tags:
  - architecture
  - san
---
# Nexus Dashboard — Standards


<div class="kb-summary">
Standards reference covering Overview, Cluster Naming, Network Interface Standards, Sizing Guidelines, Site Registration Standards and 6 more sections.

*Applies to: Cisco MDS · Nexus*
</div>

```text
┌──────────────────────── Cisco Nexus Dashboard — Architecture Design Standards ────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    ND design standards: node sizing, HA topology, network requirements, app placement rules   │   │
│   │           Always deploy 3 master nodes minimum; never 1-node or 2-node in production          │   │
│   │          OOB and Data networks must be separate VLANs; MTU 9000 required on Data VLAN         │   │
│   │        NDI and NDFC can co-exist on same cluster; NDO should be on a dedicated cluster        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Size cluster → configure networks → deploy nodes → install apps → validate                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Node Sizing         │  │        Network Design       │  │        App Placement        │   │
│   │         Virt: 16vCPU        │  │        OOB mgmt VLAN        │  │        NDFC + NDI OK        │   │
│   │       Virt: 64 GB RAM       │  │        Data VLAN sep.       │  │         NDO separate        │   │
│   │      Virt: 550 GB disk      │  │        MTU 9000 data        │  │       Per Cisco guide       │   │
│   │        Phys: UCS C220       │  │        Ext svc IP /27       │  │       App compat list       │   │
│   │        3 masters + W        │  │        DNS + NTP req.       │  │       Worker for scale      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Always check Cisco ND hardware and software compatibility guide before deployment                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Requirement    │       Spec       │        Why        │      Verify      │      Notes       │   │
│   │     HA nodes     │  3 masters min   │       Quorum      │  ND cluster UI   │   Add workers    │   │
│   │     OOB VLAN     │    L3 routed     │    Admin access   │    Ping ND IP    │    Dedicated     │   │
│   │    Data VLAN     │    Jumbo MTU     │     Telemetry     │   Ping fabric    │     MTU 9000     │   │
│   │    App compat    │   Cisco matrix   │      Co-exist     │    App health    │   NDO separate   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: vSphere cluster (DRS, HA) · dedicated data NIC for each ND node · OOB switch             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Master node    = ND node running Kubernetes control plane; always deploy exactly 3                 │
│    Worker node    = Additional ND compute node for app pods; scale-out option                         │
│    Standby node   = Spare master; auto-joins if a master fails; recommended in production             │
│    OOB network    = Out-of-band admin network; used for ND UI, SSH, and switch SSH access             │
│    Data network   = In-band fabric-facing NIC; ND apps poll switches and receive telemetry            │
│    MTU 9000       = Jumbo frames required on Data VLAN for ND telemetry and flow export               │
│    Ext. svc IP    = Pool of IPs for Kubernetes LoadBalancer services (ND apps endpoints)              │
│    App compat     = Cisco publishes which app versions run together on same ND release                │
│    NDO separation = NDO multi-site orchestration works best isolated from NDFC/NDI cluster            │
│    DNS required   = ND nodes must resolve DNS; add ND hostnames to DNS before deploy                  │
│    NTP required   = All ND nodes and managed switches must be NTP-synchronised                        │
│    Cisco HCL      = Hardware Compatibility List; verify server model and NIC before deploy            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [Nexus Dashboard](../index.md) reference.

---

## Overview

This page defines design standards, naming conventions, sizing guidelines, and configuration baselines for Cisco Nexus Dashboard deployments. Apply these standards at initial deployment and validate during periodic operational reviews.

---

## Cluster Naming

| Object | Convention | Example |
|---|---|---|
| ND cluster hostname (per node) | `nd-<site>-<n>` | `nd-dc1-1`, `nd-dc1-2`, `nd-dc1-3` |
| ND cluster VIP / management IP | `nd-<site>.corp.example.com` | `nd-dc1.corp.example.com` |
| ND DNS entry | One A record per node + CNAME for cluster UI | `nd-dc1.corp.example.com → 10.10.5.20` |

Clients (engineers, scripts) should use the cluster DNS name, not individual node IPs. This allows transparent failover when the cluster elects a new leader.

---

## Network Interface Standards

Each ND node requires three interfaces. Follow this assignment convention:

| Interface | Network | VLAN | Example IP Range |
|---|---|---|---|
| `mgmt0` | Management | VLAN 100 (mgmt) | 10.10.5.0/24 |
| `data0` | SAN/LAN fabric data network | VLAN 200 (fabric mgmt) | 10.20.0.0/16 |
| `app0` | ND cluster internal | Dedicated or same as mgmt | 192.168.100.0/24 |

The `data0` network must have routed connectivity to all managed switch management interfaces. The `app0` network must have L2 adjacency (or low-latency L3) between all ND cluster nodes — use a dedicated VLAN if possible.

---

## Sizing Guidelines

### NDFC SAN-Only (3-Node Cluster, OVA)

| Fabric Size | vCPU/node | RAM/node | Storage/node | Notes |
|---|---|---|---|---|
| Small (≤ 50 switches) | 16 | 64 GB | 500 GB | Standard OVA |
| Medium (≤ 150 switches) | 16 | 64 GB | 1 TB | Increase storage only |
| Large (≤ 500 switches) | 24 | 128 GB | 2 TB | Physical appliance preferred |

### NDFC + NDI Combined (3-Node Cluster)

NDI adds significant resource overhead due to flow telemetry ingestion. Minimum for NDFC + NDI:
- vCPU: 24 per node
- RAM: 128 GB per node
- Storage: 2 TB per node (NDI retains 30 days of telemetry by default)

For large-scale NDI (> 20,000 flows/second): use a 5-node cluster with physical appliances.

---

## Site Registration Standards

Each managed fabric (data centre site) is registered as a site in Nexus Dashboard. Follow these naming and scoping conventions:

| Object | Convention | Example |
|---|---|---|
| Site name | `<SITE>-<FABRIC-TYPE>` | `DC1-SAN`, `DC1-ACI`, `DC2-SAN` |
| Site description | Include city, building, and primary contact | `Data Centre 1 — Sydney — SAN team` |

Avoid generic names like `Site1` or `Fabric-A`. Use names that immediately identify the physical location and fabric type.

---

## Application Version Compatibility Standards

Always verify the Cisco ND-App compatibility matrix before upgrades:
- URL: `https://www.cisco.com/c/en/us/support/cloud-systems-management/nexus-dashboard/series.html`

Apply this rule: **upgrade ND platform before upgrading hosted apps**. Never run an app version that requires a higher ND platform version than is installed.

| Upgrade Order | Notes |
|---|---|
| 1. Take ND cluster backup | Pre-upgrade mandatory |
| 2. Upgrade ND platform | All apps will be temporarily unavailable |
| 3. Validate ND cluster health | All nodes healthy, all apps Running |
| 4. Upgrade NDFC (if applicable) | Follow NDFC release notes |
| 5. Upgrade NDI (if applicable) | Follow NDI release notes |
| 6. Validate end-to-end | Fabric discovery, alerts, telemetry |

---

## NDFC SAN Configuration Baselines

### VSAN Naming

| Object | Convention | Example |
|---|---|---|
| VSAN display name | `<SITE>-VSAN-<ID>` | `DC1-VSAN-10` |
| VSAN ID range (production) | 10–99 | VSAN 10, VSAN 11 |
| VSAN ID range (management) | 100–109 | VSAN 100 |
| VSAN ID range (test/dev) | 200–299 | VSAN 200 |

### Zone Naming (NDFC)

Same conventions as DCNM standards apply — see [DCNM Standards](../../cisco-dcnm/architecture/design-standards/index.md) for the zone naming table. NDFC uses the same zone model as DCNM.

### NDFC Fabric Template Standards

When creating a new SAN fabric in NDFC, use the **MDS** fabric template. Configure:

| Setting | Recommended Value | Notes |
|---|---|---|
| Default zone mode | `deny` | Never use `permit`; forces explicit zoning |
| Zone mode | Enhanced zoning | Better default-deny semantics |
| Device alias mode | Enhanced | Fabric-wide CFS distribution |
| SNMP version | v3 only | Disable v1/v2c |
| SSH key type | RSA 2048+ | Per switch, stored in NDFC |

---

## Backup Standards

| Backup Type | Frequency | Retention | Storage |
|---|---|---|---|
| ND cluster full backup | Weekly | 4 copies | External SCP/SFTP server |
| NDFC zone export (all fabrics) | Before each zone change | 90 days | Change management system |
| Pre-upgrade ND backup | Before every upgrade | Indefinite | External backup server |

The ND backup includes the full cluster state: NDFC database (zones, device aliases, inventory), NDI telemetry data (optional), and platform configuration (users, LDAP, certificates). Exclude large telemetry datasets from routine backups to keep backup size manageable.

---

## Alert and Notification Standards

| Severity | Notification Method | Audience |
|---|---|---|
| Critical | Email + page (PagerDuty / oncall) | SAN team on-call |
| Major | Email | SAN team distribution list |
| Minor | Email (digest daily) | SAN team distribution list |
| Info | Dashboard only | — |

Configure notification rules per application (NDFC and NDI have independent alert configurations). All production fabrics must have at minimum a Critical alert email rule configured before handover to operations.

---

## Access Control Standards

| Account Type | Auth Method | Role | Notes |
|---|---|---|---|
| Named engineers | LDAP or SAML SSO | Minimum required role | No shared accounts |
| Service accounts | Local + API token | Site Operator or lower | Password in vault |
| Break-glass admin | Local | Admin | One account; stored in vault |
| Monitoring scripts | Local service account | Viewer | API-only; no GUI login needed |

LDAP or SAML must be configured and tested before retiring the initial local admin account. The break-glass local admin is retained permanently as a recovery mechanism.

---

## Change Management Requirements

All changes performed through Nexus Dashboard or NDFC must be accompanied by:

1. An approved change record with the change window specified
2. A pre-change backup (ND cluster backup + zone export)
3. Rollback plan documented (ND cluster restore or zone rollback)
4. Post-change validation results recorded
5. Change record closed with actual start/end times and outcome

For zone changes: export the before and after zone set and attach both to the change record.
