---
tags:
  - aria-logs
  - operations
  - vmware
---
# Aria Operations for Logs — CLI Reference

*Applies to: VMware Aria 8.x*
![Aria Operations for Logs — CLI Reference](../../../../../assets/virtualization-vmware-aria-operations-for-logs-operations-cl.svg)

```bash
# SSH to the Log Insight appliance
ssh admin@<li-appliance-fqdn>

# Check appliance status
li-admin status

# Show cluster node status
li-admin cluster-info

# Restart Log Insight services
li-admin restart

# Check log collection status
li-admin log-collection-status

# Show current storage usage
li-admin storage
```


```text title="Expected output"
admin@li-appliance-fqdn's password: 
Last login: Wed Mar 13 14:22:18 2024 from 192.168.1.45

Log Insight Appliance Status:
  Version: 8.14.1 Build 21567890
  Status: RUNNING
  Uptime: 45 days, 3 hours, 22 minutes
  License: Valid (expires 2025-03-15)

Cluster Information:
  Node Name: li-node-01.corp.local
  Node IP: 192.168.50.10
  Cluster Status: HEALTHY
  Cluster Size: 3 nodes
  Master Node: li-node-01.corp.local
  Replication Factor: 3

Restarting Log Insight services...
  Stopping ingestion service... [OK]
  Stopping query service... [OK]
  Stopping storage service... [OK]
  Starting storage service... [OK]
  Starting query service... [OK]
  Starting ingestion service... [OK]
  Restart completed successfully in 2m 34s

Log Collection Status:
  Active Collectors: 47
  Messages/sec: 12,847
  Dropped Messages: 0
  Parser Errors: 3
  Last Update: 2024-03-13 14:25:09 UTC

Storage Usage:
  Total Capacity: 2.0 TB
  Used: 1.34 TB (67%)
  Available: 660 GB (33%)
  Retention: 30 days
  Compression Ratio: 8.2:1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey,password).` | Verify the admin account credentials and ensure SSH key-based authentication is configured, or use the correct password for the admin user. |
    | `li-admin: command not found` | SSH directly to the appliance management interface or ensure you are logged into the correct Log Insight appliance node with proper shell access. |
    | `Cluster Status: UNHEALTHY - 1 node unreachable (li-node-03.corp.local)` | Check network connectivity to the unreachable node and verify all cluster nodes are powered on and have valid IP configurations. |
```bash
# Run a log query
curl -k -X POST https://<li-fqdn>/api/v1/events/query \
  -H "Authorization: Bearer <sessionId>" \
  -H "Content-Type: application/json" \
  -d '{"query":"text CONTAINS error","startTimeMillis":<epoch_ms>,"endTimeMillis":<epoch_ms>}'

# List all alerts
curl -k -X GET https://<li-fqdn>/api/v1/alerts \
  -H "Authorization: Bearer <sessionId>"

# List alert recommendations
curl -k -X GET https://<li-fqdn>/api/v1/notification/channels \
  -H "Authorization: Bearer <sessionId>"
```

```text title="Expected output"
{
  "results": [
    {
      "eventId": "evt-2024-001847",
      "timestamp": 1704067200000,
      "text": "Connection timeout error detected on host esx-prod-04.corp.local",
      "severity": "ERROR",
      "source": "vmkernel"
    },
    {
      "eventId": "evt-2024-001846",
      "timestamp": 1704066900000,
      "text": "Memory pressure error on cluster compute-01",
      "severity": "ERROR",
      "source": "VC"
    }
  ],
  "pageInfo": {"pageNumber": 0, "pageSize": 100, "totalCount": 247}
}
[
  {
    "alertId": "alert-5f8c2a1b",
    "name": "High CPU Utilization",
    "severity": "WARNING",
    "status": "ACTIVE",
    "affectedResources": 3,
    "lastUpdated": 1704067845000
  },
  {
    "alertId": "alert-6d9e4f2c",
    "name": "Disk Space Critical",
    "severity": "CRITICAL",
    "status": "ACTIVE",
    "affectedResources": 1,
    "lastUpdated": 1704067200000
  }
]
[
  {
    "channelId": "ch-smtp-001",
    "name": "Email - Operations Team",
    "type": "EMAIL",
    "enabled": true,
    "recipientCount": 5
  },
  {
    "channelId": "ch-slack-002",
    "name": "Slack - Alerts Channel",
    "type": "SLACK",
    "enabled": true,
    "recipientCount": 1
  }
]
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip certificate verification, or import the CA certificate into your system trust store. |
    | `{"error":"Unauthorized","message":"Invalid or expired session token"}` | Regenerate the session token by authenticating with valid credentials and update the `<sessionId>` value. |
    | `curl: (7) Failed to connect to <li-fqdn> port 443: Connection refused` | Verify the Aria Operations for Logs appliance is running and the FQDN/IP is correct and reachable from your network. |
```bash
# Send logs via CFAPI (Log Insight Ingestion API)
curl -k -X POST https://<li-fqdn>:9543/api/v1/events/ingest/<agentId> \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"text":"test log message","timestamp":<epoch_ms>,"fields":[{"name":"hostname","content":"myhost"}]}]}'
```

```text title="Expected output"
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   156  100    42  100   114    280    760 --:--:-- --:--:-- --:--:--:--:--
{"status":"success","eventCount":1,"ingestionId":"550e8400-e29b-41d4-a716-446655440000"}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification, or import the Log Insight CA certificate into your system trust store. |
    | `{"status":"error","message":"Invalid agentId"}` | Verify the agentId matches a registered agent in Log Insight by checking Administration > Agents or using the agent list API endpoint. |
    | `curl: (7) Failed to connect to <li-fqdn>:9543: Connection refused` | Confirm Log Insight is running and listening on port 9543 with `curl -k https://<li-fqdn>:9543/api/v1/version`, and verify network connectivity to the Log Insight instance. |
