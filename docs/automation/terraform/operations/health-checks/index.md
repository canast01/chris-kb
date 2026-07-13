---
tags:
  - operations
  - terraform
description: "Health Checks reference covering Drift Detection Flow, Daily Checks."
---
# Terraform — Health Checks

<div class="kb-summary">
Health Checks reference covering Drift Detection Flow, Daily Checks.

*Applies to: Terraform 1.x*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
provider_drift: "Provider Drift" {shape: rectangle}
workspace_management: "Workspace Management" {shape: rectangle}
backend_connectivity: "Backend Connectivity" {shape: rectangle}
drift_detection_flow: "Drift Detection Flow" {shape: rectangle}
daily_checks: "Daily Checks" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> provider_drift
provider_drift -> workspace_management
workspace_management -> backend_connectivity
backend_connectivity -> drift_detection_flow
drift_detection_flow -> daily_checks
daily_checks -> generate_report
```

## Before you begin

- **Access:** Provider credentials configured (`terraform login` or env vars)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

```bash
# 1. Terraform version
terraform version

# 2. Provider versions
terraform providers

# 3. State file integrity — verify count matches expected resources
terraform state list | wc -l

# 4. Plan drift check — exit 0 = no changes, exit 2 = changes detected
terraform plan -detailed-exitcode; echo "Exit: $?"

# 5. Workspace list
terraform workspace list

# 6. Backend connectivity — should succeed without errors
terraform init -backend=true

# 7. Validate configuration
terraform validate

# 8. State lock check — inspect backend for stale locks; this is informational
terraform force-unlock --help
```


```text title="Expected output"
Terraform v1.5.7
on linux_amd64

Your version of Terraform is out of date! The newest version
is 1.6.2. You can update by downloading from https://www.terraform.io/downloads.html

Providers used by the current state:

provider[registry.terraform.io/hashicorp/aws]
  version = 1.2.3
  locked version = 1.2.3

provider[registry.terraform.io/hashicorp/kubernetes]
  version = 2.18.1
  locked version = 2.18.1

47

No changes. Your infrastructure matches the configuration.

Exit: 0

  default
* prod
  staging

Successfully configured the backend "s3"! Terraform will automatically
use this backend in subsequent commands.

Success! The configuration is valid.

Usage: terraform force-unlock [options] LOCK_ID

  Manually unlock the state for the defined backend, which removes the lock on
  the state file database.
```

!!! warning "Common errors"
    **`Error: Backend initialization required: please run "terraform init"`** — Run `terraform init` in the working directory to initialize the backend and download provider plugins.
    **`Error: Error acquiring the state lock`** — Verify backend connectivity and check for stale locks with `terraform force-unlock <lock-id>` if the lock is orphaned.
Compare the output against the expected resource count tracked in your runbook. A sudden drop or spike indicates a state manipulation issue.

**Inspect a specific resource**

```bash
terraform state show <resource_address>
```


```text title="Expected output"
# aws_instance.web_server:
resource "aws_instance" "web_server" {
  ami                    = "ami-0c55b159cbfafe1f0"
  associate_public_ip_address = true
  availability_zone      = "us-east-1a"
  instance_type          = "t3.medium"
  key_name               = "prod-deploy-key"
  private_ip             = "10.0.2.45"
  public_ip              = "203.0.113.87"
  security_groups        = [
    "sg-0a1b2c3d4e5f6g7h8",
  ]
  subnet_id              = "subnet-0f1e2d3c4b5a6789"
  tags = {
    "Environment" = "production"
    "Name"        = "web-server-01"
  }
  vpc_security_group_ids = [
    "sg-0a1b2c3d4e5f6g7h8",
  ]
}
```

!!! warning "Common errors"
    **`Error: resource address "resource_address" not found in the current state`** — Replace `<resource_address>` with the actual resource type and name (e.g., `aws_instance.web_server`).
    **`Error: No state file found`** — Initialize the Terraform working directory with `terraform init` and ensure a state file exists in the current directory or remote backend.
**Remove a stale resource from state (non-destructive)**

```bash
terraform state rm <resource_address>
```


```text title="Expected output"
Removed aws_instance.web_server from state
```

!!! warning "Common errors"
    **`Error: resource address "aws_instance.web_server" does not exist in the current state`** — Verify the exact resource address with `terraform state list` before attempting removal.
    **`Error: Failed to read state`** — Ensure you have read/write permissions on the state file and backend is accessible (check `terraform init` completed successfully).
Use only when a resource has been manually deleted outside Terraform and the state entry is orphaned.

**Pull remote state to inspect locally**

```bash
terraform state pull > state-snapshot.json
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Failed to read state` — Ensure you are in the correct Terraform working directory and have initialized the workspace with `terraform init`.**
    **`Error: Insufficient permissions to read state` — Verify your AWS/cloud credentials are configured and have `s3:GetObject` permissions if using remote state.**
Review `state-snapshot.json` for unexpected `null` values, duplicate serial numbers, or missing resource blocks.

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Resource count | Matches expected | Investigate additions or removals |
| Serial number | Incrementing | Reset or re-init if repeated |
| Lock file present | None (steady state) | Force-unlock if stale |
| State file age | Updated on last apply | Re-run plan to verify |

---

## Provider Drift

Provider version drift occurs when local `.terraform.lock.hcl` entries diverge from what is declared in `required_providers`, or when a provider registry releases a new version that was not pinned.

**Check configured providers and their sources**

```bash
terraform providers
```


```text title="Expected output"
Providers required by configuration:

