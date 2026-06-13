---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
---
# InsightIQ — Troubleshooting

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
```text
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

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
