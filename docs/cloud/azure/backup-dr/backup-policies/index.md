---
tags:
  - azure
description: "Backup policies define when backups run, how many recovery points are retained, and at what tiers"
---
# Backup Policies

<div class="kb-summary">
Backup policies define when backups run, how many recovery points are retained, and at what tiers

*Applies to: Azure*
</div>

---

```d2
direction: down

creating_a_vm_backup_policy: "Creating a VM Backup Policy" {shape: rectangle}
retention_rules_reference: "Retention Rules Reference" {shape: rectangle}
modifying_an_existing_policy: "Modifying an Existing Policy" {shape: rectangle}
assigning_a_policy_to_protected_item: "Assigning a Policy to Protected Items" {shape: rectangle}
deleting_a_policy: "Deleting a Policy" {shape: rectangle}

creating_a_vm_backup_policy -> retention_rules_reference: uses
retention_rules_reference -> modifying_an_existing_policy: uses
modifying_an_existing_policy -> assigning_a_policy_to_protected_item: uses
assigning_a_policy_to_protected_item -> deleting_a_policy: uses
```

## Creating a VM Backup Policy

Policies are defined in JSON. Below is a minimal daily VM backup policy template.

```json
{
  "eTag": null,
  "location": "eastus",
  "properties": {
    "backupManagementType": "AzureIaasVM",
    "instantRpRetentionRangeInDays": 2,
    "schedulePolicy": {
      "schedulePolicyType": "SimpleSchedulePolicy",
      "scheduleRunFrequency": "Daily",
      "scheduleRunTimes": ["2026-01-01T02:00:00Z"]
    },
    "retentionPolicy": {
      "retentionPolicyType": "LongTermRetentionPolicy",
      "dailySchedule": {
        "retentionTimes": ["2026-01-01T02:00:00Z"],
        "retentionDuration": {"count": 30, "durationType": "Days"}
      },
      "weeklySchedule": {
        "daysOfTheWeek": ["Sunday"],
        "retentionTimes": ["2026-01-01T02:00:00Z"],
        "retentionDuration": {"count": 12, "durationType": "Weeks"}
      },
      "monthlySchedule": {
        "retentionScheduleFormatType": "Weekly",
        "retentionScheduleWeekly": [{"daysOfTheWeek": ["Sunday"], "weeksOfTheMonth": ["First"]}],
        "retentionTimes": ["2026-01-01T02:00:00Z"],
        "retentionDuration": {"count": 12, "durationType": "Months"}
      }
    },
    "timeZone": "UTC"
  }
}
```

```bash
# Create the policy from the JSON file
az backup policy create \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <policy-name> \
  --policy @vm-backup-policy.json \
  --backup-management-type AzureIaasVM
```


```text title="Expected output"
Command group 'backup policy' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-backup-rg/providers/Microsoft.RecoveryServices/vaults/prod-vault-01/backupPolicies/vm-daily-backup-policy",
  "name": "vm-daily-backup-policy",
  "properties": {
    "backupManagementType": "AzureIaasVM",
    "schedulePolicy": {
      "schedulePolicyType": "SimpleSchedulePolicy",
      "scheduleRunFrequency": "Daily",
      "scheduleRunTimes": [
        "2024-01-15T02:00:00Z"
      ]
    },
    "retentionPolicy": {
      "retentionPolicyType": "LongTermRetentionPolicy",
      "dailySchedule": {
        "retentionTimes": [
          "2024-01-15T02:00:00Z"
        ],
        "retentionDuration": {
          "count": 30,
          "durationType": "Days"
        }
      }
    }
  },
  "type": "Microsoft.RecoveryServices/vaults/backupPolicies"
}
```

!!! warning "Common errors"
    **`Invalid template member reference 'vm-backup-policy.json'. Specify the correct path to the file.`** — Verify the JSON file exists in the current directory and use the correct relative or absolute path.
    **`The policy definition in the JSON file is invalid. Error: Missing required property 'schedulePolicy'.`** — Ensure the JSON file contains all required properties including `schedulePolicy`, `retentionPolicy`, and `backupManagementType`.
    **`The specified resource group '<rg>' could not be found.`** — Replace `<rg>` with an actual resource group name that exists in your subscription.
