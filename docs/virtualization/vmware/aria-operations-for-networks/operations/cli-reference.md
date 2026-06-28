---
tags:
  - aria-networks
  - operations
  - cli
  - vmware
---
# Aria Operations for Networks — CLI Reference

<div class="kb-summary">
CLI and API reference for Aria Operations for Networks (vRNI): SSH appliance service management, collector operations, IPFIX diagnostics, REST API authentication, flow and data-source queries, application security group export, and VAMI management.

*Applies to: Aria Operations for Networks 6.x*
</div>
![Aria Operations for Networks — CLI Reference](../../../../assets/virtualization-vmware-aria-operations-for-networks-operation.svg)

## Before you begin

- **Access:** SSH to platform VM as `ubuntu` user; sudo to root for service commands
- **Collector access:** SSH to each collector VM separately — collector and platform are separate appliances
- **API token lifetime:** 24 hours by default; re-authenticate if commands return 401

---

## SSH Access

```bash
# Platform VM
ssh ubuntu@aon-platform.corp.local
sudo -i   # become root for service management

# Collector VM
ssh ubuntu@aon-collector.corp.local
sudo -i
```

---

## Platform Service Management

```bash
# Check all platform services at once
sudo systemctl status vrni-platform nginx cassandra kafka elasticsearch postgres

# Individual service status
sudo systemctl status vrni-platform      # Main AON application
sudo systemctl status nginx              # Reverse proxy (UI/API entry point)
sudo systemctl status cassandra          # Flow data store
sudo systemctl status kafka              # Internal message bus
sudo systemctl status elasticsearch      # Search index
sudo systemctl status postgres           # Config/metadata database

# Restart a service
sudo systemctl restart vrni-platform

# View platform application log (first stop for errors)
sudo tail -f /var/log/app.log
sudo journalctl -u vrni-platform -f --since "1 hour ago"
```

---

## Collector Service Management

```bash
# On each collector VM:
sudo systemctl status ni-collector
sudo systemctl restart ni-collector

# Collector logs — shows flow receipt and forwarding status
sudo journalctl -u ni-collector -f --since "1 hour ago"
sudo journalctl -u ni-collector -n 200

# View proxy.log — confirms IPFIX/NetFlow packets received
sudo tail -f /var/log/proxy.log

# Re-pair collector to Platform VM (run if collector shows as offline after IP/cert change)
sudo /home/ubuntu/support/pairing.sh
# Prompts:
#   Platform FQDN: aon-platform.corp.local
#   Pairing key:   <paste from AON UI → Settings → Infrastructure → Collectors>
```

---

## Disk Usage

High disk usage stops flow data collection. Alert at 80%, critical at 90%.

```bash
# Overall disk usage
df -hT

# Data partitions (Cassandra flow store + Elasticsearch index)
df -h /var/lib/cassandra
df -h /var/lib/elasticsearch
df -h /var/log

# Top disk consumers by directory
du -sh /var/lib/cassandra/*
du -sh /var/lib/elasticsearch/*

# Free journal space (safe operation)
sudo journalctl --vacuum-size=1G
```

---

## Network Connectivity Diagnostics

```bash
# Test TCP 443 connectivity to a collector from the platform VM
nc -zv aon-collector.corp.local 443

# Test connectivity to data sources
curl -sk https://vcenter.corp.local/rest/com/vmware/cis/session \
  -X POST -u 'svc-aon:PASSWORD' -o /dev/null -w "HTTP %{http_code}\n"

curl -sk https://nsxmgr.corp.local/api/v1/cluster \
  -u 'svc-aon:PASSWORD' -o /dev/null -w "HTTP %{http_code}\n"

# Check which ports are listening on platform VM
ss -tlnp | grep -E '443|8080|9042|2181|9200'

# DNS resolution test
nslookup aon-collector.corp.local
dig aon-collector.corp.local
```

---

## IPFIX / NetFlow Diagnostics

```bash
# Verify UDP 2055 (NetFlow/IPFIX) is being received from switches/vDS
# Run on the collector VM:
sudo tcpdump -i eth0 -n udp port 2055 -c 50

# Count packets per second arriving
sudo tcpdump -i eth0 -n udp port 2055 --immediate-mode -q 2>/dev/null | \
  awk 'BEGIN{c=0; t=systime()} {c++; if(systime()-t>=5){print c/5 " pps"; c=0; t=systime()}}'

# Expected: 10–1000+ pps on a busy network; 0 pps = IPFIX not reaching collector
```

