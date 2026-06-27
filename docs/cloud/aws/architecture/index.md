---
tags:
  - architecture
  - aws
---
# AWS — Architecture

<div class="kb-summary">
Multi-account AWS platform managed through AWS Organizations with SCPs, IAM Identity Center SSO, and Transit Gateway hub-and-spoke networking. All production workloads run in dedicated member accounts; no workloads in the management account.

*Applies to: AWS*
</div>

![AWS — Architecture — Diagram](../../../assets/cloud-aws-architecture-diagram.svg)


![AWS Platform Architecture](../../../assets/aws-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Organizations, IAM Identity Center, Transit Gateway, and SCPs.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>DirectConnect, IdP federation, GuardDuty, and billing integrations.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Account structure, tagging, naming, and security baselines.</span>
</a>

</div>

