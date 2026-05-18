# Database

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Database Platform Overview                        │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│  │  SQL Server  │  │   Oracle     │  │  PostgreSQL  │                │
│  │  Always On   │  │  Data Guard  │  │  Patroni     │                │
│  │  AG (HA)     │  │  RAC / DG    │  │  Streaming   │                │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                │
│         │                 │                  │                       │
│  ┌──────▼─────────────────▼─────────────────▼────────────────────┐   │
│  │              Shared Infrastructure                            │   │
│  │  Storage: FlashArray / PowerMax / PowerScale (NFS/SMB)        │   │
│  │  Backup: Veeam / NetBackup with VSS / RMAN / pg_dump          │   │
│  │  Monitoring: Aria Ops / custom exporters / slow query logs    │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │  Config repository: version-controlled baseline configs    │      │
│  │  my.cnf · postgresql.conf · sqlserver.conf · init.ora     │       │
│  └────────────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────────────┘
```

Operational references for database health, maintenance, and troubleshooting.

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="database-backup-validation/"><strong>Backup Validation</strong><span>Verifying database backups are complete, consistent, and restorable.</span></a>
<a class="kb-card" href="database-capacity-monitoring/"><strong>Capacity Monitoring</strong><span>Tracking database growth, tablespace usage, log space, and forecasting expansion needs.</span></a>
<a class="kb-card" href="database-failover/"><strong>Failover</strong><span>Planned and unplanned database failover procedures for SQL Server, Oracle, and PostgreSQL.</span></a>
<a class="kb-card" href="database-health-check/"><strong>Health Check</strong><span>Daily database health checks — connections, blocking, long-running queries, and error logs.</span></a>
<a class="kb-card" href="database-maintenance/"><strong>Maintenance</strong><span>Index rebuilds, statistics updates, log truncation, and scheduled maintenance tasks.</span></a>
<a class="kb-card" href="database-performance-troubleshooting/"><strong>Performance Troubleshooting</strong><span>Diagnosing slow queries, blocking chains, lock contention, and I/O bottlenecks.</span></a>
<a class="kb-card" href="database-replication-check/"><strong>Replication Check</strong><span>Verifying replication lag, sync state, and replica health for HA database configurations.</span></a>
</div>
