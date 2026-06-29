---
tags:
  - azure
---
# Failover

<div class="kb-summary">
Azure Site Recovery supports three types of failover: test failover (non-disruptive validation), planned failover (zero data loss), and unplanned failover (best-effort, used during real incidents). All failovers move protected workloads to the recovery region.

*Applies to: Azure*
</div>

---

## Failover Decision Flow

```d2
direction: right

failoverNeeded: "Failover Required" {shape: rectangle}
drDrill: "drDrill" {shape: rectangle}
testFailover: "Test Failover\nIsolated test VNet\nNo production impact" {shape: rectangle}
cleanup: "Cleanup\ntest VMs deleted" {shape: rectangle}
plannedFailover: "Planned Failover\nClean VM shutdown\nZero RPO" {shape: rectangle}
drVMRunning: "DR VM Running\nin Recovery Region" {shape: rectangle}
commit: "Commit Failover\ncut primary VM" {shape: rectangle}
unplannedFailover: "Unplanned Failover\nImmediate cutover\nPossible data loss" {shape: rectangle}
planned: "planned" {shape: rectangle}

failoverNeeded -> drDrill
testFailover -> cleanup
plannedFailover -> drVMRunning
drVMRunning -> commit
unplannedFailover -> drVMRunning
```

## Failover Types Compared

| Type | Data Loss | VM Shutdown | Use Case |
|---|---|---|---|
| Test Failover | None | No (production continues) | DR drills, compliance validation |
| Planned Failover | None | Yes (clean shutdown first) | Planned maintenance, region migration |
| Unplanned Failover | Possible | No (immediate cutover) | Real disaster, primary region failure |

---

## Pre-Failover Checks

```bash
# Check replication health before failover
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems?api-version=2022-10-01" \
  --query "value[].{Name:name, Health:properties.replicationHealth, RPO:properties.rpoInSeconds}" \
  --output table

# Confirm the vault is accessible
az backup vault show \
  --resource-group <dr-rg> \
  --name <vault-name> \
  --query "properties.provisioningState" --output tsv

# Verify target network exists in DR region
az network vnet show \
  --resource-group <dr-rg> \
  --name <target-vnet-name> \
  --query "provisioningState" --output tsv
```


```text title="Expected output"
Name                                    Health    RPO
--------------------------------------  --------  -----
vm-prod-web-01                          Normal    300
vm-prod-db-02                           Normal    450
vm-prod-app-03                          Normal    300
vm-prod-cache-01                        Normal    600
Succeeded
Succeeded
```

!!! warning "Common errors"
    **`ResourceNotFound`** — Verify the subscription ID, resource group name, and vault name are correct and exist in the target region.
    **`AuthorizationFailed`** — Ensure your Azure CLI account has Reader or Contributor permissions on the Recovery Services vault and target resource group.
    **`The resource 'Microsoft.Network/virtualNetworks/<target-vnet-name>' under resource group '<dr-rg>' was not found`** — Confirm the target virtual network has been pre-created in the DR region before initiating failover.
---

## Test Failover

Test failover spins up a replica VM in an isolated network. Production replication is unaffected.

