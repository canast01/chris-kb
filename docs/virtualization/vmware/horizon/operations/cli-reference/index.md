# Horizon — CLI Reference


<div class="kb-summary">
CLI Reference reference covering Session Management, vdmexport / vdmimport, UAG CLI (hzedge), PowerShell — VMware.Hv.Helper, Horizon REST API.
</div>

  Horizon CLI Tools
```powershell
┌──────────────────────────────────────────────────────────────────┐
│  vdmadmin.exe          │  vdmexport / vdmimport                  │
│  ┌────────────────┐    │  ┌──────────────────────────────────┐   │
│  │ -L -sessions   │    │  │ vdmexport -f backup.ldif         │   │
│  │ -L -pools      │    │  │ vdmimport -f backup.ldif         │   │
│  │ -L -servers    │    │  └──────────────────────────────────┘   │
│  │ -D -m <vm>     │    │                                         │
│  └────────────────┘    │  hzedge (UAG shell)                     │
│                        │  ┌──────────────────────────────────┐   │
│  VMware.Hv.Helper      │  │ hzedge gethealth                 │   │
│  ┌────────────────┐    │  │ hzedge getblast / getpcoip       │   │
│  │ Connect-HVServer│   │  └──────────────────────────────────┘   │
│  │ Get-HVPool      │   │                                         │
│  │ Get-HVSession   │   │  Horizon REST API                       │
│  │ Get-HVMachine   │   │  ┌──────────────────────────────────┐   │
│  └────────────────┘    │  │ POST /rest/login → Bearer token  │   │
│                        │  │ GET  /rest/inventory/v1/sessions  │   │
└───────────────────────────┴──────────────────────────────────────┘
```
┌─────────────────────────────────── VMware Horizon — CLI Reference ────────────────────────────────────┐
│                                                                                                       │
│  Horizon CLI tools: vdmadmin.exe on Connection Server, PowerCLI Horizon module,                       │
│  and the Horizon REST API for automation.                                                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              vdmadmin Commands               │  │               Horizon REST API              │   │
│   │         vdmadmin -L (list sessions)          │  │               POST /rest/login              │   │
│   │           vdmadmin -Q (kiosk mode)           │  │         GET /rest/inventory/v1/farms        │   │
│   │          vdmadmin -A (agent config)          │  │         GET /rest/inventory/v1/pools        │   │
│   │            vdmexport / vdmimport             │  │          DELETE /rest/sessions/{id}         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  vdmadmin runs on Connection Server; REST API requires Horizon admin credentials.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               PowerCLI Horizon               │  │            Desktop & Session Ops            │   │
│   │         Connect-HVServer -Server cs          │  │             Send-HVDesktopReboot            │   │
│   │           Get-HVPool (list pools)            │  │             Disconnect-HVSession            │   │
│   │        Get-HVMachine (list desktops)         │  │              Set-HVPool -Enable             │   │
│   │        Get-HVLocalSession (sessions)         │  │               Remove-HVMachine              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vdmadmin runs locally on Connection Server; PowerCLI connects from jump host;                        │
│  REST API accessible on Connection Server port 443.                                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vdmadmin      = Horizon admin CLI; Windows .exe on Connection Server                                 │
│  vdmexport     = export Horizon LDAP config to backup file                                            │
│  vdmimport     = import Horizon LDAP config from backup file                                          │
│  Connect-HVServer= PowerCLI; connect to Horizon Connection Server                                     │
│  Get-HVPool    = PowerCLI; list all Horizon desktop/app pools                                         │
│  Get-HVMachine = PowerCLI; list desktop VM status                                                     │
│  REST API      = Horizon REST API; JSON; bearer token auth                                            │
│  POST /rest/login= obtain session token for REST API                                                  │
│  DELETE /rest/sessions= force disconnect a Horizon session                                            │
│  Kiosk mode    = shared desktop mode; no user AD account needed                                       │
│  Agent config  = configure Horizon Agent on desktop VM via vdmadmin                                   │
│  Remove-HVMachine= PowerCLI; remove a desktop VM from pool                                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

### Desktop and Pool Operations

```cmd
:: List all pools
vdmadmin.exe -L -pools

:: List all desktops in a pool
vdmadmin.exe -L -desktops -poolid LON-KW-W11-IC

:: List desktops in error state
vdmadmin.exe -L -desktops -poolid LON-KW-W11-IC | findstr /i "error"

:: Reset a specific desktop (hard reset)
vdmadmin.exe -D -m <machine-name>

:: Remove a desktop from a pool (deletes the VM)
vdmadmin.exe -D -m <machine-name> -delete
```

### Entitlement Management

