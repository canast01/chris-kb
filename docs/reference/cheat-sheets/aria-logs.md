---
tags:
  - aria-logs
  - monitoring
description: "Top-10 Aria Logs (Log Insight) commands for agent control, syslog configuration, and log queries via CLI and REST API."
---
# Aria Logs Cheat Sheet

*Applies to: All products*

<div class="kb-summary">
Top-10 Aria Logs (Log Insight) commands for agent control, syslog configuration, and log queries via CLI and REST API.
</div>
![Aria Logs Cheat Sheet](../../assets/reference-cheat-sheets-aria-logs.svg)

## Log Insight Agent (liagent)

```bash
# Linux agent control
systemctl status liagent                       # agent service status
systemctl restart liagent                      # restart agent
cat /var/log/liagent.log | tail -50            # recent agent log

# Agent config file: /etc/liagent.ini
# Key settings:
#   [server]
#   hostname = loginsight.lab.local
#   port = 9543
#   proto = cfapi
#   ssl = yes

/usr/lib/loginsight-agent/liagent -d            # debug mode (foreground, verbose)
```


```text title="Expected output"
● liagent.service - VMware Log Insight Agent
     Loaded: loaded (/usr/lib/systemd/system/liagent.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 14:32:15 UTC; 2 days ago
   Main PID: 2847 (liagent)
      Tasks: 8 (limit: 4915)
     Memory: 124.3M
        CPU: 2h 14m 32s
     CGroup: /system.slice/liagent.service
             └─2847 /usr/lib/loginsight-agent/liagent

2024-01-18 14:32:15 host-prod-01 liagent[2847]: Agent version 8.8.2 build 21589234
2024-01-18 14:32:16 host-prod-01 liagent[2847]: Connected to loginsight.lab.local:9543 (cfapi)
2024-01-18 14:32:17 host-prod-01 liagent[2847]: SSL certificate verified: CN=loginsight.lab.local
2024-01-18 14:33:02 host-prod-01 liagent[2847]: Heartbeat sent (uptime: 47s)
2024-01-18 15:14:33 host-prod-01 liagent[2847]: Collected 1247 log events from /var/log/syslog
2024-01-18 16:45:21 host-prod-01 liagent[2847]: Collected 892 log events from /var/log/auth.log
2024-01-18 17:22:09 host-prod-01 liagent[2847]: Buffer queue: 2134 events pending
2024-01-18 18:01:44 host-prod-01 liagent[2847]: Heartbeat sent (uptime: 3h 29m)

[2024-01-18 18:15:33.421] DEBUG: Agent initialization complete
[2024-01-18 18:15:34.156] DEBUG: Loading config from /etc/liagent.ini
[2024-01-18 18:15:34.289] DEBUG: Server: loginsight.lab.local:9543 (proto=cfapi, ssl=yes)
[2024-01-18 18:15:34.512] DEBUG: Connecting to 192.168.1.45:9543...
[2024-01-18 18:15:34.834] DEBUG: TLS handshake successful
[2024-01-18 18:15:35.102] DEBUG: Agent UUID: a7f2c1e9-4d8b-11ee-be56-0242ac120002
[2024-01-18 18:15:35.445] DEBUG: Starting log collection threads (4 workers)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Job for liagent.service failed because the control process exited with error code.` | Check `/var/log/liagent.log` for the root cause and verify `/etc/liagent.ini` has correct hostname and port settings. |
    **`Connection refused (111) to loginsight.lab.
## REST API

```bash
BASE="https://loginsight/api/v1"

# Authenticate
SESSION=$(curl -sk -X POST $BASE/sessions \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"VMware1!","provider":"Local"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['sessionId'])")
HDR="-H \"Authorization: Bearer $SESSION\""

# Queries
curl -sk $HDR "$BASE/events/text/CONTAINS+error?limit=100" | python3 -m json.tool

# Ingestion status
curl -sk $HDR "$BASE/cluster/vips" | python3 -m json.tool                # VIP config
curl -sk $HDR "$BASE/cluster" | python3 -m json.tool                     # cluster node health

# Alerts
curl -sk $HDR "$BASE/alerts" | python3 -m json.tool                      # configured alerts
```


```text title="Expected output"
{
  "events": [
    {
      "text": "Connection error: timeout on host db-node-03",
      "timestamp": 1704067234000,
      "source": "vcenter-01.lab.local",
      "severity": "ERROR"
    },
    {
      "text": "Authentication error: invalid credentials for user root",
      "timestamp": 1704067198000,
      "source": "esx-host-12.lab.local",
      "severity": "ERROR"
    }
  ],
  "eventCount": 847,
  "pageNumber": 1
}
{
  "vips": [
    {
      "ip": "192.168.1.45",
      "hostname": "loginsight-vip.lab.local",
      "role": "primary",
      "status": "ACTIVE"
    }
  ]
}
{
  "nodes": [
    {
      "nodeId": "node-1",
      "hostname": "loginsight-node-01",
      "ip": "192.168.1.41",
      "status": "HEALTHY",
      "diskUsage": 67
    },
    {
      "nodeId": "node-2",
      "hostname": "loginsight-node-02",
      "ip": "192.168.1.42",
      "status": "HEALTHY",
      "diskUsage": 71
    }
  ]
}
{
  "alerts": [
    {
      "alertId": "alert-uuid-8f2c4a1b",
      "name": "High Memory Usage",
      "enabled": true,
      "threshold": 85
    },
    {
      "alertId": "alert-uuid-3d9e7f5c",
      "name": "Disk Space Critical",
      "enabled": true,
      "threshold": 90
    }
  ],
  "totalAlerts": 12
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command to skip SSL verification (already present in example, but ensure it appears before `-X`). |
    | `jq: parse error: Invalid JSON text at line 1` | Verify the sessionId was successfully extracted by testing `curl -sk -X POST $BASE/sessions ... | python3 -c "import sys,json; print(json.load(sys.stdin))"` to confirm valid JSON response before piping to sessionId extraction. |
    | `curl: (401) Unauthorized` | Confirm the SESSION variable contains a valid token by running `echo $SESSION` and verify the token hasn't expired; re-authenticate if necessary. |
## See also

- [Aria Logs Procedures](../../../virtualization/vmware/products/aria-operations-for-logs/operations/procedures/)
- [Aria Logs Troubleshooting](../../../virtualization/vmware/products/aria-operations-for-logs/troubleshooting/common-issues/)
