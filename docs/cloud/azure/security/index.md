# Azure — Security
```
┌─────────────────────────────────────── Azure Security Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Azure Security — Authentication, Encryption, and Threat Detection               │   │
│   │  Authentication: Entra ID SSO · MFA · Conditional Access · PIM for just-in-time admin access  │   │
│   │   Encryption: Key Vault (keys+secrets+certs) · Customer-Managed Keys · Private Link for PaaS  │   │
│   │ Threat detection: Defender for Cloud (posture + CSPM) · Secure Score · Defender plans per svc │   │
│   │     Network security: NSGs · Azure Firewall in hub · WAF on App Gateway · DDoS Protection     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication controls access · Encryption protects data · Defender detects and remediates threats│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │          Encryption         │  │       Threat Detection      │   │
│   │      Entra ID: SSO+MFA      │  │    Key Vault: keys/certs    │  │      Defender for Cloud     │   │
│   │      Conditional Access     │  │    CMK: storage+SQL+disk    │  │     Secure Score: target    │   │
│   │     PIM: JIT privileged     │  │      TLS: App GW + APIM     │  │     Defender plans: VMs     │   │
│   │    RBAC: least privilege    │  │   Private Link: no pub IP   │  │   Microsoft Sentinel: SIEM  │   │
│   │  Access reviews: quarterly  │  │       Disk: SSE + CMK       │  │   NSG + Firewall: network   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Authentication + RBAC prevent access · Encryption protects data                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Authentication  │  Access Control  │     Encryption    │    Hardening     │    Key Vault     │   │
│   │  Entra ID: SSO   │  RBAC: Contrib   │   KV: key create  │  Defender plans  │   Key: rotate    │   │
│   │  MFA: all users  │  PIM: JIT role   │    CMK: storage   │   Secure Score   │   Secret: get    │   │
│   │   Cond. Access   │  MI: no secret   │   TLS: 1.2+ only  │  Policy: audit   │   Cert: import   │   │
│   │  Access review   │   Custom role    │   Disk: SSE-CMK   │     NSG + FW     │ RBAC: Key Vault  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure HSM for Key Vault · Defender for Cloud backend · Entra ID global service                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Key Vault        = Managed secrets, keys, and certificates; RBAC + access policy; HSM-backed option  │
│  CMK              = Customer-Managed Key; encryption key you control in Key Vault; used for Azure     │
│  SSE              = Server-Side Encryption; Azure encrypts managed disks at rest using PME or CMK     │
│  Private Link     = Private Endpoint mapping PaaS service to VNet IP; eliminates public internet      │
│  Defender for Cloud= CSPM + CWPP; security posture management and workload protection across Azure    │
│  Secure Score     = Numeric score (0-100) of security posture; improvements mapped to recommendations │
│  Defender plans   = Per-resource workload protection: VMs, SQL, Storage, Containers, Key Vault, DNS   │
│  Microsoft Sentinel= Cloud-native SIEM + SOAR; ingests logs, detects threats, automates response      │
│  Conditional Access= Entra ID engine; blocks, MFAs, or allows sign-in based on device, location, risk │
│  PIM              = Privileged Identity Management; JIT admin access with approval and time limits    │
│  TLS validation   = Enforce minimum TLS 1.2 on Storage accounts, App Gateway, and API Management      │
│  Access review    = Periodic audit of who has what access; approvers confirm or remove assignments    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Entra ID, SSO, MFA, Conditional Access, and PIM.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Azure RBAC, management group policies, and service principals.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Key Vault, customer-managed keys, data-at-rest, and Private Link.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Defender for Cloud, Secure Score, NSG hardening, and security baselines.</span>
</a>

</div>
