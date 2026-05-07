# Operations

> Part of the [Terraform](../) reference.

---

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Review `terraform plan` output in CI pipeline for any unexpected o | `terraform plan` |  |
| [ ] Confirm remote backend (S3, Azure Blob, or Terraform Cloud) is acc |  |  |
| [ ] Review active workspace | `terraform workspace list` | confirm correct workspace is selected |
| [ ] Check `.terraform.lock.hcl` for expired provider versions or depre | `.terraform.lock.hcl` |  |
| [ ] Review open pull requests that modify Terraform code for pending u |  |  |
| [ ] Check for stale state lock files that may indicate a stuck or aban |  |  |
| [ ] Confirm sensitive variable sources (Vault, SSM Parameter Store, en |  |  |

## Health Check

- [ ] Remote backend is reachable and state file is present and valid
- [ ] State is not locked: no `terraform.tfstate.lock.info` file or backend lock active
- [ ] `terraform validate` passes with no errors
- [ ] `terraform plan` produces expected output — no unintended resource changes
- [ ] All provider plugins are initialized: `.terraform/` directory present
- [ ] Workspace is set to the correct environment: `terraform workspace show`
- [ ] Sensitive variables are resolvable (Vault token valid, SSM accessible)
- [ ] CI pipeline last run passed for the target workspace

```bash
# Validate configuration syntax
terraform validate

# Show current workspace
terraform workspace show

# List all workspaces
terraform workspace list

# Check plan for drift (no changes expected in steady state)
terraform plan -out=tfplan

# Show current state summary
terraform show

# Check if state is locked (S3 backend example)
aws s3api head-object \
  --bucket <state-bucket> \
  --key <path/to/terraform.tfstate>
```

## Change Readiness

- [ ] `terraform plan` output reviewed and all proposed changes are intentional and approved
- [ ] State is not currently locked by another operation
- [ ] Correct workspace is selected for the target environment
- [ ] Sensitive variables (Vault/SSM/env) are accessible and not expired
- [ ] Remote backend is accessible and state file is current
- [ ] State file snapshot or manual backup taken before destructive operations
- [ ] Rollback plan documented (previous state file version identified in backend)
- [ ] CI pipeline passing on the branch to be applied

| Item | Status | Notes |
|---|---|---|
| `terraform plan` reviewed | | Approver name |
| State not locked | | Confirmed / Lock ID if present |
| Correct workspace | | Workspace name |
| State backup | | Backend version ID or manual copy |
| Rollback plan | | Previous state version reference |

## Incident Triage

- [ ] Check if state is locked — identify the lock holder and determine if it is stale
- [ ] Run `terraform plan` to detect drift between state and actual infrastructure
- [ ] Run `terraform show` to inspect the current recorded state for the affected resource
- [ ] Check provider API connectivity (AWS, Azure, GCP CLI auth working)
- [ ] Review recent `terraform apply` logs in CI for the last successful and failed runs
- [ ] If state is corrupt or inconsistent, restore from the last known-good state backup
- [ ] Use `terraform state list` and `terraform state show <resource>` to inspect specific resources

| Question | Answer |
|---|---|
| Is state locked? | `terraform force-unlock <lock-id>` if stale |
| Is there drift? | `terraform plan` output |
| Which resource is affected? | `terraform state show <resource>` |
| Is the provider API reachable? | Test with AWS/Azure/GCP CLI |
| Was a recent apply the cause? | Check CI apply logs |

## Maintenance Window

1. Notify team of the planned Terraform change and scope (workspace, resources affected).
2. Back up the state file — record the current backend version ID or copy state locally.
3. Confirm the state is not locked before starting.
4. Run `terraform plan -out=tfplan` and review the output one final time.
5. Execute `terraform apply tfplan`; monitor output for errors.
6. For destructive operations (`terraform state rm`, `terraform destroy`), pause after each resource and validate.
7. Use `terraform import` for any resources created out-of-band that must be brought under management.
8. Run `terraform plan` after apply to confirm zero changes remain.

## Post-Change Validation

- [ ] `terraform plan` shows zero changes after apply — state is consistent with infrastructure
- [ ] Resources are accessible and healthy in the provider console (AWS/Azure/GCP)
- [ ] State is not locked
- [ ] CI pipeline is passing on the applied branch
- [ ] Remote backend state file updated timestamp reflects the apply
- [ ] No deprecated resource warnings in `terraform validate` output
- [ ] Sensitive variable sources still accessible after the change
- [ ] Rollback state backup retained until the change is confirmed stable
