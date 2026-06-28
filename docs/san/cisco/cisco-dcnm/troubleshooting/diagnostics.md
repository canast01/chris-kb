---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
---
# Cisco DCNM — Diagnostics

<div class="kb-summary">
Cisco DCNM (Data Center Network Manager) diagnostic commands: check all service health with appmgr status, query the REST health API, inspect PostgreSQL and Elasticsearch database state, test SSH and SNMP connectivity to managed switches, debug discovery failures, check HA replication lag, and collect the support bundle for Cisco TAC cases.

*Applies to: Cisco DCNM 11.x / NDFC (Nexus Dashboard Fabric Controller) 12.x*
</div>
![Cisco DCNM — Diagnostics](../../../../assets/san-cisco-cisco-dcnm-troubleshooting-diagnostics.svg)




```mermaid
graph TD
    A([DCNM Issue]) --> B{What type of problem?}
    B -->|DCNM UI or API unresponsive| C[appmgr status\nGET /rest/health]
    B -->|Switch discovery failing| D[grep switch-IP /var/log/dcnm/discovery.log\nTest SSH and SNMP to switch]
    B -->|Performance data missing| E[appmgr db-status\nCheck pmdb size and retention]
    B -->|Slow UI or API timeouts| F[Measure REST API response time\nCheck PostgreSQL slow queries]
    B -->|HA failover or split-brain| G[dcnm-ha-status.sh\nCheck replication lag on standby]
    B -->|Analytics or topology wrong| H[curl localhost:9200/_cluster/health\nCheck Elasticsearch shard state]
    C --> I{Which service down?}
    I -->|dcnm| J[journalctl -u dcnm -n 100\nCheck disk space: df -h]
    I -->|postgres| K[pg_isready -U postgres\njournalctl -u postgresql -n 50]
    I -->|elasticsearch| L[curl localhost:9200/_cluster/health\nCheck if disk is full]
    D --> M[ssh -v dcnm_mgmt@switch-ip show version\nsnmpget -v3 switch-ip sysDescr.0]
    E --> N[psql -U postgres pmdb\nSELECT count FROM pmdata; check retention]
    F --> O[time curl REST /rest/inventory/switches\nSELECT pid,duration,query FROM pg_stat_activity WHERE state != idle]
    G --> P[psql -U postgres\nSELECT now() - pg_last_xact_replay_timestamp]
    H --> Q[curl localhost:9200/_cluster/health?pretty\nCheck status=red or yellow unassigned shards]
    J --> R[Collect DCNM support bundle\ncollect-support-bundle.sh]
    K --> R
    L --> R
    M --> R
    N --> R
    O --> R
    P --> R
    Q --> R
    R --> S[Open Cisco TAC case\nAttach bundle and switch show tech-support]

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,B,I dark
    class C,D,E,F,G,H,J,K,L,M,N,O,P,Q action
    class R,S escalate
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_dcnm_service_status: "Step 1 — Check DCNM service status" {shape: rectangle}
step_2_authenticate_and_check_rest_a: "Step 2 — Authenticate and check REST API" {shape: rectangle}
step_3_check_postgresql_database_hea: "Step 3 — Check PostgreSQL database health" {shape: rectangle}
step_4_test_switch_connectivity: "Step 4 — Test switch connectivity" {shape: rectangle}
step_5_debug_discovery_and_fabric_is: "Step 5 — Debug discovery and fabric issues" {shape: rectangle}
step_6_check_ha_replication_status: "Step 6 — Check HA replication status" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_dcnm_service_status: investigate
symptom -> step_2_authenticate_and_check_rest_a: investigate
symptom -> step_3_check_postgresql_database_hea: investigate
symptom -> step_4_test_switch_connectivity: investigate
symptom -> step_5_debug_discovery_and_fabric_is: investigate
symptom -> step_6_check_ha_replication_status: investigate
step_1_check_dcnm_service_status -> resolution
step_2_authenticate_and_check_rest_a -> resolution
step_3_check_postgresql_database_hea -> resolution
step_4_test_switch_connectivity -> resolution
step_5_debug_discovery_and_fabric_is -> resolution
step_6_check_ha_replication_status -> resolution
```

## Before you begin

- **Access:** SSH to DCNM server (root or admin); DCNM admin UI credentials; SSH access to managed MDS/NX-OS switches
- **Gather first:** the specific symptom (switch not discovered, no performance data for a fabric, UI unreachable), the switch name or fabric name affected, and when the issue started
- **Scope:** confirm whether the issue affects one switch, one fabric, or the entire DCNM platform

