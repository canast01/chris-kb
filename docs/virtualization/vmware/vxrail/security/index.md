# VxRail — Security

```
┌───────────────────── VxRail Security Layers ───────────────────────────────────┐
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  iDRAC (Hardware OOB)                                                   │    │
│  │  root/Calvin changed │ LDAP/AD │ OOB VLAN only │ Secure Boot │ FW via LCM│   │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                    │                                            │
│  ┌─────────────────────────────────▼───────────────────────────────────────┐    │
│  │  ESXi Host                                                              │    │
│  │  Lockdown Mode (Normal) │ SSH/Shell disabled │ Host Profiles compliant  │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                    │                                            │
│  ┌─────────────────────────────────▼───────────────────────────────────────┐    │
│  │  vSAN                                                                   │    │
│  │  Data-at-rest encryption (KMS/NKP) │ In-transit encryption (AES-NI)    │     │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                    │                                            │
│  ┌─────────────────────────────────▼───────────────────────────────────────┐    │
│  │  VxRail Manager                                                         │    │
│  │  mystic password rotated │ LDAP ► AD groups ► roles │ API on jump hosts │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                    │                                            │
│  ┌─────────────────────────────────▼───────────────────────────────────────┐    │
│  │  Network                                                                │    │
│  │  Mgmt / vSAN / vMotion / iDRAC on separate VLANs │ NSX DFW (optional)  │     │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Security Model Overview

VxRail security combines vSphere/vSAN security (managed through vCenter) with VxRail-specific controls (managed through VxRail Manager). The Dell hardware layer adds iDRAC security as a third dimension.

| Layer | Security Controls | Managed By |
|---|---|---|
| VxRail Manager | Admin accounts, API access, LCM access | VxRail Plugin / direct login |
| vSphere / vCenter | Roles, permissions, lockdown mode, host profiles | vCenter |
| vSAN | Encryption, storage policies | vCenter / storage policy engine |
| iDRAC | Hardware OOB access, firmware security | iDRAC UI / RACADM CLI |
| Network | VLANs, firewall, NSX (if deployed) | Network team / NSX Manager |

---

## Authentication

### VxRail Manager Accounts

VxRail Manager has a local admin account (`mystic`) and supports LDAP integration.

**Change the default mystic password immediately after initial deployment:**

```bash
# SSH to VxRail Manager VM
ssh mystic@<vxrail-manager-ip>
passwd mystic
# Also update via VxRail Plugin: System → User Management
```

Store the new password in the organisation's secrets vault. The `mystic` account is the equivalent of an admin account — losing it requires Dell support-assisted recovery.

### LDAP Integration (Active Directory)

Configure AD authentication for VxRail Manager:

**VxRail Plugin → System → User Management → LDAP → Configure**

| Field | Example |
|---|---|
| LDAP URL | `ldaps://ldap.example.local:636` |
| Base DN | `DC=corp,DC=local` |
| Bind DN | `CN=vxrailbind,OU=ServiceAccounts,DC=corp,DC=local` |
| Admin Group | `CN=VxRail-Admins,OU=Groups,DC=corp,DC=local` |

Use LDAPS (port 636, TLS) rather than plain LDAP (port 389). Test connectivity before saving.

### vCenter Authentication

vCenter authentication for the VxRail cluster follows standard vSphere RBAC. See the vCenter security pages for SSO and LDAP configuration.

The VxRail Plugin requires specific vCenter permissions to operate. A dedicated vCenter service account (`vxrail-vc-svc`) should be configured with the minimum required permissions rather than using `administrator@vsphere.local`.

```powershell
# PowerCLI — create a custom role for VxRail Manager vCenter integration
New-VIRole -Name "VxRail-Manager-Role" -Privilege (
    Get-VIPrivilege -Id @(
        "Host.Configuration.StoragePartitionConfiguration",
        "Host.Configuration.NetConfig",
        "Host.Configuration.FirmwareConfig",
        "VirtualMachine.Config.AddExistingDisk",
        "Datastore.Move",
        "Global.Health"
    )
)

# Assign role to the VxRail service account on the datacenter
New-VIPermission \
    -Entity (Get-Datacenter "DC-PROD") \
    -Principal "CORP\vxrail-vc-svc" \
    -Role "VxRail-Manager-Role" \
    -Propagate $true
```

### iDRAC Authentication

Each VxRail node has an iDRAC with its own authentication. Factory default credentials (`root` / `Calvin`) must be changed before connecting to the production network.

```bash
# Via RACADM — change iDRAC root password
racadm set iDRAC.Users.2.Password "NewStr0ngP@ss!!"

# Or configure LDAP/AD on iDRAC for centralised auth:
racadm set iDRAC.LDAP.Enable Enabled
racadm set iDRAC.LDAP.Server "ldap.example.local"
racadm set iDRAC.LDAP.BaseDN "DC=corp,DC=local"
```

iDRAC access should be restricted to a dedicated OOB management network — not reachable from VM subnets.

---

## Access Control

### VxRail Manager Roles

| Role | Permissions |
|---|---|
| Admin (mystic) | Full VxRail Manager access including LCM |
| Read-only (if LDAP configured) | View cluster health, no changes |

LDAP group-based role assignment allows mapping AD groups to VxRail Manager access levels.

