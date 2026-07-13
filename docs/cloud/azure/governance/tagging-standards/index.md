---
tags:
  - azure
description: "Azure resource tags are key-value pairs applied to resources and resource groups for organisation, cost attribution, automation, and governance. A..."
---
# Tagging Standards

<div class="kb-summary">
Azure resource tags are key-value pairs applied to resources and resource groups for organisation, cost attribution, automation, and governance. A consistent tagging standard is the foundation of effective cloud management.

*Applies to: Azure*
</div>

## Tag Governance Flow

```d2
direction: right

deploy: "Resource Deployment\nPortal / IaC / CLI" {shape: rectangle}
policyCheck: "Azure Policy\nrequire-tag deny effect" {shape: rectangle}
tagPresent: "tagPresent" {shape: rectangle}
taggedResource: "Tagged Resource\ncompliant" {shape: rectangle}
costMgmt: "Cost Management\nfilter by tag" {shape: rectangle}
automation: "Automation\ntag-based operations" {shape: rectangle}
blocked: "Deployment BLOCKED\n400 error — policy deny" {shape: rectangle}

deploy -> policyCheck
policyCheck -> tagPresent
taggedResource -> costMgmt
costMgmt -> automation
```

## Required Tags

Define a small, stable set of mandatory tags. Every resource and resource group must carry all required tags.

| Tag Key | Description | Example Values | Owner |
|---|---|---|---|
| `environment` | Lifecycle stage | prod, staging, dev, sandbox | Platform team |
| `team` | Owning team | platform, data, frontend, security | All teams |
| `project` | Associated project or workload | project-alpha, shared-infra | All teams |
| `cost-centre` | Finance cost centre code | CC-1001, CC-2030 | Finance |
| `owner` | Primary contact email | chris.a@example.com | All teams |
| `managed-by` | Provisioning method | terraform, bicep, manual | All teams |

## Applying Tags via CLI

```bash
# Apply required tags to a resource group
az group update \
  --name rg-project-alpha-prod \
  --tags environment=prod team=platform project=project-alpha cost-centre=CC-1001 owner=chris.a@example.com managed-by=terraform

# Apply tags to an individual resource
az resource tag \
  --ids /subscriptions/<sub-id>/resourceGroups/rg-project-alpha-prod/providers/Microsoft.Compute/virtualMachines/vm-app-01 \
  --tags environment=prod team=platform project=project-alpha

# Update a single tag on a resource (merge, not replace)
az resource tag \
  --ids <resource-id> \
  --tags owner=new.owner@example.com

# Remove all tags from a resource
az tag delete \
  --resource-id <resource-id>
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-project-alpha-prod",
  "location": "eastus",
  "managedBy": null,
  "name": "rg-project-alpha-prod",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": {
    "cost-centre": "CC-1001",
    "environment": "prod",
    "managed-by": "terraform",
    "owner": "chris.a@example.com",
    "project": "project-alpha",
    "team": "platform"
  },
  "type": "Microsoft.Resources/resourceGroups"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-project-alpha-prod/providers/Microsoft.Compute/virtualMachines/vm-app-01",
  "tags": {
    "environment": "prod",
    "project": "project-alpha",
    "team": "platform"
  }
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-project-alpha-prod/providers/Microsoft.Compute/virtualMachines/vm-app-01",
  "tags": {
    "environment": "prod",
    "owner": "new.owner@example.com",
    "project": "project-alpha",
    "team": "platform"
  }
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`The resource with id <resource-id> does not exist.`** — Verify the subscription ID and resource path are correct by running `az resource list --query "[].id"` to find the exact resource ID.
    **`The provided resource id '<resource-id>' is invalid.`** — Ensure the resource ID follows the format `/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/<provider>/<resource-type>/<resource-name>` with no extra slashes or typos.
    **`AuthorizationFailed: The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Resources/tags/write' on resource '<resource-id>'.`** — Assign the "Tag Contributor" or "Owner" role to your user account on the target resource or subscription using `az role assignment create`.
## Tag Enforcement with Policy

