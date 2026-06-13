---
tags:
  - linux
---
# PostgreSQL

<div class="kb-summary">
PostgreSQL open-source object-relational database — MVCC, streaming replication, autovacuum.
</div>

```text
┌───────────────────────────────────────────── PostgreSQL ──────────────────────────────────────────────┐
│                                                                                                       │
│   Open-source object-relational database; widely used for OLTP, analytics, and platform services      │
│   MVCC concurrency model: readers never block writers; each transaction sees a consistent snapshot    │
│   Streaming replication + Patroni: standard HA pattern for production deployments                     │
│                                                                                                       │
│   Sections in this guide                                                                              │
│   Architecture: process model (postmaster/backend), MVCC, WAL, replication topologies                 │
│   Deploy: installation, PostgreSQL + PgBouncer + Patroni stack setup                                  │
│   Operations: health checks, CLI reference, backup/restore, install and upgrade procedures            │
│   Security: access control (pg_hba.conf), authentication (scram-sha-256), encryption, hardening       │
│   Troubleshooting: common issues, diagnostics (pg_stat_*), escalation thresholds                      │
│                                                                                                       │
│   Key terms:                                                                                          │
│   postmaster    = supervisor process; forks one backend per client connection                         │
│   MVCC          = Multi-Version Concurrency Control; old row versions kept for snapshot reads         │
│   WAL           = Write-Ahead Log; durability mechanism and replication source                        │
│   Patroni       = Python HA template using etcd/Consul for leader election and failover               │
│   PgBouncer     = lightweight connection pooler; sits between application and PostgreSQL              │
│   autovacuum    = background process that removes dead tuples and updates planner statistics          │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">
  <a class="kb-card" href="architecture/">Architecture</a>
  <a class="kb-card" href="deploy/">Deploy</a>
  <a class="kb-card" href="operations/">Operations</a>
  <a class="kb-card" href="security/">Security</a>
  <a class="kb-card" href="troubleshooting/">Troubleshooting</a>
</div>
