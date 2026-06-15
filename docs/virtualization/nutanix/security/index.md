# Nutanix — Security

<div class="kb-summary">
Security configuration for Nutanix HCI — OS hardening, SSH lockdown, Active Directory integration, RBAC access control, and data-at-rest encryption. Aligned with the Nutanix Security Configuration Guide.

*Applies to: AOS 6.x · AHV*
</div>

```text
┌─────────────────────────── Nutanix Security — Hardening and Access Control ───────────────────────────┐
│                                                                                                       │
│  OS hardening, SSH lockdown, AD integration, RBAC, and data-at-rest encryption;                       │
│  aligned with Nutanix Security Configuration Guide.                                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Cluster Hardening               │  │                Access Control               │   │
│   │         Lockdown mode: SSH key-only          │  │        AD: Prism Central integration        │   │
│   │        Port firewall: iptables on CVM        │  │        RBAC: built-in roles + custom        │   │
│   │         STIG: Nutanix STIG available         │  │            MFA: TOTP or SAML IdP            │   │
│   │         NCC: security check plugins          │  │          Audit: user action logging         │   │
│   │          TLS 1.2+ enforced on APIs           │  │          No shared service accounts         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Lockdown mode removes password SSH; key-only access via nutanix or root user.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Data Encryption                │  │               Network Security              │   │
│   │        At-rest: AOS native encryption        │  │          CVM firewall: default-deny         │   │
│   │          KMS: external key manager           │  │             Prism: TLS port 9440            │   │
│   │         SEDs: self-encrypting drives         │  │          Storage: iSCSI/NFS to AHV          │   │
│   │        Instant Secure Erase on retire        │  │         Flow: micro-seg for AHV VMs         │   │
│   │         Backup encryption: PD snaps          │  │         VLAN isolation: mgmt network        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Nutanix nodes with SED option for hardware encryption; separate management VLAN;                     │
│  AD/LDAP reachable from Prism Central on management network.                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Lockdown mode = CVM setting; disables password SSH; key authentication only                          │
│  STIG          = Security Technical Implementation Guide; DoD hardening baseline                      │
│  AOS encryption= software-based at-rest encryption; no special hardware needed                        │
│  SED           = Self-Encrypting Drive; hardware encryption; key managed by KMS                       │
│  KMS           = Key Management Server; external; required for SED management                         │
│  Flow          = Nutanix micro-segmentation; AHV VM network policy enforcement                        │
│  Prism RBAC    = role-based access; Cluster Admin, VM Admin, Monitor built-in                         │
│  SAML IdP      = SSO via Okta/ADFS/Azure AD; Prism Central setting                                    │
│  CVM firewall  = iptables rules on each CVM; default-deny inbound                                     │
│  ISE           = Instant Secure Erase; cryptographic erase on drive retirement                        │
│  NCC security  = NCC plugins: SSH, TLS, open ports, default passwords                                 │
│  Audit log     = Prism Central user activity log; API calls and UI actions                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="hardening/">
    <strong>Hardening</strong>
    <span>CVM OS hardening, SSH lockdown, password policy, TLS configuration, port exposure, and Nutanix SCG alignment.</span>
  </a>
  <a class="kb-card" href="authentication/">
    <strong>Authentication</strong>
    <span>AD/LDAP integration, SAML/SSO for Prism Central, local account management, and session timeout settings.</span>
  </a>
  <a class="kb-card" href="access-control/">
    <strong>Access Control</strong>
    <span>Prism Element built-in roles, Prism Central custom RBAC, categories-based VM access, and projects.</span>
  </a>
  <a class="kb-card" href="encryption/">
    <strong>Encryption</strong>
    <span>Data-at-rest encryption (software and SED), native key manager, KMIP external KMS, and key rotation.</span>
  </a>
</div>
