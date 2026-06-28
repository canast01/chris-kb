---
tags:
  - horizon
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Horizon — Diagnostics

<div class="kb-summary">
Horizon diagnostic commands: read Connection Server debug-*.log and vlsi-*.log logs, collect the support bundle from Horizon Admin UI, inspect Horizon Agent logs in the desktop VM, test UAG health and display protocol port connectivity, query the Horizon REST API for pool and session status, and use vdmadmin to list sessions and assignments.

*Applies to: Horizon 8.x*
</div>
![Horizon — Diagnostics](../../../../assets/virtualization-vmware-horizon-troubleshooting-diagnostics.svg)




```mermaid
graph TD
    A([Horizon Issue]) --> B{What type of problem?}
    B -->|Login failure or no session| C[Horizon Admin UI → Events\nFilter by ERROR and user account]
    B -->|Black screen after session connects| D[Check Horizon Agent in desktop VM\ndebug-*.log and wsnm_*.log]
    B -->|Desktop pool not provisioning| E[Horizon Admin UI → Pools → hover red error\nCheck vlsi-*.log for vCenter API errors]
    B -->|External access not working| F[curl https://uag:9443/rest/healthcheck\nCheck UAG esmanager.log]
    B -->|Slow session or low frame rate| G[Blast session: Ctrl+Alt+Shift+P\nCheck client → UAG → desktop network latency]
    B -->|Connection Server health alarm| H[Get-WinEvent VMware Application events\nCheck CS debug-*.log]
    C --> I{Error type?}
    I -->|LDAP / auth error| J[Check AD connectivity on CS\nTest-NetConnection ad.domain.local -Port 389]
    I -->|Entitlement error| K[Verify user is entitled to pool\nvdmadmin -A -d pool -list]
    I -->|Certificate error| L[Check CS certificate in MMC\nCheck UAG certificate via curl]
    D --> M[Check Horizon Agent service status\nGet-Service VMwareHorizonViewAgent]
    E --> N[Check vCenter credentials in Horizon\nAdmins → vCenter → Edit → Test Connection]
    F --> O[SSH to UAG; check gateway.log\ntail /opt/vmware/gateway/logs/gateway.log]
    G --> P[Test Blast port from client\nnc -vz uag.example.com 8443]
    H --> Q[Collect Connection Server support bundle\nHorizon Admin → Support → Generate Bundle]
    J --> Q
    K --> Q
    L --> Q
    M --> Q
    N --> Q
    O --> Q
    P --> Q
    Q --> R[Open VMware SR\nmysupport.vmware.com]

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,B,I dark
    class C,D,E,F,G,H,J,K,L,M,N,O,P action
    class Q,R escalate
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_horizon_admin_ui_events: "Step 1 — Check Horizon Admin UI events" {shape: rectangle}
step_2_read_connection_server_debug_: "Step 2 — Read Connection Server debug log" {shape: rectangle}
step_3_check_horizon_agent_in_the_de: "Step 3 — Check Horizon Agent in the desktop VM" {shape: rectangle}
step_4_test_uag_health_and_display_p: "Step 4 — Test UAG health and display protocol ports" {shape: rectangle}
step_5_use_vdmadmin_for_session_and_: "Step 5 — Use vdmadmin for session and assignment diagnostics" {shape: rectangle}
step_6_query_horizon_rest_api: "Step 6 — Query Horizon REST API" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_horizon_admin_ui_events: investigate
symptom -> step_2_read_connection_server_debug_: investigate
symptom -> step_3_check_horizon_agent_in_the_de: investigate
symptom -> step_4_test_uag_health_and_display_p: investigate
symptom -> step_5_use_vdmadmin_for_session_and_: investigate
symptom -> step_6_query_horizon_rest_api: investigate
step_1_check_horizon_admin_ui_events -> resolution
step_2_read_connection_server_debug_ -> resolution
step_3_check_horizon_agent_in_the_de -> resolution
step_4_test_uag_health_and_display_p -> resolution
step_5_use_vdmadmin_for_session_and_ -> resolution
step_6_query_horizon_rest_api -> resolution
```

## Before you begin

