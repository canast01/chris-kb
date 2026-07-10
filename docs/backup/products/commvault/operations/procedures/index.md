---
tags:
  - commvault
  - operations
---
# Commvault Operational Procedures — Runbooks

```bash
# Check client connectivity readiness
qoperation execscript -sn QS_CheckReadiness

# Confirm all jobs are complete (no active jobs)
qlist jobs

# Check CommServe services status
qlist services
```

```d2
direction: right

add_a_client: "Add a Client" {shape: rectangle}
create_a_storage_policy: "Create a Storage Policy" {shape: rectangle}
create_a_subclient_and_schedule: "Create a Subclient and Schedule" {shape: rectangle}
run_an_adhoc_backup: "Run an Ad-Hoc Backup" {shape: rectangle}
restore_files_from_backup: "Restore Files from Backup" {shape: rectangle}
change_a_backup_schedule: "Change a Backup Schedule" {shape: rectangle}

add_a_client -> create_a_storage_policy
create_a_storage_policy -> create_a_subclient_and_schedule
create_a_subclient_and_schedule -> run_an_adhoc_backup
run_an_adhoc_backup -> restore_files_from_backup
restore_files_from_backup -> change_a_backup_schedule
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Add a Client

CommCell Console → Client Computers → New Client → push install or manual install → configure content path.

## Create a Storage Policy

Policies → Storage Policies → New → select primary disk library → add secondary copy → set retention.

## Create a Subclient and Schedule

Client → Agent → Subclient → configure content → assign storage policy → set Full + Incremental schedule.

## Run an Ad-Hoc Backup

Right-click subclient → Backup → Full or Incremental → monitor in Job Controller.

## Restore Files from Backup

Client → Agent → Subclient → Browse and Restore → select restore point → choose files → restore to original or alternate location.

## Change a Backup Schedule

Subclient → Properties → Schedules tab → modify frequency, time, or retention.

## Retire a Client

CommCell Console → select client → Deconfigure → Release Licence → Delete Client (after confirming all backups no longer needed).

## Rotate Storage Policy Copies (Tape to Tape)

CommCell Console → Storage Policies → select policy → Copies → initiate auxiliary copy job to move data to secondary media.

## Check Backup SLA Compliance

CommCell Console → Reports → Backup Job Summary → filter by last 24h → identify missed or failed jobs by client.

## Recover the CommServe Database

Boot DR CommServe (if primary lost) → restore CommServe DB from backup → reconnect MediaAgents → verify client connections restored.

---

## Verify

- **Job status:** confirm backup job completed with status Success (not Warning)
- **Recovery test:** restore a single file or VM from the new backup to confirm restorability
- **Retention:** verify old recovery points are expiring per the configured retention policy

---

## See also

- [Commvault — Health Checks](../health-checks/)
- [Commvault — CLI Reference](../cli-reference/)
- [Commvault — Common Issues](../../troubleshooting/common-issues/)
