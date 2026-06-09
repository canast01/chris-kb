# VMware Runbooks

<div class="kb-summary">
Step-by-step operational runbooks for vSphere platform tasks.
</div>

```text
┌──────────────────────────── VMware Platform — Operational Runbooks ─────────────────────────────────────┐
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
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="vm-snapshot/">
  <strong>VM Snapshot Runbook</strong>
  <span>Procedure for creating, managing, and removing VM snapshots — including pre/post-change snapshot workflow.</span>
</a>

</div>
