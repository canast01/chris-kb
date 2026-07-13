---
tags:
  - azure
description: "Azure Site Recovery (ASR) orchestrates replication, failover, and failback for Azure VMs and on-premises workloads. It enables business continuity with..."
---
# Azure Site Recovery

<div class="kb-summary">
Azure Site Recovery (ASR) orchestrates replication, failover, and failback for Azure VMs and on-premises workloads. It enables business continuity with RPO targets as low as 30 seconds for Azure-to-Azure replication.

*Applies to: Azure*
</div>

---

## ASR Replication Flow

```d2
direction: right

sourceVM: "Source VM\nPrimary Region" {shape: rectangle}
asrAgent: "ASR Mobility Agent\nor Azure Fabric" {shape: rectangle}
cacheStorage: "Cache Storage Account\nPrimary Region" {shape: rectangle}
replication: "Continuous Replication\nRPO ~ 30 seconds" {shape: rectangle}
targetStorage: "Replica Managed Disk\nDR Region" {shape: rectangle}
vault: "Recovery Services Vault\nDR Region" {shape: rectangle}
failover: "Failover\nTest · Planned · Unplanned" {shape: rectangle}
targetVM: "Target VM\nDR Region — running" {shape: rectangle}

sourceVM -> asrAgent
asrAgent -> cacheStorage
cacheStorage -> replication
replication -> targetStorage
targetStorage -> vault
vault -> failover
failover -> targetVM
```

## Prerequisites and Vault Setup

```bash
# Create a Recovery Services Vault in the target (DR) region
az backup vault create \
  --resource-group <dr-rg> \
  --name <asr-vault-name> \
  --location <dr-region>

# Confirm vault exists and is active
az backup vault show \
  --resource-group <dr-rg> \
  --name <asr-vault-name> \
  --query "properties.provisioningState" --output tsv
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg-eastus/providers/Microsoft.RecoveryServices/vaults/asr-vault-prod",
  "location": "eastus",
  "name": "asr-vault-prod",
  "properties": {
    "provisioningState": "Succeeded",
    "publicNetworkAccess": "Enabled",
    "redundancySettings": {
      "standardTierStorageRedundancy": "GeoRedundant"
    }
  },
  "resourceGroup": "dr-rg-eastus",
  "sku": {
    "name": "Standard"
  },
  "tags": null,
  "type": "Microsoft.RecoveryServices/vaults"
}
Succeeded
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceGroupNotFound` | Verify the resource group name with `az group list` and ensure it exists in the target region. |
    | `VaultNameAlreadyExists` | Choose a unique vault name; Recovery Services vault names must be globally unique across Azure. |
    | `InvalidLocation` | Confirm the DR region is valid by running `az account list-locations --query "[].name"` and use the correct region identifier. |
ASR operations are primarily performed through the Azure portal or PowerShell/REST API. The `az` CLI has limited native ASR cmdlets; use the portal or `az rest` for full ASR control.

| Component | Purpose |
|---|---|
| Recovery Services Vault | Container for all ASR configuration and data |
| Replication Policy | Defines RPO, crash-consistent snapshot frequency |
| Network Mapping | Maps source VNets to target VNets |
| Cache Storage Account | Staging area for replication delta data |

---

## Enabling Replication (Azure-to-Azure)

```bash
# Get the source VM resource ID
az vm show \
  --resource-group <source-rg> \
  --name <vm-name> \
  --query id --output tsv

# Use az rest to trigger replication (Azure-to-Azure)
az rest --method PUT \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<source-fabric>/replicationProtectionContainers/<source-container>/replicationProtectedItems/<item-name>?api-version=2022-10-01" \
  --body @enable-replication.json

# List all replicated items
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems?api-version=2022-10-01" \
  --query "value[].{Name:name, Health:properties.replicationHealth, RPO:properties.rpoInSeconds}" \
  --output table
```


```text title="Expected output"
/subscriptions/a1b2c3d4-e5f6-4789-a012-b3c4d5e6f7a8/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-server-01

(no output — command completes silently)

Name                          Health    RPO
------------------------------  --------  -----
web-server-01                  Normal    300
db-server-02                   Warning   1200
app-tier-03                    Normal    300
cache-node-04                  Critical  3600
backup-vm-05                   Normal    300
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationProtectedItems/write' over scope '/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>'` | Assign the user or service principal the "Site Recovery Contributor" role on the Recovery Services vault. |
    | `InvalidResourceId : The provided resource id '<resource-id>' is invalid.` | Verify the subscription ID, resource group name, vault name, and fabric/container names match exactly in the URI. |
    | `MissingRequiredProperty : The request body is missing required property 'properties'.` | Ensure enable-replication.json contains a valid properties object with replication settings like policyId and providerSpecificInput. |
