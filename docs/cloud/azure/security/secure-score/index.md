---
tags:
  - azure
  - security
description: "Microsoft Defender for Cloud Secure Score is a quantified measure of an Azure environment's security posture. It aggregates security recommendations..."
---
# Azure — Secure Score

<div class="kb-summary">
Microsoft Defender for Cloud Secure Score is a quantified measure of an Azure environment's security posture. It aggregates security recommendations across subscriptions into a single percentage that rises as recommendations are remediated.

*Applies to: Azure*
</div>

```d2
direction: down

score_calculation: "Score Calculation" {shape: rectangle}
viewing_secure_score: "Viewing Secure Score" {shape: rectangle}
recommendations: "Recommendations" {shape: rectangle}
common_highimpact_recommendations: "Common High-Impact Recommendations" {shape: rectangle}
remediating_via_cli: "Remediating via CLI" {shape: rectangle}
exemptions: "Exemptions" {shape: rectangle}

score_calculation -> viewing_secure_score: uses
viewing_secure_score -> recommendations: uses
recommendations -> common_highimpact_recommendations: uses
common_highimpact_recommendations -> remediating_via_cli: uses
remediating_via_cli -> exemptions: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Score Calculation

```text
Secure Score = (Sum of points earned) / (Sum of max points) × 100%

Points earned per control = max points × (healthy resources / total resources)
```

Security recommendations are grouped into **security controls** (e.g., "Enable MFA", "Protect applications with WAF"). Each control has a maximum point value. Partial completion of a control earns partial points.

## Viewing Secure Score

```text
Microsoft Defender for Cloud → Secure posture → Secure score
```

Shows:
- Overall score across all subscriptions
- Score per subscription
- Score trend over time
- Top recommendations by potential score increase

## Recommendations

Each recommendation shows:

| Field | Meaning |
|---|---|
| **Severity** | High / Medium / Low |
| **Score impact** | Points gained by remediating this recommendation |
| **Unhealthy resources** | Resources not complying with the recommendation |
| **Quick fix** | One-click automated remediation (where available) |
| **Exemption** | Mark a resource as exempt if recommendation doesn't apply |

## Common High-Impact Recommendations

| Recommendation | Control | Score impact |
|---|---|---|
| Enable MFA for accounts with owner permissions | Enable MFA | High |
| Enable MFA for accounts with write permissions | Enable MFA | High |
| Subscriptions should have a contact email address | Enable security contact | Medium |
| System updates should be installed on machines | Apply system updates | High |
| Vulnerabilities in security configuration should be remediated | Remediate security configurations | High |
| Management ports should be closed on VMs | Restrict unauthorized network access | High |
| Endpoint protection should be enabled on VMs | Enable endpoint protection | Medium |
| Storage accounts should restrict network access | Restrict unauthorized network access | Medium |
| Key vaults should have soft delete enabled | Enable encryption at rest | Medium |

## Remediating via CLI

```bash
# View all recommendations for a subscription
az security assessment list --output table

# View details of a specific recommendation
az security assessment show \
  --name <assessment-name> \
  --resource-id /subscriptions/<sub-id>

# Example: Enable just-in-time VM access (Quick fix)
az security jit-policy create \
  --resource-group <rg> \
  --vm-name <vm-name> \
  --location <region> \
  --kind "Basic" \
  --virtual-machines '[{
    "id": "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm-name>",
    "ports": [
      {"number": 22, "protocol": "TCP", "allowedSourceAddressPrefix": "*", "maxRequestAccessDuration": "PT3H"},
      {"number": 3389, "protocol": "TCP", "allowedSourceAddressPrefix": "*", "maxRequestAccessDuration": "PT3H"}
    ]
  }]'
```


```text title="Expected output"
Name                                          ResourceId                                                                                                                    DisplayName                                    State
----------------------------------------------  ----------------------------------------------------------------------------------------------------------------------------------  ------------------------------------------  ---------
4fb6c0a0-1fb0-45fd-b4af-38e8b9e1b88a          /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01  Enable just-in-time VM access                 Healthy
550e8400-e29b-41d4-a716-446655440000          /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Sql/servers/db-server-prod      Enable Transparent Data Encryption on SQL DB  Unhealthy
6ba7b810-9dad-11d1-80b4-00c04fd430c8          /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/logs2024  Require secure transfer for storage account    Unhealthy
...

