# Terraform — Backup & Restore

## State File Backup

The Terraform state file is the source of truth for managed infrastructure. Back it up before any destructive operation.

```bash
# Local state — copy with timestamp
cp terraform.tfstate "terraform.tfstate.bak-$(date +%Y%m%d-%H%M%S)"

# Remote state (S3) — copy to versioned archive bucket
aws s3 cp s3://my-tf-state/project/terraform.tfstate \
    s3://my-tf-state-backup/project/terraform.tfstate.$(date +%Y%m%d-%H%M%S)

# Pull remote state locally for inspection
terraform state pull > terraform.tfstate.local-$(date +%Y%m%d)
```
┌──────────────────────────────────── Terraform — Backup & Restore ─────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │Terraform backup: git repo for .tf code; S3 versioning for state file; .terraform.lock.hcl in g│   │
│   │    Enable S3 versioning on state bucket; DynamoDB table for lock; enable S3 access logging    │   │
│   │        State restore: download previous version from S3, push with terraform state push       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               What to Back Up                │  │                Restore Steps                │   │
│   │          Git repo (.tf + lock file)          │  │       1. Identify state version in S3       │   │
│   │         S3 bucket (versioned state)          │  │         2. Download previous version        │   │
│   │        DynamoDB table (lock metadata)        │  │      3. terraform state push state.bak      │   │
│   │          .terraform.lock.hcl in git          │  │          4. terraform plan (verify)         │   │
│   │          tfvars (non-secret values)          │  │        5. Correct any drift manually        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   S3 versioning   = preserves all state file versions; restore from Version ID in S3 console  │   │
│   │   state push       = terraform state push <file>; overwrites remote state; use with caution   │   │
│   │State corruption = most common cause: concurrent apply or force-unlock; check state integrity f│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## State Recovery After Corruption

```bash
# Check state is parseable
terraform show

# If corrupt, restore from backup
terraform state push terraform.tfstate.bak-<timestamp>

# Reconcile drift after restore
terraform plan
terraform apply -target=<drifted-resource>
```

## Checklist Before Destructive Operations

- [ ] Pull current state: `terraform state pull > pre-op-state.tfstate`
- [ ] Tag the backup with ticket/date
- [ ] Confirm S3 versioning is enabled on the state bucket
- [ ] Confirm DynamoDB state lock table exists
- [ ] Run `terraform plan` and review output before `apply`
