---
tags:
  - operations
  - terraform
description: "Terraform operational procedures — standard apply workflow, plan and apply strategies, change readiness, workspace management, state operations, incident..."
---
# Terraform — Procedures

<div class="kb-summary">
Terraform operational procedures — standard apply workflow, plan and apply strategies, change readiness, workspace management, state operations, incident triage, and provider credential rotation.

*Applies to: Terraform 1.x*
</div>

## Before you begin

- **Access:** Provider credentials configured (`terraform login` or env vars)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Standard Apply Workflow

```d2
direction: right

writeCode: "Write / Edit\nHCL code" {shape: rectangle}
fmt: "terraform fmt\n-recursive" {shape: rectangle}
validate: "terraform validate" {shape: rectangle}
plan: "terraform plan\n-out=tfplan" {shape: oval}
reviewPlan: "Review Plan\n(human / PR approval" {shape: rectangle}
apply: "terraform apply tfplan" {shape: rectangle}
postPlan: "Post-apply plan\n(zero changes expected" {shape: rectangle}
stateBackup: "State backed up\nin remote backend" {shape: rectangle}

writeCode -> fmt
fmt -> validate
validate -> plan
plan -> reviewPlan
reviewPlan -> apply
reviewPlan -> writeCode
apply -> postPlan
apply -> stateBackup
```

Use `-target` sparingly — it creates drift between the plan and real state if overused.

### Passing Variables at Apply Time

```bash
# Inline variable values
terraform apply -var="instance_type=t3.medium" -var="region=eu-west-1"

# From a var file
terraform apply -var-file="envs/production.tfvars"

# From environment variables (TF_VAR_ prefix)
export TF_VAR_db_password="s3cretpassword"
terraform apply
```


```text title="Expected output"
var.instance_type
  Enter a value: t3.medium

var.region
  Enter a value: eu-west-1

Plan: 3 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_instance.web: Creating...
aws_instance.web: Still creating... [10s elapsed]
aws_instance.web: Creation complete after 15s [id=i-0a7f2c9e4b1d5f3a2]
aws_security_group.allow_ssh: Creation complete after 3s [id=sg-087a3f5c2b9e1d4a6]
aws_ebs_volume.data: Creation complete after 8s [id=vol-0f2e8c1a3b5d7g9h1]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unsupported argument on line 12, in resource "aws_instance" "web": on instance_type = var.instance_type` | Verify the variable name matches your Terraform configuration and check for typos in the resource block. |
    | `Error: variables not allowed` | Remove the `export` statement; use `-var-file` or inline `-var` flags instead, or ensure `TF_VAR_` environment variables are set before running `terraform apply`. |
    | `Error: Failed to read variables file "envs/production.tfvars": no such file or directory` | Verify the file path is correct relative to your working directory and that the file exists with `ls -la envs/production.tfvars`. |
### Apply in CI/CD Pipelines

```yaml
# GitHub Actions example
- name: Terraform Init
  run: terraform init
  working-directory: infra/

- name: Terraform Plan
  id: plan
  run: terraform plan -out=tfplan -no-color
  working-directory: infra/
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

- name: Terraform Apply
  if: github.ref == 'refs/heads/main'
  run: terraform apply -auto-approve tfplan
  working-directory: infra/
```

### Apply Behaviour Reference

| Flag | Effect |
|---|---|
| `-auto-approve` | Skip interactive confirmation |
| `-target=resource` | Limit apply to specific resource(s) |
| `-var="key=val"` | Pass a variable inline |
| `-var-file=file.tfvars` | Load variables from a file |
| `-parallelism=N` | Concurrent resource operations (default 10) |
| `-refresh=false` | Skip state refresh (faster, less safe) |
| `-compact-warnings` | Summarise warnings instead of full detail |

---

## Plan Workflows

### terraform plan Basics

`terraform plan` generates an execution plan showing what changes Terraform will make.

```bash
# Basic plan — shows changes, does not apply
terraform plan

# Plan with variable file
terraform plan -var-file="envs/prod.tfvars"

# Plan with inline variable
terraform plan -var="instance_count=3"

# Plan with exit codes (useful in scripts)
terraform plan -detailed-exitcode
# 0 = no changes, 1 = error, 2 = changes pending
```


