---
tags:
  - architecture
  - terraform
---
# Terraform — Standards


<div class="kb-summary">
Consistent Terraform standards prevent state corruption, make code reviewable, and enable teams to manage infrastructure at scale without heroics.
</div>

---

## Directory Structure

### Root module (single environment)

```text
┌──────────────────────────────────── Terraform — Design Standards ─────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   TF standards: consistent module structure, remote state, provider pinning, CI enforcement   │   │
│   │ Directory layout: modules/ (reusable), environments/ (per-env root), shared/ (cross-env data) │   │
│   │    CI: terraform fmt -check → validate → tflint → checkov → plan → manual approval → apply    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                File Structure                │  │                Quality Rules                │   │
│   │              main.tf: resources              │  │           terraform fmt -recursive          │   │
│   │           variables.tf: all inputs           │  │              terraform validate             │   │
│   │           outputs.tf: all exports            │  │            tflint: provider rules           │   │
│   │       versions.tf: required_providers        │  │            checkov: security scan           │   │
│   │       backend.tf: remote state config        │  │           No hardcoded credentials          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   tflint      = Terraform linter; checks for unused vars, deprecated syntax, provider rules   │   │
│   │ checkov     = Bridgecrew IaC security scanner; checks for open SGs, unencrypted storage, etc. │   │
│   │         terraform-docs = auto-generate module README from variables.tf and outputs.tf         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
### Module versioning policy

| Environment | Policy |
|---|---|
| dev | May use `~>` (patch-level flexibility) for testing new versions |
| staging | Must match prod version |
| prod | Must use exact version pin (`=`) |

Use `~>` (pessimistic constraint) only when the module author follows semver strictly:

```hcl
version = "~> 5.8"    # Allows 5.8.x, not 5.9 or 6.x
version = "~> 5.8.0"  # Allows 5.8.x only — stricter
version = "5.8.0"     # Exact — safest for production
```

---

## Variable and Output Standards

### Variables

```hcl
# variables.tf
variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, prod)"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod"
  }
}

variable "vpc_cidr_block" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
  validation {
    condition     = can(cidrnetmask(var.vpc_cidr_block))
    error_message = "vpc_cidr_block must be a valid CIDR block"
  }
}

variable "enable_nat_gateway" {
  type        = bool
  description = "Create NAT gateways for private subnets"
  default     = true
}

variable "tags" {
  type        = map(string)
  description = "Additional tags to apply to all resources"
  default     = {}
}

# Sensitive variables — never have defaults in code
variable "db_password" {
  type        = string
  description = "Master password for RDS instance"
  sensitive   = true
}
```

### Outputs

```hcl
# outputs.tf
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "List of IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "db_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = false  # Endpoint is not a secret — make accessible
}

output "db_password" {
  description = "RDS master password (sensitive)"
  value       = var.db_password
  sensitive   = true  # Prevents display in plan/apply output
}
```

---

## tfvars Management

```hcl
# terraform.tfvars — default values (committed to Git — no secrets)
environment       = "dev"
aws_region        = "eu-west-1"
vpc_cidr_block    = "10.10.0.0/16"
enable_nat_gateway = false

tags = {
  managed_by  = "terraform"
  team        = "platform"
  cost_centre = "platform-engineering"
}
```

```hcl
# prod.tfvars — environment-specific overrides
environment        = "prod"
vpc_cidr_block     = "10.0.0.0/16"
enable_nat_gateway = true
```

```bash
# Apply with environment-specific vars
terraform apply -var-file="prod.tfvars"

