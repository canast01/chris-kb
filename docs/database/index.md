# Database


<div class="kb-summary">
Operational references for database health, maintenance, and troubleshooting.
</div>

```powershell
┌────────────────────────── Database — Health, Backup, Failover & Performance ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Database operational references: PostgreSQL, MySQL/MariaDB, and SQL Server procedures     │   │
│   │    Covers: daily health checks, backup validation, planned/unplanned failover, maintenance    │   │
│   │      Performance: slow query diagnosis, blocking chains, lock contention, I/O bottlenecks     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Monitor → Backup → Maintain → Capacity plan → Troubleshoot → Failover                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Health & Monitoring     │  │      Backup & Recovery      │  │         Performance         │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      Connection counts      │  │     Job completion check    │  │        Slow query log       │   │
│   │      Blocking/deadlocks     │  │     Restore verification    │  │        EXPLAIN / AWR        │   │
│   │      Long-running txns      │  │       Replication lag       │  │       Lock contention       │   │
│   │       Error log review      │  │      Failover procedure     │  │       I/O bottlenecks       │   │
│   │       Capacity alerts       │  │     Maintenance windows     │  │        Index rebuild        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    WAL          = Write-Ahead Log (PostgreSQL); transaction log; used for replication and PITR        │
│    Always On AG = SQL Server availability group; synchronous replica; automatic failover capable      │
│    RMAN         = Oracle Recovery Manager; backup and restore tool for Oracle databases               │
│    pgBackRest   = PostgreSQL backup tool; supports full/diff/incr; WAL archiving and PITR             │
│    AWR          = Automatic Workload Repository (Oracle); performance snapshot repository             │
│    PITR         = Point-In-Time Recovery; restore DB to a specific moment using WAL/log replay        │
│    Blocking     = Query holding locks that other queries are waiting on; degrades throughput          │
│    TDE          = Transparent Data Encryption; encrypts DB files at rest; transparent to app          │
│    Deadlock     = Two transactions each waiting for the other to release locks; DB auto-kills one     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="database-backup-validation/"><strong>Backup Validation</strong><span>Verifying database backups are complete, consistent, and restorable.</span></a>
<a class="kb-card" href="database-capacity-monitoring/"><strong>Capacity Monitoring</strong><span>Tracking database growth, tablespace usage, log space, and forecasting expansion needs.</span></a>
<a class="kb-card" href="database-failover/"><strong>Failover</strong><span>Planned and unplanned database failover procedures for SQL Server, Oracle, and PostgreSQL.</span></a>
<a class="kb-card" href="database-health-check/"><strong>Health Check</strong><span>Daily database health checks — connections, blocking, long-running queries, and error logs.</span></a>
<a class="kb-card" href="database-maintenance/"><strong>Maintenance</strong><span>Index rebuilds, statistics updates, log truncation, and scheduled maintenance tasks.</span></a>
<a class="kb-card" href="database-performance-troubleshooting/"><strong>Performance Troubleshooting</strong><span>Diagnosing slow queries, blocking chains, lock contention, and I/O bottlenecks.</span></a>
<a class="kb-card" href="database-replication-check/"><strong>Replication Check</strong><span>Verifying replication lag, sync state, and replica health for HA database configurations.</span></a>
</div>
