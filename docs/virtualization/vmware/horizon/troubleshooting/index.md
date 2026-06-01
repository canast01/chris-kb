# Horizon (VDI) — Troubleshooting

<div class="kb-summary">
Horizon (VDI) — Troubleshooting reference.
</div>

```
┌────────────────────────────────────── Horizon — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Connection Server failures; desktop not starting or stuck in provisioning state        │   │
│   │          Blast/PCoIP protocol latency; session disconnects; pool provisioning errors          │   │
│   │             UAG certificate issues; vGPU driver issues; App Volumes mount failures            │   │
│   │      Diagnostics: Horizon events DB, /opt/vmware/hzn logs, UAG admin UI, esxtop for vGPU      │   │
│   │     Escalation: collect Horizon log bundle and UAG support bundle; open GSS case with TAM     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define the triage path · diagnostics isolate the layer                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │         CS fail/down        │  │      Horizon events DB      │  │       Horizon log bndl      │   │
│   │        Desktop stuck        │  │       /opt/vmware/hzn       │  │       UAG support bndl      │   │
│   │       Blast/PCoIP lag       │  │         UAG admin UI        │  │        GSS case open        │   │
│   │       Session disconn       │  │         esxtop vGPU         │  │        TAM escalation       │   │
│   │        Pool prov err        │  │         App Vol log         │  │        Event DB query       │   │
│   │         UAG cert err        │  │           DCT tool          │  │         RCA template        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics pinpoint root cause                                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │     CS down      │    Events DB     │  /opt/vmware/hzn  │  Horizon bundle  │    Restart CS    │   │
│   │  Desktop stuck   │   UAG admin UI   │  /var/log/vmware  │   GSS P1 case    │  Recompose pool  │   │
│   │ Blast/PCoIP lag  │   esxtop vGPU    │    UAG /var/log   │   TAM escalate   │  Check MTU/QoS   │   │
│   │  Pool prov err   │     DCT tool     │    App Vol logs   │  Event DB query  │   Re-prov pool   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 ESXi hosts · GPU cards · RAM DIMMs · Network NICs · UAG VMs · vCenter · AD domain                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Connection Server  = Horizon broker; if down no new sessions; check Windows service and event log    │
│  UAG                = Unified Access Gateway; cert issues cause client connection failures            │
│  Desktop pool       = Group of desktops; stuck provisioning may indicate snapshot or vCenter error    │
│  Instant clone provisioning = Fork operation from parent VM; fails if parent snapshot is stale        │
│  Blast Extreme      = Display protocol; lag indicates MTU, QoS, or bandwidth constraint               │
│  PCoIP              = Display protocol; session drops often tied to UDP port blockage or MTU          │
│  vGPU               = NVIDIA virtual GPU; driver mismatch causes display or performance failures      │
│  DCT (Desktop Connectivity Tool) = Horizon diagnostic tool for end-to-end session connectivity        │
│  Horizon events database = SQL DB logging all session and admin events; query for error codes         │
│  Recompose          = Operation to push new image to pool desktops; resolves stuck provisioning       │
│  Log bundle         = Horizon diagnostic package collected from Connection Server for GSS             │
│  TAM escalation     = Technical Account Manager escalation for critical production incidents          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── Horizon — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Connection Server failures; desktop not starting or stuck in provisioning state        │   │
│   │          Blast/PCoIP protocol latency; session disconnects; pool provisioning errors          │   │
│   │             UAG certificate issues; vGPU driver issues; App Volumes mount failures            │   │
│   │      Diagnostics: Horizon events DB, /opt/vmware/hzn logs, UAG admin UI, esxtop for vGPU      │   │
│   │     Escalation: collect Horizon log bundle and UAG support bundle; open GSS case with TAM     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define the triage path · diagnostics isolate the layer                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │         CS fail/down        │  │      Horizon events DB      │  │       Horizon log bndl      │   │
│   │        Desktop stuck        │  │       /opt/vmware/hzn       │  │       UAG support bndl      │   │
│   │       Blast/PCoIP lag       │  │         UAG admin UI        │  │        GSS case open        │   │
│   │       Session disconn       │  │         esxtop vGPU         │  │        TAM escalation       │   │
│   │        Pool prov err        │  │         App Vol log         │  │        Event DB query       │   │
│   │         UAG cert err        │  │           DCT tool          │  │         RCA template        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics pinpoint root cause                                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │     CS down      │    Events DB     │  /opt/vmware/hzn  │  Horizon bundle  │    Restart CS    │   │
│   │  Desktop stuck   │   UAG admin UI   │  /var/log/vmware  │   GSS P1 case    │  Recompose pool  │   │
│   │ Blast/PCoIP lag  │   esxtop vGPU    │    UAG /var/log   │   TAM escalate   │  Check MTU/QoS   │   │
│   │  Pool prov err   │     DCT tool     │    App Vol logs   │  Event DB query  │   Re-prov pool   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 ESXi hosts · GPU cards · RAM DIMMs · Network NICs · UAG VMs · vCenter · AD domain                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Connection Server  = Horizon broker; if down no new sessions; check Windows service and event log    │
│  UAG                = Unified Access Gateway; cert issues cause client connection failures            │
│  Desktop pool       = Group of desktops; stuck provisioning may indicate snapshot or vCenter error    │
│  Instant clone provisioning = Fork operation from parent VM; fails if parent snapshot is stale        │
│  Blast Extreme      = Display protocol; lag indicates MTU, QoS, or bandwidth constraint               │
│  PCoIP              = Display protocol; session drops often tied to UDP port blockage or MTU          │
│  vGPU               = NVIDIA virtual GPU; driver mismatch causes display or performance failures      │
│  DCT (Desktop Connectivity Tool) = Horizon diagnostic tool for end-to-end session connectivity        │
│  Horizon events database = SQL DB logging all session and admin events; query for error codes         │
│  Recompose          = Operation to push new image to pool desktops; resolves stuck provisioning       │
│  Log bundle         = Horizon diagnostic package collected from Connection Server for GSS             │
│  TAM escalation     = Technical Account Manager escalation for critical production incidents          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently seen problems and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to VMware support.</span>
</a>

</div>
