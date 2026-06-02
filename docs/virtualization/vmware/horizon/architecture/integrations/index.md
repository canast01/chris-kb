# Horizon — Integrations


<div class="kb-summary">
Integrations reference covering Active Directory, vCenter Integration, vSAN Integration, App Volumes Integration, Dynamic Environment Manager (DEM) Integration and 4 more sections.
</div>

## Active Directory

Active Directory is a hard dependency — Connection Server must be domain-joined. Horizon uses AD for:

- User authentication (Kerberos/NTLM via Connection Server)
- Entitlement groups (AD security groups mapped to desktop pools)
- Group Policy delivery (Horizon ADMX templates applied via GPO)
- Computer account management (Instant Clone domain join — OU for machine accounts)
- DEM and App Volumes group-based assignment

### Connection Server Domain Join

The Connection Server is a standard domain member. Install Windows Server, join the domain, then install Horizon Connection Server software.

```powershell
# Verify domain join before CS install
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()

# Check DNS resolves AD DCs
nslookup _ldap._tcp.dc._msdcs.<your-domain>
```
```text
┌──────────────────────────────────── VMware Horizon — Integrations ────────────────────────────────────┐
│                                                                                                       │
│  Horizon integrates with AD for identity, vCenter for VM management, Workspace ONE                    │
│  for unified endpoint management, and third-party printing/profile solutions.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Identity & Auth                │  │                Infrastructure               │   │
│   │          Active Directory: required          │  │            vCenter: VM lifecycle            │   │
│   │           RADIUS: MFA integration            │  │          vSAN/NFS: desktop storage          │   │
│   │              RSA/Duo: OTP token              │  │         NSX: micro-seg desktop VLAN         │   │
│   │             Smart card: PIV/CAC              │  │          vSphere HA: pool recovery          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  AD is mandatory; all other integrations are optional but recommended for enterprise.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Workspace ONE Integration           │  │              Profile & Printing             │   │
│   │           W1 Access: SAML gateway            │  │           DEM: profile management           │   │
│   │            W1 UEM: policy + apps             │  │          FSLogix: profile container         │   │
│   │          Digital workspace: unified          │  │         ThinPrint: virtual printing         │   │
│   │          App Volumes: app delivery           │  │           CIFS/NFS: profile share           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  All Horizon components on management network; UAG on DMZ; desktop VMs on                             │
│  dedicated VLAN; profile shares on NAS over CIFS/NFS.                                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Workspace ONE Access= SAML-based app portal; unified access layer                                    │
│  Workspace ONE UEM  = Unified Endpoint Management; policy/app delivery                                │
│  App Volumes        = app delivery via AppStacks; no per-desktop install                              │
│  DEM               = Dynamic Environment Manager; profile personalisation                             │
│  FSLogix           = Microsoft profile container; VHDX per user on share                              │
│  RADIUS            = Multi-Factor Auth backend protocol                                               │
│  Smart card        = PIV/CAC certificate login; AD smart card auth                                    │
│  NSX               = micro-segment desktop VMs from each other                                        │
│  ThinPrint         = virtual printing solution for VDI                                                │
│  AppStack          = App Volumes package; writable volume or app layer                                │
│  SAML gateway      = W1 Access presents SAML to Horizon Connection Server                             │
│  CIFS              = file share protocol; desktop profiles stored here                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Key GPO paths (in GPMC):
- `Computer Configuration > Administrative Templates > VMware Blast` — display protocol settings
- `Computer Configuration > Administrative Templates > VMware View Agent Configuration` — agent behavior, USB, clipboard
- `User Configuration > Administrative Templates > VMware DEM` — DEM policy enforcement

### Required AD Permissions for Instant Clone Domain Join

Create a dedicated service account with delegated permissions on the OU where desktop computer accounts will reside:

| Permission | Why |
|---|---|
| Create Computer Objects | Provision new machine accounts |
| Delete Computer Objects | Clean up on desktop deletion |
| Reset Password | Reset machine account at each clone |
| Read/Write all properties | Update computer account attributes |

```cmd
dsacls "OU=Horizon-Desktops,DC=corp,DC=example,DC=com" /I:S /G "CORP\svc-horizon-ic:CCDC;Computer"
dsacls "OU=Horizon-Desktops,DC=corp,DC=example,DC=com" /I:S /G "CORP\svc-horizon-ic:WP;;Computer"
```

---

## vCenter Integration

Connection Server communicates with vCenter via the vSphere API. Each Connection Server pod registers one or more vCenter instances.

### Adding vCenter to Connection Server

In Horizon Admin Console: **Settings > Servers > vCenter Servers > Add**

Required inputs:
- vCenter server FQDN or IP
- Service account credentials
- Datacenter(s) to manage

### vCenter Service Account Privileges

Create a dedicated vSphere role and assign to the service account at the datacenter level:

| Privilege | Required For |
|---|---|
| VirtualMachine.Snapshot.Create/Remove | Instant Clone replica creation |
| VirtualMachine.Provisioning.Clone | VM cloning |
| VirtualMachine.Interact.PowerOn/Off | Power management |
| VirtualMachine.Config.AddRemoveDevice | Disk attach/detach (App Volumes) |
| Datastore.AllocateSpace | Disk provisioning |
| Network.Assign | NIC assignment at clone time |
| Resource.AssignVMToPool | Resource pool assignment |
| Host.Local.ReconfigVM | Instant Clone fork (vmFork) |
| Global.DisableMethods | Required by Connection Server |

```powershell
# PowerCLI — create and assign the role
Connect-VIServer vcenter.corp.example.com

