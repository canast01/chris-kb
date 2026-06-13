---
tags:
  - dell
  - security
---
# CloudIQ — Access Control


<div class="kb-summary">
CloudIQ role-based access control — user management, RBAC configuration, and access policy enforcement.
</div>

```text
┌──────────────────────────────────── Dell CloudIQ — Access Control ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      CloudIQ RBAC: Admin, Operator, Viewer roles scoped to org, site, or individual array     │   │
│   │       Admin: full config, user management, alert policy, SCG management, and data export      │   │
│   │   Operator: acknowledge/resolve alerts, apply recommendations, view all metrics and reports   │   │
│   │     Viewer: read-only access to health scores, dashboards, and reports; no config changes     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identity verified → role resolved → scope checked → action permitted or denied → logged            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Roles            │  │           Policies          │  │          Governance         │   │
│   │            Admin            │  │       Least privilege       │  │       Quarterly review      │   │
│   │           Operator          │  │       Monitor = Viewer      │  │       Auto-deactivate       │   │
│   │            Viewer           │  │        Ops = Operator       │  │         Named admins        │   │
│   │          Org scope          │  │     Admin = named users     │  │          Access log         │   │
│   │          Site scope         │  │      No shared accounts     │  │         Offboard SOP        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Identity managed in CloudIQ portal or federated via SAML IdP (Okta, Azure AD, Ping)                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Role       │   Permissions    │       Scope       │    Assignment    │   Review Freq    │   │
│   │      Admin       │   Full config    │      Org-wide     │    Named only    │    Quarterly     │   │
│   │     Operator     │   Alert + recs   │     Site/array    │     Ops team     │    Quarterly     │   │
│   │      Viewer      │    Read-only     │     Any scope     │    Monitoring    │      Annual      │   │
│   │    API token     │   Scoped perms   │      Org-wide     │    Automation    │  90-day rotate   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: identity in CloudIQ cloud or federated SAML IdP; no on-prem identity server needed       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RBAC           = Role-Based Access Control; assigns permissions based on role not individual       │
│    Admin role     = Full access: users, alerts, SCG, config, export; limit to 2-3 named people        │
│    Operator role  = Can acknowledge alerts, apply recommendations, and run reports; no user mgmt      │
│    Viewer role    = Read-only; appropriate for monitoring teams and executive dashboards              │
│    Scope          = RBAC can be limited to specific site or array; not just org-wide                  │
│    Least privilege = Assign minimum role needed; default to Viewer, elevate only when justified       │
│    No shared accts = Each engineer has individual login; shared accounts defeat audit trail           │
│    Auto-deactivate = Accounts idle 90 days auto-disabled; re-activation requires admin approval       │
│    Quarterly review = Access list reviewed by storage lead; remove leavers and role mismatches        │
│    Offboard SOP   = Immediate account disable when engineer leaves; token revocation checklist        │
│    Federation     = SAML links corporate IdP; user roles assigned via group attribute mapping         │
│    API token scope = Tokens created with minimum required permissions; not org-admin by default       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [CloudIQ](../../index.md) reference.

---

CloudIQ provides role-based access control to limit what each user can view and modify.

| Role | Permissions |
|---|---|
| CloudIQ Admin | Full access: manage users, roles, notification rules, API credentials, and all system data |
| System Admin | Manage and view assigned systems; cannot manage users or global settings |
| Viewer | Read-only access to dashboards, health scores, capacity, and alerts; cannot modify settings or acknowledge alerts |

Assign roles under **Settings > Users**. Apply the principle of least privilege — most operational users should be Viewer or System Admin; CloudIQ Admin should be restricted to a small number of named individuals.
