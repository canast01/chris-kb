---
tags:
  - confluence
  - operations
---
# Confluence — Operations Procedures

```bash
# Create a page via REST API
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/wiki/rest/api/content" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "page",
    "title": "My New Page",
    "space": {"key": "ENG"},
    "ancestors": [{"id": "12345"}],
    "body": {
      "storage": {
        "value": "<p>Page content here</p>",
        "representation": "storage"
      }
    }
  }'

# Update an existing page (increment version number)
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345" \
  -H "Content-Type: application/json" \
  -d '{"version":{"number":4},"type":"page","title":"Updated Title","body":{"storage":{"value":"<p>New content</p>","representation":"storage"}}}'
```


```text title="Expected output"
{
  "id": "98765",
  "type": "page",
  "title": "My New Page",
  "space": {
    "id": 45821,
    "key": "ENG",
    "name": "Engineering"
  },
  "ancestors": [
    {
      "id": "12345",
      "type": "page",
      "title": "Parent Page"
    }
  ],
  "version": {
    "by": {
      "username": "user",
      "userKey": "557058:a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    },
    "when": "2024-01-15T09:42:18.523Z",
    "number": 1
  },
  "links": {
    "webui": "/wiki/spaces/ENG/pages/98765/My+New+Page"
  }
}
{
  "id": "12345",
  "type": "page",
  "title": "Updated Title",
  "version": {
    "number": 4,
    "when": "2024-01-15T09:43:22.891Z"
  }
}
```

!!! warning "Common errors"
    **`{"statusCode":401,"data":{"authorized":false,"valid":true,"errors":["AUTHENTICATION_DENIED"]}}`** — Verify the API token is valid and has not expired; regenerate it in Confluence user settings if needed.
    **`{"statusCode":404,"data":{"authorized":true,"valid":true,"errors":["The content with id 12345 does not exist or you do not have permission to see it."]}}`** — Confirm the page ID exists and your user account has edit permissions on that page in the target space.
    **`{"statusCode":409,"data":{"authorized":true,"valid":true,"errors":["Conflict: The version number you provided does not match the current version."]}}`** — Fetch the current page version number using a GET request before updating, then increment it by one in the PUT request.
```bash
# Get current restrictions
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/restriction"

# Add a view restriction for a specific group
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/restriction/byOperation/read/group/developers"

# Remove all restrictions (inherit from space)
curl -u user:token -X DELETE \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/restriction"
```

```text title="Expected output"
{
  "read": {
    "restrictions": [
      {
        "type": "group",
        "name": "confluence-users",
        "key": "confluence-users"
      }
    ],
    "content": {
      "id": "12345",
      "type": "page",
      "title": "Operations Runbook"
    }
  },
  "update": {
    "restrictions": [],
    "content": {
      "id": "12345",
      "type": "page"
    }
  }
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`{"statusCode":401,"message":"Authentication failed; invalid username, password, or token."}`** — Verify the API token is valid and has not expired; regenerate in Atlassian account settings if needed.
    **`{"statusCode":404,"message":"The content with id 12345 could not be found."}`** — Confirm the page ID is correct by checking the page URL or using the Confluence API to list content IDs.
    **`{"statusCode":403,"message":"You do not have permission to restrict this content."}`** — Ensure your user account has Edit permissions on the page and Admin role in the space.
```bash
# Watch a page (receive change notifications)
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/wiki/rest/api/user/watch/content/12345"

# Unwatch
curl -u user:token -X DELETE \
  "https://your-instance.atlassian.net/wiki/rest/api/user/watch/content/12345"

# List watchers of a page
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/notification/child-created"
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
{
  "results": [
    {
      "type": "user",
      "user": {
        "type": "known",
        "username": "jsmith",
        "userKey": "ff8080814d8a0d4f014d8a1234567890",
        "fullName": "John Smith",
        "email": "jsmith@company.com"
      }
    },
    {
      "type": "user",
      "user": {
        "type": "known",
        "username": "mchen",
        "userKey": "ff8080814d8a0d4f014d8a9876543210",
        "fullName": "Maria Chen",
        "email": "mchen@company.com"
      }
    }
  ],
  "start": 0,
  "limit": 25,
  "size": 2
}
```

!!! warning "Common errors"
    **`401 Unauthorized`** — Verify your Confluence API token is valid and base64-encoded correctly in the `-u user:token` parameter.
    **`404 Not Found`** — Confirm the page ID (12345) exists and you have permission to access it; use `GET /content` to list available pages.
    **`403 Forbidden`** — Ensure your user account has the required permissions to watch content or view watchers in the space.
```bash
# Archive a single page via REST API
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345" \
  -H "Content-Type: application/json" \
  -d '{"version":{"number":3},"type":"page","status":"archived"}'

