---
tags:
  - dell
---
# Secure Connect Gateway (SCG) — CLI Reference

<div class="kb-summary">
SCG CLI reference: `dcicli` command usage for connectivity verification, `supportassist` log collection, device inventory queries, and remote support tunnel management.

*Applies to: Secure Connect Gateway*
</div>

---

Secure Connect Gateway (SCG) is Dell's remote support and telemetry gateway appliance, replacing the older SupportAssist Enterprise and ESRS (EMC Secure Remote Services) agents. It collects telemetry from registered Dell devices and forwards it to Dell's backend over an outbound HTTPS connection.

SCG is managed via:
- **SSH** to the SCG appliance → SCG management shell
- **SCG REST API** (port 9443) for programmatic management
- **Unisphere / iDRAC / product-specific UIs** which register themselves with SCG automatically

> **SSH access**: `ssh admin@<SCG_IP>` (default port 22)  
> **REST API base URL**: `https://<SCG_IP>:9443/scg/rest/v1`  
> **Web UI**: `https://<SCG_IP>` (port 443)

---

```d2
direction: down

quickreference_command_table: "Quick-Reference Command Table" {shape: rectangle}
scg_management_shell: "SCG Management Shell" {shape: rectangle}
device_registration: "Device Registration" {shape: rectangle}
connectivity_check: "Connectivity Check" {shape: rectangle}
log_collection: "Log Collection" {shape: rectangle}
rest_api_curl: "REST API (curl)" {shape: rectangle}

quickreference_command_table -> scg_management_shell: uses
scg_management_shell -> device_registration: uses
device_registration -> connectivity_check: uses
connectivity_check -> log_collection: uses
log_collection -> rest_api_curl: uses
```

## Quick-Reference Command Table

| Command | Purpose |
|---|---|
| `ssh admin@<SCG_IP>` | Open SCG management shell |
| `dsagw status` | DSA Gateway service status |
| `dsagw list-devices` | All registered devices and connectivity status |
| `dsagw restart` | Restart the SCG gateway service |
| `device-register --host <ip> --type <type>` | Register a new device with SCG |
| `device-list` | List all registered devices |
| `device-status --id <device_id>` | Connectivity and telemetry status for a device |
| `supportassist collect --id <device_id>` | Trigger diagnostic collection from a device |
| `log show --component gateway --lines 100` | View SCG gateway logs |
| `GET /devices` (REST) | List all devices via REST API |
| `GET /connectivity` (REST) | Check SCG backend connectivity status |

---

## SCG Management Shell

After SSHing to the SCG appliance, you land in the SCG CLI shell. Commands below run from within this shell unless otherwise noted.

```bash
# --- Connect to SCG ---
ssh admin@<SCG_IP>
# Default credentials: admin / <set during deployment>
# You will land at the SCG> prompt or admin shell

# --- SCG gateway service status ---
dsagw status

# Show detailed status including version, uptime, last telemetry upload
dsagw status --verbose

# --- List all registered devices ---
dsagw list-devices

# Show device list with connectivity state and last contact time
dsagw list-devices --format table

# --- Restart the SCG gateway service ---
# Use when: telemetry uploads are stalled, after network changes, after SCG upgrade
dsagw restart

# --- Stop / start the SCG service ---
dsagw stop
dsagw start

# --- Show SCG version and build information ---
dsagw version

# --- Show SCG appliance network configuration ---
dsagw network show

# Configure a proxy (if SCG reaches Dell backend through a proxy)
dsagw network set-proxy \
  --host proxy.corp.example.com \
  --port 8080 \
  --username proxyuser \
  --password '<proxypass>'

# Disable proxy
dsagw network clear-proxy

# Show current proxy setting
dsagw network show-proxy

# --- Test connectivity to Dell backend ---
dsagw connectivity-check

# Verbose connectivity test (shows each endpoint tested)
dsagw connectivity-check --verbose
# Expected: all endpoints report PASS
# Endpoints tested:
#   esrs.emc.com (legacy)
#   esrs3.emc.com
#   downloads.dell.com
#   api.dell.com

# --- Show SCG TLS certificate details ---
dsagw certificate show

# Regenerate self-signed certificate
dsagw certificate regenerate
```


