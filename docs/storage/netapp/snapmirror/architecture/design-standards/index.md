# SnapMirror — Standards


<div class="kb-summary">
> Part of the [SnapMirror Architecture](../index.md) reference.
</div>
```
┌────────────────────────── NetApp SnapMirror — Architecture Design Standards ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     SnapMirror design standards: network isolation, redundancy, sizing, naming conventions    │   │
│   │          Network: dedicated storage VLAN; jumbo frames for iSCSI; dual-fabric for FC          │   │
│   │          Redundancy: dual controllers, multipath I/O, and no single points of failure         │   │
│   │       Monitoring: set capacity and latency alerts; baseline performance after deployment      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Requirements → architecture design → redundancy review → size → deploy                             │
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
│    Update             = incremental transfer; only sends new or changed blocks since last successfu...│
│    Snapmirror break   = breaks the DR relationship; activates destination volume for read-write       │
│    Resync             = re-establishes a broken SnapMirror relationship from the last common snapshot │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN volumes│
│    Mediator           = ONTAP Mediator; quorum service for SM-BC running on Linux VM at third site    │
│    SnapVault          = SnapMirror variant for backup retention; destination has independent schedule │
│    MirrorAndVault     = policy combining SnapMirror DR and SnapVault backup retention copies          │
│    Fanout             = single source volume replicating to multiple destination clusters simultane...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Naming Conventions

| Object | Pattern | Example |
|---|---|---|
| SnapMirror policy | `sm-<type>-<retention>` | `sm-async-daily`, `sm-xdp-weekly` |
| Relationship label | `<frequency>` | `hourly`, `daily`, `weekly` |
| Destination volume | `<source_vol>_dr` or `<source_vol>_vault` | `vol_app01_dr`, `vol_app01_vault` |
| Intercluster LIF | `ic-<node>-<port>` | `ic-node01-e0e` |
| Cluster peer | `<site1>-<site2>` | `prod-dr` |

## Replication Policy Baseline

- All Tier-1 production volumes must have an active SnapMirror relationship; no Tier-1 volume may be unprotected
- RPO must be documented per application and aligned with the SnapMirror schedule configured for that volume
- SnapMirror schedule (transfer frequency) must be set to achieve the documented RPO with margin — schedule at twice the frequency of the RPO where bandwidth allows
- XDP relationships with `MirrorAndVault` policy are preferred for DR volumes that also require independent snapshot retention on the destination
- Consistency groups (CGs) must be used for multi-volume workloads (database data + log volumes) to ensure crash-consistent replication across related volumes
- SnapMirror Sync or SMBC required for Tier-0 workloads where zero data loss is a hard requirement

## Configuration Checklist

- [ ] Cluster peer relationship established between source and destination clusters
- [ ] SVM peer relationship established between source and destination SVMs
- [ ] Intercluster LIFs configured on a dedicated replication network (separate from data traffic)
- [ ] Destination volume created as type DP (not RW) with equal or greater size than source
- [ ] SnapMirror policy created with correct rules, schedule, and retention settings
- [ ] Relationship created with `snapmirror create` specifying correct `-type` (XDP for async, StrictSync/Sync for synchronous)
- [ ] Baseline transfer completed with `snapmirror initialize` and confirmed healthy
- [ ] Lag monitoring alert configured in ONTAP EMS (`snapmirror.lag.warn` threshold set per RPO)
- [ ] Relationship documented with `-comment` field: owner, RPO tier, last DR test date
- [ ] DR test scheduled within 90 days of relationship creation
