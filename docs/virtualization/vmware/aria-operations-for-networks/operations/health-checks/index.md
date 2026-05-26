# Aria Operations for Networks — Health Checks

## UI Health Dashboard

**UI path:** Settings → Infrastructure → Health

The Health dashboard displays:
- Platform VM status (CPU, memory, disk utilization)
- Per-Collector status (connected/disconnected, flows per second, last heartbeat)
- Per-data-source status (last successful sync, sync errors)
- Active problems count and severity breakdown
- License status and expiry date

Key indicators to check at a glance:

| Indicator | Healthy State | Action if Unhealthy |
|---|---|---|
| Platform VM status | Green / Running | Check services on Platform VM |
| Each Collector status | Connected | See Common Issues — Collector Disconnected |
| vCenter Last Sync | Within last 20 minutes | Re-verify vCenter credentials; check network |
| NSX-T Last Sync | Within last 20 minutes | Re-verify NSX-T API access; check TLS |
| Flows per second | > 0 for each collector | Check NetFlow config on switches; check UDP 2055 |
| Disk usage (Platform) | < 80% | Reduce retention or expand disk |
| License status | Valid / Days remaining > 30 | Renew license in Broadcom licensing portal |

## Verify Collectors Are Connected

**UI:** Settings → Accounts and Data Sources → Collectors

Each Collector should show:
- Status: **Connected**
- Last heartbeat: within the last 2 minutes
- Flows per second: non-zero if any NetFlow source is configured

Via REST API:

```bash
TOKEN=$(curl -sk -X POST "https://aon.example.local/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk "https://aon.example.local/api/ni/collectors" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "
import sys, json
from datetime import datetime, timezone
data = json.load(sys.stdin)
for c in data.get('results', []):
    last_hb = c.get('last_heartbeat_ms', 0) / 1000
    dt = datetime.fromtimestamp(last_hb, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC') if last_hb else 'Never'
    print(f\"{c.get('nickname',''):<25} {c.get('status',''):<15} Last HB: {dt}\")
"
```

## Verify Data Source Sync Status

**UI:** Settings → Accounts and Data Sources → select each source → View Details

Check:
- **Last Sync**: should be recent (vCenter/NSX-T: within 20 minutes)
- **Sync Status**: Success
- **Error message**: if present, indicates auth or connectivity failure

Via REST API:

```bash
curl -sk "https://aon.example.local/api/ni/datasources" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for ds in data.get('results', []):
    name = ds.get('nickname', ds.get('credentials', {}).get('ip', ''))
    dtype = ds.get('datasource_type', '')
    enabled = ds.get('enabled', False)
    last_sync = ds.get('last_successful_collection_time', 'Never')
    print(f'{name:<30} {dtype:<20} Enabled:{enabled} LastSync:{last_sync}')
"
```

## Verify Flow Data Is Being Received

**UI search query** (in the search bar at top of screen):

```text
flows where collector = "aon-collector-dc1" grouped by Flow Type
```

This returns a count of flows grouped by East-West / North-South. If the count is 0 or the query returns no results, flow data is not arriving.

Additional flow verification queries:

```bash
# Flows in the last 15 minutes
flows where time_range = "last 15 minutes"

# Flows from a specific subnet
flows where source ip = "10.10.20.0/24"

# Top talkers by bytes
flows where time_range = "last 1 hour" order by bytes desc
```

**Check flow ingestion via tcpdump on Collector VM:**

```bash
ssh ubuntu@aon-collector.example.local

# Confirm UDP 2055 packets are arriving
sudo tcpdump -i eth0 udp port 2055 -n -c 20

# See which source IPs are sending flows
sudo tcpdump -i eth0 udp port 2055 -n 2>/dev/null | \
  awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head -20
```

## Check Disk Usage on Platform VM

```bash
ssh ubuntu@aon-platform.example.local

# Overall disk layout
df -hT

# Cassandra data (flow store) — typically largest consumer
df -h /var/lib/cassandra

# Elasticsearch (search index)
df -h /var/lib/elasticsearch

# Log directory
df -h /var/log

# Identify top consumers
sudo du -sh /var/lib/cassandra/data/* 2>/dev/null | sort -rh | head -10
sudo du -sh /var/lib/elasticsearch/data/* 2>/dev/null | sort -rh | head -10

# Check inode usage (can exhaust before disk space)
df -i
```

