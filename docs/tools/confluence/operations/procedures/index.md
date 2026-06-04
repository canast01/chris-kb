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
```text
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
