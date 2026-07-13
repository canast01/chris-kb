---
tags:
  - azure
description: "Policy exemptions allow specific resources, resource groups, or subscriptions to be excluded from policy evaluation. Exemptions are preferred over..."
---
# Policy Exemptions

<div class="kb-summary">
Policy exemptions allow specific resources, resource groups, or subscriptions to be excluded from policy evaluation. Exemptions are preferred over assignment exclusions because they are auditable, time-bound, and can be reviewed independently.

*Applies to: Azure*
</div>

## Exemption Decision Flow

```d2
direction: right

nonCompliant: "Non-compliant Resource\nidentified by policy" {shape: rectangle}
review: "review" {shape: rectangle}
remediate: "Remediate\nfix resource config" {shape: rectangle}
compliant: "Compliant\n✓" {shape: oval}
waiver: "Waiver Category\nknown non-compliance" {shape: rectangle}
mitigated: "Mitigated Category\nalternative control in place" {shape: rectangle}
exempt: "Create Exemption\ntime-bound · documented" {shape: rectangle}
noAction: "Accept Risk\ndocument decision" {shape: rectangle}
justification: "justification" {shape: rectangle}

nonCompliant -> review
remediate -> compliant
waiver -> mitigated
mitigated -> exempt
```

## Creating Exemptions

```bash
# Create an exemption for a specific resource
az policy exemption create \
  --name "legacy-vm-public-ip-exemption" \
  --policy-assignment "/subscriptions/<sub-id>/providers/Microsoft.Authorization/policyAssignments/deny-public-ip" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01" \
  --exemption-category Waiver \
  --display-name "Legacy VM - public IP required until migration" \
  --description "This VM requires a public IP until the migration to private endpoint is complete in Q3 2026" \
  --expires-on 2026-09-30T00:00:00Z

# Create an exemption for an entire resource group
az policy exemption create \
  --name "sandbox-rg-exemption" \
  --policy-assignment "/subscriptions/<sub-id>/providers/Microsoft.Authorization/policyAssignments/require-cost-centre-tag" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-sandbox" \
  --exemption-category Mitigated \
  --display-name "Sandbox RG - tagging not required" \
  --expires-on 2026-12-31T00:00:00Z

# List all exemptions on a subscription
az policy exemption list \
  --scope "/subscriptions/<subscription-id>" \
  --output table

# Show a specific exemption
az policy exemption show \
  --name "legacy-vm-public-ip-exemption" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01"

# Delete an exemption
az policy exemption delete \
  --name "legacy-vm-public-ip-exemption" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01"
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-a012-b3c4d5e6f7a8/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01/providers/Microsoft.Authorization/policyExemptions/legacy-vm-public-ip-exemption",
  "name": "legacy-vm-public-ip-exemption",
  "type": "Microsoft.Authorization/policyExemptions",
  "displayName": "Legacy VM - public IP required until migration",
  "description": "This VM requires a public IP until the migration to private endpoint is complete in Q3 2026",
  "exemptionCategory": "Waiver",
  "expiresOn": "2026-09-30T00:00:00Z",
  "policyAssignmentId": "/subscriptions/a1b2c3d4-e5f6-4789-a012-b3c4d5e6f7a8/providers/Microsoft.Authorization/policyAssignments/deny-public-ip"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-a012-b3c4d5e6f7a8/resourceGroups/rg-sandbox/providers/Microsoft.Authorization/policyExemptions/sandbox-rg-exemption",
  "name": "sandbox-rg-exemption",
  "type": "Microsoft.Authorization/policyExemptions",
  "displayName": "Sandbox RG - tagging not required",
  "exemptionCategory": "Mitigated",
  "expiresOn": "2026-12-31T00:00:00Z",
  "policyAssignmentId": "/subscriptions/a1b2c3d4-e5f6-4789-a012-b3c4d5e6f7a8/providers/Microsoft.Authorization/policyAssignments/require-cost-centre-tag"
}
Name                                  DisplayName                                    ExemptionCategory    ExpiresOn
------------------------------------  -----------------------------------------------  -------------------  ----------
legacy-vm-public-ip-exemption         Legacy VM - public IP required until migration  Waiver               2026-09-30
sandbox-rg-exemption                  Sandbox RG - tagging not required               Mitigated            2026-12-31
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-a012-b3c4d5e6f7a8/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01/providers/Microsoft.Authorization/policyExemptions/legacy-vm-public-ip-exemption",
  "name": "legacy-vm-public-ip-exemption",
  "displayName": "Legacy VM - public IP required until migration",
  "exemptionCategory": "Waiver",
  "expiresOn": "2026-09-30T00:00:00Z"
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`The policy assignment '/subscriptions/<sub-id>/providers/Microsoft.Authorization/policyAss
## Waiver vs Mitigated

The exemption category communicates the rationale for the exemption and is important for audit purposes.

| Category | Meaning | Example |
|---|---|---|
| `Waiver` | The policy intent does not apply to this resource | Deny-public-IP exempted for a bastion jumpbox |
| `Mitigated` | The policy intent is satisfied through an alternative control | No diagnostic settings because logs go to a 3rd-party SIEM instead |

