---
tags:
  - security
  - vmware
  - vsan
  - vsphere-8
---
# vSAN — Security

<div class="kb-summary">
Security reference for VMware vSAN. Covers vCenter SSO authentication, role-based access control, data-at-rest encryption, KMS integration, and hardening baselines aligned to VMware security guidance and DISA STIGs.

*Applies to: vSAN 7.x / 8.x*
</div>

```text
┌─────────────────────────────────────────── vSAN — Security ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ vSAN data-at-rest encryption via external KMS (KMIP); key rotation without data re-encryption │   │
│   │    Host Trust Authority provides TPM-based attestation; ensures only trusted hosts join the   │   │
│   │  vSAN stretched cluster requires authentication between sites; network isolation per segment  │   │
│   │     SPBM security policies enforce encryption and FTT compliance; audit via vCenter events    │   │
│   │   RBAC inherited from vCenter SSO; AD groups map to roles; in-transit encryption on vSAN ESA  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication controls cluster access · access control enforces RBAC                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │       vCenter SSO auth      │  │         vCenter RBAC        │  │       Data-at-rest enc      │   │
│   │        KMS/KMIP intg        │  │       Datastore perms       │  │       KMS provider cfg      │   │
│   │       Host trust auth       │  │      Cluster-level acc      │  │         Key rotation        │   │
│   │        AD group RBAC        │  │     Admin role: vCenter     │  │       In-transit encr       │   │
│   │       Cert management       │  │         Policy RBAC         │  │       vSAN ESA native       │   │
│   │      vSAN stretch auth      │  │         Audit events        │  │       TPM attestation       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth gates cluster membership · RBAC scopes access                                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   vCenter SSO    │   RBAC inherit   │    Data-at-rest   │     KMIP KMS     │  vCenter events  │   │
│   │     KMS/KMIP     │  Datastore perm  │   KMS key rotate  │   TLS vSAN net   │   Policy audit   │   │
│   │ Host trust auth  │    Admin role    │   In-transit enc  │    TPM attest    │    HCL audit     │   │
│   │  AD group RBAC   │ Least privilege  │   ESA native enc  │  Cert rotation   │   SIEM forward   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers with NVMe/SSD/HDD · TPM 2.0 chip · RAM DIMMs · 25GbE NICs · Key Management Server        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  KMS           = Key Management Server; external KMIP-compatible server holding vSAN encryption keys  │
│  KMIP          = Key Management Interoperability Protocol; standard API for integrating external KMS  │
│  Data-at-rest  = vSAN encryption of disk data; enabled cluster-wide; keys held by external KMS        │
│  Host Trust Authority = vSphere service using TPM attestation to verify host integrity before joining │
│  TPM           = Trusted Platform Module; chip providing hardware root of trust for host attestation  │
│  vSAN stretched = Two-site cluster; auth and network isolation between sites required for security    │
│  SPBM          = Storage Policy-Based Management; policies can enforce encryption compliance per VM   │
│  FTT           = Failures To Tolerate; security-relevant as it controls data redundancy level         │
│  Erasure coding = RAID-5/6 in vSAN; distributes parity across hosts; efficient redundancy method      │
│  Key rotation  = Replacing encryption keys without re-encrypting data; shallow vs deep rekey options  │
│  In-transit    = vSAN ESA encrypts data in flight between hosts on the vSAN network layer             │
│  vCenter RBAC  = Role-based access control inherited by vSAN; all datastore access managed via vCenter│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO integration, identity sources, and local accounts.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>vSAN data-at-rest encryption and key management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, compliance, and STIG configuration.</span>
</a>

</div>

