---
tags:
  - azure
---
# Azure — Backup Jobs

```text
  Trigger
     │
     ▼
```

```text
     │
     ▼
  az backup job list --status Failed
```
```bash

## List all backup jobs in a vault
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --output table

## Filter jobs by status (Completed, Failed, InProgress, Cancelled)
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --status Failed \
  --output table

## Filter jobs by operation type
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --operation Backup \
  --output table

## Filter jobs within a specific time range
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --start-date 2026-05-01T00:00:00 \
  --end-date 2026-05-07T23:59:59 \
  --output table
```

```text title="Expected output"
Name                                 Operation    Status       Item Name            Start Time                 Duration
-----------------------------------  -----------  -----------  -------------------  -------------------------  ----------
cae3f8d2-4a1b-47c9-8f2e-9b1c5d7e2a4f  Backup       Completed    vm-prod-01           2026-05-05T14:32:00+00:00  00:45:23
b2e1d9c8-7f4a-4b2c-9e3d-1a5c8f2b6e9d  Backup       Completed    vm-prod-02           2026-05-05T15:18:00+00:00  00:38:15
9f7e2d1c-5b8a-4c3f-8e9d-2b6c7a1e4f5d  Backup       Failed       sql-db-backup        2026-05-04T22:00:00+00:00  00:12:45
7c4b1a9e-3f2d-4e8c-9b5a-6d8e1f2c3a4b  Backup       InProgress   file-share-01        2026-05-07T09:15:00+00:00  00:18:32
5a8e3d2c-1f4b-4a7c-8e9d-2b5c6f1a3e4d  Restore      Completed    vm-prod-03           2026-05-06T11:45:00+00:00  00:22:10
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceGroupNotFound` | Verify the resource group name with `az group list` and ensure it exists in your subscription. |
    | `VaultNotFound` | Confirm the vault name and resource group are correct using `az backup vault list --resource-group <rg>`. |
    | `InvalidDateFormat` | Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS) for `--start-date` and `--end-date` parameters. |
```bash
## Show full details for a job (job ID from list output)
az backup job show \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <job-id>

## Get just the status and error details
az backup job show \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <job-id> \
  --query "{Status:properties.status, Error:properties.errorDetails[0].errorMessage}" \
  --output table
```

```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/prod-backup-rg/providers/Microsoft.RecoveryServices/vaults/prod-vault-01/backupJobs/cbb2d5e7-4f8a-11ee-a136-001a7dda7113",
  "name": "cbb2d5e7-4f8a-11ee-a136-001a7dda7113",
  "type": "Microsoft.RecoveryServices/vaults/backupJobs",
  "properties": {
    "jobType": "AzureIaaSVMJob",
    "duration": "00:15:32.1234567",
    "status": "Completed",
    "startTime": "2024-01-15T09:30:45.123456Z",
    "endTime": "2024-01-15T09:46:17.456789Z",
    "entityFriendlyName": "prod-vm-01",
    "backupManagementType": "AzureIaaSVM",
    "operation": "Backup",
    "errorDetails": []
  }
}

Status    Error
--------  -------
Completed
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The resource 'Microsoft.RecoveryServices/vaults/<vault-name>/backupJobs/<job-id>' under resource group '<rg>' was not found.` | Verify the job ID exists by running `az backup job list` and confirm the vault name and resource group are correct. |
    | `InvalidResourceGroup: The resource group '<rg>' could not be found.` | Ensure the resource group name is spelled correctly and exists in your subscription using `az group list`. |
    | `AuthorizationFailed: The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/backupJobs/read' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>'.` | Grant the user or service principal the "Backup Reader" or "Backup Operator" role on the Recovery Services vault. |
```bash
## Wait for a specific job to complete (polls every 30 seconds)
az backup job wait \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <job-id>

## Trigger on-demand backup and wait for completion
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

```text title="Expected output"
Waiting for job completion...
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.RecoveryServices/vaults/prod-vault/backupJobs/cdf2d798-3692-4e44-9b67-8f5c6d4e3a2b",
  "name": "cdf2d798-3692-4e44-9b67-8f5c6d4e3a2b",
  "type": "Microsoft.RecoveryServices/vaults/backupJobs",
  "properties": {
    "jobType": "AzureIaaSVMJob",
    "duration": "00:15:32.5000000",
    "status": "Completed",
    "startTime": "2024-01-15T10:22:14.123456Z",
    "endTime": "2024-01-15T10:37:46.623456Z",
    "activityId": "12345678-1234-1234-1234-123456789012"
  }
}
Backup job triggered successfully.
Waiting for job completion...
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.RecoveryServices/vaults/prod-vault/backupJobs/a7f3e2c1-9d8b-4f6a-5c3e-1b2d4a6f8e9c",
  "name": "a7f3e2c1-9d8b-4f6a-5c3e-1b2d4a6f8e9c",
  "status": "Completed",
  "startTime": "2024-01-15T10:40:05.456789Z",
  "endTime": "2024-01-15T10:52:18.789012Z",
  "duration": "00:12:13.3322110"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The specified backup item could not be found.` | Verify the container-name and item-name match the protected VM exactly using `az backup container list` and `az backup item list`. |
    | `InvalidParameterValue: The value of parameter 'retain-until' is invalid.` | Ensure the retain-until date is in YYYY-MM-DD format and is at least 7 days in the future. |
    | `JobNotFound: The job with ID '<job-id>' was not found in the vault.` | Confirm the job ID exists and belongs to the specified vault; check recent jobs with `az backup job list --resource-group <rg> --vault-name <vault-name>`. |
```bash
## List all failed jobs with error messages
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --status Failed \
  --query "[].{Item:properties.entityFriendlyName, Operation:properties.operation, Error:properties.errorDetails[0].errorString, Time:properties.startTime}" \
  --output table

