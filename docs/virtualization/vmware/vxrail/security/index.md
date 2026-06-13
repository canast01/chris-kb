---
tags:
  - security
  - vmware
  - vxrail
---
# VxRail — Security

<div class="kb-summary">
Security reference for VxRail in the VMware product context. Covers iDRAC LDAP authentication, ESXi lockdown mode, vSAN encryption, Secure Boot, and access control.

*Applies to: VxRail 7.x / 8.x*
</div>

```text
┌────────────────────────────────────────── VxRail — Security ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         iDRAC LDAP/AD authentication with OOB-only VLAN access for hardware management        │   │
│   │      ESXi lockdown mode (normal) with host profiles enforcement across all cluster nodes      │   │
│   │     vCenter SSO for all management plane access; VxRail Manager TLS certificates enforced     │   │
│   │      vSAN data-at-rest encryption with KMIP-compatible KMS integration for key management     │   │
│   │      Secure Boot on all nodes; STIG alignment via host profiles; syslog forwarded to SIEM     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates hardware access · access control limits management scope                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │        iDRAC LDAP/AD        │  │       RBAC via vCenter      │  │      vSAN data-at-rest      │   │
│   │      ESXi lockdown mode     │  │       iDRAC user roles      │  │       iDRAC HTTPS only      │   │
│   │         vCenter SSO         │  │       VxRail Mgr roles      │  │       Secure Boot ESXi      │   │
│   │       VxRail Mgr local      │  │         LCM op roles        │  │        VxRail Mgr TLS       │   │
│   │          iDRAC 2FA          │  │       Least privilege       │  │        iDRAC SSL cert       │   │
│   │       Svc acct policy       │  │         Audit events        │  │          Syslog TLS         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth controls who accesses hardware · RBAC scopes management                                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │    iDRAC LDAP    │   vCenter RBAC   │    vSAN encrypt   │   Secure Boot    │  vCenter events  │   │
│   │  ESXi lockdown   │   iDRAC roles    │    iDRAC HTTPS    │   SSH disabled   │   iDRAC audit    │   │
│   │   vCenter SSO    │   VxRail roles   │     VxRail TLS    │  Host profiles   │  Syslog to SIEM  │   │
│   │    iDRAC 2FA     │ Least privilege  │   Cert rotation   │    STIG align    │  LCM log audit   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell PowerEdge servers · TPM 2.0 · NVMe/SSD/HDD · iDRAC OOB network · CA infrastructure              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  iDRAC             = Integrated Dell Remote Access Controller; LDAP/AD auth; OOB-only VLAN access     │
│  Lockdown mode     = ESXi host setting preventing direct SSH/DCUI; all management via vCenter only    │
│  vSAN encryption   = Data-at-rest encryption on vSAN datastore; keys managed by external KMIP KMS     │
│  KMS/KMIP          = Key Management Server / protocol; external key store for vSAN and VM encryption  │
│  Secure Boot       = UEFI feature verifying ESXi VIB signatures on all VxRail nodes at boot time      │
│  Host Profile      = vCenter config template enforcing lockdown, NTP, syslog, and security settings   │
│  VxRail Manager TLS = TLS certificate on VxRail Manager VM; used for API and plugin communications    │
│  STIG alignment    = Defense Information Systems Agency hardening guide applied via host profiles     │
│  OOB VLAN          = Out-of-band management VLAN restricted to iDRAC access only; no VM traffic       │
│  LDAP/AD integration = iDRAC and vCenter authenticate against Active Directory for role mapping       │
│  RBAC              = Role-Based Access Control; vCenter roles applied to VxRail management operations │
│  2FA on iDRAC      = Two-factor authentication on iDRAC console; reduces OOB access risk              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">

<div class="kb-card">
<h3><a href="authentication/">Authentication</a></h3>
<p>iDRAC LDAP/AD, VxRail Manager accounts, vCenter SSO, and service account policy.</p>
</div>

<div class="kb-card">
<h3><a href="access-control/">Access Control</a></h3>
<p>RBAC roles, lockdown mode, exception users, and network access scoping.</p>
</div>

<div class="kb-card">
<h3><a href="encryption/">Encryption</a></h3>
<p>vSAN at-rest and in-transit encryption, iDRAC HTTPS, Secure Boot, and TLS.</p>
</div>

<div class="kb-card">
<h3><a href="hardening/">Hardening</a></h3>
<p>Full hardening checklist for VxRail Manager, iDRAC, vSphere, and network.</p>
</div>

</div>

