---
tags:
  - deployment
  - horizon
  - vmware
---
# Horizon — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware Horizon VDI and published applications. Phases 1–2 establish the prerequisites and Connection Server pod; Phases 3–4 cover external access via UAG and desktop pool configuration; Phases 5–6 add application layering (App Volumes), user environment management (DEM), and final validation.

*Applies to: Horizon 8.x*
</div>

```text
┌───────────────────────────────────── Horizon — Deployment Phases ─────────────────────────────────────┐
│                                                                                                       │
│  Six phases from AD/vCenter prerequisites to a validated VDI environment. Complete each phase         │
│  and confirm the exit criterion before advancing to the next phase.                                   │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌──────────────────────────────┐    │
│   │  Phase 1: Prerequisites    │  │   Phase 2: Connection      │  │  Phase 3: Unified Access     │    │
│   │  AD OUs + service accounts │  │   Server Pod               │  │  Gateway (UAG)               │    │
│   │  SQL: Events DB + AV DB    │  │  Install primary CS        │  │  Deploy OVA — DMZ NIC config │    │
│   │  DNS: FQDNs + VIP A-record │  │  Install replica CSs       │  │  Blast + PCoIP edge service  │    │
│   │  vCenter linked, certs CA  │  │  Load balancer pool + VIP  │  │  SAML / cert trust to CS     │    │
│   └────────────────────────────┘  └────────────────────────────┘  └──────────────────────────────┘    │
│                                                                                                       │
│                ▼                               ▼                               ▼                      │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌──────────────────────────────┐    │
│   │  Phase 4: Desktop Pools    │  │  Phase 5: App Volumes      │  │  Phase 6: Validation         │    │
│   │  & RDSH Farms              │  │  & DEM                     │  │                              │    │
│   │  Golden image + IC parent  │  │  App Volumes Mgr deploy    │  │  Session broker: all CS up   │    │
│   │  Instant clone pool config │  │  AppStack capture + assign │  │  UAG: external Blast test    │    │
│   │  RDSH farm + app publish   │  │  DEM agent + GPO + share   │  │  Pool: VMs available + login │    │
│   │  Entitlement: AD groups    │  │  Writable volumes for users│  │  App Volumes: AppStack attach│    │
│   └────────────────────────────┘  └────────────────────────────┘  └──────────────────────────────┘    │
│                                                                                                       │
│  Physical Infrastructure: Connection Server VMs (Windows 2019/2022, 8 vCPU/32 GB) on vSphere;         │
│  UAG VMs in DMZ with dual-NIC; ESXi hosts with vSAN/NFS storage for desktop pools.                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Connection Server = Windows broker service; ADAM (AD LDS) config store; max 7 per pod                │
│  Replica CS        = secondary broker; auto-replicates ADAM from primary CS                           │
│  UAG               = Unified Access Gateway; OVA appliance; DMZ; proxies Blast/PCoIP                  │
│  Instant clone     = vmFork-based pool; ~30 sec provision from running parent VM                      │
│  AppStack          = App Volumes VMDK; attached at login; real-time app delivery                      │
│  DEM               = Dynamic Environment Manager; GPO-based user profile and env policy               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Phase 1 — Prerequisites

**Exit criterion:** AD, SQL, DNS, vCenter, and PKI ready; service accounts created and tested.

### Active Directory

Create the following in AD before installing any Horizon components:

```text
OU=VDI,DC=example,DC=local
  OU=Computers-IC     ← instant clone machine accounts
  OU=Computers-Full   ← full clone / RDSH machine accounts
  OU=Horizon-Servers  ← Connection Server computer accounts
```

Service accounts required:

| Account | Permissions | Purpose |
|---|---|---|
| `svc-horizon-cs` | Domain user; local admin on CS VMs | Horizon Connection Server service |
| `svc-horizon-composer` | Write to VDI computer OUs | Instant clone domain join |
| `svc-horizon-av` | Domain user | App Volumes Manager registration |
| `svc-horizon-events` | SQL: db_owner on Events DB | Horizon Events database writes |

### SQL Server — Events DB and App Volumes DB

```sql
-- Create Horizon Events database
CREATE DATABASE HorizonEvents COLLATE Latin1_General_CS_AS;
GO

