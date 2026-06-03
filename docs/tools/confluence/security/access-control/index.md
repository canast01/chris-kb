# Confluence — Access Control


<div class="kb-summary">
Space permissions, page restrictions, group-based access, and least-privilege configuration.
</div>

## Access Control Model

Confluence has two levels of access control:

1. **Space Permissions** — control what users/groups can do within a space (view, edit, create pages, manage space).
2. **Page Restrictions** — control who can view or edit individual pages within a space.

Both are additive: a user must have space permission before page restrictions apply.

```text
┌───────────────────────────────────── Confluence — Access Control ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Confluence Access Control Hierarchy                              │   │
│   │        Global permissions → Space permissions → Page restrictions (most specific wins)        │   │
│   │        Groups managed in LDAP/AD; sync to Confluence; assign to spaces not individuals        │   │
│   │         Page restrictions override space-level view/edit rights for sensitive content         │   │
│   │            Admin role: Confluence Administrators group; limit to 2-3 named accounts           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Access control layers from global to page; most restrictive setting wins                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Global Permissions     │  │      Space Permissions      │  │      Page Restrictions      │   │
│   │      Can use Confluence     │  │          View space         │  │          View only          │   │
│   │        Create spaces        │  │        Add/edit pages       │  │          Edit only          │   │
│   │         Manage users        │  │       Add attachments       │  │       View+Edit combo       │   │
│   │         System admin        │  │         Space admin         │  │         Inheritable         │   │
│   │       Confluence admin      │  │        Export/import        │  │      Child pages apply      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LDAP/AD for group source · Confluence DB stores permission ACLs · IdP for auth                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Global permission = instance-wide rights; set via Admin > Global Permissions                         │
│  Space permission  = per-space ACL; View/AddPages/AddComments/Admin; assign to groups                 │
│  Page restriction  = per-page ACL; overrides space for that page and optionally children              │
│  Inheritance       = page restrictions can cascade to child pages if set during creation              │
│  Group assignment  = best practice is to assign permissions to LDAP groups, not individuals           │
│  Space admin       = can manage space members and page tree; cannot change global settings            │
│  System admin      = full Confluence access including server config and mail settings                 │
│  Confluence admin  = application-level admin; can manage users, plugins, and permissions              │
│  Anonymous access  = global toggle for unauthenticated users; default OFF in enterprise               │
│  Can use Confluence = base permission; must be granted for any user to log in                         │
│  LDAP group sync   = groups from AD mapped to Confluence groups; updated on each poll                 │
│  Audit trail       = Admin > Audit Log records all permission changes with timestamp                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── Confluence — Access Control ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Confluence Access Control Hierarchy                              │   │
│   │        Global permissions → Space permissions → Page restrictions (most specific wins)        │   │
│   │        Groups managed in LDAP/AD; sync to Confluence; assign to spaces not individuals        │   │
│   │         Page restrictions override space-level view/edit rights for sensitive content         │   │
│   │            Admin role: Confluence Administrators group; limit to 2-3 named accounts           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Access control layers from global to page; most restrictive setting wins                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Global Permissions     │  │      Space Permissions      │  │      Page Restrictions      │   │
│   │      Can use Confluence     │  │          View space         │  │          View only          │   │
│   │        Create spaces        │  │        Add/edit pages       │  │          Edit only          │   │
│   │         Manage users        │  │       Add attachments       │  │       View+Edit combo       │   │
│   │         System admin        │  │         Space admin         │  │         Inheritable         │   │
│   │       Confluence admin      │  │        Export/import        │  │      Child pages apply      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LDAP/AD for group source · Confluence DB stores permission ACLs · IdP for auth                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Global permission = instance-wide rights; set via Admin > Global Permissions                         │
│  Space permission  = per-space ACL; View/AddPages/AddComments/Admin; assign to groups                 │
│  Page restriction  = per-page ACL; overrides space for that page and optionally children              │
│  Inheritance       = page restrictions can cascade to child pages if set during creation              │
│  Group assignment  = best practice is to assign permissions to LDAP groups, not individuals           │
│  Space admin       = can manage space members and page tree; cannot change global settings            │
│  System admin      = full Confluence access including server config and mail settings                 │
│  Confluence admin  = application-level admin; can manage users, plugins, and permissions              │
│  Anonymous access  = global toggle for unauthenticated users; default OFF in enterprise               │
│  Can use Confluence = base permission; must be granted for any user to log in                         │
│  LDAP group sync   = groups from AD mapped to Confluence groups; updated on each poll                 │
│  Audit trail       = Admin > Audit Log records all permission changes with timestamp                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Example: IT Infrastructure space (space key: INFRA)
- View: AD group "confluence-infra-viewers"    → All IT staff
- Edit: AD group "confluence-infra-editors"    → Infrastructure engineers
- Admin: AD group "confluence-infra-admins"    → Team lead + wiki admin
```text

### Removing Default "All Logged-In Users" Access