---

## Retention Rules Reference

| Tier | Minimum | Maximum | Notes |
|---|---|---|---|
| Snapshot (instant restore) | 1 day | 5 days | Stored in the resource group |
| Daily vault | 7 days | 9999 days | Stored in the Recovery Services Vault |
| Weekly vault | 1 week | 5163 weeks | Each Sunday (or chosen day) |
| Monthly vault | 1 month | 1188 months | First/last week of month |
| Yearly vault | 1 year | 99 years | Specified month and week |

---

## Modifying an Existing Policy

```bash
# Export the current policy to a file for editing
az backup policy show \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <policy-name> > current-policy.json

# Apply the modified policy (overwrites existing)
az backup policy set \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <policy-name> \
  --policy @current-policy.json
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-backup-rg/providers/Microsoft.RecoveryServices/vaults/prod-vault-01/backupPolicies/DailyBackupPolicy",
  "name": "DailyBackupPolicy",
  "type": "Microsoft.RecoveryServices/vaults/backupPolicies",
  "properties": {
    "backupManagementType": "AzureIaasVM",
    "schedulePolicy": {
      "schedulePolicyType": "SimpleSchedulePolicy",
      "scheduleRunFrequency": "Daily",
      "scheduleRunTimes": [
        "2024-01-15T02:00:00Z"
      ]
    },
    "retentionPolicy": {
      "retentionPolicyType": "LongTermRetentionPolicy",
      "dailySchedule": {
        "retentionTimes": [
          "2024-01-15T02:00:00Z"
        ],
        "retentionDuration": {
          "count": 30,
          "durationType": "Days"
        }
      }
    }
  }
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ResourceNotFound: The specified backup policy 'DailyBackupPolicy' was not found in vault 'prod-vault-01'.`** — Verify the policy name matches exactly with `az backup policy list --resource-group <rg> --vault-name <vault-name>`.
    **`InvalidJsonInput: The JSON file 'current-policy.json' is malformed or missing required fields.`** — Ensure the exported JSON is valid by running `jq empty current-policy.json` before applying, and do not remove required fields like `schedulePolicy` or `retentionPolicy`.
    **`AuthorizationFailed: The user does not have permission to modify backup policies in this vault.`** — Confirm your account has the "Backup Operator" or "Contributor" role on the Recovery Services vault using `az role assignment list --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>`.
---

## Assigning a Policy to Protected Items

```bash
# Change the policy for an already-protected VM
az backup item set-policy \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --container-name <container-name> \
  --name <vm-name> \
  --backup-management-type AzureIaasVM \
  --workload-type VM \
  --policy-name <new-policy-name>

# List items using a specific policy
az backup item list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --query "[?properties.policyId contains '<policy-name>'].{Name:name, State:properties.protectionState}" \
  --output table
```


```text title="Expected output"
Name                             State
---------------------------------  ----------------
prod-web-vm-01                    Protected
prod-web-vm-02                    Protected
prod-db-vm-03                    Protected
staging-app-vm-01                Protected
dev-test-vm-02                   ProtectionStopped
```

!!! warning "Common errors"
    **`The item with name '<vm-name>' not found in the container '<container-name>'`** — Verify the VM name and container name match exactly using `az backup container list` and `az backup item list`.
    **`The policy with name '<new-policy-name>' does not exist in the vault`** — Confirm the policy exists in the vault with `az backup policy list --resource-group <rg> --vault-name <vault-name>`.
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>' under resource group '<rg>' was not found`** — Ensure the vault name and resource group are correct and the vault exists in your subscription.
---

## Deleting a Policy

```bash
# Delete a policy (only if no items are assigned to it)
az backup policy delete \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --name <policy-name>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`The policy 'DailyBackupPolicy' cannot be deleted because it is still associated with 1 protected item(s).`** — Disassociate or delete all backup items using this policy before attempting deletion.
    **`ResourceNotFound: The resource 'Microsoft.RecoveryServices/vaults/<vault-name>/backupPolicies/<policy-name>' does not exist.`** — Verify the policy name is correct and exists in the specified vault using `az backup policy list`.