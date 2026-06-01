# Secure Connect Gateway (SCG) — CLI Reference


<div class="kb-summary">
> Part of the [Secure Connect Gateway](../index.md) reference.
</div>
```powershell
┌────────────────────────────────────── Dell SCG — CLI Reference ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            SCG CLI: command-line interface for all management and operational tasks           │   │
│   │            Access: SSH or REST client to management IP; authenticate as admin role            │   │
│   │        Commands: status, list, create, modify, delete, show, and diagnostic operations        │   │
│   │          Scripting: use REST API or CLI in automation for provisioning and reporting          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH → authenticate → show status → configure → verify → log output                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Collection         │  │        Array adapters       │  │         Per product         │   │
│   │          Transport          │  │        HTTPS outbound       │  │          No inbound         │   │
│   │         CloudIQ feed        │  │       Telemetry relay       │  │        Near real-time       │   │
│   │        Support tunnel       │  │        Remote assist        │  │        On-demand only       │   │
│   │           Alerting          │  │         Email/syslog        │  │       Threshold rules       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Category     │     Command      │      Purpose      │      Output      │      Notes       │   │
│   │      Status      │   show status    │    Health check   │   State/alerts   │    Daily run     │   │
│   │       List       │     list all     │     Inventory     │   Name/ID/size   │    Read-only     │   │
│   │      Create      │  create volume   │     Provision     │    New object    │    Change req    │   │
│   │      Delete      │ delete resource  │    Decommission   │   Confirmation   │   Irreversible   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SCG VM or appliance on-prem · outbound HTTPS to Dell · connected storage arrays          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SCG                = Secure Connect Gateway; replaces ESRS as Dell remote support relay platform   │
│    ESRS               = EMC Secure Remote Services; predecessor to SCG; still supported on older ar...│
│    Adapter            = SCG component connecting to a specific array type: Unity, PowerStore, PowerMax│
│    CloudIQ relay      = SCG forwards array health telemetry to CloudIQ SaaS for analytics             │
│    Support tunnel     = Dell TAC can open an encrypted on-demand remote session via SCG               │
│    Device registration = arrays registered in SCG; SCG authenticates to Dell support portal           │
│    Site               = SCG logical grouping of arrays at a physical location within the organisation │
│    Policy             = SCG alert policy; defines which events trigger email or syslog notifications  │
│    SCG bundle         = log/diagnostic collection submitted to Dell support via SCG upload            │
│    Gateway HA         = two SCG instances in active-active; both relay telemetry independently        │
│    Port 9443          = SCG local management UI port; REST API also served on port 9443               │
│    Outbound only      = SCG connections are outbound HTTPS; no inbound firewall rules required        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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
