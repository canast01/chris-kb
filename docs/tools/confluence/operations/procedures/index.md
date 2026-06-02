# Confluence — Procedures


<div class="kb-summary">
Procedures reference covering Page Management, Creating Pages, Page History and Versioning, Page Permissions, Watching and Notifications and 13 more sections.
</div>

## Page Management

Creating, organizing, and managing Confluence pages including templates, macros, history, and permissions.

## Creating Pages

New pages can be created from the space sidebar, a parent page, or via API.

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
```
┌───────────────────────────────── Confluence — Operations Procedures ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Confluence Standard Operating Procedures                           │   │
│   │         Planned restart: drain LB → stop Confluence → maintenance → start → add to LB         │   │
│   │             Space archival: export as XML → disable space → move to archive space             │   │
│   │         User offboard: deactivate LDAP account → remove group memberships → audit log         │   │
│   │           Plugin update: test in staging → UPM update in prod → verify functionality          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SOPs reduce error rates and ensure consistent execution of routine operations                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Maintenance SOPs               │  │                 Content SOPs                │   │
│   │             Planned restart SOP              │  │              Space archival SOP             │   │
│   │              Plugin update SOP               │  │              User offboard SOP              │   │
│   │              DB maintenance SOP              │  │            Content migration SOP            │   │
│   │                 Upgrade SOP                  │  │             Audit log review SOP            │   │
│   │              Backup verify SOP               │  │            Permission review SOP            │   │
│   │                 Reindex SOP                  │  │              GDPR deletion SOP              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Confluence VMs · LB for draining · PostgreSQL · NFS · UPM for plugins                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LB drain       = remove node from load balancer pool before maintenance; in-flight reqs complete     │
│  UPM            = Universal Plugin Manager; Admin > Manage Apps for add-on updates                    │
│  Space archival = export space as XML; disable space; accessible via search but read-only             │
│  User offboard  = deactivate in LDAP; Confluence sync picks up deactivation within poll interval      │
│  DB maintenance = VACUUM ANALYZE in PostgreSQL; run during low-traffic windows                        │
│  GDPR deletion  = remove personal data; Confluence has no native right-to-erasure tool                │
│  Content migrate = use Confluence space import/export to move content between instances               │
│  Permission review = quarterly review of space admin list and global permission groups                │
│  Audit log review = Admin > Audit Log; monthly review of privilege escalation events                  │
│  Upgrade SOP    = snapshot VMs → backup DB → run installer → verify → cutover                         │
│  Reindex SOP    = Admin > Content Indexing > Rebuild; during off-peak; takes 30+ min for large        │
│  VACUUM ANALYZE = PostgreSQL command; reclaims storage and updates query planner statistics           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Add a version comment when saving: **Edit → Save → enter comment** — this helps trace why content changed.

## Page Permissions

Restrict access at the page level in addition to space-level controls.

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

| Permission Level | Scope | Overrides Space? |
|-----------------|-------|-----------------|
| Space admin | All pages in space | Base level |
| Space view | Space-level read | Yes |
| Page restriction | Single page only | Yes (additive) |
| Anonymous access | Public pages | Requires global setting |

## Watching and Notifications

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

---

## Cleanup

Practical guidance for archiving pages, removing orphaned content, and keeping spaces tidy.

## Archiving Pages

Archiving removes a page from navigation without deleting it. Archived pages remain searchable but are hidden from space tree views.

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

To archive in bulk, use: **Space Settings → Content Tools → Archive**.

## Removing Orphaned Pages

Orphaned pages have no parent and do not appear in the space tree. They accumulate over migrations and copy-paste operations.

```bash
# Find pages with no parent using CQL in Advanced Search:
# space = "ENG" AND ancestor = null AND status = current

# Via API — fetch pages and filter for empty ancestors
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content?spaceKey=ENG&expand=ancestors&limit=100" \
  | jq '.results[] | select(.ancestors == []) | {id, title}'
```

Review each result before deletion — some root-level pages are intentional.

## Bulk Delete Operations

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

| Operation | UI Location | API Method |
|-----------|------------|------------|
| Archive page | Page Actions → Archive | PUT /content/{id} status=archived |
| Delete page | Page Actions → Delete | DELETE /content/{id} |
| Move page | Page Actions → Move | PUT /content/{id}/move |
| Restore archived | Space Admin → Archived | PUT /content/{id} status=current |
| Bulk delete | Space Admin → Content Tools | Iterate DELETE |

## Quarterly Cleanup Checklist

Run these checks every quarter to keep spaces healthy:

```bash
# Find pages not updated in 365+ days (paste in Advanced Search CQL box)
# space = "ENG" AND lastModified < "2025-05-01" AND status = current

# Find stub pages (under 100 characters of body content)
# Use export + jq pipeline to check body length
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content?spaceKey=ENG&expand=body.storage&limit=50" \
  | jq '.results[] | select((.body.storage.value | length) < 100) | {id, title}'
```

- Remove or archive pages with no views in 12 months
- Merge stub pages (fewer than 3 lines of real content)
- Consolidate duplicate how-to pages
- Update or delete pages with broken links

## Handling Attachment Bloat

Attachments are a major source of storage growth. Remove stale versions.

```bash
# List attachments for a page
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/child/attachment"

# Delete a specific attachment version
curl -u user:token -X DELETE \
  "https://your-instance.atlassian.net/wiki/rest/api/content/ATTACHMENT_ID/version/1"
```

| Attachment Type | Typical Size | Recommended Action |
|----------------|-------------|-------------------|
| Old screenshots | 200 KB–2 MB | Delete superseded versions |
| PDF exports | 1–10 MB | Link externally if still needed |
| Log files | Variable | Delete; store in object storage |
| Video recordings | 50–500 MB | Move to dedicated media host |

---

## Search

Mastering CQL search syntax, filtering results, saved searches, and label-based discovery.

## CQL Syntax Basics

Confluence Query Language (CQL) powers advanced search. Access it via **Search → Advanced Search**.

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

## CQL Operators Reference

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Exact match | `space = "ENG"` |
| `~` | Contains / fuzzy | `title ~ "deploy"` |
| `!=` | Not equal | `status != archived` |
| `IN` | Matches any in list | `type IN (page, blogpost)` |
| `NOT IN` | Excludes list | `space NOT IN ("ARCHIVE")` |
| `>` / `<` | Date comparison | `lastModified > "2025-01-01"` |
| `AND` / `OR` | Boolean logic | `label = "ops" AND type = page` |

## Filtering by Content Type and Dates

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

## Running CQL Queries via API

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

## Labels

Labels are the fastest way to build cross-space navigation without restructuring pages.

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

| Field | CQL Keyword | Search Type |
|-------|------------|-------------|
| Title | `title ~` | Fuzzy or exact |
| Body text | `text ~` | Full-text index |
| Labels | `label =` | Exact match only |
| Creator | `creator =` | Username or accountId |
| Last modified | `lastModified >` | ISO date string |
| Space key | `space =` | Exact space key |
| Ancestor page | `ancestor =` | Page ID |

## Saved Searches

Save frequent CQL queries for team reuse. In the UI: run an advanced search, then click the bookmark icon → **Save this search**. Saved searches appear in the search sidebar.

```bash
# Export search results to a file for reporting
curl -s -u user:token -G \
  "https://your-instance.atlassian.net/wiki/rest/api/search" \
  --data-urlencode 'cql=space = "ENG" AND label = "needs-review"' \
  --data-urlencode 'limit=100' \
  | jq -r '.results[] | [.title, ._links.webui] | @tsv' > needs_review.tsv
```
