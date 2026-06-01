# InsightIQ Operations

<div class="kb-summary">
InsightIQ Operations reference covering Daily Checklist, Cluster Connection Troubleshooting, Capacity Review (Weekly), Appliance Health Checks, Alert Threshold Review (Monthly) and 2 more sections.
</div>

## Daily Checklist

| Check | Location | Pass Criteria |
|---|---|---|
| Cluster connection status | Dashboard > Clusters | All clusters show Active (green) |
| Appliance disk usage | Administration > System Status | Data volume below 80% used |
| Latest data collection timestamp | Dashboard > [Cluster] > Overview | Last data point within last 15 minutes |
| Active alert review | Administration > Alerts > Active Alerts | No unacknowledged Critical latency or throughput alerts |

If a cluster shows as Disconnected or the last data point is stale (> 30 minutes), investigate before stand-up.

## Cluster Connection Troubleshooting

```text
Symptom: Cluster shows Disconnected or Missing in InsightIQ

1. Test manual API connectivity from InsightIQ appliance:
   curl -sk https://<cluster-mgmt-ip>:8080/platform/1/statistics/summary/drive -u svc-insightiq

2. Check if the svc-insightiq account is active on the cluster:
   (on OneFS CLI) isi auth users view svc-insightiq

3. Verify network connectivity (TCP 8080):
   telnet <cluster-mgmt-ip> 8080

4. If password has been rotated: update credential in InsightIQ
   Administration > Clusters > [Cluster] > Edit > Update Password

5. Restart the InsightIQ collection service if credential fix doesn't resolve:
   sudo systemctl restart iiq
```
┌─────────────────────────────────────── InsightIQ — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Daily Checks        │  │         Weekly Tasks        │  │        Monthly Tasks        │   │
│   │      Verify collection      │  │        Review reports       │  │      Capacity planning      │   │
│   │       Check disk usage      │  │         Check alerts        │  │       Retention review      │   │
│   │      Verify backup ran      │  │      Top talker review      │  │        Trend analysis       │   │
│   │     Confirm clusters up     │  │        Latency review       │  │        Report to mgmt       │   │
│   │     Check service status    │  │       Capacity outlook      │  │        Access review        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Daily ops via InsightIQ web UI · admin CLI for service checks · NFS backup verification              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Collection verify = Confirm InsightIQ shows Connected and recent data for each cluster               │
│  Disk usage = Monitor InsightIQ VM datastore; alert at 80% to expand before full                      │
│  Backup verification = Confirm nightly iiq_backup completed and archive exists on NFS                 │
│  Service status = iiq_status on appliance confirms data collection daemon running                     │
│  Top talker review = Weekly check of clients generating most IO; spot unexpected growth               │
│  Latency review = Review average and p95 latency trends; flag increases to storage team               │
│  Capacity outlook = Review InsightIQ capacity report for projected full dates                         │
│  Retention review = Monthly check that old data purging correctly per retention policy                │
│  Trend analysis = Monthly review of 30/90-day performance trends for capacity planning                │
│  Access review = Monthly check of InsightIQ user list; remove stale accounts                          │
│  Management report = Monthly PDF summary of performance trends for leadership review                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

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
