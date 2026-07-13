---
tags:
  - servicenow
description: "Structured validation procedure to confirm system health and application functionality after any upgrade, patch, or configuration change. Complete within..."
---
# Post-Upgrade Validation

<div class="kb-summary">
Structured validation procedure to confirm system health and application functionality after any upgrade, patch, or configuration change. Complete within the maintenance window before declaring success.

*Applies to: ServiceNow*
</div>

## Validation Flow

```d2
direction: right

A: "Upgrade Complete" {shape: rectangle}
B: "Platform Health\nOS / hypervisor / firmware" {shape: rectangle}
C: "Service Health\nAll services started?" {shape: rectangle}
D: "Application Health\nApp responds correctly?" {shape: rectangle}
E: "Monitoring\nAlerts cleared?" {shape: rectangle}
F: "Performance\nMetrics normal?" {shape: rectangle}
G: "G" {shape: rectangle}
H: "Declare success\nRemove snapshot\nClose change ticket" {shape: rectangle}
I: "Rollback decision\nor targeted fix" {shape: rectangle}

A -> B
B -> C
C -> D
D -> E
E -> F
G -> H
G -> I
```

### VMware ESXi

```bash
# Host health
esxcli system health status get
vim-cmd hostsvc/hostsummary | grep -E "powerState|connectionState"

# Confirm expected version
vmware -v
esxcli system version get

# All VMs running (check no VMs failed to power on after host reboot)
vim-cmd vmsvc/getallvms | wc -l
esxcli vm process list | wc -l

# Storage paths healthy
esxcli storage core path list | grep -c "Active (I/O)"
esxcli storage core path list | grep "Dead\|Standby" | wc -l
```


```text title="Expected output"
System Health Status: Green
powerState = "poweredOn"
connectionState = "connected"
VMware ESXi 7.0.3 build-19193900
Product: VMware ESXi
Version: 7.0.3
Build: 19193900
Release Date: 2023-09-15
147
147
42
3
```

!!! warning "Common errors"
    **`System Health Status: Yellow`** — Check `esxcli system health status list` to identify which subsystem is degraded (typically storage or memory), then remediate the specific component before proceeding.
    **`vim-cmd: Unknown command`** — Verify the vSphere API is running with `service-control --status vmware-vpxd` and restart if needed; if persists, the ESXi host may need a reboot.
    **`grep: (standard input) is empty`** — Confirm storage devices are detected with `esxcli storage core device list`; if no devices appear, rescan HBAs using `esxcli storage core adapter rescan --adapter=vmhba0`.
## 2. Service Health

```bash
# Linux — check all expected services are running
for svc in nginx postgresql haproxy; do
  systemctl is-active $svc && echo "$svc: OK" || echo "$svc: FAILED"
done

# Generic — check listening ports
ss -tlnp | grep -E "80|443|5432|6379|9200"
netstat -tulnp

# Windows — check services
Get-Service | Where-Object {$_.StartType -eq 'Automatic' -and $_.Status -ne 'Running'}
```


```text title="Expected output"
nginx: OK
postgresql: OK
haproxy: OK
LISTEN    0      128                0.0.0.0:80            0.0.0.0:*    users:(("nginx",pid=2847,fd=6))
LISTEN    0      128                0.0.0.0:443          0.0.0.0:*    users:(("nginx",pid=2847,fd=7))
LISTEN    0      128              127.0.0.1:5432        0.0.0.0:*    users:(("postgres",pid=1923,fd=3))
LISTEN    0      128              127.0.0.1:6379        0.0.0.0:*    users:(("redis-server",pid=2156,fd=4))
LISTEN    0      128              127.0.0.1:9200        0.0.0.0:*    users:(("java",pid=3401,fd=42))

Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      2847/nginx
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      2847/nginx
tcp        0      0 127.0.0.1:5432         0.0.0.0:*               LISTEN      1923/postgres
tcp        0      0 127.0.0.1:6379         0.0.0.0:*               LISTEN      2156/redis-server
tcp        0      0 127.0.0.1:9200         0.0.0.0:*               LISTEN      3401/java

Status   Name               StartType
Stopped  WinRM              Automatic
Stopped  WinDefend          Automatic
```

