---
tags:
  - servicenow
---
# Pre-Maintenance Checks

<div class="kb-summary">
Pre-Maintenance Checks reference covering Overview, Pre-Check Timeline, Environment Health Checklist, Backup Verification, Rollback Readiness and 2 more sections.

*Applies to: ServiceNow*
</div>

## Overview

Pre-maintenance checks are the final gate before a window opens. They confirm that the environment is in the expected state, backups are valid, the team is ready, and all logistical requirements are met. A failed pre-check is a reason to defer — not push through.

---

## Pre-Check Timeline

| Activity                           | When                           |
|------------------------------------|--------------------------------|
| Environment health sweep           | 24 hours before window         |
| Backup verification                | 24 hours before window         |
| Implementation plan review         | 24 hours before window         |
| Team readiness confirmation        | Day of window (morning)        |
| Final go/no-go sweep               | 30–60 minutes before window    |
| Baseline metric snapshot           | Immediately before first task  |

If the 24-hour sweep uncovers an issue, decide whether to resolve it or defer the window before the day-of checks begin.

---

## Environment Health Checklist

- [ ] All services affected by the maintenance window are currently healthy
- [ ] No active incidents or degraded services on affected CIs
- [ ] Monitoring dashboards showing normal state (no unexplained drift in metrics)
- [ ] No alerts currently firing on affected services
- [ ] Recent changes reviewed — nothing unexpected landed in the last 24 hours
- [ ] Disk space adequate on all affected hosts (minimum 20% free)
- [ ] Network connectivity confirmed between maintenance team and affected systems

---

## Backup Verification

Confirm backups before any destructive or irreversible task.

| Asset Type          | Backup Check                                        | Pass Criteria                  |
|---------------------|-----------------------------------------------------|--------------------------------|
| Database            | Last full backup completed without errors           | Within 24 hours; size normal   |
| VM / server         | Snapshot or image taken                             | Snapshot exists and is healthy |
| Config files        | Config exported and stored in version control       | Commit present in repo         |
| Application data    | App-level export or backup job confirmed            | Export file present and sized  |

For critical databases or destructive migrations, perform a test restore of a subset before the window opens.

---

## Rollback Readiness

- [ ] Backout plan reviewed by a second engineer
- [ ] Rollback tested in non-production (where applicable)
- [ ] Rollback decision deadline set and recorded in the ticket
- [ ] All team members on the bridge aware of backout criteria
- [ ] Any required vendor support for rollback confirmed and on standby

---

## Team and Access Readiness

- [ ] All required engineers confirmed available and aware of their roles
- [ ] Bridge/virtual room open and tested (audio, video, screen share)
- [ ] VPN, jump hosts, and bastion access confirmed for all participants
- [ ] Credentials and secrets confirmed accessible (vault, password manager)
- [ ] Runbook / implementation plan visible to all participants
- [ ] Escalation contacts available and notified of window time

---

## Final Go / No-Go

The go/no-go decision is made on the bridge 30 minutes before window open. Record the outcome in the ticket.

| Condition                                             | Decision       |
|-------------------------------------------------------|----------------|
| All pre-check items passed                            | Go             |
| All team members present on bridge                    | Go             |
| Backup confirmed valid                                | Go             |
| Active alert on affected service (unrelated)          | Assess; likely No-Go |
| Backup failed or not found                            | No-Go          |
| Required engineer absent, no backup available         | No-Go          |
| Unexpected infrastructure event in last 2 hours       | No-Go          |

A no-go defers the window. Communicate the deferral to stakeholders immediately.
