# Jira — Components

## Boards

Kanban vs Scrum boards, swimlanes, board configuration, and saved filters.

## Kanban vs Scrum Boards

| Feature | Kanban | Scrum |
|---------|--------|-------|
| Sprints | No | Yes (time-boxed) |
| Backlog | Optional | Yes |
| Velocity tracking | No | Yes |
| WIP limits | Yes | No |
| Best for | Continuous flow, ops | Feature development |
| Issue types | Any | Story, Task, Bug, Sub-task |

Choose Kanban for support queues and operational work. Choose Scrum for product/feature development with defined sprint goals.

## Creating and Configuring a Board

```bash
# Jira REST API — create a board
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/rest/agile/1.0/board" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Platform Team Board",
    "type": "scrum",
    "filterId": 12345
  }'

# Get board details
curl -u user:token \
  "https://your-instance.atlassian.net/rest/agile/1.0/board/10"

# List all boards
curl -u user:token \
  "https://your-instance.atlassian.net/rest/agile/1.0/board?projectKeyOrId=PLAT"
```

Board configuration lives at: **Board → Board Settings → Columns / Swimlanes / Quick Filters**.

## Columns and Workflows

Board columns map to workflow statuses. Adding a status to a column makes it appear in that column.

```
Typical Scrum column layout:
  To Do → In Progress → In Review → Done

Typical Kanban layout:
  Backlog → Selected → In Progress → Done
```

```bash
# Get column configuration for a board
curl -u user:token \
  "https://your-instance.atlassian.net/rest/agile/1.0/board/10/configuration"

# Move an issue to a new status (transition)
ISSUE="PLAT-123"
TRANSITION_ID=31   # get from /rest/api/2/issue/{key}/transitions
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/rest/api/2/issue/${ISSUE}/transitions" \
  -H "Content-Type: application/json" \
  -d "{\"transition\":{\"id\":\"${TRANSITION_ID}\"}}"
```

## Swimlanes

Swimlanes divide the board horizontally, grouping issues by a field.

| Swimlane Type | Groups By | Best For |
|--------------|----------|----------|
| Assignee | Person | Seeing per-person WIP |
| Epic | Epic link | Multi-epic sprint visibility |
| Query (JQL) | Custom JQL | Priority tiers, issue types |
| None | — | Flat board view |

Configure at: **Board Settings → Swimlanes**.

## Board Filters (JQL)

Every board is backed by a saved JQL filter. Fine-tuning it controls which issues appear.

```bash
# Get the filter backing a board
curl -u user:token \
  "https://your-instance.atlassian.net/rest/agile/1.0/board/10/configuration" \
  | jq '.filter'

# Update a saved filter
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/rest/api/2/filter/12345" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Platform Board Filter",
    "jql": "project = PLAT AND issuetype in standardIssueTypes() ORDER BY rank ASC"
  }'
```

Useful JQL for board filters:

```
# Active sprint + backlog for Scrum
project = PLAT AND sprint in openSprints() OR sprint = EMPTY ORDER BY rank ASC

# Kanban: exclude sub-tasks and epics
project = PLAT AND issuetype not in (Sub-task, Epic) ORDER BY rank ASC

# Quick filter: my issues
assignee = currentUser()

# Quick filter: high priority
priority in (Highest, High)
```

## Quick Filters

Quick filters are board-level toggles that apply additional JQL on top of the board filter.

```bash
# List quick filters for a board
curl -u user:token \
  "https://your-instance.atlassian.net/rest/agile/1.0/board/10/configuration" \
  | jq '.quickFilters'
```

Common quick filters to configure:
- `assignee = currentUser()` — My issues
- `priority in (Highest, High)` — High priority
- `issuetype = Bug` — Bugs only
- `sprint in openSprints()` — Current sprint

---

## Projects

Project types, scheme configuration, issue types, and permission management.

## Project Types

| Type | Board | Best For |
|------|-------|----------|
| Scrum | Scrum | Planned sprint-based development |
| Kanban | Kanban | Continuous flow, ops, support |
| Business | Timeline | Non-software project tracking |
| Service Management | Queue | IT service desk, incident triage |

```bash
# List all projects
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/project?expand=lead,description"

# Create a Scrum software project
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/rest/api/2/project" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "PLAT",
    "name": "Platform Engineering",
    "projectTypeKey": "software",
    "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
    "lead": "jsmith"
  }'

# Get project details
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/project/PLAT"
```

## Issue Type Schemes

Issue type schemes define which issue types are available in a project.

```bash
# List all issue type schemes
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/issuetypescheme"

# Get the scheme associated with a project
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/issuetypescheme/project?projectId=10001"

# List issue types for a project
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/issuetype/project?projectId=10001"
```

| Issue Type | Scope | Typical Use |
|-----------|-------|------------|
| Epic | Large body of work | Group related stories |
| Story | User-facing feature | Scrum unit of delivery |
| Task | Technical work | Infrastructure, chores |
| Bug | Defect | Regression, production issue |
| Sub-task | Child of any type | Breakdown of work |
| Spike | Research | Time-boxed investigation |

## Workflow Schemes

Workflows define the statuses and transitions available for each issue type.

```bash
# List workflow schemes
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/workflowscheme"

# Get the workflow scheme for a project
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/workflowscheme/project?projectId=10001"

# Get available transitions for an issue
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-42/transitions"

# Perform a transition
curl -u user:token -X POST \
  "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-42/transitions" \
  -H "Content-Type: application/json" \
  -d '{"transition": {"id": "31"}}'
```

## Permission Schemes

Permission schemes control who can create, edit, transition, and delete issues.

```bash
# List all permission schemes
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/permissionscheme"

# Get a specific scheme
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/permissionscheme/10000?expand=permissions"

# Get the permission scheme for a project
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/project/PLAT/permissionscheme"
```

| Permission | Typical Grantee | Notes |
|-----------|----------------|-------|
| Browse Projects | All users | Required for any access |
| Create Issues | Developers, PMs | Allow ticket creation |
| Edit Issues | Developers, PMs | Modify fields |
| Transition Issues | Developers | Move through workflow |
| Administer Projects | Project lead | Full project config |
| Delete Issues | Admins only | High risk — restrict tightly |

## Custom Fields

```bash
# List all custom fields
curl -u user:token \
  "https://your-instance.atlassian.net/rest/api/2/field" \
  | jq '.[] | select(.custom == true) | {id, name, type: .schema.type}'

# Set a custom field value on an issue
curl -u user:token -X PUT \
  "https://your-instance.atlassian.net/rest/api/2/issue/PLAT-42" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"customfield_10016": 5}}'
```
