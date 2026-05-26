---
title: Jira — Access Control
---

# Jira — Access Control

Jira's access control model is layered: global permissions govern what users can do across the entire instance, project permission schemes govern per-project actions, and issue security schemes further restrict who can see individual issues.

---

## Access Control Architecture

```text
Global Permissions
  └── Project Permission Scheme (per project)
        ├── Project Roles (Developer, QA, PM, Viewer)
        └── Issue Security Scheme (per project)
              └── Issue Security Level (per issue)
```
┌──────────────────────────────────────── Jira — Access Control ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Jira Access Control Hierarchy                                 │   │
│   │         Global perms → Permission scheme → Issue security scheme (most specific wins)         │   │
│   │        Groups from LDAP/AD; assign groups to project roles; roles to permission schemes       │   │
│   │       Issue security: hides individual issues from users without assigned security level      │   │
│   │         Jira Admins group: limit to 2-3 named accounts; never use for day-to-day work         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Layers: global → project scheme → issue security; LDAP groups feed project roles                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Global Perms        │  │        Project Perms        │  │        Issue Security       │   │
│   │       Administer Jira       │  │        Browse project       │  │       Security levels       │   │
│   │       Create projects       │  │        Create issues        │  │       Assign to issue       │   │
│   │         Browse users        │  │         Edit issues         │  │        Default level        │   │
│   │        Manage groups        │  │        Admin project        │  │       Restricted level      │   │
│   │       LDAP group sync       │  │         Role members        │  │       Inherited child       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LDAP/AD for group source · Jira DB stores permission ACLs · IdP for auth                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Global permission = instance-wide; Administer Jira, Create Projects, Browse Users                    │
│  Permission scheme = project permission template; assign to one or many projects                      │
│  Issue security    = fine-grained visibility; can hide issues even within same project                │
│  Project role      = named membership group per project (e.g. Developers, Reporters)                  │
│  Role member       = user or group assigned to a role in a specific project                           │
│  LDAP group sync   = groups imported from AD; assign to project roles                                 │
│  Security level    = named tier within issue security scheme; assigned per issue                      │
│  Browse project    = minimum permission to see a project and its issues                               │
│  Admin project     = can manage project settings, components, versions                                │
│  Administer Jira   = full admin rights; can create schemes, users, and projects                       │
│  Issue inherit     = issue security can be inherited from parent issue                                │
│  Audit log         = Admin > Audit Log; records permission and scheme changes                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Critical control:** Remove `jira-software-users` from global Browse Users permission if the user directory is large — it can expose all usernames to every authenticated user.

---

## Project Permission Schemes

Each project uses a permission scheme that maps actions to roles, groups, or users.

### Default Permission Scheme — Hardened Version

| Permission | Grantee |
|---|---|
| Browse Projects | Project Role: Viewer, Developer, QA, PM |
| Create Issues | Project Role: Developer, QA, PM |
| Edit Issues | Project Role: Developer, QA, PM |
| Assign Issues | Project Role: Developer, PM |
| Close Issues | Project Role: Developer, QA, PM |
| Resolve Issues | Project Role: Developer, QA |
| Delete Issues | Project Role: PM |
| Manage Sprints | Project Role: PM |
| View Development Tools | Project Role: Developer |
| Administer Projects | Project Role: PM |
| Transition Issues | Project Role: Developer, QA, PM |
| Schedule Issues | Project Role: PM |
| View Voters and Watchers | Project Role: Developer, QA, PM |
| Manage Watchers | Project Role: PM |

### Creating a Permission Scheme via API

```bash
# Create a new permission scheme
curl -u "admin:TOKEN" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://jira.corp.example.com/rest/api/2/permissionscheme" \
  -d '{
    "name": "Hardened Project Scheme",
    "description": "Least-privilege project permissions",
    "permissions": [
      {
        "permission": "BROWSE_PROJECTS",
        "holder": {"type": "projectRole", "parameter": "Viewer"}
      },
      {
        "permission": "CREATE_ISSUES",
        "holder": {"type": "projectRole", "parameter": "Developer"}
      }
    ]
  }'

# Assign a permission scheme to a project
curl -u "admin:TOKEN" \
  -H "Content-Type: application/json" \
  -X PUT \
  "https://jira.corp.example.com/rest/api/2/project/{projectKey}/permissionscheme" \
  -d '{"id": 10200}'
```

---

## Project Roles

Project Roles define positions within a project (Developer, QA, PM). Users and groups are assigned to roles per-project.

### Standard Role Structure

| Role | Typical Members | Permissions |
|---|---|---|
| Administrators | Project lead, IT admin | Full project admin |
| PM / Project Manager | Product owner | Manage sprints, schedule, delete |
| Developer | Dev team members | Create, edit, transition, view dev tools |
| QA | QA team members | Create, edit, transition, test execution |
| Viewer | Stakeholders, read-only users | Browse only |
| Service Desk Team | SD agents | Service Management specific |