```bash
# List data sources (agents)
curl -k -X GET https://<li-fqdn>/api/v1/agents \
  -H "Authorization: Bearer <sessionId>"

# List content packs
curl -k -X GET https://<li-fqdn>/api/v1/content/contentpackmetadata \
  -H "Authorization: Bearer <sessionId>"

# Get system info
curl -k -X GET https://<li-fqdn>/api/v1/system/info \
  -H "Authorization: Bearer <sessionId>"

# Get storage info
curl -k -X GET https://<li-fqdn>/api/v1/system/storage \
  -H "Authorization: Bearer <sessionId>"
```

```text title="Expected output"
[
  {
    "id": "agent-001",
    "name": "vcenter-prod-01.corp.local",
    "status": "CONNECTED",
    "lastHeartbeat": "2024-01-15T14:32:18Z",
    "version": "8.10.2"
  },
  {
    "id": "agent-002",
    "name": "esxi-host-12.corp.local",
    "status": "CONNECTED",
    "lastHeartbeat": "2024-01-15T14:31:55Z",
    "version": "8.10.2"
  }
]
[
  {
    "id": "pack-vmware-001",
    "name": "VMware vSphere",
    "version": "2.5.1",
    "status": "INSTALLED",
    "releaseDate": "2023-11-20"
  },
  {
    "id": "pack-linux-001",
    "name": "Linux OS",
    "version": "3.1.0",
    "status": "INSTALLED",
    "releaseDate": "2023-10-15"
  }
]
{
  "productName": "VMware Aria Operations for Logs",
  "version": "8.10.2.1",
  "buildNumber": "22837456",
  "deploymentType": "DISTRIBUTED",
  "uptime": "45 days 12 hours"
}
{
  "totalCapacity": "5242880",
  "usedCapacity": "3145728",
  "availableCapacity": "2097152",
  "percentageUsed": 60,
  "retentionDays": 30
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification or import the CA certificate into your system trust store. |
    | `{"error":"Unauthorized","message":"Invalid or expired session token"}` | Regenerate the sessionId by authenticating to the API first using valid credentials. |
    | `curl: (7) Failed to connect to <li-fqdn> port 443: Connection refused` | Verify the Aria Operations for Logs instance is running and accessible at the specified FQDN and port 443. |
```bash
# Daily health check
li-admin status
li-admin cluster-info
li-admin storage

# Check for active alerts via API
curl -k -X GET https://<li-fqdn>/api/v1/alerts?active=true \
  -H "Authorization: Bearer <sessionId>"

# Verify agent connectivity
curl -k -X GET https://<li-fqdn>/api/v1/agents \
  -H "Authorization: Bearer <sessionId>"
```


```text title="Expected output"
=== Cluster Status ===
Node: li-master-01.corp.local (192.168.1.45)
  Status: HEALTHY
  Role: Master
  Uptime: 45d 12h 23m
Node: li-worker-01.corp.local (192.168.1.46)
  Status: HEALTHY
  Role: Worker
  Uptime: 45d 11h 58m
Node: li-worker-02.corp.local (192.168.1.47)
  Status: HEALTHY
  Role: Worker
  Uptime: 45d 10h 15m

=== Cluster Info ===
Cluster Name: production-logs
Version: 8.14.2
Build: 21567890
Nodes: 3/3 Online
Replication Factor: 2

=== Storage Status ===
Total Capacity: 2.5 TB
Used: 1.8 TB (72%)
Available: 700 GB
Retention Policy: 30 days

{
  "alerts": [
    {
      "id": "alert-uuid-a1b2c3d4",
      "severity": "WARNING",
      "message": "Storage utilization above 70%",
      "timestamp": "2024-01-15T09:32:15Z"
    },
    {
      "id": "alert-uuid-e5f6g7h8",
      "severity": "INFO",
      "message": "Backup completed successfully",
      "timestamp": "2024-01-15T08:00:00Z"
    }
  ],
  "count": 2
}

{
  "agents": [
    {
      "id": "agent-001",
      "hostname": "app-server-01.corp.local",
      "status": "CONNECTED",
      "last_heartbeat": "2024-01-15T09:35:42Z",
      "version": "8.14.2"
    },
    {
      "id": "agent-002",
      "hostname": "app-server-02.corp.local",
      "status": "CONNECTED",
      "last_heartbeat": "2024-01-15T09:35:38Z",
      "version": "8.14.2"
    },
    {
      "id": "agent-003",
      "hostname": "db-server-01.corp.local",
      "status": "DISCONNECTED",
      "last_heartbeat": "2024-01-15T08:12:19Z",
      "version": "8.14.1"
    }
  ],
  "total": 3,
  "connected": 2
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl commands to skip certificate verification, or import the CA certificate into your system trust store. |
    | `401 Unauthorized` | Verify the sessionId bearer token is valid and not expired by obtaining a fresh token via the authentication endpoint. |
    | `curl: (7) Failed to connect to <li-fqdn> port 443: Connection refused` | Confirm the Aria Operations for Logs appliance is running and the FQDN/IP address and port 443 are accessible from your network. |
## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## See also

- [Aria Ops for Logs — Procedures](../procedures/)
- [Aria Operations for Logs — Scripts Reference](../scripts/)
- [Aria Operations for Logs — Health Checks](../health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
