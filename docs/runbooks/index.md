# Runbooks

Common operational procedures for infrastructure tasks.


```
┌────────────────────────────────── Runbooks — Operational Procedures ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Runbooks: step-by-step operational procedures for common infrastructure tasks         │   │
│   │           Each runbook: pre-checks → steps → validation → rollback path → close-out           │   │
│   │          Run all runbooks under a change ticket; document start/end time and outcome          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Request arrives → identify runbook → raise change ticket → execute → validate → close              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Access / Identity      │  │        Infrastructure       │  │        Storage / VMs        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Account unlock       │  │        Server reboot        │  │       Volume expansion      │   │
│   │     Certificate renewal     │  │       Service restart       │  │         VM snapshot         │   │
│   │        Password reset       │  │         Disk cleanup        │  │       Snapshot delete       │   │
│   │       Group membership      │  │         Log rotation        │  │        LUN expansion        │   │
│   │       SSO token reset       │  │           NTP fix           │  │       Datastore extend      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Runbook     = Documented procedure with explicit steps; reduces error rate in ops tasks            │
│    Pre-checks  = Verify system state is safe to proceed before any change                             │
│    Validation  = Post-execution verification that the task succeeded as expected                      │
│    Rollback    = Steps to undo the change if validation fails; always plan before executing           │
│    Change ticket= Every runbook execution linked to a change request for auditability                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="account-unlock/"><strong>Account Unlock</strong><span>Unlocking locked AD accounts, resetting passwords, and checking lockout source.</span></a>
<a class="kb-card" href="certificate-renewal/"><strong>Certificate Renewal</strong><span>Renewing SSL/TLS certificates for infrastructure components, web services, and appliances.</span></a>
<a class="kb-card" href="disk-space-cleanup/"><strong>Disk Space Cleanup</strong><span>Identifying and clearing disk space on Windows and Linux — logs, temp files, and snapshots.</span></a>
<a class="kb-card" href="server-reboot/"><strong>Server Reboot</strong><span>Safe server reboot procedure — pre-checks, graceful shutdown, and post-reboot validation.</span></a>
<a class="kb-card" href="service-restart/"><strong>Service Restart</strong><span>Restarting services on Windows and Linux — safe order, dependency checks, and validation.</span></a>
<a class="kb-card" href="storage-volume-expansion/"><strong>Storage Volume Expansion</strong><span>Expanding LUNs, file systems, and logical volumes across block and file storage platforms.</span></a>
<a class="kb-card" href="vm-snapshot/"><strong>VM Snapshot</strong><span>Creating, managing, and deleting VM snapshots — best practices and cleanup procedures.</span></a>
</div>
