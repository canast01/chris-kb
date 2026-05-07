# Jira Boards

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
