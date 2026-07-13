---
tags:
  - netapp
  - operations
description: "InsightIQ Operations reference covering Daily Checklist, Cluster Connection Troubleshooting, Capacity Review (Weekly), Appliance Health Checks, Alert..."
---
# InsightIQ Operations

<div class="kb-summary">
InsightIQ Operations reference covering Daily Checklist, Cluster Connection Troubleshooting, Capacity Review (Weekly), Appliance Health Checks, Alert Threshold Review (Monthly) and 2 more sections.

*Applies to: InsightIQ*
  <a class="kb-card" href="faq/"><strong>FAQ</strong><span>Frequently asked questions, common issues, and quick answers for day-to-day operations.</span></a>
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Daily Checklist

| Check | Location | Pass Criteria |
|---|---|---|
| Cluster connection status | Dashboard > Clusters | All clusters show Active (green) |
| Appliance disk usage | Administration > System Status | Data volume below 80% used |
| Latest data collection timestamp | Dashboard > [Cluster] > Overview | Last data point within last 15 minutes |
| Active alert review | Administration > Alerts > Active Alerts | No unacknowledged Critical latency or throughput alerts |

If a cluster shows as Disconnected or the last data point is stale (> 30 minutes), investigate before stand-up.

## Cluster Connection Troubleshooting

## Appliance Health Checks

```bash
# Check InsightIQ service status
sudo systemctl status iiq

# Check PostgreSQL service
sudo systemctl status postgresql

# Check disk usage on data volume
df -h /data

# Review recent errors in InsightIQ logs
sudo journalctl -u iiq --since "24 hours ago" | grep -i error

# Check database size
psql -U iiq -c "SELECT pg_size_pretty(pg_database_size('iiq'));"
```


```text title="Expected output"
● iiq.service - InsightIQ Service
     Loaded: loaded (/etc/systemd/system/iiq.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:23:47 UTC; 2 days ago
   Main PID: 4782 (java)
      Tasks: 47 (limit: 4096)
     Memory: 2.3G
     CGroup: /system.slice/iiq.service
             └─4782 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -Xmx4g...

● postgresql.service - PostgreSQL Database Server
     Loaded: loaded (/etc/systemd/system/postgresql.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2015-01-15 09:18:12 UTC; 2 days ago
   Main PID: 3891 (postgres)
      Tasks: 12 (limit: 4096)
     Memory: 856M
     CGroup: /system.slice/postgresql.service

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda3      500G  387G  113G  78% /data

Jan 15 09:45:23 iiq-prod-01 iiq[4782]: ERROR: Connection timeout to collector 192.168.1.45
Jan 15 10:12:08 iiq-prod-01 iiq[4782]: ERROR: Failed to parse metrics from array-sn-7a8b9c
Jan 15 11:33:41 iiq-prod-01 iiq[4782]: ERROR: Database query exceeded 30s timeout

 pg_size_pretty
----------------
 4821 MB
(1 row)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL: Ident authentication failed for user "iiq"` | Verify the PostgreSQL pg_hba.conf allows local connections for the iiq user, or run psql with `-h localhost` and ensure the iiq user exists. |
    | `Unit iiq.service could not be found.` | Confirm the InsightIQ service file exists at `/etc/systemd/system/iiq.service` and run `sudo systemctl daemon-reload` to refresh systemd. |
    | `df: '/data': No such file or directory` | Mount the data volume with `sudo mount /dev/sdX /data` or verify the mount point exists and is accessible. |
## Alert Threshold Review (Monthly)

- Review the past month's active alerts for noise patterns
- Adjust thresholds for workloads with known high baselines (document deviations from standard)
- Validate SNMP trap delivery to monitoring platform with a test trap
- Confirm SMTP alert emails are being delivered (check spam/junk filters)

## Report Generation

### On-Demand Report

```text
InsightIQ web UI > Reports > Custom Report
- Select: Cluster, Time Range, Metrics (throughput, latency, CPU)
- Format: PDF or CSV
- Download or email directly
```

### Scheduled Report Validation

```text
Administration > Reports > Scheduled Reports
- Verify each scheduled report shows Last Run within expected window
- If a report failed: check SMTP configuration and recipient list
- Manually trigger to test: Actions > Run Now
```

## Monthly Tasks

- Generate monthly capacity planning report for all clusters and share with management
- Validate InsightIQ database backup is completing (check cron logs or backup target)
- Review InsightIQ appliance OS patches and schedule maintenance window if needed
- Review user accounts and remove stale accounts (Administration > Users)

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Architecture](../architecture/)
- [Capacity](../capacity/)
- [Cli Reference](../cli-reference/)
- [Deploy](../deploy/)
- [Design Standards](../design-standards/)
- [Integration](../integration/)
- [Learning Path](../learning-path/)
- [Lifecycle](../lifecycle/)
- [Performance](../performance/)
- [Reports](../reports/)
- [Scripts](../scripts/)
- [Security](../security/)
- [Troubleshooting](../troubleshooting/)
- [Vendor Support](../vendor-support/)
- [Workloads](../workloads/)
- [InsightIQ — Overview](../)