## Retry a failed backup job (re-trigger on-demand)
az backup protection backup-now \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --container-name <container-name> \
  --item-name <vm-name> \
  --backup-management-type AzureIaasVM \
  --retain-until 2026-06-30
```

```text title="Expected output"
Item                          Operation      Error                                    Time
------------------------------  -----------  ----------------------------------------  -----------------------
prod-db-server-01             ConfigureBackup  Snapshot creation failed: timeout       2024-01-15T09:23:45Z
web-app-vm-02                 Backup         VM agent not responding                  2024-01-15T08:47:12Z
file-share-backup-03          Backup         Insufficient disk space on vault         2024-01-15T07:15:33Z

Backup job triggered with ID: 12345678-1234-1234-1234-123456789abc
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The resource 'Microsoft.RecoveryServices/vaults/<vault-name>' could not be found.` | Verify the vault name and resource group name are correct and the vault exists in the specified region. |
    | `InvalidParameterValue: The container name '<container-name>' is not valid for this vault.` | List available containers with `az backup container list --resource-group <rg> --vault-name <vault-name>` and use the exact container name. |
    | `BadRequest: The item '<vm-name>' is not protected or the protection policy is not configured.` | Enable backup protection for the VM first using `az backup protection enable-for-vm` before attempting to trigger a backup. |
```bash
## Cancel a job that is currently in progress
az backup job stop \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <job-id>
```

```text title="Expected output"
Command group 'backup job' is in preview and under development. Reference and examples may change without notice.
Job cancellation request submitted successfully.
Job ID: b47e3c92-1a4f-4e8d-9f2c-5d8a1b6c3e9f
Status: CancellationInProgress
Vault: prod-backup-vault
Resource Group: prod-backups
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `(ResourceNotFound) The resource 'Microsoft.RecoveryServices/vaults/<vault-name>/backupJobs/<job-id>' does not exist.` | Verify the job ID exists by running `az backup job list --resource-group <rg> --vault-name <vault-name>` and use the correct job ID from the output. |
    | `(AuthorizationFailed) The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/backupJobs/read' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>'.` | Ensure your user account has the "Backup Operator" or "Backup Administrator" role assigned on the Recovery Services vault. |
    | `(InvalidOperation) Cannot cancel job in state 'Completed'.` | Only jobs in "InProgress" or "Waiting" states can be cancelled; check the job status with `az backup job show` before attempting cancellation. |
```bash
## Query backup job alerts in Azure Monitor (requires diagnostic settings enabled)
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "AddonAzureBackupJobs | where JobStatus == 'Failed' | project TimeGenerated, JobOperation, BackupItemFriendlyName, JobFailureCode | order by TimeGenerated desc | take 20" \
  --output table

## List configured diagnostic settings on the vault
az monitor diagnostic-settings list \
  --resource <vault-resource-id> \
  --output table
```


```text title="Expected output"
TimeGenerated                    JobOperation         BackupItemFriendlyName    JobFailureCode
2024-01-15T14:32:18.000000Z     ConfigureBackup      prod-sql-db-01            UserErrorBlobNotFound
2024-01-15T13:45:22.000000Z     Backup               vm-app-server-02          UserErrorVMNotFound
2024-01-15T12:18:56.000000Z     Restore              file-share-backup-01      UserErrorInvalidOperation
2024-01-15T11:05:33.000000Z     Backup               db-cluster-primary        ServiceFabricInternalError
2024-01-15T09:22:11.000000Z     ConfigureBackup      legacy-exchange-srv       UserErrorUnsupportedDiskType

Name                 ResourceGroup        VaultName              Logs    Metrics    Destination
diagnostic-prod     prod-backup-rg       backup-vault-eastus    True    True       /subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/resourceGroups/prod-backup-rg/providers/microsoft.operationalinsights/workspaces/backup-analytics
diagnostic-staging  staging-backup-rg    backup-vault-westus    True    False      /subscriptions/b2c3d4e5-f6g7-4h8i-9j0k-1l2m3n4o5p6q/resourceGroups/staging-backup-rg/providers/microsoft.operationalinsights/workspaces/staging-logs
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: (ResourceNotFound) The resource '<vault-resource-id>' could not be found.` | Verify the vault resource ID is correct and the vault exists in the current subscription using `az backup vault list`. |
    | `ERROR: The workspace '<workspace-id>' does not exist or you do not have permission to access it.` | Confirm the workspace ID is valid and your user account has Reader permissions on the Log Analytics workspace using `az role assignment list --scope <workspace-id>`. |