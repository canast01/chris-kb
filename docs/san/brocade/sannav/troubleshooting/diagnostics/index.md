# Brocade SANnav — Diagnostics

```bash
# Temporarily set log level (resets on restart)
sudo sed -i 's/level="INFO"/level="DEBUG"/' /opt/sannav/conf/log4j2.xml
sannav restart
# ... reproduce issue, collect logs ...
sudo sed -i 's/level="DEBUG"/level="INFO"/' /opt/sannav/conf/log4j2.xml
sannav restart
```

```text
┌──────────────────────────────────── Brocade SANnav — Diagnostics ─────────────────────────────────────┐
│                                                                                                       │
│  SANnav diagnostics: service logs, DB status, API health, performance data, MAPS review.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          SANnav Service Diagnostics          │  │             Database Diagnostics            │   │
│   │          journalctl -u sannav: logs          │  │            sannav-admin db-status           │   │
│   │        sannav-admin status: services         │  │           PostgreSQL: pg_activity           │   │
│   │        curl /api/v1/health: response         │  │        Elasticsearch: cluster health        │   │
│   │         netstat: port 443 listening          │  │           df -h: disk space check           │   │
│   │          top: CPU/RAM on SANnav VM           │  │            du -sh: data dir sizes           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  journalctl and sannav-admin are first-line diagnostics; DB status if data issues.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Switch-Level Diagnostics           │  │          Escalation Data Collection         │   │
│   │        switchshow: verify port state         │  │           Export SANnav logs: GUI           │   │
│   │          errshow: switch error log           │  │           supportsave: each switch          │   │
│   │         fabricshow: fabric topology          │  │            Audit log export: CSV            │   │
│   │          nsshow: device login state          │  │          API debug: verbose logging         │   │
│   │            MAPS: dashboard alerts            │  │         Screenshot: UI issue record         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM · vSphere monitoring · Brocade FC switch management ports · NFS backup                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  journalctl      = systemd log viewer; shows SANnav service start/stop and errors                     │
│  sannav-admin    = SANnav VM CLI; status/db-status/restart subcommands                                │
│  pg_activity     = PostgreSQL active query monitor; identifies slow queries                           │
│  Elasticsearch   = analytics DB; cluster health yellow/red = data issues                              │
│  /api/v1/health  = SANnav REST health endpoint; returns service status JSON                           │
│  df -h           = disk free check; Elasticsearch fills disk causing UI failures                      │
│  top             = Linux process monitor; check SANnav CPU/RAM consumption                            │
│  switchshow      = FOS CLI first check; verify switch not reporting errors                            │
│  errshow         = FOS error log; correlate switch events with SANnav issues                          │
│  MAPS dashboard  = SANnav aggregated view of all MAPS alerts across fabric                            │
│  supportsave     = FOS diagnostic bundle; required when escalating to Broadcom TAC                    │
│  Audit log CSV   = exported SANnav user action log; shared during security review                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Check InfluxDB is responding
curl -sk http://localhost:8086/health
# Expected: {"name":"influxdb","message":"ready for queries and writes","status":"pass",...}

# Check InfluxDB data size
du -sh /opt/sannav/data/influxdb/

# If InfluxDB is consuming excessive disk, reduce data retention:
# Navigate to Administration > System > Data Retention
# Set SAN Analytics retention to 14 days (from default 30)
```
```bash
# Check discovery log for a specific switch IP
grep "10.20.1.5" /opt/sannav/logs/discovery.log | tail -50

# Manually test HTTPS connectivity to the switch
curl -sk -o /dev/null -w "HTTP status: %{http_code}\n" \
  https://10.20.1.5/rest/loginresult
# Expected: 200 (unauthenticated) or 401 (HTTPS works, credentials needed)
# If curl returns error: connection refused or SSL error — fix at network/switch level

# Test authentication against switch API
curl -sk -X POST https://10.20.1.5/rest/login \
  -H "Content-Type: application/json" \
  -d '{"credentials":{"loginName":"sannav_svc","password":"<pass>"}}'
# Expected: { "authToken": "..." }
# If credentials error: update credentials on switch or in SANnav
```
```bash
# CPU: identify top processes
top -b -n 3 -d 1 | grep -v "^$\|^top\|^Tasks\|^%\|^KiB\|^MiB" | head -30

# Memory breakdown
free -h
# If SANnav server is consuming > 80% of RAM, check for memory leaks
ps aux --sort=-%mem | head -10

# Disk I/O
iostat -x 2 5
# High %util on the SANnav datastore disk suggests slow storage

# Network: check for dropped packets on the management interface
ip -s link show eth0
# RX/TX errors or drops indicate a network problem, not SANnav
```
```bash
# Measure REST API response time
time curl -sk -X POST https://sannav-dc1.corp.example.com/rest/login \
  -H "Content-Type: application/json" \
  -d '{"credentials":{"loginName":"svc-monitor","password":"<pass>"}}'

# Expected: < 2 seconds
# If > 5 seconds: SANnav server is under load or PostgreSQL is slow
```
```bash
# Confirm traps are arriving at UDP 162
sudo tcpdump -i eth0 -n udp port 162 -c 20

# Check event engine processing
tail -f /opt/sannav/logs/event-engine.log | grep -i "received\|processed\|drop\|error"

# If traps arrive but are not processed, check SNMP credential match
# The trap source IP must match a discovered switch's IP in SANnav
# Traps from unknown IPs are silently discarded

# Restart event engine only (without full restart)
sudo systemctl restart sannav-event-engine
```
