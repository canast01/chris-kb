---
tags:
  - security
---
# OpenShift — Security

<div class="kb-summary">
OpenShift security: RBAC, OAuth identity providers, etcd encryption, pod security admission, SCC, and CIS hardening. Enterprise security controls built into the platform.

*Applies to: OpenShift 4.x*
</div>

```text
┌───────────────────────────────────────── OpenShift Security ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  OpenShift Security Controls                                  │   │
│   │        Four sub-sections: Access Control (RBAC), Authentication, Encryption, Hardening        │   │
│   │            SCC enforcement: default restricted-v2; deny root; drop all capabilities           │   │
│   │     RBAC + OAuth: role bindings per namespace; LDAP, HTPasswd, or OIDC identity providers     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Identity & Access               │  │              Platform Hardening             │   │
│   │           RBAC Roles + ClusterRoles          │  │           SCC: restricted-v2 default        │   │
│   │            OAuth identity providers          │  │              PSA namespace labels           │   │
│   │                LDAP group sync               │  │            etcd encryption at rest          │   │
│   │             Service account tokens           │  │           NetworkPolicy default deny        │   │
│   │            Remove kubeadmin secret           │  │             CIS benchmark controls          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
```
<div class="kb-grid">
  <a class="kb-card" href="access-control/">
    <span class="kb-card-title">Access Control</span>
    <span class="kb-card-desc">RBAC, groups, service accounts, and project isolation</span>
  </a>
  <a class="kb-card" href="authentication/">
    <span class="kb-card-title">Authentication</span>
    <span class="kb-card-desc">OAuth server, LDAP, HTPasswd, and OpenID Connect identity providers</span>
  </a>
  <a class="kb-card" href="encryption/">
    <span class="kb-card-title">Encryption</span>
    <span class="kb-card-desc">etcd encryption at rest, secret management, and TLS certificate rotation</span>
  </a>
  <a class="kb-card" href="hardening/">
    <span class="kb-card-title">Hardening</span>
    <span class="kb-card-desc">SCC, pod security admission, CIS benchmark, and audit logging</span>
  </a>
</div>

