# Azure — Secure Score

Microsoft Defender for Cloud Secure Score is a quantified measure of an Azure environment's security posture. It aggregates security recommendations across subscriptions into a single percentage that rises as recommendations are remediated.

## Score Calculation

```
Secure Score = (Sum of points earned) / (Sum of max points) × 100%

Points earned per control = max points × (healthy resources / total resources)
```

Security recommendations are grouped into **security controls** (e.g., "Enable MFA", "Protect applications with WAF"). Each control has a maximum point value. Partial completion of a control earns partial points.

## Viewing Secure Score

```
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

## Regulatory Compliance

Defender for Cloud maps recommendations to compliance standards (CIS, NIST SP 800-53, ISO 27001, PCI DSS).

```
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
