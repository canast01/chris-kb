---
tags:
  - servicenow
---
# Incident Resolution

<div class="kb-summary">
Incident Resolution reference covering Overview, Resolution vs Workaround, Resolution Steps Process, RCA Triggers, Post-Resolution Monitoring and 1 more sections.

*Applies to: ServiceNow*
</div>

## Overview

Resolution is the phase where the immediate problem is fixed and service is restored. It is distinct from root cause analysis — resolution focuses on getting users back online; RCA focuses on understanding why the failure happened and preventing recurrence. Both are important, but do not let RCA work delay restoration.

---

## Resolution vs Workaround

Be explicit about whether you have applied a permanent fix or a temporary workaround.

| Type         | Definition                                              | Next Step                          |
|--------------|---------------------------------------------------------|------------------------------------|
| Permanent fix| Root cause addressed; problem will not recur            | Close incident after validation    |
| Workaround   | Service restored but root cause still present           | Keep incident open; schedule fix   |
| Mitigated    | Impact reduced but not fully resolved                   | Keep P1 open; re-assess priority   |

If a workaround is applied, the incident should not be closed — it should be downgraded to a lower priority with a permanent fix scheduled and tracked.

---

## Resolution Steps Process

Follow this sequence to restore service methodically.

- [ ] Identify the specific component or configuration causing the failure
- [ ] Confirm the proposed fix with a second engineer before applying it
- [ ] Apply the fix in a controlled manner (one step at a time where possible)
- [ ] Validate immediately after each step — do not batch changes during resolution
- [ ] Confirm service health before declaring resolved
- [ ] Document each action taken and its timestamp in the incident ticket
- [ ] Notify stakeholders when service is restored (use communication templates)

---

## RCA Triggers

A formal Root Cause Analysis is required when any of the following are true:

| Trigger                                        | RCA Owner           |
|------------------------------------------------|---------------------|
| P1 incident of any duration                    | Infra Lead          |
| P2 incident exceeding SLA resolution time      | Infra Lead          |
| Repeat incident (same root cause, third time)  | Engineering Manager |
| Data loss or data exposure confirmed           | Security Lead + CTO |
| Customer-reported incident (external visibility)| Engineering Manager|

The RCA document must be started within 24 hours of resolution and completed within 5 business days. Use the RCA template in the project management section.

---

## Post-Resolution Monitoring

Service restoration is not the end of the incident window.

| Duration              | Monitoring Level                        |
|-----------------------|-----------------------------------------|
| First 30 minutes      | Active: engineer watching dashboards    |
| First 2 hours (P1)    | Active: monitoring alerts, error rate   |
| First 24 hours (P1)   | On-call aware; alert thresholds lowered |
| First 4 hours (P2)    | Active: monitoring alerts               |

If the issue recurs during the monitoring window, reopen the incident immediately — do not open a new ticket; continue the original timeline.

---

## Incident Closure Checklist

- [ ] Service confirmed healthy and validated
- [ ] Monitoring observation period completed without recurrence
- [ ] Resolution type documented (permanent fix / workaround)
- [ ] All stakeholders notified of resolution
- [ ] Incident ticket updated with full resolution summary
- [ ] RCA ticket created if required (linked to incident)
- [ ] Any follow-up actions ticketed and assigned
- [ ] Incident ticket closed with accurate start/end times and duration
