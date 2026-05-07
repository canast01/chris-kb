# Confluence Cleanup

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
