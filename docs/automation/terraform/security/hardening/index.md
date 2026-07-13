---
tags:
  - security
  - terraform
description: "Hardening reference covering Security Scanning Pipeline, Dependency and Provider Security, Hardening Checklist."
---
# Terraform — Hardening

<div class="kb-summary">
Hardening reference covering Security Scanning Pipeline, Dependency and Provider Security, Hardening Checklist.

*Applies to: Terraform 1.x*
</div>

```d2
direction: down

security_scanning_pipeline: "Security Scanning Pipeline" {shape: rectangle}
dependency_and_provider_security: "Dependency and Provider Security" {shape: rectangle}
hardening_checklist: "Hardening Checklist" {shape: rectangle}

security_scanning_pipeline -> dependency_and_provider_security: hardens
dependency_and_provider_security -> hardening_checklist: hardens
```

## Before you begin

- **Access:** Provider credentials configured (`terraform login` or env vars)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Security Scanning Pipeline

```d2
direction: right

prOpen: "Pull Request\nopened" {shape: rectangle}
tfFmt: "terraform fmt -check\n(formatting" {shape: rectangle}
tfValidate: "terraform validate\n(syntax" {shape: rectangle}
tfsec: "tfsec .\n(misconfig scan" {shape: rectangle}
checkov: "checkov -d .\n(policy-as-code" {shape: rectangle}
tfPlan: "terraform plan\n-out=tfplan" {shape: rectangle}
sentinel: "Sentinel / OPA\npolicy evaluation" {shape: rectangle}
reviewGate: "Human Review\n(plan output in PR" {shape: rectangle}
tfApply: "terraform apply\n(main branch only" {shape: rectangle}

prOpen -> tfFmt
tfFmt -> tfValidate
tfValidate -> tfsec
tfsec -> checkov
checkov -> tfPlan
tfPlan -> sentinel
sentinel -> reviewGate
sentinel -> prOpen
reviewGate -> tfApply
reviewGate -> prOpen
```

## Dependency and Provider Security

```bash
# Lock provider versions to prevent unexpected upgrades
terraform providers lock

# Review the lock file for unexpected version changes
git diff .terraform.lock.hcl

# Verify provider checksums after init
cat .terraform.lock.hcl | grep -A5 "provider"

# Use version constraints to limit provider versions
# versions.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"   # allows patch updates only within 5.x
    }
  }
  required_version = ">= 1.5.0"
}
```


```text title="Expected output"
# Lock provider versions to prevent unexpected upgrades
Terraform will lock provider versions in .terraform.lock.hcl

# Review the lock file for unexpected version changes
diff --git a/.terraform.lock.hcl b/.terraform.lock.hcl
index 4a2c8f1..9e3d5c2 100644
--- a/.terraform.lock.hcl
+++ b/.terraform.lock.hcl
@@ -1,6 +1,6 @@
 # This file is maintained automatically by "terraform init".
 # Manual edits may be lost in a future update.
-provider "registry.terraform.io/hashicorp/aws" {
+provider "registry.terraform.io/hashicorp/aws" {
   version     = "5.42.0"
-  constraints = "~> 5.0"
+  constraints = "~> 5.1"

# Verify provider checksums after init
provider "registry.terraform.io/hashicorp/aws" {
  version     = "5.42.0"
  constraints = "~> 5.0"
  hashes = [
    "h1:lfGEkp3fvJ8UTnxYv+8RINN4Cjxc8C8+Tnc8LExPHE=",
    "h1:mV7g+8n6DTT9vxJ8xfewKM8P7hvto2nQoAZMHBFAZ4=",
  ]
}

(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Failed to lock provider versions`** — Run `terraform init` first to download providers before attempting to lock versions.
    **`fatal: pathspec '.terraform.lock.hcl' did not match any files`** — Execute `terraform init` to generate the lock file before running `git diff`.
## Hardening Checklist

| Area | Practice |
|---|---|
| Static analysis | Run `tfsec` or `checkov` in CI before every plan |
| Policy enforcement | Use Sentinel or OPA to enforce tagging and compliance rules |
| Provider versions | Lock with `terraform providers lock`; review changes in PRs |
| Sensitive outputs | Mark with `sensitive = true`; review plan output for exposed secrets |
| State access | Restrict state bucket to the Terraform automation role |
| `.gitignore` | Exclude `*.tfvars`, `*.tfstate`, `*.tfstate.backup`, `.terraform/` |
| Code review | All Terraform PRs reviewed before apply; plan output included |
| Audit logs | Enable CloudTrail / Azure Monitor for all provider API calls |

---

## See also

- [Terraform — Authentication](../authentication/)
- [Terraform — Access Control](../access-control/)
- [Terraform — Encryption](../encryption/)