### vSphere RBAC for VxRail Operations

Define vCenter roles for VxRail-specific operational tasks:

| Team | vCenter Role | Scope |
|---|---|---|
| VxRail Administrators | Administrator | VxRail Cluster object |
| Storage Operations | Custom (vSAN ops) | Cluster level |
| Application / VM Owners | VM Operator (custom) | VM Folder / Resource Pool |
| Read-only / Monitoring | Read-only | Datacenter |

### Host Lockdown Mode

Apply Normal Lockdown mode to all VxRail ESXi hosts. VxRail Manager requires connectivity to the hosts for LCM operations — this is handled via the vCenter API path, which is permitted under Normal Lockdown.

```powershell
# Enable Normal Lockdown on all VxRail hosts
Get-Cluster "VxRail-Cluster" | Get-VMHost | ForEach-Object {
    $_.ExtensionData.EnterLockdownMode()
    Write-Host "Lockdown enabled: $($_.Name)"
}
```

**Exception users**: Add the VxRail Manager service account to the ESXi exception list if VxRail Manager needs direct host access (required for certain LCM operations). Review VxRail documentation for the specific version.

---

## Encryption

### vSAN Data-at-Rest Encryption

Enable vSAN encryption to protect data stored on node disks. Requires a Key Management Server (KMS) or vCenter Native Key Provider.

**vCenter → Cluster → Configure → vSAN → Services → Encryption → Enable**

```powershell
# Enable vSAN encryption (PowerCLI)
# Ensure a KMS or NKP is already configured in vCenter
Set-VsanClusterConfiguration -Cluster "VxRail-Cluster" -EncryptionEnabled $true
```

**Warning**: Enabling vSAN encryption on an existing cluster triggers a full disk reformat (data rebuild). This takes several hours depending on the amount of data. Ensure the cluster has sufficient capacity to tolerate nodes being in rebuild state.

Before enabling:
- Confirm VxRail cluster has enough available capacity (>25% free)
- Schedule a maintenance window
- Back up all critical VMs
- Confirm the KMS/NKP is healthy and accessible

### vSAN Data-in-Transit Encryption

Encrypts vSAN network traffic between nodes. Does not require a KMS. Enables without a full data rebuild.

**vCenter → Cluster → Configure → vSAN → Services → In-Transit Encryption → Enable**

Enable this on all production VxRail clusters — the overhead is minimal on modern hardware (AES-NI accelerated).

### iDRAC Secure Boot and Firmware Verification

Ensure iDRAC Secure Boot is enabled to verify firmware signatures:

```bash
# Check Secure Boot status via RACADM
racadm get BIOS.SysProfileSettings.SecureBoot
# Expected: Enabled

# Check iDRAC firmware version
racadm getversion -f idrac
```

Keep iDRAC firmware current — Dell includes iDRAC firmware updates in VxRail LCM bundles, so staying on current LCM versions addresses iDRAC CVEs automatically.

---

## Hardening Checklist

### VxRail Manager

- [ ] `mystic` default password changed; password stored in vault
- [ ] LDAP configured; AD groups mapped to VxRail Manager roles
- [ ] API access restricted to admin jump hosts at network layer
- [ ] SSH to VxRail Manager VM restricted to admin jump hosts (port 22)
- [ ] VxRail Manager VM backed up (not just snapshot)

### iDRAC (Per Node)

- [ ] Default `root`/`Calvin` credentials changed on all iDRAC interfaces
- [ ] iDRAC IP reachable only from OOB management network (not from VM subnets)
- [ ] iDRAC LDAP configured for centralised authentication
- [ ] iDRAC firmware current (managed via VxRail LCM bundles)
- [ ] iDRAC Secure Boot enabled

### vSphere / ESXi

- [ ] Normal Lockdown Mode enabled on all VxRail hosts
- [ ] SSH disabled on all hosts (`TSM-SSH` service stopped)
- [ ] ESXi Shell disabled (`TSM` service stopped)
- [ ] Host profiles applied and all hosts compliant
- [ ] vSAN data-at-rest encryption enabled (if required by data classification)
- [ ] vSAN in-transit encryption enabled
- [ ] vCenter backup current (VAMI, daily)
- [ ] NKP backup downloaded and stored securely (if using Native Key Provider)

### Network

- [ ] Management network segregated from VM networks (separate VLANs)
- [ ] vSAN network not reachable from VM subnets
- [ ] iDRAC on dedicated OOB VLAN
- [ ] vCenter VAMI port 5480 restricted to admin subnets
- [ ] NSX DFW rules applied if NSX is deployed on the VxRail cluster

---

## Dell SupportAssist / Secure Remote Services

Dell SupportAssist provides proactive monitoring and automated case creation for VxRail hardware faults. When enabled, Dell receives hardware telemetry from iDRAC and can proactively dispatch parts.

Enable SupportAssist: **VxRail Plugin → Support → SupportAssist → Enable**

Security considerations:
- SupportAssist communicates outbound to Dell's cloud (no inbound connection required)
- All data is transmitted over TLS
- Limit the types of data shared to hardware health only (not application-level data)
- Review and confirm data sharing scope before enabling in regulated environments (PCI, HIPAA)

```bash
# Check SupportAssist status via API
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxrail-manager-ip>/rest/vxm/v1/support-assist/status"
```
