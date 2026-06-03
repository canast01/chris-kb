# Aria Automation — Access Control


<div class="kb-summary">
Access Control reference covering RBAC Model, Configuring AD Group Role Assignments, Content Sharing (Service Broker), Approval Policies, Reviewing Role Assignments via API and 1 more sections.
</div>

## RBAC Model

Aria Automation uses a **project-based access control** model. All resource provisioning is scoped to a project. Organisation-level roles control platform administration; project-level roles control what users can do within a project.

### Organisation-Level Roles

| Role | Permissions |
|---|---|
| **Administrator** | Full platform access — all projects, all infrastructure, all administration |
| **Member** | Can access projects they are explicitly assigned to; no platform-level administration |

### Project-Level Roles

| Role | Permissions |
|---|---|
| **Owner** | Full control over the project — manage members, cloud zones, quotas, templates, and all deployments |
| **Member** | Request from catalog, manage own deployments, run Day-2 actions on own resources |
| **Viewer** | Read-only access to deployments and catalog items within the project |

---

## Configuring AD Group Role Assignments

Roles are assigned to groups (AD groups synced via VIDM), not individuals.

**Add a group to a project:**

```text
┌────────────────────────────────── Aria Automation — Access Control ───────────────────────────────────┐
│                                                                                                       │
│  vRA access is governed by project membership, catalog entitlements, and approval policies.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Roles and Permissions             │  │             Project Access Model            │   │
│   │        System Admin: full vRA access         │  │      Project member: request+manage own     │   │
│   │      Project Admin: manage one project       │  │     Project Admin: manage members+quotas    │   │
│   │        Member: request catalog items         │  │     Entitlement: catalog item → project     │   │
│   │        Viewer: read-only deployments         │  │    No cross-project visibility by default   │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Entitlements and policies control which users can request and who must approve.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Catalog Entitlements             │  │              Approval Policies              │   │
│   │      Entitle item → user/group/project       │  │        Policy: approver group + level       │   │
│   │     Source: published catalog items only     │  │    Mandatory for prod-tier catalog items    │   │
│   │     Sharing: item accessible across orgs     │  │     Auto-approve: dev/test environments     │   │
│   │      Revoke: remove entitlement record       │  │       Audit: approval decisions logged      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliance · vIDM (user/group source) · AD/LDAP · Postgres (policy store)                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  System Admin      = Global vRA admin role; full access to all projects and configurations            │
│  Project Admin     = Role scoped to one project; manages members, quotas, and entitlements            │
│  Project member    = Can request catalog items and manage own deployments within project              │
│  Viewer role       = Read-only access to deployment status; cannot request or modify                  │
│  Entitlement       = Record linking a catalog item (or source) to a project or user/group             │
│  Catalog source    = Blueprint/Terraform/ABX library shared as catalog item collection                │
│  Approval policy   = Named rule requiring human authorisation before vRA provisions resources         │
│  Approval level    = Single or multi-level; e.g. manager then finance for expensive items             │
│  Auto-approve      = Policy setting for non-prod items; request proceeds without human input          │
│  vIDM group        = AD group synced to vIDM; mapped to vRA project role                              │
│  Cross-project     = Sharing catalog items from one project to another via entitlement                │
│  Audit log         = vRA records who requested, who approved, and timestamps for compliance           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────── Aria Automation — Access Control ───────────────────────────────────┐
│                                                                                                       │
│  vRA access is governed by project membership, catalog entitlements, and approval policies.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Roles and Permissions             │  │             Project Access Model            │   │
│   │        System Admin: full vRA access         │  │      Project member: request+manage own     │   │
│   │      Project Admin: manage one project       │  │     Project Admin: manage members+quotas    │   │
│   │        Member: request catalog items         │  │     Entitlement: catalog item → project     │   │
│   │        Viewer: read-only deployments         │  │    No cross-project visibility by default   │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Entitlements and policies control which users can request and who must approve.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Catalog Entitlements             │  │              Approval Policies              │   │
│   │      Entitle item → user/group/project       │  │        Policy: approver group + level       │   │
│   │     Source: published catalog items only     │  │    Mandatory for prod-tier catalog items    │   │
│   │     Sharing: item accessible across orgs     │  │     Auto-approve: dev/test environments     │   │
│   │      Revoke: remove entitlement record       │  │       Audit: approval decisions logged      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliance · vIDM (user/group source) · AD/LDAP · Postgres (policy store)                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  System Admin      = Global vRA admin role; full access to all projects and configurations            │
│  Project Admin     = Role scoped to one project; manages members, quotas, and entitlements            │
│  Project member    = Can request catalog items and manage own deployments within project              │
│  Viewer role       = Read-only access to deployment status; cannot request or modify                  │
│  Entitlement       = Record linking a catalog item (or source) to a project or user/group             │
│  Catalog source    = Blueprint/Terraform/ABX library shared as catalog item collection                │
│  Approval policy   = Named rule requiring human authorisation before vRA provisions resources         │
│  Approval level    = Single or multi-level; e.g. manager then finance for expensive items             │
│  Auto-approve      = Policy setting for non-prod items; request proceeds without human input          │
│  vIDM group        = AD group synced to vIDM; mapped to vRA project role                              │
│  Cross-project     = Sharing catalog items from one project to another via entitlement                │
│  Audit log         = vRA records who requested, who approved, and timestamps for compliance           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

- Source: select the Assembler content source (or a git-backed content source)
- Target: select the project(s) to share with
- Optionally filter which templates are shared (by name or tag)

---

## Approval Policies

Approval policies add a human approval gate before provisioning.

**Create and assign an approval policy:**

```bash
Service Broker → Content & Policies → Policies → New Policy → Approval Policy
```

Configuration:
- Scope: project-level (all requests in the project) or catalog item-level (specific items)
- Approver groups: AD groups (any member can approve)
- Auto-reject if not approved within: 5 business days

```bash
# List approval policies via API
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/policy/api/policies?type=com.vmware.policy.approval" | \
  jq '.content[] | {name: .name, scope: .scope, approvers: .definition.approvers}'

# List pending approvals
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/approval/api/requests?status=PENDING" | \
  jq '.content[] | {id: .id, requester: .requestedBy, item: .catalogItemName}'
```

---

## Reviewing Role Assignments via API

```bash
# List all organisation-level role assignments
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/csp/gateway/am/api/orgs/<org-id>/role-assignments" | \
  jq '.items[] | {principal: .principal, role: .role}'

# List project membership
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/project-service/api/projects/<project-id>/members" | \
  jq '.members[] | {email: .email, role: .role}'
```

Audit role assignments monthly — remove access for team members who have changed roles or left the organisation.

---

## Least Privilege for Service Accounts

Service accounts used in event broker subscriptions and ABX actions should have the minimum required role:

| Service Account | Role | Purpose |
|---|---|---|
| `svc-vra-api` | Member (specific project) | Automation scripts that query deployments |
| `svc-vra-pipeline` | Owner (specific project) | CI/CD pipeline deployments |
| `svc-vra-monitor` | Viewer (all projects) | Monitoring and audit reporting |