```bash
# Trigger test failover
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<source-fabric>/replicationProtectionContainers/<source-container>/replicationProtectedItems/<item-name>/testFailover?api-version=2022-10-01" \
  --body '{
    "properties": {
      "networkId": "<test-vnet-id>",
      "failoverDirection": "PrimaryToRecovery",
      "providerSpecificDetails": {"instanceType": "A2A"}
    }
  }'

# Monitor the test failover job
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationJobs?api-version=2022-10-01" \
  --query "value[?properties.jobType=='TestFailover'].{Name:name, State:properties.state}" \
  --output table

# Clean up test failover (mandatory after validation)
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<source-fabric>/replicationProtectionContainers/<source-container>/replicationProtectedItems/<item-name>/testFailoverCleanup?api-version=2022-10-01" \
  --body '{"properties": {"comments": "DR drill completed - clean up"}}'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg/providers/Microsoft.RecoveryServices/vaults/prod-vault/replicationJobs/8f4e9c2a-1b3d-4e5f-6a7b-8c9d0e1f2a3b",
  "name": "8f4e9c2a-1b3d-4e5f-6a7b-8c9d0e1f2a3b",
  "type": "Microsoft.RecoveryServices/vaults/replicationJobs",
  "properties": {
    "jobType": "TestFailover",
    "state": "InProgress",
    "startTime": "2024-01-15T14:32:18.5432109Z",
    "endTime": null
  }
}
Name                                      State
----------------------------------------  -----------
8f4e9c2a-1b3d-4e5f-6a7b-8c9d0e1f2a3b    Succeeded
9g5f0d3b-2c4e-5f6g-7b8c-9d0e1f2a3b4c    Succeeded

{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg/providers/Microsoft.RecoveryServices/vaults/prod-vault/replicationJobs/7d3c8b1a-2e4f-5a6b-7c8d-9e0f1a2b3c4d",
  "name": "7d3c8b1a-2e4f-5a6b-7c8d-9e0f1a2b3c4d",
  "type": "Microsoft.RecoveryServices/vaults/replicationJobs",
  "properties": {
    "jobType": "TestFailoverCleanup",
    "state": "Succeeded",
    "startTime": "2024-01-15T14:45:22.1234567Z",
    "endTime": "2024-01-15T14:47:33.9876543Z"
  }
}
```

!!! warning "Common errors"
    **`The provided URI is invalid or the resource does not exist.`** — Verify all placeholder values (<sub-id>, <vault-name>, <item-name>) are replaced with actual resource names and IDs from your Azure environment.
    **`Authorization failed for request. Caller is not authorized to perform action 'Microsoft.RecoveryServices/vaults/replicationJobs/read' on resource.`** — Ensure your Azure CLI account has the "Site Recovery Operator" or "Contributor" role assigned on the Recovery Services vault.
    **`The test failover cannot be initiated because the protected item is not in a valid state.`** — Verify the replication item has completed initial replication and is in "Protected" state using `az rest --method GET --uri "...replicationProtectedItems/<item-name>?api-version=2022-10-01"`.
---

## Planned Failover

Planned failover shuts down the source VM cleanly, synchronises all pending data, then brings up the target VM. Zero data loss guaranteed.

```bash
# Trigger planned failover
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<source-fabric>/replicationProtectionContainers/<source-container>/replicationProtectedItems/<item-name>/plannedFailover?api-version=2022-10-01" \
  --body '{
    "properties": {
      "failoverDirection": "PrimaryToRecovery",
      "providerSpecificDetails": {"instanceType": "A2A"}
    }
  }'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg-prod/providers/Microsoft.RecoveryServices/vaults/vault-dr-01/replicationFabrics/fabric-eastus/replicationProtectionContainers/container-01/replicationProtectedItems/vm-app-prod-01/plannedFailover",
  "name": "vm-app-prod-01",
  "type": "Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/plannedFailover",
  "properties": {
    "friendlyName": "vm-app-prod-01",
    "name": "vm-app-prod-01",
    "currentScenario": {
      "scenarioName": "PlannedFailover",
      "jobId": "d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a",
      "startTime": "2024-01-15T14:32:18.5432109Z"
    },
    "failoverHealth": "Normal",
    "lastSuccessfulFailoverTime": "2024-01-15T14:32:18.5432109Z"
  }
}
```

!!! warning "Common errors"
    **`AuthorizationFailed: The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/plannedFailover/action'`** — Ensure your Azure user or service principal has the "Site Recovery Operator" or "Contributor" role assigned to the Recovery Services vault.
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<source-fabric>/replicationProtectionContainers/<source-container>/replicationProtectedItems/<item-name>' under resource group '<dr-rg>' was not found.`** — Verify the subscription ID, resource group name, vault name, fabric name, container name, and protected item name are correct and exist in your subscription.
    **`BadRequest: The item is not in a state that allows failover. Current state: 'NotStarted'. Replication must be enabled and synchronized before failover.`** — Enable replication for the item and wait for initial synchronization to complete before attempting failover.
