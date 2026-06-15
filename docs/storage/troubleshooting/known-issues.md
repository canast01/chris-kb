---
tags:
  - troubleshooting
  - storage
  - known-issues
---
# Storage — Known Issues Reference

<div class="kb-summary">
Index of storage product known issues and error codes. This top-level page links to per-product known-issues catalogs covering NetApp, Pure Storage, Dell storage, and Ceph.

*Applies to: All storage products in this KB*
</div>

```text
┌─────────────────────────────── Storage Troubleshooting Known Issues.Md ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Troubleshooting: Storage Troubleshooting Known Issues.Md platform               │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │             Management: Storage Troubleshooting Known Issues.Md management console            │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Storage Troubleshooting Known Issues.Md infrastructure · management network · monitorin  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Troubleshooting    = Storage Troubleshooting Known Issues.Md platform overview and core concepts   │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

Storage issues often surface as application errors (I/O timeout, permission denied) — identify the protocol layer (NFS, iSCSI, FC, S3) before diving into array-specific known issues.

## Storage Product Known-Issues Pages

### NetApp

| Product | Known Issues |
|---|---|
| ONTAP | [ONTAP — Known Issues](netapp/ontap/troubleshooting/known-issues/) |
| SnapCenter | [SnapCenter — Known Issues](netapp/snapcenter/troubleshooting/known-issues/) |
| SnapMirror | [SnapMirror — Known Issues](netapp/snapmirror/troubleshooting/known-issues/) |
| InsightIQ | [InsightIQ — Known Issues](netapp/insightiq/troubleshooting/known-issues/) |
| Keystone | [Keystone — Known Issues](netapp/keystone/troubleshooting/known-issues/) |
| Superna Eyeglass | [Superna Eyeglass — Known Issues](netapp/superna-eyeglass/troubleshooting/known-issues/) |

### Pure Storage

| Product | Known Issues |
|---|---|
| FlashArray | [FlashArray — Known Issues](pure/flasharray/troubleshooting/known-issues/) |
| FlashBlade | [FlashBlade — Known Issues](pure/flashblade/troubleshooting/known-issues/) |
| Pure1 | [Pure1 — Known Issues](pure/pure1/troubleshooting/known-issues/) |

### Dell Storage

| Product | Known Issues |
|---|---|
| PowerStore | [PowerStore — Known Issues](dell/powerstore/troubleshooting/known-issues/) |
| PowerScale | [PowerScale — Known Issues](dell/powerscale/troubleshooting/known-issues/) |
| PowerMax | [PowerMax — Known Issues](dell/powermax/troubleshooting/known-issues/) |
| Data Domain | [Data Domain — Known Issues](dell/data-domain/troubleshooting/known-issues/) |
| Unity | [Unity — Known Issues](dell/unity/troubleshooting/known-issues/) |
| VPLEX | [VPLEX — Known Issues](dell/vplex/troubleshooting/known-issues/) |
| RecoverPoint | [RecoverPoint — Known Issues](dell/recoverpoint/troubleshooting/known-issues/) |

### Open Source

| Product | Known Issues |
|---|---|
| Ceph | [Ceph — Known Issues](ceph/troubleshooting/known-issues/) |

## See also

- [Storage — Common Issues](index.md)
- [NFS — Known Issues](../networking/protocols/nfs/troubleshooting/known-issues/)
- [iSCSI — Known Issues](../networking/protocols/iscsi/troubleshooting/known-issues/)
