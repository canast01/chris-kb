---
tags:
  - troubleshooting
  - vmware
  - vxrail
---
# VxRail — Troubleshooting

<div class="kb-summary">
Troubleshooting guide for VxRail in the VMware product context. Covers VxRail plugin unavailability, LCM pre-check failures, vSAN degraded states, and node rejoin procedures.

*Applies to: VxRail 7.x / 8.x*
</div>

```text
┌────────────────────────────────────── VxRail — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          VxRail plugin unavailable in vCenter; LCM pre-check failure blocking upgrade         │   │
│   │              vSAN object degraded or resync stuck; iDRAC hardware alert on a node             │   │
│   │  Node not rejoining cluster after maintenance; network mismatch causing VxRail Manager issues │   │
│   │        Diagnostics: VxRail API debug, LCM logs, vSAN health UI, iDRAC system event log        │   │
│   │    Escalation: support bundle export, Dell GSS P1, TAM contact, log archive for ProSupport    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define triage path · diagnostics isolate root cause · escalation engages Dell support│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │        Plugin unavail       │  │       VxRail API debug      │  │         VxRail bndl         │   │
│   │       LCM pre-chk fail      │  │        LCM log files        │  │      Dell support case      │   │
│   │        vSAN degraded        │  │        vSAN health UI       │  │        GSS escalation       │   │
│   │         iDRAC alert         │  │       iDRAC sys event       │  │         TAM contact         │   │
│   │       Node not rejoin       │  │       get-tech-support      │  │       P1 Dell ProSupp       │   │
│   │         Net mismatch        │  │       vm-support bndl       │  │         Log archive         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics pinpoint root cause · escalation gets Dell support engaged│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │  Plugin unavail  │  VxRail API dbg  │  VxRail Mgr logs  │  Bundle export   │  Restart VxRail  │   │
│   │ LCM pre-chk fail │  LCM log files   │  /var/log/vmware  │   Dell support   │   Fix + retry    │   │
│   │  vSAN degraded   │  vSAN health UI  │   /var/log/vsan   │   GSS P1 case    │   Replace disk   │   │
│   │ Node not rejoin  │  iDRAC sys evt   │     iDRAC /log    │   TAM contact    │   Re-add node    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell PowerEdge servers · NVMe/SSD/HDD · iDRAC OOB · 25GbE NICs · ToR switches                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VxRail plugin     = vCenter plugin provided by VxRail Manager; shows cluster health and LCM status   │
│  LCM pre-check     = Validation run before upgrade; fails if vSAN resync, network, or health issues   │
│  vSAN object health = vSAN tracks each VM object; degraded = FTT violated; resync = rebuilding copies │
│  iDRAC SEL         = System Event Log on iDRAC; hardware faults (disk, PSU, fan, NIC) recorded here   │
│  get-tech-support  = VxRail CLI command collecting full diagnostic bundle for Dell GSS cases          │
│  Support bundle    = Compressed log archive from VxRail Manager, ESXi hosts, and iDRAC for escalation │
│  TAM               = Technical Account Manager; Dell named support contact for critical escalations   │
│  Dell ProSupport   = Dell premium support tier; P1 = production down, response in under 4 hours       │
│  Node rejoin       = Process of ESXi host re-entering vSAN cluster after maintenance or failure       │
│  Network mismatch  = VLAN or MTU misconfiguration preventing VxRail Manager from reaching ESXi hosts  │
│  VxRail Mgr restart = Restarting Mystic service on VxRail Manager VM to recover plugin or API issues  │
│  GSS escalation    = Global Support Services; Dell/VMware support organisation for P1/P2 incidents    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <div class="kb-card">
    <h3><a href="common-issues/">Common Issues</a></h3>
    <p>VxRail plugin unavailability, LCM failures, vSAN degraded states, and node offline procedures.</p>
  </div>
  <div class="kb-card">
    <h3><a href="diagnostics/">Diagnostics</a></h3>
    <p>Log collection from VxRail Manager, ESXi hosts, iDRAC, and Dell support bundle generation.</p>
  </div>
  <div class="kb-card">
    <h3><a href="escalation/">Escalation</a></h3>
    <p>Dell support case creation, severity levels, required information, and TAM escalation.</p>
  </div>
</div>

