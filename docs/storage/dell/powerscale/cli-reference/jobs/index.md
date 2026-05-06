# Jobs (Background Tasks)

> Part of the Dell PowerScale (Isilon) CLI Reference. OneFS uses a job engine to run background tasks — FlexProtect rebuilds, SmartPools tiering, quota accounting, deduplication, and more.

## Check Running Jobs

```bash
# Summary of currently running jobs
isi job status

# List all active jobs
isi job jobs list

# List jobs in a specific state
isi job jobs list --state running
isi job jobs list --state paused
isi job jobs list --state waiting
isi job jobs list --state failed

# View details of a specific job
isi job jobs view <job_id>
```

## Job Types

```bash
# List all available job types
isi job types list

# View details and description of a job type
isi job types view <type_name>

# Key job types:
# FlexProtect      — re-protects data after a node or drive failure
# SmartPools       — moves files between tiers based on file pool policies
# Dedupe           — block-level deduplication (requires SmartDedupe license)
# QuotaScan        — recalculates quota accounting
# ShadowStoreDelete — removes shadow store data (snapshots/dedupe)
# MultiScan        — combined integrity and protection scan
# AutoBalance      — rebalances data across nodes
```

## Start and Cancel Jobs

```bash
# Start a job manually (useful after drive replacement)
isi job jobs start FlexProtect
isi job jobs start QuotaScan
isi job jobs start SmartPools

# Cancel a running job
isi job jobs cancel <job_id>

# Pause a job (can be resumed)
isi job jobs pause <job_id>

# Resume a paused job
isi job jobs resume <job_id>
```

## Job History

```bash
# View completed job history
isi job history list

# View history for a specific job type
isi job history list | grep SmartPools

# Job events (detailed log entries)
isi job events list

# Events for a specific job
isi job events list --job-id <job_id>
```

## Job Impact Policies

```bash
# List impact policies (control resource usage during jobs)
isi job policies list

# View a policy
isi job policies view <policy_name>

# Modify a job type's impact policy (e.g., run Dedupe at low impact)
isi job types modify Dedupe --policy LOW
```

## Monitoring FlexProtect

FlexProtect is the most critical background job — runs after node/drive failures:

```bash
# Check if FlexProtect is running
isi job jobs list | grep FlexProtect

# Check overall data protection status
isi status | grep -E "SmartFail|Unhealthy|At risk"

# Check for unprotected files
isi job jobs list | grep MultiScan
isi status -n all | grep -i "unprotected\|degraded"
```
