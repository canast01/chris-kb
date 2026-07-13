---
tags:
  - security
  - terraform
description: "Access Control reference covering Terraform RBAC and Backend Access Model, Least Privilege IAM for Terraform, Workspace and Environment Separation, Access..."
---
# Terraform — Access Control

<div class="kb-summary">
Access Control reference covering Terraform RBAC and Backend Access Model, Least Privilege IAM for Terraform, Workspace and Environment Separation, Access Control Reference.

*Applies to: Terraform 1.x*
</div>

## Before you begin

- **Access:** Provider credentials configured (`terraform login` or env vars)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Terraform RBAC and Backend Access Model

```d2
direction: right

ciRunner: "CI/CD Runner\n(GitHub Actions / GitLab" {shape: rectangle}
tfRole: "IAM Role:\nterraform-automation\n(least privilege" {shape: rectangle}
s3State: "S3 State Bucket\n(private + encrypted" {shape: rectangle}
dynamoLock: "DynamoDB Lock Table" {shape: rectangle}
targetResources: "Target Resources\n(EC2, RDS, VPC..." {shape: rectangle}
humanReview: "Human Reviewer\n(read-only credentials" {shape: rectangle}
auditLog: "CloudTrail / Audit Log" {shape: rectangle}

ciRunner -> tfRole
tfRole -> s3State
tfRole -> dynamoLock
tfRole -> targetResources
humanReview -> s3State
tfRole -> auditLog
humanReview -> auditLog
```

## Workspace and Environment Separation

Use separate credentials and backends per environment to prevent a staging Terraform run from modifying production.

```hcl
# Use workspace-specific state paths
terraform {
  backend "s3" {
    bucket = "myorg-terraform-state"
    key    = "env/${terraform.workspace}/terraform.tfstate"
    region = "eu-west-1"
  }
}
```

## Access Control Reference

| Area | Practice |
|---|---|
| State bucket | Private, encrypted, access restricted to Terraform role |
| State locking | DynamoDB or equivalent backend locking enabled |
| IAM role | Dedicated per-environment role with least privilege |
| CI/CD | Credentials injected via secrets; not stored in code |
| Human access | Use read-only credentials for review; write credentials for planned applies only |

---

## See also

- [Terraform — Authentication](../authentication/)
- [Terraform — Hardening](../hardening/)
- [Terraform — Encryption](../encryption/)