---

## Unplanned Failover

Used when the primary region is unavailable. Accept potential data loss of up to one RPO cycle.

```bash
# Trigger unplanned failover to latest recovery point
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<source-fabric>/replicationProtectionContainers/<source-container>/replicationProtectedItems/<item-name>/unplannedFailover?api-version=2022-10-01" \
  --body '{
    "properties": {
      "failoverDirection": "PrimaryToRecovery",
      "sourceSiteOperations": "NotRequired",
      "providerSpecificDetails": {
        "instanceType": "A2A",
        "recoveryPointId": "latest"
      }
    }
  }'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/dr-rg-prod/providers/Microsoft.RecoveryServices/vaults/vault-dr-001/replicationFabrics/fabric-eastus2/replicationProtectionContainers/container-prod/replicationProtectedItems/vm-app-server-01/unplannedFailover",
  "name": "vm-app-server-01",
  "type": "Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/unplannedFailover",
  "properties": {
    "failoverDirection": "PrimaryToRecovery",
    "sourceSiteOperations": "NotRequired",
    "providerSpecificDetails": {
      "instanceType": "A2A",
      "recoveryPointId": "2024-01-15T14:32:45.1234567Z",
      "recoveryPointType": "Latest"
    },
    "startTime": "2024-01-15T14:33:12.5678901Z",
    "endTime": null,
    "state": "InProgress",
    "percentageComplete": 0
  }
}
```

!!! warning "Common errors"
    **`AuthorizationFailed : The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/unplannedFailover/action' over scope '/subscriptions/<sub-id>/resourceGroups/<dr-rg>'`** — Assign the user or service principal the "Site Recovery Operator" or "Contributor" role on the Recovery Services vault.
    **`ResourceNotFound : The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<source-fabric>/replicationProtectionContainers/<source-container>/replicationProtectedItems/<item-name>' under resource group '<dr-rg>' was not found.`** — Verify the subscription ID, resource group, vault name, fabric name, container name, and protected item name are correct using `az recovery-services-backup container list`.
    **`BadRequest : Failover cannot be triggered because the replication health is 'Critical' or the item is in 'NotStarted' state.`** — Check replication status with `az rest --method GET --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<source-fabric>/replicationProtectionContainers/<source-container>/replicationProtectedItems/<item-name>?api-version=2022-10-01"` and ensure replication is healthy before retrying.
---

## Recovery Plans

Recovery plans define the order in which VMs are failed over and allow pre/post scripts.

```bash
# List all recovery plans in the vault
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationRecoveryPlans?api-version=2022-10-01" \
  --query "value[].{Name:name, Groups:properties.groups}" \
  --output table

# Trigger a recovery plan failover
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationRecoveryPlans/<plan-name>/plannedFailover?api-version=2022-10-01" \
  --body '{"properties": {"failoverDirection": "PrimaryToRecovery", "providerSpecificDetails": [{"instanceType": "A2A"}]}}'
```


```text title="Expected output"
Name                          Groups
------------------------------  --------
prod-app-recovery-plan        3
dr-database-failover-plan     2
web-tier-recovery-plan        4

{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg/providers/Microsoft.RecoveryServices/vaults/prod-vault/replicationRecoveryPlans/prod-app-recovery-plan/plannedFailover/12345678-1234-1234-1234-123456789012",
  "name": "prod-app-recovery-plan",
  "type": "Microsoft.RecoveryServices/vaults/replicationRecoveryPlans/plannedFailover",
  "properties": {
    "friendlyName": "prod-app-recovery-plan",
    "status": "InProgress",
    "startTime": "2024-01-15T14:32:18.5432109Z",
    "allowedOperations": [
      "Resume",
      "Cancel"
    ]
  }
}
```

