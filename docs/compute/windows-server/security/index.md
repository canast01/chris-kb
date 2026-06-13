---
tags:
  - security
  - windows
---
# Windows Server — Security



<div class="kb-summary">
Windows Server hardening — security baselines, local admin controls, Windows Firewall, audit policy, and BitLocker configuration.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌───────────────────────────────── Windows Server — Security Overview ──────────────────────────────────┐
│                                                                                                       │
│  Security pillars: identity/access control, auth hardening, encryption, and OS hardening.             │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │        Authentication       │  │          Encryption         │   │
│   │    AD RBAC + local groups   │  │    MFA via Azure AD / Duo   │  │   BitLocker drive encrypt   │   │
│   │   NTFS + Share permissions  │  │    Kerberos + NTLM config   │  │     TLS 1.2/1.3 enforce     │   │
│   │    Protected Users group    │  │    LAPS managed passwords   │  │    EFS for file-level enc   │   │
│   │     PAW for admin access    │  │   Smart card / cert login   │  │    IPsec transport/tunnel   │   │
│   │      JEA constrained PS     │  │    NPS RADIUS for network   │  │       WinRM HTTPS only      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Identity and access form the foundation; encryption protects data at rest and in transit.            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Hardening          │  │      Monitoring & Audit     │  │          Compliance         │   │
│   │    CIS Benchmark baseline   │  │   Security event audit log  │  │      GPO STIG policies      │   │
│   │      Disable SMBv1/NTLM     │  │    Advanced Audit Policy    │  │     SCAP scanning tools     │   │
│   │    AppLocker / WDAC rules   │  │    Event forwarding (WEF)   │  │    Defender ATP policies    │   │
│   │   Credential Guard enable   │  │    SIEM integration logs    │  │     PCI/SOX/HIPAA audits    │   │
│   │   Windows Defender enable   │  │    Logon/logoff tracking    │  │     Vuln scan quarterly     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · TPM 2.0 chip · UEFI Secure Boot · HSM for key storage                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RBAC           = Role-Based Access Control; permissions via AD group membership                      │
│  NTFS           = New Technology File System; supports ACLs, EFS, and auditing                        │
│  LAPS           = Local Admin Password Solution; randomises local admin passwords in AD               │
│  PAW            = Privileged Access Workstation; hardened device for admin tasks only                 │
│  JEA            = Just Enough Administration; PowerShell role-based remoting sessions                 │
│  BitLocker      = Windows full-disk encryption using TPM + PIN or USB key                             │
│  Credential Guard= Virtualisation-based security isolates LSASS credential store                      │
│  CIS Benchmark  = Center for Internet Security hardening baseline for Windows Server                  │
│  STIG           = Security Technical Implementation Guide; DoD hardening standard                     │
│  WEF            = Windows Event Forwarding; centralises events from multiple servers                  │
│  AppLocker      = policy-based app whitelisting; controls which executables run                       │
│  WDAC           = Windows Defender Application Control; kernel-level code integrity                   │
│  Defender ATP   = Microsoft Defender for Endpoint; EDR and threat detection                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Active Directory, local accounts, and authentication configuration.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC, local groups, file permissions, and GPO-based access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>BitLocker, TLS, and encrypted communication.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, CIS benchmarks, and compliance.</span>
</a>

</div>
