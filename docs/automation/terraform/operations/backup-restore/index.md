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

## Restore State from Backup

```bash
# List available state versions in S3
aws s3api list-object-versions \
    --bucket my-tf-state \
    --prefix project/terraform.tfstate \
    --query 'Versions[*].[VersionId,LastModified]' \
    --output table

# Restore a specific version
VERSION_ID="abc123..."
aws s3api get-object \
    --bucket my-tf-state \
    --key project/terraform.tfstate \
    --version-id "$VERSION_ID" \
    terraform.tfstate.restored

# Push restored state
terraform state push terraform.tfstate.restored
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
