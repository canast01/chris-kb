# Horizon — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Collect Horizon Support Bundle, Windows Event Log (Connection Server), Horizon Agent Logs in Guest VM, UAG Log Collection, Test Display Protocol Connectivity and 3 more sections.
</div>

  Diagnostic Data Sources
```powershell
┌──────────────────────────────────────────────────────────────┐
│  Connection Server                UAG                                                                 │
│  ┌────────────────────────────┐   ┌────────────────────────┐                                          │
│  │ C:\ProgramData\VMware\VDM\ │   │ /opt/vmware/gateway/   │                                          │
│  │  logs\debug-<date>.txt     │   │  logs/esmanager.log    │                                          │
│  │  audit-<date>.txt          │   │ REST: GET /rest/v1/    │                                          │
│  │  ws_tomcat-<date>.txt      │   │  config/logs/collect   │                                          │
│  └────────────────────────────┘   └────────────────────────┘                                          │
│                                                                                                       │
│  Desktop VM (guest)               DCT Support Bundle                                                  │
│  ┌────────────────────────────┐   ┌────────────────────────┐                                          │
│  │ C:\ProgramData\VMware\VDM\ │   │ Horizon Console →      │                                          │
│  │  logs\ (Horizon Agent)     │   │  Help → Download       │                                          │
│  │ Get-Service "VMware        │   │  Support Bundle        │                                          │
│  │  Horizon View Agent"       │   │  (ZIP of all CS logs)  │                                          │
│  └────────────────────────────┘   └────────────────────────┘                                          │
└──────────────────────────────────────────────────────────────┘
```
```
┌──────────────────────────────────── VMware Horizon — Diagnostics ─────────────────────────────────────┐
│                                                                                                       │
│  Horizon diagnostics use Connection Server logs, support bundles, Horizon admin UI,                   │
│  and desktop agent logs to identify root causes of session and provisioning failures.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Connection Server Logs            │  │                  Agent Logs                 │   │
│   │          C:\ProgramData\VMware\VDM           │  │          C:\ProgramData\VMware\VDM          │   │
│   │           debug-*.log: main broker           │  │          debug-*.log on desktop VM          │   │
│   │           vlsi-*.log: vCenter ops            │  │           wsnm_*.log: display path          │   │
│   │          support bundle: zip via UI          │  │            Event log: Windows App           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Start with CS debug log; if session connects but black screen, check agent logs.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Admin UI Diagnostics             │  │               UAG Diagnostics               │   │
│   │           Horizon Admin: Dashboard           │  │              UAG admin UI: 9443             │   │
│   │          Events: filter by severity          │  │           /rest/healthcheck: 200?           │   │
│   │          Pool: provisioning errors           │  │           UAG log: /opt/vmware/etc          │   │
│   │          Sessions: filter by state           │  │          Cert: check UAG cert date          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Collect CS support bundle via Horizon Admin UI; agent logs from desktop VM;                          │
│  UAG logs via SSH to UAG appliance.                                                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  debug-*.log   = CS main log; broker decisions, auth, pool operations                                 │
│  vlsi-*.log    = vCenter API interaction log; provisioning details                                    │
│  wsnm_*.log    = agent display protocol log; Blast/PCoIP session                                      │
│  ProgramData   = Windows hidden folder; Horizon stores logs here                                      │
│  Support bundle= Horizon Admin UI > Support > Generate Bundle                                         │
│  Horizon Admin = web UI for Horizon management; port 443 on CS                                        │
│  Events tab    = Horizon UI event log; filter by error/warning                                        │
│  UAG admin     = port 9443; cert, edge service, health config                                         │
│  /rest/healthcheck= UAG health endpoint; returns 200 OK if healthy                                    │
│  UAG log       = /opt/vmware/etc/esmanager/; edge service logs                                        │
│  Windows App log= Windows Event Viewer; Horizon Agent events here                                     │
│  Pool error    = UI shows red error; hover for provisioning reason                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```
┌──────────────────────────────────── VMware Horizon — Diagnostics ─────────────────────────────────────┐
│                                                                                                       │
│  Horizon diagnostics use Connection Server logs, support bundles, Horizon admin UI,                   │
│  and desktop agent logs to identify root causes of session and provisioning failures.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Connection Server Logs            │  │                  Agent Logs                 │   │
│   │          C:\ProgramData\VMware\VDM           │  │          C:\ProgramData\VMware\VDM          │   │
│   │           debug-*.log: main broker           │  │          debug-*.log on desktop VM          │   │
│   │           vlsi-*.log: vCenter ops            │  │           wsnm_*.log: display path          │   │
│   │          support bundle: zip via UI          │  │            Event log: Windows App           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Start with CS debug log; if session connects but black screen, check agent logs.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Admin UI Diagnostics             │  │               UAG Diagnostics               │   │
│   │           Horizon Admin: Dashboard           │  │              UAG admin UI: 9443             │   │
│   │          Events: filter by severity          │  │           /rest/healthcheck: 200?           │   │
│   │          Pool: provisioning errors           │  │           UAG log: /opt/vmware/etc          │   │
│   │          Sessions: filter by state           │  │          Cert: check UAG cert date          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Collect CS support bundle via Horizon Admin UI; agent logs from desktop VM;                          │
│  UAG logs via SSH to UAG appliance.                                                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  debug-*.log   = CS main log; broker decisions, auth, pool operations                                 │
│  vlsi-*.log    = vCenter API interaction log; provisioning details                                    │
│  wsnm_*.log    = agent display protocol log; Blast/PCoIP session                                      │
│  ProgramData   = Windows hidden folder; Horizon stores logs here                                      │
│  Support bundle= Horizon Admin UI > Support > Generate Bundle                                         │
│  Horizon Admin = web UI for Horizon management; port 443 on CS                                        │
│  Events tab    = Horizon UI event log; filter by error/warning                                        │
│  UAG admin     = port 9443; cert, edge service, health config                                         │
│  /rest/healthcheck= UAG health endpoint; returns 200 OK if healthy                                    │
│  UAG log       = /opt/vmware/etc/esmanager/; edge service logs                                        │
│  Windows App log= Windows Event Viewer; Horizon Agent events here                                     │
│  Pool error    = UI shows red error; hover for provisioning reason                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Windows Event Log (Connection Server)

