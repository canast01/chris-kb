# Confluence Search

Mastering CQL search syntax, filtering results, saved searches, and label-based discovery.

## CQL Syntax Basics

Confluence Query Language (CQL) powers advanced search. Access it via **Search → Advanced Search**.

```
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

```
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