```text title="Expected output"
admin@192.168.1.50's password: 
SCG> dsagw status
Service Status: RUNNING
Uptime: 45 days, 3 hours, 22 minutes
Last Telemetry Upload: 2024-01-15 14:32:18 UTC

SCG> dsagw status --verbose
Service Status: RUNNING
Version: 2.4.1
Build: 20240110.001
Uptime: 45 days, 3 hours, 24 minutes
Last Telemetry Upload: 2024-01-15 14:32:18 UTC
Telemetry Upload Interval: 24 hours
Connected Devices: 12

SCG> dsagw list-devices
Device ID                          | Hostname          | Status
-----------------------------------|-------------------|----------
5f8c2a1b-4d9e-11ee-a5c1-0242ac120002 | storage-array-01  | ONLINE
7a3f5e9c-4d9e-11ee-a5c1-0242ac120003 | storage-array-02  | ONLINE
9b2d1f4a-4d9e-11ee-a5c1-0242ac120004 | nas-cluster-prod  | ONLINE
...

SCG> dsagw list-devices --format table
Hostname          | Device ID                            | Last Contact       | Connectivity
------------------|--------------------------------------|--------------------|--------------
storage-array-01  | 5f8c2a1b-4d9e-11ee-a5c1-0242ac120002 | 2024-01-15 14:28:45 | CONNECTED
storage-array-02  | 7a3f5e9c-4d9e-11ee-a5c1-0242ac120003 | 2024-01-15 14:29:12 | CONNECTED
nas-cluster-prod  | 9b2d1f4a-4d9e-11ee-a5c1-0242ac120004 | 2024-01-15 14:30:01 | CONNECTED

SCG> dsagw restart
Stopping SCG gateway service...
Service stopped successfully.
Starting SCG gateway service...
Service started successfully.
Status: RUNNING

SCG> dsagw version
SCG Version: 2.4.1
Build Number: 20240110.001
Build Date: 2024-01-10 09:15:32 UTC

SCG> dsagw network show
Interface: eth0
IP Address: 192.168.1.50
Netmask: 255.255.255.0
Gateway: 192.168.1.1
DNS Servers: 8.8.8.8, 8.8.4.4

SCG> dsagw connectivity-check
Testing connectivity to Dell backend endpoints...
esrs.emc.com: PASS (response time: 145ms)
esrs3.emc.com: PASS (response time: 132ms)
downloads.dell.com: PASS (response time: 198ms)
api.dell.com: PASS (response time: 156ms)
Overall Status: ALL ENDPOINTS REACHABLE

SCG> dsagw certificate show
Certificate Subject: CN=scg-gateway.
```
---

## Device Registration

SCG can auto-discover and register Dell devices, or you can register them manually.

```bash
# --- List registered devices (from SCG shell) ---
device-list

# Show device list with ID, IP, type, status
device-list --format long

# --- Register a device manually ---
# Supported types: POWERMAX, UNITY, VMAX, DATADOMAIN, POWERSTORE,
#                  ISILON, IDRAC, NETWORKER, AVAMAR
device-register \
  --host 10.10.10.50 \
  --type POWERMAX \
  --username <username> \
  --password '<password>'

# Register a Data Domain appliance
device-register \
  --host 10.10.10.60 \
  --type DATADOMAIN \
  --username sysadmin \
  --password '<password>'

# Register an iDRAC for a server
device-register \
  --host 10.10.10.70 \
  --type IDRAC \
  --username root \
  --password '<password>'

# --- Check device registration and connectivity status ---
DEVICE_ID="<device_id>"    # From device-list output

device-status --id "${DEVICE_ID}"

# Key status fields:
#   Connection Status    – CONNECTED / DISCONNECTED / UNKNOWN
#   Last Contact         – Timestamp of last successful telemetry
#   Collection Status    – ACTIVE / IDLE / ERROR
#   Telemetry Enabled    – true/false

# --- Remove a registered device ---
device-deregister --id "${DEVICE_ID}"

# --- Trigger an immediate telemetry collection from a device ---
device-collect --id "${DEVICE_ID}"

# Verify collection completed
device-status --id "${DEVICE_ID}"
```