```cmd
:: List entitlements for a pool
vdmadmin.exe -L -entitlements -poolid LON-KW-W11-IC

:: Add AD group entitlement to a pool
vdmadmin.exe -A -entitlement -group "CN=VDI-LON-KW-Users,OU=Groups,DC=corp,DC=example,DC=com" -poolid LON-KW-W11-IC

:: Remove entitlement
vdmadmin.exe -R -entitlement -group "CN=VDI-LON-KW-Users,OU=Groups,DC=corp,DC=example,DC=com" -poolid LON-KW-W11-IC
```

### User Operations

```cmd
:: List assigned desktops for a user (Full Clone or persistent assignment)
vdmadmin.exe -L -assignments -u domain\username

:: Release a persistent desktop assignment (frees desktop for another user)
vdmadmin.exe -A -release -u domain\username -poolid LON-PW-W11-FC

:: Unlock a user account locked by too many failed logon attempts
vdmadmin.exe -N -unlock -u domain\username
```

### Connection Server Management

```cmd
:: List all Connection Servers in the pod
vdmadmin.exe -L -servers

:: Show Connection Server status and health
vdmadmin.exe -L -servers -verbose

:: List events from a Connection Server
vdmadmin.exe -L -events -n 100

:: List events filtered by severity
vdmadmin.exe -L -events -severity ERROR -n 50
```

---

## vdmexport / vdmimport

These tools back up and restore the Connection Server LDAP configuration.

```cmd
:: Export (backup)
cd "C:\Program Files\VMware\VMware View\Server\tools\bin"

vdmexport.exe -f C:\Backups\cs-config-backup.ldif

:: Export verbose — shows what is being exported
vdmexport.exe -f C:\Backups\cs-config-backup.ldif -v

:: Import (restore) — overwrites existing config
vdmimport.exe -f C:\Backups\cs-config-backup.ldif

:: Import with update (doesn't fail on existing entries)
vdmimport.exe -f C:\Backups\cs-config-backup.ldif -u

:: Import verbose
vdmimport.exe -f C:\Backups\cs-config-backup.ldif -v
```

---

## UAG CLI (hzedge)

UAG is a Linux appliance — SSH access is available if enabled at deploy time. The `hzedge` command provides health and configuration queries.

```bash
# SSH to UAG
ssh admin@uag-prod-01.corp.example.com

# Check overall UAG health
hzedge gethealth

# Check Horizon Edge service status
hzedge getedgeconfigsummary

# List configured services (Horizon, reverse proxy, etc.)
hzedge getservices

# Check Blast Extreme gateway status
hzedge getblast

# Check PCoIP gateway status
hzedge getpcoip

# Check tunnel status
hzedge gettunnel

# View current authenticated sessions count
hzedge getsessioninfo
```

### UAG REST API (health check endpoint)

```bash
# From any machine — no authentication required for health endpoint
curl -sk https://uag-prod-01.corp.example.com/favicon.ico -o /dev/null -w "%{http_code}"
# Expect: 200

# Full UAG REST API health check (requires admin credentials)
curl -sk -u admin:<password> https://uag-prod-01.corp.example.com:9443/rest/v1/monitor/stats
```

---

## PowerShell — VMware.Hv.Helper

`VMware.Hv.Helper` is the Horizon PowerShell module (community + VMware module). Install via PowerShell Gallery or from Horizon install media.

```powershell
# Install from PowerShell Gallery
Install-Module VMware.PowerCLI -Scope CurrentUser
Install-Module VMware.Hv.Helper -Scope CurrentUser

# Or import from local path (Horizon install media)
Import-Module "C:\Horizon\PowerShell\VMware.Hv.Helper.psm1"
```

### Connect to Horizon

```powershell
# Connect using Horizon REST or ADAM service
$cs = "cs01.corp.example.com"
$cred = Get-Credential  # Horizon Administrator account

Connect-HVServer -Server $cs -Credential $cred
```

### Pool Operations

```powershell
# List all pools
Get-HVPool

# Get specific pool details
Get-HVPool -PoolName "LON-KW-W11-IC"

# List pools with session counts
Get-HVPool | Select-Object @{N="Pool";E={$_.Base.Name}},
  @{N="Enabled";E={$_.Base.Enabled}},
  @{N="Type";E={$_.Type}}

# Disable a pool (stops new sessions)
Set-HVPool -PoolName "LON-KW-W11-IC" -Enable $false

# Enable a pool
Set-HVPool -PoolName "LON-KW-W11-IC" -Enable $true

# Get pool provisioning settings
(Get-HVPool -PoolName "LON-KW-W11-IC").AutomatedDesktopData.VmNamingSettings
```

### Desktop Operations

