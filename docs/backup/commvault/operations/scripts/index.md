---
tags:
  - commvault
  - operations
---
# Commvault — Scripts


<div class="kb-summary">
PowerShell and qscript automation for Commvault job management, SLA reporting, client health checks, and storage utilisation.

*Applies to: Commvault 2024.x*
</div>

```text
┌──────────────────────────── Commvault Scripts — Automation and Reporting ─────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          PowerShell / Bash Scripts           │  │               Python (CV SDK)               │   │
│   │        Daily job failure report email        │  │          cvpysdk: OOP REST wrapper          │   │
│   │          SLA compliance CSV export           │  │        CommCell() → client.backups()        │   │
│   │           Disk library space alert           │  │       Trigger backup programmatically       │   │
│   │        MA status health check script         │  │           Query job history to DB           │   │
│   │         qlist jobs | parse failures          │  │         Automated new client onboard        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Scripts use qoperation/qlist CLI or REST API; store credentials in vault (not plain text)          │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     Common Script Examples                                    │   │
│   │      Daily report: qlist jobs -jobtype backup -status failed | mail -s "CV Failures" ops@     │   │
│   │           Disk check: qlist storage -type disk | awk '{if ($5>80) print "WARN:"$1}'           │   │
│   │         New client: qoperation addclient -clientName HOST -username admin -os windows         │   │
│   │             Aux copy trigger: qoperation auxcopy -storagepolicy SP_Name -allCopies            │   │
│   │          Python SDK: from cvpysdk.commcell import Commcell; cc=Commcell(cs, user, pw)         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Scripts run on CommServe host or jump host with cv CLI in PATH                                       │
│  Python SDK: pip install cvpysdk; requires Python 3.8+; HTTPS 443 to CommServe                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  cvpysdk        = Commvault Python SDK (pip install cvpysdk); open-source REST wrapper                │
│  Commcell()     = Primary cvpysdk class; authenticates and connects to CommServe                      │
│  qlist output   = Tab-separated or CSV output suitable for shell parsing                              │
│  Pre-Post Script= Script run before/after subclient backup (app quiesce, notify, etc.)                │
│  Alert Script   = Script triggered by CommServe alert event (job fail, disk low, etc.)                │
│  REST Token     = Session token from POST /Login; used as header for subsequent API calls             │
│  Job History DB = SQL view in CSDB exposing completed job data for custom reporting                   │
│  Cron / Task    = OS scheduler (cron on Linux, Task Scheduler on Windows) for reports                 │
│  Mail Relay     = SMTP server configured in CommServe for alert email delivery                        │
│  Secret Vault   = HashiCorp Vault or CyberArk; store CV admin credentials, not plaintext              │
│  addclient      = qoperation subcommand to register new client in CommCell                            │
│  allCopies      = Flag in auxcopy command to replicate all storage policy copies                      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- **Job status:** confirm backup job completed with status Success (not Warning)
- **Recovery test:** restore a single file or VM from the new backup to confirm restorability
- **Retention:** verify old recovery points are expiring per the configured retention policy

---

## See also

- [Commvault — Procedures](../procedures/)
- [Commvault — CLI Reference](../cli-reference/)
- [Commvault — Health Checks](../health-checks/)
