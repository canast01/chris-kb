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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`command not found: base64`** — Install coreutils package (`apt-get install coreutils` on Debian/Ubuntu or `brew install coreutils` on macOS).
    **`export: not valid in this context`** — Ensure you are running these commands in a bash shell, not sh or dash; use `bash` explicitly if needed.
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123" | python3 -m json.tool
```

```text title="Expected output"
{
  "expand": "changelog,names,schema,transitions,operations,editmeta,changelog,versionedRepresentations",
  "id": "10042",
  "key": "PROJ-123",
  "self": "https://jira.company.com/rest/api/2/issue/10042",
  "fields": {
    "summary": "Update authentication module for OAuth2 compliance",
    "description": "Implement OAuth2 token refresh mechanism",
    "status": {
      "self": "https://jira.company.com/rest/api/2/status/3",
      "description": "In Progress",
      "iconUrl": "https://jira.company.com/images/icons/statuses/inprogress.png",
      "name": "In Progress",
      "id": "3"
    },
    "assignee": {
      "self": "https://jira.company.com/rest/api/2/user?username=jsmith",
      "name": "jsmith",
      "emailAddress": "jsmith@company.com",
      "displayName": "John Smith"
    },
    "priority": {
      "self": "https://jira.company.com/rest/api/2/priority/2",
      "iconUrl": "https://jira.company.com/images/icons/priorities/high.png",
      "name": "High",
      "id": "2"
    },
    "created": "2024-01-15T09:23:44.000-0500",
    "updated": "2024-01-18T14:52:12.000-0500"
  }
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.company.com port 443: Connection refused`** — Verify `$JIRA_URL` is correct and the Jira instance is accessible from your network.
    **`{"errorMessages":["Issue does not exist or you do not have permission to see it."]}`** — Confirm the issue key exists and your `$JIRA_USER` account has permission to view it.
    **`curl: (401) Unauthorized`** — Ensure `$JIRA_TOKEN` is a valid API token and `$JIRA_USER` matches the token owner.
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123?fields=summary,status,assignee,priority" \
  | python3 -m json.tool
```

```text title="Expected output"
{
  "expand": "changelog,names,operations,versionedRepresentations,editmeta,changelog,names",
  "id": "10042",
  "key": "PROJ-123",
  "self": "https://jira.company.com/rest/api/2/issue/10042",
  "fields": {
    "summary": "Update load balancer configuration for prod cluster",
    "status": {
      "self": "https://jira.company.com/rest/api/2/status/3",
      "description": "In Progress",
      "iconUrl": "https://jira.company.com/images/icons/statuses/inprogress.png",
      "name": "In Progress",
      "id": "3"
    },
    "assignee": {
      "self": "https://jira.company.com/rest/api/2/user?username=jsmith",
      "name": "jsmith",
      "emailAddress": "jsmith@company.com",
      "displayName": "John Smith",
      "active": true
    },
    "priority": {
      "self": "https://jira.company.com/rest/api/2/priority/2",
      "iconUrl": "https://jira.company.com/images/icons/priorities/high.png",
      "name": "High",
      "id": "2"
    }
  }
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.company.com port 443: Connection refused`** — Verify the JIRA_URL environment variable is correct and the Jira instance is accessible from your network.
    **`{"errorMessages":["Issue does not exist or you do not have permission to see it."]}`** — Confirm PROJ-123 exists and your JIRA_USER has permission to view the issue.
    **`curl: (401) Unauthorized`** — Ensure JIRA_TOKEN is a valid API token and JIRA_USER matches the token owner account.
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

```text title="Expected output"
{
  "id": "10847",
  "key": "PROJ-2891",
  "self": "https://jira.company.com/rest/api/2/issue/10847",
  "changelog": {
    "histories": []
  }
}
```

!!! warning "Common errors"
    **`"errorMessages": ["Field 'assignee' cannot be set. It is not on the appropriate screen, or unknown."]`** — Remove the assignee field from the request or verify the user exists and the field is available in your Jira workflow.
    **`curl: (7) Failed to connect to jira.company.com port 443: Connection refused`** — Verify the JIRA_URL environment variable is set correctly and the Jira instance is accessible from your network.
    **`"errorMessages": ["Component with name 'Authentication' does not exist or you do not have permission to see it."]`** — Replace the component name with a valid component key or verify the component exists in the PROJ project.
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

```text title="Expected output"
{
  "id": "10847",
  "key": "PROJ-123",
  "self": "https://jira.company.com/rest/api/2/issue/10847"
}
```

!!! warning "Common errors"
    **`"errorMessages":["Field 'assignee' cannot be set. It is not on the appropriate screen, or unknown."]`** — Verify the assignee username exists and is valid in your Jira instance; use `/rest/api/2/user/search?username=jsmith` to confirm.
    **`curl: (7) Failed to connect to jira.company.com port 443: Connection refused`** — Ensure `${JIRA_URL}` is set correctly and the Jira server is reachable; test with `curl -I ${JIRA_URL}`.
    **`"errorMessages":["You do not have permission to edit this issue"]`** — Verify that `${JIRA_USER}` has Edit permission on PROJ-123; check issue permissions in Jira or contact your Jira administrator.
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/transitions" \
  | python3 -m json.tool
```

```text title="Expected output"
{
  "expand": "transitions",
  "transitions": [
    {
      "id": "11",
      "name": "In Progress",
      "to": {
        "self": "https://jira.example.com/rest/api/2/status/3",
        "description": "This issue is being actively worked on.",
        "iconUrl": "https://jira.example.com/images/icons/statuses/inprogress.png",
        "name": "In Progress",
        "id": "3",
        "statusCategory": {
          "self": "https://jira.example.com/rest/api/2/statuscategory/4",
          "id": 4,
          "key": "indeterminate",
          "colorName": "yellow",
          "name": "In Progress"
        }
      }
    },
    {
      "id": "21",
      "name": "Done",
      "to": {
        "self": "https://jira.example.com/rest/api/2/status/10000",
        "description": "Work has finished on this issue.",
        "iconUrl": "https://jira.example.com/images/icons/statuses/done.png",
        "name": "Done",
        "id": "10000",
        "statusCategory": {
          "self": "https://jira.example.com/rest/api/2/statuscategory/3",
          "id": 3,
          "key": "done",
          "colorName": "green",
          "name": "Done"
        }
      }
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.example.com port 443: Connection refused`** — Verify the JIRA_URL environment variable is set correctly and the Jira instance is accessible from your network.
    **`{"errorMessages":["Issue does not exist or you do not have permission to see it."],"errors":{}}`** — Confirm PROJ-123 exists, check that JIRA_USER has browse permissions on the project, and verify JIRA_TOKEN is valid and not expired.
    **`command not found: python3`** — Install Python 3 or use `jq` instead: `curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" "${JIRA_URL}/rest/api/2/issue/PROJ-123/transitions" | jq .`
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

```text title="Expected output"
{
  "id": "10047",
  "key": "PROJ-123",
  "self": "https://jira.company.com/rest/api/2/issue/10047",
  "transitions": [
    {
      "id": "31",
      "name": "Done",
      "to": {
        "self": "https://jira.company.com/rest/api/2/status/10000",
        "description": "Work has been completed",
        "iconUrl": "https://jira.company.com/images/icons/statuses/done.png",
        "name": "Done",
        "id": "10000",
        "statusCategory": {
          "self": "https://jira.company.com/rest/api/2/statuscategory/3",
          "id": 3,
          "key": "done",
          "colorName": "green",
          "name": "Done"
        }
      }
    }
  ]
}
```

!!! warning "Common errors"
    **`{"errorMessages":["User 'automation' does not have permission to transition issue"],"errors":{}}`** — Verify the JIRA_USER account has the "Transition Issues" permission in the project's permission scheme.
    **`{"errorMessages":["Field 'resolution' cannot be set. It is not on the appropriate screen, or unknown."],"errors":{}}`** — Remove the resolution field or confirm it is available on the transition screen for workflow state 31 in your JIRA configuration.
    **`curl: (7) Failed to connect to jira.company.com port 443: Connection refused`** — Verify JIRA_URL is correct and the JIRA instance is accessible from your network (check firewall rules and VPN connectivity).
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X POST \
  -H "Content-Type: application/json" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/comment" \
  -d '{
    "body": "Reproduced in UAT. Escalating to senior dev."
  }'
```

```text title="Expected output"
{
  "self": "https://jira.company.com/rest/api/2/issue/PROJ-123/comment/10047",
  "id": "10047",
  "author": {
    "self": "https://jira.company.com/rest/api/2/user?username=devops.admin",
    "name": "devops.admin",
    "emailAddress": "devops.admin@company.com",
    "displayName": "DevOps Admin",
    "active": true
  },
  "body": "Reproduced in UAT. Escalating to senior dev.",
  "updateAuthor": {
    "self": "https://jira.company.com/rest/api/2/user?username=devops.admin",
    "name": "devops.admin"
  },
  "created": "2024-01-15T14:32:18.447-0500",
  "updated": "2024-01-15T14:32:18.447-0500",
  "visibility": {
    "type": "role",
    "value": "Developers"
  }
}
```

!!! warning "Common errors"
    **`{"errorMessages":["Issue does not exist or you do not have permission to see it."],"errors":{}}`** — Verify PROJ-123 exists and your JIRA_USER has browse/comment permissions on that project.
    **`curl: (6) Could not resolve host: jira.company.com`** — Ensure JIRA_URL environment variable is set correctly and the Jira instance is reachable from your network.
    **`{"errorMessages":["You must provide a body."],"errors":{}}`** — Confirm the JSON payload includes a non-empty "body" field in the -d argument.
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

```text title="Expected output"
{
  "self": "https://jira.company.com/rest/api/2/issue/PROJ-123/worklog/10847",
  "author": {
    "self": "https://jira.company.com/rest/api/2/user?username=devops.admin",
    "name": "devops.admin",
    "emailAddress": "devops.admin@company.com",
    "avatarUrls": {
      "48x48": "https://jira.company.com/secure/useravatar?avatarId=10452"
    },
    "displayName": "DevOps Admin",
    "active": true
  },
  "updateAuthor": {
    "self": "https://jira.company.com/rest/api/2/user?username=devops.admin",
    "name": "devops.admin",
    "displayName": "DevOps Admin",
    "active": true
  },
  "created": "2026-05-08T14:22:31.547+0000",
  "updated": "2026-05-08T14:22:31.547+0000",
  "timeSpent": "3h 30m",
  "timeSpentSeconds": 12600,
  "id": "10847",
  "comment": "Investigated root cause and implemented fix",
  "started": "2026-05-08T09:00:00.000+0000"
}
```

!!! warning "Common errors"
    **`{"errorMessages":["Authentication failed; please check you have supplied the correct credentials."],"errors":{}}`** — Verify `JIRA_USER` and `JIRA_TOKEN` environment variables are set correctly and the token has API access permissions.
    **`{"errorMessages":["Issue does not exist or you do not have permission to see it."],"errors":{}}`** — Confirm the issue key PROJ-123 exists in your Jira instance and your user account has permission to view and log work on it.
    **`{"errorMessages":["You do not have permission to create worklog on this issue."],"errors":{}}`** — Ensure your Jira user role has the "Log Work" permission assigned in the project's permission scheme.
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -X POST \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@/path/to/screenshot.png" \
  "${JIRA_URL}/rest/api/2/issue/PROJ-123/attachments"
```

```text title="Expected output"
{
  "id": 10042,
  "self": "https://jira.company.com/rest/api/2/attachment/10042",
  "filename": "screenshot.png",
  "author": {
    "self": "https://jira.company.com/rest/api/2/user?username=devops.admin",
    "name": "devops.admin",
    "emailAddress": "devops.admin@company.com",
    "avatarUrls": {
      "48x48": "https://jira.company.com/secure/useravatar?size=large&ownerId=devops.admin"
    },
    "displayName": "DevOps Admin",
    "active": true
  },
  "created": "2024-01-15T14:32:18.547+0000",
  "size": 245678,
  "mimeType": "image/png",
  "content": "https://jira.company.com/secure/attachment/10042/screenshot.png",
  "thumbnail": "https://jira.company.com/secure/thumbnail/10042/_/screenshot.png"
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.company.com port 443: Connection refused`** — Verify the JIRA_URL environment variable is set correctly and the Jira instance is accessible from your network.
    **`{"errorMessages":["Issue does not exist or you do not have permission to see it."],"errors":{}}`** — Confirm PROJ-123 exists, the issue key is correct, and your JIRA_USER has permission to attach files to that issue.
    **`curl: (26) Failed to open/read local data from "/path/to/screenshot.png"`** — Replace `/path/to/screenshot.png` with the actual absolute path to an existing file.
```bash
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -G "${JIRA_URL}/rest/api/2/search" \
  --data-urlencode "jql=project = PROJ AND status = 'In Progress' AND assignee = jdoe" \
  --data-urlencode "fields=key,summary,status,assignee,priority" \
  --data-urlencode "maxResults=50" \
  | python3 -m json.tool
```

```text title="Expected output"
{
  "expand": "names,schemas",
  "startAt": 0,
  "maxResults": 50,
  "total": 3,
  "issues": [
    {
      "expand": "changelog,html",
      "id": "10042",
      "key": "PROJ-1847",
      "self": "https://jira.company.com/rest/api/2/issue/10042",
      "fields": {
        "summary": "Update database connection pooling configuration",
        "status": {
          "self": "https://jira.company.com/rest/api/2/status/3",
          "description": "In Progress",
          "iconUrl": "https://jira.company.com/images/icons/statuses/inprogress.png",
          "name": "In Progress",
          "id": "3"
        },
        "priority": {
          "self": "https://jira.company.com/rest/api/2/priority/2",
          "iconUrl": "https://jira.company.com/images/icons/priorities/high.png",
          "name": "High",
          "id": "2"
        },
        "assignee": {
          "self": "https://jira.company.com/rest/api/2/user?username=jdoe",
          "name": "jdoe",
          "emailAddress": "jdoe@company.com",
          "displayName": "John Doe"
        }
      }
    },
    {
      "key": "PROJ-1823",
      "fields": {
        "summary": "Implement SSL certificate renewal automation",
        "status": {"name": "In Progress", "id": "3"},
        "priority": {"name": "Medium", "id": "3"},
        "assignee": {"name": "jdoe", "displayName": "John Doe"}
      }
    },
    {
      "key": "PROJ-1801",
      "fields": {
        "summary": "Review infrastructure monitoring alerts",
        "status": {"name": "In Progress", "id": "3"},
        "priority": {"name": "Low", "id": "4"},
        "assignee": {"name": "jdoe", "displayName": "John Doe"}
      }
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.company.com port 443: Connection refused`** — Verify the JIRA_URL environment variable is set correctly and the Jira server is accessible from your network.
    **`401 Unauthorized`** — Ensure JIRA_USER and JIRA_TOKEN environment variables are set with valid credentials and the token has API access permissions.
    **`jq: parse error: Invalid JSON`** — Confirm the Jira API endpoint is returning valid JSON; check that the API version (rest/api/2) matches your Jira instance version.
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

```text title="Expected output"
Transitioning PROJ-1847...
Transitioning PROJ-1848...
Transitioning PROJ-1849...
Transitioning PROJ-1850...
Transitioning PROJ-1851...
Transitioning PROJ-1852...
Transitioning PROJ-1853...
Transitioning PROJ-1854...
...
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.example.com port 443: Connection refused`** — Verify `${JIRA_URL}` is correct and the Jira instance is running and accessible from this host.
    **`"errorMessages":["You do not have permission to transition this issue"]`** — Ensure `${JIRA_USER}` has the "Transition Issues" permission in the target project.
    **`"errorMessages":["Transition id 21 is invalid"]`** — Verify transition ID 21 exists for the target status by running `curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" "${JIRA_URL}/rest/api/2/issue/PROJ-1847/transitions" | python3 -m json.tool` and checking the available IDs.
```bash
# macOS
brew install atlassian/taps/atlas

# Linux
curl -sL https://deb.cli.atlassian.com/install.sh | bash

# Verify
atlas version
```

```text title="Expected output"
==> Downloading https://github.com/atlassian/cli/releases/download/v2.14.3/atlas-darwin-arm64.tar.gz
==> Downloading https://github.com/atlassian/cli/releases/download/v2.14.3/atlas-darwin-arm64.tar.gz
==> Installing atlassian/taps/atlas
==> /usr/local/Cellar/atlas/2.14.3
🍺  atlas@2.14.3 installed successfully

atlas version 2.14.3 (build 2024-01-15)
```

!!! warning "Common errors"
    **`Error: No available formula with the name "atlassian/taps/atlas"`** — Run `brew tap atlassian/taps` first to add the Atlassian tap repository.
    **`curl: (7) Failed to connect to deb.cli.atlassian.com port 443`** — Verify internet connectivity and check that your firewall/proxy allows HTTPS access to Atlassian's package repository.
    **`atlas: command not found`** — Ensure the installation completed without errors and that `/usr/local/bin` (macOS) or `/usr/local/bin` (Linux) is in your `$PATH` environment variable.
```bash
atlas login
# Opens browser for OAuth authentication
```

```text title="Expected output"
Opening browser for authentication...
Waiting for authentication to complete...
Successfully authenticated as: john.smith@company.com
Session token stored in: /home/jsmith/.atlasrc
Authentication complete. You can now use atlas CLI commands.
```

!!! warning "Common errors"
    **`Error: Failed to open browser. Please visit https://auth.atlassian.com/authorize?client_id=abc123... manually`** — Set the `BROWSER` environment variable or manually open the provided URL in your browser and paste the verification code.
    **`Error: Authentication timeout after 5 minutes`** — Re-run `atlas login` and complete the OAuth flow within the time limit, or check your network connectivity.
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

```text title="Expected output"
$ atlas admin sites list
SITE_ID                              NAME                 STATUS    REGION
site-prod-us-east-1                  Production US-East   ACTIVE    us-east-1
site-prod-eu-west-1                  Production EU-West   ACTIVE    eu-west-1
site-staging-us-east-1               Staging US-East      ACTIVE    us-east-1

$ atlas jira issue create --project PROJ --type Story --summary "Implement rate limiting on API gateway" --description "Add rate limiting to prevent abuse" --assignee jdoe@example.com
Issue created successfully.
Key: PROJ-4521
URL: https://jira.example.com/browse/PROJ-4521

$ atlas jira issue view PROJ-123
Key:         PROJ-123
Summary:     Fix authentication timeout issue
Type:        Bug
Status:      Open
Assignee:    jdoe@example.com
Priority:    High
Created:     2024-01-15T09:32:14.000Z
Updated:     2024-01-16T14:22:08.000Z

$ atlas jira issue transition PROJ-123 "In Progress"
Transitioned PROJ-123 to In Progress

$ atlas jira board sprint list --board-id 42
SPRINT_ID    NAME              STATE      START_DATE           END_DATE
1847         Sprint 24         ACTIVE     2024-01-08           2024-01-22
1848         Sprint 25         FUTURE     2024-01-23           2024-02-05
1849         Sprint 26         FUTURE     2024-02-06           2024-02-20

$ atlas jira issue list --jql "project = PROJ AND priority = Critical"
KEY       SUMMARY                                    STATUS         ASSIGNEE
PROJ-119  Database connection pool exhaustion        In Progress    msmith@example.com
PROJ-245  SSL certificate expiration alert missing   Open           jdoe@example.com
PROJ-367  Memory leak in worker threads              In Progress    kchen@example.com
```

!!! warning "Common errors"
    **`Error: authentication failed — invalid credentials`** — Verify your Jira API token is set in `~/.atlas/config.yml` or the `ATLAS_JIRA_TOKEN` environment variable.
    **`Error: project PROJ not found`** — Confirm the project key exists and you have permission to access it by running `atlas jira project list`.
    **`Error: user jdoe@example.com not found in this instance`** — Verify the email address is correct and the user account exists in your Jira instance.
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

```text title="Expected output"
● jira.service - Atlassian JIRA
     Loaded: loaded (/etc/systemd/system/jira.service; enabled; vendor preset: disabled)
     Active: active (running) since Thu 2024-01-18 14:32:15 UTC; 2min 43s ago
       Docs: https://confluence.atlassian.com/jira
    Process: 8742 ExecStart=/opt/atlassian/jira/bin/start-jira.sh (code=exited, status=0/SUCCESS)
   Main PID: 8751 (java)
      Tasks: 47 (limit: 4096)
     Memory: 1.2G
        CPU: 18s
     CGroup: /system.slice/jira.service
             └─8751 /usr/lib/jvm/java-11-openjdk-11.0.18.0.10-1.el7_9.x86_64/bin/java -Djava.awt.headless=true...

Jan 18 14:32:45 jira-prod-01 jira[8751]: 2024-01-18 14:32:45,123 INFO [main] [com.atlassian.jira.startup.JiraStartupLogger] JIRA started successfully in 30 seconds
Jan 18 14:32:46 jira-prod-01 jira[8751]: 2024-01-18 14:32:46,456 INFO [main] [com.atlassian.jira.upgrade.UpgradeManager] Upgrade check completed
```

!!! warning "Common errors"
    **`Job for jira.service failed because the control process exited with error code.`** — Check `/var/log/jira/catalina.out` for Java startup errors and verify sufficient heap memory is allocated in `setenv.sh`.
    **`Failed to start jira.service: Unit jira.service not found.`** — Ensure the systemd service file exists at `/etc/systemd/system/jira.service` and run `systemctl daemon-reload` after creating or modifying it.
    **`Permission denied`** — Run the command with `sudo` or ensure your user is in the `jira` group with `groups $USER`.
```bash
# Start full reindex (background)
curl -u "${JIRA_USER}:${JIRA_TOKEN}" -X POST \
  "${JIRA_URL}/rest/api/2/reindex?type=BACKGROUND_PREFERRED"

# Check reindex progress
curl -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/reindex" | python3 -m json.tool
```

```text title="Expected output"
{"taskId":"AO7D3E8F-1234-5678-90AB-CDEF12345678"}
{
  "currentIndex": 847293,
  "currentIndexedValue": "PROJ-8472",
  "description": "Reindexing issues in the background",
  "entityCount": 1205847,
  "finished": false,
  "progressUrl": "/secure/RapidBoard.jspa?rapidView=42",
  "running": true,
  "startTime": 1704067200000,
  "taskId": "AO7D3E8F-1234-5678-90AB-CDEF12345678"
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.example.com port 443: Connection refused`** — Verify `${JIRA_URL}` is correct and the Jira instance is running and accessible from your network.
    **`{"errorMessages":["User does not have permission to administer Jira"]}`** — Ensure `${JIRA_USER}` has Jira System Administrator permissions.
    **`curl: (6) Could not resolve host: jira.example.com`** — Check DNS resolution and network connectivity to the Jira hostname.
```bash
curl -u "${JIRA_USER}:${JIRA_TOKEN}" -X POST \
  "${JIRA_URL}/rest/api/2/jql/autocomplete/request/data/refresh"
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.example.com port 443: Connection refused`** — Verify the JIRA_URL environment variable is set correctly and the Jira instance is accessible from your network.
    **`curl: (401) Unauthorized`** — Ensure JIRA_USER and JIRA_TOKEN environment variables are set and the API token has appropriate permissions for the autocomplete endpoint.
    **`curl: (403) Forbidden`** — Confirm your Jira user account has the "Use REST APIs" global permission and access to the Jira instance.
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

```d2
direction: down

verify: "Verify" {shape: rectangle}

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
