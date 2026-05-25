# Runbooks

```text
┌──────────────────────────────────────────────────────────────────────┐
│                     Runbook Execution Pattern                        │
│                                                                      │
│  Ticket / alert raised                                               │
│        │                                                             │
│  ┌─────▼──────────────────────────────────────────────────────────┐  │
│  │  Identify runbook                                              │  │
│  │  Account unlock · Cert renewal · Disk cleanup · Reboot        │   │
│  │  Service restart · Volume expand · VM snapshot                │   │
│  └─────┬──────────────────────────────────────────────────────────┘  │
│        │                                                             │
│  ┌─────▼──────────────────────────────────────────────────────────┐  │
│  │  Pre-checks                                                    │  │
│  │  Backup current state · Notify stakeholders · Verify access   │   │
│  └─────┬──────────────────────────────────────────────────────────┘  │
│        │                                                             │
│  ┌─────▼──────────────────────────────────────────────────────────┐  │
│  │  Execute steps (ordered, with checkpoints)                     │  │
│  └─────┬──────────────────────────────────────────────────────────┘  │
│        │                                                             │
│  ┌─────▼────────────────────┐    ┌──────────────────────────────┐    │
│  │  Validate outcome        │    │  Rollback if failed          │    │
│  │  Service health checks   │    │  Restore from snapshot/bkp   │    │
│  └─────┬────────────────────┘    └──────────────────────────────┘    │
│        │                                                             │
│  ┌─────▼──────────────────────────────────────────────────────────┐  │
│  │  Document outcome in ticket · Close change record             │   │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

Common operational procedures for infrastructure tasks.

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="account-unlock/"><strong>Account Unlock</strong><span>Unlocking locked AD accounts, resetting passwords, and checking lockout source.</span></a>
<a class="kb-card" href="certificate-renewal/"><strong>Certificate Renewal</strong><span>Renewing SSL/TLS certificates for infrastructure components, web services, and appliances.</span></a>
<a class="kb-card" href="disk-space-cleanup/"><strong>Disk Space Cleanup</strong><span>Identifying and clearing disk space on Windows and Linux — logs, temp files, and snapshots.</span></a>
<a class="kb-card" href="server-reboot/"><strong>Server Reboot</strong><span>Safe server reboot procedure — pre-checks, graceful shutdown, and post-reboot validation.</span></a>
<a class="kb-card" href="service-restart/"><strong>Service Restart</strong><span>Restarting services on Windows and Linux — safe order, dependency checks, and validation.</span></a>
<a class="kb-card" href="storage-volume-expansion/"><strong>Storage Volume Expansion</strong><span>Expanding LUNs, file systems, and logical volumes across block and file storage platforms.</span></a>
<a class="kb-card" href="vm-snapshot/"><strong>VM Snapshot</strong><span>Creating, managing, and deleting VM snapshots — best practices and cleanup procedures.</span></a>
</div>
