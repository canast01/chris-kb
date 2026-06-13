---
tags:
  - commvault
  - troubleshooting
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

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