-- Create App Volumes database
CREATE DATABASE AppVolumes COLLATE Latin1_General_CS_AS;
GO

-- Grant service account access
USE HorizonEvents;
CREATE USER [EXAMPLE\svc-horizon-events] FOR LOGIN [EXAMPLE\svc-horizon-events];
ALTER ROLE db_owner ADD MEMBER [EXAMPLE\svc-horizon-events];
```

### DNS Records

```dns
horizon-cs-vip.example.local     A  10.10.1.20   ; Connection Server LB VIP
horizon-cs01.example.local       A  10.10.1.21   ; CS node 1
horizon-cs02.example.local       A  10.10.1.22   ; CS node 2
uag-ext.example.com              A  203.0.113.10  ; UAG external FQDN (public)
uag-int.example.local            A  10.10.1.30   ; UAG internal NIC
```

### CA Certificate Readiness

Obtain a certificate for the Connection Server pool FQDN (`horizon-cs-vip.example.local`) and the UAG external FQDN (`uag-ext.example.com`). Both must be issued by a CA trusted by end-user devices.

---

## Phase 2 — Connection Server Pod

**Exit criterion:** Primary CS installed, at least one replica joined, ADAM replication verified, load balancer pool healthy.

### Install Primary Connection Server

Run the Horizon Connection Server installer on the first Windows Server 2019/2022 VM:

```powershell
# Run on the primary CS VM (domain-joined, 8 vCPU / 32 GB RAM)
VMware-Horizon-Connection-Server-x86_64-<version>.exe /silent /install `
  /v"VDM_SERVER_INSTANCE_TYPE=1 `
     VDM_SERVER_NAME=horizon-cs01.example.local `
     VDM_INITIAL_ADMIN_SID=<domain-admins-SID> `
     VDM_LICENSE_KEY=XXXXX-XXXXX-XXXXX-XXXXX"

# Verify service is running
Get-Service -Name "VMware Horizon View Connection Server"
```

After install, complete initial configuration in the Horizon Administrator console (`https://horizon-cs01.example.local/admin`):

1. Apply license key (Administration → Product Licensing and Usage).
2. Add vCenter: View Configuration → Servers → vCenter Servers → Add.
3. Set data recovery password (for ADAM backup).
4. Configure Events DB: View Configuration → Event Configuration → point to SQL `HorizonEvents`.

### Install Replica Connection Servers

```powershell
# Run on each replica VM — select Replica role
VMware-Horizon-Connection-Server-x86_64-<version>.exe /silent /install `
  /v"VDM_SERVER_INSTANCE_TYPE=2 `
     VDM_INITIAL_SERVER_URL=https://horizon-cs01.example.local"

# Verify ADAM replication from replica
vdmadmin -A -d example.local -u svc-horizon-cs -p <password> -verbose
```

### Verify ADAM Replication

```powershell
# Check replication state between Connection Servers
# Horizon Console → View Configuration → Servers → Connection Servers
# All servers must show: Status = Connected, Replication = OK

# CLI check
Get-Service "VMware Horizon View Connection Server" -ComputerName horizon-cs01,horizon-cs02
```

### Load Balancer Pool

Add all Connection Server IPs to the LB pool. Configure health check: HTTPS on port 443, path `/broker/xml`. The pool VIP (`horizon-cs-vip.example.local`) is used by UAG and the Horizon Client.

---

## Phase 3 — Unified Access Gateway (UAG)

**Exit criterion:** UAG deployed in DMZ, external FQDN resolves to UAG VIP, Blast Extreme session from external client succeeds.

### Deploy UAG OVA

UAG uses a PowerShell-based deployment script (`deploy-ova-uag.ps1`) and an INI configuration file:

```powershell
# uag.ini — configure before deployment
[General]
source=VMware-Unified-Access-Gateway-<version>.ova
target=vi://administrator@vsphere.local:<password>@vcenter.example.local/Datacenter/host/cluster

deploymentOption=twonic
netInternet=PG-DMZ-External
netManagementNetwork=PG-Management

