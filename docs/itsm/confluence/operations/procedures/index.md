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
```bash
# Find pages with no parent using CQL in Advanced Search:
# space = "ENG" AND ancestor = null AND status = current

# Via API — fetch pages and filter for empty ancestors
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content?spaceKey=ENG&expand=ancestors&limit=100" \
  | jq '.results[] | select(.ancestors == []) | {id, title}'
```
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
```bash
# Find pages not updated in 365+ days (paste in Advanced Search CQL box)
# space = "ENG" AND lastModified < "2025-05-01" AND status = current

# Find stub pages (under 100 characters of body content)
# Use export + jq pipeline to check body length
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content?spaceKey=ENG&expand=body.storage&limit=50" \
  | jq '.results[] | select((.body.storage.value | length) < 100) | {id, title}'
```
```bash
# List attachments for a page
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/child/attachment"

# Delete a specific attachment version
curl -u user:token -X DELETE \
  "https://your-instance.atlassian.net/wiki/rest/api/content/ATTACHMENT_ID/version/1"
```
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
```bash
# Export search results to a file for reporting
curl -s -u user:token -G \
  "https://your-instance.atlassian.net/wiki/rest/api/search" \
  --data-urlencode 'cql=space = "ENG" AND label = "needs-review"' \
  --data-urlencode 'limit=100' \
  | jq -r '.results[] | [.title, ._links.webui] | @tsv' > needs_review.tsv
```

---

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