```powershell
# Horizon-specific event sources:
Get-WinEvent -LogName "Application" -MaxEvents 50 | 
  Where-Object { $_.ProviderName -like "*VMware*" } |
  Select-Object TimeCreated, LevelDisplayName, Message

# VMware Horizon LDAP service (ADAM/AD LDS) errors:
Get-WinEvent -LogName "ADAM (VMwareVDMDS)" -MaxEvents 20
```

---

## Horizon Agent Logs in Guest VM

```powershell
# Inside the desktop VM:
C:\ProgramData\VMware\VDM\logs\

# Or via Event Viewer in the guest:
Get-WinEvent -LogName "Application" -ComputerName <desktop-vm-ip> |
  Where-Object { $_.ProviderName -like "*Horizon*" -or $_.ProviderName -like "*VMware*" } |
  Select-Object -First 20

# Check Horizon Agent service
Get-Service -ComputerName <desktop-vm-ip> -Name "VMware Horizon View Agent"
```

---

## UAG Log Collection

```bash
# SSH to UAG appliance
ssh root@uag.example.local

# Log locations:
/opt/vmware/gateway/logs/esmanager.log    # Edge Service Manager
/opt/vmware/gateway/logs/gateway.log      # Main gateway log
/var/log/messages                          # OS syslog

# Collect UAG log bundle via REST API:
curl -sk -X GET "https://uag.example.local:9443/rest/v1/config/logs/collect" \
  -u admin:<password> -o uag-logs-$(date +%Y%m%d).zip
```

---

## Test Display Protocol Connectivity

```bash
# From a client machine — test Blast port:
nc -vz uag.example.local 8443

# Test PCoIP:
nc -vz uag.example.local 4172

# Test HTTPS tunnel:
nc -vz uag.example.local 443

# Trace the path to UAG:
traceroute uag.example.local
```

---

## Session Diagnostics with vdmadmin

```powershell
# vdmadmin.exe is in C:\Program Files\VMware\VMware View\Server\tools\bin\

# List active sessions
& "C:\Program Files\VMware\VMware View\Server\tools\bin\vdmadmin.exe" -L -d <pool-name>

# List user assignments
& "vdmadmin.exe" -A -d <pool-name> -list

# List all Connection Servers
& "vdmadmin.exe" -S -list
```

---

## Horizon REST API Diagnostics

```bash
# Authenticate to Horizon REST API
TOKEN=$(curl -sk -X POST https://horizon-cs01.example.local/rest/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","domain":"corp"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('access_token',''))")

# Get Connection Server health
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://horizon-cs01.example.local/rest/monitor/connection-servers | python3 -m json.tool

# Get pool summary
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://horizon-cs01.example.local/rest/inventory/v1/desktop-pools | python3 -m json.tool
```

---

## Horizon Performance Tracker

For diagnosing in-session performance (latency, frame rate, bandwidth):

```text
Inside a Blast session: Ctrl+Alt+Shift+P → opens Performance Tracker overlay
Displays: frames per second, bandwidth, latency, packet loss
```

High latency (>50ms) → check network path between client and UAG, or UAG and desktop.
Low frame rate → check vGPU allocation, ESXi CPU contention, or display protocol settings.
