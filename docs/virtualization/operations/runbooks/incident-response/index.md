# Incident Response Runbook

```
┌────────────────────────────────────── Incident Response Runbook ──────────────────────────────────────┐
│                                                                                                       │
│    Use for any active VMware platform issue; follow phases in order                                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Detect + Assess       │  │        Contain + Fix        │  │       Resolve + Close       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │     Alert or user report    │  │        Isolate scope        │  │       Verify fix holds      │   │
│   │    Confirm issue is real    │  │        Prevent spread       │  │        Monitor 30 min       │   │
│   │     Open incident ticket    │  │    Apply fix / workaround   │  │     Notify stakeholders     │   │
│   │    Define scope: VM/host    │  │       Collect evidence      │  │         Close ticket        │   │
│   │    Set severity P1/P2/P3    │  │        Escalate if P1       │  │         Schedule RCA        │   │
│   │     Notify stakeholders     │  │      Update ticket live     │  │       Post-mortem doc       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    P1 = Critical; full platform or business service down; immediate escalation required               │
│    P2 = Major; significant degradation; resolve within business hours                                 │
│    P3 = Minor; limited impact; resolve within next maintenance window                                 │
│    Contain   = Stop the issue spreading before applying a fix; e.g. isolate a host                    │
│    Workaround = Temporary fix to restore service; permanent fix follows in RCA action                 │
│    Post-mortem = Written RCA document; timeline, root cause, and preventive actions                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Use this when there is an active VMware platform issue.

```text
Incident Triage Flow
═══════════════════════════════════════════════════════════

  DETECT
  ├─ Alert fired / user report / monitoring alarm
  └─ Confirm issue is real ──► open incident ticket
           │
           ▼
  ASSESS
  ├─ Define scope: VM · host · cluster · full platform?
  ├─ Identify impacted services and users
  └─ Set severity P1 / P2 / P3
           │
           ▼
  CONTAIN
  ├─ Prevent further spread (isolate host, disable change)
  ├─ Confirm HA has restarted critical VMs
  └─ Communicate status to stakeholders
           │
           ▼
  FIX
  ├─ vCenter available? ──► check alarms, events, tasks
  ├─ Host issue?         ──► ping, SSH, vpxa, hostd
  ├─ Storage issue?      ──► paths, vSAN health, APD/PDL
  ├─ Network issue?      ──► uplinks, port groups, NSX
  └─ Escalate to vendor if root cause unclear
           │
           ▼
  VALIDATE
  ├─ All hosts connected
  ├─ VMs running
  ├─ Monitoring clean
  └─ Application owner confirms OK
           │
           ▼
  DOCUMENT
  └─ Timeline · evidence · resolution → close ticket → RCA
```

## Steps

1. Confirm the issue scope
2. Identify impacted systems
3. Check vCenter availability
4. Check host and cluster health
5. Review active alarms
6. Check recent tasks and events
7. Check datastore and vSAN health
8. Check network health
9. Check hardware alerts
10. Review logs
11. Escalate if needed
12. Document findings
13. Confirm recovery
14. Communicate status
15. Complete RCA if required

## Evidence to Capture

- Date and time of issue
- Impacted VMs, hosts, clusters, or datastores
- Screenshots of alarms
- Recent vCenter events
- Logs from vCenter or ESXi
- Support bundles if needed
- Timeline of actions taken
- Validation after recovery
