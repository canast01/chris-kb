---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# CloudIQ — Diagnostics

<div class="kb-summary">
CloudIQ diagnostic commands: check SCG service health, test outbound connectivity, verify per-device polling, collect log bundles, and diagnose proxy-related connectivity failures.

*Applies to: Dell CloudIQ / Secure Connect Gateway (SCG)*
</div>
![CloudIQ — Diagnostics](../../../../assets/storage-dell-cloudiq-troubleshooting-diagnostics.svg)

```d2
direction: right

A: "CloudIQ Issue" {shape: rectangle}
B: "scg status\nSCG service running?" {shape: rectangle}
C: "C" {shape: rectangle}
D: "systemctl status dsagw\nCheck service errors" {shape: rectangle}
E: "scg connectivity --test\nOutbound HTTPS reachable?" {shape: rectangle}
F: "F" {shape: rectangle}
G: "Check proxy settings\nSCG UI → Settings → Proxy" {shape: rectangle}
H: "scg device list\nIdentify unreporting device" {shape: rectangle}
I: "scg device test --id\nTest specific device" {shape: rectangle}
J: "J" {shape: rectangle}
K: "Update device credentials\nSCG UI → Devices → Edit" {shape: rectangle}
L: "curl https://array-mgmt-ip\nVerify array reachable from SCG" {shape: rectangle}
M: "scg log collect\nCollect diagnostic bundle" {shape: rectangle}
N: "Open Dell SR\nsupport.dell.com" {shape: rectangle}

A -> B
C -> D
C -> E
F -> G
F -> H
H -> I
J -> K
J -> L
D -> M
G -> M
K -> M
L -> M
M -> N
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_scg_service_health: "Step 1 — Check SCG service health" {shape: rectangle}
step_2_test_outbound_connectivity_to: "Step 2 — Test outbound connectivity to CloudIQ" {shape: rectangle}
step_3_list_and_test_devices: "Step 3 — List and test devices" {shape: rectangle}
step_4_read_scg_log_files: "Step 4 — Read SCG log files" {shape: rectangle}
step_5_collect_support_bundle: "Step 5 — Collect support bundle" {shape: rectangle}
log_locations: "Log locations" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_scg_service_health: investigate
symptom -> step_2_test_outbound_connectivity_to: investigate
symptom -> step_3_list_and_test_devices: investigate
symptom -> step_4_read_scg_log_files: investigate
symptom -> step_5_collect_support_bundle: investigate
symptom -> log_locations: investigate
step_1_check_scg_service_health -> resolution
step_2_test_outbound_connectivity_to -> resolution
step_3_list_and_test_devices -> resolution
step_4_read_scg_log_files -> resolution
step_5_collect_support_bundle -> resolution
log_locations -> resolution
```

## Before you begin

- **Access:** SSH to the SCG appliance as `admin`; SCG web UI (`https://<scg-ip>`); CloudIQ portal (`cloudiq.dell.com`) with admin role
- **Gather first:** which specific arrays are not reporting in CloudIQ, how long the gap has been, and the SCG version from SCG UI → Settings → About
- **Scope:** confirm whether the issue affects all arrays (SCG or outbound problem) or a specific array (device credential or network problem)
- **Proxy note:** if the SCG is behind a proxy, all outbound connectivity tests must route through it — verify the proxy allows HTTPS to `cloudiq.dell.com` and `esrs3.emc.com` on port 443

---

## Step 1 — Check SCG service health

```bash
# SSH to the SCG appliance
ssh admin@<scg-ip>

# Check SCG service status
scg status
# Expected output (healthy):
#   SCG Service: Running
#   Version: <version>
#   Connected to CloudIQ: Yes
#   Last sync: <timestamp within last 15 minutes>

# Check the underlying dsagw gateway service
systemctl status dsagw
# Expected: active (running); no recent restart loops
# If status shows failed: check dsagw log with journalctl -u dsagw -n 100

# Check disk space on SCG appliance
df -h /
# SCG log accumulation can fill disk; alert if < 20% free
```


```text title="Expected output"
admin@192.168.1.45's password: 
Last login: Wed Jan 15 14:22:33 2025 from 10.0.0.88

SCG Service: Running
Version: 2.4.1-build.8847
Connected to CloudIQ: Yes
Last sync: 2025-01-15 14:18:47 UTC

● dsagw.service - Dell Storage Gateway
     Loaded: loaded (/etc/systemd/system/dsagw.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2025-01-15 13:45:22 UTC; 33min ago
   Main PID: 4521 (dsagw)
      Tasks: 24 (limit: 4096)
     Memory: 287.3M
        CPU: 12m 34.234s
     CGroup: /system.slice/dsagw.service
             └─4521 /opt/dell/dsagw/bin/dsagw -c /etc/dsagw/dsagw.conf

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1       50G   38G   9.2G  82% /
```

