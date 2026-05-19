# Aria Operations for Networks — CLI Reference

```
┌─────────────── Aria Networks CLI: Platform & Collector ────────────────────────┐
│                                                                                 │
│  Platform VM (ssh ubuntu@aon-platform)                                          │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  cat /etc/build.info              ── show version/build                 │   │
│  │  systemctl status vrni-platform   ── main app service                  │    │
│  │  systemctl status nginx cassandra kafka elasticsearch postgres          │   │
│  │  df -hT / df -h /var/lib/cassandra ── disk usage                       │    │
│  │  nc -zv <collector-ip> 443        ── test collector reachability        │   │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  Collector VM (ssh ubuntu@aon-collector)                                         │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  systemctl status ni-collector    ── collector service                  │   │
│  │  journalctl -u ni-collector -f    ── follow collector log               │   │
│  │  sudo pairing.sh                  ── re-pair to Platform VM             │   │
│  │  tcpdump -i eth0 udp port 2055    ── verify NetFlow arriving            │   │
│  │  nc -zv aon-platform 443          ── test upload path                  │    │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  REST API (from anywhere):                                                      │
│  POST /api/ni/auth/token ── get bearer token                                    │
│  GET  /api/ni/collectors  ── collector status                                   │
│  GET  /api/ni/datasources ── data source sync status                            │
│  POST /api/ni/search      ── query flows and topology                           │
└────────────────────────────────────────────────────────────────────────────────┘
```

## SSH Access

**Platform VM** default OS user is `ubuntu`. There is no direct root login via SSH by default.

```bash
ssh ubuntu@aon-platform.example.local

# Become root for service management
sudo -i

# Or use sudo for individual commands
sudo systemctl status vrni-platform
```

**Collector VM** also uses `ubuntu` as the default SSH user.

```bash
ssh ubuntu@aon-collector.example.local
sudo -i
```

SSH is available on port 22. Restrict access to jump hosts only — see Hardening page.

## Platform VM CLI Commands

### Version and Build Info

```bash
# Show platform version
cat /etc/build.info

# Or via the support script
sudo /home/ubuntu/support/show-version.sh
```

Output format:
```
Product: VMware Aria Operations for Networks
Version: 6.14.0
Build: 23456789
Release Date: 2024-09-15
```

### Service Status

```bash
# Check all platform services at once
sudo systemctl status vrni-platform nginx cassandra kafka elasticsearch postgres

# Individual service status
sudo systemctl status vrni-platform      # Main application
sudo systemctl status nginx              # Reverse proxy (UI/API)
sudo systemctl status cassandra          # Flow data store
sudo systemctl status kafka              # Internal message bus
sudo systemctl status elasticsearch      # Search index
sudo systemctl status postgres           # Config database

# Start / stop / restart services
sudo systemctl restart vrni-platform
sudo systemctl restart nginx
```

### List Collectors

```bash
# From the Platform VM, show connected collectors and their status
curl -sk -X GET "https://localhost/api/ni/collectors" \
  -H "Authorization: NetworkInsight $(cat /tmp/api-token)" \
  | python3 -m json.tool

# Or use the support script (if available on your version)
sudo /home/ubuntu/support/list-collectors.sh
```

### Disk Usage

```bash
# Overall disk usage
df -hT

# Data partition specifically (Cassandra data)
df -h /var/lib/cassandra
df -h /var/lib/elasticsearch
df -h /var/log

# Top disk consumers
du -sh /var/lib/cassandra/*
du -sh /var/lib/elasticsearch/*
```

### Network Diagnostics from Platform VM

```bash
# Test connectivity to a Collector
nc -zv 10.10.10.51 443

# Test DNS resolution
nslookup aon-collector.example.local
dig aon-collector.example.local

# Check listening ports
ss -tlnp | grep -E '443|8080|9042|2181|9200'
```

## Collector VM CLI Commands

### Collector Service Status

```bash
ssh ubuntu@aon-collector.example.local
sudo systemctl status ni-collector

# View collector logs
sudo journalctl -u ni-collector -f --since "1 hour ago"
sudo journalctl -u ni-collector -n 200
```

### Re-Pair Collector

```bash
# Trigger re-pairing to Platform VM
sudo /home/ubuntu/support/pairing.sh
# Prompts:
#   Platform FQDN: aon-platform.example.local
#   Pairing key:   <paste key from UI>
```

### Test NetFlow Receipt on Collector

```bash
# Verify UDP 2055 is being received from switches
sudo tcpdump -i eth0 -n udp port 2055 -c 50

# Count packets per second
sudo tcpdump -i eth0 -n udp port 2055 --immediate-mode -q 2>/dev/null | \
  awk 'BEGIN{c=0; t=systime()} {c++; if(systime()-t>=5){print c/5 " pps"; c=0; t=systime()}}'
```

### Test Connectivity from Collector to Data Sources