[Horizon]
proxyDestinationUrl=https://horizon-cs-vip.example.local:443
proxyDestinationUrlThumbprints=sha1:<cs-vip-thumbprint>
blastExternalUrl=https://uag-ext.example.com:8443
pcoipExternalUrl=203.0.113.10:4172
tunnelExternalUrl=https://uag-ext.example.com:443

# Deploy
pwsh deploy-ova-uag.ps1 uag.ini
```

### Configure UAG Edge Service

After deployment, log in to the UAG Admin UI at `https://<uag-management-ip>:9443`:

1. Configure → Edge Service Settings → Horizon → Enable.
2. Set Connection Server URL: `https://horizon-cs-vip.example.local`.
3. Upload the CS pool certificate (PEM format) for thumbprint trust.
4. If using Workspace ONE Access for SAML SSO: configure Identity Provider metadata under Authentication Methods.

### Firewall Rules Required

| Source | Destination | Port | Protocol | Purpose |
|---|---|---|---|---|
| Internet | UAG external NIC | 443 | TCP | Horizon Client HTTPS + Blast |
| Internet | UAG external NIC | 8443 | TCP/UDP | Blast Extreme primary |
| Internet | UAG external NIC | 4172 | UDP | PCoIP |
| UAG internal NIC | CS VIP | 443 | TCP | UAG → Connection Server |
| UAG internal NIC | Desktop VMs | 22443 | TCP/UDP | Blast Extreme via UAG |

---

## Phase 4 — Desktop Pools and RDSH Farms

**Exit criterion:** At least one instant clone pool provisioned with available desktops; users can connect and reach the desktop.

### Prepare the Golden Image

```powershell
# On the master VM (joined to domain, Windows 10/11 or Server 2019/2022)
# Install Horizon Agent
VMware-Horizon-Agent-x86_64-<version>.exe /silent /install `
  /v"VDM_VC_MANAGED_AGENT=1 ADDLOCAL=Core,BlastAgent,SVIAgent,USB,RTAV"

# Shut down and take a snapshot in vCenter — this is the parent snapshot
# Name it: "IC-Parent-v1-YYYYMMDD"
Stop-Computer -Force
```

### Create an Instant Clone Desktop Pool

In the Horizon Administrator console:

```text
Catalog → Desktop Pools → Add
  → Pool Type: Automated Desktop Pool
  → User Assignment: Floating (or Dedicated)
  → vCenter Server: select registered vCenter
  → Desktop Pool ID: WIN11-IC-POOL-01
  → Display Name: Windows 11 VDI
  → Provisioning: Instant Clones
  → Parent VM: <master-vm-name>
  → Snapshot: IC-Parent-v1-YYYYMMDD
  → Datastore: select vSAN datastore
  → Naming: WIN11-{n}  (generates WIN11-001, WIN11-002, ...)
  → Min provisioned: 10   Max: 50
  → Domain: example.local  OU: OU=Computers-IC,OU=VDI,DC=example,DC=local
  → Service account: EXAMPLE\svc-horizon-composer
```

### Create an RDSH Farm and Application Pool

```text
Catalog → Farms → Add
  → Farm Type: Automated Farm
  → Server OS: Windows Server 2022
  → Farm ID: RDSH-FARM-01
  → Naming: RDSH-{n}
  → Horizon Agent: SVIAgent + RDSH role

Catalog → Application Pools → Add
  → Pool source: Farm — RDSH-FARM-01
  → Select applications to publish
```

### Entitle Users to Pools

```text
Catalog → Desktop Pools → [pool] → Entitlements → Add Entitlement
  → Search for AD group: VDI-Users-Standard
  → Add

# CLI — list entitlements
vdmadmin -A -d example.local -u svc-horizon-cs -p <password>
```

---

## Phase 5 — App Volumes and Dynamic Environment Manager

**Exit criterion:** AppStack attaches at user login; DEM applies user profile settings; writable volumes persist user data across sessions.

### Deploy App Volumes Manager

```powershell
# On Windows Server VM (separate from Connection Server)
App-Volumes-Manager-<version>.exe /silent /norestart

