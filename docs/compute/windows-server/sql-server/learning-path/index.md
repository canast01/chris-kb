# SQL Server — Learning Path

<div class="kb-summary">
Recommended reading order for SQL Server on Windows. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌───────────────────────────────────── SQL Server — Learning Path ──────────────────────────────────────┐
│                                                                                                       │
│    5 stages in order: Architecture → Deploy → Operations → Security → Troubleshoot                    │
│                                                                                                       │
│   ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│   │  Architecture  │  │     Deploy     │  │    Operations   │  │    Security    │  │  Troubleshoot  │ │
│   │                │  │                │  │                 │  │                │  │                │ │
│   │  How It Works  │  │ Initial Setup  │  │  Health Checks  │  │ Access Control │  │ Common Issues  │ │
│   │Design Standards│  │Install/Upgrade │  │  CLI Reference  │  │ Authentication │  │  Diagnostics   │ │
│   │  Integrations  │  │                │  │    Procedures   │  │   Encryption   │  │   Escalation   │ │
│   │                │  │                │  │ Backup & Restore│  │   Hardening    │  │                │ │
│   │                │  │                │  │     Scripts     │  │                │  │                │ │
│   └────────────────┘  └────────────────┘  └─────────────────┘  └────────────────┘  └────────────────┘ │
│                                                                                                       │
│    Stage 1 (Architecture) builds understanding. Stage 3 (Operations) is daily work. Troubleshoot last.│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```
| Stage | Focus | Time investment |
|-------|-------|----------------|
| 1 — Architecture | SQLOS, buffer pool, WAL, Always On AG | 5–6 h |
| 2 — Deployment | Installation baseline, tempdb, AG wizard | 3–4 h |
| 3 — Operations | AG health, job monitoring, index maintenance | ongoing |
| 4 — Security | Logins, TDE, Always Encrypted, SQL Audit | 3–4 h |
| 5 — Troubleshooting | Query Store, Extended Events, deadlocks, CHECKDB | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand SQL Server's memory, I/O, and transaction log architecture, and how Always On Availability Groups provide HA and DR without shared storage.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — SQL Server process architecture (SQLOS scheduler model, worker threads, memory management with `max server memory`, buffer pool for data page cache), the write-ahead logging (WAL) protocol (`CHECKPOINT` and log truncation), transaction log VLF (virtual log file) structure, and how the log is reused after backup
- [Design Standards](../architecture/design-standards/) — instance vs database isolation decisions (multiple instances add complexity; multiple databases per instance is preferred), `tempdb` file count = number of logical CPU cores (up to 8), data/log/`tempdb` volume separation onto different disks for I/O isolation, AG replica placement (sync for HA, async for DR), and maintenance window design for index rebuilds and CHECKDB
- [Integrations](../architecture/integrations/) — Windows Server Failover Clustering (WSFC) as the underlying HA framework for AG, SQL Server Agent for job scheduling (backups, index maintenance, integrity checks), SSRS for report delivery, and linked server configuration for cross-instance queries

**Key concepts before moving on**:

- `max server memory` must be set — leaving it at default allows SQL Server to consume all OS RAM, causing the OS and other processes to page to disk
- The transaction log does not shrink automatically — it grows to accommodate the largest transaction ever seen and only truncates (not shrinks) after a log backup
- An AG primary synchronises log records to secondaries; a synchronous secondary confirms before the primary acknowledges the commit — network latency directly impacts write throughput on sync replicas
- `tempdb` contention is a common bottleneck on high-concurrency workloads — multiple `tempdb` data files with `AUTOGROWTH` disabled and equal initial sizes are the fix

**Why first**: SQL Server configuration choices — `max server memory`, MAXDOP, `tempdb` layout, AG synchronisation mode — are set at installation time and affect every query. Get them right before the first database is created.

---

## Stage 2 — Deployment

**Goal**: Install SQL Server with a correct baseline configuration and a working Always On AG before accepting application databases.

**Read**:

- [Deploy](../deploy/) — pre-installation checklist (Windows power plan = High Performance, instant file initialisation grant, lock pages in memory, disk partitioning — 64KB allocation unit for data volumes), SQL Server installation wizard configuration (instance name, collation, service accounts as gMSA, `tempdb` file count and size), and AG creation via the Availability Group Wizard (WSFC prerequisite, endpoint creation, listener creation)
- [Install & Upgrade](../operations/install-upgrade/) — cumulative update (CU) installation procedure (install on secondary → failover → install on old primary), major version in-place upgrade, and AG rolling upgrade sequence to maintain HA throughout

**Deployment principles**:

- Use group Managed Service Accounts (gMSA) for SQL Server Engine and Agent service accounts — they rotate passwords automatically and do not require a password in service configuration
- Set `MAXDOP` to match your workload type: OLTP workloads prefer lower MAXDOP (2–4); DSS/analytics workloads can use higher values up to the physical core count per NUMA node
- Disable `AUTO_CLOSE` on all user databases — it causes repeated database open/close cycles and degrades performance on busy servers

---

## Stage 3 — Operations

**Goal**: Keep SQL Server healthy — monitoring AG state, job success, index fragmentation, and query performance on every shift.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; AG dashboard in SSMS (synchronisation state, log send/redo queue), SQL Agent job failure review (`msdb.dbo.sysjobhistory`), database online status (`SELECT name, state_desc FROM sys.databases`), blocking query check (`sys.dm_exec_requests WHERE blocking_session_id <> 0`), and disk free space on data/log/`tempdb` volumes
- [CLI Reference](../operations/cli-reference/) — T-SQL DMV queries (`sys.dm_exec_*`, `sys.dm_os_*`, `sys.dm_hadr_*`), `sqlcmd -S server -Q "SELECT @@VERSION"`, `bcp` for bulk data export/import, `sqlpackage` for DACPAC deployment, `Invoke-Sqlcmd` PowerShell cmdlet, and SSMS key workflows (Activity Monitor, Query Store dashboard, AG Dashboard)
- [Procedures](../operations/procedures/) — AG planned manual failover (`ALTER AVAILABILITY GROUP [AG] FAILOVER`), index rebuild/reorganise job management (Ola Hallengren solution), Query Store activation and forced plan management, database file pre-growth to avoid auto-growth events, and SQL Agent job creation and scheduling
- [Backup & Restore](../operations/backup-restore/) — full backup weekly → differential daily → log backup every 15–30 minutes; `COPY_ONLY` for ad-hoc restores without breaking the differential chain; log shipping as secondary DR; and restore sequence with `NORECOVERY` / `RECOVERY` and point-in-time (`STOPAT`)
- [Scripts](../operations/scripts/) — blocking query alert script (threshold-based), AG synchronisation health DMV dashboard, index fragmentation report, Ola Hallengren maintenance plan alternative, and backup verification (`RESTORE VERIFYONLY`) script

**Daily rhythm**: AG dashboard → SQL Agent job failures → blocking queries → disk space on all volumes → backup chain verification.

---

## Stage 4 — Security

**Goal**: Enforce least-privilege SQL access, protect data at rest and in transit, and audit all privileged database operations.

**Read**:

- [Access Control](../security/access-control/) — SQL Server login vs database user model (Windows login preferred over SQL login), fixed server roles (`sysadmin`, `securityadmin`, `dbcreator`) and fixed database roles (`db_datareader`, `db_datawriter`, `db_owner`), schema-based permission grants (`GRANT SELECT ON SCHEMA::dbo TO [app_user]`), and Row-Level Security (RLS) for multi-tenant data isolation
- [Authentication](../security/authentication/) — Windows Authentication (Kerberos) vs SQL Authentication (`Mixed Mode` — avoid SQL logins for human accounts), group Managed Service Account (gMSA) for SQL Server services, Contained Database Authentication for portable databases, and SQL Server Audit for authentication event logging
- [Encryption](../security/encryption/) — Transparent Data Encryption (TDE) for database files and backups at rest, Always Encrypted for column-level encryption with client-side key management (application cannot see plaintext on the server), TLS for client connections (disable TLS 1.0/1.1 via `Protocols` in SQL Server Configuration Manager), and SQL Server Audit to a Windows Security log or file target
- [Hardening](../security/hardening/) — Surface Area Configuration (disable `xp_cmdshell`, CLR integration, OLE Automation, Ad Hoc Distributed Queries unless required), renaming the `sa` account and disabling it, enabling C2 audit mode or SQL Server Audit for compliance, `TRUSTWORTHY OFF` on all user databases, and firewall rules allowing only port 1433 from known application server IPs

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose query performance regressions, blocking chains, AG failover events, and data corruption without data loss or extended downtime.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — AG secondary not synchronising (log send queue growing, network bandwidth, or secondary disk I/O), blocking chain causing application timeout (identify head blocker with `sys.dm_exec_requests`), plan regression after statistics update (use Query Store to force last known good plan), `tempdb` version store contention (`-1204` and `1105` errors), and database in `SUSPECT` mode after unclean shutdown
- [Diagnostics](../troubleshooting/diagnostics/) — Query Store plan comparison (identify plan change date and force previous plan), Extended Events session for blocking (system_health session captures deadlocks by default), `sys.dm_os_wait_stats` for top wait types since last restart, `DBCC CHECKDB WITH NO_INFOMSGS, ALL_ERRORMSGS` for consistency checking, and SQL Server error log review (`xp_readerrorlog` or SSMS)
- [Escalation](../troubleshooting/escalation)] — Microsoft CSS case creation with `SQLDiag` or PSSDiag output (generates comprehensive diagnostic package), SQL Nexus for automated performance analysis of PSSDiag data, `DBCC PAGE` and `DBCC IND` for page-level corruption investigation, and data recovery specialists for beyond-repair `.mdf` / `.ndf` page corruption

**Why last**: Troubleshooting makes most sense once you understand the buffer pool, transaction log lifecycle, AG log streaming, and what healthy wait statistics and query plan reuse look like on your specific workload.