Use Azure Policy to enforce tag presence and prevent resource creation without required tags.

```bash
# Assign "Require a tag on resources" policy for each required tag
for TAG in environment team project cost-centre owner managed-by; do
  az policy assignment create \
    --name "require-tag-${TAG}" \
    --policy "96670d01-0a4d-4649-9c89-2d3abc0a5025" \
    --scope "/subscriptions/<subscription-id>" \
    --params "{\"tagName\": {\"value\": \"${TAG}\"}}"
done

# Assign "Allowed tag values" policy for environment tag
az policy assignment create \
  --name "allowed-environment-values" \
  --policy "d1cf8b34-ac74-4cdf-9ef7-13f9de23ea3c" \
  --scope "/subscriptions/<subscription-id>" \
  --params '{
    "tagName": {"value": "environment"},
    "tagValue": {"value": ["prod", "staging", "dev", "sandbox"]}
  }'

# Check compliance for tag policies
az policy state list \
  --filter "policyAssignmentName eq 'require-tag-environment' and complianceState eq 'NonCompliant'" \
  --query "[].{Resource:resourceId, RG:resourceGroup}" \
  --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/providers/Microsoft.Authorization/policyAssignments/require-tag-environment",
  "name": "require-tag-environment",
  "type": "Microsoft.Authorization/policyAssignments",
  "properties": {
    "displayName": "require-tag-environment",
    "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/96670d01-0a4d-4649-9c89-2d3abc0a5025",
    "scope": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789",
    "notScopes": []
  }
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/providers/Microsoft.Authorization/policyAssignments/require-tag-team",
  "name": "require-tag-team",
  ...
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/providers/Microsoft.Authorization/policyAssignments/allowed-environment-values",
  "name": "allowed-environment-values",
  "type": "Microsoft.Authorization/policyAssignments",
  "properties": {
    "displayName": "allowed-environment-values",
    "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/d1cf8b34-ac74-4cdf-9ef7-13f9de23ea3c",
    "scope": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789"
  }
}

Resource                                                                                    RG
----------------------------------------------------------------------------------------------
/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01  prod-rg
/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/legacy-rg/providers/Microsoft.Storage/storageAccounts/legacydata2024  legacy-rg
```

!!! warning "Common errors"
    **`InvalidResourceId : The resource id '<subscription-id>' is invalid.`** — Replace `<subscription-id>` with your actual subscription ID (e.g., `a1b2c3d4-e5f6-4789-0abc-def123456789`).
    **`PolicyDefinitionNotFound : Policy definition '96670d01-0a4d-4649-9c89-2d3abc0a5025' not found.`** — Verify the policy definition ID exists in your tenant; use `az policy definition list --query "[].id"` to confirm.
    **`AuthorizationFailed : The client 'user@example.com' with object id 'xyz' does not have authorization to perform action 'Microsoft.Authorization/policyAssignments/write' over scope '/subscriptions/...'.`** — Ensure your account has Owner or
## Tag Inheritance

Tags on resource groups are not automatically inherited by child resources. Use the `Inherit a tag from the resource group if missing` built-in policy to propagate tags.

