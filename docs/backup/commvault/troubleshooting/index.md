# Commvault — Troubleshooting



<div class="kb-summary">
Commvault — Troubleshooting reference.
</div>

```text
┌────────────────────────────── Commvault Troubleshooting — Decision Tree ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        Problem Reported                                       │   │
│   │            Backup job failed · Restore failed · Slow backup · CommServe unreachable           │   │
│   │          First check: CommCell Console Job Activity → view job details and error code         │   │
│   │           Error code lookup: Commvault KB (ma.commvault.com) or cv_help <error_code>          │   │
│   │                Collect: job ID, client name, MA name, error message, log files                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Triage by component: CommServe → MediaAgent → Client → Network → Storage                           │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               CommServe Issues               │  │              MediaAgent Issues              │   │
│   │     Services down: check GxCVD/GxJobMgr      │  │      MA offline: check GxCLMgrS service     │   │
│   │     SQL errors: check CSDB log, reindex      │  │     DDB corrupt: run DDB Verify + repair    │   │
│   │    Job stuck queued: check resource pool     │  │      Disk full: prune or expand library     │   │
│   │      Log: C:\CV\Log Files\CommServe.log      │  │     Log: C:\CV\Log Files\MediaAgent.log     │   │
│   │       CS restart: net stop/start GxCVD       │  │     MA restart: net stop/start GxCLMgrS     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    For unresolved issues: collect CV_DIAG bundle → open Commvault Support case                        │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    Client / Network Issues                                    │   │
│   │             Client unreachable: ping, telnet CS:8400, check firewall/proxy config             │   │
│   │                  iDA not responding: restart GxFWD / GxCVD service on client                  │   │
│   │                Network: check bandwidth, test MA:8403 reachability from client                │   │
│   │             App backup fail: check VSS/RMAN/VDI integration; review app agent log             │   │
│   │            CV_DIAG: CommCell → Help → Diagnostics → Run Diagnostics; zip and upload           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Network: traceroute client → MA (port 8403); verify MTU and QoS settings                             │
│  Storage: check MA disk I/O (iostat); full library is common backup failure cause                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  GxCVD          = CommVault Communications Service; core daemon on all CV components                  │
│  GxJobMgr       = Job Manager service on CommServe; schedules and monitors all jobs                   │
│  GxCLMgrS       = Client Manager Service; manages iDA agents on client machines                       │
│  GxFWD          = CommVault Firewall Daemon; handles tunnel/proxy communications                      │
│  CV_DIAG        = Diagnostic collection tool; generates zip of all logs and config                    │
│  Error Code     = 4-digit Commvault error code; searchable in ma.commvault.com KB                     │
│  DDB Verify     = Job scanning all DDB entries for corruption; run monthly or on error                │
│  Resource Pool  = CommServe construct limiting concurrent jobs per MA or client group                 │
│  CSDB Integrity = SQL DBCC CHECKDB on CommCell database; run quarterly                                │
│  Job Details    = Per-phase job log with timestamps, data rates, and error codes                      │
│  ma.commvault.com = Commvault support portal; KB articles and case management                         │
│  Triage Order   = CS services → MA services → Client connectivity → App agent → Network               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Job failures, DDB errors, authentication failures, and MediaAgent issues.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and support bundle collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Vendor support portal, case requirements, and support tiers.</span>
</a>

</div>
