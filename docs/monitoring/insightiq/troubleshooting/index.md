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
┌───────────────────────────────────── InsightIQ — Troubleshooting ─────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Collection Stops               │  │              Performance Issues             │   │
│   │               Check iiq_status               │  │               Check VM CPU/mem              │   │
│   │             Check PAPI TCP 8080              │  │               Check disk usage              │   │
│   │               Verify PAPI user               │  │               Check PostgreSQL              │   │
│   │              Restart collection              │  │            Reduce collection int            │   │
│   │              Check cluster PAPI              │  │              Open Dell support              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Logs: /var/log/isilon/insightiq/ · iiq_status on VM · PAPI test from VM                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  iiq_status = Show InsightIQ collection daemon status (running/stopped)                               │
│  PAPI TCP 8080 = Test connectivity: curl -k https://<cluster>:8080/platform/1/auth                    │
│  PAPI user test = Verify credential: curl -u <user>:<pass> https://<cluster>:8080/platform/1          │
│  Restart collection = iiq_stop then iiq_start to recover stalled collection process                   │
│  Disk full = df -h /data; if > 95%, purge old data or expand VMDK                                     │
│  PostgreSQL check = Check DB service: systemctl status postgresql                                     │
│  VM CPU/mem = If InsightIQ VM is starved, add vCPU or RAM via vSphere                                 │
│  Reduce interval = Increase collection interval from 30s to 5m to reduce DB write load                │
│  PAPI on cluster = Verify cluster PAPI is enabled and accessible (isi_backend_cache_rpc_test)         │
│  Log review = /var/log/isilon/insightiq/collection.log for error details                              │
│  Dell support = support.dell.com; attach collection log and iiq_status output                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