# List all archived pages in a space
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content?spaceKey=ENG&status=archived&limit=50"
```

```text title="Expected output"
{"id":"12345","type":"page","status":"archived","title":"Legacy Deployment Guide","version":{"number":3,"when":"2024-01-15T09:42:31.000Z","by":{"username":"admin","userKey":"557058:a1b2c3d4-e5f6-7890-abcd-ef1234567890"}},"space":{"id":98765,"key":"ENG","name":"Engineering"},"links":{"self":"https://your-instance.atlassian.net/wiki/rest/api/content/12345"}}

{"results":[{"id":"12345","type":"page","status":"archived","title":"Legacy Deployment Guide","version":{"number":3}},{"id":"12346","type":"page","status":"archived","title":"Old Runbook v2.1","version":{"number":5}},{"id":"12347","type":"page","status":"archived","title":"Deprecated API Docs","version":{"number":2}},{"id":"12348","type":"page","status":"archived","title":"2022 Infrastructure Plan","version":{"number":4}}],"limit":50,"size":4,"start":0}
```

!!! warning "Common errors"
    **`{"statusCode":401,"data":{"authorized":false,"valid":false,"errors":["INVALID_USER_OR_PASSWORD"]}}`** — Verify the API token is valid and has not expired; regenerate it in your Atlassian account settings if needed.
    **`{"statusCode":403,"data":{"authorized":true,"valid":true,"errors":["You do not have permission to modify this page"]}}`** — Ensure your user account has Edit or Admin permissions on the target page or space.
    **`{"statusCode":404,"data":{"errors":["Could not find content with id 12345"]}}`** — Confirm the page ID exists and has not already been deleted; retrieve the correct ID from the page URL or via a content search API call.
```bash
# Find pages with no parent using CQL in Advanced Search:
# space = "ENG" AND ancestor = null AND status = current

# Via API — fetch pages and filter for empty ancestors
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content?spaceKey=ENG&expand=ancestors&limit=100" \
  | jq '.results[] | select(.ancestors == []) | {id, title}'