!!! warning "Common errors"
    **`nginx: FAILED`** — Run `systemctl start nginx && systemctl enable nginx` to start the service and enable it on boot.
    **`ss: command not found`** — Install iproute2 with `apt-get install iproute2` or use `netstat -tulnp` as a fallback.
    **`Get-Service : The term 'Get-Service' is not recognized`** — Run the PowerShell command on Windows only; use `wmic service list brief` on Windows systems without PowerShell.
| Service | Expected Port | Check Command | Status |
|---|---|---|---|
| Web / App | 443, 80 | `curl -sk https://localhost/health` | ☐ |
| Database | 5432 / 1433 | `pg_isready` / `sqlcmd -Q "SELECT 1"` | ☐ |
| Monitoring agent | 9100 / 12489 | `systemctl is-active node_exporter` | ☐ |
| Backup agent | varies | Check Veeam/Commvault agent status | ☐ |

## 3. Application Health

```bash
# HTTP health endpoint
curl -sk https://<app-url>/health | python3 -m json.tool

# Check response time (< 2s expected)
curl -sk -o /dev/null -w "%{time_total}" https://<app-url>/

# Database connectivity from app
psql -h <db-host> -U appuser -d appdb -c "SELECT version();"

# Check application logs for errors post-upgrade
journalctl -u myapp --since "1 hour ago" | grep -iE "error|exception|fatal"
tail -200 /var/log/myapp/app.log | grep -iE "error|exception"
```


```text title="Expected output"
{
  "status": "healthy",
  "version": "2.4.1",
  "database": "connected",
  "uptime_seconds": 3847,
  "timestamp": "2024-01-15T14:32:18Z"
}
0.847

PostgreSQL 12.14 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 9.4.0, 64-bit

Jan 15 14:28:42 app-prod-01 myapp[2847]: INFO: Database migration completed successfully
Jan 15 14:29:15 app-prod-01 myapp[2847]: INFO: Cache warmed in 1.2s
Jan 15 14:31:05 app-prod-01 myapp[2847]: WARNING: Slow query detected (2.3s) on endpoint /api/reports
(no matching lines — no errors in last hour)
(no matching lines — no errors in app.log)
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command or use `--cacert /path/to/ca.crt` with a valid certificate.
    **`psql: error: could not translate host name "<db-host>" to address: Name or service not known`** — Replace `<db-host>` with the actual database hostname (e.g., `db-prod-01.internal`) and verify network connectivity with `ping`.
    **`Unit myapp.service not found`** — Verify the systemd service name with `systemctl list-units --type=service | grep myapp` and update the `journalctl -u` parameter accordingly.
## 4. Monitoring Validation

```bash
# Confirm no new alerts fired post-upgrade
# Check Prometheus alerts
curl -s http://prometheus:9090/api/v1/alerts | \
  python3 -c "import sys,json; [print(a['labels']['alertname']) for a in json.load(sys.stdin)['data']['alerts'] if a['state']=='firing']"

# Confirm metrics are flowing (not stale)
curl -s http://prometheus:9090/api/v1/query?query=up | \
  python3 -m json.tool | grep '"value"'

# Check node_exporter last scrape
curl -s http://<host>:9100/metrics | grep "node_time_seconds"
```


```text title="Expected output"
AlertmanagerDown
HighMemoryUsage
PrometheusRemoteWriteErrors
"value": [
  1702541823.456,
  "1"
]
"value": [
  1702541824.123,
  "1"
]
"value": [
  1702541825.789,
  "1"
]
# HELP node_time_seconds Seconds since boot.
# TYPE node_time_seconds gauge
node_time_seconds 2847392.45
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to prometheus:9090: Connection refused`** — Verify Prometheus service is running with `systemctl status prometheus` and check firewall rules allow port 9090.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Confirm the Prometheus endpoint is responding with valid JSON by testing `curl -s http://prometheus:9090/api/v1/alerts` directly.
    **`curl: (7) Failed to connect to <host>:9100: No route to host`** — Replace `<host>` with the actual hostname/IP and verify node_exporter is listening on port 9100 with `netstat -tlnp | grep 9100`.
