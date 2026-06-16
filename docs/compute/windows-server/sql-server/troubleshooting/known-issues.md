---
tags:
  - troubleshooting
  - sql-server
  - windows-server
  - known-issues
---
# Microsoft SQL Server — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known SQL Server bugs, error codes, and workarounds covering connectivity, AG failover, blocking, and backup.

*Applies to: SQL Server 2019 / 2022*
</div>

```text
┌──────────────────────────────────────── Microsoft SQL Server ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Relational DB — Always On Availability Groups, TempDB, blocking analysis           │   │
│   │                     Protocols: TDS (TCP 1433) · Kerberos (SPN-based auth)                     │   │
│   │                         Management: SSMS / sqlcmd / Azure Data Studio                         │   │
│   │            Client connect -> SPN/auth -> Query -> Buffer pool -> Storage/AG replica           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Engine           │  │       Database Engine       │  │     sqlservr.exe process    │   │
│   │              HA             │  │         Always On AG        │  │     Sync/async replicas     │   │
│   │             Auth            │  │       Windows/SQL auth      │  │     SPN needed for Kerb.    │   │
│   │            TempDB           │  │       Shared system DB      │  │    1 file/core recommend    │   │
│   │           Locking           │  │         Lock manager        │  │    Blocking chains, DMVs    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    SQL Server    │    DB engine     │      TCP 1433     │   Windows/SQL    │   sqlservr.exe   │   │
│   │   AG listener    │ HA virtual endpt │      TCP 1433     │       N/A        │Moves w/ failover │   │
│   │      TempDB      │Temp object store │      Internal     │       N/A        │ PAGELATCH issues │   │
│   │       DMVs       │ Diagnostic views │        N/A        │     sysadmin     │ dm_exec_requests │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: SQL Server host(s) - Windows Failover Cluster - shared/local storage                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TDS            = Tabular Data Stream; SQL Server network wire protocol                               │
│  Always On AG   = Availability Group; databases replicated for HA                                     │
│  AG listener    = virtual name/IP that follows the current primary                                    │
│  SPN            = Service Principal Name; required for Kerberos auth                                  │
│  TempDB         = shared system DB for temp objects, sorts, versioning                                │
│  PAGELATCH      = contention on an in-memory page, often TempDB-related                               │
│  Blocking sess. = a session holding a lock another session waits on                                   │
│  WFC            = Windows Failover Cluster; underlies AG auto-failover                                │
│  Failover mode  = AG setting: automatic vs manual failover                                            │
│  dm_exec_requests= DMV showing currently executing requests/blocking                                  │
│  Double-hop     = Kerberos delegation issue acting on a remote resource                               │
│  Mirroring endpt= AG comms endpoint, default port 5022                                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- SQL Server errors appear in SQL Server Management Studio (SSMS) → Management → SQL Server Logs.
- Error log: `SELECT * FROM sys.fn_xe_file_target_read_file(...)` or view in SSMS.
- Most connectivity errors are port (1433) or authentication (Windows vs SQL auth mode) issues.

## Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Error 10061 `No connection could be made` | SQL 2019/2022 | SQL Server not listening or TCP 1433 blocked | Enable TCP in SQL Server Configuration Manager; allow 1433 in Windows Firewall | N/A |
| `Login failed for user NT AUTHORITY\ANONYMOUS LOGON` | SQL 2019/2022 | Kerberos double-hop issue; SPN not registered | Register SPN: `setspn -A MSSQLSvc/<host>:1433 <domain>\<svc-account>` | N/A |
| `Cannot open database requested by login` | All | Database offline or user not mapped to database | Bring database online; check user-database mapping in SSMS | N/A |

## Availability Groups

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| AG secondary shows `Not Synchronizing` | SQL 2019/2022 | Endpoint port 5022 blocked between AG replicas | Verify TCP 5022 between all replica nodes; check AG endpoint: `SELECT * FROM sys.database_mirroring_endpoints` | N/A |
| Automatic failover not triggering | SQL 2019/2022 | Failover mode not set to `Automatic` or health detection threshold too high | Set AG failover mode: `ALTER AVAILABILITY GROUP ... MODIFY REPLICA ... WITH (FAILOVER_MODE = AUTOMATIC)` | N/A |
| `AG listener not reachable` after failover | SQL 2019/2022 | Windows Failover Cluster VIP not responding | Check Windows Failover Cluster Manager → Networks; verify listener VIP moved to new primary | N/A |

## Performance

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| High blocking — `SPID waiting on LCK_M_X` | All | Long-running transaction holding lock | Identify blocker: `SELECT * FROM sys.dm_exec_requests WHERE blocking_session_id != 0` | N/A |
| TempDB contention (`PAGELATCH_EX`) | SQL 2019/2022 | TempDB data files too few for concurrent sessions | Add TempDB files: 1 per logical CPU core (up to 8) via `ALTER DATABASE tempdb ADD FILE` | N/A |

## See also

- [SQL Server — Common Issues](common-issues.md)
- [Windows Server — Known Issues](../../troubleshooting/known-issues/)
- [Active Directory — Known Issues](../../active-directory/troubleshooting/known-issues/)