!!! warning "Common errors"
    **`AuthorizationFailed : The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationRecoveryPlans/plannedFailover/action' over scope '/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>'`** — Assign the Site Recovery Contributor role to your user or service principal on the Recovery Services vault.
    **`ResourceNotFound : The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>/replicationRecoveryPlans/<plan-name>' under resource group '<dr-rg>' was not found.`** — Verify the vault name, resource group, and recovery plan name are correct using `az recovery-services vault list` and `az site-recovery recovery-plan list`.
    **`BadRequest : Invalid failover direction. Allowed values are 'PrimaryToRecovery' or 'RecoveryToPrimary'.`** — Ensure the failoverDirection property matches the current replication state and use the correct direction for your scenario.
---

## Commit Failover

After a failover (planned or unplanned), commit to finalize the state and stop reverse delta sync.

```bash
# Commit failover for a protected item
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<source-fabric>/replicationProtectionContainers/<source-container>/replicationProtectedItems/<item-name>/failoverCommit?api-version=2022-10-01"
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg-prod/providers/Microsoft.RecoveryServices/vaults/vault-dr-01/replicationFabrics/fabric-primary/replicationProtectionContainers/container-01/replicationProtectedItems/vm-app-server-01/failoverCommit",
  "name": "vm-app-server-01",
  "type": "Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems",
  "properties": {
    "friendlyName": "vm-app-server-01",
    "protectionStatus": "Protected",
    "replicationHealth": "Normal",
    "failoverHealth": "Normal",
    "lastSuccessfulFailoverTime": "2024-01-15T14:32:18.5432109Z",
    "lastSuccessfulTestFailoverTime": "2024-01-14T10:15:42.1234567Z",
    "failoverCommitStatus": "Committed"
  }
}
```

!!! warning "Common errors"
    **`ERROR: (AuthorizationFailed) The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/failoverCommit/action' over scope '/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>'`** — Assign the user or service principal the "Site Recovery Operator" or "Contributor" role on the Recovery Services vault.
    **`ERROR: (ResourceNotFound) The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<source-fabric>/replicationProtectionContainers/<source-container>/replicationProtectedItems/<item-name>' under resource group '<dr-rg>' was not found.`** — Verify the vault name, fabric name, container name, and protected item name are correct using `az recovery-services-backup item list`.
    **`ERROR: (InvalidRequestContent) The request content was invalid and could not be deserialized: 'Missing required property: api-version in query parameters.'`** — Ensure the `api-version=2022-10-01` parameter is included in the URI query string without modification.
---

## Post-Failover Validation

```bash
# Confirm DR VM is running
az vm show \
  --resource-group <dr-rg> \
  --name <dr-vm-name> \
  --show-details \
  --query "powerState" --output tsv

# Check activity log for failover-related events
az monitor activity-log list \
  --resource-group <dr-rg> \
  --start-time $(date -u -d '2 hours ago' +%Y-%m-%dT%H:%M:%SZ) \
  --query "[].{Time:eventTimestamp, Op:operationName.value, Status:status.value}" \
  --output table
```


```text title="Expected output"
VM running

Time                          Op                                    Status
----------------------------  ------------------------------------  ---------
2024-01-15T14:32:18.123456Z   Microsoft.Compute/virtualMachines/start  Succeeded
2024-01-15T14:31:45.987654Z   Microsoft.Compute/virtualMachines/write  Succeeded
2024-01-15T14:30:12.654321Z   Microsoft.Network/networkInterfaces/write  Succeeded
2024-01-15T14:29:33.456789Z   Microsoft.Compute/disks/read  Succeeded
2024-01-15T14:28:01.234567Z   Microsoft.RecoveryServices/vaults/backupFabrics/protectionContainers/protectedItems/backup  Succeeded
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Compute/virtualMachines/<dr-vm-name>' under resource group '<dr-rg>' was not found.`** — Verify the resource group name and DR VM name are correct and exist in your subscription.
    **`AuthorizationFailed: The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Compute/virtualMachines/read' over scope '/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.Compute/virtualMachines/<dr-vm-name>'.`** — Ensure your Azure CLI account has Reader or Contributor role assigned to the DR resource group.