---

## Step 1 — Check DCNM service status

```bash
# SSH to DCNM
ssh root@dcnm-dc1.corp.example.com

# Check all DCNM application services
appmgr status
# Expected: all services showing "running" state
# Problem: any service in "stopped" or "restarting" state

# Check disk space (Elasticsearch fills disk causing cascading failures)
df -h
# Expected: all mounts < 80% used; /data often fills first

# Check DCNM REST API health (no auth required)
curl -sk https://localhost/rest/health | python3 -m json.tool
# Expected: all components healthy

# Check DCNM database status
appmgr db-status
# Expected: all databases connected

# Check ports are listening
netstat -tlnp | grep -E "443|5432|9200"
# Expected: 443=DCNM HTTPS, 5432=PostgreSQL, 9200=Elasticsearch
```

---

## Step 2 — Authenticate and check REST API

```bash
# Get DCNM API session cookie
DCNM_HOST="https://dcnm-dc1.corp.example.com"
curl -sk -c dcnm-cookie.txt -X POST "$DCNM_HOST/rest/logon" \
  -H "Content-Type: application/json" \
  -d '{"expirationTime":600000}' \
  -u admin:<password> | python3 -m json.tool
# Expected: token in response body; cookie saved to dcnm-cookie.txt

# Get inventory of all switches
curl -sk -b dcnm-cookie.txt "$DCNM_HOST/rest/inventory/switches" \
  | python3 -c "
import json,sys
for sw in json.load(sys.stdin):
    print(sw.get('ipAddress',''), '|', sw.get('logicalName',''), '|', sw.get('managementState',''))
"
# Expected: managementState = manageable or managed for all switches

# Measure REST API response time (baseline < 3 seconds for < 200 switches)
time curl -sk -b dcnm-cookie.txt "$DCNM_HOST/rest/inventory/switches" > /dev/null

# Trigger manual rediscovery for a specific switch
curl -sk -b dcnm-cookie.txt -X POST \
  "$DCNM_HOST/rest/san/fabric/rediscover" \
  -H "Content-Type: application/json" \
  -d '{"fabricName": "DC1-FABRIC-A", "rediscoverAll": false,
       "switchSerialNumbers": ["<serialNumber>"]}'
```

---

## Step 3 — Check PostgreSQL database health

```bash
# Test if PostgreSQL accepts connections
pg_isready -U postgres
# Expected: /tmp/.s.PGSQL.5432 - accepting connections

# Connect to DCNM configuration database
psql -U postgres sane

-- Check table sizes (find unexpectedly large tables)
SELECT relname, pg_size_pretty(pg_relation_size(relid)) AS size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_relation_size(relid) DESC LIMIT 20;

-- Check slow queries
SELECT pid, now() - query_start AS duration, state, left(query, 100)
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC LIMIT 10;

-- Check for table bloat (dead tuples)
SELECT relname, n_dead_tup, n_live_tup,
  round(n_dead_tup::numeric/greatest(n_live_tup,1)*100, 1) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;
\q

# If bloat is high, run VACUUM
sudo -u postgres vacuumdb --all --analyze

# Check performance data database size
psql -U postgres pmdb
-- Check size
SELECT pg_size_pretty(pg_database_size('pmdb'));
-- Check oldest and newest data points
SELECT min(collecttime), max(collecttime) FROM pmdata;
\q
# If pmdb is consuming excessive disk:
# DCNM GUI → Administration → Settings → Data Retention
# Reduce performance data retention to 14 days
```

---

## Step 4 — Test switch connectivity

```bash
# Test SSH from DCNM to a managed switch
ssh -v -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
  dcnm_mgmt@<switch-ip> 'show version brief' 2>&1
# Expected: MDS or NX-OS version string; failure = SSH auth or connectivity issue

# Test SNMP v3 GET (confirm DCNM polling credentials work)
snmpget -v3 -u dcnm_poll -l authPriv \
  -a SHA -A <auth-pass> -x AES -X <priv-pass> \
  <switch-ip> sysDescr.0
# Expected: MDS IOS system description string; Error = SNMP credential mismatch

# Confirm SNMP traps are arriving from switches
tcpdump -i eth0 -n udp port 162 -c 20
# Each line = one trap from a switch; no output = switches not sending or firewall blocking

# Capture SNMP trap traffic to file for analysis
tcpdump -i eth0 -n udp port 162 -c 200 -w /tmp/dcnm-trap-capture.pcap
```

