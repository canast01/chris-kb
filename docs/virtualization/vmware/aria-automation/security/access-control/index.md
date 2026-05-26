# Aria Automation — Access Control

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
Infrastructure → Administration → Projects → select project → Members → Add Members
```

Search for the AD group by name (synced from VIDM), select a role (Owner / Member / Viewer), and save.

| AD Group | Project | Role |
|---|---|---|
| `GG-VRA-Platform-Admins` | (Organisation level) | Administrator |
| `GG-APP-TEAM-LON` | `proj-app-lon-prod` | Owner |
| `GG-APP-TEAM-LON-DEV` | `proj-app-lon-prod` | Member |
| `GG-OPS-READONLY` | All projects | Viewer |

---

## Project Configuration

Projects are the primary isolation boundary in Aria Automation.

**Create a project:**

```text
Infrastructure → Administration → Projects → New Project
```

Configure:
- Name: `proj-app-lon-prod`
- Description: London production application team
- Cloud zones: add target vCenter cloud zones and NSX zones
- Cost limits: set monthly spend limit if integrated with Aria Cost
- Quota: set CPU, memory, and VM count limits to prevent runaway provisioning

**Cloud zone quota example:**

| Resource | Limit |
|---|---|
| VMs | 50 |
| vCPU | 200 |
| Memory | 800 GB |
| Storage | 10 TB |

---

## Content Sharing (Service Broker)

Catalog items are shared to projects — a template not shared to a project is not visible to that project's users.

**Share a catalog item:**

```bash
Service Broker → Content & Policies → Content Sharing → New Content Sharing Policy
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