```text title="Expected output"
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create
  ~ update in-place
  - destroy

Terraform will perform the following actions:

  # aws_instance.web[0] will be created
  + resource "aws_instance" "web" {
      + ami           = "ami-0c55b159cbfafe1f0"
      + instance_type = "t3.medium"
      + tags          = {
          + "Name" = "web-server-prod-01"
        }
    }

  # aws_security_group.allow_http will be updated in-place
  ~ resource "aws_security_group" "allow_http" {
      ~ ingress {
          + cidr_blocks = ["0.0.0.0/0"]
          + from_port   = 80
        }
    }

Plan: 3 to add, 1 to change, 0 to destroy.

Changes to Outputs:
  + instance_ids = [
      + "i-0a1b2c3d4e5f6g7h8",
    ]
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Variables not allowed` | Remove `-var` flags from `terraform plan` if using a `.tfvars` file, or ensure the variable is declared in your Terraform configuration. |
    | `Error: Failed to read variables file "envs/prod.tfvars": no such file or directory` | Verify the path to your `.tfvars` file is correct relative to your working directory and the file exists. |
### Saving Plan Files

Saving a plan guarantees the apply step executes exactly what was reviewed.

```bash
# Save plan to a binary file
terraform plan -out=tfplan

# View a saved plan in human-readable form
terraform show tfplan

# View as JSON for scripting / audit
terraform show -json tfplan > plan.json

# Extract resource changes from JSON plan
terraform show -json tfplan | \
  jq '.resource_changes[] | {address, actions: .change.actions}'

# Apply from a saved plan (no confirmation prompt)
terraform apply tfplan
```


```text title="Expected output"
Terraform used the following state to generate this plan. Resources and data
sources in your configuration may have changed since the last apply, in that
case you may need to run apply again to reconcile.

No changes. Your infrastructure matches the configuration.

Plan: 0 to add, 0 to change, 0 to destroy.

Saved the plan to: tfplan

─────────────────────────────────────────────────────────────────────────────

Terraform v1.5.2
on linux_amd64

Changes to Outputs:

  ~ outputs = {
      ~ "vpc_id" = "vpc-0a1b2c3d4e5f6g7h8" -> "vpc-0x9y8z7w6v5u4t3s2r"
    }

Plan: 0 to add, 0 to change, 1 to destroy.

{
  "address": "aws_vpc.main",
  "actions": [
    "delete"
  ]
}
{
  "address": "aws_subnet.private",
  "actions": [
    "update"
  ]
}

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: No saved plan file found` | Verify the tfplan file exists in the current directory with `ls -la tfplan`. |
    | `Error: jq: command not found` | Install jq using `apt-get install jq` (Ubuntu/Debian) or `brew install jq` (macOS). |
    | `Error: Error reading plan file: invalid plan format` | Regenerate the plan file by running `terraform plan -out=tfplan` again, as the binary format may be corrupted or from an incompatible Terraform version. |
### Reading Plan Output

Understanding the plan output symbols:

| Symbol | Meaning |
|---|---|
| `+` green | Resource will be created |
| `-` red | Resource will be destroyed |
| `~` yellow | Resource will be updated in-place |
| `-/+` | Resource must be destroyed and recreated |
| `<=` | Data source will be read |

```bash
# Example plan output snippet
  # aws_instance.web will be updated in-place
  ~ resource "aws_instance" "web" {
        id            = "i-0abc12345def"
      ~ instance_type = "t3.small" -> "t3.medium"
        # (all other attributes unchanged)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```


```text title="Expected output"
# aws_instance.web will be updated in-place
  ~ resource "aws_instance" "web" {
        id            = "i-0abc12345def"
      ~ instance_type = "t3.small" -> "t3.medium"
        # (all other attributes unchanged)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: resource does not support in-place update for "instance_type"` | Stop the instance, apply the change, or use `create_before_destroy` lifecycle rule to avoid downtime. |
    | `Error: Invalid or unknown key: instance_type` | Verify the resource type supports the `instance_type` argument and check for typos in the Terraform configuration. |
