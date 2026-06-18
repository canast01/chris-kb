---
tags:
  - troubleshooting
  - powerstore
  - dell
  - known-issues
---
# Dell PowerStore — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known PowerStore bugs, error codes, and workarounds covering NAS, SAN, replication, and PowerStore Manager UI.

*Applies to: PowerStore OS 3.x / 4.x*
</div>

```text
┌─────────────────────────────────────────── Dell PowerStore ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       PowerStore: mid-range NVMe all-flash array with unified block and file capability       │   │
│   │                     Protocols: FC · iSCSI · NVMe-oF · NFS · SMB · REST API                    │   │
│   │                           Management: PowerStore Manager / REST API                           │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           T-model           │  │          Block only         │  │        iSCSI/FC/NVMe        │   │
│   │           X-model           │  │         Block + File        │  │       Unified protocol      │   │
│   │            Metro            │  │       Sync replication      │  │       Zero-RPO stretch      │   │
│   │          Protection         │  │        Snapshot/Clone       │  │       Immutable snaps       │   │
│   │             Mgmt            │  │          PSM / REST         │  │         Unified pane        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   Volume group   │ Logical containe │      iSCSI/FC     │    Host group    │  Shared policy   │   │
│   │Protection policy │ Snapshot/repl ru │      Internal     │    Admin role    │    Per volume    │   │
│   │   Metro volume   │ Sync replication │    Internal RPC   │   Certificate    │     Zero RPO     │   │
│   │     Snapshot     │     PiT copy     │      Internal     │    Admin role    │ Space-efficient  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerStore T/X appliance · NVMe drives · SAS expansion shelves · 10/25 GbE               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerStore         = Dell mid-range NVMe storage; T-model block-only, X-model unified block+file   │
│    PowerStore Manager = browser GUI and REST API endpoint for all PowerStore operations               │
│    Volume group       = logical collection of volumes sharing snapshot and replication policies       │
│    Protection policy  = assigned to volumes; defines snapshot schedule, retention, and replication    │
│    Metro volume       = synchronously replicated volume across two sites; zero RPO active-active      │
│    Snapshot           = space-efficient point-in-time copy; crash-consistent or app-consistent        │
│    Clone              = full writable copy of a volume or file system; independent lifecycle          │
│    Applied-to         = PowerStore host mapping; volumes are applied-to a host or host group object   │
│    Capacity license   = PowerStore uses usable-capacity licensing; licensed in TiB increments         │
│    Storage container  = PowerStore X-model; unified block and file from the same storage pool         │
│    Appliance          = single PowerStore node pair (dual controllers); scalable to 4 appliances      │
│    NVMe-oF            = NVMe over Fabrics; FC-NVMe or NVMe/TCP host connectivity on PowerStore        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- PowerStore alerts appear in PowerStore Manager → Infrastructure → Events.
- Collect logs via `gather_diagnostic_information` from the PowerStore CLI for support.
- SRS (Secure Remote Services) / ESRS must be active for proactive support.

## Host Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| iSCSI host shows single path | PowerStore 3.x | Multipath not configured on host | Install `multipath-tools`; configure `multipath.conf` with `user_friendly_names yes` | N/A |
| NFS export `Access Denied` | PowerStore 3.x | Export host access not configured for client IP | Add client IP to NAS server export access list in PowerStore Manager | N/A |

## Replication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Replication session stuck in `Synchronizing` | PowerStore 3.x | WAN bandwidth insufficient; replication behind | Check replication lag; verify TCP 443 between PowerStore management IPs cross-site | N/A |
| `Replication protection group out of sync` after network interruption | PowerStore 3.x | Session aborted mid-transfer | Pause and resume replication session in PowerStore Manager | N/A |

## PowerStore Manager

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Manager UI `503` after node reboot | PowerStore 3.x | Management services not fully started | Wait 5 minutes; if persistent, check node health via `service_user` CLI | N/A |
| Software upgrade stuck at `Validating` | PowerStore 4.x | ESRS / SRS connectivity check failing during preflight | Verify TCP 443 from PowerStore to esrs.dell.com; retry upgrade | N/A |

## See also

- [Dell PowerStore — Common Issues](common-issues/)
- [Dell CloudIQ — Known Issues](../../cloudiq/troubleshooting/known-issues.md)
