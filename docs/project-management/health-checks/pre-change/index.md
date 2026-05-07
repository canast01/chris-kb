# Pre-Change Health Check

## Overview

The pre-change check confirms that the environment is in a stable, known-good state before a change window opens. Implementing a change into an already-degraded environment makes root cause analysis harder, increases risk, and can breach the backout plan assumptions. If the environment is not healthy, the change should not proceed.

---

## Pre-Change Check Timeline

| Activity                           | When                        |
|------------------------------------|-----------------------------|
| Full pre-check sweep               | 24 hours before window      |
| Backup verification                | 24 hours before window      |
| Stakeholder notification sent      | 24–48 hours before window   |
| Go/no-go confirmation check        | 30 minutes before window    |
| Pre-change baseline snapshot       | Immediately before start    |

If the 24-hour sweep identifies issues, decide whether to resolve them or postpone the change before the go/no-go check.

---

## Pre-Change Checklist

- [ ] All services affected by the change are currently healthy
- [ ] No active incidents or P1/P2 issues on affected systems
- [ ] No monitoring alerts currently firing on affected CIs
- [ ] Recent backup confirmed successful (check backup console, not just schedule)
- [ ] Rollback / backout plan reviewed and tested in non-production
- [ ] Change ticket approved and all required approvals in place
- [ ] Change window confirmed with stakeholders (notification sent)
- [ ] All team members confirmed available and on the change bridge
- [ ] Escalation contacts confirmed available (vendor support, on-call lead)
- [ ] Access to all required systems confirmed (VPN, jump hosts, credentials)
- [ ] Runbook / implementation plan steps reviewed by the implementing engineer

---

## Go / No-Go Decision

The go/no-go check happens 30 minutes before the change window opens. Anyone on the bridge can call no-go if they have a valid concern.

| Condition                                       | Decision      |
|-------------------------------------------------|---------------|
| All pre-checks passed                           | Go            |
| Minor alert firing, unrelated to change scope   | Go (document) |
| Backup failed in last 24 hours                  | No-Go         |
| Active incident on an affected service          | No-Go         |
| Required team member unavailable, no backup     | No-Go         |
| Approval missing from required approver         | No-Go         |
| Environment behaving differently than expected  | No-Go pending investigation |

A no-go decision must be recorded in the change ticket with the reason. Reschedule promptly and communicate to stakeholders.

---

## Baseline Snapshot

Immediately before starting the change, record these values. You will compare against them in the post-change check.

| Metric               | Captured Value | Timestamp |
|----------------------|----------------|-----------|
| Service error rate   |                |           |
| Response time (p95)  |                |           |
| CPU utilisation      |                |           |
| Memory utilisation   |                |           |
| Disk usage           |                |           |
| Active connections   |                |           |

Store the snapshot in the change ticket. This is your baseline for validating success.

---

## Backup Verification

Backup verification is not just confirming the backup job ran — it is confirming the backup is restorable.

- [ ] Backup job completed without errors (check logs, not just status)
- [ ] Backup file is present in the expected location
- [ ] Backup file size is consistent with previous runs (significant deviation is a warning sign)
- [ ] For critical changes, perform a test restore of a representative subset to confirm integrity
- [ ] Record backup timestamp and location in the change ticket
