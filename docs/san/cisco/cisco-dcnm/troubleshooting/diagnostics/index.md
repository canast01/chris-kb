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

```text
┌────────────────────────────────────── Cisco DCNM — Diagnostics ───────────────────────────────────────┐
│                                                                                                       │
│  DCNM diagnostics: service logs, DB health, REST health endpoint, NX-OS show commands.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          DCNM Platform Diagnostics           │  │             Database Diagnostics            │   │
│   │         appmgr status: all services          │  │           appmgr db-status: check           │   │
│   │         GET /rest/health: API check          │  │            PostgreSQL: pg_isready           │   │
│   │           journalctl -u dcnm: log            │  │         Elasticsearch cluster health        │   │
│   │          netstat -tlnp 443: listen           │  │           df -h: disk usage check           │   │
│   │           top: CPU/RAM on DCNM VM            │  │         du -sh: data directory sizes        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  appmgr status and journalctl are first-line; DB and disk status if data issues.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Switch-Level Diagnostics           │  │             TAC Escalation Data             │   │
│   │          show interface fc: errors           │  │            Export DCNM logs: GUI            │   │
│   │             show flogi database              │  │            show tech-support: MDS           │   │
│   │             show zoneset active              │  │            Audit log export: CSV            │   │
│   │              show system health              │  │           API debug: verbose mode           │   │
│   │          show environment: sensors           │  │            Screenshots: UI issue            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM VM · vSphere monitoring · Cisco MDS switch management ports · syslog server                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  appmgr status   = DCNM VM CLI; shows all service health in one view                                  │
│  GET /rest/health = DCNM REST health endpoint; returns service status JSON                            │
│  journalctl      = systemd log viewer; shows DCNM service errors and restarts                         │
│  pg_isready      = PostgreSQL CLI; checks if DB accepts connections                                   │
│  Elasticsearch   = DCNM analytics DB; cluster health API shows shard status                           │
│  df -h           = disk free check; Elasticsearch fills disk causing failures                         │
│  show tech-support= NX-OS MDS full diagnostic bundle; required for Cisco TAC                          │
│  show flogi database= FC login database on MDS; verifies HBA access                                   │
│  show zoneset active= NX-OS active zone set verification                                              │
│  show system health= MDS overall health; checks modules and fabric state                              │
│  show environment= MDS sensor data: temperature, fan, PSU readings                                    │
│  Audit log CSV   = DCNM user action export; shared during security investigations                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
