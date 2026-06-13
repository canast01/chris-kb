---
tags:
  - operations
---
# Virtualization Evidence Collection


<div class="kb-summary">
Virtualization Evidence Collection reference covering Overview, Pre-Checks, Steps, Validation, Rollback and 1 more sections.
</div>

```text
┌───────────────────────────── Virtualization Evidence Collection Runbook ──────────────────────────────┐
│                                                                                                       │
│    Collect evidence before vendor escalation, RCA work, or major incident review                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Pre-Checks                  │  │                   Collect                   │   │
│   │        ──────────────────────────────        │  │        ─────────────────────────────        │   │
│   │             Confirm issue scope              │  │           Screenshot active alarms          │   │
│   │           Confirm affected objects           │  │           Export tasks and events           │   │
│   │        Confirm timestamps + timezone         │  │           Note object names + IDs           │   │
│   │            Confirm recent changes            │  │           Collect ESXi / VCSA logs          │   │
│   │         Confirm ticket / case number         │  │           Capture version strings           │   │
│   │                                              │  │            Export support bundle            │   │
│   │                                              │  │             Attach all to ticket            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Support bundle  = vm-support.sh output; full ESXi/VCSA log archive for vendor support              │
│    Tasks + events  = vCenter audit trail; export via Monitor → Tasks for the time window              │
│    Affected object = VM, host, datastore, or network affected by the incident                         │
│    Case number     = Vendor support ticket ID; always reference in evidence bundle name               │
│    Timezone        = Always record timestamps in UTC to avoid ambiguity across regions                │
│    RCA             = Root Cause Analysis; requires accurate timeline and evidence log                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

Use this before vendor escalation, RCA work, or major incident review.

## Pre-Checks

- Confirm issue scope.
- Confirm affected objects.
- Confirm timestamps.
- Confirm recent changes.
- Confirm ticket or case number if available.

## Steps

1. Capture screenshots of alarms.
2. Export recent tasks and events.
3. Capture affected object names.
4. Capture timestamps and timezone.
5. Collect support bundles if needed.
6. Record commands already run.
7. Record impact and current status.

## Validation

- Evidence is complete enough for handoff.
- Timeline is clear.
- Affected systems are listed.
- Next owner has what they need.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
