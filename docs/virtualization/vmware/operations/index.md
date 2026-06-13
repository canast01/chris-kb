---
tags:
  - operations
  - vmware
---
# VMware Operations

<div class="kb-summary">
Operational runbooks and procedures for VMware platform management.
</div>

```text
┌──────────────────────────────── VMware Platform — Operations Overview ────────────────────────────────┐
│                                                                                                       │
│   Day-2 operations: runbooks for repeatable tasks; health checks for platform state review            │
│   All runbooks use PowerCLI or vCenter UI steps; tested against vSphere 8.x / VCF 5.x                 │
│   Run health check weekly minimum; always run before and after significant change windows             │
│                                                                                                       │
│   Common operational tasks                                                                            │
│   VM snapshot: create → verify post-change → remove within 72h; consolidate before next change        │
│   Host maintenance: enter DRS drain → wait for evacuation → apply patch → remediate → exit maint      │
│   Cluster health: check HA status → vSAN health service → alarm panel → resource utilisation          │
│   Capacity review: cluster utilisation trend → growth forecast → raise procurement if >80% sustained  │
│   Certificate expiry: VMCA leaf certs → machine SSL → solution user certs → 90-day renewal trigger    │
│                                                                                                       │
│   Escalation path when a fault cannot be resolved from operational checks                             │
│   Step 1: Review the vCenter event timeline for the affected object (VM, host, datastore)             │
│   Step 2: Run the PowerCLI health check script and record output                                      │
│   Step 3: Collect the vm-support bundle from the affected ESXi host                                   │
│   Step 4: Raise a VMware support case via the Broadcom GSS portal with the bundle attached            │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Runbook      = documented step-by-step procedure for a specific repeatable operational task         │
│   DRS drain    = vSphere migrates all running VMs off a host before it enters maintenance mode        │
│   vm-support   = ESXi support bundle; collect with: vm-support -w /tmp/support; retrieve via SCP      │
│   GSS          = Global Support Services; Broadcom support portal for raising VMware cases            │
│   Change window = scheduled maintenance window; major platform changes require a CAB ticket           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-2">

<a class="kb-card" href="morning-health-check/">
  <strong>Morning Health Check</strong>
  <span>Start-of-shift check sequence: vCenter → ESXi → vSAN → NSX → Aria Ops. Under 20 minutes. Includes sign-off checklist.</span>
</a>

<a class="kb-card" href="runbooks/">
  <strong>Runbooks</strong>
  <span>Step-by-step operational runbooks — VM snapshots, host maintenance mode, vCenter backup, certificate rotation, and vSAN capacity review.</span>
</a>

</div>
