# Confluence — Standards

## Page Templates

Creating and managing page templates, blueprints, and template variables.

## Page Templates vs Blueprints

Templates are static page skeletons. Blueprints are templates enhanced with a multi-step creation wizard.

```bash
# List global templates
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/template?type=global"

# List space-level templates
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/template?type=space&spaceKey=ENG"

# Get a specific template by ID
curl -u user:token \
  "https://your-instance.atlassian.net/wiki/rest/api/template/TEMPLATE_ID"
```
```

To create via UI: **Space Settings → Look and Feel → Templates → Create New Template**.

## Template Variables and Placeholders

```xml
<!-- Inline placeholder — shows as grey hint text in the editor -->
<ac:placeholder>Enter the service name here</ac:placeholder>

<!-- Metadata table with placeholders at page top -->
<table>
  <tr><th>Owner</th><td><ac:placeholder>@owner</ac:placeholder></td></tr>
  <tr><th>Review date</th><td><ac:placeholder>YYYY-MM-DD</ac:placeholder></td></tr>
  <tr><th>Status</th><td><ac:placeholder>Draft / Approved / Retired</ac:placeholder></td></tr>
</table>
```

Variable best practices:
- Add placeholder hint text for each field
- Group related variables in a metadata table at the top
- Keep variable names short and self-explanatory
- Do not use required-field macros unless the team is trained on them

## Updating and Deleting Templates

```bash
# Update an existing template
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/wiki/rest/api/template" \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "TEMPLATE_ID",
    "name": "Runbook Template v2",
    "templateType": "page",
    "space": {"key": "OPS"},
    "body": {
      "storage": {
        "value": "<h2>Updated body</h2>",
        "representation": "storage"
      }
    }
  }'

# Delete a template
curl -u user:token -X DELETE \
  "https://your-instance.atlassian.net/wiki/rest/api/template/TEMPLATE_ID"
```

Note: updating a template does not retroactively change pages already created from it.

## Common Storage Format Macros

| Macro Name | Storage Tag | Purpose |
|-----------|-------------|---------|
| Placeholder | `<ac:placeholder>` | Prompts author to fill in |
| Panel | `<ac:structured-macro ac:name="panel">` | Highlighted info box |
| Status | `<ac:structured-macro ac:name="status">` | Coloured status badge |
| Table of Contents | `<ac:structured-macro ac:name="toc">` | Auto-generated nav |
| Code Block | `<ac:structured-macro ac:name="code">` | Syntax-highlighted code |
| Info | `<ac:structured-macro ac:name="info">` | Blue info panel |

## Blueprints

Blueprints add a creation wizard with fill-in fields before the page body is created. They require an Atlassian Connect app.

```json
// atlassian-connect.json blueprint module entry
{
  "blueprints": [{
    "key": "incident-blueprint",
    "name": "Incident Report",
    "createResult": "edit",
    "template": {"url": "/templates/incident.xml"},
    "wizard": {
      "steps": [{
        "title": "Incident Details",
        "instructions": "Fill in the key incident fields below"
      }]
    }
  }]
}
```
