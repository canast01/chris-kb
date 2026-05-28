# Change Approval Process

```
┌─────────────────────────────────────────── Change Approval ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Change approval: RFC submitted to CAB with risk matrix, impact, and backout plan       │   │
│   │           CAB reviews risk, impact, and readiness; approves, defers, or rejects RFC           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         RFC Submission Requirements          │  │             CAB Review Criteria             │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │          Change description + scope          │  │         Risk: Low/Med/High/Critical         │   │
│   │            Business justification            │  │          Impact: services affected          │   │
│   │          Risk and impact assessment          │  │            Backout plan complete?           │   │
│   │             Implementation steps             │  │              Testing completed?             │   │
│   │                 Backout plan                 │  │            Maintenance window OK?           │   │
│   │                Test evidence                 │  │            Stakeholders notified?           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │    Risk level    │  Approval path   │   Notice period   │      Window      │   PIR required   │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │       Low        │    Change mgr    │  3 business days  │  Business hours  │     Optional     │   │
│   │      Medium      │       CAB        │  5 business days  │   Maintenance    │     Required     │   │
│   │       High       │  CAB + sponsor   │  7 business days  │   Maintenance    │     Required     │   │
│   │    Emergency     │       ECAB       │     < 4 hours     │       ASAP       │     Required     │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Risk matrix  = Likelihood × impact grid; determines required approval path                         │
│    Business sponsor= Senior stakeholder sign-off required for high-risk changes                       │
│    Deferred     = CAB sends RFC back with questions; requestor must resubmit after addressing         │
│    Notice period= Minimum lead time between RFC submission and earliest implementation date           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