```text title="Expected output"
ID                                   IP            Type       Status       Last Contact
================================================================================================
device-001                           10.10.10.50   POWERMAX   CONNECTED    2024-01-15 14:32:18
device-002                           10.10.10.60   DATADOMAIN CONNECTED    2024-01-15 14:28:45
device-003                           10.10.10.70   IDRAC      DISCONNECTED  2024-01-15 13:55:02

Device registered successfully.
Device ID: device-004
Host: 10.10.10.50
Type: POWERMAX
Status: PENDING_VERIFICATION

Device registered successfully.
Device ID: device-005
Host: 10.10.10.60
Type: DATADOMAIN
Status: PENDING_VERIFICATION

Device registered successfully.
Device ID: device-006
Host: 10.10.10.70
Type: IDRAC
Status: PENDING_VERIFICATION

Connection Status:    CONNECTED
Last Contact:        2024-01-15 14:32:18
Collection Status:   ACTIVE
Telemetry Enabled:   true
Firmware Version:    T9.1.0.0

Device device-004 deregistered successfully.

Telemetry collection initiated for device device-004.
Collection Job ID: job-20240115-001

Connection Status:    CONNECTED
Last Contact:        2024-01-15 14:35:22
Collection Status:   ACTIVE
Telemetry Enabled:   true
```

!!! warning "Common errors"
    **`Error: Authentication failed for host 10.10.10.50`** — Verify the username and password are correct and the device account is not locked.
    **`Error: Unable to reach host 10.10.10.60 on port 443`** — Confirm the device IP is reachable and firewall rules allow SCG to connect on the required port.
    **`Error: Device type POWERMAX is not supported in this SCG version`** — Check the SCG release notes and upgrade if necessary, or use a supported device type.
---

## Connectivity Check

```bash
# --- Test SCG → Dell backend connectivity ---
dsagw connectivity-check

# Sample output (all should show PASS):
# Checking esrs.emc.com:443           ... PASS
# Checking esrs3.emc.com:443          ... PASS
# Checking downloads.dell.com:443     ... PASS
# Checking api.dell.com:443           ... PASS

# --- Test from the SCG OS shell (requires dropping to bash) ---
# Type 'bash' or 'shell' at the SCG> prompt if permitted:
curl -sv --max-time 10 https://esrs3.emc.com/ 2>&1 | grep -E "Connected|SSL|HTTP"

# Test proxy connectivity
curl -sv --max-time 10 \
  --proxy http://proxy.corp.example.com:8080 \
  https://esrs3.emc.com/ 2>&1 | grep -E "Connected|SSL|HTTP"

# --- DNS resolution check ---
nslookup esrs3.emc.com
nslookup api.dell.com

# --- Check firewall requirements (outbound from SCG) ---
# Required outbound HTTPS (port 443) destinations:
#   esrs.emc.com
#   esrs3.emc.com
#   downloads.dell.com
#   api.dell.com
#   *.api.dell.com

# Test TCP connectivity to each
nc -zv esrs3.emc.com 443
nc -zv api.dell.com 443
nc -zv downloads.dell.com 443
```


```text title="Expected output"
SCG> dsagw connectivity-check
Checking esrs.emc.com:443           ... PASS
Checking esrs3.emc.com:443          ... PASS
Checking downloads.dell.com:443     ... PASS
Checking api.dell.com:443           ... PASS
Checking *.api.dell.com:443         ... PASS

*   Trying 185.12.45.67:443...
* Connected to esrs3.emc.com (185.12.45.67) port 443 (#0)
* SSL connection using TLSv1.3 / ECDHE-RSA-AES256-GCM-SHA384
* HTTP/1.1 200 OK

*   Trying 10.50.12.8:8080...
* Connected to proxy.corp.example.com (10.50.12.8) port 8080 (#0)
* HTTP/1.1 200 OK

Server:  8.8.8.8
Address: 8.8.8.8#53
Name:    esrs3.emc.com
Address: 185.12.45.67

Server:  8.8.8.8
Address: 8.8.8.8#53
Name:    api.dell.com
Address: 203.0.113.42

Connection to esrs3.emc.com 443 port [tcp/https] succeeded!
Connection to api.dell.com 443 port [tcp/https] succeeded!
Connection to downloads.dell.com 443 port [tcp/https] succeeded!
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to esrs3.emc.com port 443: Connection timed out`** — Verify outbound HTTPS (port 443) is not blocked by firewall rules; check SCG security group or network ACLs permit egress to Dell domains.
    **`nslookup: can't resolve 'esrs3.emc.com': No answer`** — Confirm DNS resolver is configured on SCG (check /etc/resolv.conf) and can reach upstream DNS servers; test with `nslookup 8.8.8.8` first.
    **`nc: getaddrinfo for host "api.dell.com" port 443: Temporary failure in name resolution`** — Ensure DNS is functional by running `nslookup api.dell.com` first; if DNS fails, configure nameserver in SCG network settings before retrying connectivity tests.
---

## Log Collection

