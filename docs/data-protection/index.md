# Data Protection

```
┌──────────────────────────────────────────────────────────────────────┐
│                   Data Protection Overview                           │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │    Backup    │  │ Replication  │  │   Snapshot   │              │
│  │  Veeam       │  │ SRDF/A       │  │  Array-level │              │
│  │  NetBackup   │  │ SnapMirror   │  │  VM snapshot │              │
│  │  Commvault   │  │ vSphere Rep  │  │  TimeFinder  │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                  │                      │
│  ┌──────▼─────────────────▼─────────────────▼────────────────────┐  │
│  │              Protected Data                                   │  │
│  │   VMs · Databases · File shares · Object storage              │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  Retention policy  ·  Immutable (WORM)  ·  3-2-1 rule     │     │
│  │  Key mgmt  ·  Encryption at rest & in transit             │     │
│  └────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="backup-validation/"><strong>Backup Validation</strong><span>Verifying backup jobs are complete, restores are testable, and retention policies are met.</span></a>
<a class="kb-card" href="data-classification/"><strong>Data Classification</strong><span>Data classification tiers, labelling requirements, and handling rules per classification level.</span></a>
<a class="kb-card" href="data-encryption/"><strong>Data Encryption</strong><span>Encryption at rest and in transit — standards, key management, and compliance requirements.</span></a>
<a class="kb-card" href="data-governance/"><strong>Data Governance</strong><span>Data ownership, access controls, audit requirements, and regulatory alignment.</span></a>
<a class="kb-card" href="data-retention-policy/"><strong>Data Retention Policy</strong><span>Retention schedules by data type, legal hold procedures, and deletion verification.</span></a>
<a class="kb-card" href="key-management/"><strong>Key Management</strong><span>KMS architecture, key rotation procedures, and HSM integration references.</span></a>
<a class="kb-card" href="recovery-testing/"><strong>Recovery Testing</strong><span>Restore test procedures, DR test schedules, and test result documentation.</span></a>
</div>
