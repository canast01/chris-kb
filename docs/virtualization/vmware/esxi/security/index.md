# ESXi — Security

<div class="kb-summary">
Security reference for VMware ESXi. Covers vCenter SSO authentication, lockdown mode, role-based access control, VM and vSAN encryption, and host hardening aligned to VMware security guidance and DISA STIGs.
</div>

```
┌─────────────────────────────────────────── ESXi — Security ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      ESXi security layers: authentication, access control, encryption, and host hardening     │   │
│   │Authentication: all management via vCenter SSO; direct host login via DCUI for break-glass only│   │
│   │   Access: lockdown mode (normal/strict) restricts direct access; RBAC inherited from vCenter  │   │
│   │  Encryption: VM encryption via vSAN/storage policy; vMotion encrypted; vTPM per VM supported  │   │
│   │    Hardening: DISA STIG / VMware Security Guide baseline; SSH disabled; secure boot enabled   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates access · lockdown mode enforces vCenter-only management                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │     vCenter SSO: primary    │  │   Lockdown: normal/strict   │  │     VM encrypt: KMS/KMIP    │   │
│   │    DCUI: break-glass only   │  │      RBAC from vCenter      │  │      vMotion: encrypted     │   │
│   │    Local root: min 1 acct   │  │   Firewall: service rules   │  │      vTPM: per-VM chip      │   │
│   │     SSH: disabled by std    │  │     Shell: time-limited     │  │      Secure boot: UEFI      │   │
│   │     MFA: via vCenter SSO    │  │     Syslog: to vRLI/SIEM    │  │    vSAN encrypt: at rest    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Authentication controls who logs in · access control limits what they can do                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   vCenter SSO    │  Lockdown mode   │   VM encryption   │   SSH disabled   │  Syslog to SIEM  │   │
│   │ DCUI breakglass  │   RBAC inherit   │    vMotion encr   │  Secure boot on  │  vCenter events  │   │
│   │  Local root: 1   │  Host FW rules   │    vTPM per VM    │   Shell: timed   │  Firewall audit  │   │
│   │   SSH key auth   │ Shell access log │   KMS/KMIP keys   │ DISA STIG align  │ Host log review  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server · TPM 2.0 chip · UEFI firmware · iDRAC/iLO OOB management · Physical access controls      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Lockdown mode  = Host setting preventing direct access; all management must go through vCenter       │
│  DCUI           = Direct Console User Interface; physical/IPMI console on ESXi host; break-glass      │
│  vTPM           = Virtual Trusted Platform Module; per-VM emulated TPM 2.0 for BitLocker and          │
│  KMS            = Key Management Server; external KMIP-compatible server for VM encryption keys       │
│  KMIP           = Key Management Interoperability Protocol; standard API for KMS integration          │
│  Secure Boot    = UEFI feature verifying ESXi VIB signatures; prevents loading unsigned modules       │
│  vMotion encrypt = AES-256 encryption of vMotion traffic between ESXi hosts in vCenter 6.5+           │
│  SSH            = Secure Shell; direct host CLI access; should be disabled per security baseline      │
│  ESXi firewall  = Host-based firewall; rules control which services/IPs can reach VMkernel ports      │
│  DISA STIG      = Defense Information Systems Agency Security Technical Implementation Guide for ESXi │
│  Host profile   = Configuration template that enforces security settings consistently across all hosts│
│  Syslog         = ESXi log forwarding to vRLI or external SIEM; configured via esxcli or host profile │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────────── ESXi — Security ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      ESXi security layers: authentication, access control, encryption, and host hardening     │   │
│   │Authentication: all management via vCenter SSO; direct host login via DCUI for break-glass only│   │
│   │   Access: lockdown mode (normal/strict) restricts direct access; RBAC inherited from vCenter  │   │
│   │  Encryption: VM encryption via vSAN/storage policy; vMotion encrypted; vTPM per VM supported  │   │
│   │    Hardening: DISA STIG / VMware Security Guide baseline; SSH disabled; secure boot enabled   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates access · lockdown mode enforces vCenter-only management                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │     vCenter SSO: primary    │  │   Lockdown: normal/strict   │  │     VM encrypt: KMS/KMIP    │   │
│   │    DCUI: break-glass only   │  │      RBAC from vCenter      │  │      vMotion: encrypted     │   │
│   │    Local root: min 1 acct   │  │   Firewall: service rules   │  │      vTPM: per-VM chip      │   │
│   │     SSH: disabled by std    │  │     Shell: time-limited     │  │      Secure boot: UEFI      │   │
│   │     MFA: via vCenter SSO    │  │     Syslog: to vRLI/SIEM    │  │    vSAN encrypt: at rest    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Authentication controls who logs in · access control limits what they can do                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   vCenter SSO    │  Lockdown mode   │   VM encryption   │   SSH disabled   │  Syslog to SIEM  │   │
│   │ DCUI breakglass  │   RBAC inherit   │    vMotion encr   │  Secure boot on  │  vCenter events  │   │
│   │  Local root: 1   │  Host FW rules   │    vTPM per VM    │   Shell: timed   │  Firewall audit  │   │
│   │   SSH key auth   │ Shell access log │   KMS/KMIP keys   │ DISA STIG align  │ Host log review  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server · TPM 2.0 chip · UEFI firmware · iDRAC/iLO OOB management · Physical access controls      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Lockdown mode  = Host setting preventing direct access; all management must go through vCenter       │
│  DCUI           = Direct Console User Interface; physical/IPMI console on ESXi host; break-glass      │
│  vTPM           = Virtual Trusted Platform Module; per-VM emulated TPM 2.0 for BitLocker and          │
│  KMS            = Key Management Server; external KMIP-compatible server for VM encryption keys       │
│  KMIP           = Key Management Interoperability Protocol; standard API for KMS integration          │
│  Secure Boot    = UEFI feature verifying ESXi VIB signatures; prevents loading unsigned modules       │
│  vMotion encrypt = AES-256 encryption of vMotion traffic between ESXi hosts in vCenter 6.5+           │
│  SSH            = Secure Shell; direct host CLI access; should be disabled per security baseline      │
│  ESXi firewall  = Host-based firewall; rules control which services/IPs can reach VMkernel ports      │
│  DISA STIG      = Defense Information Systems Agency Security Technical Implementation Guide for ESXi │
│  Host profile   = Configuration template that enforces security settings consistently across all hosts│
│  Syslog         = ESXi log forwarding to vRLI or external SIEM; configured via esxcli or host profile │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, LDAP, local accounts, and identity sources.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, lockdown mode, and least privilege.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>VM encryption, vSAN encryption, and key management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Host hardening, STIG compliance, and security baselines.</span>
</a>

</div>
