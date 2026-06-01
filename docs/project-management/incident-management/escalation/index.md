# Incident Escalation


<div class="kb-summary">
Incident Escalation reference covering Overview, Priority Definitions, Escalation Matrix, P1/P2 Escalation Checklist, Vendor Escalation and 1 more sections.
</div>

## Overview

Escalation ensures that incidents get the right people involved at the right time. Failing to escalate promptly extends outage duration and can breach SLAs. Over-escalating creates alert fatigue and burns out senior staff on minor issues. The matrix below provides clear criteria for when and how to escalate.

---

## Priority Definitions

| Priority | Criteria                                                               | Initial Response |
|----------|------------------------------------------------------------------------|-----------------|
| P1       | Complete service outage; data loss; security breach; SLA breach imminent | 15 minutes      |
| P2       | Significant degradation; partial outage; subset of users affected      | 30 minutes      |
| P3       | Minor degradation; workaround available; no SLA risk                   | 2 hours         |
| P4       | Informational; no current user impact; monitoring warning only         | 8 hours / next day |

Priority is set at triage and can be upgraded or downgraded as more information becomes available. Upgrades must happen immediately; downgrades can wait until impact is confirmed reduced.

---

## Escalation Matrix

| Tier       | When to Escalate                                      | Escalate To                      |
|------------|-------------------------------------------------------|----------------------------------|
| Tier 1     | Initial response; standard tooling and runbooks       | On-call engineer                 |
| Tier 2     | 30 min no progress on P1; P2 escalating; new scope    | Infra Lead / Senior Engineer     |
| Tier 3     | P1 exceeding 1 hour; data loss confirmed; breach      | CTO / VP Infra                   |
| Vendor     | Issue isolated to vendor-managed component            | Vendor support (see below)       |
| Security   | Suspected breach, data exposure, or ransomware        | Security Lead + Legal (immediate)|

Escalation does not transfer ownership — the original responder remains engaged until explicitly handed over.

---

## P1/P2 Escalation Checklist

Before escalating to Tier 2 or above:

- [ ] Incident ticket created with P1/P2 priority set
- [ ] Initial impact assessment documented in the ticket
- [ ] Basic diagnosis steps completed (service status, recent changes, log scan)
- [ ] What you have tried and what you know documented in the ticket
- [ ] Ready to brief the escalation contact with: symptom, impact, duration, steps taken

---

## Vendor Escalation

| Vendor Contact Step      | When                                         | What to Provide                        |
|--------------------------|----------------------------------------------|----------------------------------------|
| Standard support ticket  | Non-urgent, within SLA                       | Description, logs, screenshots         |
| Priority/P1 hotline      | Active P1 with vendor component implicated   | Contract/account number, ticket ref    |
| Account manager          | Escalation stalled; SLA breach at risk       | Ticket ref, business impact statement  |
| Executive escalation     | Vendor unresponsive; major SLA breach        | Formal escalation email via management |

Keep the vendor ticket number in your incident ticket. Update both tickets as the incident progresses.

---

## De-escalation Criteria

Do not maintain P1 status indefinitely. De-escalate when:

- [ ] Primary service fully restored and validated
- [ ] Monitoring confirms stable state for 30+ minutes
- [ ] No further immediate risk to users or data
- [ ] Root cause understood well enough to confirm the fix holds
- [ ] Senior stakeholders notified of de-escalation

Document de-escalation time and reason in the incident ticket. Keep the ticket open for RCA work.