---

## REST API — Authentication

```bash
AON="https://aon.corp.local"

# Authenticate and store token
TOKEN=$(curl -sk -X POST "${AON}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

echo "Token acquired: ${TOKEN:0:20}..."

# Export for use in subsequent commands
export AON_TOKEN="$TOKEN"
export AON_URL="$AON"

# Create a long-lived service account token
curl -sk -X POST "${AON}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc-monitoring@local","password":"<password>"}' \
  | python3 -m json.tool

# Revoke a token
curl -sk -X DELETE "${AON}/api/ni/auth/token" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}"
```

---

## REST API — Data Sources

```bash
# List all configured data sources with sync status
curl -sk -X GET "${AON_URL}/api/ni/datasources" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
ds = json.load(sys.stdin)
for d in ds.get('results', []):
    print(f\"{d.get('nickname','?'):<30} {d.get('datasource_type','?'):<20} {d.get('enabled','')}\")"

# Get details of a specific data source
DS_ID="datasource-vcenter-001"
curl -sk -X GET "${AON_URL}/api/ni/datasources/${DS_ID}" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" | python3 -m json.tool

# Trigger a manual re-sync on a data source
curl -sk -X POST "${AON_URL}/api/ni/datasources/${DS_ID}/sync" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}"
```

---

## REST API — Flow Queries

```bash
# Get flows from a specific VM in the last hour
curl -sk -X POST "${AON_URL}/api/ni/search" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "flows where source vm name = '\''web-01'\'' and time_range = '\''last 1 hour'\''",
    "page": {"start_index": 0, "end_index": 100}
  }' | python3 -m json.tool

# Get all East-West flows on port 3306 (MySQL)
curl -sk -X POST "${AON_URL}/api/ni/search" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "flows where destination port = 3306 and flow type = East-West",
    "page": {"start_index": 0, "end_index": 200}
  }' | python3 -m json.tool

# List open problems/anomalies
curl -sk -X GET "${AON_URL}/api/ni/problems?status=OPEN" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for p in data.get('results', []):
    print(f\"{p.get('severity',''):<10} {p.get('name',''):<60}\")"
```

---

## REST API — Applications and Security Groups

```bash
# List all defined applications
curl -sk -X GET "${AON_URL}/api/ni/groups/applications" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for app in data.get('results', []):
    print(f\"{app['entity_id']:<40} {app.get('name','')}\")"

# Get NSX-T security group recommendations for an application
APP_ID="application-12345"
curl -sk -X GET "${AON_URL}/api/ni/applications/${APP_ID}/security-groups" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" | python3 -m json.tool

# Push security group recommendations to NSX-T
NSX_DS_ID="datasource-nsx-001"
curl -sk -X POST "${AON_URL}/api/ni/applications/${APP_ID}/security-groups/export" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"nsx_manager_id\": \"${NSX_DS_ID}\"}" | python3 -m json.tool
```

---

## REST API — Collectors and Alerts

```bash
# List all collectors and their status
curl -sk -X GET "${AON_URL}/api/ni/collectors" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data.get('results', []):
    print(f\"{c.get('nickname',''):<30} {c.get('status',''):<15} {c.get('ip_address','')}\")"

# List all active alerts
curl -sk -X GET "${AON_URL}/api/ni/alerts" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" | python3 -m json.tool

# Acknowledge an alert
ALERT_ID="alert-789"
curl -sk -X PUT "${AON_URL}/api/ni/alerts/${ALERT_ID}/acknowledge" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Acknowledged by ops team"}' | python3 -m json.tool
```

---

## See also

- [AON Operational Procedures](procedures/)
- [AON Scripts](scripts/)
- [AON Health Checks](health-checks/)

## Verify

- **Service status:** `sudo systemctl status vrni-platform` shows `active (running)`
- **Flow data:** AON UI → Flow Map — flows visible for known workloads
- **API test:** `curl -sk -H "Authorization: NetworkInsight $AON_TOKEN" "$AON_URL/api/ni/datasources" | python3 -m json.tool` returns datasource list
