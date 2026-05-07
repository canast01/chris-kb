# Jira Tasks

Task creation, sub-tasks, issue linking, workflow transitions, and bulk operations.

## Creating Tasks

Tasks represent technical work that does not map directly to a user story (infra changes, chores, spikes).

```bash
# Create a task via REST API
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/rest/api/2/issue" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PLAT"},
      "summary": "Upgrade Terraform AWS provider to v5",
      "issuetype": {"name": "Task"},
      "description": "Provider v5 required for new S3 features. See migration guide.",
      "priority": {"name": "Medium"},
      "assignee": {"name": "jsmith"},
      "labels": ["infrastructure", "terraform"]
    }
  }'

# Get a task by key
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-123"
```

## Sub-tasks

Sub-tasks break a parent issue into trackable pieces of work.

```bash
# Create a sub-task
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/rest/api/2/issue" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PLAT"},
      "summary": "Test provider upgrade in dev environment",
      "issuetype": {"name": "Sub-task"},
      "parent": {"key": "PLAT-123"}
    }
  }'

# List sub-tasks for a parent issue
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-123" \
  | jq '.fields.subtasks[] | {key: .key, summary: .fields.summary, status: .fields.status.name}'
```

| Issue Type | Has Parent | Use Case |
|-----------|-----------|----------|
| Epic | No | Large theme |
| Story | Epic (optional) | User-facing feature |
| Task | Epic (optional) | Technical work |
| Bug | Epic (optional) | Defect |
| Sub-task | Story / Task / Bug | Work breakdown |

## Issue Linking

Link issues to express relationships: blocks, is blocked by, duplicates, relates to.

```bash
# Create an issue link
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/rest/api/2/issueLink" \
  -H "Content-Type: application/json" \
  -d '{
    "type": {"name": "Blocks"},
    "inwardIssue": {"key": "PLAT-123"},
    "outwardIssue": {"key": "PLAT-456"}
  }'

# List available link types
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/issueLinkType"

# Delete a link
curl -u user:token -X DELETE \
  "https://your-instance.atlassian.net/rest/api/2/issueLink/LINK_ID"
```

| Link Type | Direction | Meaning |
|-----------|----------|---------|
| Blocks | A blocks B | A must complete before B starts |
| Clones | A clones B | A is a duplicate of B |
| Relates to | A relates to B | General relationship |
| Duplicates | A duplicates B | Same work tracked twice |

## Workflow Transitions

```bash
# Get available transitions for an issue
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-123/transitions" \
  | jq '.transitions[] | {id: .id, name: .name}'

# Perform a transition (move to "In Progress")
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-123/transitions" \
  -H "Content-Type: application/json" \
  -d '{"transition": {"id": "21"}}'

# Transition with a comment
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-123/transitions" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": {"id": "31"},
    "update": {
      "comment": [{"add": {"body": "Deployed to prod — monitoring for 30 min"}}]
    }
  }'
```

## Bulk Operations

```bash
# Bulk assign issues to a new assignee (via search + update loop)
ISSUES=$(curl -s -u user:token -G \
  "https://your-instance.atlassian.net/rest/api/2/search" \
  --data-urlencode 'jql=project = PLAT AND assignee = "olduser" AND status != Done' \
  | jq -r '.issues[].key')

for ISSUE in $ISSUES; do
  curl -s -u user:token -X PUT \
    "https://your-instance.atlassian.net/rest/api/2/issue/${ISSUE}" \
    -H "Content-Type: application/json" \
    -d '{"fields": {"assignee": {"name": "newuser"}}}' 
done

# Bulk transition via Jira UI:
# Board or issue list → select issues → Actions → Transition
```

```bash
# Add a label to multiple issues
for ISSUE in PLAT-100 PLAT-101 PLAT-102; do
  curl -s -u user:token -X POST \
    "https://your-instance.atlassian.net/rest/api/2/issue/${ISSUE}" \
    -H "Content-Type: application/json" \
    -d '{"update": {"labels": [{"add": "needs-review"}]}}'
done
```
