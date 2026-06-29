---
tags:
  - operations
  - san
---
# Brocade SANnav — CLI Reference
![Brocade SANnav — CLI Reference](../../../../assets/san-brocade-sannav-operations-cli-reference.svg)

```bash
# Show status of all SANnav services
sannav status

# Start all services
sannav start

# Stop all services (maintenance only)
sannav stop

# Restart all services
sannav restart

# Show current version
sannav version

# Show license summary
sannav license
```


```text title="Expected output"
SANnav Service Status:
  sannav-core         RUNNING (pid 4521)
  sannav-db           RUNNING (pid 4522)
  sannav-api          RUNNING (pid 4523)
  sannav-ui           RUNNING (pid 4524)
  sannav-collector    RUNNING (pid 4525)

Starting SANnav services...
  sannav-core         [OK]
  sannav-db           [OK]
  sannav-api          [OK]
  sannav-ui           [OK]
  sannav-collector    [OK]
All services started successfully.

Stopping SANnav services...
  sannav-collector    [OK]
  sannav-ui           [OK]
  sannav-api          [OK]
  sannav-db           [OK]
  sannav-core         [OK]
All services stopped.

Restarting SANnav services...
  Stopping services...  [OK]
  Starting services...  [OK]
All services restarted successfully.

SANnav Version: 2.3.1.0 (Build 2024.01.15)
License Summary:
  License Status:     VALID
  Expiration Date:    2025-12-31
  Licensed Switches:  256
  Licensed Hosts:     1024
  Current Usage:      48 switches, 312 hosts
```

!!! warning "Common errors"
    **`sannav: command not found`** — Ensure SANnav is installed and `/opt/sannav/bin` is in your PATH, or use the full path `/opt/sannav/bin/sannav`.
    **`Error: Failed to start sannav-db [FAILED]`** — Check database disk space with `df -h /var/lib/sannav` and verify database service logs with `journalctl -u sannav-db -n 50`.
    **`Error: License expired or invalid`** — Renew or update your SANnav license file in `/opt/sannav/etc/license.key` and restart services.
```bash
# Show current IP configuration
ip addr show eth0

# Show hostname
hostname

# Show DNS configuration
cat /etc/resolv.conf

# Test connectivity to a managed switch
curl -sk -o /dev/null -w "%{http_code}" https://<switch-ip>/rest/loginresult
# Expected: 200 or 401 (reachable); anything else = connectivity problem

# Test LDAP connectivity
ldapsearch -H ldaps://ldap.corp.example.com \
  -D "CN=sannav-svc,OU=Service Accounts,DC=corp,DC=example,DC=com" \
  -w <password> -b "DC=corp,DC=example,DC=com" "(sAMAccountName=testuser)"
```

```text title="Expected output"
1: lo    inet 127.0.0.1/8 scope host lo
1: lo    inet6 ::1/128 scope host lo
2: eth0  inet 192.168.10.45/24 brd 192.168.10.255 scope global eth0
2: eth0  inet6 fe80::250:56ff:fe9a:b1c2/64 scope link

sannav-mgmt-01.corp.example.com

nameserver 192.168.1.10
nameserver 192.168.1.11
search corp.example.com

200

# search result
search: 2
result: 0 Success

dn: CN=testuser,OU=Users,DC=corp,DC=example,DC=com
objectClass: person
objectClass: organizationalPerson
objectClass: user
sAMAccountName: testuser
mail: testuser@corp.example.com
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to <switch-ip> port 443: Connection refused`** — Verify the switch IP is correct and the management interface is reachable with `ping <switch-ip>` before retrying.
    **`ldap_sasl_bind(SIMPLE): Can't contact LDAP server (-1)`** — Confirm LDAP server hostname resolves and port 636 is accessible; check firewall rules and DNS with `nslookup ldaps://ldap.corp.example.com`.
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the DN path matches your Active Directory structure.
```bash
# Main application log
tail -f /opt/sannav/logs/server.log

# Discovery engine log
tail -f /opt/sannav/logs/discovery.log

# Event processing log
tail -f /opt/sannav/logs/event-engine.log

# Upgrade log
cat /opt/sannav/logs/upgrade.log

# Search logs for errors in the last 100 lines
grep -i "ERROR\|FATAL\|Exception" /opt/sannav/logs/server.log | tail -100

# Show system journal (OS-level)
journalctl -u sannav -n 100 --no-pager
```