.
├── provider[registry.terraform.io/hashicorp/aws]
│   └── ~> 5.0
├── provider[registry.terraform.io/hashicorp/azurerm]
│   └── ~> 3.80
└── provider[registry.terraform.io/hashicorp/kubernetes]
    └── ~> 2.23

Providers required by state:

.
├── provider[registry.terraform.io/hashicorp/aws] 5.12.0
├── provider[registry.terraform.io/hashicorp/azurerm] 3.85.0
└── provider[registry.terraform.io/hashicorp/kubernetes] 2.23.1
```

!!! warning "Common errors"
    **`Error: No configuration files`** — Run `terraform init` first to initialize the working directory and download provider plugins.
    **`Error: Incompatible provider version`** — Update the provider constraint in your `.tf` files or run `terraform init -upgrade` to fetch compatible versions.
**Review lock file constraints**

```bash
cat .terraform.lock.hcl
```


```text title="Expected output"
# This file is maintained automatically by "terraform init".
# Manual edits may be lost in future updates.

provider "registry.terraform.io/hashicorp/aws" {
  version     = "5.31.0"
  constraints = "~> 5.0"
  hashes = [
    "h1:liSsUIlq1iYIc7xNUVcib1LlXnLYveMdPCVwmBEMAc=",
    "h1:mLiMVYvEsKpqKJqAMhWBqKzJBKKJmVQvJLHXPLDqZc=",
  ]
}

provider "registry.terraform.io/hashicorp/null" {
  version     = "3.2.2"
  constraints = ">= 3.0"
  hashes = [
    "h1:zT1ZbegaAYHwQaTBgTjGQ/N+AzByxiGRQX7ZohIQVc=",
  ]
}
```

!!! warning "Common errors"
    **`cat: .terraform.lock.hcl: No such file or directory`** — Run `terraform init` in the working directory to generate the lock file.
    **`Permission denied`** — Check file permissions with `ls -la .terraform.lock.hcl` and ensure the user has read access.
Confirm that the `version` and `constraints` fields in the lock file match the versions declared in `versions.tf` or the root module.

**Re-initialise and upgrade providers (controlled)**

```bash
terraform init -upgrade
```


```text title="Expected output"
Initializing the backend...

Upgrading modules...
- aws_vpc_module in modules/vpc
- aws_security_module in modules/security
- aws_rds_module in modules/rds

Upgrading provider plugins...
- Upgrading hashicorp/aws from v5.12.0 to v5.28.1
- Upgrading hashicorp/random from v3.4.3 to v3.5.1

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" next.
```

!!! warning "Common errors"
    **`Error: Failed to download module source`** — Verify the module source URL is correct and accessible, and check your network connectivity and VCS credentials.
    **`Error: Incompatible provider version`** — Review the required_providers block in your configuration and adjust version constraints to match available releases.
Run this only during a planned maintenance window. After upgrading, run `terraform plan` to verify no unintended resource changes are introduced by the new provider version.

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Lock file present | Yes, committed to VCS | Re-init and commit |
| Provider version pinned | `~>` or exact version | Add version constraint |
| Plan after provider upgrade | No changes | Review provider changelog |

---

## Workspace Management

Workspaces isolate state between environments (e.g., `dev`, `staging`, `prod`). Confirm that the correct workspace is active before any operation.

**List all workspaces**

```bash
terraform workspace list
```


```text title="Expected output"
default
* prod
  staging
  dev
