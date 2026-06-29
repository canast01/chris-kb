---
tags:
  - azure
---
# Cost Allocation Tags

<div class="kb-summary">
Tags are the primary mechanism for attributing Azure costs to teams, projects, environments, and cost centres.

*Applies to: Azure*
</div>

```d2
direction: down

enforcement_with_policy: "Enforcement with Policy" {shape: rectangle}
cost_allocation_rules: "Cost Allocation Rules" {shape: rectangle}
tag_inheritance: "Tag Inheritance" {shape: rectangle}
reporting_on_tag_coverage: "Reporting on Tag Coverage" {shape: rectangle}

enforcement_with_policy -> cost_allocation_rules: uses
cost_allocation_rules -> tag_inheritance: uses
tag_inheritance -> reporting_on_tag_coverage: uses
```

## Enforcement with Policy

Use Azure Policy to enforce tag presence and valid values. The built-in `Require a tag on resources` and `Require a tag and its value on resources` policies cover most cases.

```bash
# Assign built-in "Require a tag on resources" policy at subscription scope
az policy assignment create \
  --name "require-cost-centre-tag" \
  --policy "871b6d14-10aa-478d-b590-94f262ecfa99" \
  --scope "/subscriptions/<subscription-id>" \
  --params '{"tagName": {"value": "cost-centre"}}'

# List all policy assignments on a subscription
az policy assignment list \
  --scope "/subscriptions/<subscription-id>" \
  --output table

# Check compliance state for the assignment
az policy state list \
  --policy-assignment "require-cost-centre-tag" \
  --query "[?complianceState=='NonCompliant'].{Resource:resourceId}" \
  --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/policyAssignments/require-cost-centre-tag",
  "name": "require-cost-centre-tag",
  "type": "Microsoft.Authorization/policyAssignments",
  "displayName": "require-cost-centre-tag",
  "policyDefinitionId": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/policyDefinitions/871b6d14-10aa-478d-b590-94f262ecfa99",
  "scope": "/subscriptions/12345678-1234-1234-1234-123456789012",
  "notScopes": [],
  "parameters": {
    "tagName": {
      "value": "cost-centre"
    }
  },
  "description": null,
  "displayName": "require-cost-centre-tag",
  "enforcementMode": "Default"
}

Name                          Type                      Scope
------------------------------  -------------------------  -----------------------------------------------
require-cost-centre-tag        Microsoft.Authorization   /subscriptions/12345678-1234-1234-1234-123456789012
inherited-audit-storage        Microsoft.Authorization   /subscriptions/12345678-1234-1234-1234-123456789012
...

Resource
-------------------------------------------
/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01
/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/dev-rg/providers/Microsoft.Storage/storageAccounts/devstg9847
/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/test-rg/providers/Microsoft.Sql/servers/testdb-srv
```

!!! warning "Common errors"
    **`Policy definition not found`** — Verify the policy definition ID exists in your subscription or use `az policy definition list` to find the correct built-in policy ID.
    **`Invalid scope format`** — Ensure the subscription ID is valid and the scope follows the format `/subscriptions/<subscription-id>` without extra slashes or whitespace.
    **`Authorization failed`** — Confirm your Azure account has `Microsoft.Authorization/policyAssignments/write` permissions at the subscription scope.
### Policy Effect Options for Tag Enforcement

| Effect | Behaviour |
|---|---|
| `Audit` | Logs non-compliant resources; does not block creation |
| `Deny` | Blocks resource creation/update if tag is missing |
| `Modify` | Automatically adds or updates the tag at creation time |

Start with `Audit` to baseline compliance, then switch to `Deny` or `Modify` after a remediation sprint.

## Cost Allocation Rules

In Microsoft Cost Management, cost allocation rules let you redistribute shared costs (e.g., a shared networking subscription) to other subscriptions or resource groups based on tag-defined proportions.

```bash
# Cost allocation rules are managed via the Cost Management REST API or portal.
# Use the CLI to verify tag coverage before configuring allocation:

# Count resources per team tag value
az resource list \
  --query "sort_by([].{Team:tags.team, Name:name}, &Team)" \
  --output table
```


