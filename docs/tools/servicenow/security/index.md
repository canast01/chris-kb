# ServiceNow — Security



<div class="kb-summary">
ServiceNow — Security reference.
</div>

```
┌───────────────────────────────────────── ServiceNow Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │              Identity & Access               │                                                    │
│   │           SSO via SAML 2.0 / OIDC            │                                                    │
│   │         MFA enforced for all admins          │                                                    │
│   │          Role-based ACLs on tables           │                                                    │
│   │         IP allowlisting per instance         │                                                    │
│   └──────────────────────────────────────────────┘                                                ┴   │
│                                                  ┴  ┌─────────────────────────────────────────────┐   │
│                                                     │               Data Protection               │   │
│                                                     │             TLS 1.2+ all traffic            │   │
│                                                     │         Field-level encryption (FLE)        │   │
│                                                     │           Attachment scanning + AV          │   │
│                                                     │        Audit log every record change        │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Access control → encryption → audit logging → incident response                                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │              Platform Hardening              │                                                    │
│   │           Unused plugins disabled            │                                                    │
│   │            Session timeout 30 min            │                                                    │
│   │           Password policy enforced           │                                                    │
│   │          Update sets change control          │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │              Compliance & Audit             │   │
│                                                     │           SOC 2 Type II certified           │   │
│                                                     │           Audit log export to SIEM          │   │
│                                                     │           Quarterly access reviews          │   │
│                                                     │            Vulnerability scanning           │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS — hosted in ServiceNow datacentres; no on-prem hardware for cloud instances          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ACL        = Access Control List; table/field rules evaluated at read/write time                     │
│  FLE        = Field-Level Encryption; encrypts sensitive fields in DB at rest                         │
│  SAML       = Security Assertion Markup Language; SSO federation protocol                             │
│  MFA        = Multi-Factor Authentication; second factor required at login                            │
│  Update Set = package of config changes; moved between instances via import/export                    │
│  Audit Log  = sys_audit table; records every insert/update/delete with user + timestamp               │
│  IP Allow   = network access policy; restricts instance to approved source IPs                        │
│  SOC 2      = AICPA audit standard; ServiceNow maintains Type II certification                        │
│  SIEM       = Security Information and Event Management; receives audit exports                       │
│  Plugin     = optional ServiceNow capability; disabled plugins reduce attack surface                  │
│  Session    = authenticated user context; timeout enforced to prevent stale sessions                  │
│  Role       = named permission set assigned to users; controls table and form access                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, SAML, and authentication configuration.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, ACLs, and permission management.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data encryption at rest and in transit.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security hardening and compliance settings.</span>
</a>

</div>
