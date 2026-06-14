---
title: RCA Template
tags:
  - operations
---

# RCA Template


<div class="kb-summary">
RCA Template reference covering Summary, Impact, Timeline, Root Cause, Resolution and 2 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌───────────────────────────────── RCA Template — Root Cause Analysis ──────────────────────────────────┐
│                                                                                                       │
│    Complete after every P1/P2 incident; attach to change record and share with team                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Document Sections               │  │                 Action Items                │   │
│   │        ──────────────────────────────        │  │        ─────────────────────────────        │   │
│   │            Summary: what happened            │  │           Immediate: already done           │   │
│   │           Impact: systems + users            │  │          Short-term: within 7 days          │   │
│   │           Timeline: ordered events           │  │        Long-term: prevent recurrence        │   │
│   │          Root cause: why it failed           │  │           Owner assigned per item           │   │
│   │             Contributing factors             │  │                Due dates set                │   │
│   │                What went well                │  │               Tracked in ITSM               │   │
│   │               Lessons learned                │  │           Reviewed at team meeting          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Root cause      = The single underlying reason the incident occurred; not a symptom                │
│    Contributing    = Factors that made the failure worse or harder to detect                          │
│    Timeline        = Chronological event log from first detection to resolution                       │
│    5 Whys          = Ask "why" five times to drill from symptom to root cause                         │
│    Action item     = Specific task with owner and due date to prevent recurrence                      │
│    Blameless RCA   = Focus on system/process failures, not individual mistakes                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Summary

Brief description of what happened.

## Impact

Systems, users, applications, or services affected.

## Timeline

| Time | Event |
|---|---|
| HH:MM | Issue detected |
| HH:MM | Investigation started |
| HH:MM | Cause identified |
| HH:MM | Fix applied |
| HH:MM | Service restored |

## Root Cause

Explain the actual cause of the issue.

## Resolution

Explain what was done to fix it.

## Prevention

List steps to reduce the chance of the issue happening again.

## Evidence

Attach logs, screenshots, events, support case numbers, and validation results.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [VMware Backup Failure Runbook](backup-failure.md)
- [VMware Certificate Renewal Runbook](certificate-renewal-planning.md)
- [vCenter Certificate Rotation Runbook](certificate-rotation.md)
- [Virtualization Runbooks](index.md)
