# Horizon — Health Checks


<div class="kb-summary">
Health Checks reference covering Desktop Pool Health, Active Session Count vs License, UAG Health Check, App Volumes Manager Health, DEM Share Accessibility and 3 more sections.
</div>

  Health Check Chain
```text
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Connection      │    │  Composer /      │    │  vCenter                                              │
│  Servers         │───►│  App Volumes Mgr │───►│  (pool/datastore                                      │
│  (all green?)    │    │  (healthy?)      │    │   capacity?)                                          │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```
┌─────────────────────────────────── VMware Horizon — Health Checks ────────────────────────────────────┐
│                                                                                                       │
│  Horizon health checks verify Connection Server status, pool availability, agent                      │
│  health, UAG connectivity, and session counts against licensed capacity.                              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Connection Server Health           │  │                 Pool Health                 │   │
│   │           All CS: Connected status           │  │           Available desktops count          │   │
│   │          AD: reachable from all CS           │  │            No pool in error state           │   │
│   │           Cert: not expired on CS            │  │          Provisioning: no stuck VMs         │   │
│   │         Services: all running on CS          │  │          vCenter: connected to pool         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  CS status and pool availability are the primary daily health indicators.                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             UAG & Session Health             │  │            Capacity & Performance           │   │
│   │         UAG: reachable from external         │  │          Sessions < licensed limit          │   │
│   │          UAG: health endpoint green          │  │             Blast latency <50ms             │   │
│   │        Active sessions: normal range         │  │           vCPU/RAM: no contention           │   │
│   │           Abandoned sessions: none           │  │          Disk IOPS: within baseline         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Connection Servers and UAGs are VMs; desktop VMs on ESXi cluster; monitor                            │
│  ESXi host resource utilisation to predict capacity for new sessions.                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CS Connected  = Connection Server can reach LDAP and vCenter                                         │
│  UAG health    = REST endpoint /rest/healthcheck on UAG port 443                                      │
│  Pool error    = pool stuck in provisioning, error, or maintenance                                    │
│  Available count= desktops ready for session assignment                                               │
│  Blast latency = display protocol round-trip; <50ms = good UX                                         │
│  Abandoned     = session disconnected without logout; wasted license                                  │
│  Licensed limit= concurrent sessions allowed by Horizon licence                                       │
│  Provisioning stuck= instant clone VM not completing creation                                         │
│  vCenter link  = Connection Server must reach vCenter for pool management                             │
│  AD reachable  = Connection Server must reach AD for user authentication                              │
│  Cert expiry   = expired cert causes browser login failures                                           │
│  Session count = active + disconnected; both consume licence                                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
         │
         ▼
```text
```
┌──────────────────┐
│  Desktop Pools                                                                                        │
│  (Available > 0,                                                                                      │
│   Error = 0?)                                                                                         │
└──────────────────┘
```text
┌─────────────────────────────────── VMware Horizon — Health Checks ────────────────────────────────────┐
│                                                                                                       │
│  Horizon health checks verify Connection Server status, pool availability, agent                      │
│  health, UAG connectivity, and session counts against licensed capacity.                              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Connection Server Health           │  │                 Pool Health                 │   │
│   │           All CS: Connected status           │  │           Available desktops count          │   │
│   │          AD: reachable from all CS           │  │            No pool in error state           │   │
│   │           Cert: not expired on CS            │  │          Provisioning: no stuck VMs         │   │
│   │         Services: all running on CS          │  │          vCenter: connected to pool         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  CS status and pool availability are the primary daily health indicators.                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             UAG & Session Health             │  │            Capacity & Performance           │   │
│   │         UAG: reachable from external         │  │          Sessions < licensed limit          │   │
│   │          UAG: health endpoint green          │  │             Blast latency <50ms             │   │
│   │        Active sessions: normal range         │  │           vCPU/RAM: no contention           │   │
│   │           Abandoned sessions: none           │  │          Disk IOPS: within baseline         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Connection Servers and UAGs are VMs; desktop VMs on ESXi cluster; monitor                            │
│  ESXi host resource utilisation to predict capacity for new sessions.                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CS Connected  = Connection Server can reach LDAP and vCenter                                         │
│  UAG health    = REST endpoint /rest/healthcheck on UAG port 443                                      │
│  Pool error    = pool stuck in provisioning, error, or maintenance                                    │
│  Available count= desktops ready for session assignment                                               │
│  Blast latency = display protocol round-trip; <50ms = good UX                                         │
│  Abandoned     = session disconnected without logout; wasted license                                  │
│  Licensed limit= concurrent sessions allowed by Horizon licence                                       │
│  Provisioning stuck= instant clone VM not completing creation                                         │
│  vCenter link  = Connection Server must reach vCenter for pool management                             │
│  AD reachable  = Connection Server must reach AD for user authentication                              │
│  Cert expiry   = expired cert causes browser login failures                                           │
│  Session count = active + disconnected; both consume licence                                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Acceptable ratio: Available desktops should be ≥ 10% of pool size to handle burst demand.

---

## Active Session Count vs License

```powershell
# Using VMware.Hv.Helper PowerShell module
Connect-HVServer -Server horizon-cs01.example.local -Credential (Get-Credential)