```bash
# --- View SCG gateway logs (from SCG shell) ---
log show --component gateway

# Show last N lines
log show --component gateway --lines 200

# View logs with a time filter
log show --component gateway --since "2026-01-01 00:00:00"

# --- View device-specific collection logs ---
log show --component collector --device-id "${DEVICE_ID}"

# --- Available log components ---
# gateway     – Core SCG gateway process (connectivity, auth, telemetry upload)
# collector   – Per-device telemetry collection
# api         – REST API access log
# system      – OS-level SCG appliance log

# --- View logs from OS shell (if bash access is permitted) ---
tail -f /opt/dell/scg/logs/gateway.log
tail -f /opt/dell/scg/logs/collector.log

# --- Trigger a SupportAssist log bundle from a registered device ---
# This pushes diagnostic data to Dell proactively (e.g. before calling support)
supportassist collect --id "${DEVICE_ID}"

# Collect for a specific case number
supportassist collect --id "${DEVICE_ID}" --case-number 12345678

# Check collection job status
supportassist status --id "${DEVICE_ID}"

# --- SCG appliance system logs (OS level) ---
journalctl -u scg-gateway --since "1 hour ago"
journalctl -u scg-gateway -f

# --- Download SCG appliance support bundle ---
# From SCG shell:
supportbundle create
# Bundle will be at /var/support/scg_bundle_<date>.tar.gz
# Copy off with SCP:
# scp admin@<SCG_IP>:/var/support/scg_bundle_<date>.tar.gz /local/path/
```


```text title="Expected output"
[2026-01-15T14:32:18.445Z] [gateway] Connection established to collector node-prod-01 (192.168.1.42:8443)
[2026-01-15T14:32:19.102Z] [gateway] Authentication token refreshed for device 5f8a2c1d-9e4b-11ed-a1eb-0242ac120002
[2026-01-15T14:32:22.567Z] [gateway] Telemetry upload successful: 1247 metrics, 342 KB
[2026-01-15T14:32:25.891Z] [gateway] Health check passed for 8 registered devices
[2026-01-15T14:32:31.234Z] [gateway] API request from 10.0.5.18 - GET /api/v2/devices (200 OK)
[2026-01-15T14:32:45.678Z] [gateway] Sync cycle completed in 2.3s
...
(showing last 200 lines)

Jan 15 14:28:00 scg-appliance scg-gateway[4521]: Started gateway service v2.4.1-build.8847
Jan 15 14:28:15 scg-appliance scg-gateway[4521]: Listening on 0.0.0.0:8443
Jan 15 14:28:22 scg-appliance scg-gateway[4521]: Loaded 12 device profiles from /etc/scg/devices.conf
Jan 15 14:28:45 scg-appliance scg-gateway[4521]: Connected to backend at dell-telemetry.cloud.internal
Jan 15 14:29:10 scg-appliance scg-gateway[4521]: Collection cycle 1 completed: 8 devices, 0 errors

SupportAssist collection job initiated
Job ID: sa-job-20260115-7f3a9c2e
Device: node-prod-01 (5f8a2c1d-9e4b-11ed-a1eb-0242ac120002)
Status: IN_PROGRESS
Estimated completion: 2026-01-15T14:45:00Z

Support bundle created successfully
Location: /var/support/scg_bundle_20260115_143201.tar.gz
Size: 487 MB
```

!!! warning "Common errors"
    **`log show: component 'gateway' not found`** — Verify the component name matches one of the available options (gateway, collector, api, system) and that SCG is running.
    **`supportassist collect: Device ID not registered or offline`** — Ensure the device is registered in SCG and has active connectivity; check with `log show --component gateway` for connection errors.
    **`Permission denied: /var/support/scg_bundle_*.tar.gz`** — Run the supportbundle command from the SCG shell with appropriate admin privileges, or use `sudo` if executing from OS shell.
---

## REST API (curl)

The SCG REST API runs on port 9443. Authenticate with Basic auth or an API token.

