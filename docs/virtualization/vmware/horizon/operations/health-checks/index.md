# Horizon — Health Checks

```
  Health Check Chain
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Connection      │    │  Composer /      │    │  vCenter         │
│  Servers         │───►│  App Volumes Mgr │───►│  (pool/datastore │
│  (all green?)    │    │  (healthy?)      │    │   capacity?)      │
└──────────────────┘    └──────────────────┘    └──────────────────┘
         │                                                │
         ▼                                                ▼
┌──────────────────┐                         ┌──────────────────┐
│  UAG             │                         │  Active Directory   │
│  (port 443/8443  │                         │  (LDAP/Kerberos     │
│   reachable?)    │                         │   connectivity?)    │
└──────────────────┘                         └──────────────────┘
         │
         ▼
┌──────────────────┐
│  Desktop Pools                                                   │
│  (Available > 0,                                                 │
│   Error = 0?)                                                    │
└──────────────────┘
```

---

## Connection Server Dashboard

```
Horizon Console → Dashboard → Summary
  Global health indicator: Green = all services healthy
  vCenter connection: should show Connected
  Composer: Connected (if using Linked Clones — not needed for Instant Clone)
  Pod status: all Connection Servers should show green
```

---

## Desktop Pool Health

```
Horizon Console → Inventory → Desktops
  For each pool, check:
    - Available: desktops ready to accept new sessions
    - Provisioned: total VMs in pool (Available + Connected + Disconnected)
    - Error: should be 0 — investigate any in error state immediately
    - Maintenance: expected only during admin maintenance
```

Acceptable ratio: Available desktops should be ≥ 10% of pool size to handle burst demand.

---

## Active Session Count vs License

```powershell
# Using VMware.Hv.Helper PowerShell module
Connect-HVServer -Server horizon-cs01.corp.local -Credential (Get-Credential)

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
curl -sk https://uag.corp.local/favicon.ico  # should return 200
curl -sk https://uag.corp.local:9443/rest/v1/monitor/health \
  -u admin:<password> | python3 -m json.tool
# Look for "RUNNING" status on all services

# Test Blast gateway reachability from external network
# Blast: TCP 8443 (HTTPS)
# PCoIP: TCP/UDP 4172
nc -vz uag.corp.local 8443
nc -vz uag.corp.local 4172
```

---

## App Volumes Manager Health

```
App Volumes Manager UI → Activity → Current Activity
  No stuck attachments or detachments
App Volumes Manager UI → Infrastructure → Managers
  All managers show Healthy
```

```bash
# Test App Volumes Manager API
curl -sk https://appvol-mgr.corp.local/cv_api/status
```

---

## DEM Share Accessibility

Dynamic Environment Manager reads GPO config from a UNC share. Verify accessibility:

```powershell
# On a desktop VM or Connection Server:
Test-Path "\\fileserver.corp.local\DEM-Config\General"
# Should return True

# Check DEM Agent service in a desktop VM
Get-Service -ComputerName <desktop-vm> -Name "User Environment Manager Agent"
```

---

## Certificate Expiry

```bash
# Check Connection Server SSL certificate
echo | openssl s_client -connect horizon-cs01.corp.local:443 -servername horizon-cs01.corp.local 2>/dev/null \
  | openssl x509 -noout -dates

# Check UAG certificate
echo | openssl s_client -connect uag.corp.local:443 -servername uag.corp.local 2>/dev/null \
  | openssl x509 -noout -dates

# Check UAG Blast gateway cert (port 8443)
echo | openssl s_client -connect uag.corp.local:8443 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## Check for Provisioning Errors

```powershell
Connect-HVServer -Server horizon-cs01.corp.local -Credential (Get-Credential)

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
