# Ceph — Security

<!-- diagram:ceph-security -->

<div class="kb-summary">
Ceph security: CephX authentication for all daemon and client communication, RBAC capabilities per user, encryption at rest with dmcrypt, and TLS for RGW S3 endpoints.
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
│  Key terms:                                                                                           │
│                                                                                                       │
│  CephX         = Ceph's shared-secret authentication protocol; all daemons and clients use it         │
│  capability    = CephX permission string: allow r/rw/* per service (mon, osd, mds) and pool           │
│  client.admin  = CephX superuser key; full cluster access; protect and rotate regularly               │
│  dmcrypt       = Linux kernel block device encryption used for OSD at-rest encryption                 │
│  msgr2 secure  = Ceph messenger v2 encryption mode; encrypts OSD-to-OSD and client traffic            │
│  RBD encrypt   = Per-image client-side encryption; LUKS key managed in client keyring                 │
│  SSE-KMS       = RGW server-side encryption with external KMS (Vault); per-object or per-bucket       │
│  profile rbd   = Pre-defined CephX capability preset granting pool-level RBD access                   │
│  keyring       = File holding CephX shared secret: /etc/ceph/ceph.client.<name>.keyring               │
│  MON keyring   = Master authentication database on MON nodes; only cephadm should write this          │
│  pg_autoscaler = MGR module; disable in production to prevent unplanned PG count changes              │
│  firewalld     = Linux firewall; restrict cluster-network ports to Ceph nodes only                    │
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
