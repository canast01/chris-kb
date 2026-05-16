# Horizon — Diagnostics

---

## Connection Server Log Location

```powershell
# Primary log directory:
C:\ProgramData\VMware\VDM\logs\

# Key log files:
debug-<date>.txt    # Main debug log — verbose, includes all events
audit-<date>.txt    # Admin and user audit events
ws_tomcat-<date>.txt # Web service (Horizon console) log

# Follow live log output (PowerShell):
Get-Content "C:\ProgramData\VMware\VDM\logs\debug-2024-01-01.txt" -Wait -Tail 50
```

---

## Collect Horizon Support Bundle

```
Horizon Console → Help → Download Support Bundle
  Selects logs from all Connection Servers in the pod
  Downloads as ZIP — attach to VMware Support case
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
ssh root@uag.corp.local

# Log locations:
/opt/vmware/gateway/logs/esmanager.log    # Edge Service Manager
/opt/vmware/gateway/logs/gateway.log      # Main gateway log
/var/log/messages                          # OS syslog

# Collect UAG log bundle via REST API:
curl -sk -X GET "https://uag.corp.local:9443/rest/v1/config/logs/collect" \
  -u admin:<password> -o uag-logs-$(date +%Y%m%d).zip
```

---

## Test Display Protocol Connectivity

```bash
# From a client machine — test Blast port:
nc -vz uag.corp.local 8443

# Test PCoIP:
nc -vz uag.corp.local 4172

# Test HTTPS tunnel:
nc -vz uag.corp.local 443

# Trace the path to UAG:
traceroute uag.corp.local
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
TOKEN=$(curl -sk -X POST https://horizon-cs01.corp.local/rest/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","domain":"corp"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('access_token',''))")

# Get Connection Server health
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://horizon-cs01.corp.local/rest/monitor/connection-servers | python3 -m json.tool

# Get pool summary
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://horizon-cs01.corp.local/rest/inventory/v1/desktop-pools | python3 -m json.tool
```

---

## Horizon Performance Tracker

For diagnosing in-session performance (latency, frame rate, bandwidth):

```
Inside a Blast session: Ctrl+Alt+Shift+P → opens Performance Tracker overlay
Displays: frames per second, bandwidth, latency, packet loss
```

High latency (>50ms) → check network path between client and UAG, or UAG and desktop.
Low frame rate → check vGPU allocation, ESXi CPU contention, or display protocol settings.
