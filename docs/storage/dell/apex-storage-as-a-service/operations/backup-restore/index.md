# APEX Storage as a Service — Backup & Restore

```text
┌──────────────────────────────── Dell Apex STaaS — Backup and Restore ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Apex backup: native snapshots, replication, and external backup target integration      │   │
│   │           Native snapshots: crash-consistent, scheduled; retained on the same array           │   │
│   │           Replication: async volume replication to secondary Apex or PowerStore site          │   │
│   │         External backup: PowerProtect DD, Avamar, or third-party via NFS/iSCSI backup         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Snapshot (local) → replication (remote) → backup target → test restore quarterly                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Snapshots          │  │         Replication         │  │       External Backup       │   │
│   │       Crash-consistent      │  │         Async remote        │  │        PowerProt. DD        │   │
│   │        App-consistent       │  │         RPO minutes         │  │            Avamar           │   │
│   │       Scheduled policy      │  │        Failover test        │  │         Third-party         │   │
│   │       Retention rules       │  │         Reverse sync        │  │          NFS mount          │   │
│   │        Clone restore        │  │        Site failback        │  │         iSCSI target        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Test restores quarterly; document RTO/RPO; keep one restore tested per critical volume             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Method      │       RPO        │        RTO        │      Where       │      Notes       │   │
│   │     Snapshot     │  Sched (hours)   │      Minutes      │    Same array    │   No off-site    │   │
│   │   Replication    │     Minutes      │    Minutes/hrs    │   Remote site    │    Async lag     │   │
│   │    DD backup     │      Hours       │       Hours       │   DD appliance   │   Dedup ratio    │   │
│   │   App-consist.   │   Transaction    │      Minutes      │   VSS/quiesce    │   Agent needed   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: secondary Apex or PowerStore at DR site · DD appliance on-premises or hosted             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Crash-consistent = Snapshot taken without quiescing I/O; suitable for block volumes                │
│    App-consistent   = Snapshot taken with application quiesce (VSS/freeze); DB-safe                   │
│    Async replication = Volume data replicated after write commit; lag = RPO in minutes                │
│    RPO              = Recovery Point Objective; maximum acceptable data loss time                     │
│    RTO              = Recovery Time Objective; maximum acceptable restore duration                    │
│    Reverse sync     = After failover, sync changes back to primary to prepare failback                │
│    DD Boost         = Dell Data Domain protocol; deduplication-aware backup streams                   │
│    Retention policy = How many snapshots to keep; older ones auto-deleted when count met              │
│    Clone restore    = Create writable clone of snapshot; use as restored volume                       │
│    VSS              = Volume Shadow Copy Service; Windows app-consistent snapshot mechanism           │
│    Dedup ratio      = DD data reduction ratio; typically 20:1 to 55:1 for backup data                 │
│    Failback         = Return primary workload to original site after DR failover resolves             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [APEX Storage as a Service](../../index.md) reference.

---

Data backup on APEX STaaS is the customer's responsibility using the same backup solutions as for any other storage platform (e.g., PowerProtect Data Manager, Avamar, Networker). Dell manages the hardware and infrastructure layer only.

Key items to document and protect:

- **APEX API credentials**: store client ID and client secret in a secrets vault; cannot be retrieved after creation
- **Subscription records**: retain documentation of subscription ID, committed tier, burst ceiling, contract dates, and SLA tier
- **Monthly usage exports**: export APEX Console billing data monthly and retain for billing reconciliation
