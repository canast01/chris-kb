# Jira Reporting

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

## Cumulative Flow Diagram (CFD)

CFD shows how many issues are in each status over time. Widening bands indicate bottlenecks.

```bash
# Fetch CFD data
curl -u user:token \
  "https://your-instance.atlassian.net/rest/greenhopper/1.0/rapid/charts/cumulativeflowdiagram?rapidViewId=10&swimlaneId=0&fromDate=2025-01-01&toDate=2025-03-31"
```

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

| Report | Location in Jira | Frequency |
|--------|-----------------|-----------|
| Sprint Report | Board → Reports → Sprint Report | End of each sprint |
| Velocity | Board → Reports → Velocity Chart | Sprint planning |
| Burndown | Board → Reports → Burndown | Daily standup |
| CFD | Board → Reports → Cumulative Flow | Weekly |
| Created vs Resolved | Project → Reports → Created vs Resolved | Monthly |
