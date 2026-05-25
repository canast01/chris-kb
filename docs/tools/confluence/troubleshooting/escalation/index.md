# Confluence — Escalation

This page defines the escalation process for Confluence incidents: who handles what, when to escalate, what to collect before raising a ticket, SLA expectations, and how to reach Atlassian Support in a production emergency.

---

## Escalation Matrix

| Level | Team / Role | Handles | Escalate When |
|---|---|---|---|
| **L1** | Service Desk / IT Helpdesk | Password resets, basic access issues, "how do I" questions, space permission requests | Issue requires server access, logs, or admin intervention |
| **L2** | Platform / Infrastructure Engineer | Application restarts, log analysis, plugin issues, LDAP sync, performance, backup/restore, upgrades | Cannot resolve within SLA; root cause unknown after 1 hour investigation; production down |
| **L3** | Senior Platform Engineer / Architect | Data corruption, cluster failures, complex upgrade issues, security incidents, cross-system integration failures | Requires Atlassian Support involvement; incident affects business-critical data |
| **Atlassian Support** | Atlassian Platinum / Premier Support | Product defects, confirmed bugs, DC cluster internals, licensing | Product bug confirmed; P1 production outage without L2/L3 resolution path |

---

## When to Escalate Immediately (P1 Criteria)

Escalate directly to L3 and open an Atlassian Support ticket **without waiting** if:

- Confluence is completely unavailable and cannot be restarted within 15 minutes
- Data loss is suspected (pages missing, attachments inaccessible)
- Database corruption detected
- Security incident: unauthorized access, data exfiltration suspicion
- Cluster split-brain persisting after node restart
- Upgrade failure with database schema partially migrated and no clean rollback path

---

## Information to Collect Before Escalating

Collect all of the following **before** contacting L3 or Atlassian. Providing this upfront avoids back-and-forth and reduces time-to-resolution significantly.

### Required for All Escalations

```text
[ ] Confluence version (Admin > System Information > Confluence Version)
[ ] Deployment type: Server / Data Center / Cloud
[ ] Number of cluster nodes (DC)
[ ] Java version: java -version
[ ] OS and kernel: uname -a
[ ] Database type and version: psql --version
[ ] Time of first occurrence (with timezone — e.g. 2026-05-08 09:15 UTC+2)
[ ] Symptoms description: what the user sees, error message (exact text)
[ ] Steps to reproduce (if reproducible)
[ ] Recent changes: upgrade, plugin install, config change, DB maintenance
[ ] Whether the issue is intermittent or constant
```

### Artifacts to Attach

```bash
# 1. Generate support zip (see Diagnostics page)
# Admin > Troubleshooting and Support Tools > Create Support Zip

# 2. Thread dumps (capture before restart if possible)
CONF_PID=$(pgrep -f confluence | head -1)
for i in 1 2 3; do
  jstack -l "$CONF_PID" > "/tmp/threaddump_escalation_${i}.txt"
  sleep 10
done

# 3. Heap histogram
jmap -histo:live "$CONF_PID" > /tmp/heap_histo_escalation.txt

# 4. Full application log (last 24 hours, untruncated)
cp /var/atlassian/application-data/confluence/logs/atlassian-confluence.log \
  /tmp/atlassian-confluence-escalation.log

# 5. System info
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/settings/systemInfo" | jq '.' > /tmp/systeminfo.json

# 6. Plugin list
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/plugins/1.0/" \
  | jq '[.plugins[] | {key, version, enabled, userInstalled}]' \
  > /tmp/plugins.json

# 7. Database stats
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass)) AS size
      FROM pg_tables WHERE schemaname='public' ORDER BY 2 DESC LIMIT 20;" \
  > /tmp/db_table_sizes.txt
```

---

## Atlassian Support Ticket Template

