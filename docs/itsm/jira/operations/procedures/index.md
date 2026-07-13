---
tags:
  - jira
  - operations
description: "Jira operational procedures — story and epic creation, sprint management, backlog grooming, workflow configuration, user and permission management, board..."
---
# Jira — Procedures

<div class="kb-summary">
Jira operational procedures — story and epic creation, sprint management, backlog grooming, workflow configuration, user and permission management, board setup, and reporting.

*Applies to: Jira 9.x / Cloud*
</div>

```d2
direction: right

stories: "Stories" {shape: rectangle}
story_structure: "Story Structure" {shape: rectangle}
epics: "Epics" {shape: rectangle}
story_splitting: "Story Splitting" {shape: rectangle}
tasks: "Tasks" {shape: rectangle}
creating_tasks: "Creating Tasks" {shape: rectangle}

stories -> story_structure
story_structure -> epics
epics -> story_splitting
story_splitting -> tasks
tasks -> creating_tasks
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Stories

Story structure, acceptance criteria, story points, epics, and estimation.

## Story Structure

A well-formed user story answers: who needs this, what they need, and why.

Estimation tips:
- Use planning poker for team alignment
- Anchor estimates to reference stories the team knows
- If a story reaches 8 points, consider splitting it
- Avoid converting points to hours in team communication

```bash
# Set story points via API
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-123" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"customfield_10016": 5}}'

# Get story points for all issues in a sprint
curl -u user:token -G \
  "https://your-instance.atlassian.net/rest/api/2/search" \
  --data-urlencode 'jql=project = PLAT AND sprint in openSprints()' \
  --data-urlencode 'fields=summary,customfield_10016' \
  | jq '.issues[] | {key: .key, points: .fields.customfield_10016}'