```bash
# Assign tag inheritance policy for environment and team tags
az policy assignment create \
  --name "inherit-tag-environment" \
  --policy "96670d01-0a4d-4649-9c89-2d3abc0a5025" \
  --scope "/subscriptions/<subscription-id>"

# Use Modify effect policy for automatic tag inheritance
az policy assignment create \
  --name "inherit-environment-from-rg" \
  --policy "9be884c0-2312-4049-b562-7e7cd8cc6bb2" \
  --scope "/subscriptions/<subscription-id>" \
  --params '{"tagName": {"value": "environment"}}' \
  --mi-system-assigned \
  --location uksouth
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/providers/Microsoft.Authorization/policyAssignments/inherit-tag-environment",
  "name": "inherit-tag-environment",
  "type": "Microsoft.Authorization/policyAssignments",
  "identity": {
    "type": "None"
  },
  "displayName": null,
  "policyDefinitionId": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/providers/Microsoft.Authorization/policyDefinitions/96670d01-0a4d-4649-9c89-2d3abc0a5025",
  "scope": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "notScopes": null,
  "parameters": null,
  "metadata": {
    "createdBy": "user@contoso.com",
    "createdOn": "2024-01-15T10:32:45.123456Z",
    "updatedBy": "user@contoso.com",
    "updatedOn": "2024-01-15T10:32:45.123456Z"
  },
  "enforcementMode": "Default"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/providers/Microsoft.Authorization/policyAssignments/inherit-environment-from-rg",
  "name": "inherit-environment-from-rg",
  "type": "Microsoft.Authorization/policyAssignments",
  "identity": {
    "type": "SystemAssigned",
    "principalId": "f7e8d9c0-b1a2-3456-7890-abcdef123456"
  },
  "displayName": null,
  "policyDefinitionId": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/providers/Microsoft.Authorization/policyDefinitions/9be884c0-2312-4049-b562-7e7cd8cc6bb2",
  "scope": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "parameters": {
    "tagName": {
      "value": "environment"
    }
  },
  "metadata": {
    "createdBy": "user@contoso.com",
    "createdOn": "2024-01-15T10:32:47.654321Z",
    "updatedBy": "user@contoso.com",
    "updatedOn": "2024-01-15T10:32:47.654321Z"
  },
  "enforcementMode": "Default"
}
```

!!! warning "Common errors"
    **`Policy definition 96670d01-0a4d-4649-9c89-2d3abc0a5025 not found.`** — Verify the policy definition ID exists in your subscription or use `az policy definition list` to find the correct built-in policy ID.
## Reporting on Tag Coverage

```bash
# Find resources missing the cost-centre tag
az resource list \
  --query "[?tags.\"cost-centre\" == null].{Name:name, RG:resourceGroup, Type:type}" \
  --output table

# Find resources with no tags at all
az resource list \
  --query "[?tags == null || tags == {}].{Name:name, RG:resourceGroup}" \
  --output table

# Export all resource tags to JSON for audit
az resource list \
  --query "[].{Name:name, RG:resourceGroup, Type:type, Tags:tags}" \
  --output json > resource-tags-$(date +%Y%m%d).json

# Count resources per team value
az resource list \
  --query "sort_by([?tags.team != null].{Team:tags.team, Name:name}, &Team)" \
  --output table
```


```text title="Expected output"
Name                                    RG                Type
------------------------------------    ----------------  ----------------------------------------
prod-db-server-01                       prod-rg           Microsoft.DBforPostgreSQL/servers
storage-backup-vault                    backup-rg         Microsoft.Storage/storageAccounts
legacy-app-vm                           legacy-rg         Microsoft.Compute/virtualMachines
...

Name                                    RG
------------------------------------    ----------------
untagged-function-app                   dev-rg
orphaned-disk-001                       cleanup-rg
...

resource-tags-20240115.json created successfully.

Team              Name
----------------  ----------------------------------------
backend            api-service-prod
backend            cache-redis-01
frontend          web-app-portal
frontend          cdn-distribution
infra             monitoring-workspace
...
```

!!! warning "Common errors"
    **`ERROR: The subscription of the request is invalid.`** — Ensure you are logged in with `az login` and the correct subscription is set via `az account set --subscription <subscription-id>`.
    **`ERROR: The following arguments are required: --resource-group/-g`** — Remove the `--resource-group` filter if querying all subscriptions, or add `-g <resource-group-name>` to scope to a specific group.
    **`jq: parse error: Unexpected end of JSON input`** — If piping to `jq`, ensure the JSON file was written completely; re-run the export command or check disk space with `df -h`.
## Tag Naming Conventions

| Convention | Recommendation |
|---|---|
| Case | Lowercase with hyphens (`cost-centre`, not `CostCentre`) |
| Special characters | Avoid — can break automation and policy matching |
| Max tag keys | Azure supports 50 tags per resource; stay under 15 for manageability |
| Tag key consistency | Use the same key names across all resources (no aliases) |
| Automation tags | Prefix automation-specific tags (e.g., `auto-shutdown: 19:00`) |
