---
tags:
  - troubleshooting
  - postgresql
  - linux
  - known-issues
---
# PostgreSQL — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known PostgreSQL bugs, error codes, and workarounds covering connectivity, replication, vacuum, and Patroni HA.

*Applies to: PostgreSQL 15.x / 16.x*
</div>

```text
┌───────────────────────────────────────────── PostgreSQL ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Relational DB — MVCC, streaming replication, extensible, Patroni HA              │   │
│   │                         Protocols: PostgreSQL wire protocol (TCP 5432)                        │   │
│   │                     Management: psql CLI / pgAdmin / Patroni REST API (HA)                    │   │
│   │             Client connect -> pg_hba.conf check -> Query planner -> Storage -> WAL            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │         Concurrency         │  │             MVCC            │  │  Readers never block writes │   │
│   │         Replication         │  │       Streaming (WAL)       │  │        Async or sync        │   │
│   │              HA             │  │        Patroni + etcd       │  │      Automated failover     │   │
│   │         Maintenance         │  │          Autovacuum         │  │     Reclaims dead tuples    │   │
│   │          Extensions         │  │      pg_stat_statements     │  │      Query perf insight     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │     postgres     │ DB server proc.  │      TCP 5432     │   pg_hba rules   │ One per cluster  │   │
│   │       WAL        │ Write-Ahead Log  │      Internal     │       N/A        │ Basis for repl.  │   │
│   │     Patroni      │ HA orchestration │     REST 8008     │       N/A        │Needs etcd quorum │   │
│   │     pg_dump      │  Logical backup  │        N/A        │     DB user      │  Per-DB export   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: DB server host(s) - WAL storage - standby replicas - etcd cluster                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  MVCC           = Multi-Version Concurrency Control; readers never block writers                      │
│  WAL            = Write-Ahead Log; basis for replication and crash recovery                           │
│  Autovacuum     = background process reclaiming space from dead rows                                  │
│  TXID wraparound= critical failure if vacuum falls badly behind                                       │
│  Patroni        = open-source HA template managing automatic failover                                 │
│  pg_stat_activity = view of current connections and running queries                                   │
│  Replication slot = reserves WAL on primary so replica retains segments                               │
│  pg_hba.conf    = host-based auth rules controlling who can connect                                   │
│  Logical repl.  = row-level replication, can target a subset of tables                                │
│  Checkpoint     = periodic dirty-buffer flush, reduces crash recovery time                            │
│  VACUUM FREEZE  = aggressive vacuum preventing transaction ID wraparound                              │
│  HAProxy check  = routes traffic only to the current Patroni primary                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- PostgreSQL logs: `/var/log/postgresql/postgresql-*.log` or via `journalctl -u postgresql`.
- `pg_activity` or `SELECT * FROM pg_stat_activity` for active query monitoring.
- Autovacuum issues are the most common silent performance degrader — check `pg_stat_user_tables`.

## Connectivity

| Error Code | Description | Cause | Fix |
|---|---|---|---|
| `FATAL: password authentication failed` | Wrong password or `pg_hba.conf` rejects method | Verify `pg_hba.conf` allows connection method (md5/scram); check password | N/A |
| `FATAL: no pg_hba.conf entry for host` | Client IP not in `pg_hba.conf` | Add client IP/subnet to `pg_hba.conf`; `pg_reload_conf()` | N/A |
| `could not connect to server: Connection refused` | PostgreSQL not listening on TCP | Check `listen_addresses` in `postgresql.conf`; restart if changed | N/A |

## Replication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Streaming replica lag growing | PostgreSQL 15/16 | WAN bandwidth or primary write rate too high | Increase `wal_keep_size`; consider `pg_logical` for more efficient replication | N/A |
| `replication slot inactive` consuming WAL | PostgreSQL 15/16 | Replica connected to slot dropped; slot not cleaned up | Drop unused slot: `SELECT pg_drop_replication_slot('slot_name')` | N/A |

## Vacuum / Bloat

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Table bloat growing rapidly | All | Autovacuum not keeping up with DELETE/UPDATE rate | Run manual `VACUUM ANALYZE <table>`; increase `autovacuum_vacuum_cost_delay` | N/A |
| `Transaction ID wraparound` warning | All | Autovacuum not processing table within 2B transactions | Run emergency `VACUUM FREEZE <table>` immediately | N/A |

## Patroni HA

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Patroni cluster `No Leader` after split-brain | Patroni 3.x | etcd quorum lost; all nodes in follower state | Restore etcd quorum; or use `patronictl failover --force <cluster> <node>` | N/A |
| HAProxy not routing to primary | Patroni 3.x | HAProxy health check not detecting new primary after failover | Restart HAProxy; verify Patroni REST API (port 8008) responds with primary status | N/A |

## See also

- [PostgreSQL — Common Issues](common-issues.md)
- [Linux — Known Issues](../../troubleshooting/known-issues/)
