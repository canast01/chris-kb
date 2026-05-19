# Horizon — Install and Upgrade

```
  Upgrade Sequence (strictly ordered)
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  1. vCenter   │──►│  2. Connection│──►│  3. UAG       │──►│  4. Horizon   │
│  (if          │   │  Servers      │   │  (redeploy    │   │  Agent in     │
│   upgrading   │   │  (rolling —   │   │   from new    │   │  golden image │
│   vSphere)    │   │   one at a    │   │   OVA)        │   │  + push pools)│
└───────────────┘   │   time)       │   └───────────────┘   └───────────────┘
                    └───────────────┘
                            │
                   ┌────────▼────────┐   ┌───────────────┐
                   │  5. App Volumes │──►│  6. App Vol   │
                   │  Manager        │   │  Agent (in    │
                   └─────────────────┘   │  AppStacks)   │
                                         └───────────────┘
```

---

## Prerequisites

| Requirement | Detail |
|---|---|
| Windows Server | 2019 or 2022 for Connection Server |
| Domain | Connection Server must be domain-joined |
| vCenter | Supported version — check Horizon Compatibility Matrix |
| SQL Server | Optional — for Events DB (SQLExpress included but not recommended for production) |
| DNS | FQDN for each Connection Server resolvable internally and externally |
| NTP | All servers time-synchronized (±5 seconds) |
| Certificate | Wildcard or SAN cert for Connection Server and UAG |

---

## Connection Server Installation

```powershell
# Run installer on Windows Server — must be domain admin
# Download: customerconnect.vmware.com → VMware Horizon → Connection Server installer

# Silent install (for automation):
VMware-Horizon-Connection-Server-x86_64-<version>.exe /silent /norestart `
  /v"VDM_SERVER_INSTANCE_TYPE=1 VDM_FQDN=horizon-cs01.example.local `
  VDM_INITIAL_ADMIN_SID=<domain-admin-SID>"
```

For replica servers (additional Connection Servers in the same pod):
```powershell
VMware-Horizon-Connection-Server-x86_64-<version>.exe /silent /norestart `
  /v"VDM_SERVER_INSTANCE_TYPE=2 VDM_IP_PROTOCOL_USAGE=IPv4 `
  VDM_INITIAL_ADMIN_SID=<domain-admin-SID> `
  VDM_INITIAL_ADMIN_PASSWORD=<password>"
```

---

## Horizon Agent Installation in Golden Image

Install Horizon Agent into the golden image VM (the template for Instant Clone pools):

```powershell
# Silent install — customize components as needed
VMware-Horizon-Agent-x86_64-<version>.exe /silent /norestart `
  /v"VDM_SKIP_BROKER_REGISTRATION=1 RDP_CHOICE=1 `
  ADDLOCAL=Core,SVIAgent,BlastAgent,PCoIP,ClientDriveRedirection,USB,RTAV"
```

Key components:
- `Core` — required
- `BlastAgent` — Blast Extreme display protocol
- `PCoIP` — PCoIP display protocol (optional if Blast-only)
- `SVIAgent` — Instant Clone support (required for IC pools)
- `USB` — USB redirection
- `RTAV` — Real-Time Audio-Video

Shut down the VM and take a snapshot before creating a pool.

---

## UAG Deployment

UAG is deployed from OVA. Use PowerShell for repeatable deployment:

```powershell
# Download UAG OVA and deploy-ova-uag.ps1 from VMware
# Edit uag.ini config file:
[General]
source=VMware-Unified-Access-Gateway-<version>.ova
target=vi://administrator@vsphere.local:password@vcenter.example.local/...
deploymentOption=onenic  # or twonic, threenic for DMZ placement
netInternet=VM Network
netManagementNetwork=VM Network
netBackendNetwork=VM Network

[Horizon]
proxyDestinationUrl=https://horizon-cs01.example.local:443
proxyDestinationUrlThumbprints=sha1:<cs01-thumbprint>

# Deploy
pwsh deploy-ova-uag.ps1 uag.ini
```

Post-deployment, configure Edge Service settings via UAG Admin UI (port 9443) or REST API.

---

## App Volumes Manager Installation

```powershell
# Deploy App Volumes Manager on Windows Server
App-Volumes-Manager-<version>.exe /silent /norestart

# Configure SQL database connection during wizard
# Default port: HTTPS 443

# After install, register Connection Servers:
# App Volumes Manager → Configuration → Managers → Register new
```

---

## Upgrade Order

Upgrade components in this strict order:

1. **vCenter** (if upgrading vSphere simultaneously)
2. **Connection Servers** — one at a time, verify health before proceeding to next
3. **UAG** — redeploy from new OVA (stateless appliance — redeploy is the upgrade path)
4. **Horizon Agent in golden image** — update snapshot, push to pools
5. **App Volumes Manager**
6. **App Volumes Agent** (in App Volumes VHD/AppStacks — update via App Volumes Manager)

> Never upgrade Connection Servers simultaneously — always rolling, one at a time.

---

## Upgrade a Connection Server (Rolling)

```powershell
# 1. Put the CS being upgraded into Quiesce mode (drains sessions)
#    Horizon Console → Settings → Servers → [CS] → Set Maintenance Mode: Quiesce

# 2. Wait for sessions to drain or force-migrate

# 3. Run the new installer (upgrade in-place)
VMware-Horizon-Connection-Server-x86_64-<new-version>.exe /silent

# 4. Verify service is running
Get-Service -Name "VMware Horizon View Connection Server"

# 5. Disable maintenance mode
#    Horizon Console → Settings → Servers → [CS] → Disable Maintenance Mode

# 6. Proceed to next Connection Server
```

---

## Version Compatibility Reference

Check the VMware Product Interoperability Matrix before upgrade:
- https://interopmatrix.vmware.com
- Key dependencies: Horizon ↔ vSphere ↔ App Volumes ↔ DEM ↔ vSAN

---

## Post-Install Verification

```powershell
# Verify all Connection Servers are healthy after upgrade
Get-HVLocalSession  # should return sessions from all CS nodes
# Horizon Console → Dashboard → all servers green

# Test desktop provisioning — create a test pool, provision 1 desktop, confirm it connects
```
