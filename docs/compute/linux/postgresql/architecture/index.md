# PostgreSQL — Architecture

<div class="kb-summary">
Architecture overview, design standards, and integrations.
</div>

![PostgreSQL Architecture Overview](../../../../assets/postgresql-architecture-overview.svg)

```text
┌───────────────────────────────── PostgreSQL — Architecture Reference ─────────────────────────────────┐
│                                                                                                       │
│   PostgreSQL process model: one backend process per client connection; postmaster is the supervisor   │
│   WAL-based replication: standby continuously replays WAL segments from primary                       │
│   MVCC: old row versions (dead tuples) accumulate; autovacuum reclaims space and updates statistics   │
│                                                                                                       │
│   Process model                                                                                       │
│   postmaster: parent process; forks a backend per client; manages shared memory init                  │
│   backend (postgres): handles one client session; separate address space; dies cleanly on crash       │
│   autovacuum launcher: spawns autovacuum workers to VACUUM and ANALYZE tables                         │
│   bgwriter: flushes dirty pages from shared_buffers to disk in the background                         │
│                                                                                                       │
│   Storage and MVCC                                                                                    │
│   Heap files: table data stored in 8 KB pages; each row version (tuple) is kept for MVCC              │
│   Dead tuples: old row versions not visible to any transaction; removed by VACUUM                     │
│   TOAST: large values (>2 KB) compressed and stored in a side table automatically                     │
│   pg_wal: WAL segment directory; each segment is 16 MB; base for replication and crash recovery       │
│                                                                                                       │
│   Replication                                                                                         │
│   Physical (streaming): byte-identical copy of WAL; standby is read-only replica                      │
│   Logical replication: row-level changes decoded from WAL; selective table replication                │
│   Synchronous: primary waits for standby WAL write before reporting commit success                    │
│                                                                                                       │
│   Key terms:                                                                                          │
│   WAL          = Write-Ahead Log; durability mechanism and replication source                         │
│   MVCC         = Multi-Version Concurrency Control; readers see snapshot, not live data               │
│   VACUUM        = cleans dead tuples; required to prevent table bloat and XID wraparound              │
│   TOAST         = The Oversized-Attribute Storage Technique; handles large column values              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">How It Works</a>
  <a class="kb-card" href="design-standards/">Design Standards</a>
  <a class="kb-card" href="integrations/">Integrations</a>
</div>