## 5. Performance Baseline Comparison

```bash
# CPU — compare to pre-upgrade baseline
mpstat 1 10 | tail -1

# Memory
free -h

# Disk I/O
iostat -x 1 5 | tail -10

# Network
sar -n DEV 1 5 | grep -v lo

# Application response time (compare to pre-upgrade SLA)
for i in {1..10}; do
  curl -sk -o /dev/null -w "%{time_total}\n" https://<app-url>/
done | awk '{sum+=$1; count++} END {printf "Avg: %.3fs\n", sum/count}'
```


```text title="Expected output"
Linux 4.15.0-213-generic (svc-app-prod-01) 	01/15/2025 	_x86_64_	(16 CPU)

Average:	12.45	 5.23	 2.18	 0.08	80.06
MemTotal:        65894456 kB
MemFree:         42156892 kB
MemAvailable:    51203748 kB
Buffers:          1245632 kB
Cached:           8956124 kB
SwapTotal:       16777216 kB
SwapFree:        16777216 kB
Linux 4.15.0-213-generic (svc-app-prod-01) 	01/15/2025 	_x86_64_	(16 CPU)

Device            r/s     w/s     rMB/s   wMB/s   rrqm/s  wrqm/s  %rrqm  %wrqm r_await w_await svctm  %util
sda               8.20   12.45    0.34    0.89    0.12    2.34    1.44  15.82   4.32    8.76   2.18   4.42
sdb               2.10    3.80    0.12    0.45    0.00    0.98    0.00  20.51   3.21    6.89   1.95   1.18
dm-0              9.45   15.23    0.42    1.12    0.00    0.00    0.00   0.00   3.98    7.54   1.87   4.63
IFACE     RXPCK/s TXPCK/s RXKB/s  TXKB/s RXCMP/s TXCMP/s RXMCST/s
eth0       1245.3  1089.2   342.1   298.5    0.0     0.0      0.0
eth1        89.2    76.4    12.3    11.8    0.0     0.0      0.0
Avg: 0.487s
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command or use `--cacert /path/to/ca-bundle.crt` with your organization's CA certificate.
    **`command not found: mpstat`** — Install sysstat package with `sudo apt-get install sysstat` (Debian/Ubuntu) or `sudo yum install sysstat` (RHEL/CentOS).
    **`Name or service not known`** — Verify the `<app-url>` placeholder is replaced with the actual application hostname and that DNS resolution is working with `nslookup <app-url>`.
## 6. Replication and Data Integrity

```bash
# VMware vSphere Replication / SRM
Get-SpbmReplicationGroup | Select-Object Name, State, RPO, LatestRpo

# NetApp SnapMirror
snapmirror show -destination-path <svm:vol> -fields state,lag-time

# Dell RecoverPoint
# Check via UNISPHERE: verify consistency groups healthy, lag within SLA

# Database replication
# PostgreSQL streaming replication
psql -c "SELECT client_addr, state, sent_lsn, replay_lsn, write_lag, flush_lag FROM pg_stat_replication;"
```


```text title="Expected output"
Name                          State      RPO        LatestRpo
----                          -----      ---        ---------
prod-vm-cluster-01            Healthy    01:00:00   00:45:32
prod-vm-cluster-02            Healthy    01:00:00   00:58:12
dr-sync-group-03              Healthy    00:30:00   00:28:47

                                    Source Destination State    Lag-time
                                    ------ ----------- -----    --------
