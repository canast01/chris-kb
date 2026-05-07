# Backup Jobs

Azure Backup jobs represent discrete backup, restore, and configuration operations. Monitoring job status is essential for confirming scheduled backups ran successfully and for diagnosing failures.

---

## Listing and Filtering Jobs

```bash
# List all backup jobs in a vault
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --output table

# Filter jobs by status (Completed, Failed, InProgress, Cancelled)
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --status Failed \
  --output table

# Filter jobs by operation type
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --operation Backup \
  --output table

# Filter jobs within a specific time range
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --start-date 2026-05-01T00:00:00 \
  --end-date 2026-05-07T23:59:59 \
  --output table
```

| Job Status | Meaning |
|---|---|
| Completed | Job finished successfully |
| CompletedWithWarnings | Job succeeded but had non-fatal issues |
| Failed | Job did not complete — action required |
| InProgress | Job is currently running |
| Cancelled | Job was manually cancelled |

---

## Inspecting a Specific Job

```bash
# Show full details for a job (job ID from list output)
az backup job show \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <job-id>

# Get just the status and error details
az backup job show \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <job-id> \
  --query "{Status:properties.status, Error:properties.errorDetails[0].errorMessage}" \
  --output table
```

---

## Waiting for a Job to Complete

Use `az backup job wait` in automation pipelines to block until a job finishes before proceeding.

```bash
# Wait for a specific job to complete (polls every 30 seconds)
az backup job wait \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <job-id>

# Trigger on-demand backup and wait for completion
JOB_ID=$(az backup protection backup-now \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --container-name <container-name> \
  --item-name <vm-name> \
  --backup-management-type AzureIaasVM \
  --retain-until 2026-06-30 \
  --query name --output tsv)

az backup job wait \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name "$JOB_ID"
```

---

## Failed Job Remediation

```bash
# List all failed jobs with error messages
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --status Failed \
  --query "[].{Item:properties.entityFriendlyName, Operation:properties.operation, Error:properties.errorDetails[0].errorString, Time:properties.startTime}" \
  --output table

# Retry a failed backup job (re-trigger on-demand)
az backup protection backup-now \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --container-name <container-name> \
  --item-name <vm-name> \
  --backup-management-type AzureIaasVM \
  --retain-until 2026-06-30
```

Common failure causes and remediation:

| Error | Likely Cause | Remediation |
|---|---|---|
| `UserErrorVmNotInDesirableState` | VM is in a stopped/deallocated state | Start the VM before the backup window |
| `GuestAgentSnapshotTaskStatusError` | VM agent not running or outdated | Update/reinstall the Azure VM agent |
| `ExtensionSnapshotFailedNoNetwork` | DNS or outbound connectivity issue | Check NSG rules, allow backup service tags |
| `BackupOperationFailedV2` | Transient failure | Retry; escalate if persistent |
| `UserErrorRpNotFound` | Recovery point expired or deleted | Adjust retention policy |

---

## Cancelling a Running Job

```bash
# Cancel a job that is currently in progress
az backup job stop \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <job-id>
```

---

## Job Monitoring via Azure Monitor

```bash
# Query backup job alerts in Azure Monitor (requires diagnostic settings enabled)
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "AddonAzureBackupJobs | where JobStatus == 'Failed' | project TimeGenerated, JobOperation, BackupItemFriendlyName, JobFailureCode | order by TimeGenerated desc | take 20" \
  --output table

# List configured diagnostic settings on the vault
az monitor diagnostic-settings list \
  --resource <vault-resource-id> \
  --output table
```
