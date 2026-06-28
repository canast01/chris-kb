---
tags:
  - servicenow
---
# Change Request (RFC)

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