```

!!! warning "Common errors"
    **`Error: Not a valid terraform directory`** — Run the command from the directory containing your `.terraform` directory or re-initialize with `terraform init`.
    **`Error: Failed to read state file`** — Ensure the backend is accessible (check AWS credentials, network connectivity, or remote state lock) and run `terraform init` to reinitialize the backend.
The active workspace is marked with `*`.

**Show current workspace**

```bash
terraform workspace show
```


```text title="Expected output"
default
```

!!! warning "Common errors"
    **`Error: Not a valid terraform directory`** — Run the command from the directory containing your `.terraform` directory or re-initialize with `terraform init`.
    **`Error: Failed to read state file`** — Ensure the state backend is accessible and credentials are valid; check `terraform login` or backend configuration in `terraform.tf`.
**Switch workspace**

```bash
terraform workspace select <workspace_name>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: workspace "<workspace_name>" does not exist`** — Run `terraform workspace list` to see available workspaces, then use the correct name.
    **`Error: Failed to select workspace: invalid character in workspace name`** — Workspace names must contain only alphanumeric characters, hyphens, and underscores; rename or use a valid existing workspace.
**Confirm state is scoped to the correct workspace**

```bash
terraform state list
```


```text title="Expected output"
aws_instance.web_server_01
aws_instance.web_server_02
aws_instance.database_primary
aws_security_group.app_tier
aws_security_group.db_tier
aws_rds_instance.postgres_main
aws_s3_bucket.logs_archive
aws_cloudwatch_log_group.application_logs
```

!!! warning "Common errors"
    **`Error: No state file was found!`** — Initialize the Terraform working directory with `terraform init` to create or load the state file.
    **`Error: Error reading state file: stat .terraform/terraform.tfstate: permission denied`** — Ensure your user has read permissions on the `.terraform` directory and state file with `chmod 600 .terraform/terraform.tfstate`.
Run this immediately after switching workspaces to verify the resource list matches the expected environment.

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Active workspace | Matches target environment | Switch before running plan/apply |
| State per workspace | Separate, non-overlapping | Audit if resources appear in wrong workspace |
| Workspace naming | Consistent convention | Rename or document deviations |

---

## Backend Connectivity

The remote backend (S3, Terraform Cloud, Azure Blob, GCS, etc.) must be reachable and properly authenticated for state reads, writes, and locking.

**Test backend connectivity**

```bash
terraform init -backend=true
```


```text title="Expected output"
Initializing the backend...

Successfully configured the backend "local"! Terraform will automatically
use this backend in subsequent commands provided the backend configuration
remains at these settings.

Initializing provider plugins...
- Finding latest version of hashicorp/aws...
- Installing hashicorp/aws v5.38.0...
- Installed hashicorp/aws v5.38.0 (signed by HashiCorp)

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that would be required to apply your current configuration.
```

!!! warning "Common errors"
    **`Error: Unsupported or incorrectly formatted backend configuration`** — Verify the backend block in your terraform configuration files has valid syntax and the backend type is supported.
    **`Error: Failed to download provider plugin`** — Check your internet connection and ensure your Terraform registry credentials are configured if using a private registry.
A clean init with no errors confirms backend credentials and network access are valid.

**Check backend configuration**

```bash
cat backend.tf
```


```text title="Expected output"
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-state-prod-us-east-1"
    key            = "health-checks/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

!!! warning "Common errors"
    **`cat: backend.tf: No such file or directory`** — Ensure you are in the correct Terraform working directory (typically the root of your infrastructure-as-code repository).
    **`Permission denied`** — Run `chmod +r backend.tf` or check that your user has read permissions on the file.
Verify that the bucket/container name, region, and key path are correct for the current environment.

**Validate credentials (AWS example)**

```bash
aws sts get-caller-identity
```


```text title="Expected output"
{
    "UserId": "AIDAI7K8Q9M2L5N3P7R9",
    "Account": "987654321098",
    "Arn": "arn:aws:iam::987654321098:user/terraform-admin"
}
```

!!! warning "Common errors"
    **`Unable to locate credentials`** — Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
    **`An error occurred (UnauthorizedOperation) when calling the GetCallerIdentity operation: User: arn:aws:iam::987654321098:user/terraform-admin is not authorized to perform: sts:GetCallerIdentity`** — Add the `sts:GetCallerIdentity` permission to the IAM user or role's policy.
Replace with the equivalent CLI check for your cloud provider (e.g., `az account show` for Azure, `gcloud auth list` for GCP).

**Force-unlock a stale lock (use with caution)**

```bash
terraform force-unlock <lock-id>
```


```text title="Expected output"
Terraform state lock with ID "8f4c2a91-7e3b-4d19-b8f2-1a6c5e9d2b3f" forcefully unlocked.
```

!!! warning "Common errors"
    **`Error: Error acquiring the state lock`** — Verify the lock ID is correct and the state backend is accessible by checking `terraform state list`.
    **`Error: resource not found`** — Ensure you are in the correct Terraform working directory and the backend configuration matches the locked state.
