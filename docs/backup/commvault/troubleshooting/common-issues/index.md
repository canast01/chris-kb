---
tags:
  - commvault
  - troubleshooting
search:
  boost: 1.5
---
# Commvault — Common Issues


<div class="kb-summary">
Common Commvault issues — backup job failures, media agent errors, deduplication problems, and client connectivity failures.

*Applies to: Commvault 2024.x*
</div>

```text
┌──────────────────────────── Commvault Common Issues — Symptoms and Fixes ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Issue: Backup Jobs Consistently Failing                            │   │
│   │                    Symptom: jobs show "Failed" status; error in job details                   │   │
│   │             Cause A: disk library full → fix: prune expired data or expand library            │   │
│   │                Cause B: client iDA offline → fix: restart GxCVD on client host                │   │
│   │              Cause C: MA unreachable → fix: check network, restart GxCLMgrS on MA             │   │
│   │                Cause D: DDB corruption → fix: run DDB Verification + repair job               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Issue: Slow Backup Performance                                │   │
│   │           Symptom: backup throughput < expected; jobs taking 3x longer than baseline          │   │
│   │             Cause A: DDB fragmentation → fix: run DDB defrag job; schedule monthly            │   │
│   │             Cause B: network saturation → fix: enable bandwidth throttling or QoS             │   │
│   │          Cause C: MA CPU/disk bottleneck → fix: check iostat; add MA or upgrade disk          │   │
│   │             Cause D: too many concurrent jobs → fix: reduce max concurrent streams            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Issue: CommServe Unreachable                                 │   │
│   │               Symptom: CommCell Console cannot connect; clients cannot register               │   │
│   │                 Check A: Windows services GxCVD, GxJobMgr, SQL Server running                 │   │
│   │                    Check B: port 8400/8401 open; test: telnet <CS_IP> 8400                    │   │
│   │               Check C: CSDB accessible; test: sqlcmd -S localhost -Q "SELECT 1"               │   │
│   │                Fix: restart CV services; if SQL down, restore from CSDB backup                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Disk full: check mount path with df -h (Linux) or Get-PSDrive (Windows PowerShell)                   │
│  Network: use iperf3 between client and MA to measure actual throughput                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  DDB Defrag     = MediaAgent job that rewrites DDB to reduce fragmentation overhead                   │
│  Library Full   = Disk library mount path at 100% usage; new backup writes fail                       │
│  Pruning        = Commvault job removing expired chunks from library to free space                    │
│  Throughput     = Backup data rate in MB/s; baseline by running benchmark backup                      │
│  Concurrent Streams = Number of parallel data streams to a single MA                                  │
│  GxJobMgr       = CommServe Job Manager; if stopped, no jobs will run                                 │
│  sqlcmd         = SQL Server CLI tool; use to verify CSDB is responding                               │
│  iperf3         = Network throughput test tool; use between client and MA servers                     │
│  GxCLMgrS       = MediaAgent component service; if stopped, MA shows offline in CS                    │
│  Max Streams    = CommCell setting limiting parallel backup jobs per MA                               │
│  DDB Repair     = Automated repair mode of DDB Verification job; fixes detectable errors              │
│  CSDB Restore   = Last-resort recovery: restore SQL backup + replay transaction logs                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
CommVault job failures are classified by error code and phase. The first diagnostic step is to open the job detail in the Job Controller and expand the phase-level log — this shows the specific module and error code.

| Symptom | Likely Cause | Remediation |
|---|---|---|
| Job fails: network error (phase: backup) | MediaAgent cannot reach client on port 8400 | Check firewall rules; confirm client service is running (`cvd` daemon) |
| Job fails: DDB is offline | DDB disk full or corrupted | Check DDB disk space; run DDB verification; restore DDB from backup if corrupted |
| CommServe SQL errors | SQL Server disk full or SQL service issue | Check SQL Server disk; review SQL Server error log; free space or expand volume |
| Client authentication failure | Certificate mismatch or firewall blocking 8403 | Re-register client certificate; check `cvd` and `cvfwd` ports |
| MediaAgent offline | Service stopped or network issue | Restart CommVault services on MediaAgent; check `CVMA` service status |
| Auxiliary copy stuck | Source copy not pruned or tape library busy | Check tape drive availability; verify source data is not in use |
| DDB corruption | Unexpected shutdown during write | Run `qoperation execscript -sn QS_DDBVerify`; escalate if phase 2 fails |

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> A[Backup job stuck — offline client]
    S --> B[Dedup DB corruption]
    S --> C[Restore to different client failed]
    S --> D[Media agent unreachable]
    S --> E[Schedule not triggering]
    A --> A1{Client reachable on 8400?}
    A1 -->|No| A2[Check firewall and restart GxCVD on client — see Common Issues Reference]
    A1 -->|Yes| A3[Check job phase log for hung pre/post script or VSS error]
    B --> B1{DDB disk full?}
    B1 -->|Yes| B2[Free DDB disk space and run DDB Verification job — see Common Issues Reference]
    B1 -->|No| B3[Run qoperation execscript -sn QS_DDBVerify and escalate if phase 2 fails]
    C --> C1{Cross-client restore permission granted?}
    C1 -->|No| C2[Grant restore permission to target client in CommCell Console]
    C1 -->|Yes| C3[Check destination client credentials and iDA compatibility]
    D --> D1{GxCLMgrS service running?}
    D1 -->|No| D2[Restart CommVault services on MediaAgent — see Common Issues Reference]
    D1 -->|Yes| D3[Check network between CommServe and MediaAgent on port 8400]
    E --> E1[Verify GxJobMgr service is running and schedule window is active — see Common Issues Reference]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class A,B,C,D,E,A2,A3,B2,B3,C2,C3,D2,D3,E1 section
    class A1,B1,C1,D1 decision
    class S start
```

---

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
