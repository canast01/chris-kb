---
tags:
  - operations
  - terraform
---
# Terraform — Backup & Restore

```bash
# Local state — copy with timestamp
cp terraform.tfstate "terraform.tfstate.bak-$(date +%Y%m%d-%H%M%S)"

# Remote state (S3) — copy to versioned archive bucket
aws s3 cp s3://my-tf-state/project/terraform.tfstate \
    s3://my-tf-state-backup/project/terraform.tfstate.$(date +%Y%m%d-%H%M%S)

# Pull remote state locally for inspection
terraform state pull > terraform.tfstate.local-$(date +%Y%m%d)
```
```text
┌──────────────────────────────────── Terraform — Backup & Restore ─────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     TF backup: git repo for .tf; S3 versioning for state file; .terraform.lock.hcl in git     │   │
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
│   │    State corruption = most common: concurrent apply or force-unlock; check integrity first    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