Obtain the lock ID from the backend error message or by inspecting the lock object directly in the backend store. Only unlock if you have confirmed no active `apply` is running.

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| `terraform init` exit code | 0 | Check credentials and network |
| Backend lock file | Absent (steady state) | Investigate running operations |
| Credential expiry | Valid | Rotate or renew before expiry |
| Backend region/endpoint | Correct for environment | Update `backend.tf` |

---

## Drift Detection Flow

### terraform import

Import real resources into state that were created outside Terraform.

```bash
# Import an existing AWS EC2 instance
terraform import aws_instance.web01 i-0abcd1234efgh5678

# Import with a module path
terraform import module.network.aws_vpc.main vpc-0a1b2c3d4e5f

# Import an Azure resource
terraform import azurerm_resource_group.rg /subscriptions/SUB_ID/resourceGroups/my-rg
```


```text title="Expected output"
aws_instance.web01: Importing from ID "i-0abcd1234efgh5678"...
aws_instance.web01: Import complete!
  Imported aws_instance (ID: i-0abcd1234efgh5678)

module.network.aws_vpc.main: Importing from ID "vpc-0a1b2c3d4e5f"...
module.network.aws_vpc.main: Import complete!
  Imported aws_vpc (ID: vpc-0a1b2c3d4e5f)

azurerm_resource_group.rg: Importing from ID "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-rg"...
azurerm_resource_group.rg: Import complete!
  Imported azurerm_resource_group (ID: /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-rg)
```

!!! warning "Common errors"
    **`Error: resource address "aws_instance.web01" does not exist in the configuration`** — Add the resource block `resource "aws_instance" "web01" {}` to your Terraform configuration before running import.
    **`Error: error reading resource: ResourceNotFound`** — Verify the resource ID is correct and exists in the target cloud account/subscription.
    **`Error: error reading resource: Unauthorized`** — Ensure your cloud credentials (AWS_PROFILE, ARM_CLIENT_ID, etc.) have permissions to read the target resource.
After import, add the matching resource block to your `.tf` files, then run `terraform plan` to verify state matches configuration.

### moved Blocks

The `moved` block updates state when you rename or move resources without recreating them.

```hcl
# terraform/moved.tf
moved {
  from = aws_instance.old_name
  to   = aws_instance.new_name
}

moved {
  from = aws_security_group.sg
  to   = module.network.aws_security_group.sg
}
```

```bash
# Verify no unintended changes after adding moved blocks
terraform plan
# Should show: "0 to add, 0 to change, 0 to destroy"
```


```text title="Expected output"
Terraform used the following state to generate this plan:

resource "aws_instance" "web_server" is read as:
  - id = "i-0a7f3c8e9b2d1f4a6"
  - ami = "ami-0c55b159cbfafe1f0"
  - instance_type = "t3.micro"
  - tags = {
      "Name" = "production-web-01"
    }

No changes. Infrastructure is up-to-date.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

!!! warning "Common errors"
    **`Error: Resource instance managed by a different state`** — Ensure all `moved` blocks reference the correct source and destination resource addresses, and run `terraform state list` to verify the current state structure.
    **`Error: Invalid moved block: source and destination cannot be the same`** — Remove or correct the `moved` block so source and destination addresses differ (e.g., `from = aws_instance.old` to `to = aws_instance.new`).
### Scheduled Drift Detection

Run drift checks on a schedule in CI/CD to get early warnings.

```yaml
# .github/workflows/drift-check.yml
name: Terraform Drift Check

on:
  schedule:
    - cron: '0 8 * * 1-5'   # weekdays at 08:00 UTC
  workflow_dispatch:

jobs:
  drift:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        run: terraform init
        working-directory: infra/

      - name: Check for Drift
        id: plan
        run: terraform plan -detailed-exitcode -refresh=true -no-color
        working-directory: infra/
        continue-on-error: true

      - name: Notify on Drift
        if: steps.plan.outputs.exitcode == '2'
        run: |
          echo "DRIFT DETECTED — manual review required"
          # Add Slack/Teams notification here
        env:
          exitcode: ${{ steps.plan.outputs.exitcode }}
```

### Drift Causes and Remediation

| Drift cause | Detection | Remediation |
|---|---|---|
| Manual console change | `terraform plan` shows difference | Re-apply config or import and update code |
| Resource auto-modified by cloud provider | `terraform plan -refresh=true` | Update code to match or accept with `-refresh-only` |
| Resource deleted outside Terraform | Plan shows resource will be recreated | Import if it exists; allow recreation if intentional |
| State file out of date | Refresh shows many differences | Run `terraform apply -refresh-only` then review |

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

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Terraform — Procedures](../procedures/)
- [Terraform — CLI Reference](../cli-reference/)
- [Terraform — Common Issues](../../troubleshooting/common-issues/)
