---
tags:
  - servicenow
---
# Change Risk Assessment

<div class="kb-summary">
Change Risk Assessment reference covering Overview, Risk Assessment Matrix, Risk Identification Checklist, Risk Mitigation Examples, Residual Risk and Acceptance and 1 more sections.

*Applies to: ServiceNow*
</div>

## Overview

Risk assessment is a mandatory step for every change above the Standard tier. It ensures that implementation teams and approvers have a shared understanding of what could go wrong, how likely that is, and what controls are in place to reduce the probability or limit the impact. A well-completed risk assessment is a decision-support tool, not a compliance checkbox.

---

## Risk Assessment Matrix

Score impact and likelihood independently, then multiply for the overall risk score.

| Score | Impact                                         | Likelihood                         |
|-------|------------------------------------------------|------------------------------------|
| 1     | Negligible — no user-facing effect             | Very unlikely — routine, well-tested |
| 2     | Minor — limited to non-critical service/team   | Unlikely — similar to previous changes |
| 3     | Moderate — multiple teams or services affected | Possible — some unknowns remain    |
| 4     | Significant — critical service degraded        | Likely — new approach or technology |
| 5     | Severe — major outage or data loss potential   | Near certain — high complexity     |

**Risk Score = Impact × Likelihood**

| Risk Score | Level    | Approval Required              |
|------------|----------|--------------------------------|
| 1–4        | Low      | Standard or Normal approval    |
| 5–9        | Medium   | Normal — full CAB review       |
| 10–14      | High     | Major — CAB + senior sign-off  |
| 15–25      | Critical | Major — executive approval required |

---

## Risk Identification Checklist

Work through these categories when completing a risk assessment.

- [ ] **Service impact** — which services could be degraded or disrupted?
- [ ] **Data risk** — could data be lost, corrupted, or exposed?
- [ ] **Dependency risk** — are any upstream/downstream services at risk?
- [ ] **Time risk** — is the change window long enough? What if it overruns?
- [ ] **Rollback risk** — can the change be reversed? How long does rollback take?
- [ ] **Resource risk** — do all required people and tools have confirmed availability?
- [ ] **Testing coverage** — has the change been fully tested in a representative environment?
- [ ] **Third-party risk** — does the change involve vendor-managed components?

---

## Risk Mitigation Examples

| Risk                              | Mitigation                                        |
|-----------------------------------|---------------------------------------------------|
| Service unavailability            | Schedule during off-peak hours; notify users      |
| Config error causes outage        | Dry-run in staging; peer-review implementation steps |
| Rollback exceeds change window    | Extend window before start; pre-stage rollback    |
| Key engineer unavailable          | Identify backup resource before change start      |
| Vendor component fails            | Pre-agree vendor support during window            |
| Monitoring misses issues post-change | Set up extra alerting 24h before and 24h after |

---

## Residual Risk and Acceptance

After mitigations are documented, re-score the residual risk. If residual risk is still High or Critical, the change owner must obtain explicit written acceptance from the business owner before proceeding.

Residual risk acceptance must be recorded on the change ticket, not in email. This creates an auditable record.

---

## Risk Review During Implementation

Risk assessment is not a one-time activity. During the change window:

- Re-evaluate risk if the implementation deviates from the approved plan
- If a new risk is identified mid-window that was not assessed, pause and assess
- If the revised risk score would change the approval tier, escalate immediately
- Document any mid-window risk assessments in the change ticket notes