# Get current active session count
$sessions = Get-HVLocalSession
Write-Host "Active sessions: $($sessions.Count)"

# Get licensed session count from License page
# Horizon Console → Settings → Product Licensing and Usage
```

---

## UAG Health Check

```bash
# UAG exposes a health API endpoint
curl -sk https://uag.example.local/favicon.ico  # should return 200
curl -sk https://uag.example.local:9443/rest/v1/monitor/health \
  -u admin:<password> | python3 -m json.tool
# Look for "RUNNING" status on all services

# Test Blast gateway reachability from external network
# Blast: TCP 8443 (HTTPS)
# PCoIP: TCP/UDP 4172
nc -vz uag.example.local 8443
nc -vz uag.example.local 4172
```

---

## App Volumes Manager Health

```text
App Volumes Manager UI → Activity → Current Activity
  No stuck attachments or detachments
App Volumes Manager UI → Infrastructure → Managers
  All managers show Healthy
```

```bash
# Test App Volumes Manager API
curl -sk https://appvol-mgr.example.local/cv_api/status
```

---

## DEM Share Accessibility

Dynamic Environment Manager reads GPO config from a UNC share. Verify accessibility:

```powershell
# On a desktop VM or Connection Server:
Test-Path "\\fileserver.example.local\DEM-Config\General"
# Should return True

# Check DEM Agent service in a desktop VM
Get-Service -ComputerName <desktop-vm> -Name "User Environment Manager Agent"
```

---

## Certificate Expiry

```bash
# Check Connection Server SSL certificate
echo | openssl s_client -connect horizon-cs01.example.local:443 -servername horizon-cs01.example.local 2>/dev/null \
  | openssl x509 -noout -dates

# Check UAG certificate
echo | openssl s_client -connect uag.example.local:443 -servername uag.example.local 2>/dev/null \
  | openssl x509 -noout -dates

# Check UAG Blast gateway cert (port 8443)
echo | openssl s_client -connect uag.example.local:8443 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## Check for Provisioning Errors

```powershell
Connect-HVServer -Server horizon-cs01.example.local -Credential (Get-Credential)

# Get desktops in error state
Get-HVDesktop | Where-Object { $_.Base.BasicState -eq "ERROR" } | 
  Select-Object -ExpandProperty Base | 
  Select-Object Name, BasicState, DesktopSummaryData

# Delete error-state desktops (they will be reprovisioned automatically)
Get-HVDesktop | Where-Object { $_.Base.BasicState -eq "ERROR" } |
  Remove-HVDesktop -Confirm:$false
```

---

## Verify External Access (Blast/PCoIP)

From an external network (outside the corporate LAN):

```bash
# Blast Extreme — TCP 8443 to UAG
nc -vz uag.public.corp.com 8443

# PCoIP — TCP 4172 and UDP 4172 to UAG
nc -vz uag.public.corp.com 4172

# HTTPS Tunnel — TCP 443 to UAG
nc -vz uag.public.corp.com 443
```

If any port is blocked, check the perimeter firewall rules for UAG external interface.
