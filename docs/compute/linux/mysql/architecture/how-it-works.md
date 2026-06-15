---
tags:
  - architecture
  - linux
---
# MySQL / MariaDB — How It Works

<div class="kb-summary">
MySQL architecture — InnoDB storage engine, buffer pool, query execution pipeline, redo/undo logs, replication binlog, and connection threading model.

*Applies to: MySQL 8.x · MariaDB 10.x*
</div>

```text
┌───────────────────────────────────────── Compute Linux Mysql ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Linux: Compute Linux Mysql platform                              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                       Management: Compute Linux Mysql management console                      │   │
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
│    Physical: Compute Linux Mysql infrastructure · management network · monitoring                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Linux              = Compute Linux Mysql platform overview and core concepts                       │
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


## Storage Engine: InnoDB

InnoDB is the default storage engine. Key components:

| Component | Role |
|---|---|
| Buffer pool | In-memory cache of data and index pages; target 70–80% of available RAM |
| Redo log (iblogfile) | Write-ahead log for crash recovery; circular; controlled by `innodb_log_file_size` |
| Undo log | Stores old row versions for MVCC and rollback |
| Change buffer | Caches secondary index changes when the index page is not in buffer pool |
| Doublewrite buffer | Prevents partial-page writes on crash; enabled by default |

## Query Execution Pipeline

```text
Client → Connection thread → Parser → Optimizer → Storage engine
         (thread cache)       (SQL)    (query plan)  (InnoDB/MyISAM)
```

1. **Parse** — SQL tokenised, syntax validated
2. **Optimise** — cost-based query planner selects index access path
3. **Execute** — storage engine reads/writes pages via buffer pool
4. **Return** — result set sent to client; connection returned to thread cache

## Replication Architecture

MySQL replication is asynchronous by default:

```text
Primary: writes → binary log (binlog) → replica I/O thread reads binlog
Replica: relay log → SQL thread applies → committed to replica data files
```

- **GTID mode** (`gtid_mode=ON`) identifies transactions globally; simplifies failover
- **Semi-sync replication** (`rpl_semi_sync_master_enabled`) waits for at least one replica ACK before commit — reduces data loss on failover
- **Binlog format**: `ROW` preferred (deterministic); `STATEMENT` smaller but can diverge

## Key Configuration Parameters

| Parameter | Default | Notes |
|---|---|---|
| `innodb_buffer_pool_size` | 128M | Set to 70–80% of RAM |
| `innodb_log_file_size` | 48M | Larger = faster writes, slower recovery; 1–4 GB typical |
| `max_connections` | 151 | Each connection uses ~1 MB RAM |
| `innodb_flush_log_at_trx_commit` | 1 | `1` = full ACID; `2` = risk 1 sec data loss on crash |
| `sync_binlog` | 1 | `1` = binlog flushed per commit; safest |

## Transaction Isolation

InnoDB defaults to `REPEATABLE READ`. MVCC provides non-blocking reads by keeping old row versions in the undo log. Long-running transactions hold undo log space — watch `innodb_history_list_length`.

---

## See also

- [Mysql — Design Standards](design-standards/)
- [Mysql — Integrations](integrations/)
- [Mysql — Deploy](../deploy/)
