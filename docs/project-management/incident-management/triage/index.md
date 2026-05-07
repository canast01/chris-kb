# Incident Triage

## Overview

Triage is the first structured activity after an alert fires or an issue is reported. The goal is to characterise the problem quickly — not to solve it. In 10–15 minutes, triage should produce a clear priority, an initial impact statement, and a decision about whether to escalate or investigate solo. Speed and accuracy both matter.

---

## Triage Process Flow

1. Acknowledge the alert or report — stop the escalation timer
2. Identify the affected service(s) and their criticality
3. Assess current user impact (from monitoring and direct checks)
4. Set an initial priority
5. Open an incident ticket
6. Determine whether to escalate immediately or continue solo investigation
7. Post initial update to stakeholders

Complete steps 1–6 within 15 minutes for P1s and within 30 minutes for P2s.

---

## Initial Diagnosis Checklist

- [ ] Check monitoring dashboard for alerts on the affected service
- [ ] Check the service health endpoint or status page
- [ ] Review recent changes: any deployments, config changes, or infra work in the last 2 hours?
- [ ] Check infrastructure health: CPU, memory, disk, network on affected hosts
- [ ] Check application logs for errors around the time the issue started
- [ ] Check database connectivity and query performance if applicable
- [ ] Check upstream dependencies (are services this one relies on healthy?)
- [ ] Check downstream reports (are services consuming this one reporting issues?)

---

## Priority Assignment Guide

| Symptom                                           | Likely Priority |
|---------------------------------------------------|-----------------|
| Complete service unavailable to all users         | P1              |
| Error rate > 50% on primary user-facing function  | P1              |
| Partial outage affecting > 30% of users           | P1 or P2        |
| Performance degraded, service still functional    | P2 or P3        |
| Single user or team affected                      | P3              |
| Alert firing but no confirmed user impact         | P3 or P4        |
| Capacity warning (no current impact)              | P4              |

When in doubt, start higher and de-escalate when you have more information.

---

## Ticket Creation at Triage

Create the incident ticket before deep investigation begins — not after. Minimum fields to complete at triage:

| Field              | What to Enter                                          |
|--------------------|--------------------------------------------------------|
| Title              | Short, factual description (e.g., "prod API returning 502") |
| Priority           | Based on initial assessment                            |
| Affected service   | CI name from CMDB                                      |
| Detection time     | When alert fired or issue was reported                 |
| Impact summary     | Who is affected and how                                |
| Initial findings   | What you have checked so far                           |
| Assigned engineer  | Named individual taking the investigation              |

Update the ticket as you learn more. A sparse ticket is better than a delayed one.

---

## Escalate or Investigate Solo?

Make this decision at the end of triage, not after 45 minutes of solo debugging.

- [ ] Is the priority P1? → Escalate immediately; open the bridge
- [ ] Has investigation been going 20 minutes with no clear path forward? → Escalate
- [ ] Does the scope suggest multiple services or systems? → Escalate
- [ ] Is a recent change the suspected cause? → Involve the change owner
- [ ] Is the issue in a vendor-managed component? → Open vendor ticket in parallel
- [ ] Is this within your area of expertise and scope is contained? → Proceed solo with a check-in reminder set
