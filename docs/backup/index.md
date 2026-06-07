# Backup

<div class="kb-summary">
Enterprise backup product knowledge base — Veeam, Commvault, NetBackup, and Dell Cyber Recovery vault. Backup protects data and enables point-in-time recovery; disaster recovery procedures and runbooks are in the DR section.
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
│                                             ▼                                                         │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Backup Products                                                   │   │
│   │          Veeam       — VM + physical backup, instant recovery, Veeam ONE monitoring           │   │
│   │          Commvault   — enterprise data platform; backup, archive, compliance, and cloud       │   │
│   │          NetBackup   — enterprise backup for VMs, servers, databases, and tape                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
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


</div>
