---
tags:
  - ceph
  - security
---
# Ceph — Security

<!-- diagram:ceph-security -->

<div class="kb-summary">
Ceph security: CephX authentication for all daemon and client communication, RBAC capabilities per user, encryption at rest with dmcrypt, and TLS for RGW S3 endpoints.

*Applies to: Ceph Reef / Squid*
</div>

```text
┌──────────────────────────────────────────── Ceph Security ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     Ceph Security Controls                                    │   │
│   │        Four sub-sections: Access Control (CephX), Authentication, Encryption, Hardening       │   │
│   │            CephX: all clients require a key; granular capabilities per pool/service           │   │
│   │            Encryption: dmcrypt at OSD level; msgr2 secure for in-transit encryption           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Identity & Access               │  │           Data & Network Security           │   │
│   │            CephX shared-secret auth          │  │             OSD dmcrypt encryption          │   │
│   │          Capability per pool/service         │  │            RBD per-image encryption         │   │
│   │               profile rbd preset             │  │              RGW SSE-S3 / SSE-KMS           │   │
│   │             Key rotation (manual)            │  │               msgr2 secure mode             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
```
<div class="kb-grid">
  <a class="kb-card" href="access-control/">
    <span class="kb-card-title">Access Control</span>
    <span class="kb-card-desc">CephX auth users, capabilities, per-pool permissions, admin key management</span>
  </a>
  <a class="kb-card" href="authentication/">
    <span class="kb-card-title">Authentication</span>
    <span class="kb-card-desc">CephX shared secret auth, key distribution, client trust model</span>
  </a>
  <a class="kb-card" href="encryption/">
    <span class="kb-card-title">Encryption</span>
    <span class="kb-card-desc">OSD-level dmcrypt at rest, RBD image encryption, RGW server-side encryption</span>
  </a>
  <a class="kb-card" href="hardening/">
    <span class="kb-card-title">Hardening</span>
    <span class="kb-card-desc">Network firewall rules, disable unused modules, monitoring alerts, CIS controls</span>
  </a>
</div>
