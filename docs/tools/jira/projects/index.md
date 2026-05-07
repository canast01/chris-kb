# Jira Projects

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