# Configure SQL connection during installer wizard:
#   Server: sql-server.example.local
#   Database: AppVolumes
#   Auth: Windows Auth using svc-horizon-av

# After install — register Connection Servers:
# App Volumes Manager (https://avmgr.example.local) →
#   Configuration → Managers → Register New
#   URL: https://horizon-cs01.example.local
```

### Register vCenter and Create Storage

```text
App Volumes Manager → Configuration → Storage
  → Add vCenter: vcenter.example.local (service account: svc-horizon-av)
  → Add Datastore: select vSAN datastore for AppStack storage
  → Writable Volumes datastore: same or dedicated datastore
```

### Capture and Assign an AppStack

```powershell
# Create a new AppStack package in App Volumes Manager:
# Packages → Create Package → Capture on a packaging VM
# Install the application(s) on the packaging VM
# Complete capture in App Volumes Manager → package is stored as VMDK

# Assign AppStack to AD group:
# Assignment → Applications → [AppStack] → Assign → AD Group: VDI-Apps-Office
```

### Deploy DEM

```powershell
# Install DEM Agent on golden image (add to golden image before taking IC snapshot)
DEM-Agent-<version>.exe /silent ADDLOCAL=DEM_AGENT `
  /v"DEMSHARE=\\fileserver.example.local\DEM-Config$ `
     PROFILEARCHIVE=\\fileserver.example.local\DEM-Profiles$"

# Apply loopback GPO in AD for the VDI computers OU:
# Computer Config → Admin Templates → System → Group Policy
#   → User Group Policy loopback processing mode: Replace

# DEM Management Console: configure FlexEngine directives:
#   - Drive maps: H: → \\fileserver\home\%username%
#   - Printer maps: default printer by AD site
#   - Environment variables: APPDATA redirect
```

---

## Phase 6 — Validation

**Exit criterion:** All checks in this phase pass. Sign off on the deployment and hand to operations.

### Connection Server Health

```powershell
# All CSs in pod must be green
# Horizon Console → Dashboard → System Health

# CLI
Get-Service "VMware Horizon View Connection Server" -ComputerName horizon-cs01,horizon-cs02

# Check ADAM replication
vdmadmin -A -d example.local -u svc-horizon-cs -p <password>
# All replica servers should show "Replication: OK"
```

### UAG External Connectivity

```powershell
# Test from an external client (or a VM with no corporate network access)
# Open Horizon Client → enter: uag-ext.example.com
# Authenticate with AD credentials
# Confirm desktop session launches over Blast Extreme (port 8443)

# Verify UAG edge service health via REST API
Invoke-RestMethod -Uri "https://<uag-mgmt-ip>:9443/rest/v1/monitor/service/horizon" `
  -Credential (Get-Credential admin) -SkipCertificateCheck
# Expected: "serviceProviderId" returned and status UP
```

### Pool Provisioning and Desktop Login

```powershell
# Confirm VMs are in Available state
# Horizon Console → Catalog → Desktop Pools → [pool] → Inventory
# Available VMs must equal min-provisioned count

# Log in as a test user
# Verify: desktop launches, drive maps apply, printer mapped
# Verify: AppStack attached (application appears in Start Menu)
# Verify: DEM profile loads (settings persist on reconnect)
```

### Post-Deployment Checklist

| Check | Command / Location | Pass Criterion |
|---|---|---|
| Connection Servers | Horizon Console → Dashboard | All servers green |
| ADAM replication | `vdmadmin -A -d example.local` | All replicas: OK |
| vCenter registered | View Configuration → Servers | Connected |
| UAG edge service | UAG Admin UI port 9443 → Monitor | Horizon service: UP |
| Pool provisioning | Catalog → Pools → Inventory | Available VMs = min count |
| External Blast session | Horizon Client → uag-ext FQDN | Desktop launches (port 8443) |
| App Volumes attach | Test user login | AppStack VMDK shows in guest |
| DEM policies | Test user login | Drive maps + printers applied |
| Events DB | View Configuration → Event Config | Last event timestamp recent |
| Certificates | Browser to CS VIP + UAG external | No certificate warnings |
