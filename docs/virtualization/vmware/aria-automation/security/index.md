---
tags:
  - aria-automation
  - security
  - vmware
---
# Aria Automation — Security

<div class="kb-summary">
Aria Automation hardening — RBAC configuration, endpoint credentials, certificate management, and audit logging.

*Applies to: Aria Automation 8.x*
</div>

```text
┌───────────────────────────────────── Aria Automation — Security ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Workspace ONE/vIDM for SSO; org/project RBAC for catalog and blueprint access control     │   │
│   │   API token management with TTL; approval policies for deployment governance and compliance   │   │
│   │   Secret references for credential storage; Password Locker replaces plaintext in blueprints  │   │
│   │   TLS enforced on all endpoints; cloud account credentials stored encrypted; HTTPS API only   │   │
│   │         Audit log captures all request, catalog, and ABX events for compliance review         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates Aria access · RBAC scopes catalog and blueprints · secrets protect credentials│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │         WS1/vIDM SSO        │  │        Org/proj roles       │  │      TLS all endpoints      │   │
│   │         AD/LDAP intg        │  │         Custom roles        │  │       Secrets at rest       │   │
│   │        API token auth       │  │        Resource-level       │  │       Password Locker       │   │
│   │          OAuth 2.0          │  │       Approval policy       │  │       Cert management       │   │
│   │        Project member       │  │       Catalog entitle       │  │          HTTPS API          │   │
│   │      Break-glass admin      │  │        Cloud zone acc       │  │         Secret refs         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth controls who uses Aria · RBAC limits catalog and blueprint scope                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   vIDM/WS1 SSO   │    Org admin     │    TLS enforced   │  API token TTL   │  Request audit   │   │
│   │     AD/LDAP      │  Project roles   │    Secrets encr   │ Min permissions  │  Catalog events  │   │
│   │    API tokens    │   Custom roles   │  Password Locker  │  Cert rotation   │  ABX log audit   │   │
│   │    OAuth 2.0     │ Approval policy  │     HTTPS only    │   Secret refs    │  Org event log   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VM (Automation appliance) · RAM DIMMs · Network NICs · Identity provider infrastructure          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vIDM (Identity Manager) = VMware Identity Manager; provides SSO for Aria Automation via SAML/OAuth   │
│  Workspace ONE = Broadcom unified endpoint and identity platform; SSO source for Aria Automation      │
│  Organization  = Top-level Aria Automation tenant; all projects and users belong to an organization   │
│  Project       = Aria Automation grouping; scopes cloud zones, members, and catalog entitlements      │
│  RBAC          = Role-based access control; org/project roles control blueprint and catalog access    │
│  API token     = Bearer token for Aria REST API; has configurable TTL; scoped to user role            │
│  Approval policy = Deployment governance requiring approver action before request proceeds            │
│  Entitlement   = Service Broker policy controlling which projects can consume which catalog items     │
│  Password Locker = Aria Automation encrypted credential store; replaces plaintext blueprint passwords │
│  Secret reference = Blueprint reference to Password Locker entry; keeps credentials out of IaC code   │
│  Cloud account credentials = Encrypted vCenter/cloud API keys stored in Aria Automation               │
│  OAuth 2.0     = Token-based authorization protocol; used for Aria API and third-party integrations   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, Workspace ONE Access, and identity sources.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Project-based RBAC, roles, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>TLS certificates, secrets management, and Vault integration.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
