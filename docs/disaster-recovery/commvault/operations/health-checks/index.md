# Commvault — Health Checks


<div class="kb-summary">
Health Checks reference covering Daily Checklist, Weekly Checks.
</div>

```text
┌───────────────────────────── Commvault Health Checks — Daily and Weekly ──────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Daily Health Checks              │  │             Weekly Health Checks            │   │
│   │        Review overnight job failures         │  │          Run SLA compliance report          │   │
│   │         Check CommServe services up          │  │         Validate aux copy completion        │   │
│   │        Verify disk library free space        │  │      Check DDB health and fragmentation     │   │
│   │      Review alert emails for anomalies       │  │        Review library capacity trends       │   │
│   │       Check MA status (active/offline)       │  │       Verify DR CommServe sync status       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Health checks use Command Center dashboards, qlist CLI, and CommServe event log                    │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    CommServe Service Health                                   │   │
│   │        Check Windows services: CommVault Communications (GxCVD), Job Manager (GxJobMgr)       │   │
│   │          Check SQL Server: CSDB query response time < 2s; check for blocking queries          │   │
│   │                 Check CV log directory: disk < 80% full; rotate logs if needed                │   │
│   │                 Windows Event Log: look for GxJobMgr, MSSQL errors in last 24h                │   │
│   │           CommServe DR sync: SQL log shipping lag < 15 min; test failover quarterly           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    MediaAgent health includes DDB consistency and connectivity from all clients                       │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       MediaAgent Health                                       │   │
│   │              MA status: all configured MAs should show Ready in CommCell Console              │   │
│   │         DDB fragmentation: run DDB Verification job monthly; check for corrupt chunks         │   │
│   │                  Disk library: free space > 20%; monitor growth trend weekly                  │   │
│   │             Network throughput: MA backup streams should sustain > 500 MB/s per MA            │   │
│   │                  MA log: C:\Program Files\Commvault\Log Files\MediaAgent.log                  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Monitor disk library mount points (NFS/CIFS/LUN) for connectivity and free space                     │
│  MA server: check CPU/RAM utilization during peak backup windows (target < 80% CPU)                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  GxCVD          = CommVault Communications Service; handles all inter-component comms                 │
│  GxJobMgr       = CommVault Job Manager service; schedules and monitors all backup jobs               │
│  DDB Verify     = Job that reads all DDB fingerprints and validates against stored chunks             │
│  CSDB           = CommServe Database (SQL Server); holds all CommCell configuration                   │
│  MA Ready       = Status indicating MA service is running and library is accessible                   │
│  SLA Report     = Compliance report: % subclients with successful backup in SLA window                │
│  Log Shipping   = SQL Server mechanism replicating CSDB transaction logs to DR CommServe              │
│  Aux Copy Lag   = Time between primary backup completion and secondary copy completion                │
│  CV_DIAG        = Commvault diagnostic tool; collects all logs and config for support                 │
│  Library Prune  = Aged-out backup chunks removed from disk library per retention policy               │
│  Fragmentation  = DDB fragmentation degrades dedup performance; fixed by DDB defrag job               │
│  CommServe DR   = Passive standby CommServe; kept in sync via SQL log shipping                        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Run This Routine

Run these steps each morning for a complete CommVault CommServe health snapshot.

1. **CommServe services** — confirm core services are running:
   - Linux: `commvault list`
   - Windows: `net start | findstr /i "commvault"`
2. **Job activity summary** — CommCell Console → Job Controller → count Active / Waiting / Pending jobs; investigate any unexpected Pending or Waiting queue build-up.
3. **Alert console** — CommCell Console → Alerts → review all open Critical and High alerts; acknowledge resolved ones and action any new ones.
4. **MediaAgent connectivity** — verify all MAs show Ready status:
   ```bash
   qoperation execscript -sn GetMediaAgentStatus.sql
   ```
   Or check MA status directly in CommCell Console → MediaAgents.
5. **Library and drive status** — CommCell Console → Storage Resources → Libraries → confirm all drives show Online; investigate any Offline or Error state.
6. **Storage policy RPO compliance** — CommCell Console → Storage Policies → review last backup completion time per policy; flag any policy that has not completed within its RPO window.
7. **Failed jobs (last 24 h)** — CommCell Console → Reports → Backup Job Summary → filter Last 24 h + Failed; document each failure with error code and next action.
8. **CommServe disk space** — check host disk usage on the CommServe server:
   - Windows: `C:\Program Files\CommVault\ContentStore` — alert if >80 % used
   - Linux: `/opt/commvault/` — alert if >80 % used
9. **Client connectivity** — count offline clients:
   ```bash
   qinfo -info clientlist
   ```
   Or CommCell Console → Clients → filter for Offline; investigate any unexpected offline client.
10. **License usage** — CommCell Console → Control Panel → License Administration → confirm licence capacity is not exceeded and no component licences are expired.

Daily CommVault operations begin in the Job Controller (Command Center or Java GUI) to review all jobs from the previous 24 hours. Failed jobs display a status code — hovering reveals a description, and the job detail view shows phase-level failure logs. MediaAgent connectivity status and library health (if tape is in use) must be checked each morning, as a downed MediaAgent silently prevents any job targeting its storage pools from running. DDB space must be monitored closely; a full DDB causes all deduplication-enabled jobs to fail.

## Daily Checklist

- [ ] Job Controller — review all Failed and Pending jobs from last 24 hours
- [ ] Alert Console — clear or acknowledge resolved alerts; investigate new ones
- [ ] MediaAgent status — all MediaAgents online and communicating with CommServe
- [ ] Library status (if tape) — all drives online; no media errors
- [ ] DDB space — `qlist ddb` or Command Center Storage > Deduplication; alert if <20% free
- [ ] CommServe DB backup — confirm it completed last night

## Weekly Checks

- Verify auxiliary copy jobs ran successfully for all secondary copy pools
- Review SLA reports in Command Center — identify any clients below SLA threshold
- Run DDB verification on any DDB that has not been verified in the last 7 days
