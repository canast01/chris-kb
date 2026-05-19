# AWS — Security

<div class="kb-summary">
AWS security layers authentication (IAM Identity Center SSO, MFA), encryption (KMS, Secrets Manager, ACM), and threat detection (GuardDuty, Security Hub, Inspector). SCPs provide org-wide preventive guardrails; Config and Security Hub score detective compliance posture.
</div>

```
┌──────────────────────────────────────── AWS Security Overview ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                AWS Security — Authentication, Encryption, and Threat Detection                │   │
│   │ Authentication: IAM Identity Center SSO · MFA enforcement · no shared credentials; roles only │   │
│   │ Encryption: KMS for data-at-rest · ACM for TLS certificates · Secrets Manager for credentials │   │
│   │Threat detection: GuardDuty (ML-based) · Security Hub (posture) · Inspector (vulnerability scan│   │
│   │Preventive guardrails: SCPs limit service/region access · Config rules detect drift · WAF block│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication controls access · Encryption protects data · Threat detection responds to active thr│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │          Encryption         │  │       Threat Detection      │   │
│   │   IAM Identity Center SSO   │  │    KMS: CMK + AWS managed   │  │     GuardDuty: ML threat    │   │
│   │   MFA: virtual or hardware  │  │   Secrets Manager: rotate   │  │     Security Hub: score     │   │
│   │  Roles: no long-lived keys  │  │    ACM: TLS certs managed   │  │   Inspector: CVE scanning   │   │
│   │    SCP: deny root actions   │  │     S3: SSE-S3 / SSE-KMS    │  │   Config: drift detection   │   │
│   │   Access Analyzer: review   │  │   EBS/RDS: encrypt at rest  │  │    WAF: ALB + CloudFront    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Authentication + SCPs prevent access · Encryption protects data · GuardDuty/Hub detect active threa│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Authentication  │  Access Control  │     Encryption    │    Hardening     │ Certificate Mgr  │   │
│   │   SSO: IAM IC    │Roles: least priv │  KMS: CMK create  │  GuardDuty: org  │   ACM: request   │   │
│   │ MFA: enforce all │ SCP: deny risky  │  Secrets: rotate  │   Security Hub   │ Auto-renew: yes  │   │
│   │  No shared keys  │  Boundary: set   │     S3 SSE-KMS    │ Inspector: scan  │  ALB: TLS 1.2+   │   │
│   │  IdP: SAML 2.0   │ Access Analyzer  │   EBS: encrypted  │  Config: rules   │  DNS valid: txt  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS security regions · KMS hardware security modules · CloudFront edge for WAF · TLS endpoint termina│
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  KMS             = Key Management Service; create and manage CMKs for encryption across AWS services  │
│  CMK             = Customer Managed Key; KMS key you control; used for S3, EBS, RDS, Secrets Manager  │
│  Secrets Manager = Manages credentials, API keys, and passwords; auto-rotates via Lambda integration  │
│  ACM             = AWS Certificate Manager; provisions and auto-renews TLS certificates for ALB/CF    │
│  GuardDuty       = ML-based threat detection; analyses CloudTrail, VPC Flow Logs, and DNS logs        │
│  Security Hub    = Aggregates findings; computes security score against CIS, PCI-DSS, AWS Foundational│
│  Inspector       = Automated vulnerability scanner for EC2 OS CVEs and container image vulnerabilities│
│  WAF             = Web Application Firewall; Layer 7 rules for ALB, API Gateway, and CloudFront       │
│  SSE-KMS         = Server-side encryption with KMS CMK; allows key policy + CloudTrail audit of usage │
│  Permission Boundary= IAM policy capping maximum permissions; limits blast radius of over-provisioned │
│  Access Analyzer = IAM service that finds externally-accessible resources; generates least-priv polici│
│  IAM Identity Center= SSO for human access; enforces MFA; integrates with Okta/Azure AD via SAML/SCIM │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

![AWS Security Architecture](../../../assets/aws-security-overview.svg)

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

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security Hub, GuardDuty, Inspector, and AWS security baselines.</span>
</a>

</div>