---

## Step 5 — Debug discovery and fabric issues

```bash
# Search discovery log for a specific switch IP
grep "<switch-ip>" /var/log/dcnm/discovery.log | tail -50
# Look for: "Discovery failed", "unreachable", "auth failed", "timeout"

# Enable discovery debug for a specific switch
grep "10.20.1.5" /var/log/dcnm/discovery.log | tail -50

# Check discovery.log for recent errors across all switches
grep -i "error\|fail\|unreachable" /var/log/dcnm/discovery.log | tail -100

# Check journalctl for DCNM service-level errors
journalctl -u dcnm -n 200 --no-pager | grep -i "error\|exception\|fail"

# System resource snapshot (for performance baseline)
echo "=== $(date) ===" >> /tmp/dcnm-perf.txt
free -h >> /tmp/dcnm-perf.txt
df -h >> /tmp/dcnm-perf.txt
uptime >> /tmp/dcnm-perf.txt
iostat -x 1 3 >> /tmp/dcnm-perf.txt
ps aux --sort=-%cpu | head -15 >> /tmp/dcnm-perf.txt
```

---

## Step 6 — Check HA replication status

```bash
# On either DCNM HA node
/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-status.sh
# Expected output:
# Active Node: 10.10.5.10 (THIS NODE)
# Standby Node: 10.10.5.11 (synchronized)
# VIP: 10.10.5.15 (active)
# DB Replication Lag: 0 ms

# Check PostgreSQL replication lag (on standby node)
psql -U postgres -c "
SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;"
# Expected: < 1 second; > 1 minute = investigate HA link or replication error

# Check HA log for failover events
tail -100 /var/log/dcnm/ha.log | grep -i "error\|fail\|disconnect\|failover"

# Check Elasticsearch cluster health (unassigned shards = topology data at risk)
curl -s "localhost:9200/_cluster/health?pretty"
# Expected: status=green; yellow=1+ replica unassigned; red=primary shard missing
```

---

## Step 7 — Collect support bundle for Cisco TAC

```bash
# Generate DCNM support bundle
/usr/local/cisco/dcm/dcnm/bin/collect-support-bundle.sh \
  --output /tmp/dcnm-support-$(date +%Y%m%d).tar.gz
# Includes: all /var/log/dcnm/ logs, DB schema dump, OS state, DCNM config (masked)

# Transfer to workstation
scp root@dcnm-dc1.corp.example.com:/tmp/dcnm-support-$(date +%Y%m%d).tar.gz ./

# Also collect switch show tech-support for each affected switch
# SSH to each MDS or NX-OS switch:
ssh admin@<switch-ip>
show tech-support > /tmp/show-tech-$(hostname)-$(date +%Y%m%d).txt
exit
# Transfer the show tech file: scp admin@<switch-ip>:/tmp/show-tech-*.txt ./

# For the Cisco TAC case, include:
# - DCNM support bundle .tar.gz
# - show tech-support from affected switches
# - Discovery log excerpt (grep for the affected switch IP)
# - DCNM version: appmgr version or DCNM UI → About
# - Fabric name and switch serial number / IP
```

---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| DCNM application | `journalctl -u dcnm` | Service crash and startup errors |
| Discovery | `/var/log/dcnm/discovery.log` | Per-switch discovery attempts and failures |
| HA events | `/var/log/dcnm/ha.log` | Failover events, replication lag |
| PostgreSQL | `journalctl -u postgresql` | DB start/stop, replication errors |
| Elasticsearch | `curl localhost:9200/_cluster/health` | Shard health and disk pressure |
| DCNM general | `/var/log/dcnm/` | Full log directory; multiple components |

---

## See also

- [Cisco DCNM — Common Issues](../common-issues/)
- [Cisco DCNM — Escalation](../escalation/)

## Verify resolution

- `appmgr status` shows all services running
- `curl -sk https://localhost/rest/health` returns all components healthy
- `grep <switch-ip> /var/log/dcnm/discovery.log | tail -5` shows successful discovery
- `time curl -sk -b dcnm-cookie.txt $DCNM_HOST/rest/inventory/switches` completes in < 5 seconds
- `curl localhost:9200/_cluster/health` returns `"status":"green"` for Elasticsearch
