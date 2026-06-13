---
tags:
  - nutanix
  - security
  - access-control
  - rbac
  - prism-central
---
# Nutanix — Access Control

<div class="kb-summary">
Nutanix RBAC in Prism Central — custom roles, categories-based VM access, projects, and self-service permissions. Covers Prism Element built-in roles and the Prism Central fine-grained RBAC model.

*Applies to: AOS 6.x · AHV*
</div>

---

## Before you begin

- **Access:** Prism Central admin (for custom roles, categories, projects); Prism Element admin (for PE built-in role mappings)
- **Requires:** Active Directory integration configured — see [Authentication](authentication/) before setting up role mappings

---

## Access Control Models

| Scope | Mechanism | Where configured |
|---|---|---|
| Prism Element cluster-wide | Built-in roles (Admin/Viewer/UserAdmin) | PE → Settings → Role Mapping |
| Prism Central multi-cluster | Custom roles + entities | PC → Administration → RBAC |
| VM-level self-service | Projects + Calm | PC → Services → Self-Service |
| Categories-based | Category policies | PC → Administration → Categories |

---

## Prism Element Built-In Roles

Three roles — cannot be customised at the PE level:

| Role | Description |
|---|---|
| Cluster Admin | Full access: configure cluster, manage VMs, users |
| User Admin | Add/remove users and role mappings only |
| Viewer | Read-only access to all cluster data |

Assign via directory role mapping (see [Authentication](authentication/)) or for local users:

```text
Prism Element → Settings → Users → Local Users → edit user → assign role
```

---

## Prism Central Custom Roles (Fine-Grained RBAC)

Prism Central lets you create custom roles with specific permissions per entity type.

### Create a Custom Role

```text
Prism Central → Administration → Roles → Create Role
  Name: VM-Operator
  Permissions:
    Virtual Machines: View, Power On/Off, Launch Console
    Volume Groups: View
    Images: View
  (disable everything else)
```

### Assign a Custom Role to Users

```text
Prism Central → Administration → Roles → select role → Manage Assignments
  Add Assignment:
    Users/Groups: infra-vm-ops (AD group)
    Scope: Project (recommended) or Cluster
    Project: Team-A-Project (limits which VMs they can touch)
```

### Permission Categories

Custom roles can grant/deny permissions across:
- **Cluster** — cluster config, hosts, images, storage containers
- **Virtual Machines** — create, delete, update, power, console, clone
- **Volume Groups** — create, attach, detach
- **Categories** — assign, remove
- **Reports** — create, view, export
- **Projects** — view, manage
- **Self Service** — Calm blueprints, marketplace

---

## Categories (Tag-Based Access Control)

Categories are key-value tags applied to VMs, images, and subnets. They are the foundation of policy-based access in Prism Central.

### Create Categories

```text
Prism Central → Administration → Categories → Create Category
  Key: Team
  Values: platform, app-dev, dba
```

### Apply Categories to VMs

```text
Prism Central → VMs → select VMs → Manage Categories
  Team:platform    (assign to infra VMs)
  Team:app-dev     (assign to dev team VMs)
```

```bash
# Apply category via API (or use Calm/PC automation)
# This is typically done through PC UI or Calm blueprints
```

### Use Categories in Role Assignments

```text
Prism Central → Administration → Roles → select role → Manage Assignments
  Add Assignment:
    Group: app-dev-team
    Scope: Category Filter → Team=app-dev
```

App-dev team members can only see and manage VMs tagged `Team=app-dev`.

---

## Projects (Self-Service Workspaces)

Projects group users, quotas, networks, and VMs into isolated workspaces. Used with Calm for self-service provisioning.

### Create a Project

```text
Prism Central → Self Service → Projects → Create Project
  Name: Team-A
  Clusters: allowed clusters
  Subnets: allowed VLANs
  Users: 
    - infra-team (Cluster Admin)
    - app-dev-team (Developer — can deploy from blueprints)
  Quotas:
    vCPU: 200
    Memory: 512 GB
    Storage: 10 TB
```

### Project Roles

| Role | What they can do within the project |
|---|---|
| Project Admin | Full admin within project scope |
| Developer | Deploy Calm blueprints, manage own VMs |
| Consumer | Use deployed apps, no provisioning |
| Operator | Monitor and run day-2 ops on deployed apps |

---

## Audit Logging

All administrative actions in Prism are audit-logged.

```text
Prism Element → Settings → Audit Trails
  Filter by user, time, entity type, and action
  Export audit trail as CSV

Prism Central → Activity → Audit Logs
  Cross-cluster audit log with same filtering
```

```bash
# NCC security audit check
ncc --health_checks audit_log_check 2>/dev/null
```

---

## Verify Access Controls

- Log in with an AD user in each role and confirm they see (and cannot modify) what their role permits
- Confirm category-based scope: `Team:app-dev` user cannot see or power `Team:platform` VMs
- Check project quotas: Prism Central → Projects → select project → Usage tab

---

## See also

- [Nutanix — Authentication](authentication/)
- [Nutanix — Hardening](hardening/)
