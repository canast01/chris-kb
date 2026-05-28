# Change Request Procedure

A Request for Change (RFC) documents a planned modification to infrastructure, applications, or configuration. Every non-standard change requires an RFC before implementation.

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
┌──────────────────────────────────────── Change Request (RFC) ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        RFC: formal document capturing all change details for CAB review and audit trail       │   │
│   │        Incomplete RFCs returned by CAB; complete all mandatory fields before submission       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Mandatory Fields               │  │            Optional / Supporting            │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │          Title (short, descriptive)          │  │             Architecture diagram            │   │
│   │              Change type: S/N/E              │  │                Test evidence                │   │
│   │            Description and scope             │  │              Vendor runbook ref             │   │
│   │            Business justification            │  │          Config backup confirmation         │   │
│   │           Risk / impact assessment           │  │           Approval from app owner           │   │
│   │             Implementation steps             │  │            Change dependency list           │   │
│   │            Backout plan + trigger            │  │               Monitoring plan               │   │
│   │              Maintenance window              │  │              Communication plan             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │      Field       │       Type       │      Example      │    Mandatory     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   Change type    │     Dropdown     │       Normal      │       Yes        │      S/N/E       │   │
│   │       Risk       │     Dropdown     │       Medium      │       Yes        │     L/M/H/C      │   │
│   │      Window      │     Datetime     │   Sat 02:00 UTC   │       Yes        │   Duration too   │   │
│   │   Backout plan   │       Text       │    Step-by-step   │       Yes        │   With trigger   │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    S/N/E     = Standard / Normal / Emergency change type                                              │
│    Backout trigger= Defined condition that automatically initiates rollback (e.g., service fails test)│
│    Scope     = Exact systems, services, or components affected; used to notify correct teams          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