```text title="Expected output"
==> /opt/sannav/logs/server.log <==
2024-01-15 14:32:18.456 [INFO] SANnav Server started on 0.0.0.0:8443
2024-01-15 14:32:45.123 [INFO] Database connection pool initialized: 20 connections
2024-01-15 14:33:02.789 [INFO] License validation successful - Enterprise Edition
2024-01-15 14:35:11.234 [WARN] Fabric discovery cycle 3 completed: 247 devices scanned
2024-01-15 14:36:55.567 [INFO] Event queue processed: 1,234 events in 2.3s

==> /opt/sannav/logs/discovery.log <==
2024-01-15 14:33:15.891 [INFO] Starting discovery on fabric: prod-fabric-01
2024-01-15 14:33:42.456 [INFO] Discovered 156 switches, 892 ports active
2024-01-15 14:34:18.123 [INFO] Zoning configuration retrieved: 34 zones
2024-01-15 14:35:05.789 [WARN] Device 10.50.12.45 (switch-core-02) response time: 1247ms

==> /opt/sannav/logs/event-engine.log <==
2024-01-15 14:32:50.234 [INFO] Event engine initialized with 8 worker threads
2024-01-15 14:33:21.567 [INFO] Alert rule engine loaded: 156 rules active
2024-01-15 14:34:44.891 [INFO] Event correlation: 23 related events grouped
2024-01-15 14:36:12.345 [INFO] Notification sent to syslog: 12 alerts

Upgrade log (empty or not present):
cat: /opt/sannav/logs/upgrade.log: No such file or directory

ERROR|FATAL|Exception search results:
2024-01-14 22:15:33.456 [ERROR] Connection timeout to fabric switch 10.50.8.12 after 30s
2024-01-14 23:42:18.789 [ERROR] SNMP trap processing failed: Invalid OID format
2024-01-13 18:05:22.123 [FATAL] Database connection lost - reconnecting...
2024-01-13 18:05:24.567 [ERROR] Exception in thread "EventProcessor-3": java.net.SocketTimeoutException

Jan 15 14:32:18 sannav-prod systemd[1]: Started SANnav Application Server.
Jan 15 14:32:45 sannav-prod sannav[2847]: Database pool initialized
Jan 15 14:33:02 sannav-prod sannav[2847]: License check passed
Jan 15 14:35:11 sannav-prod sannav[2847]: Fabric discovery completed
Jan 15 14:36:55 sannav-prod sannav[2847]: Event processing: queue depth 234
```

!!! warning "Common errors"
    **`cat: /opt/sannav/logs/upgrade.log: No such
```bash
# Disk usage
df -h

# Check SANnav data directory size
du -sh /opt/sannav/data/

# Check database sizes individually
du -sh /opt/sannav/data/postgres/
du -sh /opt/sannav/data/influxdb/

# Memory usage
free -h

# CPU load
uptime
```

```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       500G  287G  213G  58% /
/dev/sda2       200G  156G   44G  78% /opt
/dev/sdb1      1000G  892G  108G  89% /data
tmpfs            32G     0   32G   0% /dev/shm
/dev/sdc1       2000G 1847G  153G  92% /backup

4.2T	/opt/sannav/data/

892G	/opt/sannav/data/postgres/
1.8T	/opt/sannav/data/influxdb/

              total        used        free      shared  buff/cache   available