---

## Replication Policy

```bash
# Create a replication policy via az rest
az rest --method PUT \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationPolicies/<policy-name>?api-version=2022-10-01" \
  --body '{
    "properties": {
      "providerSpecificInput": {
        "instanceType": "A2A",
        "multiVmSyncStatus": "Enable"
      }
    }
  }'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg-eastus/providers/Microsoft.RecoveryServices/vaults/prod-vault-01/replicationPolicies/a2a-policy-sync",
  "name": "a2a-policy-sync",
  "type": "Microsoft.RecoveryServices/vaults/replicationPolicies",
  "properties": {
    "friendlyName": "a2a-policy-sync",
    "providerSpecificInput": {
      "instanceType": "A2A",
      "multiVmSyncStatus": "Enable",
      "appConsistentFrequencyInMinutes": 60,
      "crashConsistentFrequencyInMinutes": 5,
      "recoveryPointRetentionInHours": 72
    }
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The provided URI is invalid or the resource does not exist.` | Verify the subscription ID, resource group name, and vault name are correct and exist in your Azure environment. |
    | `Authorization failed for request.` | Ensure your Azure CLI account has the "Site Recovery Contributor" role assigned on the Recovery Services vault. |
    | `Invalid JSON in request body.` | Validate the JSON syntax in the --body parameter and ensure all required properties like instanceType are properly quoted. |
| Policy Setting | Typical Value | Notes |
|---|---|---|
| RPO threshold (minutes) | 30 | Alert trigger threshold |
| App-consistent snapshot frequency (hours) | 4 | Higher = more overhead |
| Crash-consistent snapshot frequency (minutes) | 5 | Minimum recovery granularity |
| Recovery point retention (hours) | 24 | Max 72 for A2A |

---

## Test Failover

Test failover validates the recovery plan without impacting production replication.

```bash
# Trigger a test failover for a replicated item
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<fabric>/replicationProtectionContainers/<container>/replicationProtectedItems/<item-name>/testFailover?api-version=2022-10-01" \
  --body '{
    "properties": {
      "networkId": "<target-vnet-id>",
      "failoverDirection": "PrimaryToRecovery",
      "providerSpecificDetails": {"instanceType": "A2A"}
    }
  }'

# Clean up test failover resources after validation
az rest --method POST \
  --uri "https://management.azure.com/.../testFailoverCleanup?api-version=2022-10-01" \
  --body '{"properties": {"comments": "Test passed, cleaning up"}}'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg-prod/providers/Microsoft.RecoveryServices/vaults/vault-dr-01/replicationFabrics/fabric-primary/replicationProtectionContainers/container-web/replicationProtectedItems/vm-app-01/testFailover/operation-12345",
  "name": "operation-12345",
  "type": "Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/testFailover",
  "properties": {
    "targetObjectId": "vm-app-01-test",
    "jobId": "job-67890abcdef",
    "startTime": "2024-01-15T14:32:18.5432109Z",
    "endTime": null,
    "allowedActions": ["resume", "cancel"],
    "friendlyName": "Test Failover",
    "state": "InProgress",
    "stateDescription": "Test failover is in progress"
  }
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg-prod/providers/Microsoft.RecoveryServices/vaults/vault-dr-01/replicationFabrics/fabric-primary/replicationProtectionContainers/container-web/replicationProtectedItems/vm-app-01/testFailoverCleanup/operation-12346",
  "name": "operation-12346",
  "type": "Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/testFailoverCleanup",
  "properties": {
    "jobId": "job-67890abcdef-cleanup",
    "startTime": "2024-01-15T14:45:22.1234567Z",
    "endTime": "2024-01-15T14:47:33.9876543Z",
    "state": "Succeeded",
    "stateDescription": "Test failover cleanup completed successfully"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `InvalidResourceId: The resource ID is invalid or the resource does not exist.` | Verify all placeholder values (sub-id, dr-rg, vault-name, fabric, container, item-name) are correctly substituted with actual Azure resource names. |
    | `AuthorizationFailed: The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationProtectedItems/testFailover/action'.` | Ensure the user or service principal has the "Site Recovery Contributor" or equivalent role assigned on the Recovery Services vault. |
    | `BadRequest: The test failover request is invalid because the replication item is not in a protected state.` | Confirm the replication item has completed initial replication and is in a "Protected" state before initiating test failover. |
