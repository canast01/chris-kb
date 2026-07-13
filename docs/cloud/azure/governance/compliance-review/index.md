---
tags:
  - azure
description: "Azure Policy compliance reviews evaluate the current state of resources against assigned policies and surface non-compliant resources. Regular compliance..."
---
# Compliance Review

<div class="kb-summary">
Azure Policy compliance reviews evaluate the current state of resources against assigned policies and surface non-compliant resources. Regular compliance reviews are essential for maintaining governance standards and preparing for audits.

*Applies to: Azure*
</div>

## Compliance Review Cycle

```d2
direction: right

trigger: "Compliance Scan\nscheduled daily or on-demand" {shape: rectangle}
evaluate: "Policy Evaluation\nall resources vs all assignments" {shape: rectangle}
dashboard: "Compliance Dashboard\n% compliant per assignment" {shape: rectangle}
nonCompliant: "nonCompliant" {shape: rectangle}
remediate: "Create Remediation Task\nor manual fix" {shape: rectangle}
exempt: "Create Exemption\nif justified" {shape: rectangle}
report: "Compliance Report\nexport for audit" {shape: rectangle}

trigger -> evaluate
evaluate -> dashboard
dashboard -> nonCompliant
remediate -> exempt
remediate -> trigger
```

## Compliance Dashboard

The compliance dashboard in the portal shows an overall compliance percentage and breaks it down by policy assignment. Use the CLI for scripted reporting.

```bash
# Get overall compliance summary for a subscription
az policy state summarize \
  --subscription <subscription-id>

# Get compliance summary at management group scope
az policy state summarize \
  --management-group <mg-id>

# Trigger an on-demand compliance scan
az policy state trigger-scan \
  --subscription <subscription-id>

# Trigger scan for a specific resource group
az policy state trigger-scan \
  --resource-group rg-production
```


```text title="Expected output"
{
  "policyDefinitionGroupNames": [
    "Compute",
    "Storage",
    "Networking",
    "Identity"
  ],
  "results": {
    "nonCompliantResources": 12,
    "compliantResources": 287,
    "resourceDetails": [
      {
        "resourceId": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-production/providers/Microsoft.Compute/virtualMachines/vm-web-01",
        "complianceState": "NonCompliant",
        "policyAssignmentId": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/audit-encryption-policy"
      },
      {
        "resourceId": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-production/providers/Microsoft.Storage/storageAccounts/stgprod001",
        "complianceState": "NonCompliant",
        "policyAssignmentId": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/require-https-only"
      }
    ]
  }
}
Scan trigger request accepted for subscription a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d
Scan trigger request accepted for resource group rg-production
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The subscription 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' could not be found.` | Verify the subscription ID is correct and you have access to it using `az account show`. |
    | `ResourceGroupNotFound: The resource group 'rg-production' could not be found in the subscription.` | Confirm the resource group name exists in the target subscription with `az group list`. |
    | `AuthorizationFailed: The client 'user@contoso.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have authorization to perform action 'Microsoft.PolicyInsights/policyStates/triggerScan/action'.` | Ensure your account has the Policy Insights Contributor or higher role assigned at the subscription or management group scope. |
### Compliance State Values

| State | Description |
|---|---|
| Compliant | Resource satisfies all assigned policy conditions |
| NonCompliant | Resource violates at least one policy condition |
| Exempt | Resource has an active policy exemption |
| Conflict | Two policies produce conflicting evaluations |
| Not started | Evaluation has not yet run for this resource |

## Non-Compliant Resources

```bash
# List all non-compliant resources in a subscription
az policy state list \
  --subscription <subscription-id> \
  --filter "complianceState eq 'NonCompliant'" \
  --output table

# Non-compliant resources for a specific policy assignment
az policy state list \
  --filter "policyAssignmentName eq 'deny-public-ip' and complianceState eq 'NonCompliant'" \
  --output table

# Non-compliant resources with reason
az policy state list \
  --subscription <subscription-id> \
  --filter "complianceState eq 'NonCompliant'" \
  --query "[].{Resource:resourceId, Policy:policyDefinitionName, Reason:policyDefinitionReferenceId}" \
  --output table

# Count of non-compliant resources per policy
az policy state summarize \
  --subscription <subscription-id> \
  --query "value[0].policyAssignments[].{Policy:policyAssignmentName, NonCompliant:results.nonCompliantResources}" \
  --output table
```


```text title="Expected output"
ResourceId                                                          PolicyAssignmentId                                                       ComplianceState
------------------------------------------------------------------------------------------------------------------------------------  --------
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01  /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/deny-public-ip  NonCompliant
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Network/networkInterfaces/nic-web-01  /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/deny-public-ip  NonCompliant
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/dev-rg/providers/Microsoft.Storage/storageAccounts/devstg2024  /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/require-encryption  NonCompliant

ResourceId                                                          Policy                           Reason
------------------------------------------------------------------------------------------------------------------------------------  --------------------------------  --------
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01  Deny Public IP Assignment         PublicIPNotAllowed
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/dev-rg/providers/Microsoft.Storage/storageAccounts/devstg2024  Require Storage Encryption        EncryptionNotEnabled

Policy                           NonCompliant
--------------------------------  --------
deny-public-ip                    3
require-encryption                7
require-https-only                2
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: The subscription '<subscription-id>' could not be found.` | Replace `<subscription-id>` with an actual subscription ID or use `az account set --subscription <id>` to set the default subscription. |
    | `ERROR: No registered resource providers found for location 'eastus'.` | Ensure the subscription is active and you have Reader permissions; run `az account show` to verify authentication. |
    | `ERROR: The filter expression is invalid.` | Verify filter syntax uses valid OData operators (`eq`, `and`, `or`) and valid property names like `complianceState` and `policyAssignmentName`. |
