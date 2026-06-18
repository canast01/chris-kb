---
tags:
  - snapcenter
  - netapp
  - networking
  - firewall
  - ports
  - backup
---
# NetApp SnapCenter — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for NetApp SnapCenter. SnapCenter provides application-aware backup and recovery using NetApp Snapshot copies. Covers the SnapCenter Server, plugin hosts, and storage system connections.

*Applies to: SnapCenter 5.x*
</div>

```text
┌────────────────────────────────────────── NetApp SnapCenter ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          SnapCenter: centralised backup and recovery orchestration for NetApp storage         │   │
│   │                           Protocols: HTTPS · iSCSI · FC · NFS · SMB                           │   │
│   │                             Management: SnapCenter GUI / REST API                             │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Server           │  │          Windows VM         │  │       Central control       │   │
│   │           Plug-in           │  │          Host agent         │  │        App-consistent       │   │
│   │            Policy           │  │       Schedule/retain       │  │         Backup rule         │   │
│   │        Resource group       │  │       Grouped targets       │  │        Shared policy        │   │
│   │           Recovery          │  │       Volume/LUN/file       │  │       Granular restore      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   SQL plug-in    │  MSSQL backups   │       HTTPS       │   Windows auth   │  App-consistent  │   │
│   │  Oracle plug-in  │  Oracle backups  │       HTTPS       │       SSH        │ RMAN integratio  │   │
│   │  VMware plug-in  │  VM/VMDK backup  │   HTTPS/vCenter   │   vCenter SSO    │   vSphere API    │   │
│   │ SAP HANA plug-in │   HANA backups   │       HTTPS       │     SAP auth     │   Backint API    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SnapCenter Server (Windows) · ONTAP clusters · plug-in hosts · application servers       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapCenter         = NetApp backup orchestration; coordinates app-consistent snapshots via plug-i  │
│    Plug-in            = host-side agent; quiesces application before snapshot: SQL, Oracle, VMware    │
│    Resource group     = set of resources sharing a backup policy and schedule in SnapCenter           │
│    Policy             = SnapCenter object defining snapshot frequency, retention, and replication ta  │
│    App-consistent     = snapshot taken after DB quiesce; guarantees crash-consistent recovery         │
│    Clone lifecycle    = SnapCenter clone: create from snapshot, provision to host, then delete        │
│    FlexClone          = underlying ONTAP technology; SnapCenter clone maps to an ONTAP FlexClone      │
│    Vault policy       = SnapCenter policy that also replicates snapshots to SnapVault destination     │
│    Mirror policy      = SnapCenter policy that replicates snapshots via SnapMirror to DR cluster      │
│    RBAC               = SnapCenter role-based access; Admin, Backup Operator, Restore Operator roles  │
│    SMF                = SnapCenter MySQL database storing job history, policies, and resource config  │
│    SnapCenter API     = REST API on port 8143; full feature coverage for automation workflows         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Inbound — Admin to SnapCenter Server

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 8146 | TCP | Admin browsers | SnapCenter web UI (HTTPS) |
| 8145 | TCP | SnapCenter plugins | SnapCenter Server → plugin host communication |
| 22 | TCP | Jump hosts | SSH — SnapCenter Server OS access (Linux-based SnapCenter) |

## SnapCenter Server to Plugin Hosts

SnapCenter pushes plugins to managed hosts and coordinates backup jobs.

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 8145 | TCP | SnapCenter Server | Windows plugin hosts | SnapCenter SMCore service on Windows |
| 22 | TCP | SnapCenter Server | Linux plugin hosts | SSH — Linux plugin management and deployment |
| 5985/5986 | TCP | SnapCenter Server | Windows plugin hosts | WinRM — Windows host management |

## SnapCenter / Plugin Hosts to NetApp Storage

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | SnapCenter Server | ONTAP cluster management LIF | ONTAP REST API — Snapshot operations, cloning, SVM management |
| 443 | TCP | SnapCenter Server | SVM management LIF | SVM-scoped REST API for NAS/SAN operations |
| 2049 | TCP | Plugin hosts | ONTAP NFS data LIF | NFS mount for backup data path |
| 3260 | TCP | Plugin hosts | ONTAP iSCSI data LIF | iSCSI LUN access for backup data path |

## Plugin Host to SnapCenter Server (Result Reporting)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 8145 | TCP | Windows plugin hosts | SnapCenter Server | Plugin → Server result and status reporting |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin browsers | SnapCenter Server | 8146 | Web UI |
| SnapCenter Server | Windows hosts | 8145, 5986 | Plugin management |
| SnapCenter Server | Linux hosts | 22 | Linux plugin |
| SnapCenter Server | ONTAP mgmt LIF | 443 | Snapshot coordination |
| Plugin hosts | ONTAP data LIFs | 2049, 3260 | Data path for backup |

## Verify

```bash
# From admin workstation — test SnapCenter web UI
curl -sk -o /dev/null -w "%{http_code}" https://<snapcenter-server>:8146/

# From SnapCenter Server — test ONTAP API
curl -sk -o /dev/null -w "%{http_code}" https://<ontap-mgmt-lif>/api/cluster

# From plugin host — test SnapCenter Server
nc -zv <snapcenter-server> 8145

# From plugin host (Windows) — test NFS to ONTAP
showmount -e <ontap-nfs-lif>
```

## See also

- [NetApp SnapCenter — Architecture](how-it-works/)
- [NetApp ONTAP — Ports](../../ontap/architecture/ports.md)
- [NetApp SnapMirror — Ports](../../snapmirror/architecture/ports.md)
