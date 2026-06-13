---
tags:
  - troubleshooting
  - vcf
  - vmware
search:
  boost: 1.5
---
# VCF — Troubleshooting

<div class="kb-summary">
Troubleshooting reference for VMware Cloud Foundation. Covers common SDDC Manager and LCM failure patterns, workload domain issues, diagnostic commands, log collection, and escalation procedures.

*Applies to: VCF 4.x / 5.x*
</div>

```text
┌──────────────────────────────────────── VCF — Troubleshooting ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        SoS health check failures; workload domain deployment errors; LCM upgrade stalls       │   │
│   │      NSX host prep failures in VCF; SDDC Manager service issues; password rotation errors     │   │
│   │       Diagnostics: SoS tool output, SDDC Manager logs, SDDC REST API debug, NSX prep log      │   │
│   │      Log collection: VCF support bundle via SDDC Manager; attach to GSS case for analysis     │   │
│   │       Escalation: TAM/GSS for P1; BOM mismatch validation; Skyline proactive diagnostics      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define the triage path · diagnostics isolate root cause                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │       SoS health fail       │  │       SoS tool output       │  │       VCF support bndl      │   │
│   │       Workload dom err      │  │        SDDC Mgr logs        │  │       GSS/TAM escalate      │   │
│   │          LCM stall          │  │          API debug          │  │         BOM mismatch        │   │
│   │        NSX prep fail        │  │        Domain health        │  │        Core analysis        │   │
│   │        SDDC svc down        │  │         NSX prep log        │  │           Skyline           │   │
│   │       Password rot err      │  │         vSAN health         │  │          P1 process         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics pinpoint root cause                                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │     SoS fail     │   SoS tool run   │  /var/log/vmware  │   VCF bndl.tgz   │    Re-run SoS    │   │
│   │    Domain err    │  SDDC API debug  │   SDDC Mgr logs   │   GSS P1 case    │   Redeploy dom   │   │
│   │    LCM stall     │   NSX prep log   │    /var/log/nsx   │   TAM escalate   │    LCM retry     │   │
│   │  NSX prep fail   │  vSAN health UI  │   /var/log/vsan   │   BOM validate   │   Re-prep NSX    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers · PCIe NICs · ToR switches · vSAN/SAN · OOB management network                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SoS tool      = Support and Serviceability; CLI tool that validates all VCF component health states  │
│  LCM stall     = Lifecycle Manager upgrade task stuck; check SDDC Manager logs and retry via API      │
│  NSX host prep = VCF NSX transport node preparation; fails if ESXi version or network config mismatch │
│  SDDC Manager service = Core VCF service; restart via systemctl if dashboard is unresponsive          │
│  Workload domain error = Domain add/expand task failure; review SDDC Manager task log for detail      │
│  BOM mismatch  = Component versions outside validated BOM; must resolve before LCM can proceed        │
│  VCF support bundle = Downloaded from SDDC Manager; contains logs for all VCF components              │
│  Password rotation failure = SoS rotation error; check component connectivity and account lockout     │
│  Skyline Health = VMware proactive diagnostics; collects and analyzes VCF telemetry for known issues  │
│  TAM escalation = Technical Account Manager engagement for critical VCF production incidents          │
│  GSS P1/P2     = Global Support Services priority; P1=production down, P2=significant degradation     │
│  Cloud Builder deployment = Initial bring-up failures; review JSON spec and network pre-check output  │
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

