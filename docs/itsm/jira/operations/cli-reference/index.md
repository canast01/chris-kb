---
tags:
  - jira
  - operations
---
# Jira — CLI Reference

```bash
export JIRA_URL="https://jira.example.com"
export JIRA_USER="admin@example.com"
export JIRA_TOKEN="your-api-token-or-PAT"

# Shorthand for Basic Auth header (base64 encoded)
export JIRA_AUTH=$(echo -n "${JIRA_USER}:${JIRA_TOKEN}" | base64)
```

```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123" | python3 -m json.tool
```
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123?fields=summary,status,assignee,priority" \
  | python3 -m json.tool
```
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
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/transitions" \
  | python3 -m json.tool
```
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
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X POST \
  -H "Content-Type: application/json" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/comment" \
  -d '{
    "body": "Reproduced in UAT. Escalating to senior dev."
  }'
```
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
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X POST \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@/path/to/screenshot.png" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/attachments"
```
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -G "${JIRA_URL}/rest/api/2/search" \
  --data-urlencode "jql=project = PROJ AND status = 'In Progress' AND assignee = jdoe" \
  --data-urlencode "fields=key,summary,status,assignee,priority" \
  --data-urlencode "maxResults=50" \
  | python3 -m json.tool
```
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
```bash
# macOS
brew install atlassian/taps/atlas

# Linux
curl -sL https://deb.cli.atlassian.com/install.sh | bash

# Verify
atlas version
```
```bash
atlas login
# Opens browser for OAuth authentication
```
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
```bash
# Start full reindex (background)
curl -u "${JIRA_USER}:${JIRA_TOKEN}" -X POST \
  "${JIRA_URL}/rest/api/2/reindex?type=BACKGROUND_PREFERRED"

# Check reindex progress
curl -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/reindex" | python3 -m json.tool
```
```bash
curl -u "${JIRA_USER}:${JIRA_TOKEN}" -X POST \
  "${JIRA_URL}/rest/api/2/jql/autocomplete/request/data/refresh"
```
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
```text
<field> <operator> <value> [AND|OR <field> <operator> <value>] [ORDER BY <field> ASC|DESC]
```
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

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Jira — Procedures](../procedures/)
- [Jira — Scripts](../scripts/)
- [Jira — Health Checks](../health-checks/)
