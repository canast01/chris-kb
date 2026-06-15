---
tags:
  - architecture
  - windows
---
# SQL Server — How It Works

<div class="kb-summary">
SQL Server architecture — database engine, buffer pool, transaction log, WAL-based crash recovery, Always On AG replication, and query processing pipeline.

*Applies to: SQL Server 2019 / 2022*
</div>

```text
┌────────────────────────────────── Compute Windows Server Sql Server ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                   Windows Server: Compute Windows Server Sql Server platform                  │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                Management: Compute Windows Server Sql Server management console               │   │
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
│    Physical: Compute Windows Server Sql Server infrastructure · management network · monitoring       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Windows Server     = Compute Windows Server Sql Server platform overview and core concepts         │
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


## Database Engine Components

| Component | Role |
|---|---|
| Buffer Manager | In-memory page cache (buffer pool); target 80–90% of available RAM |
| Transaction Log | Sequential WAL; all changes logged before data pages written |
| Lock Manager | Row/page/table locking; escalation to table lock at threshold |
| Query Processor | Parser → Algebrizer → Optimizer → Executor |
| SQL OS | Scheduler; worker threads; memory manager |

## Buffer Pool

- Pages (8 KB) loaded from disk into buffer pool on first access
- Dirty pages written by background `LazyWriter`; `CHECKPOINT` flushes all dirty pages
- `max server memory` — set to leave ~10 GB for OS; rest to SQL Server

## Transaction Log and Recovery

SQL Server uses Write-Ahead Logging (WAL):
1. Log record written to transaction log buffer
2. Log buffer flushed to disk on `COMMIT`
3. Data page written to disk asynchronously (lazy)
4. On crash: redo committed txns, undo uncommitted from log

Log files are reused in circular fashion after `CHECKPOINT` advances the log sequence number (LSN).

## Always On Availability Groups

```text
Primary → synchronous/asynchronous log shipping → Secondary (readable replica)
          ↓
     Listener (VIP) — routes app connections to current primary
```

- **Synchronous**: primary waits for secondary ACK — zero data loss; lower throughput
- **Asynchronous**: no wait — DR sites; potential data loss on failover

## Query Processing

```text
T-SQL Query → Parse → Bind (object resolution) → Optimize (execution plan) → Execute
                                                    ↓
                                            Plan Cache (reuse)
```

`sys.dm_exec_cached_plans` — view cached plans; `DBCC FREEPROCCACHE` — clear plan cache.

---

## See also

- [Sql Server — Design Standards](design-standards/)
- [Sql Server — Integrations](integrations/)
- [Sql Server — Deploy](../deploy/)