Mem:            64Gi        48Gi        8.2Gi       2.1Gi        7.8Gi        14Gi
Swap:           16Gi        6.2Gi        9.8Gi

 10:47:23 up 127 days, 14:32,  3 users,  load average: 2.14, 2.08, 1.97
```

!!! warning "Common errors"
    **`du: cannot access '/opt/sannav/data/': Permission denied`** — Run the command with `sudo` or ensure the user has read permissions on the SANnav data directory.
    **`Filesystem /opt/sannav/data/ is 100% full`** — Archive or delete old metrics data from InfluxDB or PostgreSQL, or expand the underlying storage volume.
```bash
# Login — obtain token
TOKEN=$(curl -sk -X POST https://sannav-dc1.corp.example.com/rest/login \
  -H "Content-Type: application/json" \
  -d '{"credentials":{"loginName":"svc-monitor","password":"<password>"}}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['authToken'])")

echo "Token: $TOKEN"

# Logout (always clean up sessions)
curl -sk -X DELETE https://sannav-dc1.corp.example.com/rest/logout \
  -H "Authorization: Bearer $TOKEN"
```

```text title="Expected output"
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdmMtbW9uaXRvciIsImlhdCI6MTcwOTMxNjU0MiwiZXhwIjoxNzA5MzIwMTQyfQ.kR7mN9pQxZ2vL4wJ8hF3gT6bY1cD5eA9sK2nM0oP7qR
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   287  100   287    0     0   1245      0 --:--:-- --:--:-- 0.00s
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl (already present) or import the CA certificate into your system trust store.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Verify credentials are correct and the SanNav REST API endpoint is responding; check firewall/network connectivity to sannav-dc1.corp.example.com.
    **`curl: (7) Failed to connect to sannav-dc1.corp.example.com port 443: Connection refused`** — Confirm the SanNav service is running and listening on port 443 using `systemctl status sannav` on the target host.
```bash
# List all resource groups (fabrics)
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# List all switches
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/switches \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Get a specific switch (replace <switchId>)
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/all/switches/<switchId>" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# List all ports (can be large — pipe through grep for filtering)
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/ports \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool | grep -E '"portState"|"portType"|"portWwn"'
```

```text title="Expected output"
{
  "resourceGroups": [
    {
      "id": "fabric-prod-01",
      "name": "Production Fabric",
      "description": "Primary SAN fabric",
      "switchCount": 4
    },
    {
      "id": "fabric-dr-01",
      "name": "DR Fabric",
      "description": "Disaster recovery fabric",
      "switchCount": 2
    }
  ]
}
{
  "switches": [
    {
      "switchId": "sw-brocade-001",
      "switchName": "brocade-prod-01.corp.example.com",
      "switchType": "Brocade G630",
      "ipAddress": "10.50.12.45",
      "fabricId": "fabric-prod-01",
      "status": "Online"
    },
    {
      "switchId": "sw-brocade-002",
      "switchName": "brocade-prod-02.corp.example.com",
      "ipAddress": "10.50.12.46",
      "switchType": "Brocade G630",
      "fabricId": "fabric-prod-01",
      "status": "Online"
    },
    {
      "switchId": "sw-brocade-003",
      "switchName": "brocade-dr-01.corp.example.com",
      "ipAddress": "10.51.12.45",
      "switchType": "Brocade G620",
      "fabricId": "fabric-dr-01",
      "status": "Online"
    }
  ]
}
{
  "switch": {
    "switchId": "sw-brocade-001",
    "switchName": "brocade-prod-01.corp.example.com",
    "switchType": "Brocade G630",
    "ipAddress": "10.50.12.45",
    "fabricId": "fabric-prod-01",
    "status": "Online",
    "portCount": 48,
    "firmwareVersion": "9.1.2a",
    "serialNumber": "BRD-2021-0847392"
  }
}
      "portState": "Online",
      "portType": "E_Port",
      "portWwn": "50:00:14:40:5c:2a:b1:01"
    },
    {
      "portState": "Online",
      "portType": "F_Port",
      "portWwn": "50:00:14:40:5c:2a:b1:02"
    },
    {
      "portState": "Offline",
      "portType": "F_Port",
      "portWwn": "50:00:14:40:5c:2a:b1:03"
    },
...
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in the example, but ensure it's included if removed).
    **`jq: command not found` or `json.tool: No module named json`** — Install Python 3 (`apt-get install python3`) or use `jq` instead of `python3 -
```bash
# Get active alerts (last 100)
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/all/events?limit=100&filter=acknowledged:false" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Get events for a specific switch
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/all/events?switchId=<switchId>" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

```text title="Expected output"
{
  "data": [
    {
      "eventId": "evt-2024-001847",
      "severity": "critical",
      "message": "Port 0/24 on switch brocade-fc01 is offline",
      "timestamp": "2024-01-15T14:32:18Z",
      "acknowledged": false,
      "switchId": "switch-5f8a2c1d"
    },
    {
      "eventId": "evt-2024-001846",
      "severity": "warning",
      "message": "Temperature threshold exceeded on PSU 2",
      "timestamp": "2024-01-15T14:28:05Z",
      "acknowledged": false,
      "switchId": "switch-5f8a2c1d"
    },
    {
      "eventId": "evt-2024-001845",
      "severity": "info",
      "message": "Fabric reconfiguration completed",
      "timestamp": "2024-01-15T14:15:42Z",
      "acknowledged": false,
      "switchId": "switch-7b3e9f4a"
    }
  ],
  "totalCount": 47,
  "pageSize": 100
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in example, but ensure it's not removed).
    **`{"error": "Unauthorized", "code": 401}`** — Verify `$TOKEN` environment variable is set with a valid bearer token via `echo $TOKEN`.
    **`curl: (7) Failed to connect to sannav-dc1.corp.example.com port 443: Name or service not known`** — Confirm DNS resolution and network connectivity to the SAN Nav appliance with `nslookup sannav-dc1.corp.example.com`.
```bash
# Get defined zone set for a fabric
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/<fabricId>/zonedb" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Get active zone set
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/<fabricId>/zones/active" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

```text title="Expected output"
{
  "zoneSetName": "PROD_ZONESET_v2.3",
  "zoneSetId": "0x0a0b0c0d",
  "zones": [
    {
      "zoneName": "ZONE_STORAGE_PROD",
      "zoneId": "0x1a2b3c4d",
      "members": [
        {
          "memberType": "wwn",
          "memberValue": "50:00:14:40:5a:6b:7c:8d"
        },
        {
          "memberType": "wwn",
          "memberValue": "50:00:14:40:5a:6b:7c:9e"
        }
      ]
    },
    {
      "zoneName": "ZONE_BACKUP_PROD",
      "zoneId": "0x2d3e4f5a",
      "members": [
        {
          "memberType": "wwn",
          "memberValue": "50:00:14:40:5a:6b:7c:af"
        }
      ]
    }
  ],
  "status": "active"
}
{
  "activeZoneSetName": "PROD_ZONESET_v2.3",
  "activeZoneSetId": "0x0a0b0c0d",
  "activationTime": "2024-01-15T09:42:33Z",
  "activatedBy": "admin@corp.example.com",
  "memberCount": 12,
  "zoneCount": 3
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in the example, but ensure it's not removed).
    **`{"error": "Unauthorized", "code": 401}`** — Verify the `$TOKEN` variable is set and valid by running `echo $TOKEN` and refreshing credentials if expired.
    **`curl: (7) Failed to connect to sannav-dc1.corp.example.com port 443`** — Confirm the SANnav hostname is correct and the management interface is reachable with `ping sannav-dc1.corp.example.com`.
```bash
# Export all switches to CSV (use Accept header for CSV format)
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/switches \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: text/csv" -o switches-$(date +%Y%m%d).csv

echo "Exported to switches-$(date +%Y%m%d).csv"
```

```text title="Expected output"
Exported to switches-20250114.csv
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification (already present in the example, so ensure your curl version supports it or use `--insecure` instead).
    **`curl: (401) Unauthorized`** — Verify the `$TOKEN` variable is set and valid by running `echo $TOKEN` and confirming it matches an active API token from SANnav.
    **`curl: (7) Failed to connect to sannav-dc1.corp.example.com port 443`** — Check network connectivity and DNS resolution with `ping sannav-dc1.corp.example.com` and `nslookup sannav-dc1.corp.example.com`.
```bash
# List available firmware images
curl -sk https://sannav-dc1.corp.example.com/rest/firmware/images \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Initiate firmware upgrade on a switch
curl -sk -X POST "https://sannav-dc1.corp.example.com/rest/firmware/upgrade" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "switchIds": ["<switchId>"],
    "firmwareVersion": "9.2.1a",
    "activationMode": "AUTO"
  }' | python3 -m json.tool
```

```text title="Expected output"
{
  "images": [
    {
      "id": "img-fw-9.2.1a",
      "version": "9.2.1a",
      "releaseDate": "2024-01-15",
      "size": 524288000,
      "checksum": "a7f3e9c2b1d4f8e6",
      "status": "available"
    },
    {
      "id": "img-fw-9.1.2",
      "version": "9.1.2",
      "releaseDate": "2023-11-22",
      "size": 512000000,
      "checksum": "b2c8f1a9d3e5g7h4",
      "status": "available"
    },
    {
      "id": "img-fw-9.0.0",
      "version": "9.0.0",
      "releaseDate": "2023-09-10",
      "size": 498000000,
      "checksum": "c5d1e8f2a9b3g6h1",
      "status": "deprecated"
    }
  ]
}
{
  "taskId": "task-upgrade-20240218-001",
  "status": "INITIATED",
  "switchIds": ["10.50.12.45"],
  "firmwareVersion": "9.2.1a",
  "activationMode": "AUTO",
  "startTime": "2024-02-18T14:32:05Z",
  "estimatedDuration": 1800,
  "progress": 0
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in the example, but ensure `curl` version supports it).
    **`"error": "Invalid or expired token"`** — Regenerate the `$TOKEN` variable using the authentication endpoint and ensure it hasn't exceeded its TTL.
    **`"error": "Switch ID not found or not managed by this SANnav instance"`** — Verify the switch ID exists in SANnav inventory with `curl -sk https://sannav-dc1.corp.example.com/rest/switches -H "Authorization: Bearer $TOKEN"`.
```bash
# Count managed switches by connectivity state
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/switches \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -c "
import sys, json, collections
data = json.load(sys.stdin)
states = collections.Counter(s.get('connectivityState') for s in data.get('switches', []))
print(dict(states))
"

# List all offline F_Ports (potential host/storage connectivity issues)
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/ports \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for p in data.get('ports', []):
    if p.get('portType') == 'F_PORT' and p.get('portState') != 'ONLINE':
        print(p.get('switchName'), p.get('portIndex'), p.get('portState'))
"
```


```text title="Expected output"
{'ONLINE': 47, 'OFFLINE': 3, 'UNKNOWN': 1}
switch-dc1-01 12 OFFLINE
switch-dc1-02 5 OFFLINE
switch-dc1-03 48 OFFLINE
switch-dc2-01 3 OFFLINE
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl (already present) or import the certificate into your system's CA bundle.
    **`curl: (7) Failed to connect to sannav-dc1.corp.example.com port 443: Connection refused`** — Verify the SAN Nav appliance is running and accessible on the network; check firewall rules and DNS resolution with `nslookup sannav-dc1.corp.example.com`.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1`** — Confirm the `$TOKEN` variable is set and valid by running `echo $TOKEN` and regenerating it if expired.
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Sannav — Procedures](../procedures/)
- [Sannav — Scripts](../scripts/)
- [Sannav — Health Checks](../health-checks/)
