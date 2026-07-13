---
tags:
  - aws
  - security
description: "AWS security layers authentication (IAM Identity Center SSO, MFA), encryption (KMS, Secrets Manager, ACM), and threat detection (GuardDuty, Security Hub..."
---
# AWS — Security

<div class="kb-summary">
AWS security layers authentication (IAM Identity Center SSO, MFA), encryption (KMS, Secrets Manager, ACM), and threat detection (GuardDuty, Security Hub, Inspector). SCPs provide org-wide preventive guardrails; Config and Security Hub score detective compliance posture.

*Applies to: AWS*
</div>

![AWS — Security — Diagram](../../../assets/cloud-aws-security-diagram.svg)

![AWS Security Architecture](../../../assets/aws-security-overview.svg)

![AWS — Security — Diagram](../../../assets/cloud-aws-security-d2.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>IAM Identity Center, SSO, MFA, and federated access.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>IAM roles, policies, SCPs, and permission boundaries.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>KMS, Secrets Manager, data-at-rest, and data-in-transit controls.</span>
</a>

<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security Hub, GuardDuty, Inspector, and AWS security baselines.</span></a>
<a class="kb-card" href="kms/"><strong>KMS</strong><span>Key Management Service — CMK creation, rotation, key policies, and cross-account access.</span></a>
<a class="kb-card" href="secrets-manager/"><strong>Secrets Manager</strong><span>Secret storage, automatic rotation, cross-service access, and audit logging.</span></a>
<a class="kb-card" href="certificate-manager/"><strong>Certificate Manager (ACM)</strong><span>TLS certificate provisioning, auto-renewal, ALB/CloudFront integration, and DNS validation.</span></a>
<a class="kb-card" href="guardduty/"><strong>GuardDuty</strong><span>ML-based threat detection — findings, suppression rules, org enablement, and response.</span></a>
<a class="kb-card" href="inspector/"><strong>Inspector</strong><span>Automated vulnerability scanning for EC2 and container images — CVE findings and remediation.</span></a>
<a class="kb-card" href="security-hub/"><strong>Security Hub</strong><span>Aggregated security findings — CIS/PCI compliance score, finding suppression, and notifications.</span></a>

</div>