```

```text title="Expected output"
{
  "id": "327680",
  "title": "Engineering Standards"
}
{
  "id": "327681",
  "title": "On-Call Procedures"
}
{
  "id": "327682",
  "title": "Incident Response Runbook"
}
{
  "id": "327683",
  "title": "Infrastructure Deployment Guide"
}
{
  "id": "327684",
  "title": "Network Architecture Overview"
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to your-instance.atlassian.net port 443: Name or service not known`** — Replace `your-instance` with your actual Confluence domain name (e.g., `company.atlassian.net`).
    **`jq: parse error: Invalid JSON text at line 1`** — Verify the API token is valid and the user has API access enabled; expired or revoked tokens return HTML error pages instead of JSON.
    **`401 Unauthorized`** — Ensure the user account and API token are correct; regenerate the token in Atlassian account settings if authentication fails.
```bash
# Delete a page by ID
curl -u user:token -X DELETE \
  "https://your-instance.atlassian.net/wiki/rest/api/content/67890"

# Move multiple pages to a new parent
for PAGE_ID in 111 222 333; do
  curl -u user:token -X PUT \
    "https://your-instance.atlassian.net/wiki/rest/api/content/${PAGE_ID}/move/append/TARGET_ID"
done

# Export a page list to CSV for review
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content?spaceKey=ENG&limit=200&expand=version,ancestors" \
  | jq -r '.results[] | [.id, .title, .version.when] | @csv' > space_audit.csv
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
$ cat space_audit.csv
"67890","Getting Started with Kubernetes","2024-01-15T09:23:45.000Z"
"67891","Network Configuration Guide","2024-01-14T14:52:12.000Z"
"67892","Disaster Recovery Procedures","2024-01-13T11:08:33.000Z"
"67893","On-Call Runbook","2024-01-12T16:45:22.000Z"
"67894","Incident Response Template","2024-01-11T10:19:47.000Z"
...
```

!!! warning "Common errors"
    **`{"statusCode":401,"data":{"authorized":false,"valid":true,"allowedInPublicMode":false,"errors":[]}}`** — Verify the Atlassian API token is valid and has not expired; regenerate it in your account settings if needed.
    **`{"statusCode":404,"data":{"authorized":true,"valid":true,"errors":[{"message":"The content with id 67890 was not found or you do not have permission to view it."}]}}`** — Confirm the page ID exists and your user account has delete/edit permissions on that space.
    **`jq: parse error: Invalid numeric literal at line 1 column 6`** — Ensure the API response is valid JSON by checking that your Confluence instance URL is correct and the API endpoint is accessible.
```bash
# Find pages not updated in 365+ days (paste in Advanced Search CQL box)
# space = "ENG" AND lastModified < "2025-05-01" AND status = current

# Find stub pages (under 100 characters of body content)
# Use export + jq pipeline to check body length
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content?spaceKey=ENG&expand=body.storage&limit=50" \
  | jq '.results[] | select((.body.storage.value | length) < 100) | {id, title}'
```

```text title="Expected output"
{
  "id": "327680",
  "title": "Legacy API Deprecation Notice"
}
{
  "id": "425891",
  "title": "Q3 Roadmap TBD"
}
{
  "id": "589234",
  "title": "Incident Response - Draft"
}
{
  "id": "612447",
  "title": "TODO: Update Runbook"
}
```

!!! warning "Common errors"
    **`curl: (401) Unauthorized`** — Verify your API token is valid and base64-encoded correctly in the Authorization header, or use `-u user:token` format with proper credentials.
    **`jq: parse error: Cannot index string with string "storage"`** — Ensure the `expand=body.storage` parameter is included in the URL and the Confluence instance is returning valid JSON with nested body objects.
    **`curl: (403) Forbidden`** — Confirm your user account has read access to the ENG space and the API token has the `read:confluence-content.all` permission scope.
```bash
# List attachments for a page
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/child/attachment"

# Delete a specific attachment version
curl -u user:token -X DELETE \
  "https://your-instance.atlassian.net/wiki/rest/api/content/ATTACHMENT_ID/version/1"
```

```text title="Expected output"
{
  "results": [
    {
      "id": "att123456789",
      "type": "attachment",
      "title": "deployment-guide-v2.pdf",
      "version": {
        "number": 3
      },
      "extensions": {
        "fileSize": 2457600
      }
    },
    {
      "id": "att987654321",
      "type": "attachment",
      "title": "network-diagram.png",
      "version": {
        "number": 1
      },
      "extensions": {
        "fileSize": 1024000
      }
    }
  ],
  "start": 0,
  "limit": 25,
  "size": 2
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`{"statusCode":401,"data":{"authorized":false,"valid":true,"errors":["INVALID_USER_OR_PASSWORD"]}}`** — Verify your Confluence API token is valid and base64-encoded correctly in the `-u user:token` parameter.
    **`{"statusCode":404,"data":{"authorized":true,"valid":true,"errors":["The content with id 12345 does not exist or you do not have permission to view it."]}}`** — Confirm the page ID (12345) exists and your user has read access to that Confluence space.
    **`{"statusCode":403,"data":{"authorized":true,"valid":true,"errors":["You do not have permission to delete this attachment."]}}`** — Ensure your API token has edit/delete permissions on the page, or contact your Confluence space administrator.
```bash
# Pages in a space modified in the last 30 days
space = "ENG" AND lastModified > "2025-04-01" AND type = page

# Pages by title keyword
title ~ "runbook" AND space = "OPS"

# Pages created by a specific user
creator = "jsmith" AND type = page AND space = "ENG"

# Pages with a specific label
label = "incident" AND type = page

# Combine multiple filters
space IN ("ENG", "OPS") AND label = "on-call" AND status = current
```

```text title="Expected output"
space = "ENG" AND lastModified > "2025-04-01" AND type = page
  Results: 47 pages modified since April 1st, 2025
  Sample: "Database Migration Runbook v3.2", "Q2 Capacity Planning", "Incident Response SOP"

title ~ "runbook" AND space = "OPS"
  Results: 12 pages matching "runbook"
  Sample: "AWS Runbook", "Kubernetes Runbook", "Network Failover Runbook"

creator = "jsmith" AND type = page AND space = "ENG"
  Results: 23 pages created by jsmith
  Sample: "CI/CD Pipeline Setup", "Terraform State Management", "Docker Registry Guide"

label = "incident" AND type = page
  Results: 156 pages with "incident" label across all spaces
  Sample: "P1 Incident Playbook", "Post-Incident Review Template", "On-Call Escalation"

space IN ("ENG", "OPS") AND label = "on-call" AND status = current
  Results: 8 current pages with on-call label
  Sample: "Primary On-Call Schedule", "Secondary Escalation Matrix"
```

!!! warning "Common errors"
    **`Invalid CQL: Unexpected character at position 5`** — Remove spaces around the `=` operator; use `space="ENG"` instead of `space = "ENG"`.
    **`User 'jsmith' not found or permission denied`** — Verify the username exists in your Confluence instance and you have permission to search by creator; use the full display name if a username is not recognized.
    **`Label 'incident' does not exist in space 'ENG'`** — Confirm the label is applied to at least one page in the target space; check label spelling and capitalization.
```bash
# Filter by content type
type IN (page, blogpost, comment, attachment)

# Filter by ancestor page (all children and grandchildren)
ancestor = 12345

# Date range — ISO 8601 format
created >= "2025-01-01" AND created <= "2025-03-31"

# Pages that do NOT have a specific label
label != "archived" AND space = "ENG"

# Full-text body search
text ~ "kubernetes deployment" AND space = "ENG"
```

```text title="Expected output"
(no output — these are CQL query filter syntax examples, not executable bash commands)

Note: These lines represent Confluence Query Language (CQL) filter syntax intended for use in Confluence search or API calls, not standalone bash execution. To use these filters, they must be passed to a Confluence API endpoint or search interface.

Example API usage:
curl -u admin:token "https://confluence.example.com/rest/api/content/search?cql=type%20IN%20(page,blogpost)%20AND%20ancestor%3D12345"
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443`** — Verify the Confluence hostname is correct and the server is reachable from your network.
    **`{"statusCode":401,"message":"Unauthorized"}`** — Ensure your API token is valid and has appropriate permissions; regenerate the token in Confluence user settings if needed.
    **`Invalid CQL: unexpected character`** — Check that special characters in the CQL query are properly URL-encoded (spaces as %20, quotes as %22) when passed via curl.
```bash
# Run a CQL query from the command line
curl -u user:token -G \
  "https://your-instance.atlassian.net/wiki/rest/api/search" \
  --data-urlencode 'cql=space = "ENG" AND label = "on-call"' \
  --data-urlencode 'limit=25' \
  | jq '.results[] | {title: .title, url: ._links.webui}'

# Paginate through large result sets
START=0; LIMIT=50
while true; do
  RESULT=$(curl -s -u user:token -G \
    "https://your-instance.atlassian.net/wiki/rest/api/search" \
    --data-urlencode 'cql=space = "ENG" AND type = page' \
    --data-urlencode "limit=${LIMIT}" \
    --data-urlencode "start=${START}")
  echo "$RESULT" | jq '.results[].title'
  SIZE=$(echo "$RESULT" | jq '.size')
  [[ "$SIZE" -lt "$LIMIT" ]] && break
  START=$((START + LIMIT))
done
```

```text title="Expected output"
{
  "title": "On-Call Runbook: Incident Response",
  "url": "https://your-instance.atlassian.net/wiki/spaces/ENG/pages/524288/On-Call+Runbook"
}
{
  "title": "On-Call Escalation Procedures",
  "url": "https://your-instance.atlassian.net/wiki/spaces/ENG/pages/655360/On-Call+Escalation"
}
{
  "title": "On-Call Contact Matrix",
  "url": "https://your-instance.atlassian.net/wiki/spaces/ENG/pages/786432/Contact+Matrix"
}
"Database Migration Guide"
"API Rate Limiting Documentation"
"Kubernetes Deployment Checklist"
"Infrastructure Monitoring Setup"
"Load Balancer Configuration"
...
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to your-instance.atlassian.net port 443: Connection refused`** — Replace `your-instance` with your actual Confluence domain name (e.g., `company.atlassian.net`).
    **`jq: parse error: Invalid JSON text at line 1`** — Add `-s` flag to curl to silence progress output, or verify the API token has read permissions on the space.
    **`401 Unauthorized`** — Ensure the API token is valid and has not expired; generate a new token from your Atlassian account settings if needed.
```bash
# Add a label to a page
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/label" \
  -H "Content-Type: application/json" \
  -d '[{"prefix":"global","name":"runbook"}]'

# Remove a label
curl -u user:token -X DELETE \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/label/runbook"

# List all labels in a space
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/space/ENG/label"

# Find all pages with a label
curl -u user:token -G \
  "https://your-instance.atlassian.net/wiki/rest/api/search" \
  --data-urlencode 'cql=label = "runbook" AND space = "OPS"'
```

```text title="Expected output"
{"results":[{"id":"12345","type":"page","title":"Database Failover Procedure","_links":{"self":"https://your-instance.atlassian.net/wiki/pages/viewpage.action?pageId=12345"}}]}
(no output — command completes silently)
{"results":[{"prefix":"global","name":"runbook","id":"r1"},{"prefix":"global","name":"critical","id":"c2"},{"prefix":"global","name":"automation","id":"a3"},{"prefix":"global","name":"incident-response","id":"i4"}]}
{"results":[{"id":"12345","type":"page","title":"Database Failover Procedure","space":{"key":"OPS"}},{"id":"12346","type":"page","title":"Network Outage Response","space":{"key":"OPS"}},{"id":"12347","type":"page","title":"Storage Expansion Runbook","space":{"key":"OPS"}}],"start":0,"limit":25,"size":3}
```

!!! warning "Common errors"
    **`{"statusCode":401,"message":"Unauthorized"}`** — Verify the username and API token are correct, and that the token has API access permissions enabled.
    **`{"statusCode":404,"message":"Content with id 12345 not found"}`** — Confirm the page ID exists and is accessible to the authenticated user by checking the page URL or listing space contents.
    **`curl: (6) Could not resolve host: your-instance.atlassian.net`** — Replace `your-instance` with your actual Confluence domain name (e.g., `mycompany.atlassian.net`).
```bash
# Export search results to a file for reporting
curl -s -u user:token -G \
  "https://your-instance.atlassian.net/wiki/rest/api/search" \
  --data-urlencode 'cql=space = "ENG" AND label = "needs-review"' \
  --data-urlencode 'limit=100' \
  | jq -r '.results[] | [.title, ._links.webui] | @tsv' > needs_review.tsv
```


```text title="Expected output"
Engineering Team Review Queue	https://your-instance.atlassian.net/wiki/pages/viewpage.action?pageId=524288
Database Migration Plan v2.3	https://your-instance.atlassian.net/wiki/pages/viewpage.action?pageId=524289
API Rate Limiting Documentation	https://your-instance.atlassian.net/wiki/pages/viewpage.action?pageId=524290
Kubernetes Cluster Setup Guide	https://your-instance.atlassian.net/wiki/pages/viewpage.action?pageId=524291
Incident Response Runbook	https://your-instance.atlassian.net/wiki/pages/viewpage.action?pageId=524292
Load Balancer Configuration	https://your-instance.atlassian.net/wiki/pages/viewpage.action?pageId=524293
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to your-instance.atlassian.net port 443: Connection refused`** — Replace `your-instance` with your actual Confluence domain name (e.g., `company.atlassian.net`).
    **`jq: parse error: Invalid JSON text at line 1`** — Verify the API token is valid and the user has permission to access the Confluence REST API; expired or revoked tokens return HTML error pages instead of JSON.
    **`bash: jq: command not found`** — Install jq using your package manager (`apt-get install jq` on Debian/Ubuntu or `brew install jq` on macOS).
---

```d2
direction: right

create_a_space: "Create a Space" {shape: rectangle}
manage_space_permissions: "Manage Space Permissions" {shape: rectangle}
create_and_publish_a_page: "Create and Publish a Page" {shape: rectangle}
restrict_page_access: "Restrict Page Access" {shape: rectangle}
manage_user_accounts_admin: "Manage User Accounts (Admin)" {shape: rectangle}
run_a_space_backup: "Run a Space Backup" {shape: rectangle}

create_a_space -> manage_space_permissions
manage_space_permissions -> create_and_publish_a_page
create_and_publish_a_page -> restrict_page_access
restrict_page_access -> manage_user_accounts_admin
manage_user_accounts_admin -> run_a_space_backup
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Create a Space

Spaces are the top-level containers in Confluence — use them to group content by team, project, or product.

1. Navigate to **Spaces > Create Space**.
2. Choose the space type: **Team** (for ongoing team work), **Personal** (for individual notes), or **Software** (for project/product docs).
3. Set the space name and a short, unique space key (e.g., `ENG`, `OPS`).
4. Configure permissions — by default the creator has admin; add groups at creation or via Space Settings later.
5. Add a space description so users can identify the space from the Spaces directory.
6. Click **Create**.

---

## Manage Space Permissions

Control who can view, add pages, and administer a space.

1. Navigate to the space and click **Space Settings > Permissions**.
2. Add or remove groups or individual users in the permissions table.
3. Set permission levels: **View**, **Add Pages**, **Add Comments**, **Add Attachments**, or **Admin**.
4. Note the difference between **inherited** permissions (from global settings) and **explicit** permissions set on the space.
5. Click **Save All** to apply changes.
6. Verify by logging in as a test user or using an incognito session.

---

## Create and Publish a Page

Standard procedure for adding content to a Confluence space.

1. Click **Create** in the top navigation bar.
2. Select a template (e.g., Meeting Notes, Runbook) or start with a **Blank Page**.
3. Write content using the rich-text editor — use headings, tables, code blocks, and macros as needed.
4. Set the **parent page** in the page properties sidebar to place the page in the correct hierarchy.
5. Add **labels** to improve searchability (e.g., `runbook`, `incident`, `on-call`).
6. Click **Publish** to make the page live, or **Save as Draft** to continue editing later.

---

## Restrict Page Access

Use restrictions to limit who can view or edit a specific page, overriding space-level permissions.

1. Open the target page.
2. Click the **...** (more actions) menu and select **Restrictions**.
3. Add users or groups with either **View** or **Edit** restrictions.
4. Note that restrictions narrow access below space permissions — they cannot grant access beyond what the space allows.
5. Test with an incognito browser session to confirm the restriction behaves as expected.

---

## Manage User Accounts (Admin)

Use this for onboarding, offboarding, or group membership changes when Confluence is not fully LDAP-synced.

1. Navigate to **Confluence Admin > User Management**.
2. Search for the user by name or email.
3. Edit group membership to grant or revoke access (e.g., add to `confluence-users`, remove from `space-admins`).
4. To deactivate a stale account: **User Management > Deactivate User** — this prevents login without deleting data.
5. For LDAP-synced instances, deactivating the LDAP account is sufficient; Confluence picks up the change on the next sync.

---

## Run a Space Backup

Export a space for disaster recovery, migration, or archival purposes.

1. Navigate to **Confluence Admin > Backup & Restore**.
2. Click **Export Space**.
3. Select the target space from the list.
4. Choose the export format: **HTML** (human-readable) or **XML** (for re-import into another Confluence instance).
5. Click **Export** and wait for the archive to generate.
6. Download the archive and store it in a secure location (e.g., object storage or encrypted backup target).

---

## Index Rebuild (Search Fix)

Run this when Confluence search returns stale, missing, or incorrect results.

1. Navigate to **Confluence Admin > Content Indexing**.
2. Click **Rebuild Index**.
3. Confirm the operation — Confluence will display a warning that this is resource-intensive.
4. Schedule during off-peak hours; indexing a large instance can take 30 minutes or more.
5. Monitor progress in the Content Indexing page — the UI updates as pages are re-indexed.
6. Once complete, verify search returns expected results by running known queries.

---

## Manage Macros and Add-ons

Keep installed apps patched and remove unused add-ons to reduce attack surface and improve performance.

1. Navigate to **Confluence Admin > Manage Apps** (formerly Manage Add-ons).
2. Review the list of installed apps — check version, vendor, and last updated date.
3. Click **Update** on any apps with available updates.
4. **Disable** any apps that are unused or no longer required — disabling is safer than uninstalling as it preserves configuration.
5. Check the **Atlassian Marketplace** for security advisories on any installed apps before applying updates.
6. Test core page creation, macro rendering, and search after changes to confirm no regressions.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Confluence — Health Checks](../health-checks/)
- [Confluence — CLI Reference](../cli-reference/)
- [Confluence — Common Issues](../../troubleshooting/common-issues/)
