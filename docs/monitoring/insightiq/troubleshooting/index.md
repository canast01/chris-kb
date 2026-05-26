# InsightIQ: Collector Connectivity, Data Gaps, and Performance Issues

This page covers common InsightIQ operational problems: connectivity failures between the InsightIQ collector and PowerScale clusters, data collection gaps, and performance degradation on the InsightIQ appliance itself.

## Collector Connectivity Checks

InsightIQ communicates with PowerScale clusters via the OneFS platform API (port 8080 HTTPS). Connectivity failures result in data gaps.

```bash
# Verify InsightIQ can reach the PowerScale API from the appliance
ssh admin@insightiq.example.com

# Test connectivity to PowerScale platform API
curl -sk https://powerscale.example.com:8080/platform/1/protocols/nfs/exports \
  -u "insightiq-svc:password" | jq '.total'

# Check InsightIQ collector service status
sudo systemctl status iiq-collector

# View collector logs
sudo tail -f /var/log/insightiq/collector.log

# Restart the collector if it has stopped
sudo systemctl restart iiq-collector
```

Data gap causes and remediation:

| Cause | Symptom in UI | Fix |
|---|---|---|
| InsightIQ appliance powered off | Gap from last shutdown to restart | Data cannot be backfilled; note gap in reports |
| PowerScale API auth failure | Gap starts after password change | Update InsightIQ cluster credentials |
| PowerScale API overloaded | Intermittent gaps during peak | Increase API retry timeout in InsightIQ config |
| Time drift > 5 seconds | Metrics appear at wrong timestamps | Sync NTP on both InsightIQ and PowerScale |
| SSL certificate expired | All API calls fail | Update or re-trust SSL certificate on InsightIQ |

## Updating Cluster Credentials

If the service account password changes on PowerScale, update InsightIQ to restore collection:

```bash
# On InsightIQ web UI:
# Navigate to: InsightIQ > Clusters > [Cluster] > Edit
# Update the username and password, then click Test Connection

# Alternatively via InsightIQ CLI
sudo /opt/isilon/insightiq/bin/iiq_data_access_manage \
  --cluster powerscale.example.com \
  --username insightiq-svc \
  --update-password
```

## InsightIQ Appliance Performance Issues

InsightIQ can become slow if the database grows too large or if disk I/O is constrained.

```bash
# Check disk space on InsightIQ appliance
df -h

# Check InsightIQ database size
sudo du -sh /var/lib/insightiq/db/

# Check available memory
free -h

# Check active processes consuming resources
top -b -n 1 | head -25

# Clean up old data (if retention policy is set)
# Navigate to: InsightIQ > Settings > Data Retention
# Reduce retention period to free disk space
```

Recommended InsightIQ appliance resources:

| Resource | Minimum | Recommended (> 5 clusters) |
|---|---|---|
| vCPU | 4 | 8 |
| Memory | 16 GB | 32 GB |
| OS Disk | 60 GB | 100 GB |
| Data Disk | 500 GB | 2 TB |

## Common Troubleshooting Reference

| Problem | First Check | Second Check |
|---|---|---|
| No data for cluster | Collector service running | PowerScale API credentials valid |
| Data stops after upgrade | Collector service restarted | InsightIQ version compatible with OneFS version |
| Reports taking > 5 minutes | Data retention too long | Reduce retention; add more disk to data volume |
| Graph shows flat line | Check collection status in UI | Review collector.log for API errors |
| Cannot log in to InsightIQ UI | Web service status | Reset admin password via console |
