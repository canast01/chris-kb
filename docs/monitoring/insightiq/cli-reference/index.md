# InsightIQ CLI Reference


<div class="kb-summary">
InsightIQ is the Dell EMC analytics platform for PowerScale (Isilon) performance monitoring. It exposes a REST API and SSH access to the InsightIQ appliance for direct management. The API base URL is `https://<insightiq_fqdn>/api/json/v2`.
</div>

---

## Appliance Access

```bash
# SSH to the InsightIQ appliance
ssh administrator@<insightiq_fqdn>

# Check InsightIQ service status
sudo service insightiq status

# Restart InsightIQ service
sudo service insightiq restart

# View logs
tail -f /var/log/insightiq/insightiq.log

# Check disk space (InsightIQ database can grow large)
df -h /home/insightiq
```
┌────────────────────────────────────── InsightIQ — CLI Reference ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               InsightIQ Admin CLI — accessed via SSH or console on appliance VM               │   │
│   │                  iiq_backup — create backup of InsightIQ config and database                  │   │
│   │                           iiq_restore — restore from backup archive                           │   │
│   │                 iiq_start / iiq_stop / iiq_status — manage InsightIQ services                 │   │
│   │                  iiq_add_cluster — register a new PowerScale cluster from CLI                 │   │
│   │                  iiq_config — view or modify appliance configuration settings                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  SSH to InsightIQ VM management IP · local console via vSphere · root or iiq user                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  iiq_backup = Creates compressed archive of InsightIQ DB and config files                             │
│  iiq_restore = Restores from backup; use after re-deploy or data corruption                           │
│  iiq_status = Shows running/stopped state of InsightIQ data collection service                        │
│  iiq_add_cluster = CLI alternative to UI for adding a new PowerScale cluster                          │
│  iiq_config = View and modify InsightIQ settings (SMTP, retention, data path)                         │
│  SSH access = Required for admin CLI; restrict to management network                                  │
│  Root login = Appliance root user; use only for admin CLI operations                                  │
│  Web UI = Primary interface for dashboards and reports at https://<iiq-ip>                            │
│  Service restart = iiq_stop followed by iiq_start to recover stalled collection                       │
│  Log files = /var/log/isilon/insightiq/ for collection and service logs                               │
│  Config file = /etc/insightiq/config.conf; modified by iiq_config or manually                         │
│  Backup target = NFS mount or local directory configured in iiq_config                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```bash

---

## Capacity

```bash
# Get capacity summary for a cluster
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/clusters/<guid>/capacity"

# Get per-node capacity
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/clusters/<guid>/nodes/<node_id>/capacity"
```

---

## Reports

```bash
# List available reports
curl -k -u "admin:<pass>"   https://<insightiq_fqdn>/api/json/v2/reports

# Download a report
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/reports/<report_id>/download"   -o report.csv
```
