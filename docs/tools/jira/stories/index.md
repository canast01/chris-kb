# Jira Stories

Story structure, acceptance criteria, story points, epics, and estimation.

## Story Structure

A well-formed user story answers: who needs this, what they need, and why.

```
Title:    [Short description — verb + outcome]
Format:   As a <role>, I want <capability> so that <benefit>

Example:
  As a platform engineer, I want S3 bucket lifecycle policies managed via
  Terraform so that storage costs are automatically optimised without manual
  cleanup scripts.
```

Required fields for a story ready for development:

| Field | Description | Example |
|-------|-------------|---------|
| Summary | One-line title | Add S3 lifecycle Terraform module |
| Description | User story + context | As a... / Background / Notes |
| Acceptance Criteria | Definition of Done | See below |
| Story Points | Effort estimate | 3 |
| Epic Link | Parent epic | PLAT-10: Storage Automation |
| Priority | Relative urgency | Medium |
| Assignee | Owner | @chris |
| Sprint | Target sprint | Sprint 24 |

## Acceptance Criteria

Acceptance criteria define when a story is complete. Use the Given/When/Then format or a plain checklist.

```
# Given/When/Then format
Given an S3 bucket with objects older than 30 days
When the lifecycle policy runs
Then objects are transitioned to S3-IA storage class
And objects older than 90 days are moved to Glacier
And objects older than 365 days are deleted

# Checklist format (simpler for technical stories)
- [ ] Terraform module created at modules/s3-lifecycle/
- [ ] Module accepts bucket_name and lifecycle_rules variables
- [ ] Applied to dev environment — no state drift
- [ ] README includes usage example
- [ ] Cost reduction validated in AWS Cost Explorer
```

## Story Points

Story points measure relative complexity, not time.

```bash
# Common Fibonacci scale
1 — Trivial change, well-understood
2 — Simple, minor unknowns
3 — Moderate complexity
5 — Complex, some research needed
8 — Very complex or large scope
13 — Should be split before estimating
```

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

## Story Splitting

Split large stories using these patterns:

```
# Patterns for splitting
By workflow step:     One story per step in a user workflow
By data type:         Separate stories for each entity/type
By interface:         API first, then UI
By acceptance criterion: Each criterion becomes its own story
By happy/unhappy path: Core flow first, error handling separate
By permission level:  Admin view, user view as separate stories
```

| Signal | Action |
|--------|--------|
| Story > 8 points | Split before sprint planning |
| Multiple "and" clauses in title | Each clause is a separate story |
| Multiple system touches | Split by system boundary |
| Unclear acceptance criteria | Spike first, then story |
