# Backup

<div class="kb-summary">
Backup platform covering enterprise backup products (Veeam, Commvault, NetBackup, Dell Cyber Recovery), backup validation procedures, and recovery testing. Backup protects data and workloads; Disaster Recovery orchestrates failover — these are distinct disciplines.
</div>

```text
┌──────────────────────────────────────────────── Backup Platform ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Enterprise Backup Platform                                       │   │
│   │         Backup products protect data at rest and enable point-in-time recovery                │   │
│   │         Backup ≠ DR: backup restores data; DR restores service availability                   │   │
│   │         RPO drives backup frequency; RTO drives recovery infrastructure sizing                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Backup Products                    │  │           Data Protection                   │   │
│   │   Veeam       — VM + physical backup         │  │   Backup Validation  — verify restorability │   │
│   │   Commvault   — enterprise data platform     │  │   Recovery Testing   — DR drill procedures  │   │
│   │   NetBackup   — enterprise tape + disk       │  │   Retention Policy   — lifecycle governance │   │
│   │   Cyber Recovery — ransomware vault (Dell)   │  │   Classification     — data tier alignment  │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   Physical Infrastructure (the hardware everything above runs on):                                    │
│   Backup servers · proxy servers · dedup appliances · tape libraries · object storage targets         │
│                                                                                                       │
│   Key terms:                                                                                          │
│                                                                                                       │
│   RPO            = Recovery Point Objective — maximum acceptable data loss window                     │
│   RTO            = Recovery Time Objective — maximum acceptable recovery duration                     │
│   Dedup          = deduplication — eliminates redundant data blocks across backup jobs                │
│   Proxy          = Veeam/Commvault component that moves data from source to repository                │
│   Repository     = backup storage target — disk, dedup appliance, object store, or tape               │
│   Immutability   = backup data that cannot be modified or deleted for a defined period                │
│   Cyber vault    = air-gapped isolated copy with integrity verification (ransomware recovery)         │
│   Synthetic full = full backup assembled from incremental chains — no re-read of source               │
│   Instant VM     = boot a VM directly from backup repository without restoring to production          │
│   CBT            = Changed Block Tracking — VMware mechanism for incremental backup efficiency        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="veeam/">
  <strong>Veeam</strong>
  <span>VM and physical backup, replication, instant recovery, and Veeam ONE monitoring.</span>
</a>

<a class="kb-card" href="commvault/">
  <strong>Commvault</strong>
  <span>Enterprise data platform — backup, archive, compliance, and cloud integration.</span>
</a>

<a class="kb-card" href="netbackup/">
  <strong>NetBackup</strong>
  <span>Enterprise backup for VMs, physical servers, databases, and tape infrastructure.</span>
</a>

<a class="kb-card" href="dell-cyber-recovery/">
  <strong>Dell Cyber Recovery</strong>
  <span>Ransomware air-gap vault — PowerProtect + CyberSense integrity verification.</span>
</a>

<a class="kb-card" href="backup-validation/">
  <strong>Backup Validation</strong>
  <span>Verifying backup integrity — automated verification, test restores, and scheduling.</span>
</a>

<a class="kb-card" href="recovery-testing/">
  <strong>Recovery Testing</strong>
  <span>DR drill procedures, test scenarios, regulatory requirements, and lessons learned.</span>
</a>

</div>