```powershell
# List all desktops in a pool
Get-HVMachine -PoolName "LON-KW-W11-IC"

# List desktops in ERROR state
Get-HVMachine -PoolName "LON-KW-W11-IC" | Where-Object { $_.Base.BasicState -eq "ERROR" }

# Get desktop by name
Get-HVMachine -MachineName "LON-KW-001"

# Reset a desktop (power reset)
$machine = Get-HVMachine -MachineName "LON-KW-001"
Reset-HVMachine -MachineId $machine.Id

# Delete a desktop from pool (and delete VM)
Remove-HVMachine -MachineId $machine.Id -DeleteFromDisk $true
```

### Session Operations

```powershell
# List all active sessions
Get-HVSession

# List sessions for a specific user
Get-HVSession | Where-Object { $_.NamesData.UserName -eq "CORP\jsmith" }

# List sessions in a specific pool
Get-HVSession | Where-Object { $_.NamesData.DesktopName -eq "LON-KW-W11-IC" }

# List disconnected sessions
Get-HVSession | Where-Object { $_.SessionData.SessionState -eq "DISCONNECTED" }

# Force logoff a session
$session = Get-HVSession | Where-Object { $_.NamesData.UserName -eq "CORP\jsmith" }
Send-HVSessionLogoff -HvSession $session

# Logoff all disconnected sessions older than 2 hours
$cutoff = (Get-Date).AddHours(-2)
Get-HVSession | Where-Object {
  $_.SessionData.SessionState -eq "DISCONNECTED" -and
  $_.SessionData.DisconnectTime -lt $cutoff
} | ForEach-Object { Send-HVSessionLogoff -HvSession $_ }

# Send message to all users in a pool
Get-HVSession | Where-Object { $_.NamesData.DesktopName -eq "LON-KW-W11-IC" } |
  ForEach-Object { Send-HVSessionMessage -HvSession $_ -MessageText "Maintenance in 30 minutes" -MessageType WARNING }
```

---

## Horizon REST API

Horizon exposes a REST API on each Connection Server. Authentication returns a JWT token used in subsequent calls.

**Base URL:** `https://<connection-server>/rest/`

### Authenticate

```powershell
$csUrl = "https://cs01.corp.example.com"
$body = @{
  username = "horizon-admin"
  password = "P@ssword123"
  domain   = "corp"
} | ConvertTo-Json

$authResponse = Invoke-RestMethod -Uri "$csUrl/rest/login" `
  -Method POST -Body $body -ContentType "application/json"

$token = $authResponse.access_token
$headers = @{ Authorization = "Bearer $token" }
```

### List Pools

```powershell
$pools = Invoke-RestMethod -Uri "$csUrl/rest/inventory/v1/desktop-pools" `
  -Method GET -Headers $headers

$pools | Select-Object id, display_name, type, enabled | Format-Table
```

### List Sessions

```powershell
$sessions = Invoke-RestMethod -Uri "$csUrl/rest/inventory/v1/sessions" `
  -Method GET -Headers $headers

$sessions | Select-Object id,
  @{N="User";E={$_.user_name}},
  @{N="Desktop";E={$_.machine_name}},
  @{N="State";E={$_.session_state}} | Format-Table
```

### Force Logoff via REST

```powershell
# Single session logoff
$sessionId = "session-id-from-list"
Invoke-RestMethod -Uri "$csUrl/rest/inventory/v1/sessions/$sessionId/action/logoff" `
  -Method POST -Headers $headers

# Bulk logoff (POST array of session IDs)
$body = @($sessionId1, $sessionId2) | ConvertTo-Json
Invoke-RestMethod -Uri "$csUrl/rest/inventory/v1/sessions/action/logoff" `
  -Method POST -Headers $headers -Body $body -ContentType "application/json"
```

### Rebalance Instant Clone Pool

```powershell
# Trigger a rebalance of Instant Clone desktops across datastores
$poolId = "pool-id-from-list"
Invoke-RestMethod -Uri "$csUrl/rest/inventory/v1/desktop-pools/$poolId/action/rebalance" `
  -Method POST -Headers $headers
```

### Refresh Pool (Push New Image)

```powershell
# Refresh all Instant Clone desktops — they will refresh on next logoff
$body = @{
  logoff_policy = "FORCE_LOGOFF_AFTER_TIMEOUT"
  stop_on_first_error = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "$csUrl/rest/inventory/v1/desktop-pools/$poolId/action/refresh" `
  -Method POST -Headers $headers -Body $body -ContentType "application/json"
```

### List Farms (RDS)

```powershell
$farms = Invoke-RestMethod -Uri "$csUrl/rest/inventory/v1/farms" `
  -Method GET -Headers $headers

$farms | Select-Object id, display_name, type, enabled | Format-Table
```

### Get Desktop Machine State

```powershell
# Get all machines in a pool with their state
$machines = Invoke-RestMethod -Uri "$csUrl/rest/inventory/v1/machines?desktop_pool_id=$poolId" `
  -Method GET -Headers $headers

$machines | Group-Object -Property basic_state | Select-Object Name, Count | Format-Table
```