### Plan Review Checklist

Before approving and applying a plan, verify:

- No unexpected destroys (`-` or `-/+` on production resources)
- Resource counts match expectations
- No sensitive variable values exposed in plain text
- `instance_type`, `ami`, `cidr_block` changes are intentional
- Dependencies between resources are reflected correctly
- Module outputs used by other resources are still valid

```bash
# Highlight destroy operations in a saved JSON plan
terraform show -json tfplan | \
  jq '.resource_changes[] | select(.change.actions[] == "delete") | .address'
```


```text title="Expected output"
"aws_instance.web_server_01"
"aws_security_group.app_tier"
"aws_subnet.private_02"
"aws_route_table_association.main"
"aws_ebs_volume.backup_storage"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `jq: parse error: Invalid numeric literal at line 1 column 10` | Ensure the tfplan file exists and is a valid Terraform plan file; regenerate it with `terraform plan -out=tfplan` if corrupted. |
    | `No such file or directory` | Verify the tfplan file path is correct and the file exists in the current working directory with `ls -la tfplan`. |
    | `error: 2 positional arguments expected, got 1` | Update to `terraform show -json tfplan` (add the explicit filename argument after the `-json` flag). |
### Plan in CI/CD

```yaml
# GitHub Actions — post plan output to PR comment
- name: Terraform Plan
  id: plan
  run: terraform plan -no-color -out=tfplan 2>&1 | tee plan_output.txt
  working-directory: infra/
  continue-on-error: true

- name: Post Plan to PR
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const plan = fs.readFileSync('infra/plan_output.txt', 'utf8');
      const output = `#### Terraform Plan\n\`\`\`\n${plan.slice(0, 60000)}\n\`\`\``;
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: output
      });
```

### Useful Plan Flags

```bash
# Limit plan to specific resources
terraform plan -target=module.database

# Skip refreshing state (faster, use when you know state is current)
terraform plan -refresh=false

# Show only the plan, no preceding status messages
terraform plan -no-color 2>&1 | grep -E '^\s*(#|\+|~|-|Plan)'

# Generate a graph of the plan
terraform graph | dot -Tsvg > plan.svg
```


```text title="Expected output"
module.database.aws_db_instance.primary: Refreshing state... [id=prod-postgres-01]
module.database.aws_db_subnet_group.main: Refreshing state... [id=prod-db-subnet-group]

Terraform will perform the following actions:

  # module.database.aws_db_instance.primary will be updated in-place
  ~ resource "aws_db_instance" "primary" {
      ~ allocated_storage           = 100 -> 150
      ~ backup_retention_period     = 7 -> 14
        id                          = "prod-postgres-01"
        tags                        = {
            "Environment" = "production"
        }
    }

Plan: 1 to add, 1 to change, 0 to destroy.

