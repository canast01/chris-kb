# Horizon — Install and Upgrade


<div class="kb-summary">
Install and Upgrade reference covering Horizon Agent Installation in Golden Image, UAG Deployment, App Volumes Manager Installation, Upgrade Order, Upgrade a Connection Server (Rolling) and 2 more sections.
</div>

  Upgrade Sequence (strictly ordered)
                    └───────────────┘
                            │
                   ┌────────▼────────┐   ┌───────────────┐
                   │  5. App Volumes │──►│  6. App Vol   │
                   │  Manager        │   │  Agent (in    │
                   └─────────────────┘   │  AppStacks)   │
                                         └───────────────┘
```text
┌───────────────────────────────── VMware Horizon — Install & Upgrade ──────────────────────────────────┐
│                                                                                                       │
│  Horizon installation deploys Connection Servers on Windows VMs; upgrade applies                      │
│  the installer sequentially to each CS, then updates UAGs and agents.                                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Pre-Install Requirements           │  │                Install Steps                │   │
│   │           Windows Server 2019/2022           │  │          Install first CS: standard         │   │
│   │               AD domain joined               │  │           Add replica CS: same pod          │   │
│   │            SQL Server: events DB             │  │             Deploy UAGs via OVA             │   │
│   │            DNS: CS FQDN resolves             │  │          Link to vCenter in Horizon         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Install first Connection Server before replicas; all share same LDAP config.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Sequence               │  │                Agent Upgrade                │   │
│   │            1. Snapshot all CS VMs            │  │             Update golden image             │   │
│   │             2. Upgrade first CS              │  │         Push: Horizon Agent install         │   │
│   │            3. Upgrade replica CSs            │  │         Instant clones: auto-reclone        │   │
│   │               4. Upgrade UAGs                │  │        Full clone: manual agent push        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Connection Server VMs need 8 vCPU / 32GB RAM; Windows Server licence required;                       │
│  UAGs need dual-NIC access to both internal and external networks.                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Connection Server= Horizon broker; requires Windows Server OS                                        │
│  Replica CS    = secondary broker; replicates LDAP from first CS                                      │
│  Pod           = group of Connection Servers sharing same LDAP                                        │
│  UAG           = Unified Access Gateway; OVA deployed; DMZ placement                                  │
│  Events DB     = SQL Server; stores Horizon event log and reports                                     │
│  LDAP          = Horizon config store; Active Directory Lightweight DS                                │
│  Golden image  = master VM; Horizon Agent installed; used for clones                                  │
│  Reclone       = instant clone pool refreshes from updated golden image                               │
│  Agent push    = software distribution to full clone VMs                                              │
│  Snapshot CS   = pre-upgrade rollback point; delete within 72h                                        │
│  vCenter link  = Horizon must register vCenter in Administration UI                                   │
│  Windows Server= required OS; 2019 or 2022; domain joined                                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌───────────────────────────────── VMware Horizon — Install & Upgrade ──────────────────────────────────┐
│                                                                                                       │
│  Horizon installation deploys Connection Servers on Windows VMs; upgrade applies                      │
│  the installer sequentially to each CS, then updates UAGs and agents.                                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Pre-Install Requirements           │  │                Install Steps                │   │
│   │           Windows Server 2019/2022           │  │          Install first CS: standard         │   │
│   │               AD domain joined               │  │           Add replica CS: same pod          │   │
│   │            SQL Server: events DB             │  │             Deploy UAGs via OVA             │   │
│   │            DNS: CS FQDN resolves             │  │          Link to vCenter in Horizon         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Install first Connection Server before replicas; all share same LDAP config.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Sequence               │  │                Agent Upgrade                │   │
│   │            1. Snapshot all CS VMs            │  │             Update golden image             │   │
│   │             2. Upgrade first CS              │  │         Push: Horizon Agent install         │   │
│   │            3. Upgrade replica CSs            │  │         Instant clones: auto-reclone        │   │
│   │               4. Upgrade UAGs                │  │        Full clone: manual agent push        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Connection Server VMs need 8 vCPU / 32GB RAM; Windows Server licence required;                       │
│  UAGs need dual-NIC access to both internal and external networks.                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Connection Server= Horizon broker; requires Windows Server OS                                        │
│  Replica CS    = secondary broker; replicates LDAP from first CS                                      │
│  Pod           = group of Connection Servers sharing same LDAP                                        │
│  UAG           = Unified Access Gateway; OVA deployed; DMZ placement                                  │
│  Events DB     = SQL Server; stores Horizon event log and reports                                     │
│  LDAP          = Horizon config store; Active Directory Lightweight DS                                │
│  Golden image  = master VM; Horizon Agent installed; used for clones                                  │
│  Reclone       = instant clone pool refreshes from updated golden image                               │
│  Agent push    = software distribution to full clone VMs                                              │
│  Snapshot CS   = pre-upgrade rollback point; delete within 72h                                        │
│  vCenter link  = Horizon must register vCenter in Administration UI                                   │
│  Windows Server= required OS; 2019 or 2022; domain joined                                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
