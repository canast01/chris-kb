---
tags:
  - troubleshooting
  - vmware
  - vsan
  - vsphere-8
---
# vSAN — Troubleshooting

<div class="kb-summary">
Troubleshooting reference for VMware vSAN. Covers common failure patterns, diagnostic commands, log collection, and escalation procedures for engaging VMware support.
</div>

```text
┌─────────────────────────────────────── vSAN — Troubleshooting ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     vSAN object health issues: degraded, absent, or non-compliant components cause VM risk    │   │
│   │    Resync stalls indicate disk group failures, network issues, or hosts in maintenance mode   │   │
│   │  Disk group failures remove capacity; witness connectivity loss affects stretched cluster HA  │   │
│   │       Capacity alarms at 70%/80% thresholds; address before hitting the 100% hard limit       │   │
│   │       RVC and esxcli vsan provide CLI diagnostics; vm-support bundle for GSS escalation       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define the triage path · diagnostics isolate root cause                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │       Object degraded       │  │        RVC vsan.check       │  │         vSAN Skyline        │   │
│   │         Resync stuck        │  │        vSAN health UI       │  │        GSS log bundle       │   │
│   │       Disk group fail       │  │       esxcli vsan list      │  │         HCL validate        │   │
│   │       Witness offline       │  │         vsantop perf        │  │        Stretched log        │   │
│   │        Capacity alarm       │  │        Support bundle       │  │        ESXi host log        │   │
│   │       Component absent      │  │      Policy violations      │  │        Core analysis        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics pinpoint root cause                                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │ Object degraded  │   RVC vsan.chk   │    /var/log/vmk   │  vm-support.tgz  │   Re-add disk    │   │
│   │   Resync stuck   │   esxcli vsan    │   vCenter tasks   │   GSS P1 case    │  Maint + remove  │   │
│   │ Disk group fail  │  vSAN health UI  │   /var/log/hostd  │   HCL validate   │   Disk replace   │   │
│   │ Witness offline  │   vsantop cmd    │   Witness /logs   │   TAM escalate   │   Re-sync wait   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers with NVMe/SSD/HDD · RAM DIMMs · 25GbE NICs · Witness host · ToR switches                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Object health = vSAN object state: healthy, degraded, absent, or non-compliant per SPBM policy       │
│  Resync        = Rebuild or sync of vSAN object components; stalls indicate disk or network issues    │
│  Disk group    = OSA storage unit; single disk group failure removes all its capacity from the pool   │
│  Witness       = Stretched cluster tie-breaker; if offline, vSAN cannot vote on site partition        │
│  Component     = Individual piece of a vSAN object; absent components reduce FTT protection           │
│  APD           = All Paths Down; storage network path loss; triggers vSAN network partition           │
│  PDL           = Permanent Device Loss; disk reports fatal error; data on that disk is inaccessible   │
│  RVC           = Ruby vSphere Console; vsan.check_state and vsan.vm_object_info are key commands      │
│  esxcli vsan   = vSAN CLI namespace; storage list, cluster info, and network diagnostics              │
│  Proactive rebalance = Manual or automatic redistribution of data to equalize disk usage              │
│  Capacity alarm = vSAN threshold alert at 70% (warning) and 80% (critical) utilization                │
│  vSAN Skyline  = Proactive health analytics service; identifies issues before they cause outages      │
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