Many spaces default to allowing all logged-in users to view and edit. Restrict this for sensitive spaces:

1. Go to **Space Settings** > **Permissions**.
2. Under **Individual Users / Groups**, find the entry for **confluence-users** or **All logged-in users**.
3. Remove or reduce their permissions to View only.
4. Add explicit group entries for editors.

```bash
## Audit space permissions via REST API
curl -u admin:password \
  "https://confluence.example.local/rest/api/space/INFRA/permission" \
  | python3 -m json.tool
```

## Page Restrictions

Page restrictions limit who can view or edit individual pages, independent of space-level access. They are additive restrictions on top of space permissions.

### Setting Page Restrictions

1. Open the page > **...** (More) > **Restrictions**.
2. Set **Viewing restricted to**: specific users or groups.
3. Set **Editing restricted to**: specific users or groups.

```yaml
When to use page restrictions:
- HR or salary information within a general IT space
- Security incident pages (restricted to Security team)
- Confidential customer data within a project space
- Draft pages not ready for general viewing
```

```text
Avoid over-restricting individual pages — it creates maintenance overhead.
Prefer separate restricted spaces for consistently sensitive content.
```

## Anonymous Access

Anonymous (unauthenticated) access should be disabled in corporate environments.

1. **Global Permissions** > **Anonymous Access** — ensure this is unchecked.
2. **Space Permissions** — for each space, verify Anonymous does not have View permission.

```bash
## Check if any spaces allow anonymous access via REST API
curl -u admin:password \
  "https://confluence.example.local/rest/api/space?limit=50" \
  | python3 -m json.tool | grep "key"

## Then for each space key, check for anonymous permissions:
curl -u admin:password \
  "https://confluence.example.local/rest/api/space/SPACKEY/permission" \
  | python3 -m json.tool | grep -A5 "anonymous"
```

## Confluence Groups and AD Group Sync

Map Confluence groups to Active Directory groups via the LDAP directory configuration.

```yaml
AD Group Design for Confluence:
- GG-Confluence-Users          → Maps to: confluence-users (can log in)
- GG-Confluence-Admins         → Maps to: confluence-administrators
- GG-Confluence-INFRA-Editors  → Maps to: confluence-infra-editors
- GG-Confluence-HR-Viewers     → Maps to: confluence-hr-viewers

These AD groups are managed in Active Directory; membership synced to Confluence via LDAP.
```

```bash
## Trigger manual LDAP sync (Confluence admin)
## Administration > User Directories > Synchronise

## Or via API
curl -u admin:password -X PUT \
  "https://confluence.example.local/rest/api/user-directory/1/sync" \
  -H "Content-Type: application/json"
```

## Least Privilege Review

### Identify Over-Privileged Users

```bash
## List System Administrators
curl -u admin:password \
  "https://confluence.example.local/rest/api/group/confluence-administrators/member?limit=200" \
  | python3 -m json.tool | grep "username"

## List users with Create Space permission
curl -u admin:password \
  "https://confluence.example.local/rest/api/group/confluence-space-creators/member?limit=200" \
  | python3 -m json.tool | grep "username"
```

### Quarterly Access Review Checklist

| Check | Action |
|---|---|
| confluence-administrators group | Remove ex-employees and unnecessary accounts |
| Space admin lists | Confirm only team leads have space admin |
| Sensitive spaces with "All Users" edit | Remove and add explicit editor groups |
| Anonymous access enabled | Verify disabled globally and per-space |
| LDAP sync working | Check last sync timestamp; review errors |
| Inactive user accounts | Disable accounts not logged in for 90+ days |

## Restricting Content by Classification

For environments with formal data classification, map Confluence spaces to data classifications:

| Classification | Space Access Model |
|---|---|
| Public | All authenticated users can view; editors only for editing |
| Internal | All staff can view; team-specific editor groups |
| Confidential | Specific department group can view; no general access |
| Restricted | Named individuals only; page-level restrictions for sub-sections |

## Audit Log — Access Events

```bash
## Confluence audit log records permission changes, space creation, and admin actions
## Administration > Audit Log > Filter by category: Permissions

## Via REST API — filter for permission-related audit events
curl -u admin:password \
  "https://confluence.example.local/rest/api/audit?limit=100" \
  | python3 -m json.tool | grep -B2 -A5 "permission"

## Application log — space access errors (403 events)
grep -i "403\|permission denied\|access denied" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log | tail -20
```

## Quick Reference

| Topic | Location |
|---|---|
| Global permissions | General Configuration > Global Permissions |
| Space permissions | Space Settings > Permissions |
| Page restrictions | Page > ... > Restrictions |
| Anonymous access | General Configuration > Global Permissions > Anonymous Access |
| Group management | User Management > Groups |
| LDAP sync | User Management > User Directories > Synchronise |
| Audit log | Administration > Audit Log |
| Permission API | `GET /rest/api/space/<key>/permission` |
