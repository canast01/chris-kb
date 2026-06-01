# Daily Infrastructure Health Checks


<div class="kb-summary">
Daily Infrastructure Health Checks reference covering Overview, Morning Check Routine, What to Look For, Escalation Decision Tree, Documentation and Handover and 1 more sections.
</div>

## Overview

A consistent daily check routine catches issues before they escalate into incidents. The goal is not to review everything — it is to confirm that the most critical systems are healthy, recent changes have not caused drift, and nothing in overnight logs or alerts requires action before business hours begin.

---

## Morning Check Routine

Run these checks at the start of each working day, or at handover between on-call shifts.

| Check Area         | What to Review                                  | Tool / Location                 |
|--------------------|-------------------------------------------------|---------------------------------|
| Monitoring alerts  | Open and unacknowledged alerts                  | PagerDuty / Alertmanager        |
| Backup jobs        | Last night's backup success/failure status      | Backup console or email digest  |
| Disk space         | Filesystems above 80% used                      | Monitoring dashboard            |
| Service health     | All critical services in `UP` state             | Uptime / health check dashboard |
| Overnight changes  | Any changes deployed overnight                  | Change management tool          |
| Certificate expiry | Certs expiring within 30 days                   | Cert monitoring / Vault         |
| Replication lag    | DB replication lag within threshold             | DB monitoring                   |

Flag anything outside normal thresholds immediately. Do not wait for an alert to escalate it.

---

## What to Look For

Beyond raw alerts, use judgment to identify:

- **Creeping degradation** — metrics that are still within threshold but trending the wrong way
- **Silenced alerts** — alerts that were acknowledged overnight but not resolved
- **Scheduled job failures** — batch jobs, ETL pipelines, or cron tasks that did not complete
- **Log spikes** — a sudden increase in error-level log entries even without a firing alert
- **Capacity warnings** — disk, memory, or connection pools approaching limits

---

## Escalation Decision Tree

When a finding requires action, determine urgency before escalating.

- [ ] Is a production service actively degraded or down? → Raise P1/P2 incident immediately
- [ ] Is the issue growing or likely to cause impact within the hour? → Raise incident, notify on-call lead
- [ ] Is the issue contained but needs same-day attention? → Create task ticket, assign owner
- [ ] Is the issue low-risk and can wait until planned maintenance? → Log it, set reminder

Never sit on a finding because you are unsure. If in doubt, raise it.

---

## Documentation and Handover

Record the outcome of every daily check, even if everything is healthy.

- Use the daily check log template (date, engineer name, findings, actions taken)
- For "all clear" checks, a single line confirming each area was checked is sufficient
- For findings, include: what was found, when, what action was taken, and current status
- At shift handover, verbally walk the incoming engineer through any open items

---

## Common Daily Check Commands

```bash
# Disk usage — filesystems over 80%
df -h | awk 'NR>1 && $5+0 > 80 {print}'

# Services that are not running (systemd)
systemctl list-units --state=failed

# Last backup job exit codes (example: restic)
journalctl -u restic-backup.service --since "yesterday" | tail -20

# Certificate expiry check (example: openssl)
echo | openssl s_client -connect hostname:443 2>/dev/null | openssl x509 -noout -enddate
```

Add environment-specific commands as you test and verify them.
