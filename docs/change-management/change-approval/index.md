# Change Approval Process

Ensures all changes are assessed for risk and approved by the appropriate authority before implementation.

## Change Types and Approval Requirements

| Change Type | Risk | Approval Required | Lead Time |
|---|---|---|---|
| Standard (pre-approved) | Low | None — pre-approved template | Immediate |
| Normal — Low risk | Low-Medium | Team lead or service owner | 5 business days |
| Normal — High risk | High | CAB (Change Advisory Board) | 10 business days |
| Emergency | Critical | eCAB or single approver on-call | < 4 hours |

## CAB Approval Workflow

```text
Requester submits RFC
        ↓
Technical review (peer / architect)
        ↓
Risk assessment (Impact × Likelihood)
        ↓
CAB review meeting
        ↓
Approved / Rejected / Deferred
        ↓
Requester notified → scheduled for change window
```

## Risk Classification Matrix

| Impact ↓ / Likelihood → | Low | Medium | High |
|---|---|---|---|
| Low | Low | Low | Medium |
| Medium | Low | Medium | High |
| High | Medium | High | Critical |

- **Low / Medium**: Team lead approval
- **High**: CAB approval required
- **Critical**: CAB + service owner + management sign-off

## ITSM Approval Fields

Every RFC must include before approval:

| Field | Requirement |
|---|---|
| Business justification | Required |
| Rollback plan | Required (tested in non-prod for High/Critical) |
| Outage window | Required (start time, duration, affected services) |
| Test results | Required for High risk |
| Affected CIs | List all Configuration Items from CMDB |
| Communication plan | Required for user-impacting changes |

## Approval Checklist

- [ ] RFC fully completed (no blank required fields)
- [ ] Risk score calculated and documented
- [ ] Rollback procedure documented and tested
- [ ] Change window booked and communicated
- [ ] Service owner has reviewed and approved
- [ ] For High/Critical: CAB has reviewed in meeting (not async)
- [ ] Post-implementation review scheduled
- [ ] Related incidents/problems linked in ITSM

## Common Rejection Reasons

| Reason | Remediation |
|---|---|
| No rollback plan | Document step-by-step rollback procedure |
| Insufficient testing | Provide non-prod test evidence |
| Change window conflicts | Coordinate with affected teams; rebook window |
| Missing CMDB CIs | Update RFC with all affected configuration items |
| No stakeholder sign-off | Obtain written approval from service owner |
