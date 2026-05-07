# Azure Policy

Azure Policy — governance guardrails that audit and enforce configuration standards across Azure resources.
## Key Concepts

| Concept | Description |
|---|---|
| Policy definition | Rule that evaluates resources against conditions |
| Initiative (policy set) | Group of policy definitions applied together |
| Assignment | Applies a policy or initiative to a scope (subscription, RG, management group) |
| Effect | What the policy does: `Audit`, `Deny`, `Modify`, `DeployIfNotExists`, `AuditIfNotExists` |
| Compliance | Dashboard showing compliant vs non-compliant resources |
| Remediation task | Runs a `DeployIfNotExists` or `Modify` policy on existing non-compliant resources |

## Common Azure CLI Commands

```bash
# List policy definitions (built-in only)
az policy definition list --query '[?policyType==`BuiltIn`].{Name:displayName,ID:name}' -o table | head -20

# List policy assignments at subscription scope
az policy assignment list \
  --query '[*].{Name:displayName,Policy:policyDefinitionId,Scope:scope}' -o table

# Create a policy assignment (built-in: require tags on resources)
az policy assignment create \
  --name "require-env-tag" \
  --display-name "Require environment tag" \
  --policy "/providers/Microsoft.Authorization/policyDefinitions/<built-in-policy-id>" \
  --scope /subscriptions/<sub-id> \
  --params '{"tagName":{"value":"Environment"}}'

# Get compliance state for an assignment
az policy state summarize \
  --policy-assignment <assignment-id> \
  --query 'results.policyDetails[*].{Policy:policyDefinitionId,NonCompliant:nonCompliantResources}'

# List non-compliant resources
az policy state list \
  --filter "complianceState eq 'NonCompliant'" \
  --query '[*].{Resource:resourceId,Policy:policyDefinitionName,Time:timestamp}' -o table

# Create a remediation task (for DeployIfNotExists policies)
az policy remediation create \
  --name <remediation-name> \
  --policy-assignment <assignment-id> \
  -g <rg>
```

## Common Built-In Policies

| Policy | Effect | Use Case |
|---|---|---|
| Allowed locations | Deny | Restrict resources to approved regions |
| Require a tag and its value | Deny | Enforce resource tagging |
| Audit VMs that do not use managed disks | Audit | Surface unmanaged disks |
| Deploy Log Analytics agent for VMs | DeployIfNotExists | Auto-install monitoring agent |
| Require encryption on storage accounts | Deny | Enforce storage encryption |
| Not allowed resource types | Deny | Block specific resource types |

## Custom Policy Definition

```json
{
  "mode": "All",
  "displayName": "Deny public IP on VMs",
  "policyRule": {
    "if": {
      "allOf": [
        {
          "field": "type",
          "equals": "Microsoft.Network/publicIPAddresses"
        },
        {
          "field": "Microsoft.Network/publicIPAddresses/sku.name",
          "notEquals": "Basic"
        }
      ]
    },
    "then": {
      "effect": "Deny"
    }
  }
}
```

```bash
# Create custom policy
az policy definition create \
  --name "deny-public-ip-vm" \
  --display-name "Deny public IPs on VMs" \
  --rules policy-rule.json \
  --mode All
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Resource creation denied unexpectedly | Active policy assignments | Check `az policy assignment list` for Deny effects at the scope |
| Compliance showing stale data | Evaluation trigger | Trigger re-evaluation: `az policy state trigger-scan` |
| Remediation task failing | Managed identity permissions | Assign remediation identity the required RBAC role on scope |
| Policy not applying to existing resources | Effect type | Only `Audit`/`Deny` apply to new resources; use remediation for existing |