```bash
SCG="https://<SCG_IP>:9443/scg/rest/v1"
CREDS="admin:<password>"

# --- Get SCG gateway status ---
curl -s -k -u "${CREDS}" \
  "${SCG}/gateway/status" | python3 -m json.tool

# --- List all registered devices ---
curl -s -k -u "${CREDS}" \
  "${SCG}/devices" | python3 -m json.tool

# Key device fields:
#   id               – SCG device identifier
#   hostname         – Device IP or hostname
#   type             – POWERMAX / UNITY / DATADOMAIN / etc.
#   connectionStatus – CONNECTED / DISCONNECTED
#   lastContactTime  – ISO8601 timestamp of last telemetry

# --- Get details for a specific device ---
curl -s -k -u "${CREDS}" \
  "${SCG}/devices/${DEVICE_ID}" | python3 -m json.tool

# --- Get SCG backend connectivity status ---
curl -s -k -u "${CREDS}" \
  "${SCG}/connectivity" | python3 -m json.tool

# --- Get alerts from registered devices ---
curl -s -k -u "${CREDS}" \
  "${SCG}/alerts" | python3 -m json.tool

# Filter alerts by severity
curl -s -k -u "${CREDS}" \
  "${SCG}/alerts?severity=CRITICAL" | python3 -m json.tool

# Filter alerts by device
curl -s -k -u "${CREDS}" \
  "${SCG}/alerts?deviceId=${DEVICE_ID}" | python3 -m json.tool

# --- Trigger telemetry collection via REST ---
curl -s -k -X POST \
  -u "${CREDS}" \
  -H "Content-Type: application/json" \
  "${SCG}/devices/${DEVICE_ID}/collect" | python3 -m json.tool

# --- Get SCG version and configuration ---
curl -s -k -u "${CREDS}" \
  "${SCG}/system/info" | python3 -m json.tool

# --- Get network/proxy configuration ---
curl -s -k -u "${CREDS}" \
  "${SCG}/network/proxy" | python3 -m json.tool

# --- Update proxy configuration via REST ---
curl -s -k -X PUT \
  -u "${CREDS}" \
  -H "Content-Type: application/json" \
  "${SCG}/network/proxy" \
  -d '{
    "enabled": true,
    "host": "proxy.corp.example.com",
    "port": 8080,
    "username": "proxyuser",
    "password": "<proxypass>"
  }' | python3 -m json.tool
```


```text title="Expected output"
{
  "gatewayId": "SCG-001-PROD",
  "version": "2.4.1.0",
  "status": "HEALTHY",
  "uptime": 847293,
  "lastHealthCheck": "2024-01-15T14:32:18Z"
}
{
  "devices": [
    {
      "id": "dev-powermax-001",
      "hostname": "192.168.1.45",
      "type": "POWERMAX",
      "connectionStatus": "CONNECTED",
      "lastContactTime": "2024-01-15T14:31:52Z"
    },
    {
      "id": "dev-unity-002",
      "hostname": "unity-array.corp.local",
      "type": "UNITY",
      "connectionStatus": "CONNECTED",
      "lastContactTime": "2024-01-15T14:30:11Z"
    },
    {
      "id": "dev-datadomain-003",
      "hostname": "dd-backup-01.corp.local",
      "type": "DATADOMAIN",
      "connectionStatus": "DISCONNECTED",
      "lastContactTime": "2024-01-15T13:15:44Z"
    }
  ]
}
{
  "id": "dev-powermax-001",
  "hostname": "192.168.1.45",
  "type": "POWERMAX",
  "model": "PowerMax 8000",
  "serialNumber": "000297900123",
  "connectionStatus": "CONNECTED",
  "lastContactTime": "2024-01-15T14:31:52Z",
  "firmwareVersion": "5.2.1.0"
}
{
  "backend": "DELL_SUPPORT",
  "status": "CONNECTED",
  "latency_ms": 42,
  "lastSync": "2024-01-15T14:32:01Z"
}
{
  "alerts": [
    {
      "id": "alert-5847",
      "deviceId": "dev-powermax-001",
      "severity": "WARNING",
      "message": "Disk utilization above 85%",
      "timestamp": "2024-01-15T14:15:33Z"
    },
    {
      "id": "alert-5846",
      "deviceId": "dev-unity-002",
      "severity": "INFO",
      "message": "Scheduled snapshot completed",
      "timestamp": "2024-01-15T14:00:22Z"
    }
  ]
}
{
  "alerts": [
    {
      "id": "alert-5844",
      "deviceId": "dev-datadomain-003",
      "severity": "CRITICAL",
      "message": "Device unreachable - connection timeout",
      "timestamp": "2024-01-15T13:16:05Z"
    }
  ]
}
{
  "alerts": [
    {
      "id": "alert-5847",
      "deviceId": "dev-powermax-001",
      "severity": "WARNING",
      "message": "Disk utilization above 85%",
      "timestamp": "2
```
## See also

- [Secure Connect Gateway — Overview](../../)
