---
tags:
  - confluence
  - troubleshooting
---
# Confluence — Escalation


<div class="kb-summary">
This page defines the escalation process for Confluence incidents: who handles what, when to escalate, what to collect before raising a ticket, SLA expectations, and how to reach Atlassian Support in a production emergency.
</div>

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

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
┌───────────────────────────────── Confluence — Escalation Procedures ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Confluence Escalation Tiers                                  │   │
│   │              Tier 1: Ops team — restart, reindex, check logs, restore from backup             │   │
│   │           Tier 2: Senior engineer — JVM tuning, DB query analysis, plugin conflicts           │   │
│   │       Tier 3: Atlassian Support — open ticket with support-zip; attach thread/heap dump       │   │
│   │          Tier 4: Atlassian escalation — P1 production down; 24x7 critical support SLA         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Escalation criteria: T1 > 30 min no resolution; T2 > 2 hr; T3 > 4 hr production down               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Criteria              │  │             Artifacts to Gather             │   │
│   │            Service down > 30 min             │  │              support-zip bundle             │   │
│   │             Data loss suspected              │  │               Thread dumps x3               │   │
│   │              Security incident               │  │               Heap dump (OOM)               │   │
│   │              Repeated OOM crash              │  │              catalina.out tail              │   │
│   │             Corruption suspected             │  │              DB slow query log              │   │
│   │            Plugin breaks upgrade             │  │             Version + patch info            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Confluence VMs · PostgreSQL DB · monitoring/alerting · Atlassian Support portal                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  support-zip    = Admin > Troubleshooting > Create Support Zip; logs, config, thread dumps            │
│  Thread dump    = JVM thread snapshot; take 3 dumps 10 seconds apart for deadlock analysis            │
│  Heap dump      = full JVM memory capture; large file; required for OOM analysis                      │
│  P1 incident    = production service down; page on-call immediately; escalate within 30 min           │
│  Atlassian Support = support.atlassian.com; requires valid license; submit with support-zip           │
│  Atlassian escalation = request via account team; for critical production outages                     │
│  DB slow query  = pg_stat_statements or log_min_duration_statement=1000ms in postgresql.conf          │
│  Plugin conflict = disable plugins one-by-one in safe mode to isolate culprit                         │
│  Safe mode      = Confluence starts without any user-installed plugins for diagnostics                │
│  Corruption     = DB or index inconsistency; run reindex; compare DB row counts                       │
│  Data loss      = page versions allow recovery; check DB for deleted content                          │
│  SLA            = Atlassian support SLA: P1 1hr response, P2 4hr, P3/P4 next business day             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
| Upgrade notes | https://confluence.atlassian.com/doc/upgrading-confluence-4578.html |
| Supported platforms | https://confluence.atlassian.com/doc/supported-platforms-207488198.html |
| Data Center docs | https://confluence.atlassian.com/doc/confluence-data-center-790795844.html |

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

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