# Sensitive values via environment variables (never in .tfvars files)
export TF_VAR_db_password="$(vault kv get -field=password secret/rds/prod)"
terraform apply -var-file="prod.tfvars"
```

### `.tfvars` file rules

| File | Contains | Committed to Git? |
|---|---|---|
| `terraform.tfvars` | Non-sensitive defaults | Yes |
| `{env}.tfvars` | Non-sensitive env overrides | Yes |
| `secrets.tfvars` | Sensitive values | NEVER |
| `.auto.tfvars` | Auto-loaded values | Caution — commit if non-sensitive |

Add to `.gitignore`:

```gitignore
*.tfvars.json
secrets.tfvars
override.tf
override.tf.json
*_override.tf
*_override.tf.json
.terraform/
terraform.tfstate
terraform.tfstate.backup
.terraform.lock.hcl   # EXCEPTION: DO commit this file
```

> The `.terraform.lock.hcl` file (provider lock file) must be committed to Git. It pins provider versions for reproducible runs.

---

## Tagging Standards

All resources that support tags must be tagged. Use a `locals` block for consistency.

```hcl
# locals.tf
locals {
  mandatory_tags = {
    environment = var.environment
    managed_by  = "terraform"
    team        = "platform-engineering"
    cost_centre = var.cost_centre
    repo        = "github.com/my-org/platform-infra"
  }

  common_tags = merge(local.mandatory_tags, var.tags)
}

# Apply to resources
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr_block
  tags       = merge(local.common_tags, { Name = "vpc-${var.environment}-euw1" })
}

# AWS default tags (applies to all resources in the provider)
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = local.mandatory_tags
  }
}
```

### Required tags

| Tag key | Description | Example |
|---|---|---|
| `environment` | Deployment environment | `prod` |
| `managed_by` | Always `terraform` | `terraform` |
| `team` | Owning team | `platform-engineering` |
| `cost_centre` | FinOps cost allocation | `infra-shared` |
| `repo` | Source repository URL | `github.com/org/infra` |

---

## State File Locking

State locking prevents concurrent operations from corrupting state. It is automatic with supported backends.

```bash
# If a lock is stuck (e.g. CI runner crashed mid-apply), force-unlock:
# Get the lock ID from the error message
terraform force-unlock LOCK-ID-HERE

# Verify lock state (S3 backend — check DynamoDB)
aws dynamodb scan --table-name terraform-state-lock --region eu-west-1
```

Best practices:

- Never run `terraform apply` from multiple terminals/CI jobs simultaneously against the same workspace
- Use serialised CI pipelines (no parallel apply jobs for the same root module)
- Set the DynamoDB TTL on lock records if your backend supports it
- Alert on lock records older than 30 minutes — indicates a stuck process

---

## Code Review Checklist

Use this checklist for all Terraform PRs before merging.

### Correctness

- [ ] `terraform validate` passes
- [ ] `terraform fmt -check` passes (no formatting changes)
- [ ] Plan output reviewed — no unexpected deletions or replacements
- [ ] `lifecycle { prevent_destroy = true }` present on stateful resources (RDS, S3 buckets)
- [ ] No `create_before_destroy` missing where replacement would cause downtime

### Security

- [ ] No hardcoded credentials or secrets in `.tf` or `.tfvars` files
- [ ] Sensitive variables marked `sensitive = true`
- [ ] IAM policies follow least privilege — no `*:*` wildcards
- [ ] Security group ingress does not expose ports to `0.0.0.0/0` without justification
- [ ] Storage encryption enabled
- [ ] Public access blocked on storage buckets by default
- [ ] `tfsec` or `checkov` scan passes (or findings documented and accepted)

### State and Backend

- [ ] Backend configured correctly for the environment
- [ ] State file path is unique and descriptive
- [ ] `.terraform.lock.hcl` committed

### Modules and Versions

- [ ] Provider versions pinned in `versions.tf`
- [ ] Module versions pinned (no floating refs)
- [ ] `required_version` constraint set

### Standards

- [ ] Mandatory tags applied to all taggable resources
- [ ] Resource names follow naming convention table
- [ ] All variables have `description` and `type`
- [ ] All outputs have `description`
- [ ] `terraform-docs` output in module README is up to date

```bash
# Run tfsec (security scanner)
tfsec .

# Run checkov
checkov -d . --framework terraform

# Generate module documentation
terraform-docs markdown table --output-file README.md --output-mode inject .
```