!!! warning "Common errors"
    **`ssh: connect to host 192.168.1.45 port 22: Connection refused`** — Verify the SCG appliance is powered on and the IP address is correct; check network connectivity with `ping <scg-ip>`.
    **`● dsagw.service - Dell Storage Gateway ... Active: failed (Result: exit-code)`** — Check the dsagw service logs with `journalctl -u dsagw -n 100` to identify the root cause, then restart with `systemctl restart dsagw`.
    **`Filesystem ... Use% Mounted on ... 95% /`** — Archive or delete old SCG logs in `/var/log/dsagw/` using `find /var/log/dsagw/ -mtime +30 -delete` to free disk space before the appliance becomes unresponsive.
**If SCG service is not running:**
1. `systemctl start dsagw` to restart; wait 30 seconds and re-check `scg status`
2. If service fails to start: check `/var/log/dsagw/` for startup errors
3. If disk is full: `du -sh /var/log/dsagw/*` to identify large log files

---

## Step 2 — Test outbound connectivity to CloudIQ

```bash
# Test HTTPS connectivity to all required CloudIQ endpoints
scg connectivity --test
# Expected: all endpoints show "Reachable"
# If any show "Unreachable" or "Timeout" — the proxy or firewall is blocking traffic

# Manual connectivity test (if scg tool is unavailable)
curl -v --max-time 30 https://cloudiq.dell.com
# Expected: TLS handshake succeeds; HTTP 200 or redirect

# Test legacy ESRS endpoint (required for some SCG versions)
curl -v --max-time 30 https://esrs3.emc.com
# Expected: TLS handshake succeeds; HTTP response

# Check DNS resolution for CloudIQ
nslookup cloudiq.dell.com
# Expected: resolves to a public IP address (not NXDOMAIN or SERVFAIL)

# Check proxy configuration (if proxy is in use)
env | grep -i proxy
# Compare to SCG UI → Settings → Proxy settings
```


```text title="Expected output"
Testing HTTPS connectivity to CloudIQ endpoints...
  cloudiq.dell.com:443 ............................ Reachable
  esrs3.emc.com:443 ............................... Reachable
  telemetry.dell.com:443 .......................... Reachable
  api.cloudiq.dell.com:443 ........................ Reachable
All endpoints reachable. Configuration valid.

*   Trying 143.166.84.52...
* Connected to cloudiq.dell.com (143.166.84.52) port 443 (#0)
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Server hello (2):
* TLSv1.2 (IN), TLS Handshake finished (20):
> GET / HTTP/1.1
< HTTP/1.1 301 Moved Permanently
< Location: https://cloudiq.dell.com/login

*   Trying 207.126.97.18...
* Connected to esrs3.emc.com (207.126.97.18) port 443 (#0)
* TLSv1.2 (IN), TLS handshake, Server hello (2):
< HTTP/1.1 200 OK

Server:  203.0.113.45
Address:  203.0.113.45

Name:    cloudiq.dell.com
Address:  143.166.84.52

http_proxy=http://proxy.corp.local:8080
https_proxy=http://proxy.corp.local:8080
no_proxy=localhost,127.0.0.1,.corp.local
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to cloudiq.dell.com port 443: Connection timed out`** — Verify firewall rules allow outbound HTTPS on port 443 and check if a proxy is required in your environment.
    **`Server returned nothing (or only header "HTTP/1.0 407 Proxy Authentication Required")`** — Add proxy credentials to SCG via Settings → Proxy settings or configure curl with `-x http://user:pass@proxy:port`.
    **`nslookup: can't find cloudiq.dell.com: NXDOMAIN`** — Verify DNS servers are configured correctly and can reach public DNS (try `nslookup cloudiq.dell.com 8.8.8.8`).
**If connectivity test fails:**
1. Verify the proxy is configured correctly in SCG UI → Settings → Proxy
2. Test proxy connectivity directly: `curl -v --proxy http://<proxy-host>:<port> https://cloudiq.dell.com`
3. Engage the network team to confirm outbound HTTPS is allowed from the SCG IP to cloudiq.dell.com