```text title="Expected output"
Team    Name
------  -----------------------------------------------
devops  app-gateway-prod-01
devops  storage-account-logs-eastus
devops  vm-jumphost-02
eng     api-server-primary
eng     database-postgres-main
eng     kubernetes-cluster-aks-prod
infra   load-balancer-internal
infra   network-security-group-default
infra   virtual-network-hub-eastus2
(no team tag)  legacy-app-server-01
(no team tag)  old-storage-blob-archive
```

!!! warning "Common errors"
    **`The subscription of type '<SubscriptionType>' is not supported.`** — Ensure your Azure account has an active subscription by running `az account set --subscription <subscription-id>`.
    **`No registered resource providers found for location 'eastus' in subscription.`** — Register required resource providers with `az provider register --namespace Microsoft.Compute` (or the relevant namespace).
## Tag Inheritance

Tags do not automatically inherit from resource group to child resources. Use the `Inherit a tag from the resource group` built-in policy to propagate resource group tags.

```bash
# Assign tag inheritance policy for 'environment' tag
az policy assignment create \
  --name "inherit-environment-tag" \
  --policy "96670d01-0a4d-4649-9c89-2d3abc0a5025" \
  --scope "/subscriptions/<subscription-id>" \
  --params '{"tagName": {"value": "environment"}}'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/providers/Microsoft.Authorization/policyAssignments/inherit-environment-tag",
  "identity": {
    "principalId": "f1e2d3c4-b5a6-7890-1234-567890abcdef",
    "tenantId": "12345678-1234-1234-1234-123456789012",
    "type": "SystemAssigned"
  },
  "location": "eastus",
  "name": "inherit-environment-tag",
  "policyDefinitionId": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/providers/Microsoft.Authorization/policyDefinitions/96670d01-0a4d-4649-9c89-2d3abc0a5025",
  "scope": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "type": "Microsoft.Authorization/policyAssignments"
}
```

!!! warning "Common errors"
    **`The policy definition '96670d01-0a4d-4649-9c89-2d3abc0a5025' could not be found.`** — Verify the policy definition ID exists in your subscription or use `az policy definition list` to find the correct ID.
    **`Invalid scope: /subscriptions/<subscription-id>. Scope must be a valid Azure resource ID.`** — Replace `<subscription-id>` with your actual subscription ID from `az account show --query id`.
    **`The policy assignment 'inherit-environment-tag' already exists at scope '/subscriptions/...'.`** — Use `--force` flag to overwrite the existing assignment or choose a different assignment name.
## Reporting on Tag Coverage

```bash
# Export all resources with their tags to JSON for audit
az resource list \
  --query "[].{Name:name, RG:resourceGroup, Tags:tags}" \
  --output json > resource-tags-$(date +%Y%m%d).json

# Resources with no tags at all
az resource list \
  --query "[?tags == null || tags == {}].{Name:name, RG:resourceGroup, Type:type}" \
  --output table
```


```text title="Expected output"
{
  "Name": "prod-web-vm-01",
  "RG": "prod-web-rg",
  "Tags": {
    "Environment": "Production",
    "CostCenter": "CC-4521",
    "Owner": "platform-team"
  }
},
{
  "Name": "dev-storage-acct",
  "RG": "dev-resources",
  "Tags": null
},
{
  "Name": "staging-sql-db",
  "RG": "staging-rg",
  "Tags": {
    "Environment": "Staging",
    "CostCenter": "CC-4521"
  }
}

Name                    RG                  Type
----------------------  ------------------  --------------------------------
legacy-app-vm           legacy-rg           Microsoft.Compute/virtualMachines
backup-storage-001      backup-rg           Microsoft.Storage/storageAccounts
test-keyvault           test-rg             Microsoft.KeyVault/vaults
orphaned-nic-eth0       orphaned-rg         Microsoft.Network/networkInterfaces
```

!!! warning "Common errors"
    **`ERROR: The following arguments are required: --subscription`** — Add `--subscription <subscription-id>` or set the default subscription with `az account set --subscription <id>`.
    **`ERROR: No registered resource provider found for location 'null'`** — Ensure you are authenticated with `az login` and have permissions to list resources in the target subscription.