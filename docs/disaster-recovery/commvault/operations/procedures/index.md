# Commvault — Procedures

Operational procedures for change readiness, maintenance windows, and recurring operational tasks.

## Change Readiness Check

Before making configuration changes or running maintenance, verify the environment is ready:

```bash
# Check client connectivity readiness
qoperation execscript -sn QS_CheckReadiness

# Confirm all jobs are complete (no active jobs)
qlist jobs

# Check CommServe services status
qlist services
```

## Maintenance Window Procedure

1. Notify stakeholders of the maintenance window and expected impact.
2. Confirm all running jobs are complete or suspended.
3. Perform the required changes (configuration, patching, upgrades).
4. Run a readiness check after the window to confirm all services are healthy.
5. Monitor the Job Controller for the next 24 hours to confirm no unexpected failures.

## Auxiliary Copy Verification

Run after any maintenance window affecting secondary storage:

```bash
# List storage policies to identify secondary copies
qlist storagepolicy

# Check auxiliary copy job status
qlist jobs -d 1
```

Verify all secondary copy jobs completed successfully. Investigate any that failed or did not run.

## CommServe Database Backup

Run a manual CommServe database backup before any major change:

```bash
# Trigger CommServe database backup
qsystem dbbackup
```

Alternatively: Command Center → Storage → System Backup → Run Now. Verify the backup completes before proceeding with any change.
