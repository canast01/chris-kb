---
tags:
  - commvault
  - operations
---
# Commvault — CLI Reference

<div class="kb-summary">
CLI Reference reference covering Backup Job Lifecycle, Backup Operations, Restore Operations, Clients & Policies, CommServe Maintenance and 1 more sections.

*Applies to: Commvault 2024.x*
</div>

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Backup Job Lifecycle

From schedule trigger to media write, every CommVault backup job moves through a defined sequence of states.

```mermaid
sequenceDiagram
    participant Sched as Scheduler (CommServe)
    participant JM as Job Manager
    participant Client as Client Agent
    participant MA as MediaAgent
    participant DDB as DDB (dedup store)
    participant Storage as Storage Library

    Sched->>JM: Trigger job per schedule policy
    JM->>Client: Initiate backup — send job token
    Client->>Client: Quiesce filesystem / app (VSS)
    Client->>MA: Stream data (TCP 8403)
    MA->>DDB: Deduplicate data blocks
    DDB-->>MA: Unique blocks only
    MA->>Storage: Write to primary copy (disk library)
    Storage-->>MA: Write confirmed
    MA-->>JM: Job complete — update catalog
    JM-->>Sched: Job status: Completed
    note over MA,Storage: Auxiliary copy job (separate schedule)\ncopies from primary to secondary (offsite/tape/cloud)
```

---

## Restore Operations

### Restore Workflow Decision Tree

```d2
direction: right

q1: "q1" {shape: rectangle}
volumeRestore: "Volume-level restore\nqoperation restore\n-subclient -topath" {shape: rectangle}
vmRestore: "Full VM restore\n(VSA subclient" {shape: rectangle}
appRestore: "Application-aware restore\nPoint-in-time log replay\nor granular item restore" {shape: rectangle}
q2: "q2" {shape: rectangle}
winFlr: "File-level restore\nbrowse from catalog\nqoperation restore -subclient -topath" {shape: rectangle}
linFlr: "File-level restore\nbrowse from catalog\nqoperation restore -subclient -topath" {shape: rectangle}
verifyDest: "Verify destination\nhas sufficient space" {shape: rectangle}
execute: "Execute restore\nMonitor in Job Controller" {shape: rectangle}
validate: "Validate restored\ndata integrity" {shape: rectangle}
restoreStart: "Restore request received" {shape: rectangle}

q1 -> volumeRestore
q1 -> vmRestore
q1 -> appRestore
q2 -> winFlr
q2 -> linFlr
volumeRestore -> verifyDest
vmRestore -> verifyDest
appRestore -> verifyDest
winFlr -> verifyDest
linFlr -> verifyDest
verifyDest -> execute
execute -> validate
```

Always verify destination and time range before executing a restore.

```bash
# Restore to original location at a point in time
qoperation restore -subclient <name> -totime "2024-01-01 12:00:00"

# Restore to alternate path
qoperation restore -subclient <name> -topath /restore/destination

# List recent restore jobs
qlist jobs -d 1 -restore
```

---

## Clients & Policies

Manage client registration, storage policies, and schedules.

```bash
# List all clients
qlist client

# List storage policies
qlist storagepolicy

# List schedules
qlist schedule

# List deduplication databases
qlist ddb

# Check client connectivity readiness
qoperation execscript -sn QS_CheckReadiness

# List backup sets for a client
qlist backupset -c <client_name>
```

---

## CommServe Maintenance

Database backup and health tasks for CommServe.

```bash
# Trigger CommServe database backup
qsystem dbbackup

# Commit pending configuration changes
qcommit

# Check CommServe services status
qlist services

# Check license usage
qlist license
```

---

## REST API

All operations are also available via REST API for automation.

```bash
# Authenticate and get token
curl -X POST "https://<CommServe>/webconsole/api/Login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","domain":""}'

# List all clients
curl -X GET "https://<CommServe>/webconsole/api/Client" \
  -H "Authtoken: <token>"

# List active jobs
curl -X GET "https://<CommServe>/webconsole/api/Job?jobFilter=Active" \
  -H "Authtoken: <token>"
```

---

## Verify

- **Job status:** confirm backup job completed with status Success (not Warning)
- **Recovery test:** restore a single file or VM from the new backup to confirm restorability
- **Retention:** verify old recovery points are expiring per the configured retention policy

---

## See also

- [Commvault — Procedures](../procedures/)
- [Commvault — Scripts](../scripts/)
- [Commvault — Health Checks](../health-checks/)
