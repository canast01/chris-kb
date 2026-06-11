# VMware Horizon — Health Checks

<div class="kb-summary">
Health checks for Horizon — Connection Server status, desktop pool availability, UAG gateway health, session counts vs licensed capacity, certificate expiry, and App Volumes / DEM component health.
</div>

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
## Run This Routine

1. **Connection Server service status** — run on or against each CS:
   ```powershell
   Get-Service -ComputerName cs-prod-01 -Name wsbroker | Select Status
   ```
2. **Horizon pod health** — Horizon Console → Dashboard → confirm all Connection Servers show green status.
3. **UAG health** — open UAG admin UI at `https://<uag>:9443/admin` → verify all edge services show **Up**.
4. **Desktop pool assignment** — via Horizon PowerCLI:
   ```powershell
   Get-Pool | Select pool_id,numMachines,numConnectedSessions
   ```
5. **Instant clone parent VM** — in vCenter, verify the parent VM and replica VMs exist for each pool under the correct folder.
6. **Active session count** — Horizon Console → Monitor → Sessions → note current count vs licensed capacity limit.
7. **Certificate expiry** — check Connection Server certificate:
   ```powershell
   Get-Certificate -DnsName <cs-fqdn>
   ```
   Or: Horizon Console → Settings → Servers → Connection Servers → select server → Certificates tab.
8. **vCenter connectivity** — Horizon Console → Settings → Servers → vCenter → confirm status shows **Connected**.
9. **Composer/Instant Clone health** — Horizon Console → Monitor → Events → filter by Error/Warning → confirm no provisioning errors.
10. **Blast gateway reachability** — from a client network:
    ```bash
    curl -sk https://<uag-external>:443/
    ```
    Expect an HTTP redirect (3xx) response; a connection refused or timeout indicates a gateway issue.

---

## Session Count and Pool Status

```powershell
## Using VMware.Hv.Helper PowerShell module
Connect-HVServer -Server horizon-cs01.example.local -Credential (Get-Credential)

## Get current active session count
$sessions = Get-HVLocalSession
Write-Host "Active sessions: $($sessions.Count)"

## Get licensed session count from License page
## Horizon Console → Settings → Product Licensing and Usage
```
## UAG Health and Port Checks

```bash
# UAG exposes a health API endpoint
curl -sk https://uag.example.local/favicon.ico  # should return 200
curl -sk https://uag.example.local:9443/rest/v1/monitor/health \
  -u admin:<password> | python3 -m json.tool
## Look for "RUNNING" status on all services

## Test Blast gateway reachability from external network
## Blast: TCP 8443 (HTTPS)
## PCoIP: TCP/UDP 4172
nc -vz uag.example.local 8443
nc -vz uag.example.local 4172
```
## App Volumes Health

App Volumes Manager UI → **Activity → Current Activity** — no stuck attachments or detachments.
App Volumes Manager UI → **Infrastructure → Managers** — all managers show Healthy.

```bash
# Test App Volumes Manager API
curl -sk https://appvol-mgr.example.local/cv_api/status
```
## DEM Agent Health

```powershell
# On a desktop VM or Connection Server:
Test-Path "\\fileserver.example.local\DEM-Config\General"
## Should return True

## Check DEM Agent service in a desktop VM
Get-Service -ComputerName <desktop-vm> -Name "User Environment Manager Agent"
```
## Certificate Expiry Checks

```bash
# Check Connection Server SSL certificate
echo | openssl s_client -connect horizon-cs01.example.local:443 -servername horizon-cs01.example.local 2>/dev/null \
  | openssl x509 -noout -dates

## Check UAG certificate
echo | openssl s_client -connect uag.example.local:443 -servername uag.example.local 2>/dev/null \
  | openssl x509 -noout -dates

## Check UAG Blast gateway cert (port 8443)
echo | openssl s_client -connect uag.example.local:8443 2>/dev/null \
  | openssl x509 -noout -dates
```
## Desktop Error State Cleanup

```powershell
Connect-HVServer -Server horizon-cs01.example.local -Credential (Get-Credential)

# Get desktops in error state
Get-HVDesktop | Where-Object { $_.Base.BasicState -eq "ERROR" } | 
  Select-Object -ExpandProperty Base | 
  Select-Object Name, BasicState, DesktopSummaryData

## Delete error-state desktops (they will be reprovisioned automatically)
Get-HVDesktop | Where-Object { $_.Base.BasicState -eq "ERROR" } |
  Remove-HVDesktop -Confirm:$false
```
## External Connectivity Port Check

```bash
# Blast Extreme — TCP 8443 to UAG
nc -vz uag.public.corp.com 8443

## PCoIP — TCP 4172 and UDP 4172 to UAG
nc -vz uag.public.corp.com 4172

## HTTPS Tunnel — TCP 443 to UAG
nc -vz uag.public.corp.com 443
```