prod_svm:prod_vol_01 prod_svm:prod_vol_01_dr SnapMirrored 2m 15s
prod_svm:prod_vol_02 prod_svm:prod_vol_02_dr SnapMirrored 1m 42s
prod_svm:prod_vol_03 prod_svm:prod_vol_03_dr SnapMirrored 3m 8s

 client_addr  |   state   | sent_lsn  | replay_lsn | write_lag | flush_lag
--------------+-----------+-----------+------------+-----------+-----------
 10.45.12.88  | streaming | 0/4A2F5B8 | 0/4A2F520  | 125 ms    | 142 ms
 10.45.12.89  | streaming | 0/4A2F5B8 | 0/4A2F4F0  | 287 ms    | 301 ms
(2 rows)
```

!!! warning "Common errors"
    **`Get-SpbmReplicationGroup : The term 'Get-SpbmReplicationGroup' is not recognized`** — Load the VMware PowerCLI module with `Import-Module VMware.PowerCLI` before running the cmdlet.
    **`Error: command not found: snapmirror`** — Ensure you are connected to the NetApp cluster management interface via SSH or execute the command from the NetApp cluster console directly.
    **`psql: could not translate host name "localhost" to address`** — Specify the correct PostgreSQL host with `-h <hostname>` and verify the database is running and accessible on that host.
## 7. Post-Upgrade Cleanup

```bash
# Remove pre-upgrade snapshot (after 24h stability confirmation)
Get-VM -Name "HOSTNAME" | Get-Snapshot -Name "pre-upgrade-*" | Remove-Snapshot -Confirm:$false

# Remove temp files
rm -f /tmp/upgrade-*.log /tmp/pre-upgrade-backup-*.tar.gz

# Update CMDB / inventory
# → Update firmware/OS version in asset management system

# Close change ticket
# → Set status to "Implemented" with validation notes
```


```text title="Expected output"
Snapshot removal initiated...
Snapshot "pre-upgrade-20240115-143022" removed successfully
Snapshot "pre-upgrade-20240115-120015" removed successfully
/tmp/upgrade-hotfix-20240115.log removed
/tmp/upgrade-hotfix-20240115-secondary.log removed
/tmp/pre-upgrade-backup-HOSTNAME-20240115.tar.gz removed
/tmp/pre-upgrade-backup-HOSTNAME-20240115-incremental.tar.gz removed

CMDB update: Asset ID AST-0847293 — OS version updated to 2024.1.5
CMDB update: Firmware version updated to 8.4.2-build.19847
Change ticket CHG-0156847 status: Implemented
Validation notes appended: Post-upgrade stability confirmed. All snapshots removed. 24h monitoring complete.
```

!!! warning "Common errors"
    **`Get-VM : The term 'Get-VM' is not recognized as the name of a cmdlet, function, script file, or operable program.`** — Ensure PowerShell is running on a Windows system with Hyper-V or VMware PowerCLI module installed, or use the appropriate hypervisor CLI for your platform.
    **`rm: cannot remove '/tmp/pre-upgrade-backup-*.tar.gz': No such file or directory`** — Verify the backup files exist with `ls /tmp/pre-upgrade-backup-*.tar.gz` before removal, or adjust the glob pattern to match actual filenames.
    **`Error: CMDB API authentication failed (401 Unauthorized)`** — Confirm your ServiceNow API credentials and token are valid, and that your user account has write permissions to the CMDB table.
## Validation Sign-Off

| Check | Result | Notes |
|---|---|---|
| Platform health (OS/HW) | ☐ Pass / ☐ Fail | |
| All services running | ☐ Pass / ☐ Fail | |
| Application responding | ☐ Pass / ☐ Fail | |
| No new monitoring alerts | ☐ Pass / ☐ Fail | |
| Performance within baseline | ☐ Pass / ☐ Fail | |
| Replication healthy | ☐ Pass / ☐ Fail | |
| Snapshot removed | ☐ Done / ☐ Pending | Remove within 48h |
| CMDB updated | ☐ Done | |
| Change ticket closed | ☐ Done | |
| **Overall outcome** | ☐ **Success** / ☐ **Rolled back** | |
