---
tags:
  - aws
  - security
---
# Amazon EVS — Security

<!-- diagram:evs-security -->

<div class="kb-summary">
EVS security controls: AWS IAM for cluster management, vSphere RBAC, NSX-T micro-segmentation, encryption at rest and in transit, and CIS hardening for VCF components.

*Applies to: Amazon EVS*
</div>
![Amazon EVS — Security](../../../../assets/cloud-aws-evs-security-index.svg)


```text
┌───────────────────────────────────────── Amazon EVS Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     EVS Security Controls                                     │   │
│   │      Four sub-sections: Access Control (IAM + vSphere RBAC), Auth, Encryption, Hardening      │   │
│   │        Two RBAC planes: AWS IAM (host/cluster lifecycle) + vSphere RBAC (VM operations)       │   │
│   │          NSX-T DFW: default deny + explicit allow; VPC SGs restrict management access         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Identity & Access               │  │           Data & Network Security           │   │
│   │            AWS IAM scoped policies           │  │           vSAN encryption (NKP/KMS)         │   │
│   │               vSphere RBAC roles             │  │              VM encryption policy           │   │
│   │            AD/LDAP SSO integration           │  │             NSX-T DFW default deny          │   │
│   │              MFA for AWS console             │  │              VPC Flow Logs audit            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
```
<div class="kb-grid">
  <a class="kb-card" href="access-control/">
    <span class="kb-card-title">Access Control</span>
    <span class="kb-card-desc">IAM roles for EVS, vSphere RBAC, SDDC Manager roles, least-privilege design</span>
  </a>
  <a class="kb-card" href="authentication/">
    <span class="kb-card-title">Authentication</span>
    <span class="kb-card-desc">vCenter SSO, LDAP/AD integration, MFA for AWS console, SSH key management</span>
  </a>
  <a class="kb-card" href="encryption/">
    <span class="kb-card-title">Encryption</span>
    <span class="kb-card-desc">vSAN encryption at rest, VM encryption, TLS for VCF APIs, KMS integration</span>
  </a>
  <a class="kb-card" href="hardening/">
    <span class="kb-card-title">Hardening</span>
    <span class="kb-card-desc">NSX-T micro-segmentation, security groups, VPC flow logs, CIS controls</span>
  </a>
</div>