Always choose the correct category — auditors use this field to assess the validity of exemptions.

## Expiry

All exemptions should have an expiry date. Azure evaluates the `expiresOn` field and automatically re-applies policy evaluation when the exemption expires.

```bash
# Update an exemption to extend its expiry
az policy exemption update \
  --name "legacy-vm-public-ip-exemption" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01" \
  --expires-on 2026-12-31T00:00:00Z

# List exemptions expiring within 30 days (manual filter using query)
az policy exemption list \
  --scope "/subscriptions/<subscription-id>" \
  --query "[?expiresOn != null].{Name:name, Scope:id, Expiry:expiresOn, Category:exemptionCategory}" \
  --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01/providers/Microsoft.Authorization/policyExemptions/legacy-vm-public-ip-exemption",
  "name": "legacy-vm-public-ip-exemption",
  "type": "Microsoft.Authorization/policyExemptions",
  "properties": {
    "policyAssignmentId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/audit-public-ip",
    "exemptionCategory": "Waived",
    "expiresOn": "2026-12-31T00:00:00Z",
    "displayName": "Legacy VM Public IP Exemption",
    "description": "Exemption for legacy VM migration period"
  }
}

Name                                  Scope                                                                                                                                                 Expiry                    Category
------------------------------------  -----------------------------------------------------------------------------------------------------------------------------------------------------  ------------------------  ----------
legacy-vm-public-ip-exemption         /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01             2026-12-31T00:00:00Z      Waived
storage-encryption-exemption          /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-prod/providers/Microsoft.Storage/storageAccounts/stgprod01                  2025-06-15T00:00:00Z      Mitigated
network-nsg-exemption                 /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-network                                                                      2025-02-28T00:00:00Z      Waived
```

!!! warning "Common errors"
    **`The provided scope is invalid.`** — Verify the subscription ID and resource group name are correct, and that the resource exists in the specified scope.
    **`The policy exemption 'legacy-vm-public-ip-exemption' was not found.`** — Confirm the exemption name matches exactly and exists in the target scope before attempting to update.
    **`The date format is invalid. Expected format: YYYY-MM-DDTHH:MM:SSZ`** — Use ISO 8601 format with UTC timezone (Z suffix) for the `--expires-on` parameter.
### Exemption Lifecycle

| Stage | Action |
|---|---|
| Request | Engineer submits exemption request with justification and owner |
| Approval | Governance lead reviews and approves with expiry date |
| Creation | Exemption created via CLI with category, description, and expiry |
| Review | Exemption reviewed at 60-day mark; extended or planned for removal |
| Expiry | Azure automatically removes the exemption; policy re-applies |

## Audit Trail

Exemption creation, updates, and deletions are recorded in the Azure Activity Log. Use this for audit evidence.

```bash
# Query Activity Log for exemption operations
az monitor activity-log list \
  --subscription <subscription-id> \
  --resource-provider "Microsoft.Authorization" \
  --query "[?contains(operationName.value, 'policyExemptions')].{Time:eventTimestamp, Operation:operationName.value, Caller:caller, Status:status.value}" \
  --output table \
  --start-time 2026-05-01T00:00:00Z
```


```text title="Expected output"
Time                          Operation                                    Caller                           Status
2026-05-15T14:32:18.456789Z   Microsoft.Authorization/policyExemptions/write  user@contoso.com                 Succeeded
2026-05-14T09:17:42.123456Z   Microsoft.Authorization/policyExemptions/write  automation-svc@contoso.onmicrosoft.com  Succeeded
2026-05-12T16:45:33.789012Z   Microsoft.Authorization/policyExemptions/delete  admin@contoso.com                Succeeded
2026-05-10T11:22:05.345678Z   Microsoft.Authorization/policyExemptions/write  user@contoso.com                 Succeeded
2026-05-08T08:19:51.901234Z   Microsoft.Authorization/policyExemptions/read   audit-reader@contoso.com        Succeeded
```

!!! warning "Common errors"
    **`ERROR: The subscription '<subscription-id>' could not be found.`** — Replace `<subscription-id>` with your actual Azure subscription ID or run `az account show --query id` to retrieve it.
    **`ERROR: The following arguments are required: --subscription`** — Provide the `--subscription` parameter with a valid subscription ID or set the default subscription using `az account set --subscription <id>`.
    **`ERROR: The time format is invalid. Valid formats are: 'YYYY-MM-DDTHH:MM:SSZ' or 'YYYY-MM-DD HH:MM:SS'.`** — Ensure the `--start-time` value uses ISO 8601 format (e.g., `2026-05-01T00:00:00Z`) with a valid date.
## Exemption Best Practices

| Practice | Rationale |
|---|---|
| Always set an expiry date | Prevents exemptions from becoming permanent by default |
| Use `Mitigated` where possible | Shows compensating control exists; easier to justify in audit |
| Include ticket/Jira reference in description | Links exemption to an approved work item |
| Review all exemptions quarterly | Catch expired justifications and unnecessary exemptions |
| Scope as narrowly as possible | Resource-level is preferable to resource-group-level |
