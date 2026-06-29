---
tags:
  - azure
---
# Failback

<div class="kb-summary">
Failback is the process of returning protected workloads from the DR (recovery) region back to the primary region after a failover event.

*Applies to: Azure*
</div>

 In Azure Site Recovery, failback consists of re-protecting the DR VM, running a planned failover toward the primary, then committing and re-enabling replication.

---

## ASR Failover and Failback Flow

```d2
direction: right

primary: "Primary Region\nVM running (protected" {shape: rectangle}
replication: "Continuous Replication\nASR — RPO ~30s" {shape: rectangle}
failover: "Failover\nDR Region VM starts" {shape: rectangle}
commit: "Commit Failover\ncut primary loose" {shape: rectangle}
reprotect: "Re-protect\nreplicate DR → Primary" {shape: rectangle}
failback: "Planned Failover\nback to Primary" {shape: rectangle}
reprotectFwd: "Re-protect Forward\nresume Primary → DR" {shape: rectangle}

primary -> replication
replication -> failover
failover -> commit
commit -> reprotect
reprotect -> failback
failback -> reprotectFwd
```

## Failback Prerequisites

Before initiating failback, confirm:

| Requirement | Verification |
|---|---|
| Failover has been committed in ASR | Check replicated item state = "Failover committed" |
| Primary region infrastructure is ready | VMs, VNets, NSGs exist or are re-created |
| Network connectivity from DR to primary | VNet peering or VPN gateway routes confirmed |
| Recovery Services Vault accessible | `az backup vault show` returns Succeeded |

```bash
# Confirm vault in DR region is accessible
az backup vault show \
  --resource-group <dr-rg> \
  --name <asr-vault-name> \
  --query "properties.provisioningState" --output tsv

# Confirm current replication state via REST
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems?api-version=2022-10-01" \
  --query "value[].{Name:name, Health:properties.replicationHealth, FailoverState:properties.failoverHealth}" \
  --output table
```


```text title="Expected output"
Succeeded
Name                                          Health    FailoverState
────────────────────────────────────────────  ────────  ─────────────
vm-prod-app-01                                Normal    Ready
vm-prod-db-01                                 Normal    Ready
vm-prod-web-02                                Normal    Ready
vm-prod-cache-01                              Normal    Ready
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<asr-vault-name>' under resource group '<dr-rg>' was not found.`** — Verify the vault name and DR resource group name match your deployment, and confirm the vault exists in the correct subscription.
    
    **`AuthorizationFailed: The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/read' over scope '/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>'.`** — Ensure your Azure account has Reader or Contributor role assigned to the DR resource group or subscription.
    
    **`InvalidResourceId: The provided URI is not valid.`** — Replace `<sub-id>`, `<dr-rg>`, and `<vault-name>` placeholders with actual values; do not include angle brackets in the final command.
---

## Phase 1 — Re-Protect (Reverse Replication)

Re-protection sets up replication from the DR region back to the primary region. This must complete before failback can proceed.

```bash
# Trigger re-protect on a replicated item (DR → Primary)
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<dr-fabric>/replicationProtectionContainers/<dr-container>/replicationProtectedItems/<item-name>/reProtect?api-version=2022-10-01" \
  --body '{
    "properties": {
      "failoverDirection": "RecoveryToPrimary",
      "providerSpecificDetails": {
        "instanceType": "A2A",
        "recoveryContainerId": "<primary-container-id>"
      }
    }
  }'

# Monitor re-protect job
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationJobs?api-version=2022-10-01" \
  --query "value[?properties.jobType=='ReProtect'].{Name:name, State:properties.state, StartTime:properties.startTime}" \
  --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/a7f3c8d2-1e4b-4f9a-8c2d-5e9b1a3c7d4f/resourceGroups/dr-rg-eastus/providers/Microsoft.RecoveryServices/vaults/prod-vault-01/replicationJobs/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "name": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "type": "Microsoft.RecoveryServices/vaults/replicationJobs",
  "properties": {
    "jobType": "ReProtect",
    "state": "InProgress",
    "startTime": "2024-01-15T14:32:18.5432109Z"
  }
}

Name                                      State        StartTime
----------------------------------------  -----------  --------------------------
a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d    InProgress   2024-01-15T14:32:18.543Z
b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e    Succeeded    2024-01-15T13:47:22.891Z
c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f    Failed       2024-01-15T12:15:09.127Z
```

