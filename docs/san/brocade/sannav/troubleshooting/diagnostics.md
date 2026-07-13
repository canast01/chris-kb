---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
description: "SANnav diagnostic commands: check service health with sannav-admin and journalctl, test the REST API health endpoint, check PostgreSQL and InfluxDB..."
---
# Brocade SANnav — Diagnostics

<div class="kb-summary">
SANnav diagnostic commands: check service health with sannav-admin and journalctl, test the REST API health endpoint, check PostgreSQL and InfluxDB database status, diagnose switch discovery failures, verify SNMP trap reception, and export the SANnav support bundle for Broadcom TAC cases.

*Applies to: Brocade SANnav 2.x*
</div>
![Brocade SANnav — Diagnostics](../../../../assets/san-brocade-sannav-troubleshooting-diagnostics.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "sannav-admin status\ncurl /api/v1/health" {shape: rectangle}
D: "grep switch-ip /opt/sannav/logs/discovery.log\ncurl -sk switch-ip/rest/loginresult" {shape: rectangle}
E: "curl localhost:8086/health\nCheck InfluxDB disk usage" {shape: rectangle}
F: "tcpdump -i eth0 udp port 162\nCheck SNMP trap reception" {shape: rectangle}
G: "sannav-admin db-status\nCheck PostgreSQL health" {shape: rectangle}
H: "H" {shape: rectangle}
I: "journalctl -u sannav --since 1h\nFind failing service" {shape: rectangle}
J: "top + free -h\nCheck CPU and RAM" {shape: rectangle}
K: "Test HTTPS to switch\ncurl -sk switch-ip/rest/loginresult" {shape: rectangle}
L: "L" {shape: rectangle}
M: "Check switch credentials\nin SANnav Discover menu" {shape: rectangle}
N: "Check network and firewall\nto switch management IP on HTTPS" {shape: rectangle}
O: "df -h /opt/sannav/data\ndu -sh influxdb/ vs total" {shape: rectangle}
P: "Reduce retention policy\nAdmin → System → Data Retention" {shape: rectangle}
Q: "Q" {shape: rectangle}
R: "Check switch SNMP config\nsnmpconfig --show snmpv3" {shape: rectangle}
S: "Check trap source IP\nmust match discovered switch IP" {shape: rectangle}
T: "Collect support bundle\nSANnav GUI → Admin → Export Logs" {shape: rectangle}
A: "SANnav Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
H -> I
H -> J
D -> K
L -> M
L -> N
E -> O
O -> P
Q -> R
Q -> S
G -> I
I -> T
J -> T
M -> T
N -> T
P -> T
R -> T
S -> T
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_sannav_service_health: "Step 1 — Check SANnav service health" {shape: rectangle}
step_2_check_database_health: "Step 2 — Check database health" {shape: rectangle}
step_3_diagnose_switch_discovery_fai: "Step 3 — Diagnose switch discovery failures" {shape: rectangle}
step_4_check_snmp_trap_reception: "Step 4 — Check SNMP trap reception" {shape: rectangle}
step_5_check_sannav_host_system_perf: "Step 5 — Check SANnav host system performance" {shape: rectangle}
step_6_collect_support_bundle_for_br: "Step 6 — Collect support bundle for Broadcom TAC" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_sannav_service_health: investigate
symptom -> step_2_check_database_health: investigate
symptom -> step_3_diagnose_switch_discovery_fai: investigate
symptom -> step_4_check_snmp_trap_reception: investigate
symptom -> step_5_check_sannav_host_system_perf: investigate
symptom -> step_6_collect_support_bundle_for_br: investigate
step_1_check_sannav_service_health -> resolution
step_2_check_database_health -> resolution
step_3_diagnose_switch_discovery_fai -> resolution
step_4_check_snmp_trap_reception -> resolution
step_5_check_sannav_host_system_perf -> resolution
step_6_collect_support_bundle_for_br -> resolution
```

## Before you begin

- **Access:** SSH to the SANnav VM as `admin`; SANnav web UI admin credentials; Brocade switch CLI access via SSH
- **Gather first:** the symptom (switch missing, alert missing, UI error, performance data gap), the affected switch IP or fabric name, and whether any changes were made recently (firmware update, IP change, credential rotation)
- **Scope:** confirm whether the issue affects one switch, one fabric, or all of SANnav

---

## Step 1 — Check SANnav service health

```bash
# SSH to the SANnav VM
ssh admin@<sannav-ip>

# Check all SANnav micro-services
sannav-admin status
# Expected: all services showing "running" or "healthy"
# Problem: any service in "stopped", "error", or "unhealthy"

# REST API health check (run from SANnav VM or any host that can reach it)
curl -sk https://<sannav-ip>/api/v1/health | python3 -m json.tool
# Expected: HTTP 200 with each service status = "UP"

# SANnav systemd journal (service start/stop and crash events)
journalctl -u sannav --since "1 hour ago" | tail -100

# System resources
top -b -n 1 | head -20
free -h
df -h /opt/sannav /var
# Alert if RAM < 20% free or disk > 80% used on /opt/sannav
```


```text title="Expected output"
admin@sannav-01:~$ sannav-admin status
sannav-api                 RUNNING
sannav-collector           RUNNING
sannav-db                  RUNNING
sannav-ui                  RUNNING
sannav-scheduler           RUNNING
sannav-alerting            RUNNING

admin@sannav-01:~$ curl -sk https://192.168.1.50/api/v1/health | python3 -m json.tool
{
  "status": "UP",
  "services": {
    "api": "UP",
    "database": "UP",
    "collector": "UP",
    "scheduler": "UP"
  },
  "timestamp": "2024-01-15T14:32:18Z"
}

admin@sannav-01:~$ journalctl -u sannav --since "1 hour ago" | tail -100
Jan 15 14:15:22 sannav-01 sannav[2847]: INFO: Collector sync completed for fabric-01
Jan 15 14:20:45 sannav-01 sannav[2847]: INFO: Health check passed for all switches
Jan 15 14:31:10 sannav-01 sannav[2847]: INFO: Database backup completed

admin@sannav-01:~$ top -b -n 1 | head -20
top - 14:35:22 up 45 days, 3:22, 1 user, load average: 1.24, 1.18, 1.15
Tasks: 187 total, 2 running, 185 sleeping, 0 stopped, 0 zombie
%Cpu(s): 18.3 us, 4.2 sy, 0.0 ni, 77.1 id, 0.2 wa, 0.1 hi, 0.1 si, 0.0 st
MiB Mem : 32768.0 total, 26144.2 free, 5120.8 used, 1503.0 buff/cache
MiB Swap: 8192.0 total, 8192.0 free, 0.0 used. 25600.0 avail Mem

admin@sannav-01:~$ free -h
              total        used        free      shared  buff/cache   available
Mem:           31Gi       5.0Gi        25Gi       512Mi       1.5Gi        25Gi
Swap:          8.0Gi          0B       8.0Gi

admin@sannav-01:~$ df -h /opt/sannav /var
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       500G  285G  215G  57% /opt/sannav
/dev/sda2       100G   42G   58G  42% /var
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to curl to skip SSL verification, or import the SANnav CA certificate into your system's trust store.
    **`sannav-admin: command not found`** — Ensure you are logged in as the `admin` user and `/opt/sannav/
---

## Step 2 — Check database health

```bash
# PostgreSQL database status (stores SANnav config, topology, events)
sannav-admin db-status
# Expected: "PostgreSQL is running and healthy"

# InfluxDB health (stores SAN performance metrics: IOPS, throughput, latency)
curl -sk http://localhost:8086/health
# Expected: {"name":"influxdb","status":"pass","message":"ready for queries and writes",...}

# Check InfluxDB disk usage (largest common cause of performance data loss)
du -sh /opt/sannav/data/influxdb/
df -h /opt/sannav/data
# If InfluxDB is > 80% of the disk: reduce retention policy

# Reduce InfluxDB retention to free space
# Navigate to: SANnav UI → Administration → System → Data Retention
# Set "SAN Analytics" retention to 14 days (default: 30)
# This runs asynchronously; reclaimed space appears after compaction (may take hours)
```


```text title="Expected output"
PostgreSQL is running and healthy
{"name":"influxdb","status":"pass","message":"ready for queries and writes","checks":[],"output":""}
1.2G	/opt/sannav/data/influxdb/
Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1      100G   87G   13G  87% /opt/sannav/data
tmpfs          7.8G     0  7.8G   0% /dev/shm
/dev/sda2      500G  412G   88G  83% /var
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to localhost port 8086: Connection refused`** — Verify InfluxDB is running with `systemctl status influxdb` and check firewall rules allowing localhost:8086.
    **`du: cannot access '/opt/sannav/data/influxdb/': No such file or directory`** — Confirm InfluxDB data directory path matches your installation; check actual path with `find /opt -name influxdb -type d 2>/dev/null`.
---

## Step 3 — Diagnose switch discovery failures

```bash
# Check discovery log for the affected switch IP
grep "<switch-ip>" /opt/sannav/logs/discovery.log | tail -50
# Look for: connection refused, authentication failed, SSL error

# Test HTTPS connectivity to the switch management port
curl -sk -o /dev/null -w "HTTP status: %{http_code}\n" https://<switch-ip>/rest/loginresult
# Expected: 200 (unauthenticated) or 401 (HTTPS works; credentials needed)
# If curl fails with connection refused or SSL error: fix at network level

# Test switch REST API authentication
curl -sk -X POST https://<switch-ip>/rest/login \
  -H "Content-Type: application/json" \
  -d '{"credentials":{"loginName":"<sannav-svc-user>","password":"<password>"}}'
# Expected: { "authToken": "..." }
# If you get 401: the password for the service account on the switch needs resetting
# If you get a connection error: firewall or HTTPS on the switch is disabled

# Check the switch has FOS HTTPS management enabled
# On the switch via SSH:
#   switchshow (verify switch is online)
#   httpcfg --show (verify HTTPS REST API is enabled)
```


```text title="Expected output"
2024-01-15 10:23:47 [INFO] Discovery initiated for switch 10.50.12.45
2024-01-15 10:23:52 [DEBUG] Attempting HTTPS connection to 10.50.12.45:443
2024-01-15 10:24:01 [ERROR] Connection refused on attempt 1, retrying...
2024-01-15 10:24:15 [WARN] SSL certificate validation skipped (self-signed detected)
2024-01-15 10:24:22 [INFO] Discovery completed with 1 warning

HTTP status: 401

{
  "errors": [
    {
      "errorCode": 401,
      "errorMessage": "Authentication required"
    }
  ]
}

SSH connection to 10.50.12.45 port 22 successful
FOS Version: v9.1.0
HTTPS REST API: Enabled
Management Port: 443
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to 10.50.12.45 port 443: Connection refused`** — Verify the switch management IP is correct and HTTPS is enabled on the switch via `httpcfg --show`.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Use the `-k` flag to skip certificate verification (already included in the example), or import the switch's certificate into your CA bundle.
    **`{"errorCode": 401, "errorMessage": "Authentication required"}`** — Reset the SANnav service account password on the switch and update the credentials in SANnav's configuration file.
---

## Step 4 — Check SNMP trap reception

SANnav relies on SNMP traps from switches for real-time alerts. If traps are not arriving, alerts appear with a delay or not at all.

```bash
# Verify UDP 162 is listening on the SANnav VM
ss -tulnp | grep 162
# Expected: udp UNCONN with port 162 listening

# Capture SNMP traps arriving at the SANnav VM (run for 60 seconds then Ctrl-C)
sudo tcpdump -i eth0 -n udp port 162 -c 20
# Expected: packets with source IP = switch management IP arriving at :162
# No packets: switch is not sending traps, or firewall is blocking UDP 162

# Check SNMP configuration on the switch (run on the switch via SSH)
snmpconfig --show snmpv3
# Verify: SANnav IP is listed as a trap recipient

# If traps arrive but SANnav does not show alerts:
# The trap source IP must match the discovered switch IP in SANnav
# Traps from an IP not in the SANnav inventory are silently discarded
# Check: SANnav UI → Discover → Inventory → switch → IP address shown

# Restart SANnav event engine only (without full restart, if traps are arriving but not processed)
sudo systemctl restart sannav-event-engine
```


```text title="Expected output"
udp    UNCONN 0      0      0.0.0.0:162    0.0.0.0:*    users:(("snmptrapd",pid=2847,fd=9))
udp6   UNCONN 0      0      [::]:162       [::]:*       users:(("snmptrapd",pid=2847,fd=10))

tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
14:32:15.487291 IP 192.168.1.45.54821 > 10.50.20.18.162: SNMP, length 156
14:32:18.521847 IP 192.168.1.45.54822 > 10.50.20.18.162: SNMP, length 156
14:32:21.634012 IP 192.168.1.45.54823 > 10.50.20.18.162: SNMP, length 156
14:32:24.712556 IP 192.168.1.45.54824 > 10.50.20.18.162: SNMP, length 156
14:32:27.889234 IP 192.168.1.45.54825 > 10.50.20.18.162: SNMP, length 156
20 packets captured
20 packets received by filter
0 packets dropped by kernel

snmpv3 trap recipients:
  192.168.1.200 (SANnav-Primary)
  192.168.1.201 (SANnav-Secondary)

sannav-event-engine.service restarted successfully.
```

!!! warning "Common errors"
    **`ss: command not found`** — Install net-tools or use `netstat -tulnp | grep 162` instead on older systems.
    **`tcpdump: Permission denied`** — Run the tcpdump command with `sudo` or ensure the user is in the pcap group.
    **`Unit sannav-event-engine.service not found`** — Verify the service name with `sudo systemctl list-units | grep sannav` and use the correct service name.
---

## Step 5 — Check SANnav host system performance

```bash
# CPU — identify which SANnav process is consuming the most CPU
ps aux --sort=-%cpu | head -15

# Memory — check for near-OOM conditions
free -h
# If available memory < 2 GB: SANnav processes may be swapping; consider increasing VM RAM

# Disk I/O — check if slow storage is causing SANnav latency
iostat -x 2 5
# High %util on the SANnav datastore disk = storage bottleneck

# Network — check for dropped packets on the management NIC
ip -s link show eth0
# RX errors or drops = network issue, not SANnav

# REST API response time (should be < 2 seconds for login)
time curl -sk -X POST https://<sannav-ip>/rest/login \
  -H "Content-Type: application/json" \
  -d '{"credentials":{"loginName":"<admin>","password":"<pass>"}}'
# > 5 seconds: SANnav server under load or PostgreSQL is slow
```


```text title="Expected output"
USER       PID %CPU %MEM    VSZ   RSS TTY STAT START   TIME COMMAND
root      2847 18.3  12.5 2847392 412016 ?  Sl   09:22  45:23 /usr/java/default/bin/java -server -Xmx2048m -Xms1024m -Dcom.brocade.sannav.home=/opt/brocade/sannav
postgres  1923 8.7   9.2 1256480 301504 ?  Sl   09:15  22:11 /usr/pgsql-12/bin/postgres -D /var/lib/pgsql/12/data
root      2891 3.2   4.1  856320 134208 ?  Sl   09:23   8:45 /opt/brocade/sannav/bin/collector
root      1847 1.1   2.3  512000  75392 ?  Ss   09:10   2:33 /usr/sbin/sshd -D
root      2945 0.8   1.9  384000  62144 ?  Sl   09:25   1:52 /opt/brocade/sannav/bin/alertmanager

              total        used        free      shared  buff/cache   available
Mem:           15Gi       8.2Gi       2.1Gi       512Mi       4.7Gi       6.1Gi
Swap:          4.0Gi       1.2Gi       2.8Gi

Linux 5.10.0-8-amd64 (sannav-prod-01) 	01/15/2025 	_x86_64_	(8 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
          42.15    0.00   18.33    8.42    0.00   31.10

Device            r/s     w/s     rMB/s     wMB/s   %util rrqm/s wrqm/s r_await w_await svctm
sda              145.2   287.5    18.4      22.1   68.3   12.1   45.3   4.2     6.8    1.9
sdb               8.3    12.1     0.6       0.9   12.1    1.2    3.4   3.1     4.2    0.8

RX: bytes  packets  errors  dropped missed  mcast
    8847392 12453    0       0       0       0
TX: bytes  packets  errors  dropped carrier collsns
    5234891 9821     0       0       0       0

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   284  100   284    0     284   1847    1847 --:--:-- --:--:-- --:--:-- --:--:--
{"sessionID":"a7f2c8e9-1b4d-4a2f-9e3c-5d8f2a1b9c4e","userName":"admin"}

real
```
---

## Step 6 — Collect support bundle for Broadcom TAC

```bash
# Via SANnav GUI (recommended — includes all service logs and DB state)
# Navigate to: Administration → Support → Export Support Bundle
# Wait for download (5–15 minutes)

# Via CLI (if GUI is unavailable)
sannav-admin support-bundle --output /tmp/sannav-support-$(date +%F).tar.gz
# Then download from the VM:
scp admin@<sannav-ip>:/tmp/sannav-support-*.tar.gz ./

# Also collect supportsave from each affected Brocade switch (run on each switch via SSH)
supportsave
# Saves to the switch; download via FTP/SCP from the switch
# Required for TAC cases involving switch-SANnav interoperability

# Include in the Broadcom/SANnav TAC case:
# - SANnav support bundle
# - switch supportsave files for each affected fabric
# - Timeline of the issue and any recent changes
# - SANnav version: GUI → Administration → System → Version
```


```text title="Expected output"
admin@sannav-prod:~$ sannav-admin support-bundle --output /tmp/sannav-support-$(date +%F).tar.gz
Generating support bundle...
Collecting system logs (syslog, audit, application)...
Collecting database state and configuration...
Collecting service status (nginx, postgresql, elasticsearch)...
Collecting network diagnostics...
Bundle created: /tmp/sannav-support-2024-01-15.tar.gz (487 MB)
Completed in 8 minutes 42 seconds

admin@workstation:~$ scp admin@192.168.1.45:/tmp/sannav-support-*.tar.gz ./
sannav-support-2024-01-15.tar.gz                    100%  487MB   12.3MB/s   00:40

switch-fab1:admin> supportsave
Saving system information...
Saving configuration and logs...
Saving fabric state and performance data...
Support save file: /var/log/supportsave_20240115_143022.tar.gz (156 MB)
Completed successfully
```

!!! warning "Common errors"
    **`sannav-admin: command not found`** — Ensure you are logged in as the admin user on the SANnav VM and the sannav-admin CLI tool is in your PATH (typically pre-installed).
    **`Permission denied (publickey)`** — Verify SSH key is configured for the admin user on the SANnav VM, or use password authentication with `scp -o PubkeyAuthentication=no`.
    **`supportsave: command not found`** — SSH directly to the Brocade switch (not the SANnav VM) and run supportsave with admin or root privileges.
---

## Log locations

| Component | Path | What to look for |
|---|---|---|
| SANnav service | `journalctl -u sannav --since "1h ago"` | Service start/stop, fatal errors |
| Discovery | `/opt/sannav/logs/discovery.log` | Switch discovery connection and auth errors |
| Event engine | `/opt/sannav/logs/event-engine.log` | Trap processing, event rule matching |
| Application | `/opt/sannav/logs/application.log` | General application errors |
| InfluxDB | `curl localhost:8086/health` | Metric DB health and query status |
| PostgreSQL | `sannav-admin db-status` | Database health and replication |

---

## See also

- [SANnav — Common Issues](../common-issues/)
- [SANnav — Escalation](../escalation/)
- [SANnav — Health Checks](../../operations/health-checks/)

## Verify resolution

- `sannav-admin status` shows all services running
- `curl -sk https://<sannav-ip>/api/v1/health` returns `"status": "UP"` for all services
- The previously missing switch appears in SANnav UI → Inventory with a green health icon
- SNMP trap test: trigger a manual MAPS alert on the switch and confirm it appears in SANnav Alerts within 60 seconds
- `curl localhost:8086/health` shows InfluxDB `"status": "pass"`; performance charts show current data
