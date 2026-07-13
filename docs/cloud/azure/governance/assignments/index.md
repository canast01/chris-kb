---
tags:
  - azure
description: "A policy assignment connects a policy definition or initiative (policy set) to a specific scope in the Azure hierarchy. The assignment is the mechanism..."
---
# Policy and Initiative Assignments

<div class="kb-summary">
A policy assignment connects a policy definition or initiative (policy set) to a specific scope in the Azure hierarchy. The assignment is the mechanism that makes a policy active and enforceable.

*Applies to: Azure*
</div>

## Policy Assignment Scope Hierarchy

```d2
direction: right

mgScope: "Management Group Scope\nbroadest — all child subs inherit" {shape: rectangle}
subScope: "Subscription Scope\napplies to all RGs in subscription" {shape: rectangle}
rgScope: "Resource Group Scope\napplies to all resources in RG" {shape: rectangle}
resourceScope: "Resource Scope\nnarrowest — single resource only" {shape: rectangle}
exempt: "Exemption\nwaiver for specific scope or resource" {shape: rectangle}

mgScope -> subScope
subScope -> rgScope
rgScope -> resourceScope
```

## Creating a Policy Assignment

```bash
# Assign a built-in policy by definition ID
az policy assignment create \
  --name "deny-public-ip" \
  --policy "9daedab3-fb2d-461e-b861-71790eead4f6" \
  --scope "/subscriptions/<subscription-id>" \
  --description "Deny creation of public IP addresses" \
  --display-name "Deny Public IP Addresses"

# Assign policy at resource group scope
az policy assignment create \
  --name "require-tags-rg" \
  --policy "96670d01-0a4d-4649-9c89-2d3abc0a5025" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-production" \
  --params '{"tagName": {"value": "environment"}}'

# Assign policy at management group scope
az policy assignment create \
  --name "audit-storage-https" \
  --policy "404c3081-a854-4457-ae30-26a93ef643f9" \
  --scope "/providers/Microsoft.Management/managementGroups/mg-platform"

# List all assignments on a scope
az policy assignment list \
  --scope "/subscriptions/<subscription-id>" \
  --output table

# Show a specific assignment
az policy assignment show \
  --name "deny-public-ip" \
  --scope "/subscriptions/<subscription-id>"

# Delete an assignment
az policy assignment delete \
  --name "deny-public-ip" \
  --scope "/subscriptions/<subscription-id>"
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/policyAssignments/deny-public-ip",
  "name": "deny-public-ip",
  "type": "Microsoft.Authorization/policyAssignments",
  "displayName": "Deny Public IP Addresses",
  "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/9daedab3-fb2d-461e-b861-71790eead4f6",
  "scope": "/subscriptions/12345678-1234-1234-1234-123456789012",
  "notScopes": null,
  "parameters": null,
  "description": "Deny creation of public IP addresses",
  "metadata": {
    "createdBy": "user@contoso.com",
    "createdOn": "2024-01-15T10:32:45.123456Z",
    "updatedBy": "user@contoso.com",
    "updatedOn": "2024-01-15T10:32:45.123456Z"
  },
  "enforcementMode": "Default"
}
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-production/providers/Microsoft.Authorization/policyAssignments/require-tags-rg",
  "name": "require-tags-rg",
  "scope": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-production"
}
{
  "id": "/providers/Microsoft.Management/managementGroups/mg-platform/providers/Microsoft.Authorization/policyAssignments/audit-storage-https",
  "name": "audit-storage-https",
  "scope": "/providers/Microsoft.Management/managementGroups/mg-platform"
}
Name                  Scope                                                                      EnforcementMode
--------------------  -------------------------------------------------------------------------  ---------------
deny-public-ip        /subscriptions/12345678-1234-1234-1234-123456789012                       Default
require-tags-rg       /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-production  Default
audit-storage-https   /providers/Microsoft.Management/managementGroups/mg-platform               Default
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/policyAssignments/deny-public-ip",
  "name": "deny-public-ip",
  "displayName": "Deny Public IP Addresses",
  "description": "Deny creation of public IP addresses",
  "enforcementMode": "Default"
}
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Invalid scope: The provided scope '/subscriptions/<subscription-id>' is invalid.` | Replace `<subscription-id>` and `<sub-id>` placeholders with your actual Azure subscription ID. |
    **`Policy definition not found: '9daedab3-fb2d-461e-b861-71790eead4f6'.`**
## Assignment Scope

The scope of an assignment determines which resources are evaluated.

| Scope Level | Example | Typical Use |
|---|---|---|
| Management Group | `/providers/Microsoft.Management/managementGroups/<mg>` | Organisation-wide baseline |
| Subscription | `/subscriptions/<sub-id>` | Environment-level controls |
| Resource Group | `/subscriptions/<sub-id>/resourceGroups/<rg>` | Team or workload-specific |
| Resource | Full resource ARM ID | Edge-case single-resource control |

Assignments inherit downward — a policy assigned at MG scope applies to all subscriptions and resource groups within that MG.

## Parameters

Policy parameters allow a single policy definition to be reused across assignments with different configuration values.

