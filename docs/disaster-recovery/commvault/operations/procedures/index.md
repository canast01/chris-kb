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
```

Verify all secondary copy jobs completed successfully. Investigate any that failed or did not run.

## CommServe Database Backup

Run a manual CommServe database backup before any major change:

```bash
# Trigger CommServe database backup
qsystem dbbackup
```

Alternatively: Command Center → Storage → System Backup → Run Now. Verify the backup completes before proceeding with any change.