---

## Planned Failover

```bash
# Trigger a planned failover (minimal data loss, coordinated shutdown)
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<fabric>/replicationProtectionContainers/<container>/replicationProtectedItems/<item-name>/plannedFailover?api-version=2022-10-01" \
  --body '{
    "properties": {
      "failoverDirection": "PrimaryToRecovery",
      "providerSpecificDetails": {"instanceType": "A2A"}
    }
  }'

# Monitor job status
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationJobs?api-version=2022-10-01" \
  --query "value[?properties.jobType=='PlannedFailover'].{Name:name, State:properties.state, StartTime:properties.startTime}" \
  --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg-prod/providers/Microsoft.RecoveryServices/vaults/vault-asr-01/replicationJobs/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "name": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "type": "Microsoft.RecoveryServices/vaults/replicationJobs",
  "properties": {
    "jobType": "PlannedFailover",
    "state": "InProgress",
    "startTime": "2024-01-15T14:32:18.5432109Z",
    "endTime": null,
    "allowedActions": ["Cancel"]
  }
}

Name                                  State         StartTime
----                                  -----         ---------
a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d  InProgress    2024-01-15T14:32:18.5432109Z
b2c3d4e5-f6a7-5b6c-9d0e-1f2a3b4c5d6e  Succeeded     2024-01-15T13:45:22.1234567Z
c3d4e5f6-a7b8-6c7d-0e1f-2a3b4c5d6e7f  Succeeded     2024-01-15T12:18:55.9876543Z
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `AuthorizationFailed: The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationJobs/read' over scope '/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>'` | Ensure the service principal or user has the "Site Recovery Contributor" role assigned on the Recovery Services vault. |
    | `ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems/<item-name>' under resource group '<dr-rg>' was not found.` | Verify the protected item name, vault name, and resource group are correct, and that replication is already enabled for this VM. |
    | `BadRequest: The failover direction 'PrimaryToRecovery' is invalid for the current replication state.` | Ensure the VM is in a protected state and meets failover prerequisites (check vault > Replicated items > item status). |
---

## Commit Failover

After a failover, commit the operation to finalize the switch and stop reverse replication from the old primary.

```bash
# Commit failover
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<fabric>/replicationProtectionContainers/<container>/replicationProtectedItems/<item-name>/applyRecoveryPoint?api-version=2022-10-01" \
  --body '{"properties": {"recoveryPointId": "<rp-id>", "providerSpecificDetails": {"instanceType": "A2A"}}}'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg-prod/providers/Microsoft.RecoveryServices/vaults/vault-asr-01/replicationFabrics/fabric-eastus/replicationProtectionContainers/container-vm-01/replicationProtectedItems/vm-app-server-01/recoveryPoints/2024-01-15T14:32:45.1234567Z",
  "name": "2024-01-15T14:32:45.1234567Z",
  "type": "Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/recoveryPoints",
  "properties": {
    "recoveryPointTime": "2024-01-15T14:32:45.1234567Z",
    "recoveryPointType": "ApplicationConsistent",
    "providerSpecificDetails": {
      "instanceType": "A2A",
      "recoveryPointSyncTime": "2024-01-15T14:32:45.1234567Z"
    }
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The provided URI is invalid or the resource does not exist.` | Verify the subscription ID, resource group name, vault name, fabric name, container name, and protected item name are correct and exist in your subscription. |
    | `Invalid recovery point ID specified in the request body.` | Ensure the recovery point ID matches an actual recovery point for the protected item by listing available recovery points with `az rest --method GET --uri "...replicationProtectedItems/<item-name>/recoveryPoints?api-version=2022-10-01"`. |
    | `The operation cannot be performed because the protected item is not in a valid state for failover.` | Check that replication is healthy and the item is not already in a failover state using `az recovery-services-backup protection check-vm`. |
---

## Failback Workflow Summary

| Phase | Action | Tool |
|---|---|---|
| 1. Re-protect | Reverse replication back to primary region | Portal / REST |
| 2. Test failback | Validate primary can host the workload | Portal |
| 3. Planned failover | Switch traffic back to primary | Portal / REST |
| 4. Commit | Finalise failback, stop DR replication | Portal / REST |
| 5. Re-enable DR | Re-enable replication from primary to DR | Portal / REST |
