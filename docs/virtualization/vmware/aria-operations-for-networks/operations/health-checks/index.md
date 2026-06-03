# vRNI Health Checks

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

```text
┌───────────────────────────────────────── vRNI Health Checks ──────────────────────────────────────────┐
│                                                                                                       │
│  Data source status, flow freshness, and collector health checks for vRNI.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Data Source Health              │  │               Collector Health              │   │
│   │          All sources: green status?          │  │           Collector: online in UI?          │   │
│   │         Last sync time < 15 minutes          │  │             Flow rate: non-zero?            │   │
│   │          Credential test: passing?           │  │         Collector service: running?         │   │
│   │         Red source: check API access         │  │            proxy.log: no errors?            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Source and collector health feed into overall platform flow freshness validation.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Flow Freshness Checks             │  │               Platform Health               │   │
│   │          Flows updated < 5 min ago?          │  │              Disk usage < 80%?              │   │
│   │          Flow Map: traffic visible?          │  │            CPU/RAM within sizing?           │   │
│   │         Search returns live results?         │  │              NTP sync: in sync?             │   │
│   │        Alert rules: firing correctly?        │  │            Services: all running?           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM on vSphere; collector VMs per segment; monitoring via vROps optional                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Data Source Status  = Green/Yellow/Red indicator in vRNI UI for each configured source               │
│  Flow Freshness      = Time since last flow record received; should be < 5 minutes                    │
│  Collector Online    = Collector registered and heartbeating to platform                              │
│  proxy.log           = Collector log file; shows flow receipt rate and forwarding errors              │
│  Credential Test     = vRNI API validation that stored source credentials still work                  │
│  Flow Map            = Real-time traffic topology view; blank = no flows received                     │
│  NTP Sync            = Time accuracy required for flow timestamp correlation                          │
│  Disk Usage          = Platform datastore; >80% causes flow drop and performance issues               │
│  Alert Rule          = Configured threshold; validate firing on known traffic pattern                 │
│  Service Status      = SSH: service network-insight status; collector: service collector              │
│  Support Bundle      = Full diagnostic archive; generate if platform health is degraded               │
│  Sizing Headroom     = CPU/RAM utilisation should stay below 75% for stable operation                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Flows in the last 15 minutes
flows where time_range = "last 15 minutes"

# Flows from a specific subnet
flows where source ip = "10.10.20.0/24"

# Top talkers by bytes
flows where time_range = "last 1 hour" order by bytes desc
```
```bash
ssh ubuntu@aon-collector.example.local

# Confirm UDP 2055 packets are arriving
sudo tcpdump -i eth0 udp port 2055 -n -c 20

# See which source IPs are sending flows
sudo tcpdump -i eth0 udp port 2055 -n 2>/dev/null | \
  awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head -20
```
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
```text
flows where collector = "aon-collector-dc1" and time_range = "last 5 minutes"
```
```bash
# Check if any flows exist at all (remove time constraint)
flows where collector = "aon-collector-dc1"

# Check flows by source type
flows where source = ESXi and time_range = "last 1 hour"
flows where source = physical and time_range = "last 1 hour"
```
```bash
# Capture any UDP 2055 traffic for 30 seconds
sudo timeout 30 tcpdump -i eth0 -n udp port 2055 -c 100 -w /tmp/netflow-capture.pcap

# Read the capture
sudo tcpdump -r /tmp/netflow-capture.pcap -n | head -20

# If no packets: check firewall rules between switch and Collector
```
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
