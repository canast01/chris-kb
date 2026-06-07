# Horizon — Procedures


<div class="kb-summary">
Procedures reference covering Entitle an AD Group to a Pool, Push a Golden Image Update to an Instant Clone Pool, Add a New Connection Server Replica, Configure UAG for External Access, Enable True SSO and 4 more sections.
</div>

  Common Operational Procedures
```text
┌───────────────────────────────── VMware Horizon — Common Procedures ──────────────────────────────────┐
│                                                                                                       │
│  Common Horizon procedures: update golden image, push to pool, manage sessions,                       │
│  entitle users, and maintain certificates on Connection Servers.                                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Golden Image Update              │  │              Session Management             │   │
│   │          Power off, snapshot parent          │  │            Logoff: force if stuck           │   │
│   │             Install patches/apps             │  │            Reset: restart desktop           │   │
│   │            Snapshot: new version             │  │             Send message to user            │   │
│   │        Push scheduled via Horizon UI         │  │          Disable: maintenance mode          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Golden image update is the most frequent Horizon maintenance task; schedule off-hours.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Entitlements & Certs             │  │               Pool Maintenance              │   │
│   │          Add entitlement: AD group           │  │          Pool in maintenance: drain         │   │
│   │           Remove: revoke from pool           │  │            Delete stuck VM: force           │   │
│   │         Cert: replace on CS via MMC          │  │         Add machines: increase pool         │   │
│   │          vdmadmin: reset passwords           │  │         Disable provisioning: pause         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Golden image updates temporarily reduce pool availability; schedule maintenance windows;             │
│  certificate replacement requires IIS restart on Connection Server.                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Golden image  = parent VM for instant clone pools                                                    │
│  Push          = schedule pool to use new parent snapshot                                             │
│  Maintenance mode= pool unavailable; existing sessions continue                                       │
│  Entitlement   = AD user or group assigned to a pool                                                  │
│  Revoke        = remove AD group/user entitlement from pool                                           │
│  MMC           = Microsoft Management Console; cert store on Windows                                  │
│  IIS restart   = required after cert replacement on CS                                                │
│  Force delete  = remove stuck VM from pool that failed to provision                                   │
│  Send message  = warn users before forced logoff/pool push                                            │
│  Pool size     = min/max/spare desktops; tuned for peak usage                                         │
│  Drain         = wait for sessions to end before pool action                                          │
│  Provisioning  = Horizon auto-creates VMs to fill pool spare count                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────── VMware Horizon — Common Procedures ──────────────────────────────────┐
│                                                                                                       │
│  Common Horizon procedures: update golden image, push to pool, manage sessions,                       │
│  entitle users, and maintain certificates on Connection Servers.                                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Golden Image Update              │  │              Session Management             │   │
│   │          Power off, snapshot parent          │  │            Logoff: force if stuck           │   │
│   │             Install patches/apps             │  │            Reset: restart desktop           │   │
│   │            Snapshot: new version             │  │             Send message to user            │   │
│   │        Push scheduled via Horizon UI         │  │          Disable: maintenance mode          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Golden image update is the most frequent Horizon maintenance task; schedule off-hours.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Entitlements & Certs             │  │               Pool Maintenance              │   │
│   │          Add entitlement: AD group           │  │          Pool in maintenance: drain         │   │
│   │           Remove: revoke from pool           │  │            Delete stuck VM: force           │   │
│   │         Cert: replace on CS via MMC          │  │         Add machines: increase pool         │   │
│   │          vdmadmin: reset passwords           │  │         Disable provisioning: pause         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Golden image updates temporarily reduce pool availability; schedule maintenance windows;             │
│  certificate replacement requires IIS restart on Connection Server.                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Golden image  = parent VM for instant clone pools                                                    │
│  Push          = schedule pool to use new parent snapshot                                             │
│  Maintenance mode= pool unavailable; existing sessions continue                                       │
│  Entitlement   = AD user or group assigned to a pool                                                  │
│  Revoke        = remove AD group/user entitlement from pool                                           │
│  MMC           = Microsoft Management Console; cert store on Windows                                  │
│  IIS restart   = required after cert replacement on CS                                                │
│  Force delete  = remove stuck VM from pool that failed to provision                                   │
│  Send message  = warn users before forced logoff/pool push                                            │
│  Pool size     = min/max/spare desktops; tuned for peak usage                                         │
│  Drain         = wait for sessions to end before pool action                                          │
│  Provisioning  = Horizon auto-creates VMs to fill pool spare count                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
ool] → Entitlements → Add** — add AD groups

```powershell
# Verify pool provisioning status via PowerCLI
Connect-HVServer -Server horizon-cs-01.corp.local -Credential (Get-Credential)
Get-HVPool -PoolName "pool-ic-win11" | Select-Object -ExpandProperty AutomatedDesktopData |
  Select-Object MinimumCount, MaximumCount, SpareCount
Get-HVMachine -PoolName "pool-ic-win11" | Group-Object State | Select-Object Name, Count
```

## Create an RDS Farm and Application Pool

RDS farms deliver published desktops and RemoteApp applications from Windows Server RDSH hosts.

```powershell
# 1. Verify Horizon Agent with RDS role is installed on RDSH hosts
Get-HVFarm | Where-Object { $_.Type -eq "AUTOMATED" }

# 2. Create a manual RDS farm (add existing RDSH servers)
# Horizon Console → Farm → Add → Manual Farm
# Add RDSH hosts by FQDN — Horizon registers them as RDS hosts

# 3. Create an Application Pool from the farm
# Horizon Console → Catalog → Application Pools → Add
# Select farm, browse installed applications, publish selected apps

