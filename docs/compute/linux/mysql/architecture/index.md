# MySQL / MariaDB — Architecture

<div class="kb-summary">
Architecture overview, design standards, and integrations.
</div>

```text
┌─────────────────────────────────── MySQL — Architecture Reference ────────────────────────────────────┐
│                                                                                                       │
│   MySQL architecture: InnoDB storage engine, query processing pipeline, and replication topology      │
│   Three sub-sections: how it works, design standards, and integrations                                │
│   InnoDB is the default engine for all production use; MyISAM is legacy and not recommended           │
│                                                                                                       │
│   InnoDB internals                                                                                    │
│   Buffer pool: in-memory cache of pages; target hit rate >99% for OLTP workloads                      │
│   Redo log: write-ahead log ensuring crash recovery (innodb_log_file_size controls size)              │
│   Undo log: stores old row versions for MVCC; enables consistent reads and rollback                   │
│   Clustered index: primary key IS the table; row data stored in PK order on disk                      │
│                                                                                                       │
│   Query processing                                                                                    │
│   Parser → Optimizer → Execution engine → Storage engine (InnoDB) → Disk                              │
│   EXPLAIN shows index usage, join type, and estimated rows; use for slow query diagnosis              │
│   Query cache removed in 8.0; use ProxySQL or app-layer caching instead                               │
│                                                                                                       │
│   Replication                                                                                         │
│   Binary log (binlog) on primary; replica applies events via I/O thread + SQL thread                  │
│   GTID-based replication: each transaction has a unique ID; simplifies failover and consistency       │
│   Semi-sync: primary waits for replica ACK before commit; prevents data loss on primary failure       │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Buffer pool   = InnoDB in-memory page cache; most critical tuning parameter (60-80% of RAM)         │
│   MVCC          = Multi-Version Concurrency Control; readers don't block writers                      │
│   GTID          = Global Transaction Identifier; monotonically increasing per-server transaction ID   │
│   Clustered idx = InnoDB physical table layout; rows ordered by primary key on disk                   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">How It Works</a>
  <a class="kb-card" href="design-standards/">Design Standards</a>
  <a class="kb-card" href="integrations/">Integrations</a>
</div>