$privIds = @(
  "VirtualMachine.Snapshot.Create","VirtualMachine.Snapshot.RemoveAll",
  "VirtualMachine.Provisioning.Clone","VirtualMachine.Provisioning.DeployTemplate",
  "VirtualMachine.Interact.PowerOn","VirtualMachine.Interact.PowerOff",
  "VirtualMachine.Config.AddRemoveDevice","Datastore.AllocateSpace",
  "Network.Assign","Resource.AssignVMToPool","Host.Local.ReconfigVM","Global.DisableMethods"
)
New-VIRole -Name "Horizon-Service" -Privilege (Get-VIPrivilege -Id $privIds)
New-VIPermission -Entity (Get-Datacenter "DC-Production") `
  -Principal "CORP\svc-horizon-vc" -Role "Horizon-Service" -Propagate $true
```

---

## vSAN Integration

vSAN is the recommended storage for Horizon Instant Clone pools.

**Design considerations:**

- Instant Clone replica and parent VM VMDKs benefit from vSAN NVMe/SSD cache tier
- Use vSAN storage policies per pool type:
  - Replica/parent VMs: FTT=1, RAID-1 (recreatable — lower redundancy acceptable)
  - Persistent/writable volumes: FTT=1 or FTT=2, RAID-1 (user data)
- Thin provisioning: Instant Clone children are thin by design
- Enable vSAN deduplication and compression — desktop OS disks deduplicate heavily (50–70% savings typical)

```powershell
# Create a vSAN storage policy for desktop OS disks
$rule = New-SpbmRuleSet -AllOfRules @(
  New-SpbmRule -Capability (Get-SpbmCapability "VSAN.hostFailuresToTolerate") -Value 1,
  New-SpbmRule -Capability (Get-SpbmCapability "VSAN.stripeWidth") -Value 1
)
New-SpbmStoragePolicy -Name "Horizon-Desktop-OS-FTT1" -RuleSet $rule
```

---

## App Volumes Integration

App Volumes delivers applications as VMDKs (AppStacks) attached at login, without modifying the golden image.

### Components

| Component | Role |
|---|---|
| App Volumes Manager | Web console + SQL DB; controls assignments |
| App Volumes Agent | In-guest agent in golden image; mounts/unmounts VMDKs |
| AppStack | Read-only VMDK containing captured applications |
| Writable Volume | Per-user VMDK for user-installed apps and data |

### Integration Steps

1. Deploy App Volumes Manager (Windows Server + SQL Server — see install page)
2. Register in Horizon Admin: **Settings > App Volumes Managers**
3. Install App Volumes Agent in the golden image
4. Create AppStacks by capturing apps in a dedicated packaging VM
5. Assign AppStacks to users/groups/OUs/computers in App Volumes Manager

### Silent Agent Install in Golden Image

```cmd
msiexec /i "App Volumes Agent.msi" /qn REBOOT=ReallySuppress ^
  CLOUDVOLUMES_MANAGER_ADDR=appvol-mgr.corp.example.com ^
  CLOUDVOLUMES_MANAGER_PORT=443
```

### AppStack VMDK Datastore Layout

```text
[SAN-Datastore01] cloudvolumes/
  apps/
    Office365-2406.vmdk
    AdobeAcrobat-DC.vmdk
    AutoCAD-2025.vmdk
  writables/
    CORP_jsmith.vmdk
    CORP_jdoe.vmdk
```

---

## Dynamic Environment Manager (DEM) Integration

DEM manages user environments in stateless Instant Clone desktops — replacing roaming profiles.

### Architecture

- **DEM Management Console** — Windows app; policy XMLs written to config share
- **DEM Config Share** — HA SMB share hosting all policy definitions
- **DEM Agent** — In golden image; processes config share at logon/logoff

### Integration Steps

1. Create and share DEM Config Share:
```powershell
New-Item -ItemType Directory -Path "D:\DEMConfig"
New-SmbShare -Name "DEMConfig" -Path "D:\DEMConfig" `
  -ReadAccess "Domain Users" -FullAccess "CORP\svc-dem-admin","CORP\Horizon-Admins"
