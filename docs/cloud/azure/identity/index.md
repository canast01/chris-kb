# Azure Identity

<div class="kb-summary">
Azure Identity articles, operational checks, troubleshooting notes, and references.
</div>

```
┌─────────────────────────────────────── Azure Identity Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  Azure Identity — Entra ID, RBAC, Managed Identities, and PIM                 │   │
│   │      Entra ID: cloud identity directory; users, groups, B2B guests, and app registrations     │   │
│   │    RBAC: Owner / Contributor / Reader built-in roles + custom; scope: MG, sub, RG, resource   │   │
│   │Managed Identities: system or user-assigned; auto-managed SP for Azure services to authenticate│   │
│   │      PIM: just-in-time role activation; approval workflow; time-limited privileged access     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Entra ID is the identity source · RBAC grants access · Managed Identities remove secrets · PIM gove│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Entra ID          │  │             RBAC            │  │      Privileged Access      │   │
│   │       Users: UPN + MFA      │  │     Owner: full control     │  │      PIM: JIT activate      │   │
│   │    Groups: security+M365    │  │     Contributor: no RBAC    │  │      Approval: manager      │   │
│   │    App registrations: SPN   │  │      Reader: read-only      │  │     Time-limit: 8 hours     │   │
│   │   Conditional Access: MFA   │  │    Custom roles: JSON def   │  │      Audit: PIM history     │   │
│   │    Managed identities: MI   │  │    Scope: sub/RG/resource   │  │   Access review: quarterly  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Entra ID manages identities · RBAC controls access at scope · PIM governs privileged role assignmen│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Entra ID     │     App Reg.     │        RBAC       │    Managed ID    │       PIM        │   │
│   │   User: create   │   Register app   │    Assign: sub    │  System-assign   │  Activate: JIT   │   │
│   │  Group: add mem  │  Client secret   │     Assign: RG    │   User-assign    │   Approve: MFA   │   │
│   │   MFA: enforce   │  API permission  │    Custom role    │    RBAC to MI    │    Expiry: 8h    │   │
│   │   Cond. Access   │  Enterprise app  │    Review: list   │    No secrets    │  Access review   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Entra ID global service · Azure RBAC control plane · PIM service · ARM token endpoint                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Entra ID         = Microsoft cloud identity directory (formerly Azure AD); users, groups, apps, devic│
│  App registration = Entra ID object representing an application; has client ID, secret or certificate │
│  Service principal= Instance of an app registration in a tenant; has identity and can be assigned role│
│  Managed Identity = Azure-managed service principal; no secrets; system (tied to resource) or user-ass│
│  System-assigned MI= Identity tied to one resource; deleted when resource is deleted; most common patt│
│  User-assigned MI = Standalone identity; assigned to multiple resources; survives resource deletion   │
│  RBAC             = Role-Based Access Control; assigns built-in or custom roles at a defined scope    │
│  RBAC scope       = Hierarchy: Management Group > Subscription > Resource Group > Resource            │
│  PIM              = Privileged Identity Management; manages just-in-time access to sensitive roles    │
│  Conditional Access= Policy evaluating sign-in signals (location, device, risk) to grant, block, or MF│
│  Access review    = Periodic review of group membership or role assignments; remove stale access      │
│  B2B              = Business-to-business; inviting external users (guests) to your Entra ID tenant    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="app-registrations/">
  <strong>App Registrations</strong>
  <span>Service principal registration in Entra ID for application authentication and API access.</span>
</a>

<a class="kb-card" href="conditional-access/">
  <strong>Conditional Access</strong>
  <span>Policy-based access controls enforcing MFA, device compliance, and location restrictions.</span>
</a>

<a class="kb-card" href="enterprise-applications/">
  <strong>Enterprise Applications</strong>
  <span>Gallery and custom app integrations for SSO, provisioning, and access reviews.</span>
</a>

<a class="kb-card" href="entra-id/">
  <strong>Entra ID</strong>
  <span>Microsoft's cloud identity platform (formerly Azure AD) for users, groups, and directory management.</span>
</a>

<a class="kb-card" href="groups/">
  <strong>Groups</strong>
  <span>Security and Microsoft 365 groups for RBAC assignments, licensing, and access governance.</span>
</a>

<a class="kb-card" href="managed-identities/">
  <strong>Managed Identities</strong>
  <span>System- and user-assigned identities for Azure resources to authenticate without credentials.</span>
</a>

<a class="kb-card" href="privileged-identity-management/">
  <strong>Privileged Identity Management</strong>
  <span>Just-in-time privileged role activation with approval workflows and access reviews.</span>
</a>

<a class="kb-card" href="rbac/">
  <strong>RBAC</strong>
  <span>Role-based access control for Azure resources using built-in and custom role assignments.</span>
</a>
</div>