```bash
# Test vCenter API
curl -sk https://vcenter.example.local/rest/com/vmware/cis/session \
  -X POST -u 'svc-aon:PASSWORD' -o /dev/null -w "HTTP %{http_code}\n"

# Test NSX-T Manager API
curl -sk https://nsxmgr.example.local/api/v1/cluster \
  -u 'svc-aon:PASSWORD' -o /dev/null -w "HTTP %{http_code}\n"

# Test TCP reachability to Platform
nc -zv aon-platform.example.local 443
```

## REST API Usage

### Authentication — Obtain Token

```bash
PLATFORM="https://aon.example.local"

TOKEN=$(curl -sk -X POST "${PLATFORM}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

echo "Token: $TOKEN"
# Token is valid for 24 hours by default
```

Save token for subsequent calls:

```bash
export AON_TOKEN="$TOKEN"
export AON_URL="https://aon.example.local"
```

### List Data Sources

```bash
curl -sk -X GET "${AON_URL}/api/ni/datasources" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -m json.tool
```

Sample output fields: `entity_id`, `nickname`, `credentials.ip`, `datasource_type`, `enabled`, `enabled_at`.

### Get Data Source Sync Status

```bash
# Get all data sources with last sync timestamps
curl -sk -X GET "${AON_URL}/api/ni/datasources" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
ds = json.load(sys.stdin)
for d in ds.get('results', []):
    print(f\"{d.get('nickname',''):<30} {d.get('datasource_type',''):<20} {d.get('enabled','')}\")"
```

### Query Flows (Search API)

AON's search API accepts the same query syntax as the UI search bar:

```bash
# Get flows from a specific VM in the last hour
curl -sk -X POST "${AON_URL}/api/ni/search" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "flows where source vm name = '\''web-01'\'' and time_range = '\''last 1 hour'\''",
    "page": {"start_index": 0, "end_index": 100}
  }' \
  | python3 -m json.tool

# Get flows on a specific port
curl -sk -X POST "${AON_URL}/api/ni/search" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "flows where destination port = 3306 and flow type = East-West",
    "page": {"start_index": 0, "end_index": 200}
  }' \
  | python3 -m json.tool
```

### Get Open Problems

```bash
curl -sk -X GET "${AON_URL}/api/ni/problems?status=OPEN" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for p in data.get('results', []):
    print(f\"{p.get('severity',''):<10} {p.get('name',''):<60} {p.get('entity_id','')}\")"
```

### Get Security Group Recommendations

```bash
# List all applications
curl -sk -X GET "${AON_URL}/api/ni/groups/applications" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -m json.tool

# Get security recommendations for a specific application
APP_ID="application-12345"
curl -sk -X GET "${AON_URL}/api/ni/applications/${APP_ID}/security-groups" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -m json.tool
```

### Get Application Details

```bash
# List all defined applications
curl -sk -X GET "${AON_URL}/api/ni/groups/applications" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for app in data.get('results', []):
    print(f\"{app['entity_id']:<40} {app.get('name','')}\")"

# Get details of one application (replace APP_ID)
APP_ID="application-12345"
curl -sk -X GET "${AON_URL}/api/ni/groups/applications/${APP_ID}" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -m json.tool
```

### Manage Alerts (Pinned Alerts)

```bash
# List all alerts
curl -sk -X GET "${AON_URL}/api/ni/alerts" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -m json.tool

# Acknowledge an alert
ALERT_ID="alert-789"
curl -sk -X PUT "${AON_URL}/api/ni/alerts/${ALERT_ID}/acknowledge" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Acknowledged by ops team"}' \
  | python3 -m json.tool
```

### Export Security Recommendations to NSX

```bash
# Trigger push of recommendations to NSX-T for a given application
APP_ID="application-12345"
NSX_DS_ID="datasource-nsx-001"

curl -sk -X POST "${AON_URL}/api/ni/applications/${APP_ID}/security-groups/export" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"nsx_manager_id\": \"${NSX_DS_ID}\"}" \
  | python3 -m json.tool
```

### Check Collector Health via API

```bash
curl -sk -X GET "${AON_URL}/api/ni/collectors" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data.get('results', []):
    print(f\"{c.get('nickname',''):<30} {c.get('status',''):<15} {c.get('ip_address','')}\")"
```

### API Token Management (API Keys)

```bash
# Create a new API token (for service accounts / scripts)
curl -sk -X POST "${AON_URL}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc-monitoring@local","password":"PASSWORD"}' \
  | python3 -m json.tool

# Revoke a token
curl -sk -X DELETE "${AON_URL}/api/ni/auth/token" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}"
```

## Useful Log Paths

| Log | Path on Platform VM |
|---|---|
| Platform application log | `/var/log/vrni-platform/platform.log` |
| Nginx access log | `/var/log/nginx/access.log` |
| Nginx error log | `/var/log/nginx/error.log` |
| Cassandra log | `/var/log/cassandra/system.log` |
| Kafka log | `/var/log/kafka/server.log` |
| Elasticsearch log | `/var/log/elasticsearch/*.log` |
| Auth/audit log | `/var/log/vrni-platform/audit.log` |

| Log | Path on Collector VM |
|---|---|
| Collector service log | `journalctl -u ni-collector` |
| Collector application log | `/var/log/ni-collector/collector.log` |
