---
tags:
  - confluence
  - security
---
# Confluence — Access Control

```text

### Removing Default "All Logged-In Users" Access

Many spaces default to allowing all logged-in users to view and edit. Restrict this for sensitive spaces:

1. Go to **Space Settings** > **Permissions**.
2. Under **Individual Users / Groups**, find the entry for **confluence-users** or **All logged-in users**.
3. Remove or reduce their permissions to View only.
4. Add explicit group entries for editors.

```

```d2
direction: down

auth: "Access Control\nAuthentication" {shape: rectangle}
audit_space_permissions_via_rest_api: "Audit space permissions via REST API" {shape: rectangle}
check_if_any_spaces_allow_anonymous_: "Check if any spaces allow anonymous access via REST API" {shape: rectangle}
then_for_each_space_key_check_for_an: "Then for each space key, check for anonymous\npermissions:" {shape: rectangle}
trigger_manual_ldap_sync_confluence_: "Trigger manual LDAP sync (Confluence admin)" {shape: rectangle}
administration_user_directories_sync: "Administration > User Directories > Synchronise" {shape: rectangle}
or_via_api: "Or via API" {shape: rectangle}
resources: Protected Resources {shape: cylinder}

auth -> audit_space_permissions_via_rest_api: grants
audit_space_permissions_via_rest_api -> resources: access
auth -> check_if_any_spaces_allow_anonymous_: grants
check_if_any_spaces_allow_anonymous_ -> resources: access
auth -> then_for_each_space_key_check_for_an: grants
then_for_each_space_key_check_for_an -> resources: access
auth -> trigger_manual_ldap_sync_confluence_: grants
trigger_manual_ldap_sync_confluence_ -> resources: access
auth -> administration_user_directories_sync: grants
administration_user_directories_sync -> resources: access
auth -> or_via_api: grants
or_via_api -> resources: access
```


```text title="Expected output"
(no output — command completes silently)
```
## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

```bash
## Audit space permissions via REST API
curl -u admin:password \
  "https://confluence.example.local/rest/api/space/INFRA/permission" \
  | python3 -m json.tool
```
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

```text title="Expected output"
{"status":"SYNC_IN_PROGRESS","directory_id":1,"sync_started_at":"2024-01-15T09:42:33.521Z","estimated_completion":"2024-01-15T09:47:33.521Z","users_processed":0,"groups_processed":0}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command to skip SSL verification, or configure proper certificates on confluence.example.local. |
    | `{"errorMessages":["User is not authenticated"],"statusCode":401}` | Verify admin credentials are correct and base64-encoded properly; use `curl -u admin:password` with actual credentials or `-H "Authorization: Basic $(echo -n 'admin:password' | base64)"`. |
    | `{"errorMessages":["Directory with id 1 not found"],"statusCode":404}` | Check the correct directory ID by querying `GET /rest/api/user-directory` first to list all configured directories. |
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

```text title="Expected output"
"username": "admin",
"username": "jsmith",
"username": "kchen",
"username": "mrodriguez",
"username": "admin",
"username": "jsmith",
"username": "kchen",
"username": "agarcia",
"username": "bwilson",
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to curl to skip SSL verification, or import the self-signed certificate into your system's CA bundle. |
    | `jq: command not found` | Install `jq` package (`apt-get install jq` or `yum install jq`) and pipe to `jq '.members[].username'` instead of using `python3 -m json.tool | grep`. |
    | `401 Unauthorized` | Verify the admin credentials are correct and the user has API access enabled in Confluence user permissions. |
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


```text title="Expected output"
{
  "results": [
    {
      "timestamp": 1699564821000,
      "summary": "User permission changed",
      "category": "Permissions",
      "affectedObject": {
        "name": "Engineering Docs",
        "objectType": "Space"
      },
      "changedValues": {
        "permission": "View",
        "user": "jsmith@example.com",
        "granted": true
      }
    },
    {
      "timestamp": 1699551403000,
      "summary": "Space created",
      "category": "Permissions",
      "author": "admin",
      "affectedObject": {
        "name": "Q4-Planning",
        "objectType": "Space"
      }
    }
  ],
  "limit": 100,
  "start": 0
}
2024-11-10 14:32:15,423 ERROR [http-nio-8090-exec-12] [confluence.security.PermissionManager] 403 Permission denied: User 'dchen' lacks VIEW permission on space 'RESTRICTED'
2024-11-10 14:28:42,891 WARN [http-nio-8090-exec-8] [confluence.auth.AccessDenied] Access denied for user 'guest' attempting to edit page 'Security-Policy'
2024-11-10 14:15:09,556 ERROR [http-nio-8090-exec-3] [confluence.security.SpacePermission] 403 Permission denied: Anonymous access blocked for space 'INTERNAL'
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl or import the self-signed certificate into your system's CA bundle. |
    | `jq: parse error: Invalid JSON at line 1` | Verify the Confluence REST API endpoint is accessible and the credentials are correct; check that `python3 -m json.tool` receives valid JSON from curl. |
    | `grep: /var/atlassian/application-data/confluence/logs/atlassian-confluence.log: No such file or directory` | Confirm the Confluence logs directory path matches your installation (may be `/opt/atlassian/confluence/logs/` or check `$CONFLUENCE_HOME`). |
---

## See also

- [Confluence — Authentication](../authentication/)
- [Confluence — Hardening](../hardening/)
- [Confluence — Encryption](../encryption/)
