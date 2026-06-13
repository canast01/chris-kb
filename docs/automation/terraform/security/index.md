---
tags:
  - security
  - terraform
---
# Terraform — Security



<div class="kb-summary">
Terraform security — state file encryption, secrets handling, provider authentication, and Terraform Cloud access controls.
</div>

```text
┌──────────────────────────────────────── Terraform — Security ─────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       TF security: protect state, manage secrets, least-privilege, scan IaC with checkov      │   │
│   │   State file contains sensitive values; encrypt at rest (S3 SSE-KMS); restrict S3 bucket ACL  │   │
│   │      Provider auth: OIDC (GitHub Actions → AWS) or IAM role; avoid long-lived access keys     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        State Security       │  │        Code Security        │  │        Auth Security        │   │
│   │    S3 SSE-KMS encryption    │  │        checkov in CI        │  │       OIDC for CI auth      │   │
│   │    S3 Block Public Access   │  │       tflint for lint       │  │     Least-privilege IAM     │   │
│   │      S3 access logging      │  │    No secrets in .tfvars    │  │      No long-lived keys     │   │
│   │     DynamoDB state lock     │  │    Sensitive = true vars    │  │   Sentinel policies (TFC)   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    sensitive = true = marks variable or output as sensitive; redacted in plan/apply output    │   │
│   │    checkov       = scans Terraform configs for security issues: open SGs, no MFA, public S3   │   │
│   │ Sentinel      = HashiCorp policy-as-code; enforces tagging, resource limits, approved regions │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Provider authentication and credential management.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>State backend access control and least privilege.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Secrets management and encrypted state storage.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security scanning, policy enforcement, and compliance.</span>
</a>

</div>
