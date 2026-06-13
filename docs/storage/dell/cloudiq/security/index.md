---
tags:
  - dell
  - security
---
# CloudIQ — Security

<div class="kb-summary">
CloudIQ — Security reference: Authentication, Access Control, Encryption, Hardening.
</div>

```text
┌─────────────────────────────────────── Dell CloudIQ — Security ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  CloudIQ security: identity access management, data encryption, compliance, and audit logging │   │
│   │    Identity: SSO via SAML 2.0 / OIDC, local accounts, MFA enforcement, RBAC least privilege   │   │
│   │     Data: TLS 1.2+ in transit, AES-256 at rest, tenant isolation, data residency controls     │   │
│   │     Compliance: SOC 2 Type II certified, GDPR controls, audit log export, right-to-delete     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Auth → RBAC check → encrypted data access → action logged → compliance report                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Identity & Access      │  │        Data Security        │  │          Compliance         │   │
│   │        SSO / SAML 2.0       │  │       TLS 1.2+ transit      │  │        SOC 2 Type II        │   │
│   │        Local accounts       │  │       AES-256 at rest       │  │        GDPR controls        │   │
│   │       MFA enforcement       │  │       Tenant isolation      │  │       Audit log export      │   │
│   │          RBAC roles         │  │        Data residency       │  │       Right-to-delete       │   │
│   │      Session management     │  │        SCG cert auth        │  │       Retention policy      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Dell manages cloud infrastructure security; customer manages tenant RBAC and SCG network           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Control      │      Standard     │       Tool       │      Owner       │   │
│   │     Identity     │    MFA + RBAC    │    NIST 800-63    │   CloudIQ IAM    │     Customer     │   │
│   │     Transit      │     TLS 1.2+     │    PCI DSS 4.0    │    SCG/portal    │   Dell + Cust.   │   │
│   │     Storage      │     AES-256      │     FIPS 140-2    │    Cloud KMS     │       Dell       │   │
│   │      Audit       │ Log all actions  │     SOC 2 CC7     │    Audit log     │     Customer     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell cloud infra (AWS/Azure); customer controls SCG placement and RBAC assignments       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SAML 2.0       = Federated SSO protocol; links corporate IdP to CloudIQ for seamless login         │
│    OIDC           = OpenID Connect; OAuth2-based identity layer for modern SSO integrations           │
│    MFA            = Multi-Factor Authentication; TOTP app or email OTP; enforced at org level         │
│    RBAC           = Role-Based Access Control; Admin, Operator, Viewer roles with scoped perms        │
│    Tenant isolation = Each customer org is fully isolated; no cross-tenant data access possible       │
│    Data residency = Customer selects regional CloudIQ endpoint; data stored in chosen geography       │
│    SOC 2 Type II  = Annual third-party audit of Dell cloud security controls; report on request       │
│    GDPR controls  = Dell provides data processing agreement; audit log and deletion tools included    │
│    Right-to-delete = Customer can request deletion of all telemetry data; completed within 30 days    │
│    Audit log      = Immutable record of every portal action; user, timestamp, resource, outcome       │
│    SCG cert auth  = SCG authenticates to CloudIQ using mutual TLS certificate (not password)          │
│    Session mgmt   = Portal sessions expire after 30 min idle; re-auth required; no remember-me        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="authentication/"><strong>Authentication</strong><span>SSO, LDAP, local accounts, and identity sources.</span></a>
<a class="kb-card" href="access-control/"><strong>Access Control</strong><span>Roles, permissions, and least privilege access.</span></a>
<a class="kb-card" href="encryption/"><strong>Encryption</strong><span>TLS certificate management and data encryption.</span></a>
<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security baselines and compliance configuration.</span></a>
</div>