```bash
# List all project roles in an instance
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/role" | jq '.[].name'

# Get role members for a specific project
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/project/{projectKey}/role/{roleId}"

# Add a user to a project role
curl -u "admin:TOKEN" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://jira.corp.example.com/rest/api/2/project/{projectKey}/role/{roleId}" \
  -d '{"user": ["jsmith"]}'

# Add a group to a project role
curl -u "admin:TOKEN" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://jira.corp.example.com/rest/api/2/project/{projectKey}/role/{roleId}" \
  -d '{"group": ["jira-developers"]}'
```

---

## Issue Security Schemes

Issue security schemes restrict which users can view specific issues — used for sensitive tickets (security bugs, HR incidents, executive escalations).

### Security Level Design

| Level | Who Can View | Use Case |
|---|---|---|
| Public (default) | All project members | Standard issues |
| Internal | Staff only (no contractors) | HR-adjacent issues |
| Security | Security team + PM + Reporter | Vulnerability reports |
| Executive | Exec group + PM | Executive escalations |
| Restricted | Reporter + Assignee + PM only | Confidential investigations |

```bash
# Create an issue security scheme
curl -u "admin:TOKEN" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://jira.corp.example.com/rest/api/2/issuesecurityschemes" \
  -d '{
    "name": "Sensitive Issues Security",
    "description": "Restricts visibility of sensitive issues",
    "defaultSecurityLevelId": 10100,
    "levels": [
      {
        "name": "Public",
        "description": "Visible to all project members"
      },
      {
        "name": "Security Team Only",
        "description": "Visible only to security team and PM"
      }
    ]
  }'

# List existing security schemes
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/issuesecurityschemes" | jq '.'
```

---

## Group Management

Maintain AD/LDAP group synchronisation as the source of truth. Avoid manually adding users to Jira-internal groups.

### Recommended Group Structure

```text
AD Group                        → Jira Mapping
──────────────────────────────────────────────
GRP-Jira-Admins                → jira-administrators
GRP-Jira-Users                 → jira-software-users
GRP-Jira-ServiceDesk-Agents    → jira-servicedesk-users
GRP-<ProjectCode>-Developers   → Project role: Developer
GRP-<ProjectCode>-QA           → Project role: QA
GRP-<ProjectCode>-PM           → Project role: PM
```

```bash
# List group members
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/group/member?groupname=jira-administrators"

# Add a user to a group
curl -u "admin:TOKEN" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://jira.corp.example.com/rest/api/2/group/user?groupname=jira-software-users" \
  -d '{"name": "jsmith"}'

# Remove a user from a group
curl -u "admin:TOKEN" \
  -X DELETE \
  "https://jira.corp.example.com/rest/api/2/group/user?groupname=jira-administrators&username=jsmith"
```

---

## Access Audit and Review

```bash
#!/bin/bash
# Audit Jira administrators
JIRA_URL="https://jira.corp.example.com"
TOKEN="admin:API_TOKEN"

echo "=== Jira Administrators ==="
curl -s -u "$TOKEN" \
  "$JIRA_URL/rest/api/2/group/member?groupname=jira-administrators" \
  | jq -r '.values[].displayName'

echo "=== Users with ADMINISTER permission ==="
curl -s -u "$TOKEN" \
  "$JIRA_URL/rest/api/2/user/permission/search?permissions=ADMINISTER&maxResults=100" \
  | jq -r '.[] | "\(.displayName) - \(.emailAddress)"'
```

**Quarterly review checklist:**

- [ ] Verify jira-administrators membership matches approved admin list
- [ ] Review service account activity — disable accounts inactive for 30+ days
- [ ] Audit outside contractor and vendor access — remove expired project access
- [ ] Check projects with "Anyone" or "All logged-in users" in permission schemes
- [ ] Review issue security levels — verify sensitive issues use appropriate levels
- [ ] Confirm LDAP/AD sync is current (no orphaned accounts)
- [ ] Review marketplace app permissions — revoke unused integrations

---

## Automation and Integration Access

### Jira Automation (Cloud)

Jira automation rules run as a service account or as the rule owner. Always use a dedicated service account.

```text
Jira Automation settings → Audit log → View all rule executions
```

**Service account for automation:**
- Minimum permissions: Create Issues, Edit Issues, Transition Issues
- No global admin permissions
- Named clearly: `svc-jira-automation@corp.example.com`

### Application Links (Data Center)

Administration → Application Links — controls OAuth between Jira and Confluence, Bitbucket, Bamboo.

```bash
# List application links
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/applinks/1.0/applicationlink" | jq '.'
```

- Remove application links to decommissioned systems immediately.
- Use OAuth 2.0 (not OAuth 1.0) for new integrations.
- Audit application link permissions annually.

---

## Related Pages

- [Jira — Authentication](../authentication/index.md)
- [Jira — Encryption](../encryption/index.md)
- [Jira — Hardening](../hardening/index.md)