Assessment Name: 4fb6c0a0-1fb0-45fd-b4af-38e8b9e1b88a
Display Name: Enable just-in-time VM access
Resource Id: /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01
Status: Healthy
Description: Just-in-time VM access reduces exposure to attacks by limiting access to VMs

{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Security/jitNetworkAccessPolicies/default",
  "name": "default",
  "type": "Microsoft.Security/jitNetworkAccessPolicies",
  "location": "eastus",
  "kind": "Basic",
  "virtualMachines": [
    {
      "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
      "ports": [
        {
          "number": 22,
          "protocol": "TCP",
          "allowedSourceAddressPrefix": "*",
          "maxRequestAccessDuration": "PT3H"
        },
        {
          "number": 3389,
          "protocol": "TCP",
          "allowedSourceAddressPrefix": "*",
          "maxRequestAccessDuration": "PT3H"
        }
      ]
    }
  ]
}
```

!!! warning "Common errors"
    **`ResourceNotFound : The resource '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm-name>' could not be found.`** — Verify the subscription ID, resource group name, and VM name are correct and exist in your current Azure context.
    **`InvalidParameter : The value of parameter 'virtual-machines' is invalid.`** — Ensure the
## Exemptions

Mark a resource as exempt when a recommendation doesn't apply (e.g., a VM has a third-party endpoint agent that satisfies the requirement).

```bash
az security assessment create \
  --name <assessment-name> \
  --resource-id /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm-name> \
  --status-code "NotApplicable" \
  --status-cause "Exempt" \
  --status-description "Third-party EDR solution in use"
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/resourceGroups/prod-rg/providers/Microsoft.Security/assessments/assessment-edr-001",
  "name": "assessment-edr-001",
  "properties": {
    "displayName": "assessment-edr-001",
    "resourceDetails": {
      "id": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01"
    },
    "statusCode": "NotApplicable",
    "statusCause": "Exempt",
    "statusDescription": "Third-party EDR solution in use",
    "timeGenerated": "2024-01-15T14:32:18.5432109Z"
  },
  "type": "Microsoft.Security/assessments"
}
```

!!! warning "Common errors"
    **`The provided resource ID is invalid or the resource does not exist.`** — Verify the subscription ID, resource group name, and VM name are correct and the VM exists in that resource group.
    **`The user does not have permission to perform action 'Microsoft.Security/assessments/write' on resource.`** — Ensure your Azure account has the Security Admin or Contributor role assigned at the subscription or resource group scope.
    **`Invalid value 'NotApplicable' for status-code. Allowed values are: Healthy, Unhealthy, NotApplicable.`** — Use one of the three valid status codes: Healthy, Unhealthy, or NotApplicable (check exact casing).
## Regulatory Compliance

Defender for Cloud maps recommendations to compliance standards (CIS, NIST SP 800-53, ISO 27001, PCI DSS).

```text
Defender for Cloud → Regulatory compliance → select standard → view controls and evidence
```

Custom compliance standards can be assigned via Azure Policy initiatives.

## Score Targets

| Score | Posture assessment |
|---|---|
| < 50% | High risk — critical gaps in security controls |
| 50–70% | Moderate — basic controls in place, significant gaps remain |
| 70–90% | Good — most controls implemented, fine-tuning required |
| > 90% | Strong — near-complete control implementation |

A score above 75% is a reasonable operational target for most production environments. Scores near 100% are typically only achievable by exempting recommendations that don't apply to the workload.

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| Score dropped overnight | New resources created without controls; new recommendations added by MSFT | Review new unhealthy resources; enable Defender for new resource types |
| Recommendation shows "Not applicable" but still counts against score | Exemption not applied | Create an exemption with a justification |
| Score different per subscription | Each subscription is scored independently | Review per-subscription recommendations in Defender for Cloud |
| Quick fix greyed out | Resource is in a locked or policy-restricted state | Check resource locks and Azure Policy deny effects |
| Recommendation persists after remediation | Scan frequency — Defender re-evaluates on its own schedule (up to 12 hours) | Wait for next scan cycle; force re-evaluate via Portal |
