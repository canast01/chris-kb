---
tags:
  - srm
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# SRM — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Collect SRM Support Bundle, vSphere Replication Log Collection, SRA Logs, Check SRM Service Status, Verify Site Pairing Certificate and 2 more sections.

*Applies to: SRM 8.x / 9.x*
</div>

  SRM Diagnostic Data Sources
```text
┌────────────────────────────────────── VMware SRM — Diagnostics ───────────────────────────────────────┐
│                                                                                                       │
│  SRM diagnostics use support bundles, SRM Server logs, vSphere Replication logs,                      │
│  SRA diagnostic files, and vCenter events to diagnose failures.                                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               SRM Server Logs                │  │               vSphere Rep Logs              │   │
│   │   C:\ProgramData\VMware\VMware vCenter SRM   │  │       vSphere Rep appliance: /var/log       │   │
│   │          vmware-dr-*.log: main log           │  │           hbrsrv.log: replication           │   │
│   │            vmware-srmserver-*.log            │  │           hbrfilter.log: I/O path           │   │
│   │            Support bundle: SRM UI            │  │           vR appliance: VM on ESXi          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Start with SRM support bundle; vmware-dr-*.log has full plan execution detail.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               SRA Diagnostics                │  │                vCenter Events               │   │
│   │          SRA: vendor-specific tool           │  │              Filter: SRM events             │   │
│   │            Dell: SRDF/Metro diag             │  │          Tasks: SRM plan run tasks          │   │
│   │           NetApp: snapmirror show            │  │          Events: site pair connect          │   │
│   │             SRA log: C:\SRA\logs             │  │          Alarms: replication error          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SRM Server logs accessed via RDP to Windows VM; vSphere Rep logs via SSH to appliance;               │
│  support bundle generated via SRM vSphere Client plugin.                                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vmware-dr-*.log= main SRM log; plan execution, steps, errors                                         │
│  vmware-srmserver= SRM application service log                                                        │
│  hbrsrv.log    = vSphere Replication server log; replication status                                   │
│  hbrfilter.log = I/O filter log; per-VM replication I/O path                                          │
│  SRA log       = array adapter log; in C:\SRA\logs on SRM Server                                      │
│  Support bundle= SRM UI > Administration > Support; ZIP download                                      │
│  vSphere Rep   = vSphere Replication appliance; separate VM from SRM                                  │
│  snapmirror show= NetApp CLI; shows replication relationship status                                   │
│  SRDF          = Dell EMC array replication; vendor CLI for diag                                      │
│  vCenter events= Administration > Events; filter to SRM events                                        │
│  Plan tasks    = vCenter Tasks; SRM records plan steps as vCenter tasks                               │
│  ProgramData   = Windows hidden folder; SRM writes logs here                                          │
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
