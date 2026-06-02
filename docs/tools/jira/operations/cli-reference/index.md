# Jira — CLI Reference


<div class="kb-summary">
CLI Reference reference covering Authentication Setup, REST API — curl Examples, Atlassian CLI (atlas), Admin Console Commands, JQL Query Reference.
</div>

## Authentication Setup

### Environment Variables

Set these in your shell profile or CI environment to avoid repeating credentials:

```bash
export JIRA_URL="https://jira.example.com"
export JIRA_USER="admin@example.com"
export JIRA_TOKEN="your-api-token-or-PAT"

# Shorthand for Basic Auth header (base64 encoded)
export JIRA_AUTH=$(echo -n "${JIRA_USER}:${JIRA_TOKEN}" | base64)
```
```
┌──────────────────────────────────────── Jira — CLI Reference ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Jira Admin CLI — run on server as jira OS user                        │   │
│   │             ./start-jira.sh / ./stop-jira.sh — start/stop Jira application server             │   │
│   │               curl http://localhost:8080/status — returns JSON with state field               │   │
│   │             psql -U jira jira -c "SELECT count(*) FROM jiraissue;" — count issues             │   │
│   │                 pg_dump -Fc -U jira jira -f /backup/jira_$(date +%Y%m%d).dump                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SSH to Jira server · run as jira OS user · DB on PostgreSQL VM                                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  start-jira.sh  = JIRA_INSTALL/bin/start-jira.sh; starts Tomcat JVM process                           │
│  stop-jira.sh   = graceful shutdown; waits for active requests to complete                            │
│  GET /status    = REST endpoint; returns state: RUNNING, STARTING, STOPPING, ERROR                    │
│  jiraissue table = PostgreSQL table containing all Jira issues                                        │
│  pg_dump -Fc    = custom format dump; required for parallel pg_restore -j                             │
│  kill -3 PID    = SIGQUIT to JVM; thread dump printed to catalina.out                                 │
│  JIRA_INSTALL   = installation directory; contains bin/, conf/, atlassian-jira/                       │
│  JIRA_HOME      = data directory; attachments/, indexes/, plugins/, log/                              │
│  catalina.out   = Tomcat stdout; JIRA_INSTALL/logs/catalina.out                                       │
│  atlassian-jira.log = Jira application log; JIRA_HOME/log/atlassian-jira.log                          │
│  jira-application.properties = JIRA_HOME config; sets jira.home and cluster config                    │
│  dbconfig.xml   = JIRA_HOME; JDBC connection settings; edit to change DB params                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## REST API — curl Examples

### Get Issue

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123" | python3 -m json.tool
```

Specific fields only:

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123?fields=summary,status,assignee,priority" \
  | python3 -m json.tool
```

### Create Issue

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X POST \
  -H "Content-Type: application/json" \
  "${JIRA_URL}/rest/api/2/issue" \
  -d '{
    "fields": {
      "project":     { "key": "PROJ" },
      "issuetype":   { "name": "Bug" },
      "summary":     "Login fails on Safari 17",
      "description": "Steps to reproduce:\n1. Open Safari 17\n2. Navigate to /login\n3. Submit credentials\n\nExpected: Successful login\nActual: HTTP 500",
      "priority":    { "name": "High" },
      "assignee":    { "name": "jdoe" },
      "labels":      ["frontend", "safari"],
      "components":  [{ "name": "Authentication" }]
    }
  }' | python3 -m json.tool
```

### Update Issue Fields

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X PUT \
  -H "Content-Type: application/json" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123" \
  -d '{
    "fields": {
      "summary":  "Login fails on Safari 17 — REGRESSION",
      "priority": { "name": "Critical" },
      "assignee": { "name": "jsmith" }
    }
  }'
```

### Transition Issue (Update Status)

First, get available transitions:

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/transitions" \
  | python3 -m json.tool
```

Then execute the transition by ID:

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X POST \
  -H "Content-Type: application/json" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/transitions" \
  -d '{
    "transition": { "id": "31" },
    "fields": {
      "resolution": { "name": "Fixed" }
    },
    "update": {
      "comment": [{
        "add": { "body": "Transitioning to Done — fix deployed to prod." }
      }]
    }
  }'
