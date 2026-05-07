# Confluence Spaces

Creating and managing Confluence spaces, configuring permissions, and archiving spaces.

## Creating a Space

Spaces are the top-level containers for related pages. Space keys are uppercase, max 10 characters, and cannot be changed after creation.

```bash
# Create a space via REST API
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/wiki/rest/api/space" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "PLAT",
    "name": "Platform Engineering",
    "description": {
      "plain": {
        "value": "Internal docs for the Platform team",
        "representation": "plain"
      }
    }
  }'

# List all global spaces
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/space?limit=50&type=global"
```

## Space Permissions

Permissions apply to all pages in the space by default. Page-level restrictions can narrow access further.

```bash
# Get current space permissions
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/space/ENG/permission"

# Grant a group read access
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/wiki/rest/api/space/ENG/permission" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": {"type": "group", "identifier": "developers"},
    "operation": {"key": "read", "target": "space"}
  }'

# Remove a permission by its ID
curl -u user:token -X DELETE \
  "https://your-instance.atlassian.net/wiki/rest/api/space/ENG/permission/42"
```

| Permission | Who Needs It | Notes |
|-----------|-------------|-------|
| View Space | All readers | Required for any access |
| Add Pages | Editors | Allows creating child pages |
| Edit Pages | Editors | Includes their own pages |
| Admin Space | Space admins | Template and permission management |
| Export Space | Power users | PDF/XML exports |
| Delete Pages | Editors+ | Restrict to avoid accidents |

## Space Administration

```bash
# Update space name and description
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/wiki/rest/api/space/ENG" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Engineering (Updated)",
    "description": {"plain": {"value": "Updated description", "representation": "plain"}}
  }'

# Set a page as the space homepage
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/wiki/rest/api/space/ENG" \
  -H "Content-Type: application/json" \
  -d '{"homepage": {"id": "PAGE_ID"}}'

# Get space statistics and metadata
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/space/ENG?expand=metadata.labels,description.plain,homepage"
```

## Archiving Spaces

Archive spaces that are no longer active but must be preserved for compliance or reference.

```bash
# Archive a space
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/wiki/rest/api/space/OLDPROJ/state" \
  -H "Content-Type: application/json" \
  -d '{"key": "OLDPROJ", "state": "archived"}'

# List all archived spaces
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/space?status=archived&limit=50"

# Restore an archived space
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/wiki/rest/api/space/OLDPROJ/state" \
  -H "Content-Type: application/json" \
  -d '{"key": "OLDPROJ", "state": "current"}'
```

Before archiving: notify space members, export a full PDF/XML backup, update cross-space links, and move any still-active pages.

## Space Categories and Labels

```bash
# Add a label/category to a space
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/wiki/rest/api/space/ENG/label" \
  -H "Content-Type: application/json" \
  -d '[{"prefix": "team", "name": "platform"}]'

# Search spaces by label
curl -u user:token -G \
  "https://your-instance.atlassian.net/wiki/rest/api/space" \
  --data-urlencode 'expand=metadata.labels'
```

| Space Type | Use Case | Default Visibility |
|-----------|----------|--------------------|
| Global | Team or project docs | All logged-in users |
| Personal (~username) | Individual drafts | Owner only |
| Archived | Historical reference | Read-only, hidden in nav |
