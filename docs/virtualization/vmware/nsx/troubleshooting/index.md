---
tags:
  - nsx
  - nsx-4
  - troubleshooting
  - vmware
---
# NSX — Troubleshooting

<div class="kb-summary">
Troubleshooting reference for VMware NSX. Covers common overlay, gateway, and DFW failure patterns, diagnostic commands, log collection, and escalation procedures.

*Applies to: NSX-T 3.x / NSX 4.x*
</div>

```text
┌──────────────────────────────────────── NSX — Troubleshooting ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │NSX troubleshooting: transport node failures, routing issues, DFW drops, and escalation process│   │
│   │    Common issues: TN prep failure, BGP peer down, DFW asymmetric drop, Manager unreachable    │   │
│   │     Diagnostics: nsxcli on Edge for routing state; connectivity checker; flow analysis API    │   │
│   │        Log collection: get-tech-support on Manager and Edge; attach bundle to GSS case        │   │
│   │    Escalation: NSX support bundle; TAM for P1; verify vSphere and NSX version compatibility   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define the triage path · diagnostics isolate the layer                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │       TN prep failure       │  │      nsxcli get routes      │  │       get-tech-support      │   │
│   │        BGP peer down        │  │      Connectivity chkr      │  │        GSS P1/P2 case       │   │
│   │        DFW asymm drop       │  │      Flow analysis API      │  │        TAM escalation       │   │
│   │     Manager unreachable     │  │     Packet capture edge     │  │      Version compat chk     │   │
│   │      MTU mismatch drop      │  │       /var/log/syslog       │  │      Core dump collect      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics use nsxcli and flow analysis                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │   TN prep fail   │  nsxcli routes   │  /var/log/syslog  │  get-tech-supp   │    Re-prep TN    │   │
│   │  BGP peer down   │  Conn. checker   │    /image/logs/   │   GSS P1 case    │   BGP re-peer    │   │
│   │  DFW drop asym   │  Flow analysis   │   Manager syslog  │   TAM escalate   │   Rule reorder   │   │
│   │  MTU black hole  │   Pkt capture    │    Edge var/log   │  Compat matrix   │   MTU fix ToR    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 ESXi hosts · Edge VM nodes · ToR switches (BGP) · Physical NICs (TEP uplinks) · OOB mgmt         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TN prep failure = Transport node preparation failed; check ESXi version compat and network config    │
│  BGP peer down  = T0 BGP session to ToR dropped; check BFD timers, interface IP, and AS numbers       │
│  DFW asymmetric = Stateful DFW receives return traffic on different host with no state; causes drops  │
│  MTU mismatch   = GENEVE requires MTU ≥1600; lower ToR MTU causes silent packet drops in overlay      │
│  Connectivity checker = NSX built-in tool; tests L2/L3 connectivity between two endpoints in overlay  │
│  Flow analysis  = NSX API that queries per-VM traffic flows; identifies which DFW rule applied        │
│  get-tech-support = NSX CLI command on Manager/Edge; collects full support bundle for GSS             │
│  nsxcli         = NSX Edge CLI; namespaces: get (read), set (write), debug (packet capture)           │
│  TEP            = Tunnel End Point; VMkernel port on ESXi/Edge; source/dest of GENEVE packets         │
│  MPA            = Management Plane Agent on transport nodes; if offline, node appears disconnected    │
│  Core dump      = NSX Manager/Edge crash dump; required for P1 escalation analysis by support         │
│  Version compat = NSX to vSphere version compatibility; mismatch can cause TN prep or upgrade failures│
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