---

## Step 3 — List and test devices

```bash
# List all devices registered with SCG
scg device list
# Output columns: Device ID, Name, Type, Status, Last Poll Time
# Look for: devices with Status = "Error" or Last Poll Time = stale (> 60 minutes ago)

# Test connectivity to a specific device
scg device test --id <device_id>
# Expected: Authentication OK; API reachable
# Failure output includes: the specific error (auth failed, connection refused, TLS error)

# For arrays with management interfaces — test directly from SCG
curl -sk https://<array-management-ip>/
# Expected: HTTP 200 (or redirect to login) from the array management API
# If connection refused: the SCG cannot reach the array management interface

# For PowerStore / Unity — test specific API
curl -sk -u admin:<password> "https://<array-ip>/api/rest/system?fields=name,model"
# Expected: JSON with system name and model

# Verify SCG polling interval
# SCG UI → Settings → Polling Interval (default: 5 minutes)
```


```text title="Expected output"
$ scg device list
Device ID                            Name                 Type        Status    Last Poll Time
a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6 array-prod-01        PowerStore  OK        2024-01-15 14:32:15
b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7 array-prod-02        PowerStore  OK        2024-01-15 14:31:42
c3d4e5f6-g7h8-49i0-j1k2-l3m4n5o6p7q8 array-dr-01          Unity       Error     2024-01-15 13:15:22
d4e5f6g7-h8i9-40j1-k2l3-m4n5o6p7q8r9 array-test-01        PowerStore  OK        2024-01-15 14:33:01

$ scg device test --id c3d4e5f6-g7h8-49i0-j1k2-l3m4n5o6p7q8
Testing device: array-dr-01 (192.168.1.45)
Authentication: FAILED - Invalid credentials
API Reachability: UNREACHABLE
Connection Status: TLS handshake failed

$ curl -sk https://192.168.1.45/
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: sessionid=abc123def456; Path=/
<html><head><title>Dell EMC Unity - Login</title>...

$ curl -sk -u admin:MyP@ssw0rd "https://192.168.1.50/api/rest/system?fields=name,model"
{
  "content": {
    "name": "array-prod-01",
    "model": "PowerStore 7000T"
  }
}
```

!!! warning "Common errors"
    **`Authentication: FAILED - Invalid credentials`** — Verify the SCG credentials stored in Settings match the current array admin password, or reset the array credentials in the SCG UI.
    **`Connection Status: TLS handshake failed`** — Confirm the array management interface certificate is valid and trusted by the SCG server, or disable certificate verification if using self-signed certs in a test environment.
    **`curl: (7) Failed to connect to 192.168.1.45 port 443: Connection refused`** — Verify the array management IP is correct and reachable from the SCG host using `ping` or `traceroute`, and confirm the array's management interface is running.
---

## Step 4 — Read SCG log files

```bash
# Live SCG application log
tail -100 /var/log/scg/scg.log | grep -i "error\|fail\|warn"
# Shows: polling errors, upload failures, authentication issues per device

# dsagw telemetry gateway log (uploads to CloudIQ)
tail -100 /var/log/dsagw/dsagw.log | grep -i "error\|fail\|connection"
# Shows: TLS handshake errors, proxy errors, connection resets

# SCG telemetry forwarding logs (per-device)
ls -lth /var/log/dsagw/
# Files named by device; check the specific device's log file

# System journal for service crashes
journalctl -u dsagw -n 100 --no-pager
journalctl -u scg -n 100 --no-pager 2>/dev/null || true

# All-in-one diagnostic snapshot
{
  echo "=== scg status ==="
  scg status
  echo "=== scg connectivity --test ==="
  scg connectivity --test
  echo "=== scg device list ==="
  scg device list
  echo "=== disk space ==="
  df -h /
  echo "=== dsagw service ==="
  systemctl status dsagw
} > /tmp/cloudiq-diag-$(date +%F-%H%M).txt
```