```

2. Install DEM Agent in golden image (included in Horizon Agent installer or standalone MSI)

3. Apply GPO to desktop OU:
   - `Computer Config > VMware DEM > FlexEngine > Config Share Path` = `\\fileserver\DEMConfig`
   - `Computer Config > VMware DEM > FlexEngine > Enable FlexEngine` = Enabled
   - `Computer Config > VMware DEM > FlexEngine > Run at user logon` = Enabled

### Config Share NTFS Permissions

```text
CORP\Domain Users         — Read & Execute (This folder, subfolders, files)
CORP\svc-dem-admin        — Full Control
CORP\Horizon-Admins       — Full Control
SYSTEM                    — Full Control
```

---

## UAG Deployment

UAG is a Linux appliance (OVA) deployed in the DMZ that proxies Horizon connections from external clients.

### PowerShell Automated Deployment

VMware provides `uagdeploy.ps1` in the UAG deployment bundle.

**INI configuration file (uag-prod.ini):**
```ini
[General]
name=uag-prod-01
deploymentOption=onenic
ds=SAN-Datastore01
netInternet=VLAN-100-DMZ
source=.\VMware-UAG-2312.0-23064540_OVF10.ova
diskMode=thin

[Horizon]
proxyDestinationUrl=https://cs01.corp.example.com
proxyDestinationUrlThumbprint=sha256:AABBCC...
blastExternalUrl=https://vdi.example.com:8443
pcoipExternalUrl=203.0.113.10
tunnelExternalUrl=https://vdi.example.com:443
```

```powershell
# Deploy
.\uagdeploy.ps1 -iniFile .\uag-prod.ini `
  -vCenterServer vcenter.corp.example.com `
  -vCenterUser administrator@vsphere.local `
  -vCenterPassword $vcPass
```

### Load Balancing Multiple UAGs

- Deploy 2+ UAGs behind a load balancer (F5, NSX ALB, HAProxy)
- LB VIP is the public FQDN (e.g., `vdi.example.com`)
- No session persistence required — UAG is stateless
- Health check: `HTTPS GET https://<uag-ip>:443/favicon.ico` → expect 200

LB listener ports:
```text
443/TCP    — HTTPS + Horizon tunnel
8443/TCP   — Blast Extreme (TCP mode)
8443/UDP   — Blast Extreme (UDP/adaptive transport)
4172/TCP   — PCoIP (TCP)
4172/UDP   — PCoIP (UDP)
```

---

## True SSO with vIDM / Workspace ONE

True SSO issues a short-lived certificate at login so users who authenticate via SAML/MFA at the broker are not prompted for a password when their Windows desktop session starts.

### Prerequisites

| Component | Notes |
|---|---|
| Horizon Enrollment Server | Windows Server role; communicates with CA |
| Microsoft AD CS | Certificate Authority with enrollment agent template |
| vIDM / Workspace ONE | SAML IdP configured for Connection Server |

### Configuration Summary

1. Configure AD CS: create a certificate template based on Enrollment Agent; grant Enrollment Server the right to enroll
2. Install Horizon Enrollment Server; register with the CA
3. In Connection Server: **Settings > Servers > Connection Servers > [Edit] > Authentication > True SSO Authenticators** — add Enrollment Server
4. Configure SAML delegation on Connection Server to vIDM

```powershell
# Verify Enrollment Server connectivity from Connection Server
Test-NetConnection -ComputerName enrollment-srv.corp.example.com -Port 32111
Test-NetConnection -ComputerName ca.corp.example.com -Port 135
```

---

## SAML Authentication

SAML allows an external IdP (Workspace ONE, Okta, ADFS) to authenticate users before they reach Horizon.

### Connection Server SAML Config

In Horizon Admin: **Settings > Servers > Connection Servers > [Edit] > Authentication**:
- `Delegation of Authentication to VMware Access Point`: **Allowed** or **Required**
- `SAML Authenticator`: enter SAML metadata URL from IdP

**SAML flow:**
```text
1. User hits IdP portal (e.g., Workspace ONE)
2. IdP authenticates user (MFA, LDAP, cert)
3. IdP issues signed SAML assertion → redirects to Connection Server / UAG
4. Connection Server validates assertion signature
5. True SSO issues short-lived cert → Windows session starts without password prompt
```

---

## Carbon Black / EDR Integration

For environments requiring endpoint detection on VDI desktops:

- Install EDR agent in golden image — it installs into each Instant Clone child
- Verify EDR license model supports VDI/non-persistent (most vendors offer VDI SKUs)
- Carbon Black CBC: use VDI sensor mode (`/VDIMODE` install flag) to avoid sensor proliferation
- CrowdStrike Falcon: use `--tags` at install time to group VDI sensors; enable sensor grouping policy

**AV/EDR exclusions for Horizon directories:**

```text
C:\Program Files\VMware\VMware View\Agent\
C:\ProgramData\VMware\VDM\
C:\Windows\Temp\vmware-viewcomposer-ga-new-*
```

**App Volumes mount point exclusions (real-time scanning):**
```text
\\?\Volume{*}\   (all volumes — or specifically App Volumes mount GUIDs)
```

Test logon duration before/after agent install — EDR agents can add 5–15 seconds to desktop logon in worst-case configurations.
