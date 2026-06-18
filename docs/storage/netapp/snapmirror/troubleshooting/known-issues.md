---
tags:
  - troubleshooting
  - snapmirror
  - netapp
  - known-issues
---
# NetApp SnapMirror — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known SnapMirror bugs, error codes, and workarounds. SnapMirror is an ONTAP feature — most issues are cluster peering or intercluster LIF connectivity problems.

*Applies to: ONTAP 9.x SnapMirror / SnapVault / Cloud*
</div>

```text
┌────────────────────────────────────────── NetApp SnapMirror ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        SnapMirror: ONTAP replication technology for DR, backup, and business continuity       │   │
│   │     Protocols: SnapMirror protocol (encrypted) · NFS/SMB/iSCSI at destination after break     │   │
│   │                       Management: ONTAP System Manager / SnapMirror CLI                       │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Async            │  │        Periodic sync        │  │         RPO: minutes        │   │
│   │             Sync            │  │           Zero RPO          │  │          Sub-ms lag         │   │
│   │            SM-BC            │  │        Active-active        │  │        Transparent FO       │   │
│   │            Vault            │  │        Long retention       │  │         Backup copy         │   │
│   │            Cloud            │  │         ONTAP → CVO         │  │       Cloud DR/backup       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │ Async SnapMirror │  DR replication  │    SM protocol    │   Certificate    │   RPO minutes    │   │
│   │ Sync SnapMirror  │  Zero-RPO sync   │    SM protocol    │   Certificate    │ StrictSync/Sync  │   │
│   │      SM-BC       │ Active-active SA │    SM protocol    │     Mediator     │    No RPO/RTO    │   │
│   │    SnapVault     │ Backup retention │    SM protocol    │   Certificate    │ Longer retentio  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Source ONTAP cluster · destination ONTAP cluster · intercluster LIFs · WAN link          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapMirror         = ONTAP replication; transfers only changed blocks after initial baseline sync  │
│    Intercluster LIF   = dedicated logical interface for SnapMirror traffic between clusters           │
│    SnapMirror policy  = defines schedule, retention, and transfer type (async/sync/vault)             │
│    Baseline transfer  = first full snapshot transfer establishing the SnapMirror relationship         │
│    Update             = incremental transfer; only sends new or changed blocks since last successful  │
│    Snapmirror break   = breaks the DR relationship; activates destination volume for read-write       │
│    Resync             = re-establishes a broken SnapMirror relationship from the last common snapsho  │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN volum  │
│    Mediator           = ONTAP Mediator; quorum service for SM-BC running on Linux VM at third site    │
│    SnapVault          = SnapMirror variant for backup retention; destination has independent schedul  │
│    MirrorAndVault     = policy combining SnapMirror DR and SnapVault backup retention copies          │
│    Fanout             = single source volume replicating to multiple destination clusters simultaneo  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Run `snapmirror show -fields state,healthy,lag-time` for relationship status.
- `snapmirror show -fields last-transfer-error` gives the last failure reason.
- Intercluster LIF connectivity (ports 11104/11105) is the most common root cause.

## Relationship Errors

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `SnapMirror: Source not reachable` | ONTAP 9.x | Cluster peering broken or intercluster LIF unreachable | Verify cluster peer: `cluster peer show`; check 11104/11105 between intercluster LIFs | N/A |
| Relationship stuck in `Transferring` for >24 hours | ONTAP 9.x | Network bandwidth saturated or network interruption | Abort transfer: `snapmirror abort`; resume when bandwidth available | N/A |
| `Destination is busy` during update | ONTAP 9.x | Concurrent SnapMirror operations on same destination volume | Stagger SnapMirror schedules to avoid concurrent transfers to same destination | N/A |
| `Snapshot not found` on destination after truncation | ONTAP 9.x | Destination's common Snapshot deleted | Run `snapmirror resync` to re-establish baseline; full transfer required | N/A |

## Initialization

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Initial baseline transfer failing midway | ONTAP 9.x | Network interruption during large initial transfer | Transfer restarts from last checkpoint; no data re-sent | N/A |
| `Cluster peer not authenticated` | ONTAP 9.x | Peer relationship deleted on one side | Delete and re-create cluster peer on both sides using `cluster peer create` | N/A |

## SnapMirror to Cloud

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `S3 endpoint unreachable` | ONTAP 9.12+ | ONTAP cluster cannot reach S3 endpoint (port 443) | Verify outbound 443 from cluster management LIF to S3 endpoint FQDN | N/A |
| `Invalid credentials for cloud target` | ONTAP 9.x | S3 access key or secret key incorrect | Update cloud target credentials: `snapmirror cloud target modify` | N/A |

## See also

- [NetApp SnapMirror — Common Issues](common-issues/)
- [NetApp ONTAP — Known Issues](../../ontap/troubleshooting/known-issues.md)
- [NetApp SnapCenter — Known Issues](../../snapcenter/troubleshooting/known-issues.md)