```text title="Expected output"
tail: cannot open '/var/log/scg/scg.log' for reading: No such file or directory
2024-01-15T09:42:33.521Z ERROR [PollingThread-3] Failed to poll device 10.50.12.44: Connection timeout after 30s
2024-01-15T09:42:45.103Z WARN [AuthManager] Token refresh failed for device SN-EMC0001: 401 Unauthorized
2024-01-15T09:43:12.667Z ERROR [UploadQueue] Upload to CloudIQ failed: HTTP 503 Service Unavailable

-rw-r--r-- 1 root root 2847291 Jan 15 09:45 device-SN-EMC0001.log
-rw-r--r-- 1 root root 1923847 Jan 15 09:40 device-SN-EMC0002.log
-rw-r--r-- 1 root root  847291 Jan 15 09:35 device-SN-EMC0003.log

Jan 15 09:44:22 scg-host dsagw[4521]: TLS handshake failed: certificate verify failed
Jan 15 09:43:55 scg-host dsagw[4521]: Connection reset by peer (10.200.1.5:443)
Jan 15 09:42:10 scg-host dsagw[4521]: Proxy authentication required for 10.200.1.100:8080

=== scg status ===
SCG Service: running (PID 3847)
Connected Devices: 3/5
Last Telemetry Upload: 2024-01-15 09:45:12 UTC
=== scg connectivity --test ===
Testing connectivity to CloudIQ endpoint (api.cloudiq.dell.com)...
✓ DNS resolution: OK
✓ TCP connection: OK
✗ TLS certificate validation: FAILED (untrusted CA)
=== scg device list ===
SN-EMC0001 | 10.50.12.44 | Connected | Last poll: 9s ago
SN-EMC0002 | 10.50.12.45 | Connected | Last poll: 15s ago
SN-EMC0003 | 10.50.12.46 | Disconnected | Last poll: 4m ago
=== disk space ===
Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1       50G   38G   9.2G  82% /
=== dsagw service ===
● dsagw.service - Dell CloudIQ Telemetry Gateway
   Loaded: loaded (/etc/systemd/system/dsagw.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2024-01-15 08:12:44 UTC; 1h 33min ago
   Main PID: 4521 (dsagw)
   Tasks: 12 (limit: 4915)
   Memory: 287.4M
   CGroup: /system.slice/dsagw.service
           └─4521 /opt/dell/dsagw/bin/dsagw -c /etc/dsagw/dsag
```
---

## Step 5 — Collect support bundle

```bash
# Collect the full SCG diagnostic bundle for Dell SR
scg log collect --output /tmp/scg-bundle-$(date +%F).tar.gz
# The bundle includes: application logs, device poll history, config (credentials sanitised), system info

# Download from SCG via SCP
scp admin@<scg-ip>:/tmp/scg-bundle-*.tar.gz /tmp/
```


```text title="Expected output"
Collecting SCG diagnostic bundle...
Gathering application logs... [████████████████████] 100%
Collecting device poll history... [████████████████████] 100%
Sanitizing configuration data... [████████████████████] 100%
Capturing system information... [████████████████████] 100%
Bundle created: /tmp/scg-bundle-2024-01-15.tar.gz (287 MB)
Compression complete in 42 seconds.

admin@192.168.1.45's password:
scg-bundle-2024-01-15.tar.gz                          100%  287MB   8.2MB/s   00:35
```

!!! warning "Common errors"
    **`scg: command not found`** — Verify SCG is installed and in PATH, or use the full path `/opt/dell/scg/bin/scg` instead.
    **`Permission denied (publickey,password)`** — Ensure the admin user credentials are correct and SSH key-based auth is configured, or add `-o PubkeyAuthentication=no` to force password auth.
    **`No such file or directory`** — Check that the bundle file was successfully created in `/tmp/` by running `ls -lh /tmp/scg-bundle-*.tar.gz` on the SCG host first.
---

## Log locations

| Component | Path | What to look for |
|---|---|---|
| SCG application | `/var/log/scg/scg.log` | Polling errors, device auth failures |
| dsagw gateway | `/var/log/dsagw/dsagw.log` | TLS errors, upload failures to CloudIQ |
| Per-device telemetry | `/var/log/dsagw/<device-id>.log` | Per-system polling detail |
| CloudIQ audit log | CloudIQ portal → Admin → Audit Log | API calls, user actions, config changes |

---

## See also

- [CloudIQ — Common Issues](../common-issues/)
- [CloudIQ — Escalation](../escalation/)
- [CloudIQ — Health Checks](../../operations/health-checks/)

## Verify resolution

- `scg status` shows `Connected to CloudIQ: Yes` with a recent `Last sync` timestamp
- `scg connectivity --test` shows all endpoints as `Reachable`
- `scg device list` shows all devices with `Status = OK` and `Last Poll Time` within the last poll cycle
- In CloudIQ portal: the previously missing systems appear in the Systems page with current data
- Monitor for 2 poll cycles (typically 10 minutes) to confirm stable reporting
