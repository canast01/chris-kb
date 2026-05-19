# SRM — Install and Upgrade

```
  SRM Upgrade Sequence (strictly ordered)
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  1. vCenter   │──►│  2. SRM Server│──►│  3. SRA       │──►│  4. VR        │
│  (both sites) │   │  protected    │   │  (both SRM    │   │  Appliance    │
│               │   │  site first,  │   │   Servers)    │   │  (both sites) │
│               │   │  then recov.  │   │               │   │               │
└───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘
         │
         ▼
  After each step: verify site pairing still Connected before proceeding
```

---

## Prerequisites

| Requirement | Detail |
|---|---|
| vCenter | Version compatible with SRM version — check interopmatrix.vmware.com |
| Windows Server | 2019 or 2022 for SRM Server (Windows-based deployment) |
| OR: SRM Appliance | OVA-based deployment (available from SRM 8.x+) |
| DNS | FQDN for both SRM servers resolvable from both sites |
| Network | TCP 443 and TCP 9086 between SRM Servers across sites |
| NTP | Both sites time-synchronized |
| vSphere Replication | Optional — deploy VRA appliance if using software-based replication |
| SRA | Required for array-based replication — download from array vendor |

---

## SRM Server Installation (Windows)

```powershell
# Run installer as local admin — not domain admin required for install
VMware-srm-<version>.exe /silent /norestart

# During installation wizard:
#   vCenter Server: https://vcenter-protected.example.local
#   SSO credentials: administrator@vsphere.local
#   SRM site name: Protected-Site  (or Recovery-Site for second installation)
#   Local SRM Server: srm-protected.example.local
#   Port: 8095 (admin), 9086 (inter-site)
#   Certificate: import PFX or use auto-generated
#   Database: embedded PostgreSQL or external SQL Server
```

Install SRM on both sites before pairing. Site pairing is done from the vCenter UI after both are installed.

---

## vSphere Replication Appliance Deployment

Deploy VRA OVA at both the protected and recovery sites:

```
vCenter → Deploy OVF Template → VMware-vSphere-Replication-<version>.ovf
  Network: Management network (must reach vCenter and remote VRA)
  IP: static IP (DHCP not recommended)
  NTP: configure NTP server

Post-deploy:
  VRA Web UI (https://vra-protected.example.local:5480)
  Configuration → vCenter Server: vcenter-protected.example.local
  → Register with vCenter
```

Pair VRA appliances:
```
vCenter (Protected) → Site Recovery → New Site Pair
  Remote vCenter: vcenter-recovery.example.local
  Remote VRA: vra-recovery.example.local
  Accept certificate thumbprint
```

---

## SRA Installation

Storage Replication Adapters (SRAs) are provided by storage array vendors:

```powershell
# Example: Pure Storage SRA
# Download from: support.purestorage.com → Downloads → SRA for SRM
# Copy installer to SRM Server

# Install SRA on BOTH SRM Servers (protected AND recovery):
Pure_Storage_SRA_<version>.exe /silent

# After install, register SRA in SRM:
# Site Recovery → Storage → Storage Adapters → Configure Adapter
# Select: Pure Storage FlashArray
# Credentials: FlashArray management IP + API token
```

---

## Site Pairing

After SRM is installed on both sites and VRA/SRA is deployed:

```
vCenter (Protected Site) → Site Recovery → New Site Pair
  Remote vCenter: vcenter-recovery.example.local
  Site Recovery Manager: srm-recovery.example.local
  Credentials: administrator@vsphere.local on remote vCenter
  Accept certificate thumbprints from both SRM servers
```

After pairing, configure inventory mappings:
```
Site Recovery → Site Pair → Configure → Inventory Mappings
  Network mappings: protected networks → recovery networks
  Resource mappings: protected cluster/RP → recovery cluster/RP
  Folder mappings: protected VM folders → recovery VM folders
  Storage policy mappings (if applicable)
```

---

## Upgrade Order

Strict order — do not deviate:

1. **vCenter** — upgrade both sites' vCenters first
2. **SRM Server** — upgrade protected site first, then recovery site
   - After each upgrade, verify site pairing is still healthy before proceeding
3. **SRA** — upgrade on both SRM Servers (check vendor release notes for SRA/SRM compat)
4. **vSphere Replication Appliance** — upgrade both VRAs (upgrade protected site VRA first)

```powershell
# Take a snapshot of SRM Server VM before upgrade
New-Snapshot -VM "srm-protected" -Name "Pre-Upgrade-SRM-8.x" -Memory $false

# Run new SRM installer (in-place upgrade)
VMware-srm-<new-version>.exe /silent

# Verify service after upgrade:
Get-Service "VMware vCenter Site Recovery Manager"

# Check site pairing health:
# vCenter → Site Recovery → Summary → both sites Connected
```

---

## Post-Install Verification

```powershell
# Connect to SRM via PowerCLI
$srm = Connect-SrmServer -SrmServerAddress srm-protected.example.local
$plans = $srm.ExtensionData.Recovery.ListPlans()
Write-Host "Recovery Plans found: $($plans.Count)"

# Run a pre-check on each Recovery Plan
foreach ($plan in $plans) {
    $srm.ExtensionData.Recovery.Start($plan.MoRef, "PRECHECK_ONLY")
}
```