```

### Add Comment

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X POST \
  -H "Content-Type: application/json" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/comment" \
  -d '{
    "body": "Reproduced in UAT. Escalating to senior dev."
  }'
```

### Add Worklog

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X POST \
  -H "Content-Type: application/json" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/worklog" \
  -d '{
    "timeSpent": "3h 30m",
    "comment": "Investigated root cause and implemented fix",
    "started": "2026-05-08T09:00:00.000+0000"
  }'
```

### Attach File

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X POST \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@/path/to/screenshot.png" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/attachments"
```

### Search with JQL

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -G "${JIRA_URL}/rest/api/2/search" \
  --data-urlencode "jql=project = PROJ AND status = 'In Progress' AND assignee = jdoe" \
  --data-urlencode "fields=key,summary,status,assignee,priority" \
  --data-urlencode "maxResults=50" \
  | python3 -m json.tool
```

### Bulk Operations

Bulk transition all issues matching a JQL filter:

```bash
#!/bin/bash
# bulk-transition.sh — Transition all matching issues to a target status
JQL="project = PROJ AND status = 'To Do' AND sprint in openSprints()"
TARGET_TRANSITION_ID="21"  # "In Progress"

# Fetch all issue keys
KEYS=$(curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -G "${JIRA_URL}/rest/api/2/search" \
  --data-urlencode "jql=${JQL}" \
  --data-urlencode "fields=key" \
  --data-urlencode "maxResults=200" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for issue in data['issues']:
    print(issue['key'])
")

for KEY in ${KEYS}; do
  echo "Transitioning ${KEY}..."
  curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
    -X POST \
    -H "Content-Type: application/json" \
    "${JIRA_URL}/rest/api/2/issue/${KEY}/transitions" \
    -d "{\"transition\": {\"id\": \"${TARGET_TRANSITION_ID}\"}}"
  echo ""
done
```

---

## Atlassian CLI (atlas)

The `atlas` CLI is Atlassian's official tool for Jira Cloud administration tasks.

### Installation

```bash
# macOS
brew install atlassian/taps/atlas

# Linux
curl -sL https://deb.cli.atlassian.com/install.sh | bash

# Verify
atlas version
```

### Login

```bash
atlas login
# Opens browser for OAuth authentication
```

### Common atlas Commands

```bash
# List all sites
atlas admin sites list

# Create a Jira issue
atlas jira issue create \
  --project PROJ \
  --type Story \
  --summary "Implement rate limiting on API gateway" \
  --description "Add rate limiting to prevent abuse" \
  --assignee jdoe@example.com

# View an issue
atlas jira issue view PROJ-123

# Move issue to a status
atlas jira issue transition PROJ-123 "In Progress"

# List sprints
atlas jira board sprint list --board-id 42

# Run JQL search
atlas jira issue list --jql "project = PROJ AND priority = Critical"
```

---

## Admin Console Commands

### Jira Service Control (Linux systemd)

```bash
# Start / Stop / Restart
systemctl start jira
systemctl stop jira
systemctl restart jira
systemctl status jira

# View live logs
journalctl -u jira -f

# Jira bundled start/stop scripts
/opt/atlassian/jira/bin/start-jira.sh
/opt/atlassian/jira/bin/stop-jira.sh
```

### Reindex via REST

```bash
# Start full reindex (background)
curl -u "${JIRA_USER}:${JIRA_TOKEN}" -X POST \
  "${JIRA_URL}/rest/api/2/reindex?type=BACKGROUND_PREFERRED"

# Check reindex progress
curl -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/reindex" | python3 -m json.tool
```

### Clear Caches via REST

```bash
curl -u "${JIRA_USER}:${JIRA_TOKEN}" -X POST \
  "${JIRA_URL}/rest/api/2/jql/autocomplete/request/data/refresh"
```

Via UI: `Admin → System → Caches & Services → Flush all caches`

### User Management via REST

```bash
# Get user details
curl -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/user?username=jdoe"

# Deactivate user
curl -u "${JIRA_USER}:${JIRA_TOKEN}" -X PUT \
  -H "Content-Type: application/json" \
  "${JIRA_URL}/rest/api/2/user?username=jdoe" \
  -d '{"active": false}'

# List all users in a group
curl -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/group/member?groupname=jira-developers&maxResults=100"
```

---

## JQL Query Reference

### Syntax

```text
<field> <operator> <value> [AND|OR <field> <operator> <value>] [ORDER BY <field> ASC|DESC]
```

### Field Reference

| Field | Type | Example |
|---|---|---|
| `project` | Project key/name | `project = PROJ` |
| `issuetype` | Issue type name | `issuetype = Bug` |
| `status` | Status name | `status = "In Progress"` |
| `assignee` | Username / function | `assignee = currentUser()` |
| `reporter` | Username | `reporter = jdoe` |
| `priority` | Priority name | `priority in (High, Critical)` |
| `labels` | Label text | `labels = "regression"` |
| `component` | Component name | `component = "Authentication"` |
| `fixVersion` | Version name | `fixVersion = "2.1.0"` |
| `affectedVersion` | Version name | `affectedVersion = "2.0.0"` |
| `sprint` | Sprint function | `sprint in openSprints()` |
| `created` | Date | `created >= -7d` |
| `updated` | Date | `updated >= "2026-01-01"` |
| `resolved` | Date | `resolved >= startOfMonth()` |
| `duedate` | Date | `duedate < now() AND status != Done` |
| `text` | Full-text search | `text ~ "authentication error"` |
| `summary` | Summary text | `summary ~ "login"` |
| `description` | Description text | `description ~ "timeout"` |
| `comment` | Comment text | `comment ~ "escalated"` |
| `watcher` | Username | `watcher = currentUser()` |
| `votes` | Number | `votes > 5` |

### Operators

| Operator | Description | Example |
|---|---|---|
| `=` | Equals | `status = Done` |
| `!=` | Not equals | `status != Done` |
| `>` `<` `>=` `<=` | Comparison | `created >= -7d` |
| `~` | Contains (text) | `summary ~ "timeout"` |
| `!~` | Does not contain | `summary !~ "spike"` |
| `in` | In list | `status in ("To Do", "In Progress")` |
| `not in` | Not in list | `status not in (Done, Closed)` |
| `is EMPTY` | Field is empty | `assignee is EMPTY` |
| `is not EMPTY` | Field is set | `fixVersion is not EMPTY` |
| `was` | Historical value | `status was "In Progress"` |
| `changed` | Field changed | `status changed` |
| `changed to` | Changed to value | `status changed to Done` |
| `changed from` | Changed from value | `status changed from "To Do"` |
| `changed by` | Changed by user | `status changed by jdoe` |

### Functions

| Function | Description | Example |
|---|---|---|
| `currentUser()` | Logged-in user | `assignee = currentUser()` |
| `openSprints()` | Active sprints | `sprint in openSprints()` |
| `closedSprints()` | Completed sprints | `sprint in closedSprints()` |
| `now()` | Current date/time | `duedate < now()` |
| `startOfDay()` | Start of today | `created >= startOfDay()` |
| `startOfWeek()` | Start of this week | `created >= startOfWeek()` |
| `startOfMonth()` | Start of this month | `resolved >= startOfMonth()` |
| `startOfYear()` | Start of this year | `created >= startOfYear()` |
| `membersOf()` | Users in group | `assignee in membersOf("jira-developers")` |
| `projectsLeadByUser()` | Projects led by user | `project in projectsLeadByUser()` |

### Common JQL Queries

```jql
-- My open items
assignee = currentUser() AND status != Done ORDER BY priority DESC

-- Critical unresolved bugs
issuetype = Bug AND priority = Critical AND status != Done ORDER BY created ASC

-- Sprint overview
project = PROJ AND sprint in openSprints() ORDER BY status ASC, priority DESC

-- Overdue issues
duedate < now() AND status != Done AND status != Closed ORDER BY duedate ASC

-- Unassigned high-priority
priority in (High, Critical) AND assignee is EMPTY AND status != Done

-- Recently closed (last 7 days)
status changed to Done after -7d ORDER BY resolved DESC

-- Stuck in progress (over 5 days)
status = "In Progress" AND status changed to "In Progress" before -5d

-- Issues blocking others
issueFunction in issuesWithLinks("blocks") AND status != Done

-- Regression bugs in current release
issuetype = Bug AND labels = regression AND fixVersion in unreleasedVersions()

-- Full-text search across project
project = PROJ AND text ~ "authentication timeout" ORDER BY updated DESC
```
