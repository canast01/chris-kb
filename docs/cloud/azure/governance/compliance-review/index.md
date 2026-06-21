---
tags:
  - azure
---
# Compliance Review


<div class="kb-summary">
Azure Policy compliance reviews evaluate the current state of resources against assigned policies and surface non-compliant resources. Regular compliance reviews are essential for maintaining governance standards and preparing for audits.

*Applies to: Azure*
</div>
![Compliance Review](../../../../assets/cloud-azure-governance-compliance-review-index.svg)




## Compliance Review Cycle

```mermaid
flowchart LR
    trigger["Compliance Scan\nscheduled daily or on-demand"]
    evaluate["Policy Evaluation\nall resources vs all assignments"]
    dashboard["Compliance Dashboard\n% compliant per assignment"]
    nonCompliant{"Non-compliant\nresources found?"}
    remediate["Create Remediation Task\nor manual fix"]
    exempt["Create Exemption\nif justified"]
    report["Compliance Report\nexport for audit"]

    trigger --> evaluate --> dashboard --> nonCompliant
    nonCompliant -- Yes --> remediate & exempt
    nonCompliant -- No --> report
    remediate --> trigger
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
