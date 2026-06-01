# Superna Eyeglass — Backup & Restore


<div class="kb-summary">
Eyeglass configuration backup preserves replication policies, SyncIQ jobs, share/export configurations, access zone mappings, and SmartConnect zone settings. Without a current backup, DR failover configuration must be manually re-created.
</div>

---

## What Eyeglass Backs Up

| Category | Backed Up | Notes |
|---|---|---|
| Replication policies (SyncIQ) | Yes | Policy rules, schedules, paths |
| Share/export configuration | Yes | SMB shares, NFS exports, ACLs |
| Access zone mappings | Yes | Source → target zone mapping |
| SmartConnect zone configuration | Yes | DNS zone, subnet, pool mapping |
| DFS namespace configuration | Yes | DFS targets and referrals |
| Quota configuration | Yes | Quota policies and alerts |
| Eyeglass appliance config | Yes | Clusters, credentials, settings |
| PowerScale data | No | Data is replicated by SyncIQ, not Eyeglass |

---

## Backup Architecture

```mermaid
flowchart LR
    subgraph "Eyeglass Appliance"
        EG[Eyeglass Engine]
        CFG[Config Store]
        SCHED[Backup Scheduler]
    end
    subgraph "Backup Targets"
        LOCAL[Local Disk\n/home/admin/backups]
        NFS[NFS Share\nNAS Backup Target]
        SFTP[SFTP Server]
    end
    SCHED --> EG
    EG --> CFG
    EG --> LOCAL
    EG --> NFS
    EG --> SFTP
```
┌───────────────────────────────── Superna Eyeglass — Backup & Restore ─────────────────────────────────┐
│                                                                                                       │
│    Backup flow: quiesce source → snapshot/copy → transfer → write to target → catalog                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Backup (Protection)              │  │              Restore (Recovery)             │   │
│   │               igls quota list                │  │               igls dr runbook               │   │
│   │              Quiesce source I/O              │  │            Select recovery point            │   │
│   │             Take snapshot / CBT              │  │           Mount or copy to target           │   │
│   │           Transfer changed blocks            │  │              Validate integrity             │   │
│   │             Commit to repository             │  │             Restart application             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Key Superna Eyeglass Commands                                 │   │
│   │                                Backup trigger  : igls quota list                              │   │
│   │                                List points     : igls dr runbook                              │   │
│   │                                Health status   : igls sync status                             │   │
│   │                              Retention mgmt  : igls failover start                            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link   │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection            │
│  RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats       │
│  SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies         │
│  DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS        │
│  Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster              │
│  Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product       │
│  Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits            │
│  Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site            │
│  Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team                  │
│  Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha       │
│  Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation      │
│  igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations                         │
│  SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation         │
│  Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Restore to New/Replacement Appliance

```bash
# 1. Deploy new Eyeglass OVA (same version as backup)
# 2. Complete initial setup wizard (network, hostname)

# 3. Copy backup file to new appliance
scp eyeglass-backup-<date>.tar.gz admin@<new-eyeglass-ip>:/home/admin/

# 4. SSH to new appliance
ssh admin@<new-eyeglass-ip>

# 5. Import and restore the backup
igls backup import --file /home/admin/eyeglass-backup-<date>.tar.gz
igls backup restore --id <imported-backup-id>

# 6. Verify cluster connections
igls clusters list

# 7. Re-enter cluster credentials (passwords are not stored in backup)
igls clusters update-credentials --cluster <cluster-name>
```

**Note:** Cluster passwords and API tokens are not included in backups for security. After restore, re-enter credentials for each managed PowerScale cluster.

---

## Post-Restore Validation

```bash
# Check Eyeglass service health
igls status

# Verify all clusters are connected
igls clusters list

# Verify replication jobs are visible
igls jobs list

# Check share/export configuration loaded correctly
igls shares list
igls exports list

# Run a configuration sync to verify policies are intact
igls sync run --cluster <cluster-name>
```

**GUI validation:**

- [ ] All clusters show as Connected (green)
- [ ] Replication policies visible under DR → Replication
- [ ] Share configurations visible under Configuration → Shares
- [ ] SmartConnect zones mapped correctly
- [ ] Scheduled jobs appear in job monitor

---

## Policy Backup Export (Manual)

For additional protection, export individual policy configurations:

```bash
# Export all SyncIQ policy mappings
igls dr export --format json > eyeglass-policy-export-$(date +%Y%m%d).json

# Export DFS configuration
igls dfs export > eyeglass-dfs-export-$(date +%Y%m%d).json

# Store exports off-appliance
scp eyeglass-policy-export-*.json admin@nas:/backups/eyeglass/
```

---

## Backup Verification Testing

Test backup integrity quarterly:

1. Identify a non-production or DR Eyeglass appliance
2. Restore the latest production backup
3. Verify cluster connectivity (with read-only credentials)
4. Confirm all replication policies, shares, and access zone mappings load correctly
5. Document test result in ITSM

---

## Related Pages

- [Superna Eyeglass — Architecture](../../architecture/how-it-works/index.md)
- [Superna Eyeglass — Health Checks](../health-checks/index.md)
- [PowerScale — Backup & Restore](../../../../storage/dell/powerscale/operations/backup-restore/index.md)