```


```text title="Expected output"
{
  "id": "10042",
  "key": "PLAT-123",
  "self": "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-123",
  "fields": {
    "customfield_10016": 5
  }
}
{
  "key": "PLAT-101",
  "points": 8
}
{
  "key": "PLAT-102",
  "points": 5
}
{
  "key": "PLAT-103",
  "points": 3
}
{
  "key": "PLAT-104",
  "points": null
}
{
  "key": "PLAT-105",
  "points": 13
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `"errorMessages":["Field 'customfield_10016' cannot be set. It is not on the appropriate screen, or unknown."]` | Verify the custom field ID matches your Jira instance by checking Administration > Fields or using `curl -u user:token https://your-instance.atlassian.net/rest/api/2/field | jq '.[] | select(.name=="Story Points")'`. |
    | `curl: (6) Could not resolve host: your-instance.atlassian.net` | Replace `your-instance` with your actual Jira domain name (e.g., `mycompany.atlassian.net`). |
    | `jq: parse error: Invalid numeric literal at line 1 column 10` | Ensure the API response is valid JSON by removing any authentication errors; check credentials with `curl -u user:token https://your-instance.atlassian.net/rest/api/2/myself`. |
## Epics

Epics group related stories under a theme or deliverable.

```bash
# Create an epic
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/rest/api/2/issue" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PLAT"},
      "summary": "Storage Automation",
      "issuetype": {"name": "Epic"},
      "customfield_10011": "Storage Automation"
    }
  }'

# Link a story to an epic
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-123" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"customfield_10014": "PLAT-10"}}'

# List all stories in an epic
curl -u user:token -G \
  "https://your-instance.atlassian.net/rest/api/2/search" \
  --data-urlencode 'jql=project = PLAT AND "Epic Link" = PLAT-10'
```


```text title="Expected output"
{"id":"10042","key":"PLAT-10","self":"https://your-instance.atlassian.net/rest/api/2/issue/10042","fields":{"summary":"Storage Automation"}}
(no output — command completes silently)
{"expand":"names,schema","startAt":0,"maxResults":50,"total":3,"issues":[{"key":"PLAT-123","fields":{"summary":"Implement S3 bucket policies"}},{"key":"PLAT-124","fields":{"summary":"Configure lifecycle rules"}},{"key":"PLAT-125","fields":{"summary":"Enable versioning on buckets"}}]}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `{"errorMessages":["Authentication failed; verify you are logged in"]}` | Verify your Jira instance URL, username, and API token are correct. |
    | `{"errorMessages":["Field 'customfield_10014' does not exist or you do not have permission to edit it."]}` | Confirm the custom field ID for "Epic Link" matches your Jira instance by checking Administration > Custom Fields. |
## Story Splitting

Split large stories using these patterns:

```bash
# Patterns for splitting
By workflow step:     One story per step in a user workflow
By data type:         Separate stories for each entity/type
By interface:         API first, then UI
By acceptance criterion: Each criterion becomes its own story
By happy/unhappy path: Core flow first, error handling separate
By permission level:  Admin view, user view as separate stories
```


```text title="Expected output"
(no output — this is a documentation comment block with pattern descriptions only)
```
| Signal | Action |
|--------|--------|
| Story > 8 points | Split before sprint planning |
| Multiple "and" clauses in title | Each clause is a separate story |
| Multiple system touches | Split by system boundary |
| Unclear acceptance criteria | Spike first, then story |

---

## Tasks

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


```text title="Expected output"
{
  "id": "10042",
  "key": "PLAT-4521",
  "self": "https://your-instance.atlassian.net/rest/api/2/issue/10042",
  "fields": {
    "summary": "Upgrade Terraform AWS provider to v5",
    "status": {
      "name": "To Do"
    },
    "assignee": {
      "name": "jsmith",
      "emailAddress": "jsmith@company.atlassian.net"
    }
  }
}
{
  "expand": "changelog,html",
  "id": "10042",
  "key": "PLAT-123",
  "self": "https://your-instance.atlassian.net/rest/api/2/issue/10042",
  "fields": {
    "summary": "Upgrade Terraform AWS provider to v5",
    "description": "Provider v5 required for new S3 features. See migration guide.",
    "status": {"name": "To Do"},
    "priority": {"name": "Medium"},
    "assignee": {"name": "jsmith"},
    "labels": ["infrastructure", "terraform"],
    "created": "2024-01-15T09:42:31.000+0000"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `"errorMessages":["User 'user' does not have permission to create issues in project PLAT"]` | Verify the API token has project admin or create-issue permissions, or check project visibility settings. |
    | `curl: (7) Failed to connect to your-instance.atlassian.net port 443: Connection refused` | Replace `your-instance.atlassian.net` with your actual Jira domain and verify the instance is accessible. |
    | `"errorMessages":["Issue Type 'Task' is not valid for project PLAT"]` | Check the project's available issue types via the project settings or use `curl -u user:token "https://your-instance.atlassian.net/rest/api/2/project/PLAT/issuetypes"` to list valid types. |
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


```text title="Expected output"
{
  "id": "10047",
  "key": "PLAT-124",
  "self": "https://your-instance.atlassian.net/rest/api/2/issue/10047",
  "fields": {
    "summary": "Test provider upgrade in dev environment",
    "issuetype": {
      "name": "Sub-task"
    },
    "parent": {
      "key": "PLAT-123"
    }
  }
}
{
  "key": "PLAT-124",
  "summary": "Test provider upgrade in dev environment",
  "status": "To Do"
}
{
  "key": "PLAT-125",
  "summary": "Validate rollback procedure",
  "status": "In Progress"
}
{
  "key": "PLAT-126",
  "summary": "Document breaking changes",
  "status": "Done"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to your-instance.atlassian.net port 443: Connection refused` | Replace `your-instance.atlassian.net` with your actual Jira domain name. |
    | `{"errorMessages":["Issue does not exist or you do not have permission to see it."],"errors":{}}` | Verify that PLAT-123 exists, is accessible to your user, and that the parent issue type supports sub-tasks. |
    | `jq: parse error: Cannot index number with string "fields"` | Ensure the curl response is valid JSON; add `-s` flag to curl to suppress progress output and check authentication credentials are correct. |
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


```text title="Expected output"
{
  "id": "10042",
  "self": "https://your-instance.atlassian.net/rest/api/2/issueLink/10042",
  "type": {
    "id": "10000",
    "name": "Blocks",
    "inward": "is blocked by",
    "outward": "blocks",
    "self": "https://your-instance.atlassian.net/rest/api/2/issueLinkType/10000"
  },
  "inwardIssue": {"key": "PLAT-123", "id": "10501"},
  "outwardIssue": {"key": "PLAT-456", "id": "10502"}
}
{
  "issueLinkTypes": [
    {"id": "10000", "name": "Blocks", "inward": "is blocked by", "outward": "blocks"},
    {"id": "10001", "name": "Relates", "inward": "relates to", "outward": "relates to"},
    {"id": "10002", "name": "Duplicates", "inward": "is duplicated by", "outward": "duplicates"},
    {"id": "10003", "name": "Clones", "inward": "is cloned by", "outward": "clones"}
  ]
}
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `{"errorMessages":["Authentication failed; invalid username, password, token, or CAPTCHA challenge response."]}` | Verify the username, API token, and instance URL are correct; regenerate the token if expired. |
    | `{"errorMessages":["Issue does not exist or you do not have permission to see it."]}` | Confirm both PLAT-123 and PLAT-456 exist and the authenticated user has permission to view and link them. |
    | `{"errorMessages":["Link type 'Blocks' does not exist."]}` | Run the second curl command to list available link types and use a valid name from the response. |
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


```text title="Expected output"
{
  "id": "11",
  "name": "To Do"
}
{
  "id": "21",
  "name": "In Progress"
}
{
  "id": "31",
  "name": "Done"
}
{
  "id": "41",
  "name": "In Review"
}
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to your-instance.atlassian.net port 443: Name or service not known` | Replace `your-instance` with your actual Jira domain name (e.g., `company.atlassian.net`). |
    | `{"errorMessages":["Issue does not exist or you do not have permission to see it."]}` | Verify the issue key (PLAT-123) exists and your API token has read/write permissions for that project. |
    | `{"errorMessages":["Transition is not available for the current status of the issue."]}` | Confirm the transition ID is valid for the issue's current status by running the first command to list available transitions. |
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


```text title="Expected output"
PLAT-4521
PLAT-4589
PLAT-4603
PLAT-4671
PLAT-4702
PLAT-4758
PLAT-4819
...
Successfully updated PLAT-4521
Successfully updated PLAT-4589
Successfully updated PLAT-4603
Successfully updated PLAT-4671
Successfully updated PLAT-4702
Successfully updated PLAT-4758
Successfully updated PLAT-4819
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (401) Unauthorized` | Verify the API token is valid and base64-encoded correctly in the `-u user:token` parameter, or use `-H "Authorization: Bearer $TOKEN"` instead. |
    | `jq: parse error: Invalid JSON` | Check that the Jira instance URL is correct and accessible; the search endpoint may be returning an error page instead of JSON. |
    | `"errorMessages": ["User does not exist"]` | Confirm that "newuser" exists in your Jira instance and has permission to be assigned issues in the PLAT project. |
```bash
# Add a label to multiple issues
for ISSUE in PLAT-100 PLAT-101 PLAT-102; do
  curl -s -u user:token -X POST \
    "https://your-instance.atlassian.net/rest/api/2/issue/${ISSUE}" \
    -H "Content-Type: application/json" \
    -d '{"update": {"labels": [{"add": "needs-review"}]}}'
done
```


```text title="Expected output"
{"id":"10000","key":"PLAT-100","self":"https://your-instance.atlassian.net/rest/api/2/issue/10000"}
{"id":"10001","key":"PLAT-101","self":"https://your-instance.atlassian.net/rest/api/2/issue/10001"}
{"id":"10002","key":"PLAT-102","self":"https://your-instance.atlassian.net/rest/api/2/issue/10002"}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `{"errorMessages":["Authentication failed; invalid username, password, token, or CAPTCHA"]}` | Verify the API token is valid and base64-encoded correctly in the `-u user:token` parameter. |
    | `{"errorMessages":["You do not have permission to edit this issue"]}` | Confirm the user account has the "Edit Issues" permission in the Jira project. |
    | `curl: (6) Could not resolve host: your-instance.atlassian.net` | Replace `your-instance` with your actual Jira instance name (e.g., `company.atlassian.net`). |
---

## Reporting

Sprint reports, velocity, burndown charts, cumulative flow diagrams, and data exports.

## Sprint Reports

Sprint reports show which issues were completed, incomplete, or removed during a sprint.

```bash
# Get sprint report data via API
curl -u user:token \
  "https://your-instance.atlassian.net/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId=10&sprintId=42"

# List all sprints for a board
curl -u user:token \
  "https://your-instance.atlassian.net/rest/agile/1.0/board/10/sprint?state=closed&maxResults=10"

# Get issues completed in a sprint
curl -u user:token \
  "https://your-instance.atlassian.net/rest/agile/1.0/sprint/42/issue?jql=status+in+(Done,Resolved)"
```


```text title="Expected output"
{
  "contents": {
    "completedIssuesEstimate": 89,
    "issuesNotEstimated": 3,
    "issuesEstimate": 144,
    "completedIssuesCount": 34,
    "issuesCount": 42
  },
  "sprint": {
    "id": 42,
    "name": "Sprint 24",
    "startDate": "2024-01-15T09:00:00.000Z",
    "endDate": "2024-01-29T17:00:00.000Z"
  }
}
{
  "values": [
    {"id": 42, "name": "Sprint 24", "state": "closed", "startDate": "2024-01-15T09:00:00.000Z"},
    {"id": 41, "name": "Sprint 23", "state": "closed", "startDate": "2024-01-01T09:00:00.000Z"},
    {"id": 40, "name": "Sprint 22", "state": "closed", "startDate": "2023-12-18T09:00:00.000Z"}
  ],
  "isLast": false,
  "maxResults": 10
}
{
  "expand": "changelog,changelog.histories",
  "issues": [
    {"key": "PROJ-1847", "fields": {"summary": "Update authentication module", "status": {"name": "Done"}}},
    {"key": "PROJ-1842", "fields": {"summary": "Fix database connection pooling", "status": {"name": "Resolved"}}},
    {"key": "PROJ-1839", "fields": {"summary": "Refactor API response handler", "status": {"name": "Done"}}}
  ],
  "total": 34
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to your-instance.atlassian.net port 443: Connection refused` | Replace `your-instance` with your actual Jira domain name (e.g., `company.atlassian.net`). |
    | `{"errorMessages":["User is not authenticated"],"errors":{}}` | Verify the API token is valid and use base64 encoding: `curl -u user:$(echo -n token | base64)` or switch to `-H "Authorization: Bearer $TOKEN"` format. |
    | `{"errorMessages":["The board does not exist or you do not have permission to view it"]}` | Confirm the `rapidViewId` and `sprintId` values are correct and your user account has access to the board. |
Key sprint metrics to review:
- Commitment (story points planned at sprint start)
- Completed points vs committed points
- Issues added mid-sprint (scope creep)
- Carried-over issues (not completed)

## Velocity Chart

Velocity measures average story points completed per sprint. Use it for capacity planning.

```bash
# Fetch velocity data (GreenHopper endpoint)
curl -u user:token \
  "https://your-instance.atlassian.net/rest/greenhopper/1.0/rapid/charts/velocity?rapidViewId=10"

# Export last 10 sprints of velocity data with jq
curl -s -u user:token \
  "https://your-instance.atlassian.net/rest/greenhopper/1.0/rapid/charts/velocity?rapidViewId=10" \
  | jq '.velocityStatEntries | to_entries[] | {sprint: .key, completed: .value.completed.value, estimated: .value.estimated.value}'
```


```text title="Expected output"
{
  "sprint": "Sprint 47",
  "completed": 89,
  "estimated": 95
}
{
  "sprint": "Sprint 46",
  "completed": 76,
  "estimated": 82
}
{
  "sprint": "Sprint 45",
  "completed": 92,
  "estimated": 88
}
{
  "sprint": "Sprint 44",
  "completed": 71,
  "estimated": 79
}
{
  "sprint": "Sprint 43",
  "completed": 85,
  "estimated": 90
}
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (401) Unauthorized` | Verify the API token is valid and the user account has access to the Jira instance; regenerate the token if expired. |
    | `jq: error (at <stdin>:1): Cannot index null with string "velocityStatEntries"` | Confirm the rapidViewId=10 exists and the GreenHopper endpoint is enabled; check the board ID with `curl -s -u user:token "https://your-instance.atlassian.net/rest/greenhopper/1.0/rapidviews/list" | jq '.views'`. |
| Metric | Formula | Use |
|--------|---------|-----|
| Velocity | Avg completed points / sprint | Sprint capacity planning |
| Predictability | Completed / committed | Team reliability signal |
| Scope creep rate | Mid-sprint added / committed | Process health indicator |

## Burndown Chart

Burndown shows remaining work over a sprint's timeline. A healthy burndown trends toward zero at sprint end.

```bash
# Fetch burndown data
curl -u user:token \
  "https://your-instance.atlassian.net/rest/greenhopper/1.0/rapid/charts/scopechangeburndownchart?rapidViewId=10&sprintId=42"

# Get current sprint remaining work via JQL
curl -u user:token -G \
  "https://your-instance.atlassian.net/rest/api/2/search" \
  --data-urlencode 'jql=sprint in openSprints() AND project = PLAT AND status != Done' \
  --data-urlencode 'fields=summary,story_points,status' \
  | jq '[.issues[].fields.customfield_10016 // 0] | add'
```


```text title="Expected output"
{
  "contents": [
    {
      "key": "PLAT-1847",
      "summary": "Refactor authentication module",
      "estimatedStatistic": {
        "statFieldValue": {
          "value": 13
        }
      },
      "changedEstimatedStatistic": {
        "statFieldValue": {
          "value": 13
        }
      }
    }
  ],
  "sprint": {
    "id": 42,
    "name": "Sprint 42 - Q1 Infrastructure",
    "state": "ACTIVE"
  }
}
[
  {
    "key": "PLAT-1847",
    "fields": {
      "summary": "Refactor authentication module",
      "customfield_10016": 13,
      "status": {
        "name": "In Progress"
      }
    }
  },
  {
    "key": "PLAT-1892",
    "fields": {
      "summary": "Update load balancer config",
      "customfield_10016": 8,
      "status": {
        "name": "To Do"
      }
    }
  },
  {
    "key": "PLAT-1903",
    "fields": {
      "summary": "Database migration prep",
      "customfield_10016": 5,
      "status": {
        "name": "In Progress"
      }
    }
  }
]
31
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (401) Unauthorized` | Verify your Jira API token is valid and base64-encoded correctly in the `-u user:token` parameter. |
    | `jq: error (null) and number cannot be added` | Ensure the custom field ID `customfield_10016` matches your Jira instance's story points field by checking Administration > Custom Fields. |
## Cumulative Flow Diagram (CFD)

CFD shows how many issues are in each status over time. Widening bands indicate bottlenecks.

```bash
# Fetch CFD data
curl -u user:token \
  "https://your-instance.atlassian.net/rest/greenhopper/1.0/rapid/charts/cumulativeflowdiagram?rapidViewId=10&swimlaneId=0&fromDate=2025-01-01&toDate=2025-03-31"
```


```text title="Expected output"
{
  "queryKey": "com.atlassian.jira.plugins.jira-agile-core:greenhopper-cfd",
  "maxIssuesExceeded": false,
  "issueCount": 247,
  "columns": [
    {
      "columnId": "TODO",
      "columnName": "To Do",
      "statuses": ["10000"]
    },
    {
      "columnId": "IN_PROGRESS",
      "columnName": "In Progress",
      "statuses": ["3", "10001"]
    },
    {
      "columnId": "DONE",
      "columnName": "Done",
      "statuses": ["10002"]
    }
  ],
  "cumulativeFlowDiagramData": {
    "2025-01-01": {"TODO": 89, "IN_PROGRESS": 34, "DONE": 12},
    "2025-01-15": {"TODO": 76, "IN_PROGRESS": 52, "DONE": 31},
    "2025-02-01": {"TODO": 61, "IN_PROGRESS": 68, "DONE": 58},
    "2025-03-31": {"TODO": 42, "IN_PROGRESS": 45, "DONE": 160}
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to your-instance.atlassian.net port 443: Connection refused` | Replace `your-instance` with your actual Jira domain name (e.g., `mycompany.atlassian.net`). |
    | `{"errorMessages":["User does not have permission to view this board"],"errors":{}}` | Verify the API token has board access permissions and the `rapidViewId` matches a board the user can access. |
    | `{"errorMessages":["Invalid rapidViewId: 10"],"errors":{}}` | Confirm the board ID exists by listing available boards with `curl -u user:token "https://your-instance.atlassian.net/rest/greenhopper/1.0/boards"`. |
Interpreting the CFD:
- **Widening "In Progress" band** — WIP is accumulating, throughput is slower than input
- **Flat "Done" band** — work is not being completed
- **Steep "To Do" drop** — sudden scope removal
- **Parallel bands** — healthy, consistent flow

## JQL for Reporting

```bash
# Issues closed in the last 2 weeks
project = PLAT AND status changed to Done after "-2w"

# Issues created but not resolved in 30 days
project = PLAT AND created <= "-30d" AND resolution = Unresolved

# Bugs by priority
project = PLAT AND issuetype = Bug AND status != Done ORDER BY priority ASC

# Issues by assignee with story points
project = PLAT AND sprint in openSprints() AND assignee is not EMPTY
```


```text title="Expected output"
JQL Query 1: Issues closed in the last 2 weeks
PLAT-4521 | Upgrade database schema | Done | 2024-01-12
PLAT-4518 | Fix authentication timeout | Done | 2024-01-11
PLAT-4512 | Deploy load balancer config | Done | 2024-01-10
(3 issues)

JQL Query 2: Issues created but not resolved in 30 days
PLAT-4201 | Implement caching layer | Open | Created: 2023-12-05
PLAT-4189 | Refactor API endpoints | In Progress | Created: 2023-12-04
PLAT-4156 | Update monitoring alerts | Open | Created: 2023-12-01
(7 issues)

JQL Query 3: Bugs by priority
PLAT-4534 | Memory leak in worker process | Blocker | Open
PLAT-4531 | SSL certificate validation error | High | In Progress
PLAT-4528 | Incorrect timestamp formatting | Medium | Open
PLAT-4515 | UI button misalignment | Low | Open
(12 issues)

JQL Query 4: Issues by assignee with story points
PLAT-4520 | alice.chen | 8 points | In Progress
PLAT-4519 | bob.martinez | 5 points | In Progress
PLAT-4517 | carol.singh | 13 points | Open
PLAT-4516 | david.lee | 3 points | Done
(24 issues)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The value 'openSprints()' does not exist or you do not have permission to see it.` | Replace `openSprints()` with the actual sprint name or ID (e.g., `sprint = "Sprint 47"`), or verify the Jira project has active sprints configured. |
    | `Field 'resolution' does not exist or you do not have permission to see it.` | Use `resolution is EMPTY` instead of `resolution = Unresolved`, as Unresolved is not a valid resolution value in standard Jira configurations. |
## Exporting Data

```bash
# Export issues to CSV via REST API
curl -u user:token -G \
  "https://your-instance.atlassian.net/rest/api/2/search" \
  --data-urlencode 'jql=project = PLAT AND sprint in closedSprints()' \
  --data-urlencode 'fields=summary,assignee,status,story_points,resolutiondate' \
  --data-urlencode 'maxResults=500' \
  | jq -r '.issues[] | [.key, .fields.summary, .fields.status.name, (.fields.customfield_10016 // ""), (.fields.resolutiondate // "")] | @csv' \
  > sprint_data.csv

# Export via Jira UI
# Issues → Export → CSV (all fields) or Excel
```


```text title="Expected output"
{
  "expand": "names,schema",
  "startAt": 0,
  "maxResults": 500,
  "total": 247,
  "issues": [
    {
      "expand": "changelog,versionedRepresentations",
      "id": "10847",
      "key": "PLAT-1523",
      "fields": {
        "summary": "Implement OAuth2 token refresh mechanism",
        "status": {
          "self": "https://your-instance.atlassian.net/rest/api/2/status/10000",
          "description": "Work has been completed",
          "iconUrl": "https://your-instance.atlassian.net/images/icons/statuses/done.png",
          "name": "Done",
          "id": "10000"
        },
        "customfield_10016": 8,
        "resolutiondate": "2024-01-15T14:32:00.000-0500"
      }
    },
    ...
  ]
}
"PLAT-1523","Implement OAuth2 token refresh mechanism","Done","8","2024-01-15T14:32:00.000-0500"
"PLAT-1524","Fix database connection pooling timeout","Done","5","2024-01-14T09:18:00.000-0500"
"PLAT-1525","Update API rate limiting documentation","In Progress","3",""
"PLAT-1526","Resolve memory leak in cache layer","Done","13","2024-01-16T16:45:00.000-0500"
"PLAT-1527","Migrate legacy authentication service","In Progress","21",""
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (401) Unauthorized` | Verify your Jira username and API token are correct; generate a new token at https://id.atlassian.com/manage-profile/security/api-tokens if expired. |
    | `jq: error (at <stdin>:1): Cannot index number with string "fields"` | The custom field ID `customfield_10016` may not exist in your instance; run `curl -u user:token "https://your-instance.atlassian.net/rest/api/2/field" | jq '.[] | select(.name=="Story Points")'` to find the correct field ID. |
    | `curl: (400) Bad Request` | Ensure the JQL syntax is valid by testing it in the Jira UI search bar first, and verify the instance URL matches your Jira domain exactly. |
| Report | Location in Jira | Frequency |
|--------|-----------------|-----------|
| Sprint Report | Board → Reports → Sprint Report | End of each sprint |
| Velocity | Board → Reports → Velocity Chart | Sprint planning |
| Burndown | Board → Reports → Burndown | Daily standup |
| CFD | Board → Reports → Cumulative Flow | Weekly |
| Created vs Resolved | Project → Reports → Created vs Resolved | Monthly |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Jira — Health Checks](../health-checks/)
- [Jira — CLI Reference](../cli-reference/)
- [Jira — Common Issues](../../troubleshooting/common-issues/)
