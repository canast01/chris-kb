---
tags:
  - aws
  - troubleshooting
search:
  boost: 1.5
---
# AWS — Escalation


<div class="kb-summary">
AWS support case creation, severity level selection, TAM escalation path, and required diagnostics before opening a case.
</div>

```text
┌───────────────────────────── AWS Escalation — Support & Trusted Advisor ──────────────────────────────┐
│                                                                                                       │
│  AWS support tiers, escalation paths, and Trusted Advisor checks for proactive guidance.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Support Plans                 │  │               Escalation Path               │   │
│   │       Developer: 12h business response       │  │         1. Internal runbook attempt         │   │
│   │       Business: 1h production response       │  │         2. AWS console support case         │   │
│   │      Enterprise On-Ramp: 30min critical      │  │       3. Severity: Urgent/High/Normal       │   │
│   │     Enterprise: 15min + TAM + Concierge      │  │       4. TAM escalation if Enterprise       │   │
│   │    Business+: all Trusted Advisor checks     │  │       5. AWS executive escalation path      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Include CloudTrail events, CloudWatch metrics, and resource IDs when opening cases.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Trusted Advisor Checks            │  │            AWS Health & Proactive           │   │
│   │      Cost: idle instances, underused RI      │  │          AWS Health: account events         │   │
│   │       Security: MFA, open SGs, key age       │  │      Proactive events: TAM notification     │   │
│   │       Fault tolerance: AZ coverage, DR       │  │        Well-Architected Tool: review        │   │
│   │      Performance: overloaded instances       │  │       re:Post: community Q&A platform       │   │
│   │      Service limits: approaching quotas      │  │      Service Quotas: self-service raise     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS support infrastructure · TAM engagement portal · Trusted Advisor analysis plane                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TAM             = Technical Account Manager; designated AWS engineer for Enterprise plans            │
│  Severity Urgent  = Production system down; 15-min response time on Enterprise plan                   │
│  Severity High   = Significant business impact; 1h response on Business plan                          │
│  Trusted Advisor = AWS automated best-practice checks across 5 pillars                                │
│  Well-Architected = AWS framework review across 6 pillars; tool generates findings                    │
│  Service Quotas  = Service that tracks and enables self-service quota increase requests               │
│  Concierge       = Enterprise support specialist for billing and account questions                    │
│  re:Post         = AWS community Q&A platform replacing forums; AWS experts answer                    │
│  Proactive event = TAM-initiated notification about upcoming maintenance or risk                      │
│  Support case    = Ticket opened in AWS console with issue details and severity                       │
│  Cost optimisation check= Trusted Advisor identifies idle/underutilised resources                     │
│  Service limit   = Account-level quota on AWS resources; some auto-raise, some manual                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Troubleshooting](../index.md) section.

---

AWS Support plans range from Developer (business-hours email, general guidance) through Business (24/7 phone/chat, <1 hr critical response, Trusted Advisor full checks) to Enterprise (TAM, <15 min critical response, concierge support). Support cases are opened via the AWS Console under Support Center or programmatically via the AWS Support API (`aws support create-case`). Before opening a case, collect the affected resource ARNs, account ID, region, approximate start time of the issue, and relevant CloudWatch logs or VPC Flow Logs.

| Plan | Best for | Critical response SLA |
|---|---|---|
| Developer | Dev/test, individual | < 12 hours (business hours) |
| Business | Production workloads | < 1 hour |
| Enterprise On-Ramp | Growing production | < 30 minutes |
| Enterprise | Mission-critical / large scale | < 15 minutes + TAM |

**Key resources:**

- AWS Support Center: `console.aws.amazon.com/support`
- AWS Health Dashboard: `health.aws.amazon.com` — service event and account-specific health notifications
- Trusted Advisor: automated checks for cost, security, fault tolerance, performance, and service limits
- Support API: `aws support describe-cases`, `aws support create-case` (requires Business or Enterprise plan)

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
