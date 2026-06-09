# AWS — Security

<div class="kb-summary">
AWS security layers authentication (IAM Identity Center SSO, MFA), encryption (KMS, Secrets Manager, ACM), and threat detection (GuardDuty, Security Hub, Inspector). SCPs provide org-wide preventive guardrails; Config and Security Hub score detective compliance posture.
</div>

```text
┌──────────────────────────────────────── AWS Security Overview ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                AWS Security — Authentication, Encryption, and Threat Detection                │   │
│   │ Authentication: IAM Identity Center SSO · MFA enforcement · no shared credentials; roles only │   │
│   │ Encryption: KMS for data-at-rest · ACM for TLS certificates · Secrets Manager for credentials │   │
│   │   Threat detection: GuardDuty (ML-based) · Security Hub (posture) · Inspector (vulnerability  │   │
│   │   Preventive guardrails: SCPs limit service/region access · Config rules detect drift · WAF   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication controls access · Encryption protects data                                          │
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
│    Authentication + SCPs prevent access · Encryption protects data                                    │
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
│  AWS security regions · KMS hardware security modules · CloudFront edge for WAF                       │
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
│  Access Analyzer = IAM service that finds externally-accessible resources; generates least-priv       │
│  IAM Identity Center= SSO for human access; enforces MFA; integrates with Okta/Azure AD via SAML/SCIM │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

![AWS Security Architecture](../../../assets/aws-security-overview.svg)

```text
┌───────────────────── AWS Security Services — Prevention, Detection, and Response ─────────────────────┐
│                                                                                                       │
│    Security services span prevention, detection, and response; many can be centralised.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Prevention Services                      │  │      Detection Services                     │   │
│   │  Shield Standard: free L3/L4 DDoS            │  │  GuardDuty: ML threat detection             │   │
│   │  Shield Advanced: L7 + cost protection       │  │  GuardDuty: CloudTrail+FlowLogs+DNS         │   │
│   │  WAF: Layer 7 rules (ALB/CF/API GW)          │  │  Inspector: EC2 CVE + container scan        │   │
│   │  KMS: CMK key management + encryption        │  │  Macie: S3 PII/sensitive data finding       │   │
│   │  SCP: restrict max perms at OU level         │  │  Config: resource drift + rules eval        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Prevent access and encrypt first; detect threats; respond and investigate.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Monitoring and Audit                     │  │      Aggregation and Response               │   │
│   │  CloudTrail: all API calls logged            │  │  Security Hub: aggregates all findings      │   │
│   │  CloudTrail Org: captures all accounts       │  │  Security Hub: CIS/PCI compliance score     │   │
│   │  Config: inventory + config history          │  │  Detective: graph-based investigation       │   │
│   │  Trusted Advisor: security checks            │  │  Incident Manager: runbooks + alerts        │   │
│   │  Access Analyzer: finds external access      │  │  Systems Manager: patch + run command       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    KMS HSMs · GuardDuty ML infra · CloudFront edge for WAF · CloudTrail S3 storage                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Shield Standard = Free DDoS protection at L3/L4 for all AWS customers                              │
│    Shield Advanced = $3000/mo; L7 DDoS; cost protection; dedicated response team                      │
│    WAF             = Web Application Firewall; rules on ALB/CloudFront/API Gateway                    │
│    GuardDuty       = ML-based threat detection; analyses CloudTrail/VPC logs/DNS                      │
│    Inspector       = Automated CVE scanner for EC2 instances and container images                     │
│    Macie           = Machine learning to discover PII and sensitive data in S3                        │
│    Config          = Resource configuration recorder; evaluates compliance rules                      │
│    Security Hub    = Aggregates GuardDuty/Inspector/Macie/Config findings; scores                     │
│    Detective       = Investigates security incidents using graph analysis of logs                     │
│    KMS CMK         = Customer Managed Key; full control; CloudTrail logs all usage                    │
│    Access Analyzer = Identifies resources accessible from outside the account                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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