- **Access:** Horizon admin role; PowerShell on Connection Server(s); SSH to UAG appliance; access to the desktop VM (or RDP/console) if diagnosing agent issues
- **Gather first:** the specific symptom (login fails with error code, pool shows red, session connects but black screen), the affected username, the pool name, and the time the issue started
- **Scope:** confirm whether the issue affects one user, one pool, one Connection Server, or all Horizon sessions

---

## Step 1 — Check Horizon Admin UI events

```powershell
# On a Connection Server — Windows Event Log for Horizon events
Get-WinEvent -LogName "Application" -MaxEvents 100 |
  Where-Object { $_.ProviderName -like "*VMware*" } |
  Select-Object TimeCreated, LevelDisplayName, Message |
  Where-Object { $_.LevelDisplayName -eq "Error" } |
  Format-List

# ADAM (VMwareVDMDS) directory service errors (LDAP/AD connectivity)
Get-WinEvent -LogName "ADAM (VMwareVDMDS)" -MaxEvents 20 |
  Select-Object TimeCreated, LevelDisplayName, Message | Format-List

# Check Connection Server service state
Get-Service -Name "wsnm", "VMwareVDMDS", "cpsvc" |
  Select-Object Name, Status, StartType
# Expected: all Running
```

---

## Step 2 — Read Connection Server debug log

```powershell
# Log directory on Connection Server
$logDir = "C:\ProgramData\VMware\VDM\logs"
Get-ChildItem $logDir -Filter "debug-*.log" |
  Sort-Object LastWriteTime -Descending | Select-Object -First 3

# Most recent errors in debug log
Select-String -Path "$logDir\debug-*.log" -Pattern "ERROR" |
  Select-Object -Last 50 | Select-Object -ExpandProperty Line

# Filter by specific user for login failures
Select-String -Path "$logDir\debug-*.log" -Pattern "user.name@domain" |
  Select-Object -Last 30 | Select-Object -ExpandProperty Line

# vCenter API interaction log (for provisioning failures)
Select-String -Path "$logDir\vlsi-*.log" -Pattern "ERROR\|Fault\|Exception" |
  Select-Object -Last 30 | Select-Object -ExpandProperty Line
```

---

## Step 3 — Check Horizon Agent in the desktop VM

```powershell
# Inside the desktop VM (or remotely if you have access)
$agentLogDir = "C:\ProgramData\VMware\VDM\logs"

# Horizon Agent debug log (connection, entitlement, and agent startup)
Select-String -Path "$agentLogDir\debug-*.log" -Pattern "ERROR\|FAIL" |
  Select-Object -Last 30

# Display protocol log (Blast/PCoIP session issues, black screen)
Select-String -Path "$agentLogDir\wsnm_*.log" -Pattern "ERROR" |
  Select-Object -Last 30

# Check Horizon Agent service is running
Get-Service -Name "VMware Horizon View Agent"
# Expected: Status = Running

# Check agent Windows Event Log
Get-WinEvent -LogName "Application" |
  Where-Object { $_.ProviderName -like "*Horizon*" -or $_.ProviderName -like "*VMware*" } |
  Select-Object -First 20 | Select-Object TimeCreated, Message | Format-List
```

---

## Step 4 — Test UAG health and display protocol ports

```bash
# From a host that can reach the UAG — test the health endpoint
curl -sk https://<uag-fqdn>:9443/rest/healthcheck
# Expected: HTTP 200 OK; JSON with "ok":true

# Test display protocol ports from a client or jump host
nc -vz <uag-fqdn> 443   # HTTPS (required for all protocols)
nc -vz <uag-fqdn> 8443  # Blast HTTPS / DTLS
nc -vz <uag-fqdn> 4172  # PCoIP UDP (test with TCP first as approximation)

# Check path to UAG
traceroute <uag-fqdn>

# SSH to UAG appliance for log inspection
ssh root@<uag-ip>
tail -100 /opt/vmware/gateway/logs/esmanager.log
tail -100 /opt/vmware/gateway/logs/gateway.log

# Collect UAG log bundle via REST API
curl -sk -X GET "https://<uag-fqdn>:9443/rest/v1/config/logs/collect" \
  -u admin:<password> -o uag-logs-$(date +%Y%m%d).zip
```

---

