# Dell Data Domain

<div class="kb-summary">
Purpose-built backup appliance — inline global deduplication, DDBoost, MTree replication, and cloud tier integration for long-term backup retention and data protection target workloads.
</div>

```
┌───────────────────────────────── Dell Data Domain (PowerProtect DD) ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Data Domain: purpose-built backup deduplication appliance; up to 65:1 dedup ratio       │   │
│   │     DD Boost protocol: backup software integrates directly with DD; distributes dedup work    │   │
│   │      Protocols: DD Boost, NFS, CIFS/SMB, VTL (virtual tape), iSCSI; OST for media servers     │   │
│   │      Cloud tier: replicate MTree data to AWS S3, Azure Blob, or DD Virtual Edition for DR     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Backup app writes via DD Boost → deduplication engine → local MTree → cloud tier replication       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Dedup Engine        │  │        Data Services        │  │          Protection         │   │
│   │         Inline dedup        │  │           DD Boost          │  │         Replication         │   │
│   │         Compression         │  │          NFS / CIFS         │  │          Cloud tier         │   │
│   │        Segment store        │  │             VTL             │  │          WORM lock          │   │
│   │          65:1 ratio         │  │            iSCSI            │  │        Retention lock       │   │
│   │       Garbage collect       │  │         OST protocol        │  │          Encryption         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Integrates with NetBackup, Commvault, Veeam, Avamar, and other backup software via DD Boost        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Protocol     │     Location     │      Notes       │   │
│   │    Backup app    │ NetBackup/Veeam  │    DD Boost/OST   │   Media server   │Distributes dedup │   │
│   │   DD appliance   │ PowerProtect DD  │   All protocols   │   On-premises    │  MTree storage   │   │
│   │    Cloud tier    │  DD cloud ext.   │      HTTPS/S3     │    AWS/Azure     │  Long-term ret.  │   │
│   │    Management    │   DDMC / DD OS   │       HTTPS       │   On-premises    │ CloudIQ optional │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: 1U-6U appliance with NL-SAS/SSD tiers; cloud tier extends via WAN to S3 or Azure         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DD Boost       = Dell protocol enabling backup app to participate in dedup; reduces network load   │
│    MTree          = Logical namespace on DD; each backup job or app typically maps to an MTree        │
│    Deduplication  = Identifying and storing only unique data segments; eliminates repeated patterns   │
│    Dedup ratio    = Logical data stored divided by physical space used; 65:1 is theoretical maximum   │
│    Segment store  = DD internal on-disk format; each unique data segment stored once, indexed         │
│    Garbage collect = DD process reclaiming space from deleted or expired backup data                  │
│    VTL            = Virtual Tape Library; DD emulates tape drives for legacy backup software          │
│    OST            = OpenStorage Technology; Veritas API for deep DD Boost integration in NetBackup    │
│    Cloud tier     = DD feature extending MTree data to object storage (S3/Azure) for cold backup      │
│    WORM           = Write Once Read Many; DD Retention Lock Compliance for immutable backup copies    │
│    Replication    = DD-to-DD data replication for DR; directory-based or MTree-based scheduling       │
│    DDMC           = Data Domain Management Center; centralized management for multiple DD appliances  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
