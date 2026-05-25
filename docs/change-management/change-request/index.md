# Change Request Procedure

A Request for Change (RFC) documents a planned modification to infrastructure, applications, or configuration. Every non-standard change requires an RFC before implementation.

```text
┌──────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌─────────────────┐
│  Raise RFC   │   │    Classify      │   │  Impact /        │   │    Assign /     │
│              │   │                  │   │  Risk Assess     │   │    Submit       │
│ Title / desc │   │ Standard →       │   │                  │   │                 │
│ Justification│──►│ pre-approved     │──►│ Impact × Likeli  │──►│ Service owner   │
│ Rollback plan│   │ Normal →         │   │ = Low/Med/High   │   │ → CAB queue     │
│ Impl steps   │   │ CAB required     │   │ Rollback tested? │   │ (5 biz days)    │
│ Validation   │   │ Emergency →      │   │                  │   │                 │
└──────────────┘   │ eCAB/on-call     │   └──────────────────┘   └─────────────────┘
                   └──────────────────┘
                                                   ┌─────────────────────────────────┐
                                                   │         RFC Lifecycle           │
                                                   │ Draft → Submitted → Reviewing → │
                                                   │ Approved → Scheduled →          │
                                                   │ In Progress → Completed         │
                                                   └─────────────────────────────────┘
```

## RFC Required Fields

| Field | Description | Required? |
|---|---|---|
| Title | Short description (< 80 chars) | Mandatory |
| Description | What will be changed and how | Mandatory |
| Business justification | Why this change is needed | Mandatory |
| Systems / CIs affected | List from CMDB | Mandatory |
| Risk assessment | Impact × Likelihood; risk score | Mandatory |
| Change type | Standard / Normal / Emergency | Mandatory |
| Maintenance window | Start/end datetime UTC | Mandatory |
| Rollback plan | Step-by-step reversal procedure | Mandatory |
| Test results | Non-prod evidence (High risk) | Required for High/Critical |
| Implementation steps | Numbered runbook | Mandatory |
| Post-change validation | Smoke tests / monitoring checks | Mandatory |
| Requester | Name and contact | Mandatory |
| Service owner | Name and email | Mandatory |

## RFC Template

```markdown
Title:          [INFRA] Upgrade PostgreSQL 14 → 15 on db-prod-01
Description:    In-place major version upgrade using pg_upgrade.
Justification:  PG14 EoL November 2026; security patches no longer issued.
Systems:        db-prod-01 (CMDB: CI-4421), app-server-01 (connection pool restart)
Risk:           Medium — major version change; pg_upgrade has been tested
Change Type:    Normal
Window:         2026-05-12 22:00 UTC – 2026-05-13 01:00 UTC
Rollback:       Restore from snapshot snap-xyz taken prior to upgrade; pg_upgrade preserves old cluster

Implementation Steps:
  1. Take VM snapshot at 21:50 UTC
  2. Stop application connection pool on app-server-01
  3. Stop postgresql-14.service
  4. Run: pg_upgrade -b /usr/lib/postgresql/14/bin -B /usr/lib/postgresql/15/bin -d /var/lib/postgresql/14/main -D /var/lib/postgresql/15/main
  5. Start postgresql-15.service
  6. Run ./analyze_new_cluster.sh
  7. Start application connection pool
  8. Smoke test: psql -c "SELECT version();" and application health check

Validation:
  - psql SELECT version() returns PostgreSQL 15.x
  - Application health endpoint returns HTTP 200
  - Error rate = 0% for 30 min post-restart

Rollback Steps:
  1. Stop postgresql-15
  2. Restore VM to snapshot snap-xyz
  3. Start postgresql-14
  4. Notify stakeholders
```

## RFC Submission Process

1. Create RFC in ITSM tool; link to relevant incident/problem if applicable
2. Attach supporting documents (test evidence, architecture diagrams)
3. Assign to service owner for review
4. Service owner submits to CAB queue (5 business days before window for Normal)
5. CAB reviews at weekly meeting; approves / rejects / requests changes
6. Requester notified of decision
7. On approval: schedule window; send stakeholder notifications

## Standard Change Register

Standard changes are pre-approved recurring activities that do not require individual RFC approval. Examples:

| Standard Change | Approval Path |
|---|---|
| Monthly OS patching (approved template) | Automated via patch management |
| SSL certificate renewal (automated) | No approval required |
| DNS record update (low-risk) | Team lead self-service |
| User access provisioning (IAM workflow) | HR-triggered workflow |

## RFC Status Lifecycle

```text
Draft → Submitted → Under Review → Approved / Rejected / Deferred
                                         ↓
                                   Scheduled → In Progress → Completed / Rolled Back
```
