---
tags:
  - netapp
---
# InsightIQ — CLI Reference

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


```text title="Expected output"
administrator@insightiq.example.com's password: 
Last login: Wed Jan 15 14:32:18 2025 from 192.168.1.50
insightiq-prod-01:~$ sudo service insightiq status
● insightiq.service - NetApp InsightIQ Service
   Loaded: loaded (/etc/systemd/system/insightiq.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2025-01-15 14:28:33 UTC; 4min 12s ago
   Main PID: 2847 (java)
     Tasks: 47 (limit: 4096)
    Memory: 2.3G
insightiq-prod-01:~$ sudo service insightiq restart
insightiq-prod-01:~$ ● insightiq.service - NetApp InsightIQ Service
   Loaded: loaded (/etc/systemd/system/insightiq.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2025-01-15 14:33:01 UTC; 2s ago
   Main PID: 3156 (java)
insightiq-prod-01:~$ tail -f /var/log/insightiq/insightiq.log
2025-01-15 14:33:02,847 INFO  [main] Starting InsightIQ v5.2.1.0 Build 8847
2025-01-15 14:33:05,123 INFO  [main] Database connection pool initialized: 20 connections
2025-01-15 14:33:07,456 INFO  [main] Loading cluster discovery modules
2025-01-15 14:33:09,789 INFO  [main] InsightIQ service ready on port 8443
2025-01-15 14:33:10,012 INFO  [scheduler] Starting scheduled data collection tasks
insightiq-prod-01:~$ df -h /home/insightiq
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       500G  387G  113G  78%  /home/insightiq
```

!!! warning "Common errors"
    **`sudo: service: command not found`** — Use `sudo systemctl status insightiq` instead of `sudo service insightiq status` on systemd-based systems.
    **`Permission denied (publickey,password)`** — Verify the administrator account credentials and ensure SSH key-based authentication is configured if password auth is disabled.
    **`tail: cannot open '/var/log/insightiq/insightiq.log' for reading: No such file or directory`** — Confirm the InsightIQ service is running and check the actual log path with `sudo find /var/log -name "*insightiq*"`.
```bash
# Get capacity summary for a cluster
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/clusters/<guid>/capacity"

# Get per-node capacity
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/clusters/<guid>/nodes/<node_id>/capacity"
```

```text title="Expected output"
{
  "cluster_id": "a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6",
  "cluster_name": "prod-cluster-01",
  "total_capacity_gb": 102400,
  "used_capacity_gb": 78956,
  "available_capacity_gb": 23444,
  "capacity_utilization_percent": 77.1,
  "snapshot_reserve_gb": 5120,
  "last_updated": "2024-01-15T14:32:18Z"
}
{
  "node_id": "node-01",
  "node_name": "cluster-01-node-01",
  "total_capacity_gb": 25600,
  "used_capacity_gb": 19739,
  "available_capacity_gb": 5861,
  "capacity_utilization_percent": 77.1,
  "aggregates": [
    {
      "aggregate_name": "aggr1",
      "total_capacity_gb": 12800,
      "used_capacity_gb": 9869
    }
  ],
  "last_updated": "2024-01-15T14:32:18Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification, or import the InsightIQ certificate into your system's trusted store.
    **`curl: (401) Unauthorized`** — Verify the admin credentials are correct and URL-encoded if they contain special characters; use `-u "admin:$(echo -n 'password' | jq -sRr @uri)"` for special chars.
    **`curl: (404) Not Found`** — Confirm the cluster GUID and node_id are correct by listing clusters with `/api/json/v2/clusters` endpoint first.
```bash
# List available reports
curl -k -u "admin:<pass>"   https://<insightiq_fqdn>/api/json/v2/reports

# Download a report
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/reports/<report_id>/download"   -o report.csv
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```

## See also

- [InsightIQ — Overview](../../)
