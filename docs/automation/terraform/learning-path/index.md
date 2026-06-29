---
tags:
  - learning-path
  - terraform
---
# Terraform — Learning Path

<div class="kb-summary">
Recommended reading order for HashiCorp Terraform. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Terraform 1.x*
</div>

```d2
direction: right

S1: "Architecture" {shape: rectangle}
S2: "Deploy" {shape: rectangle}
S3: "Operations" {shape: rectangle}
S4: "Security" {shape: rectangle}
S5: "Troubleshoot" {shape: rectangle}

S1 -> S2
S2 -> S3
S3 -> S4
S4 -> S5
```
| Stage | Focus | Time investment |
|-------|-------|----------------|
| 1 — Architecture | Provider-resource-state model, dependency graph | 3–4 h |
| 2 — Deployment | Backend setup, CI/CD pipeline, version pinning | 2–3 h |
| 3 — Operations | Drift detection, state management, CLI | ongoing |
| 4 — Security | State encryption, OIDC, Sentinel policies | 2–3 h |
| 5 — Troubleshooting | State corruption, provider errors, import | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand Terraform's provider-resource-state model and how plan/apply/destroy translate into API calls against real infrastructure.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — providers, resources, data sources, the state file lifecycle (refresh → plan → apply), and the resource dependency graph that determines operation order
- [Design Standards](../architecture/design-standards/) — module structure and calling conventions, workspace conventions, remote state backends (S3+DynamoDB, Terraform Cloud, AzureRM), and variable/output patterns
- [Integrations](../architecture/integrations/) — Terraform Cloud/Enterprise as a remote execution backend, VCS-driven run triggers, and Sentinel policy-as-code enforcement on every plan

**Key concepts before moving on**:

- The state file is Terraform's source of truth — if it diverges from reality, `plan` will try to converge, potentially destroying resources
- `terraform plan` never changes infrastructure; `terraform apply` does — always review the plan output before confirming
- Modules are reusable units of configuration; root modules call child modules and pass inputs via variables
- State locking (DynamoDB for S3 backend) prevents concurrent `apply` operations from corrupting the state file

**Why first**: Terraform's state model is the source of truth for everything it manages. Understanding it before writing code prevents drift, accidental destroys, and state corruption that is difficult to recover from.

---

## Stage 2 — Deployment

**Goal**: Bootstrap a Terraform project with a safe remote backend and a working CI/CD pipeline before writing production modules.

**Read**:

- [Deploy](../deploy/) — backend configuration (`terraform { backend "s3" {} }`), provider version pinning with `required_providers`, workspace initialisation, and first `terraform apply` with a plan review gate
- [Install & Upgrade](../operations/install-upgrade/) — Terraform version management with `tfenv`, provider upgrade procedures (`terraform init -upgrade`), and state migration after major Terraform version changes

**Deployment principles**:

- Always use a remote backend for team environments — local state files cause conflicts and are not recoverable after disk loss
- Pin both Terraform CLI and provider versions with `required_version` and `required_providers` constraints
- Run `terraform plan` in CI and require a human review/approval before `terraform apply` executes against production

---

## Stage 3 — Operations

**Goal**: Run Terraform plans and applies safely, detect configuration drift, and manage the state file without corruption.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; `terraform plan` for drift detection, workspace state consistency checks, backend connectivity verification, and Terraform Cloud workspace run history
- [CLI Reference](../operations/cli-reference/) — `init`, `plan`, `apply`, `destroy`, `state list`, `state show`, `state mv`, `state rm`, `import`, `output`, `workspace`, and `taint` command patterns
- [Procedures](../operations/procedures/) — importing existing resources with `terraform import`, removing orphaned state entries with `state rm`, targeted applies with `-target`, and module refactoring without destroying resources
- [Backup & Restore](../operations/backup-restore/) — S3 versioning for state file backup, Terraform Cloud state history, manual state file backup before risky operations, and state recovery from S3 versions
- [Scripts](../operations/scripts/) — plan/apply pipeline wrapper scripts, drift detection scheduled jobs, cost estimation via Infracost integration, and workspace listing/reporting automation

**Daily rhythm**: Check workspace run history → `terraform plan` for drift → review any pending applies → verify state backend health.

---

## Stage 4 — Security

**Goal**: Protect sensitive state data, enforce code review for all infrastructure changes, and prevent unauthorised applies.

**Read**:

- [Access Control](../security/access-control/) — Terraform Cloud team permissions (read/plan/apply), remote state access policies (S3 bucket policy), variable set scoping to specific workspaces
- [Authentication](../security/authentication/) — provider credential injection via environment variables, OIDC for GitHub Actions and GitLab CI runners (no long-lived keys), and HashiCorp Vault dynamic credentials for AWS/Azure
- [Encryption](../security/encryption/) — state file encryption at rest in S3 (SSE-KMS) or Terraform Cloud (AES-256), sensitive variable masking in Terraform Cloud, and `sensitive = true` on outputs that contain secrets
- [Hardening](../security/hardening/) — Sentinel policies for mandatory tagging and resource type allowlisting, `required_providers` version constraints to prevent supply chain surprises, and `prevent_destroy` lifecycle guards on critical resources

---

## Stage 5 — Troubleshooting

**Goal**: Resolve plan failures, state inconsistencies, and provider API errors without corrupting the state file.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — state lock timeout (DynamoDB lock stuck after crash), provider authentication failure, `resource already exists` requiring `import`, dependency cycle errors, and provider version incompatibility
- [Diagnostics](../troubleshooting/diagnostics/) — `TF_LOG=DEBUG` trace output, `terraform show` to inspect state, `terraform state list` to audit managed resources, and provider-side API error codes in the plan output
- [Escalation](../troubleshooting/escalation/) — HashiCorp support for Terraform Enterprise, GitHub issues for open-source provider bugs, community Terraform forum for configuration questions, and state recovery specialists for corrupt backends

**Why last**: Troubleshooting makes most sense once you understand the state model and can distinguish between a Terraform logic error, a provider API error, and a state drift issue.

---

## See also

- [Terraform — Deploy](../deploy/)
- [Terraform — Procedures](../operations/procedures/)
- [Terraform — Common Issues](../troubleshooting/common-issues/)
