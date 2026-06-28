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

![Ceph — Security — Diagram](../../../assets/storage-ceph-security-diagram.svg)
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

