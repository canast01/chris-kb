---
tags:
  - architecture
  - linux
---
# PostgreSQL — How It Works

<div class="kb-summary">
PostgreSQL architecture — process model, shared buffer cache, WAL, MVCC, autovacuum, streaming replication, and query planner internals.

*Applies to: PostgreSQL 15.x / 16.x*
</div>

```text
┌────────────────────────────────────── Compute Linux Postgresql ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Linux: Compute Linux Postgresql platform                           │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Compute Linux Postgresql management console                    │   │
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
│    Physical: Compute Linux Postgresql infrastructure · management network · monitoring                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Linux              = Compute Linux Postgresql platform overview and core concepts                  │
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


## Process Model

PostgreSQL uses a multi-process model (not multi-threaded):

| Process | Role |
|---|---|
| `postgres` (postmaster) | Listener; spawns backend for each connection |
| Backend | One per client connection; handles queries |
| `autovacuum` | Cleans dead tuples; updates stats; runs on schedule |
| `walwriter` | Flushes WAL buffers to disk |
| `bgwriter` | Writes dirty shared buffer pages to disk |
| `checkpointer` | Periodic checkpoint: flush all dirty pages, advance WAL recovery point |
| `wal sender` | Sends WAL to streaming replicas |
| `wal receiver` | Receives WAL on replica |

## Shared Buffer Cache

`shared_buffers` is the in-memory page cache. Set to 25% of RAM (OS page cache handles the rest via `effective_cache_size`). Access path:

```text
Query → shared_buffers (hit?) → OS page cache → disk
```

## WAL (Write-Ahead Log)

All changes are written to WAL before data files:
- WAL files in `pg_wal/` — each 16 MB by default
- `wal_level`: `minimal` / `replica` / `logical` — must be `replica` for streaming
- `archive_mode=on` + `archive_command` → PITR

## MVCC and Autovacuum

PostgreSQL uses MVCC: old row versions remain until vacuumed. Dead tuples accumulate and cause table bloat. `autovacuum` reclaims space and updates planner statistics.

```sql
-- Check table bloat / dead tuples
SELECT relname, n_dead_tup, n_live_tup, last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC LIMIT 10;
```

## Key Configuration Parameters

| Parameter | Default | Notes |
|---|---|---|
| `shared_buffers` | 128MB | Set to 25% of RAM |
| `effective_cache_size` | 4GB | Hint to planner; set to 75% of RAM |
| `work_mem` | 4MB | Per-sort/hash; multiply by max_connections for total |
| `maintenance_work_mem` | 64MB | For VACUUM, CREATE INDEX; set to 1–2 GB |
| `max_connections` | 100 | Each connection ~5–10 MB RAM |
| `wal_level` | replica | Must be `replica` for streaming replication |

---

## See also

- [Postgresql — Design Standards](design-standards/)
- [Postgresql — Integrations](integrations/)
- [Postgresql — Deploy](../deploy/)
