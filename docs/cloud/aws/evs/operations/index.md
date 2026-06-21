---
tags:
  - aws
  - operations
---
# Amazon EVS — Operations

<!-- diagram:evs-operations -->

<div class="kb-summary">
EVS day-2 operations: cluster health, host management, vSAN capacity, lifecycle upgrades, backup procedures, and runbook scripts for routine administration.

*Applies to: Amazon EVS*
</div>
![Amazon EVS — Operations](../../../../assets/cloud-aws-evs-operations-index.svg)


```text
┌──────────────────────────────────────── Amazon EVS Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      EVS Day-2 Operations                                     │   │
│   │          Six sub-sections: CLI, Health Checks, Procedures, Upgrades, Backup, Scripts          │   │
│   │         Health baseline: cluster CREATED + all hosts CREATED + vSAN green + NSX stable        │   │
│   │        Host add/remove via AWS EVS API after vSAN evacuation completes (BytesToSync=0)        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                 ▼                               ▼                                 ▼                   │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌───────────────────────────────┐   │
│   │        Daily Health        │  │      Host Management       │  │         VCF Lifecycle         │   │
│   │      AWS cluster state     │  │        Add host (API)      │  │      SDDC Manager upgrades    │   │
│   │      vSAN health checks    │  │    Remove host (evacuate)  │  │       VCF upgrade sequence    │   │
│   │    NSX-T component status  │  │        HCX migration       │  │       HCX version upgrade     │   │
│   └────────────────────────────┘  └────────────────────────────┘  └───────────────────────────────┘   │
│                                                                                                       │
```
<div class="kb-grid">
  <a class="kb-card" href="cli-reference/">
    <span class="kb-card-title">CLI Reference</span>
    <span class="kb-card-desc">AWS CLI and PowerCLI commands for EVS cluster, host, and vSAN management</span>
  </a>
  <a class="kb-card" href="health-checks/">
    <span class="kb-card-title">Health Checks</span>
    <span class="kb-card-desc">Run This Routine: cluster, vSAN, NSX-T, HCX, and host health verification</span>
  </a>
  <a class="kb-card" href="procedures/">
    <span class="kb-card-title">Procedures</span>
    <span class="kb-card-desc">Add/remove hosts, maintenance mode, vSAN rebalance, NSX policy updates</span>
  </a>
  <a class="kb-card" href="install-upgrade/">
    <span class="kb-card-title">Lifecycle & Upgrades</span>
    <span class="kb-card-desc">VCF upgrades via SDDC Manager, ESXi lifecycle, NSX upgrade sequence</span>
  </a>
  <a class="kb-card" href="backup-restore/">
    <span class="kb-card-title">Backup & Restore</span>
    <span class="kb-card-desc">SDDC Manager config backup, vCenter DB backup, VM backup to S3</span>
  </a>
  <a class="kb-card" href="scripts/">
    <span class="kb-card-title">Scripts</span>
    <span class="kb-card-desc">health-check.sh, host-add.sh, vsan-rebalance.sh, hcx-status.sh</span>
  </a>
</div>

