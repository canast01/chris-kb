# Confluence Pages

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

Page creation tips: always set a parent page to avoid orphaning, use descriptive titles, and add labels immediately.

## Using Macros

Macros extend page functionality with dynamic content. Insert via `/macro-name` in the editor.

```
/toc          — Table of contents (auto-generated from headings)
/children     — List child pages dynamically
/include      — Embed another page inline
/status       — Coloured status badge (e.g. IN PROGRESS, DONE)
/info         — Info / warning / note / tip panel
/code         — Syntax-highlighted code block
/jira         — Embed a Jira issue list or single ticket
/excerpt      — Mark content for reuse with the Include macro
```

| Macro | Purpose | Common Config |
|-------|---------|--------------|
| Table of Contents | Page nav | Min heading H2, max H3 |
| Children Display | Show sub-pages | depth=1, sort=title |
| Jira Issues | Live ticket list | JQL filter |
| Status | Visual badge | Yellow / Green / Red |
| Code Block | Syntax highlight | Language: bash, python, yaml |

## Page History and Versioning

Confluence stores every save as a numbered version. You can compare and restore.

```bash
# Get version history for a page
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/version"

# Restore a specific version
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/wiki/rest/api/content/12345/version" \
  -H "Content-Type: application/json" \
  -d '{"operationKey": "restore", "params": {"versionNumber": 4}}'

# Compare versions in the UI:
# Page → ... menu → Page History → select two versions → Compare
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