digraph {
  compound = true
  newrank = true
  subgraph "root" {
    "[root] aws_db_instance.primary" [label = "aws_db_instance.primary", shape = "box"]
    "[root] aws_db_subnet_group.main" [label = "aws_db_subnet_group.main", shape = "box"]
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: resource targeting is not supported for outputs` | Remove `-target` flags that reference output values; use `-target` only for resources and modules. |
    | `Error: Failed to load plugin` | Install Graphviz (`apt-get install graphviz` on Ubuntu or `brew install graphviz` on macOS) before piping to the `dot` command. |
---

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

---

## Maintenance Window

1. Notify team of the planned Terraform change and scope (workspace, resources affected).
2. Back up the state file — record the current backend version ID or copy state locally.
3. Confirm the state is not locked before starting.
4. Run `terraform plan -out=tfplan` and review the output one final time.
5. Execute `terraform apply tfplan`; monitor output for errors.
6. For destructive operations (`terraform state rm`, `terraform destroy`), pause after each resource and validate.
7. Use `terraform import` for any resources created out-of-band that must be brought under management.
8. Run `terraform plan` after apply to confirm zero changes remain.

---

## Post-Change Validation

- [ ] `terraform plan` shows zero changes after apply — state is consistent with infrastructure
- [ ] Resources are accessible and healthy in the provider console (AWS/Azure/GCP)
- [ ] State is not locked
- [ ] CI pipeline is passing on the applied branch
- [ ] Remote backend state file updated timestamp reflects the apply
- [ ] No deprecated resource warnings in `terraform validate` output
- [ ] Sensitive variable sources still accessible after the change
- [ ] Rollback state backup retained until the change is confirmed stable

---

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

## Import Existing Infrastructure

`terraform import aws_instance.example i-1234567890abcdef0` → verify state: `terraform state show aws_instance.example` → update HCL to match imported config.

```bash
# Write the resource block in your .tf file first (required before importing)
# resource "aws_instance" "example" {
#   # attributes will be populated from state after import
# }

# Import the resource into state
terraform import aws_instance.example i-1234567890abcdef0

# Verify the imported state
terraform state show aws_instance.example

# Generate HCL from imported state (Terraform 1.5+)
terraform plan -generate-config-out=generated.tf

# Run plan — should show zero changes once HCL matches state
terraform plan
```


```text title="Expected output"
aws_instance.example: Importing from ID "i-1234567890abcdef0"...
aws_instance.example: Import complete! Resources imported: 1

# aws_instance.example:
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  subnet_id     = "subnet-0abcd1234efgh5678"
  tags = {
    Name = "web-server-prod"
  }
}

No changes. Your infrastructure matches the configuration.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: resource aws_instance.example does not exist in configuration` | Add the empty resource block to your .tf file before running terraform import. |
    | `Error: InvalidInstanceID.NotFound` | Verify the instance ID is correct and exists in the target AWS region and account. |
```bash
# Common import address formats
terraform import aws_s3_bucket.logs my-bucket-name
terraform import azurerm_resource_group.rg /subscriptions/<sub>/resourceGroups/my-rg
terraform import google_compute_instance.vm projects/my-project/zones/us-east1-b/instances/my-vm
```


```text title="Expected output"
aws_s3_bucket.logs: Importing from ID "my-bucket-name"...
aws_s3_bucket.logs: Import complete!

azurerm_resource_group.rg: Importing from ID "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/my-rg"...
azurerm_resource_group.rg: Import complete!

google_compute_instance.vm: Importing from ID "projects/my-project/zones/us-east1-b/instances/my-vm"...
google_compute_instance.vm: Import complete!

Import successful. Resources have been added to the Terraform state.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: resource address "aws_s3_bucket.logs" does not exist in the configuration` | Add the resource block `resource "aws_s3_bucket" "logs" {}` to your Terraform configuration before importing. |
    | `Error: error reading S3 Bucket (my-bucket-name): AccessDenied: Access Denied` | Verify your AWS credentials have `s3:GetBucketVersioning` and `s3:ListBucket` permissions for the target bucket. |
    | `Error: retrieving subscription ID: subscription ID can not be empty` | Replace `<sub>` with your actual Azure subscription ID in the resource ID path. |
| Step | Action |
|---|---|
| 1 | Write the resource block in `.tf` (placeholder — attributes not needed yet) |
| 2 | Run `terraform import <address> <resource-id>` |
| 3 | Run `terraform state show <address>` to see what was imported |
| 4 | Update HCL attributes to match the imported state |
| 5 | Run `terraform plan` — expect zero changes when config matches state |

## Move State Between Workspaces

`terraform state mv -state-out=other.tfstate module.old module.new` or use `terraform workspace` commands → verify with `terraform plan` showing no changes.

```bash
# List existing workspaces
terraform workspace list

# Create and switch to a new workspace
terraform workspace new staging
terraform workspace select staging

# Move a resource address within the same state file
terraform state mv aws_instance.old_name aws_instance.new_name

# Move a resource to a different state file
terraform state mv \
  -state-out=staging.tfstate \
  module.app.aws_instance.web \
  module.app.aws_instance.web

# Pull state to a local file for manual editing
terraform state pull > current.tfstate

# Push a modified state file back to the remote backend
terraform state push current.tfstate

# Verify after any state move — expect zero changes
terraform plan
```


```text title="Expected output"
* default
  staging

Successfully created and switched to workspace "staging"!

Move "aws_instance.old_name" to "aws_instance.new_name"
Successfully moved 1 resource instance(s).

Move "module.app.aws_instance.web" to "module.app.aws_instance.web"
Successfully moved 1 resource instance(s).

{
  "version": 4,
  "terraform_version": "1.5.2",
  "serial": 42,
  "lineage": "a7f3c2e1-9b4d-4f8a-b2c9-d5e8f1a3b6c4",
  "outputs": {},
  "resources": [
    {
      "mode": "managed",
      "type": "aws_instance",
      "name": "new_name",
      "instances": [...]
    }
  ]
}

State pushed to remote backend.

No changes. Your infrastructure matches the configuration.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: resource address "aws_instance.old_name" does not exist in the current state` | Verify the exact resource address with `terraform state list` before attempting the move. |
    | `Error: failed to read state from remote backend: AccessDenied` | Ensure your AWS credentials are valid and you have `s3:GetObject` and `s3:PutObject` permissions on the state bucket. |
    | `Error: state push rejected: serial number mismatch` | Do not manually edit the `serial` field in the state file; use `terraform state pull` and `terraform state push` without modifications to avoid conflicts. |
| Command | Purpose |
|---|---|
| `terraform workspace new <name>` | Create an isolated state environment |
| `terraform workspace select <name>` | Switch active workspace |
| `terraform state mv <src> <dst>` | Rename or refactor a resource address in state |
| `terraform state mv -state-out` | Move resource to a different state file |
| `terraform state pull / push` | Download or upload state from the remote backend |

## Manage Sensitive Outputs

Mark output as sensitive: `output "password" { value = random_password.db.result; sensitive = true }` → access via: `terraform output -raw password` → never log sensitive outputs in CI.

```hcl
# outputs.tf
output "db_password" {
  description = "Database master password"
  value       = random_password.db.result
  sensitive   = true   # redacted in terraform apply/plan output
}

output "db_endpoint" {
  description = "Database connection endpoint"
  value       = aws_db_instance.main.endpoint
}
```

```bash
# Access a sensitive output value (prints raw value — handle with care)
terraform output -raw db_password

# Access as JSON (sensitive values are still redacted unless -raw is used per output)
terraform output -json

# Pass a sensitive output to another tool without logging it
DB_PASS=$(terraform output -raw db_password)
psql -h "$DB_HOST" -U admin -d mydb -c "\l" <<< "$DB_PASS"

# Never do this — exposes the value in CI logs
echo "Password is: $(terraform output -raw db_password)"
```


```text title="Expected output"
sup3rS3cur3P@ssw0rd!2024
{
  "db_password": {
    "sensitive": true,
    "type": "string",
    "value": "<sensitive>"
  },
  "db_host": {
    "sensitive": false,
    "type": "string",
    "value": "prod-db-01.internal"
  },
  "db_port": {
    "sensitive": false,
    "type": "number",
    "value": 5432
  }
}
                                   List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 mydb      | admin    | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres
(4 rows)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: output not found` | Verify the output name exists in your Terraform configuration with `terraform output` (no arguments) to list all available outputs. |
    | `psql: error: FATAL: password authentication failed for user "admin"` | Ensure the password variable is correctly populated and the database user credentials match; test with `echo "$DB_PASS" | wc -c` to confirm the value was captured. |
    | `Error: output "db_password" is sensitive` | Use the `-raw` flag to access sensitive outputs directly: `terraform output -raw db_password`. |
| Practice | Reason |
|---|---|
| `sensitive = true` on output | Redacts value in `plan` and `apply` console output |
| `terraform output -raw` | Retrieves the raw string value for use in scripts |
| Store secrets in Vault/SSM | Do not rely on Terraform state as a secrets store |
| Encrypt remote backend | State contains sensitive output values in plain text |
| Never `echo` sensitive outputs | Avoids leaking values into CI logs or shell history |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Terraform — Health Checks](../health-checks/)
- [Terraform — CLI Reference](../cli-reference/)
- [Terraform — Common Issues](../../troubleshooting/common-issues/)