# 4. Verify farm health
Get-HVFarm -FarmName "farm-rdsh-apps" | Select-Object -ExpandProperty RDSFarmSummaryData
Get-HVFarmHealth -FarmName "farm-rdsh-apps"
```

RDSH hosts must have at least 1 licensed RDS CAL per concurrent user. Check licensing via `licmgr.exe` on a host.

## Add or Remove User Entitlement from a Pool

```powershell
Connect-HVServer -Server horizon-cs-01.corp.local -Credential (Get-Credential)

# Add an AD group entitlement to a pool
$pool = Get-HVPool -PoolName "pool-ic-win11"
$group = Get-HVQueryResult -EntityType ADUserOrGroupSummaryView |
  Where-Object { $_.Base.Name -eq "VDI-Users" }
New-HVEntitlement -ResourceType Desktop -ResourceId $pool.Id -UserOrGroupId $group.Id

# Remove an entitlement
$entitlement = Get-HVEntitlement -ResourceType Desktop -ResourceName "pool-ic-win11" |
  Where-Object { $_.UserOrGroupData.Name -eq "VDI-Users" }
Remove-HVEntitlement -Id $entitlement.Id

# List all entitlements for a pool
Get-HVEntitlement -ResourceType Desktop -ResourceName "pool-ic-win11" |
  Select-Object { $_.UserOrGroupData.Name }, { $_.UserOrGroupData.GroupMembershipCount }
```

## Force Logoff or Reset a User Session

```powershell
Connect-HVServer -Server horizon-cs-01.corp.local -Credential (Get-Credential)

# Find active sessions for a user
Get-HVLocalSession | Where-Object { $_.NamesData.UserName -eq "jsmith" } |
  Select-Object Id, @{N='Desktop';E={$_.NamesData.MachineOrRDSServerDNS}}, SessionState

# Force logoff a specific session
Get-HVLocalSession | Where-Object { $_.NamesData.UserName -eq "jsmith" } |
  Invoke-HVSessionLogoff

# Reset (hard reboot) a stuck desktop
Get-HVMachine -MachineName "ic-win11-0042" | Reset-HVMachine

# Disconnect without logoff (session persists, user can reconnect)
Get-HVLocalSession | Where-Object { $_.NamesData.UserName -eq "jsmith" } |
  Invoke-HVSessionDisconnect
```

## Recompose an Instant Clone Pool

Recompose pushes a new golden image snapshot to all desktops in the pool. Sessions are terminated; desktops are rebuilt from the new parent.

```powershell
Connect-HVServer -Server horizon-cs-01.corp.local -Credential (Get-Credential)

# 1. Confirm new snapshot exists on the parent VM
Get-VM "GoldenImage-Win11" | Get-Snapshot | Select-Object Name, Created

# 2. Initiate recompose (schedule for maintenance window)
$pool = Get-HVPool -PoolName "pool-ic-win11"
$snapshot = Get-HVQueryResult -EntityType BaseImageSnapshotInfo |
  Where-Object { $_.Name -eq "Snap-2026-06-Win11-Patched" }

# Recompose immediately (use -ScheduleTime for deferred)
Update-HVPool -PoolId $pool.Id -ParentVMPath $snapshot.Path -SnapshotPath $snapshot.SnapshotPath

# 3. Monitor progress
Get-HVMachine -PoolName "pool-ic-win11" | Group-Object State | Select-Object Name, Count
# States cycle: Maintenance → Deleting → Provisioning → Available
```

## Renew Certificate on Connection Servers

Horizon Connection Servers use TLS certificates for client connections and inter-component trust.

```powershell
# 1. Import new certificate into the Windows certificate store on each CS
# Run on each Connection Server:
Import-PfxCertificate -FilePath "C:\certs\horizon-cs.pfx" `
  -CertStoreLocation "Cert:\LocalMachine\My" `
  -Password (ConvertTo-SecureString "pfx-password" -AsPlainText -Force)

# 2. Find the certificate thumbprint
Get-ChildItem "Cert:\LocalMachine\My" | Where-Object { $_.Subject -match "horizon-cs" } |
  Select-Object Subject, Thumbprint, NotAfter

# 3. Set the Horizon vdm alias to use the new certificate
# Run in elevated cmd on each CS:
# certutil -repairstore My "<thumbprint>"

# 4. Restart the VMware Horizon View Connection Server service
Restart-Service -Name "WSNM" -Force
# Service name may also be "wsbroker" depending on Horizon version

# 5. Verify from a Horizon Client — confirm certificate CN and expiry match new cert
# Horizon Console → Settings → Servers → Connection Servers → [server] → Certificate
```

Repeat on all Connection Servers and Replica Servers before the old certificate expires.

## Configure Horizon Event Database

The event database records audit, session, and error events for reporting and compliance.

```sql
-- Create a dedicated database on SQL Server or PostgreSQL
-- SQL Server:
CREATE DATABASE HorizonEvents;
CREATE LOGIN horizon_event_user WITH PASSWORD = 'StrongP@ss1';
USE HorizonEvents;
CREATE USER horizon_event_user FOR LOGIN horizon_event_user;
ALTER ROLE db_owner ADD MEMBER horizon_event_user;
```

```powershell
# Configure in Horizon Console:
# Settings → Event Configuration → Event Database
# Type: Microsoft SQL Server (or PostgreSQL)
# Server: <db-server-fqdn>
# Port: 1433
# Database: HorizonEvents
# User: horizon_event_user
# Table prefix: hv_ (optional, allows sharing one DB for multiple pods)

# Verify events are flowing — check after any user session:
# Reports → Events → Recent Events should show session events
```

Event data is retained per the configured purge schedule (default 30 days). Increase for compliance requirements.
