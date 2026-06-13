---
tags:
  - dell
  - security
---
# APEX Storage as a Service — Security

<div class="kb-summary">
APEX Storage as a Service — Security reference: Authentication, Access Control, Encryption, Hardening.
</div>

```text
┌───────────────────────────────────── Dell Apex STaaS — Security ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Apex security: RBAC roles, AES-256 encryption at rest, CHAP/TLS in transit, audit       │   │
│   │        RBAC: Account Admin (billing/users), Storage Admin (volumes), Reader (view only)       │   │
│   │       Encryption at rest: AES-256 enabled by default on all arrays; no performance cost       │   │
│   │           In-transit: iSCSI CHAP, NFS Kerberos, HTTPS for Apex Console and REST API           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Auth (SSO/SAML) → RBAC role → portal access → storage ops → audit log export                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │          Encryption         │  │            Audit            │   │
│   │          RBAC roles         │  │         AES-256 rest        │  │        Apex audit log       │   │
│   │          SSO / SAML         │  │          iSCSI CHAP         │  │        CloudIQ events       │   │
│   │         MFA required        │  │         NFS Kerberos        │  │         User actions        │   │
│   │        API OAuth 2.0        │  │         TLS 1.2+ API        │  │        Retention 90d        │   │
│   │         IP allowlist        │  │         FC port sec.        │  │         SIEM export         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Dell support access is break-glass; customer must explicitly grant; logged in audit                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │    Mechanism     │       Scope       │      Verify      │      Notes       │   │
│   │       Auth       │   SSO/SAML+MFA   │      Console      │    Login test    │  Local fallback  │   │
│   │      AuthZ       │    RBAC role     │    Per resource   │    Func. test    │   Least priv.    │   │
│   │   Encrypt rest   │     AES-256      │      All data     │    Always on     │    No config     │   │
│   │    Encrypt tx    │     CHAP/TLS     │     iSCSI/API     │   CHAP active    │   Kerberos NFS   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: array self-encrypting drives (SED) · FC fabric binding · iSCSI CHAP per host             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RBAC           = Role-Based Access Control; Apex Console roles control portal operations           │
│    Account Admin  = Manages Apex subscription, billing, and user accounts; no storage ops             │
│    Storage Admin  = Creates/deletes volumes, maps hosts, manages snapshots; no billing                │
│    Reader         = Read-only access to capacity, performance, and configuration data                 │
│    SSO/SAML       = Corporate identity provider integration; single sign-on to Apex Console           │
│    MFA            = Multi-Factor Authentication; required for all Apex Console users                  │
│    OAuth 2.0      = Token-based API authentication; used for automation and integrations              │
│    AES-256        = Advanced Encryption Standard 256-bit; used for self-encrypting drives             │
│    iSCSI CHAP     = Challenge Handshake Auth Protocol; authenticates iSCSI host sessions              │
│    NFS Kerberos   = Kerberos-based authentication for NFS mounts; sec=krb5 mount option               │
│    Break-glass    = Dell emergency support access; requires customer approval; fully audited          │
│    SIEM export    = Audit log forwarding to customer SIEM (Splunk, QRadar) for retention              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="authentication/"><strong>Authentication</strong><span>SSO, LDAP, local accounts, and identity sources.</span></a>
<a class="kb-card" href="access-control/"><strong>Access Control</strong><span>Roles, permissions, and least privilege access.</span></a>
<a class="kb-card" href="encryption/"><strong>Encryption</strong><span>TLS certificate management and data encryption.</span></a>
<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security baselines and compliance configuration.</span></a>
</div>

