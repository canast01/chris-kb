---
tags:
  - dell
  - troubleshooting
---
# APEX Storage as a Service — Troubleshooting

<div class="kb-summary">
APEX Storage as a Service — Troubleshooting navigation for Common Issues, Diagnostics, Escalation.
</div>

```text
┌────────────────────────────────── Dell Apex STaaS — Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Apex troubleshooting: host path failures, performance issues, capacity alerts         │   │
│   │        Host path: check multipath status, iSCSI sessions, FC logins, VLAN reachability        │   │
│   │        Performance: check CloudIQ IOPS/latency graphs; identify noisy-neighbour volumes       │   │
│   │        Capacity: CloudIQ alert at 80% committed; open SR to expand before hitting burst       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom → CloudIQ health → host path check → array alert → SR to Dell → resolve                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Connectivity        │  │         Performance         │  │           Capacity          │   │
│   │        Host path down       │  │         High latency        │  │       Near-full alert       │   │
│   │        iSCSI session        │  │        IOPS throttle        │  │        Burst billing        │   │
│   │        FC login fail        │  │         Queue depth         │  │          Expand SR          │   │
│   │        VLAN mismatch        │  │         Noisy volume        │  │         Thin reclaim        │   │
│   │         SCG offline         │  │         Slow rebuild        │  │       Forecast review       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Hardware faults are Dell responsibility; open P1 SR immediately for controller alarms              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │   First check    │        Tool       │    Resolution    │    Escalation    │   │
│   │    Path down     │  multipath -ll   │      Host OS      │  Fix VLAN/zone   │    Dell SR P2    │   │
│   │   High latency   │  CloudIQ graph   │      CloudIQ      │  Throttle/move   │    Dell SR P2    │   │
│   │   Capacity 80%   │   Usage report   │    Apex Console   │  Open expand SR  │      P3 SR       │   │
│   │   SCG offline    │  SCG VM status   │    SCG console    │  Restart SCG VM  │    Dell SR P3    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: multipath paths (cable, SFP, switch) · iSCSI VLAN tagging · FC zone check                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    multipath -ll   = Linux command; shows all paths to each storage device with status                │
│    Path down       = Multipath shows one path in "failed" state; I/O continues on other path          │
│    iSCSI session   = Active TCP connection between host initiator and array iSCSI target              │
│    FC login fail   = Host HBA cannot FLOGI to fabric; check zoning and WWN registration               │
│    IOPS throttle   = Array QoS limiting IOPS on a volume; shown as max-rate in CloudIQ                │
│    Noisy volume    = High-I/O volume consuming array resources impacting other volumes                │
│    Queue depth     = Outstanding I/O requests per path; excessive depth causes latency                │
│    SCG offline     = Secure Connect Gateway VM stopped; CloudIQ data gap; no SupportAssist            │
│    Thin reclaim    = UNMAP/TRIM commands return unused thin-provisioned blocks to pool                │
│    Capacity SR     = Service Request to expand Apex committed tier; include usage data                │
│    P1/P2 severity  = P1=production down; P2=degraded; drives Dell response SLA                        │
│    Controller alarm = CloudIQ or SupportAssist alert on controller hardware; P1 SR now                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>

