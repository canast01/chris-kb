# Cost Allocation Tags

Tags are the primary mechanism for attributing Azure costs to teams, projects, environments, and cost centres. Effective tag strategy combined with policy enforcement ensures cost data is always actionable.

## Tag Strategy

Define a small, mandatory set of tags applied to every resource and resource group. Avoid tag sprawl — more than 10–12 required tags rarely adds value and increases compliance burden.

### Recommended Core Tag Set

| Tag Key | Example Values | Purpose |
|---|---|---|
| `environment` | prod, staging, dev, sandbox | Cost split by lifecycle stage |
| `team` | platform, data, frontend, security | Chargeback / showback by team |
| `project` | project-alpha, migration-2026 | Per-project cost tracking |
| `cost-centre` | CC-1001, CC-2030 | Finance system integration |
| `owner` | chris.a@example.com | Escalation contact |
| `managed-by` | terraform, bicep, manual | Provenance tracking |

## Applying Tags via CLI

```bash
# Tag a resource group
az group update \
  --name rg-team-alpha \
  --tags environment=prod team=platform cost-centre=CC-1001

# Tag an individual resource
az resource tag \
  --ids /subscriptions/<sub-id>/resourceGroups/rg-team-alpha/providers/Microsoft.Compute/virtualMachines/vm-web-01 \
  --tags project=project-alpha owner=chris.a@example.com

# List all tags on a resource group
az tag list \
  --resource-id /subscriptions/<sub-id>/resourceGroups/rg-team-alpha

# Find resources missing the 'cost-centre' tag
az resource list \
  --query "[?tags.\"cost-centre\" == null].{Name:name, Type:type, RG:resourceGroup}" \
  --output table
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