## Step 5 — Use vdmadmin for session and assignment diagnostics

```powershell
# vdmadmin.exe is in C:\Program Files\VMware\VMware View\Server\tools\bin\
$vdmadmin = "C:\Program Files\VMware\VMware View\Server\tools\bin\vdmadmin.exe"

# List active sessions for a specific pool
& $vdmadmin -L -d <pool-name>
# Shows: user, machine, session state, protocol, start time

# List user assignments to a dedicated desktop pool
& $vdmadmin -A -d <pool-name> -list
# Shows: which machines are assigned to which users

# List all Connection Servers in the pod
& $vdmadmin -S -list
# Shows: CS hostname, version, connection state

# For floating pool — list current desktop state
& $vdmadmin -M -d <pool-name> -list
```

---

## Step 6 — Query Horizon REST API

```bash
# Authenticate to Horizon REST API (Connection Server)
TOKEN=$(curl -sk -X POST "https://<cs-fqdn>/rest/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","domain":"corp"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('access_token',''))")

echo $TOKEN
# Expected: JWT string; empty = auth failed (check domain suffix)

# Get Connection Server health
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<cs-fqdn>/rest/monitor/connection-servers" \
  | python3 -c "
import json,sys
for cs in json.load(sys.stdin):
    print(cs.get('name',''), '|', cs.get('status',''), '|', cs.get('cs_replications_status',''))
"
# Expected: status = OK for all Connection Servers

# Get desktop pool summary
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<cs-fqdn>/rest/inventory/v1/desktop-pools" \
  | python3 -c "
import json,sys
for p in json.load(sys.stdin):
    print(p.get('name',''), '|', p.get('type',''), '|', p.get('enabled',''))
"

# Get active sessions count
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<cs-fqdn>/rest/monitor/v2/sessions" | python3 -m json.tool | head -30
```

---

## Step 7 — Collect Horizon support bundle

```powershell
# Via Horizon Admin UI (recommended for CS logs + vCenter events)
# Navigate to: Horizon Admin → Troubleshooting → Generate Support Bundle
# Click: Generate → Download
# The bundle includes: all CS log files, ADAM DB export, event log, vCenter events

# Via PowerShell on Connection Server (if UI is unavailable)
# The bundle location after UI generation:
Get-ChildItem "C:\ProgramData\VMware\VDM\logs\*bundle*" |
  Sort-Object LastWriteTime -Descending | Select-Object -First 1

# For escalation, include:
# - Horizon support bundle (from CS or Admin UI)
# - Horizon Agent debug log from affected desktop VM
# - UAG log bundle (from UAG REST API)
# - Session ID or username, time of failure, and error code from the UI or client
```

---

## Log locations

| Component | Path | What to look for |
|---|---|---|
| Connection Server | `C:\ProgramData\VMware\VDM\logs\debug-*.log` | Auth failures, pool provisioning errors, broker decisions |
| CS vCenter ops | `C:\ProgramData\VMware\VDM\logs\vlsi-*.log` | vCenter API errors during provisioning |
| Horizon Agent | `C:\ProgramData\VMware\VDM\logs\debug-*.log` (in desktop VM) | Agent startup, entitlement, and session errors |
| Agent display | `C:\ProgramData\VMware\VDM\logs\wsnm_*.log` | Blast/PCoIP protocol session events |
| UAG edge | `/opt/vmware/gateway/logs/esmanager.log` | Edge service brokering and connection errors |
| UAG gateway | `/opt/vmware/gateway/logs/gateway.log` | Main UAG log; HTTPS and protocol routing |
| Windows events | `Get-WinEvent -LogName Application` | VMware provider events for both CS and Agent |

---

## See also

- [Horizon — Common Issues](../common-issues/)
- [Horizon — Escalation](../escalation/)

## Verify resolution

- `curl -sk https://<uag-fqdn>:9443/rest/healthcheck` returns `{"ok":true}` for all UAGs
- The previously failing user can log in and reach a desktop without errors
- Horizon Admin UI → Events shows no new ERROR-level events for the affected pool or user
- Blast display protocol connectivity test (`nc -vz uag 8443`) succeeds from the affected client network
- Pool provisioning shows green in Horizon Admin UI → Desktops
