# AWS — Backup & Restore


<div class="kb-summary">
Backup & Restore reference covering EBS Snapshot — Manual, Restore EC2 from EBS Snapshot, RDS Restore, S3 — Restore a Deleted Object (Versioning), AWS Backup — Restore Job and 1 more sections.
</div>

```text
AWS Backup & Restore Flow
──────────────────────────────────────────────────────────────

  Resources (EC2/RDS/EFS/S3/DynamoDB)
          │ AWS Backup plan (daily cron)
          ▼
  ┌──────────────────────────────────────────────────────┐
  │  AWS Backup Vault                                    │
  │  Recovery Points (encrypted snapshots)               │
  └───────────────────────┬──────────────────────────────┘
                          │
            ┌─────────────┼──────────────────┐
            ▼             ▼                  ▼
  ┌──────────────┐ ┌────────────────┐ ┌────────────────┐
  │  EC2 Restore │ │  RDS Restore   │ │  S3 Restore    │
  │              │ │                │ │                │
  │  Snapshot →  │ │  Snapshot →    │ │  Versioning:   │
  │  new volume  │ │  new instance  │ │  delete marker │
  │  attach to   │ │  OR PITR to    │ │  removal       │
  │  instance    │ │  timestamp     │ │                │
  └──────────────┘ └────────────────┘ └────────────────┘
```
```text
┌──────────────────────────── AWS Operations — Backup & Restore Procedures ─────────────────────────────┐
│                                                                                                       │
│  Operational backup and restore procedures covering EC2, RDS, EBS, and S3 workflows.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Backup Procedures               │  │              Restore Procedures             │   │
│   │     EBS: create snapshot via console/CLI     │  │     EBS: restore snapshot to new volume     │   │
│   │      RDS: automated + manual snapshots       │  │        RDS: restore to point-in-time        │   │
│   │     EC2 AMI: image from running instance     │  │             EC2: launch from AMI            │   │
│   │     S3: versioning + replication policy      │  │         S3: restore previous version        │   │
│   │      AWS Backup: vault + plan schedule       │  │        Backup: restore job from vault       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Verify restore procedures regularly; test AMI launches and RDS PITR in non-prod accounts.            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Operational Checks              │  │                  Automation                 │   │
│   │      Verify snapshot completion status       │  │        AWS Backup plan: cron schedule       │   │
│   │      Check cross-region copy completion      │  │       Lambda: custom snapshot scripts       │   │
│   │     Validate retention policy compliance     │  │       EventBridge: trigger on schedule      │   │
│   │      Test restore RTO: measure duration      │  │       SNS: notify on job success/fail       │   │
│   │       Review cost of snapshot storage        │  │       Lifecycle: auto-expire old snaps      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS S3 snapshot storage · Cross-region replication infrastructure · Regional endpoints               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  EBS snapshot    = Point-in-time copy of an EBS volume stored durably in S3                           │
│  AMI             = Amazon Machine Image; snapshot + metadata needed to launch EC2                     │
│  RDS snapshot    = Database-level backup; automated (daily) or manual on demand                       │
│  PITR            = Point-in-time recovery; RDS/DynamoDB restore to any second in window               │
│  AWS Backup vault= Encrypted container for backup recovery points with access policy                  │
│  Recovery point  = A backup copy stored in a vault; has expiry and lifecycle rules                    │
│  Cross-region copy= Backup rule that replicates snapshots to another region                           │
│  RTO             = Recovery time objective; target time to restore from backup                        │
│  RPO             = Recovery point objective; maximum acceptable data loss window                      │
│  Restore job     = AWS Backup task that re-creates a resource from a recovery point                   │
│  Snapshot lifecycle= Policy that transitions or deletes snapshots after N days                        │
│  Incremental snapshot= After first full, EBS snapshots store only changed blocks                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Restore EC2 from EBS Snapshot

```bash
# Step 1: Create volume from snapshot
aws ec2 create-volume \
  --snapshot-id snap-0abc123def456789 \
  --availability-zone eu-west-1a \
  --volume-type gp3 \
  --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=restored-vol}]'

# Step 2: Stop target EC2 instance
aws ec2 stop-instances --instance-ids i-0abc123def456789

# Step 3: Detach existing root volume
aws ec2 detach-volume --volume-id vol-<existing> --instance-id i-0abc123def456789

# Step 4: Attach restored volume
aws ec2 attach-volume \
  --volume-id vol-<new> \
  --instance-id i-0abc123def456789 \
  --device /dev/xvda

# Step 5: Start instance
aws ec2 start-instances --instance-ids i-0abc123def456789
```

---

## RDS Restore

```bash
# List available automated snapshots for an RDS instance
aws rds describe-db-snapshots \
  --db-instance-identifier prod-mysql \
  --snapshot-type automated \
  --query 'DBSnapshots[*].[DBSnapshotIdentifier,SnapshotCreateTime,Status]' \
  --output table

# Restore RDS from snapshot to a new instance
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier prod-mysql-restored \
  --db-snapshot-identifier rds:prod-mysql-2026-05-15-02-30 \
  --db-instance-class db.r6g.large \
  --multi-az \
  --no-publicly-accessible

# Point-in-time restore (PITR)
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier prod-mysql \
  --target-db-instance-identifier prod-mysql-pitr \
  --restore-time 2026-05-15T14:30:00Z
```

---

## S3 — Restore a Deleted Object (Versioning)

```bash
# List versions of a deleted object
aws s3api list-object-versions \
  --bucket my-prod-bucket \
  --prefix path/to/object.txt \
  --query '{Versions:Versions[*].[VersionId,LastModified,IsLatest],DeleteMarkers:DeleteMarkers[*].[VersionId,LastModified]}'

# Remove delete marker to restore object
aws s3api delete-object \
  --bucket my-prod-bucket \
  --key path/to/object.txt \
  --version-id <delete-marker-version-id>

# Copy specific version to restore
aws s3api copy-object \
  --bucket my-prod-bucket \
  --copy-source "my-prod-bucket/path/to/object.txt?versionId=<version-id>" \
  --key path/to/object.txt
```

---

## AWS Backup — Restore Job

```bash
# List recovery points for a resource
aws backup list-recovery-points-by-resource \
  --resource-arn arn:aws:ec2:eu-west-1:<account>:volume/vol-0abc123def456789 \
  --query 'RecoveryPoints[*].[RecoveryPointArn,CreationDate,Status]' \
  --output table

# Start restore job
aws backup start-restore-job \
  --recovery-point-arn arn:aws:ec2:eu-west-1:<account>:snapshot/snap-0abc123def456789 \
  --iam-role-arn arn:aws:iam::<account>:role/AWSBackupDefaultServiceRole \
  --resource-type EBS \
  --metadata '{"availabilityZone":"eu-west-1a","volumeType":"gp3"}'

# Check restore job status
aws backup describe-restore-job --restore-job-id <job-id>
```

---

## Verify Backup Coverage

```bash
# List all resources NOT protected by AWS Backup (requires Config)
aws backup list-protected-resources \
  --query 'Results[*].[ResourceType,ResourceArn]' \
  --output table

# Check backup job status for last 24h
aws backup list-backup-jobs \
  --by-state FAILED \
  --by-created-after $(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d 'yesterday' +%Y-%m-%dT%H:%M:%SZ) \
  --query 'BackupJobs[*].[ResourceArn,ResourceType,State,StatusMessage]' \
  --output table
```