```bash
# Assign policy with multiple parameters
az policy assignment create \
  --name "allowed-locations" \
  --policy "e56962a6-4747-49cd-b67b-bf8b01975c4f" \
  --scope "/subscriptions/<subscription-id>" \
  --params '{
    "listOfAllowedLocations": {
      "value": ["uksouth", "ukwest", "northeurope"]
    }
  }'

# View the parameters of an existing assignment
az policy assignment show \
  --name "allowed-locations" \
  --scope "/subscriptions/<subscription-id>" \
  --query "parameters"
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/policyAssignments/allowed-locations",
  "type": "Microsoft.Authorization/policyAssignments",
  "name": "allowed-locations",
  "displayName": "allowed-locations",
  "policyDefinitionId": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/policyDefinitions/e56962a6-4747-49cd-b67b-bf8b01975c4f",
  "scope": "/subscriptions/12345678-1234-1234-1234-123456789012",
  "notScopes": [],
  "parameters": {
    "listOfAllowedLocations": {
      "value": [
        "uksouth",
        "ukwest",
        "northeurope"
      ]
    }
  },
  "description": null,
  "displayName": null,
  "enforcementMode": "Default"
}
{
  "listOfAllowedLocations": {
    "value": [
      "uksouth",
      "ukwest",
      "northeurope"
    ]
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The policy definition with ID 'e56962a6-4747-49cd-b67b-bf8b01975c4f' cannot be found.` | Verify the policy definition ID exists in your subscription or use `az policy definition list` to find the correct ID. |
    | `Invalid scope provided. Scope must be a valid subscription, resource group, or management group path.` | Replace `<subscription-id>` with your actual subscription ID from `az account show --query id`. |
    | `The parameter 'listOfAllowedLocations' is not defined in the policy definition.` | Check the policy definition's parameter names using `az policy definition show --name <policy-name> --query parameters` and adjust the JSON accordingly. |
## Exemptions

Specific resources or resource groups can be excluded from an assignment using exclusions (set at assignment time) or exemptions (created post-assignment).

```bash
# Add an exclusion scope at assignment creation time
az policy assignment create \
  --name "deny-public-ip" \
  --policy "9daedab3-fb2d-461e-b861-71790eead4f6" \
  --scope "/subscriptions/<subscription-id>" \
  --not-scopes "/subscriptions/<sub-id>/resourceGroups/rg-legacy"

# Create an exemption for a specific resource after assignment
az policy exemption create \
  --name "legacy-vm-exemption" \
  --policy-assignment "/subscriptions/<sub-id>/providers/Microsoft.Authorization/policyAssignments/deny-public-ip" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01" \
  --exemption-category Waiver \
  --expires-on 2026-12-31T00:00:00Z
```


```text title="Expected output"
{
  "description": null,
  "displayName": "deny-public-ip",
  "enforcementMode": "Default",
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/deny-public-ip",
  "identity": null,
  "location": null,
  "metadata": {
    "createdBy": "user@contoso.com",
    "createdOn": "2024-01-15T10:32:45.123456Z",
    "updatedBy": "user@contoso.com",
    "updatedOn": "2024-01-15T10:32:45.123456Z"
  },
  "name": "deny-public-ip",
  "notScopes": [
    "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-legacy"
  ],
  "policyDefinitionId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyDefinitions/9daedab3-fb2d-461e-b861-71790eead4f6",
  "scope": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "type": "Microsoft.Authorization/policyAssignments"
}
{
  "displayName": "legacy-vm-exemption",
  "exemptionCategory": "Waiver",
  "expiresOn": "2026-12-31T00:00:00Z",
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01/providers/Microsoft.Authorization/policyExemptions/legacy-vm-exemption",
  "name": "legacy-vm-exemption",
  "policyAssignmentId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/deny-public-ip",
  "scope": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-legacy/providers/Microsoft.Compute/virtualMachines/vm-legacy-01",
  "type": "Microsoft.Authorization/policyExemptions"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Policy definition not found with id '9daedab3-fb2d-461e-b861-71790eead4f6'.` | Verify the policy definition ID exists in your subscription using `az policy |
## Assignment Managed Identity

Policies with the `deployIfNotExists` or `modify` effect require a managed identity to perform remediation actions.

```bash
# Assign policy with system-assigned managed identity for remediation
az policy assignment create \
  --name "deploy-diag-settings" \
  --policy "<policy-definition-id>" \
  --scope "/subscriptions/<subscription-id>" \
  --mi-system-assigned \
  --location uksouth

# List assignments that have a managed identity
az policy assignment list \
  --scope "/subscriptions/<subscription-id>" \
  --query "[?identity != null].{Name:name, IdentityType:identity.type}" \
  --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/providers/Microsoft.Authorization/policyAssignments/deploy-diag-settings",
  "name": "deploy-diag-settings",
  "type": "Microsoft.Authorization/policyAssignments",
  "identity": {
    "type": "SystemAssigned",
    "principalId": "f7e6d5c4-b3a2-1098-7654-3210fedcba98"
  },
  "scope": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p",
  "location": "uksouth"
}
Name                   IdentityType
---------------------  ----------------
deploy-diag-settings   SystemAssigned
enforce-storage-https  SystemAssigned
audit-vm-encryption    UserAssigned
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Policy definition not found with id '<policy-definition-id>'.` | Replace `<policy-definition-id>` with a valid policy definition ID from `az policy definition list`. |
    | `The scope '/subscriptions/<subscription-id>' is invalid.` | Verify the subscription ID exists and you have access by running `az account show --query id`. |
    | `The operation failed because the managed identity does not have the required permissions.` | Assign the Contributor or Policy Insights Data Writer role to the system-assigned identity using `az role assignment create`. |
## Common Assignment Patterns

| Pattern | Description |
|---|---|
| Baseline at MG scope | Apply audit policies to all subscriptions via management group |
| Deny at subscription scope | Block dangerous operations per environment |
| Modify at RG scope | Auto-tag resources on creation within a team's RG |
| Exemption with expiry | Time-bound exception for legacy resources or migration windows |
