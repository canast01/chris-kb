# Horizon (VDI) — Security

```text
┌───────────────────────────────────────── Horizon — Security ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Active Directory authentication; MFA via RSA SecurID/RADIUS or SAML with Workspace ONE    │   │
│   │      Certificate management for Connection Servers and UAG; Horizon RBAC for entitlements     │   │
│   │       Blast Extreme and PCoIP traffic encrypted with TLS 1.2+; smart card auth supported      │   │
│   │    UAG performs certificate passthrough; Connection Server validates AD credentials and MFA   │   │
│   │      App Volumes and DEM file encryption; USB policy enforces device restriction per pool     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates user access · RBAC controls entitlements                                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │       AD auth primary       │  │         Horizon RBAC        │  │        Blast TLS 1.2+       │   │
│   │        RSA/RADIUS MFA       │  │       AD group entitle      │  │          PCoIP TLS          │   │
│   │         SAML/WS1 SSO        │  │       Pool permissions      │  │         Cert CS/UAG         │   │
│   │       Smart card auth       │  │      Global admin role      │  │         App Vol cert        │   │
│   │       Cert-based auth       │  │        Help desk role       │  │        DEM file encr        │   │
│   │       UAG passthrough       │  │         Audit events        │  │          USB policy         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth controls who connects · access control limits entitlements                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │     AD auth      │   RBAC entitle   │     Blast TLS     │  Cert rotation   │   CS event log   │   │
│   │     RSA MFA      │   Pool access    │     PCoIP TLS     │   MFA enforce    │  Session audit   │   │
│   │     SAML/WS1     │    Admin role    │    CS/UAG cert    │    Smart card    │  UAG access log  │   │
│   │    Smart card    │  Help desk role  │    App Vol cert   │  Lockout policy  │  Entitle audit   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 ESXi hosts · GPU cards · RAM DIMMs · Network NICs · UAG VMs · RSA/MFA server · AD domain         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Blast Extreme      = VMware display protocol; encrypted with TLS 1.2+; supports H.264 and H.265      │
│  PCoIP              = PC-over-IP display protocol; TLS-encrypted tunnel between client and UAG        │
│  UAG (Unified Access Gateway) = DMZ proxy performing cert passthrough and MFA pre-authentication      │
│  RSA SecurID        = RADIUS-based MFA token server integrated with Connection Server                 │
│  SAML               = Security Assertion Markup Language; enables WS1 Access SSO for Horizon          │
│  Smart card auth    = PIV/CAC card authentication via Connection Server or UAG                        │
│  Connection Server certificate = TLS cert on CS for Blast/PCoIP and admin UI; must be CA-signed       │
│  Entitlement        = Assignment of AD user or group to a Horizon desktop or application pool         │
│  RBAC               = Role-Based Access Control in Horizon Admin console; admin, helpdesk, auditor    │
│  Help desk role     = Horizon RBAC role allowing session management without pool administration       │
│  DEM (Dynamic Environment Manager) = User settings manager; supports file encryption for profiles     │
│  Session audit      = Horizon event DB records all session start, disconnect, and logoff events       │
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
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data encryption and certificate management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
