# Cisco DCNM — Diagnostics

> Part of the [Cisco DCNM](../../) reference.

---

## Overview

This page covers diagnostic procedures and log collection steps for investigating DCNM application issues, performance degradation, or preparing for Cisco TAC escalation.

---

## Log File Locations

| Log | Content |
|---|---|
| `/var/log/dcnm/server.log` | Main application log — startup, API, errors |
| `/var/log/dcnm/discovery.log` | Fabric discovery and switch crawl |
| `/var/log/dcnm/pm.log` | Performance manager polling |
| `/var/log/dcnm/events.log` | SNMP trap and event processing |
| `/var/log/dcnm/install.log` | Upgrade and patch installation |
| `/var/log/dcnm/audit.log` | User activity and configuration changes |
| `/var/log/dcnm/ha.log` | HA replication and failover events |
| `/var/log/messages` | OS-level system log |

---

## Generating a Support Bundle

For Cisco TAC escalation, collect the DCNM support bundle:

```bash
ssh root@dcnm-dc1.corp.example.com

# Generate support bundle
/usr/local/cisco/dcm/dcnm/bin/collect-support-bundle.sh \
  --output /tmp/dcnm-support-$(date +%Y%m%d).tar.gz

# This includes:
# - All /var/log/dcnm/ logs
# - Database schema dump (no sensitive data)
# - OS resource state
# - DCNM configuration (credentials masked)
# - Installed package list
# - Network configuration

# Transfer to workstation for TAC case upload
scp root@dcnm-dc1.corp.example.com:/tmp/dcnm-support-$(date +%Y%m%d).tar.gz ./
```

---

## Application Diagnostics

### Increase Log Verbosity

```bash
# Set server log to DEBUG temporarily
sed -i 's/level="INFO"/level="DEBUG"/g' \
  /usr/local/cisco/dcm/dcnm/conf/log4j.xml
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server restart

# ... reproduce the issue, collect logs ...

# Restore to INFO
sed -i 's/level="DEBUG"/level="INFO"/g' \
  /usr/local/cisco/dcm/dcnm/conf/log4j.xml
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server restart
```

### Java Heap Diagnostics

```bash
# Find DCNM Java PID
DCNM_PID=$(ps aux | grep "[d]cnm-server" | awk '{print $2}' | head -1)

# Show Java heap usage
jstat -gcutil ${DCNM_PID} 5s 10
# If Old Gen (O) consistently > 90%: memory pressure; restart may be needed

# Generate heap dump for Cisco TAC analysis (only when directed by TAC)
jmap -dump:live,format=b,file=/tmp/dcnm-heap-$(date +%Y%m%d).hprof ${DCNM_PID}
# Note: heap dump can be several GB; coordinate with TAC before generating
```

---

## Database Diagnostics

```bash
# Connect to DCNM database
psql -U postgres sane

-- Table sizes — find unexpected large tables
SELECT relname, pg_size_pretty(pg_relation_size(relid)) AS size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_relation_size(relid) DESC
LIMIT 20;

-- Slow queries
SELECT pid, now() - query_start AS duration, state, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC
LIMIT 10;

-- Check for bloated tables (high dead tuple count)
SELECT relname, n_dead_tup, n_live_tup,
  round(n_dead_tup::numeric/greatest(n_live_tup,1)*100, 1) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;

-- If bloat is high, run VACUUM
\q

sudo -u postgres vacuumdb --all --analyze
```

### Performance DB (pmdb)

```bash
psql -U postgres pmdb

-- Check size of performance data
SELECT count(*) FROM pmdata;
SELECT pg_size_pretty(pg_database_size('pmdb'));

-- Find oldest and newest performance records
SELECT min(collecttime), max(collecttime) FROM pmdata;

\q

# If pmdb is consuming excessive disk, reduce retention:
# DCNM GUI: Administration > Settings > Data Retention
# Set Performance Data retention to 14 days (from 30)
```

---

## Network Diagnostics

```bash
# Test SSH to a managed switch
ssh -v -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
  dcnm_mgmt@<switch-ip> 'show version brief' 2>&1

# Test SNMP v3 GET
snmpget -v3 -u dcnm_poll -l authPriv \
  -a SHA -A <auth-pass> -x AES -X <priv-pass> \
  <switch-ip> sysDescr.0

# Capture SNMP trap traffic (confirm switches sending traps)
tcpdump -i eth0 -n udp port 162 -c 50 -w /tmp/dcnm-trap-capture.pcap

# Analyse capture (requires tcpdump or Wireshark on workstation)
tcpdump -r /tmp/dcnm-trap-capture.pcap -v
```

---

## Discovery Diagnostics

```bash
# Enable discovery debug for a specific switch
grep "10.20.1.5" /var/log/dcnm/discovery.log | tail -50

# Manually trigger rediscovery via REST API
curl -sk -b dcnm-cookie.txt -X POST \
  "${DCNM_HOST}/rest/san/fabric/rediscover" \
  -H "Content-Type: application/json" \
  -d '{"fabricName": "DC1-FABRIC-A", "rediscoverAll": false,
       "switchSerialNumbers": ["<serialNumber>"]}'

# Check after 2 minutes:
curl -sk -b dcnm-cookie.txt \
  "${DCNM_HOST}/rest/inventory/switches/<serialNumber>" \
  | python3 -m json.tool | grep "managementState"
```

---

## HA Diagnostics

```bash
# On either DCNM HA node
/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-status.sh

# Expected output:
# Active Node: 10.10.5.10 (THIS NODE)
# Standby Node: 10.10.5.11 (synchronized)
# VIP: 10.10.5.15 (active)
# DB Replication Lag: 0 ms

# Check replication lag
psql -U postgres -c "
SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;"
# On standby — if lag > 1 minute: investigate HA link or replication error

# Check HA log for errors
tail -f /var/log/dcnm/ha.log | grep -i "error\|fail\|disconnect"
```

---

## Performance Diagnostics

```bash
# System resource snapshot
echo "=== $(date) ===" >> /tmp/dcnm-perf.txt
free -h >> /tmp/dcnm-perf.txt
df -h >> /tmp/dcnm-perf.txt
uptime >> /tmp/dcnm-perf.txt
iostat -x 1 3 >> /tmp/dcnm-perf.txt
ps aux --sort=-%cpu | head -10 >> /tmp/dcnm-perf.txt

# Measure REST API response time
time curl -sk -b dcnm-cookie.txt \
  "${DCNM_HOST}/rest/inventory/switches" > /dev/null
# Expected: < 3 seconds for < 200 switches
# If > 10 seconds: DB query performance issue
```