!!! warning "Common errors"
    **`AuthorizationFailed: The client 'user@contoso.com' with object id 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationProtectedItems/reProtect/action'`** — Assign the user or service principal the "Site Recovery Operator" or "Contributor" role on the Recovery Services vault.
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems/<item-name>' under resource group '<dr-rg>' was not found`** — Verify the item name, vault name, and resource group are correct, and that the replicated item exists in the DR fabric.
    **`BadRequest: The failover direction 'RecoveryToPrimary' is invalid for the current replication state of the protected item`** — Ensure the VM has completed initial replication and is in a "Protected" state before attempting re-protect.
---

## Phase 2 — Validate Replication Health Before Failback

```bash
# Check RPO and replication health after re-protect
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems/<item-name>?api-version=2022-10-01" \
  --query "properties.{Health:replicationHealth, RPO:rpoInSeconds, LastSync:lastSuccessfulTestFailoverTime}" \
  --output json
```


```text title="Expected output"
{
  "Health": "Normal",
  "RPO": 300,
  "LastSync": "2024-01-15T14:32:18.5847392Z"
}
```

!!! warning "Common errors"
    **`AuthorizationFailed: The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationProtectedItems/read' over scope '/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems/<item-name>'`** — Ensure your Azure account has Reader or Site Recovery Contributor role assigned on the Recovery Services vault.
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems/<item-name>' under resource group '<dr-rg>' was not found.`** — Verify the vault name, resource group name, and protected item name match exactly; check they exist in the correct subscription.
    **`InvalidApiVersionParameter: The api-version '2022-10-01' is invalid.`** — Update the api-version parameter to a currently supported version such as '2023-08-01' or later.
| Metric | Acceptable Threshold |
|---|---|
| Replication health | Normal |
| RPO (seconds) | < 300 (5 minutes) |
| Last sync age | < 15 minutes |
| Data change rate | Within cache storage capacity |

---

## Phase 3 — Planned Failover (Back to Primary)

```bash
# Trigger planned failover back to the primary region
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<dr-fabric>/replicationProtectionContainers/<dr-container>/replicationProtectedItems/<item-name>/plannedFailover?api-version=2022-10-01" \
  --body '{
    "properties": {
      "failoverDirection": "RecoveryToPrimary",
      "providerSpecificDetails": {"instanceType": "A2A"}
    }
  }'
```


```text title="Expected output"
{
  "id": "/subscriptions/a7f3e2c1-4b9d-47e8-9f2a-8c5d6e1b3a4f/resourceGroups/dr-rg-eastus/providers/Microsoft.RecoveryServices/vaults/prod-vault-01/replicationFabrics/eastus-fabric/replicationProtectionContainers/dr-container-01/replicationProtectedItems/vm-app-prod-01/plannedFailover",
  "name": "vm-app-prod-01",
  "type": "Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/plannedFailover",
  "properties": {
    "failoverDirection": "RecoveryToPrimary",
    "providerSpecificDetails": {
      "instanceType": "A2A",
      "recoveryPointId": "2024-01-15T14:32:18.5847392Z"
    },
    "startTime": "2024-01-15T14:32:45.123Z",
    "state": "InProgress"
  }
}
```

!!! warning "Common errors"
    **`AuthorizationFailed: The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/plannedFailover/action' over scope`** — Assign the Site Recovery Contributor role to your service principal or user account on the Recovery Services vault.
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<dr-fabric>/replicationProtectionContainers/<dr-container>/replicationProtectedItems/<item-name>' under resource group '<dr-rg>' was not found`** — Verify the subscription ID, resource group name, vault name, fabric name, container name, and protected item name are correct and exist in the specified region.
    **`BadRequest: The failover operation cannot be performed because the replication state is not 'Protected'`** — Ensure the protected item has completed initial replication and is in a Protected state before attempting planned failover.
