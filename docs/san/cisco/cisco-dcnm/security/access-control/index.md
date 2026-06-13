---
tags:
  - san
  - security
---
# Cisco DCNM — Access Control


<div class="kb-summary">
Access Control reference covering Overview, Built-In Roles, Fabric-Level Scoping, LDAP Group to Role Mapping, Service Account Configuration and 2 more sections.
</div>

```text
┌───────────────────────────────────── Cisco DCNM — Access Control ─────────────────────────────────────┐
│                                                                                                       │
│  DCNM access control: RBAC roles, ISE TACACS+, LDAP group mapping, API token scoping.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             User Accounts & RBAC             │  │          Remote Auth (ISE/TACACS+)          │   │
│   │         Built-in: network-admin/oper         │  │           Cisco ISE TACACS+ server          │   │
│   │         Custom roles via role config         │  │          Role map: privilege level          │   │
│   │        Local accounts: emergency only        │  │           RADIUS: fallback option           │   │
│   │         Account lockout: 5 attempts          │  │          Auth order: TACACS+ first          │   │
│   │        Per-fabric access restriction         │  │          Audit: all actions logged          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  RBAC and ISE TACACS+ enforce least privilege; local accounts reserved for break-glass.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              API Access Control              │  │          Management Access Control          │   │
│   │         REST API: token scoped role          │  │             HTTPS only: port 443            │   │
│   │           API key: service account           │  │          IP whitelist: src restrict         │   │
│   │          Token expiry: configurable          │  │           Session timeout: 30 min           │   │
│   │          Rate limiting: brute-force          │  │            Out-of-band: mgmt VLAN           │   │
│   │          Scope: read vs read-write           │  │            MFA: SAML SSO enforced           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM VM · Cisco ISE appliance · LDAP/AD server · management VLAN                                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RBAC            = Role-Based Access Control; network-admin/operator/read-only in DCNM                │
│  ISE             = Cisco Identity Services Engine; TACACS+ and RADIUS provider                        │
│  TACACS+         = Terminal Access Controller; centralised CLI+GUI auth with audit                    │
│  Privilege level = TACACS+ maps to DCNM role (15=admin, 5=operator, 1=read-only)                      │
│  Auth order      = DCNM tries TACACS+ first, then RADIUS, then local fallback                         │
│  Per-fabric RBAC = restrict operators to specific SAN fabrics; not all                                │
│  API token       = JWT; inherits role permissions of the user who logged in                           │
│  Service account = dedicated API user; separate from human admin accounts                             │
│  IP whitelist    = source IP restriction for DCNM management and REST API access                      │
│  Session timeout = idle GUI/API session terminated after 30 minutes                                   │
│  SAML SSO        = DCNM integrates with IdP; MFA enforced at identity provider                        │
│  Audit log       = all DCNM GUI and API actions logged with user and timestamp                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