## Remediation Tasks

Policies with `deployIfNotExists` or `modify` effects can create remediation tasks to bring non-compliant resources into compliance automatically.

```bash
# Create a remediation task for a policy assignment
az policy remediation create \
  --name "remediate-diag-settings" \
  --policy-assignment "/subscriptions/<sub-id>/providers/Microsoft.Authorization/policyAssignments/deploy-diag-settings" \
  --resource-discovery-mode ReEvaluateCompliance

# Create a remediation task for a specific resource group
az policy remediation create \
  --name "remediate-tags-rg" \
  --policy-assignment "/subscriptions/<sub-id>/providers/Microsoft.Authorization/policyAssignments/inherit-env-tag" \
  --resource-group rg-production

# List remediation tasks
az policy remediation list \
  --subscription <subscription-id> \
  --output table

# Show status of a remediation task
az policy remediation show \
  --name "remediate-diag-settings" \
  --subscription <subscription-id>

# Cancel a running remediation task
az policy remediation cancel \
  --name "remediate-diag-settings" \
  --subscription <subscription-id>
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyRemediations/remediate-diag-settings",
  "name": "remediate-diag-settings",
  "type": "Microsoft.Authorization/policyRemediations",
  "properties": {
    "policyAssignmentId": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/deploy-diag-settings",
    "resourceDiscoveryMode": "ReEvaluateCompliance",
    "provisioningState": "Succeeded",
    "createdOn": "2024-01-15T10:32:45.123456Z"
  }
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-production/providers/Microsoft.Authorization/policyRemediations/remediate-tags-rg",
  "name": "remediate-tags-rg",
  "type": "Microsoft.Authorization/policyRemediations",
  "properties": {
    "policyAssignmentId": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/inherit-env-tag",
    "resourceDiscoveryMode": "ExistingNonCompliant",
    "provisioningState": "Succeeded",
    "createdOn": "2024-01-15T10:33:12.456789Z"
  }
}
Name                    Type                                    ProvisioningState    CreatedOn
----------------------  ------                                  ------------------   -----------------------
remediate-diag-settings Microsoft.Authorization/policyRemediations  Succeeded            2024-01-15T10:32:45Z
remediate-tags-rg       Microsoft.Authorization/policyRemediations  Succeeded            2024-01-15T10:33:12Z
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyRemediations/remediate-diag-settings",
  "name": "remediate-diag-settings",
  "properties": {
    "policyAssignmentId": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/deploy-diag-settings",
    "resourceDiscoveryMode": "ReEvaluateCompliance",
    "provisioningState": "Succeeded",
    "deploymentSummary": {
      "totalDeployments": 12,
      "successfulDeployments": 11,
```
### Remediation Task States

| State | Description |
|---|---|
| Queued | Task created; waiting to start |
| Running | Actively remediating resources |
| Succeeded | All targeted resources remediated |
| Failed | One or more remediations failed |
| Canceled | Task was manually cancelled |

## Compliance Review Cadence

| Review Type | Frequency | Scope | Owner |
|---|---|---|---|
| Automated scan | Daily (triggered by deployment) | All subscriptions | Platform team |
| Non-compliant triage | Weekly | New non-compliant resources | Governance lead |
| Remediation sprint | Monthly | Backlog of non-compliant resources | All engineering teams |
| Audit preparation | Quarterly | Full compliance posture + exemptions review | Security + Governance |

## Exporting Compliance Data

```bash
# Export all compliance states to JSON for audit reporting
az policy state list \
  --subscription <subscription-id> \
  --output json > compliance-$(date +%Y%m%d).json

# Export non-compliant only
az policy state list \
  --subscription <subscription-id> \
  --filter "complianceState eq 'NonCompliant'" \
  --output json > non-compliant-$(date +%Y%m%d).json
```


```text title="Expected output"
compliance-20240115.json
non-compliant-20240115.json
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: The subscription of the context does not match the subscription in the request. Subscription id: 12345678-1234-1234-1234-123456789012` | Replace `<subscription-id>` with your actual subscription ID or run `az account show --query id -o tsv` to retrieve it. |
    | `ERROR: This operation requires a minimum CLI version of 2.50.0. You have 2.45.0` | Update Azure CLI with `az upgrade` to access the latest policy state filtering options. |
    | `ERROR: Authorization failed: User does not have permission to read policy compliance states` | Ensure your account has the "Policy Insights Data Writer" or "Reader" role assigned at the subscription scope using `az role assignment create`. |