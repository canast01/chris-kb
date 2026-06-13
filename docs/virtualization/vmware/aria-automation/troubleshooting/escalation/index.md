---
tags:
  - aria-automation
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Automation — Escalation

```bash
# SSH to the Aria Automation appliance
ssh root@vra-prod-01.example.local

# Generate the support bundle (this takes 5–15 minutes)
vracli support-bundle

# Bundle is saved to /tmp/ — check the filename
ls -lh /tmp/vracli-support-bundle*.tar.gz

# Copy to a local machine for upload
scp root@vra-prod-01.example.local:/tmp/vracli-support-bundle*.tar.gz /tmp/
```
```text
┌──────────────────────────────────── Aria Automation — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│  Escalate vRA issues when self-service diagnostics are exhausted and impact is unresolved.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │          Prepare Before Escalating          │   │
│   │          vRA service down > 30 min           │  │       Support bundle (LCM logscraper)       │   │
│   │      Data loss or corruption suspected       │  │         vRA version and patch level         │   │
│   │         Upgrade failure mid-process          │  │        Timeline of events and changes       │   │
│   │       Security breach or data exposure       │  │         Deployment events + pod logs        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Open VMware SR with P1 priority for service-down; provide bundle and timeline.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             VMware Support Path              │  │             Internal Escalation             │   │
│   │         SR: my.vmware.com or portal          │  │      Platform team: notify stakeholders     │   │
│   │       P1: live call with GSS engineer        │  │       Change freeze if upgrade-related      │   │
│   │     TAM: escalate for critical accounts      │  │       DR: consider vRA failover if HA       │   │
│   │        KB: search kb.vmware.com first        │  │        Post-incident: RCA within 48h        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliance cluster · LCM · Postgres · vIDM · vCenter · support upload endpoint                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SR                = Support Request; formal case opened with VMware GSS                              │
│  P1 priority       = Critical severity; service down with no workaround; live engineer call           │
│  GSS               = Global Support Services; VMware technical support team                           │
│  TAM               = Technical Account Manager; premium support contact for critical accounts         │
│  LCM logscraper    = Diagnostic archive tool; collect before calling support                          │
│  Support bundle    = Generated from VAMI or LCM; contains pod logs, DB state, configs                 │
│  Change freeze     = Halt all non-critical changes during active incident investigation               │
│  RCA               = Root Cause Analysis; post-incident document describing failure and fix           │
│  vRA HA            = High Availability mode; second vRA node can serve if primary fails               │
│  kb.vmware.com     = VMware Knowledge Base; search before opening SR to find known fixes              │
│  Timeline          = Chronological record of events, changes, and symptoms before the issue           │
│  Stakeholder notif = Communicate impact and ETA to application owners and business units              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
