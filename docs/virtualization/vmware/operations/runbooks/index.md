---
tags:
  - operations
  - vmware
---
# VMware Runbooks

<div class="kb-summary">
Step-by-step operational runbooks for vSphere platform tasks.
</div>

```text
┌─────────────────────────────── VMware Platform — Operational Runbooks ────────────────────────────────┐
│                                                                                                       │
│   Runbooks are step-by-step procedures for repeatable platform operations                             │
│   Each runbook covers: prerequisites, steps, verification, and rollback procedure                     │
│   All steps tested against vSphere 8.x and VCF 5.x; PowerCLI or vCenter UI paths provided             │
│                                                                                                       │
│   VM Snapshot Runbook                                                                                 │
│   Pre-change: create snapshot → record snapshot name and VM state                                     │
│   Post-change: verify application health → remove snapshot within 72 hours                            │
│   Rollback: revert to snapshot if application fails post-change; then delete snapshot                 │
│   Caution: never leave snapshots longer than 72 h — delta disk growth degrades storage performance    │
│                                                                                                       │
│   General runbook structure                                                                           │
│   Prerequisites: access level required, maintenance window, backups confirmed                         │
│   Pre-checks: gather current state (health, alarms, replication status)                               │
│   Steps: numbered actions with expected output at each step                                           │
│   Verification: confirm desired end state before closing the change                                   │
│   Rollback: defined revert procedure for each runbook (not all are reversible)                        │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Runbook    = documented operational procedure; used to ensure repeatability and auditability        │
│   Pre-check  = state capture before making any change; used as the rollback baseline                  │
│   Change window = scheduled maintenance period; runbooks must be executed inside the window           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="vm-snapshot/">
  <strong>VM Snapshot Runbook</strong>
  <span>Creating, managing, and removing VM snapshots — pre/post-change workflow and delta disk risks.</span>
</a>

<a class="kb-card" href="esxi-host-maintenance/">
  <strong>ESXi Host Maintenance Mode</strong>
  <span>Entering and exiting maintenance mode — DRS drain, capacity pre-checks, and vLCM remediation path.</span>
</a>

<a class="kb-card" href="vcenter-backup/">
  <strong>vCenter File-Based Backup</strong>
  <span>Ad-hoc and scheduled VCSA backup to SFTP — backup token management and restore summary.</span>
</a>

<a class="kb-card" href="certificate-rotation/">
  <strong>Certificate Rotation</strong>
  <span>Rotating Machine SSL, VMCA root, and custom CA certificates — pre-checks, options A/B/C, and verification.</span>
</a>

<a class="kb-card" href="vsan-capacity-check/">
  <strong>vSAN Capacity Review</strong>
  <span>Weekly capacity audit — usage thresholds, growth rate calculation, snapshot cleanup, and expansion options.</span>
</a>

</div>