If disk usage exceeds 80% on the data partition, AON will start purging older flow data. If it exceeds 90%, ingestion may pause.

## Certificate Expiry Check

**UI:** Settings → SSL Certificate → view expiry date

Via the Platform VM CLI:

```bash
# Check the currently installed certificate expiry
echo | openssl s_client -connect aon.example.local:443 -servername aon.example.local 2>/dev/null \
  | openssl x509 -noout -dates

# Output example:
# notBefore=Sep 15 00:00:00 2024 GMT
# notAfter=Sep 15 23:59:59 2025 GMT

# Days until expiry
echo | openssl s_client -connect aon.example.local:443 2>/dev/null \
  | openssl x509 -noout -enddate \
  | awk -F= '{print $2}' \
  | xargs -I{} sh -c 'echo "$(( ( $(date -d "{}" +%s) - $(date +%s) ) / 86400 )) days remaining"'
```

Alert at 60 days remaining — certificate replacement in AON requires a UI reload.

## Verify IPFIX/NetFlow Is Arriving

**UI search:** Search → type:

```text
flows where collector = "aon-collector-dc1" and time_range = "last 5 minutes"
```

Zero results indicates no flows are arriving at the Collector. Drill down:

```bash
# Check if any flows exist at all (remove time constraint)
flows where collector = "aon-collector-dc1"

# Check flows by source type
flows where source = ESXi and time_range = "last 1 hour"
flows where source = physical and time_range = "last 1 hour"
```

**From the Collector VM, test UDP 2055 reception directly:**

```bash
# Capture any UDP 2055 traffic for 30 seconds
sudo timeout 30 tcpdump -i eth0 -n udp port 2055 -c 100 -w /tmp/netflow-capture.pcap

# Read the capture
sudo tcpdump -r /tmp/netflow-capture.pcap -n | head -20

# If no packets: check firewall rules between switch and Collector
```

## Key Metrics to Monitor

Configure external monitoring (Nagios, Zabbix, Prometheus with blackbox exporter) to alert on:

| Metric | Check Method | Alert Threshold |
|---|---|---|
| HTTPS reachability | HTTP GET to `https://aon.example.local` | Non-200 response |
| API token auth | POST `/api/ni/auth/token` | Non-200 response |
| Collector status | GET `/api/ni/collectors` → status != CONNECTED | Any collector disconnected |
| Data source sync lag | GET `/api/ni/datasources` → last_sync > 30 min ago | > 30 minutes |
| Open critical problems | GET `/api/ni/problems?status=OPEN&severity=CRITICAL` | Count > 0 |
| Platform disk usage | SSH → `df -h` on data partition | > 80% |
| Flows per second per collector | UI metric / API | = 0 for > 15 minutes |
| Certificate expiry | `openssl s_client` check | < 60 days |

**Monitoring script (outputs Nagios-compatible exit codes):**

```bash
#!/bin/bash
# aon-health-check.sh

PLATFORM="https://aon.example.local"
USER="svc-monitor@local"
PASS="PASSWORD"

TOKEN=$(curl -sk -X POST "${PLATFORM}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${USER}\",\"password\":\"${PASS}\"}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('token',''))" 2>/dev/null)

if [[ -z "$TOKEN" ]]; then
  echo "CRITICAL: Cannot authenticate to AON API"
  exit 2
fi

DISCONNECTED=$(curl -sk "${PLATFORM}/api/ni/collectors" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
bad = [c['nickname'] for c in data.get('results',[]) if c.get('status') != 'CONNECTED']
print(','.join(bad))
")

if [[ -n "$DISCONNECTED" ]]; then
  echo "CRITICAL: Collectors disconnected: $DISCONNECTED"
  exit 2
fi

echo "OK: All collectors connected, API reachable"
exit 0
```

## Check Platform VM Resource Utilization

```bash
ssh ubuntu@aon-platform.example.local

# CPU load
uptime
top -bn1 | head -20

# Memory
free -h

# Process list for AON services
ps aux | grep -E 'java|cassandra|kafka|nginx|postgres|elastic'

# Java heap for platform service (if OutOfMemory suspected)
sudo jmap -heap $(pgrep -f vrni-platform) 2>/dev/null | grep -E 'Heap|used|capacity'
```

If CPU is consistently above 80% or memory is near exhaustion, refer to the Design Standards page for sizing guidance and consider upgrading to the next VM size tier.