Use this template when raising a ticket at [support.atlassian.com](https://support.atlassian.com).

```yaml
SUMMARY:
[One-line description — e.g. "Confluence DC: Search returns no results after upgrade to 9.1.0"]

PRIORITY: [Critical / High / Medium / Low]
  Critical = production down or data loss
  High     = major feature broken, workaround unavailable
  Medium   = degraded performance or functionality with workaround
  Low      = cosmetic / enhancement

PRODUCT: Confluence Data Center
VERSION: 9.x.x (build XXXXXX)

ENVIRONMENT:
  - Nodes: 3 (Active/Active Data Center)
  - Java: OpenJDK 17.0.10
  - OS: Ubuntu 22.04 LTS
  - Database: PostgreSQL 16.2
  - JVM heap: -Xmx8g
  - Approx. pages: 150,000
  - Approx. users: 2,500 (LDAP-synced)

PROBLEM STATEMENT:
Since upgrading from 8.9.3 to 9.1.0 on 2026-05-07, all searches return
zero results. The Content Indexing page shows the queue at 0 and status
"IDLE", but searches for known page titles return nothing. The issue
affects all users.

STEPS TO REPRODUCE:
1. Log in as any user
2. Click the search bar and type "Deployment Runbook" (a known page in the OPS space)
3. No results are returned

EXPECTED RESULT:
The search returns the matching page "Deployment Runbook" in the OPS space.

ACTUAL RESULT:
"No results found" — even for exact page titles.

WHAT WAS TRIED:
1. Triggered Content Indexing > Re-index — completed, no change
2. Stopped Confluence, deleted /mnt/confluence-shared/index/, restarted
   — full index rebuild completed but search still returns nothing
3. Reviewed atlassian-confluence.log — no Lucene exceptions visible

WORKAROUND:
Users can browse spaces directly but cannot search. Impact: severe.

ATTACHMENTS:
- support.zip (generated 2026-05-08 09:30 UTC+2)
- atlassian-confluence.log (full, 2026-05-07 to 2026-05-08)
- threaddumps x3
- systeminfo.json
- plugins.json (37 user-installed apps)

LICENSE:
Confluence Data Center — License ID: SEN-XXXXXXX
Contact: chris.anastasiadis@example.com (+30 210 XXX XXXX)
```

---

## SLA Expectations

### Atlassian Support SLAs (Data Center — Platinum / Premier)

| Priority | Initial Response | Target Resolution |
|---|---|---|
| P1 — Critical (production down) | 1 hour (24/7) | Best effort / case-by-case |
| P2 — High (major feature broken) | 4 hours (business hours) | 3 business days |
| P3 — Medium (degraded function) | 8 business hours | 5 business days |
| P4 — Low (cosmetic / question) | 2 business days | 10 business days |

> SLAs are for **initial response**, not resolution. Complex Data Center issues can take days to weeks if a hotfix or patch is required.

### Internal SLAs

| Severity | Description | L1 Response | L1 → L2 Escalation | L2 → L3 Escalation |
|---|---|---|---|---|
| SEV1 | Production fully unavailable | 15 min | Immediate | 30 min if unresolved |
| SEV2 | Major feature broken, no workaround | 30 min | 1 hour | 2 hours |
| SEV3 | Degraded performance, workaround exists | 2 hours | Next business day | 2 business days |
| SEV4 | Minor issue, minimal impact | Best effort | Not required | Not required |

---

## Emergency Contact Paths

### Internal Escalation

| Role | Contact | Availability |
|---|---|---|
| On-call Platform Engineer | PagerDuty rotation — alert `confluence-oncall` | 24/7 |
| Platform Engineering Lead | Slack: `#platform-ops` → `@platform-lead` | Business hours; PD after-hours |
| CISO / Security (security incidents) | Slack: `#security-incidents` | 24/7 |

### Atlassian Support

| Method | Details | Use For |
|---|---|---|
| Support portal | [support.atlassian.com](https://support.atlassian.com) | All tickets |
| Emergency escalation | Request via portal: "Escalate to Critical" button | P1 only |
| Premier Support hotline | Available for Premier plan customers — see your contract | P1 production down |
| Atlassian Community | [community.atlassian.com](https://community.atlassian.com) | Non-urgent how-to questions |
| Atlassian Partner | Your regional Atlassian partner (if contracted) | Implementation issues |

### Useful References

| Resource | URL |
|---|---|
| Confluence release notes | https://confluence.atlassian.com/doc/confluence-release-notes |
| Known issues | https://jira.atlassian.com/projects/CONFSERVER |
| Upgrade notes | https://confluence.atlassian.com/doc/confluence-upgrade-guide |
| Supported platforms | https://confluence.atlassian.com/doc/supported-platforms |
| Data Center docs | https://confluence.atlassian.com/enterprise/confluence-data-center |

---

## Post-Incident Review Template

After every SEV1 or SEV2 incident, complete a post-incident review within 5 business days.

```markdown
## Post-Incident Review — Confluence [INCIDENT-ID]

**Date of Incident:** YYYY-MM-DD
**Duration:** HH:MM (detection to resolution)
**Severity:** SEV1 / SEV2
**Affected Users:** N

### Timeline
| Time (UTC+2) | Event |
|---|---|
| 09:00 | First alert received |
| 09:05 | L2 engaged |
| ... | ... |
| 10:30 | Service restored |

### Root Cause
[One paragraph: what failed and why]

### Impact
[User-facing impact, data risk, SLA breach?]

### Resolution
[What fixed it: steps taken]

### Contributing Factors
- [e.g. No monitoring on index queue depth]
- [e.g. NFS mount timeout setting too aggressive]

### Action Items
| Action | Owner | Due Date |
|---|---|---|
| Add index queue depth alert to monitoring | Platform | 2026-05-15 |
| Increase NFS timeout in fstab | Platform | 2026-05-12 |
| Schedule quarterly restore test | Platform | 2026-06-01 |
```