---

## Phase 4 — Commit Failback

Once the primary VM is running and healthy, commit the failback to clean up the DR replica.

```bash
# Commit the failback
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<dr-fabric>/replicationProtectionContainers/<dr-container>/replicationProtectedItems/<item-name>/failoverCommit?api-version=2022-10-01"
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg-prod/providers/Microsoft.RecoveryServices/vaults/vault-dr-01/replicationFabrics/fabric-dr-secondary/replicationProtectionContainers/container-dr-01/replicationProtectedItems/vm-app-prod-01/failoverCommit",
  "name": "vm-app-prod-01",
  "type": "Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems",
  "properties": {
    "friendlyName": "vm-app-prod-01",
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
    **`The provided URI is invalid or the resource does not exist.`** — Verify the subscription ID, resource group name, vault name, fabric name, container name, and item name are correct and exist in your subscription.
    **`Authorization failed for request. Caller was not authorized to perform 'Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/failoverCommit/action' action over scope.`** — Ensure your Azure account has the Site Recovery Contributor role or equivalent permissions on the Recovery Services vault.
    **`The failover commit operation cannot be performed because the item is not in a committed failover state.`** — Run the failover operation first before attempting to commit; verify the item status is in "Failover Committed" state using `az rest --method GET` on the same URI.
---

## Phase 5 — Re-Enable DR Replication (Primary → DR)

After a successful failback, re-enable replication in the forward direction so DR protection is restored.

```bash
# Re-protect (now from primary to DR) to restore DR posture
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<primary-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<primary-fabric>/replicationProtectionContainers/<primary-container>/replicationProtectedItems/<item-name>/reProtect?api-version=2022-10-01" \
  --body '{
    "properties": {
      "failoverDirection": "PrimaryToRecovery",
      "providerSpecificDetails": {"instanceType": "A2A"}
    }
  }'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-primary-rg/providers/Microsoft.RecoveryServices/vaults/dr-vault-001/replicationFabrics/primary-fabric-eastus/replicationProtectionContainers/primary-container-001/replicationProtectedItems/vm-app-server-01/reProtect/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "name": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "type": "Microsoft.RecoveryServices/vaults/replicationFabrics/replicationProtectionContainers/replicationProtectedItems/reProtect",
  "properties": {
    "friendlyName": "vm-app-server-01",
    "name": "vm-app-server-01",
    "currentScenario": {
      "scenarioName": "A2A",
      "jobId": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
      "startTime": "2024-01-15T10:32:45.1234567Z"
    },
    "replicationStatus": "Protected",
    "failoverDirection": "PrimaryToRecovery"
  }
}
```

!!! warning "Common errors"
    **`AuthorizationFailed: The client 'user@contoso.com' with object id 'a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d' does not have permission to perform action 'Microsoft.RecoveryServices/vaults/replicationProtectedItems/reProtect/action'`** — Ensure the user or service principal has the "Site Recovery Operator" or "Contributor" role on the Recovery Services vault.
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<primary-fabric>/replicationProtectionContainers/<primary-container>/replicationProtectedItems/<item-name>' under resource group '<primary-rg>' was not found.`** — Verify the subscription ID, resource group name, vault name, fabric name, container name, and protected item name are correct and exist in the target region.
---

## Failback Checklist

| Step | Action | Status |
|---|---|---|
| 1 | Primary region infrastructure validated | |
| 2 | Re-protect job completed successfully | |
| 3 | RPO within threshold after re-protect | |
| 4 | Test failback validated (optional) | |
| 5 | Planned failover to primary completed | |
| 6 | Primary VM health checks passed | |
| 7 | Failback committed | |
| 8 | Forward replication (Primary → DR) re-enabled | |
| 9 | Stakeholders notified of recovery | |
