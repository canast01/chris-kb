# AWS Backup

<div class="kb-summary">
AWS Backup provides centralised backup management across EC2, EBS, RDS, DynamoDB, EFS, FSx, and S3, with Backup Plans defining schedules and Vault Lock enforcing immutable retention. Coverage includes backup job monitoring, restore testing, and compliance reporting.
</div>

```
┌─────────────┐    ┌──────────────────────────────────────────────┐
│  Resources  │    │              Backup Plan                      │
│  ┌────────┐ │    │  ┌──────────────┐   ┌────────────────────┐  │
│  │ EC2/EBS│ │───►│  │ Rule: Daily  │   │ Rule: Weekly       │  │
│  │ RDS    │ │    │  │ 02:00 UTC    │   │ Sun 03:00 UTC      │  │
│  │ EFS    │ │    │  │ Retain 30d   │   │ Retain 90d         │  │
│  │ S3     │ │    │  └──────┬───────┘   └─────────┬──────────┘  │
│  │DynamoDB│ │    │         │                     │              │
│  └────────┘ │    └─────────┼─────────────────────┼─────────────┘
└─────────────┘              │                     │
                             ▼                     ▼
              ┌──────────────────────┐   ┌─────────────────────┐
              │    Backup Vault      │   │  DR Vault (x-region)│
              │  ┌────────────────┐  │   │  ┌───────────────┐  │
              │  │ KMS Encrypted  │  │   │  │ Cross-region  │  │
              │  │ Vault Lock     │  │   │  │ copy enabled  │  │
              │  │ Access Policy  │  │   │  └───────────────┘  │
              │  └────────┬───────┘  │   └─────────────────────┘
              └───────────┼──────────┘
                          ▼
              ┌──────────────────────┐
              │   Recovery Points    │
              │  (Snapshots/Backups) │◄─── Restore Job ───► Target
              └──────────────────────┘
```

![AWS Backup Architecture](../../../assets/aws-backup-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="aws-backup/">
  <strong>AWS Backup</strong>
  <span>Backup service overview, configuration, and operations.</span>
</a>

<a class="kb-card" href="backup-plans/">
  <strong>Backup Plans</strong>
  <span>Backup plan creation, rules, schedules, and lifecycle policies.</span>
</a>

<a class="kb-card" href="backup-vaults/">
  <strong>Backup Vaults</strong>
  <span>Vault management, access policies, and encryption.</span>
</a>

<a class="kb-card" href="backup-jobs/">
  <strong>Backup Jobs</strong>
  <span>Job monitoring, troubleshooting, and status checks.</span>
</a>

<a class="kb-card" href="restore-testing/">
  <strong>Restore Testing</strong>
  <span>Restore validation, testing procedures, and recovery checks.</span>
</a>

<a class="kb-card" href="backup-compliance/">
  <strong>Backup Compliance</strong>
  <span>Compliance frameworks, reporting, and audit readiness.</span>
</a>

</div>
