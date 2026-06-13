---
tags:
  - security
  - vmware
  - vxrail
---
# VxRail — Hardening

<div class="kb-summary">
Hardening checklist and procedures for VxRail in the VMware product context. Covers VxRail Manager, iDRAC per-node, vSphere/ESXi, network hardening, and SupportAssist security considerations.

*Applies to: VxRail 7.x / 8.x*
</div>

```text
┌───────────────────────────────────────── VxRail — Hardening ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         VxRail Manager: mystic changed, LDAP configured, API and SSH restricted                │  │
│   │         iDRAC per node: root/Calvin replaced, OOB VLAN only, LDAP, firmware current           │   │
│   │         ESXi: Normal Lockdown, SSH disabled, Shell disabled, host profiles compliant           │  │
│   │         Network: VLAN segregation, vSAN isolated, iDRAC OOB only, VAMI port restricted        │   │
│   │         SupportAssist: outbound TLS only, data scope reviewed, regulated-env check done       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Each layer hardened independently · defence in depth · checklist drives consistency                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       VxRail Manager        │  │        iDRAC / Hardware      │  │      vSphere / ESXi         │  │
│   │   mystic → vault password   │  │   root/Calvin → replace     │  │   Normal Lockdown all hosts  │  │
│   │   LDAP AD group mapping     │  │   OOB VLAN restriction       │  │   SSH disabled TSM-SSH      │  │
│   │   API → jump hosts only     │  │   LDAP centralised auth      │  │   ESXi Shell disabled TSM   │  │
│   │   SSH → jump hosts only     │  │   FW current via LCM         │  │   Host profiles compliant   │  │
│   │   VM backup (not snapshot)  │  │   Secure Boot enabled        │  │   vSAN encryption enabled   │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Manager creds in vault · iDRAC on OOB · ESXi managed via vCenter only                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   VxRail Mgr    │      iDRAC         │   vSphere/ESXi   │    Network       │  SupportAssist  │    │
│   │  mystic vault   │  root → changed    │  Lockdown: Norm  │  VLAN segments   │  Outbound only  │    │
│   │  LDAP groups    │  OOB VLAN only     │  SSH: disabled   │  vSAN isolated   │  TLS encrypted  │    │
│   │  API jump host  │  LDAP AD groups    │  Shell: disabled │  iDRAC OOB VLAN  │  Data scope chk │    │
│   │  SSH jump host  │  FW current LCM    │  Profiles: yes   │  VAMI restricted │  Regulated env  │    │
│   │  VM backup Veeam│  Secure Boot: on   │  vSAN encrypt    │  NSX DFW rules   │  No inbound     │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell PowerEdge servers · TPM 2.0 · iDRAC OOB NIC · ToR switches · VLANs · CA infrastructure          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  mystic              = VxRail Manager local admin account; must be vaulted and LDAP configured        │
│  root/Calvin         = Factory iDRAC credentials; unique per-node replacement mandatory               │
│  Normal Lockdown     = ESXi state forcing management through vCenter; DCUI accessible to exceptions   │
│  TSM-SSH             = ESXi Tech Support Mode SSH service; must be stopped and disabled               │
│  TSM                 = ESXi Tech Support Mode shell; must be stopped and disabled                     │
│  Host Profile        = vCenter configuration template enforcing security, NTP, syslog baselines       │
│  OOB VLAN            = Out-of-band VLAN; iDRAC IPs reachable only from NOC and jump hosts             │
│  VAMI                = vCenter Appliance Management Interface; port 5480; admin-subnet only           │
│  NSX DFW             = NSX Distributed Firewall; micro-segmentation for VM-to-VM traffic              │
│  SupportAssist       = Dell proactive support tool; outbound TLS to Dell cloud; no inbound            │
│  LCM                 = Lifecycle Manager; VxRail upgrade system managing FW, ESXi, and vCenter        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## VxRail Manager Hardening

### Checklist

- [ ] `mystic` default password changed; stored in secrets vault
- [ ] LDAP configured against AD; AD groups mapped to VxRail Manager roles
- [ ] VxRail Manager API access (port 443) restricted to admin jump hosts at network layer
- [ ] SSH access to VxRail Manager VM (port 22) restricted to admin jump hosts
- [ ] VxRail Manager VM backed up with Veeam or equivalent (not just snapshot); daily, retained 14 days
- [ ] TLS certificate replaced with CA-signed certificate (not self-signed)
- [ ] `mystic` account restricted to break-glass use only after LDAP is operational

### Step-by-Step Procedure

**1 — Change the mystic password**

```bash
# Change mystic password via VxRail Manager API
curl -sk \
  -X PUT \
  -H "Authorization: Basic $(echo -n 'mystic:CurrentPassword1!' | base64)" \
  -H "Content-Type: application/json" \
  -d '{"password": "NewVaultedPassword1!"}' \
  "https://<vxrail-manager-ip>/rest/vxm/v1/system/user/password"
```

Store the new password in the vault immediately. Document the vault path in the VxRail runbook.

**2 — Configure LDAP**

VxRail Plugin → Settings → LDAP Configuration → Enable LDAP → Enter server, base DN, bind account details, and role group mappings. Refer to the [Authentication](authentication/) page for the full LDAP configuration reference.

**3 — Restrict API access at network layer**

On the management network firewall or switch ACL:

```bash
# Permit VxRail Manager API access from jump host subnet only
# Source: 10.0.200.0/24 (admin jump hosts)
# Destination: <vxrail-manager-ip>, port 443
# Action: PERMIT
# All other sources to port 443 on VxRail Manager: DENY
```

**4 — Restrict SSH access**

On the management network firewall:

```bash
# Permit SSH to VxRail Manager VM from jump host subnet only
# Source: 10.0.200.0/24
# Destination: <vxrail-manager-ip>, port 22
# Action: PERMIT
# All other sources to port 22: DENY
```

**5 — Configure VM backup**

Add the VxRail Manager VM to the Veeam backup job (or equivalent tool). Do not use vSAN snapshots as the primary backup method — snapshots degrade vSAN performance if left active and are not a substitute for off-cluster backup.

---

## iDRAC Hardening (Per Node)

Apply the following steps to every node in the VxRail cluster. Document completion per node in the build record.

### Checklist

- [ ] Default `root`/`Calvin` credentials changed; unique per-node password in vault
- [ ] iDRAC IP reachable only from OOB management VLAN — not from VM subnets or internet
- [ ] iDRAC LDAP configured for centralised authentication via AD
- [ ] iDRAC firmware current (managed automatically via VxRail LCM bundles)
- [ ] iDRAC Secure Boot enabled and verified via RACADM
- [ ] iDRAC HTTPS enforced; HTTP and Telnet disabled
- [ ] iDRAC SSL certificate replaced with CA-signed certificate

### Step-by-Step Procedure

**1 — Change root credentials (per node)**

```bash
# Change default root/Calvin credentials on iDRAC
racadm set iDRAC.Users.2.Password "UniqueNodePassword1!"

# Verify the username is root (user slot 2 on Dell iDRAC)
racadm get iDRAC.Users.2.UserName
# Expected: UserName=root
```

Use a unique password for each node — do not reuse the same password across all iDRAC interfaces. Store each per-node credential in the vault under a path that includes the node hostname or iDRAC IP.

**2 — Verify OOB VLAN restriction**

```bash
# Verify iDRAC IP is in the OOB VLAN range
racadm get iDRAC.IPv4.Address

# Confirm no routing exists from VM subnets to the OOB VLAN
# (verify on the network layer — router/firewall ACLs)
```

**3 — Configure iDRAC LDAP**

```bash
# Enable LDAP on iDRAC and map AD group to Administrator role
racadm set iDRAC.LDAP.Enable 1
racadm set iDRAC.LDAP.Server "ldap://dc01.example.local"
racadm set iDRAC.LDAP.BaseDN "DC=example,DC=local"
racadm set iDRAC.LDAP.BindDN "CN=svc-idrac,OU=ServiceAccounts,DC=example,DC=local"
racadm set iDRAC.LDAP.BindPassword "BindPassword1!"
racadm set iDRAC.LDAPRoleGroup.1.DN "CN=GRP-iDRAC-Admins,OU=VxRailGroups,DC=example,DC=local"
racadm set iDRAC.LDAPRoleGroup.1.Privilege 0x1FF
```

**4 — Verify iDRAC firmware currency**

iDRAC firmware is included in VxRail LCM bundles. Keeping the cluster on a current LCM version automatically keeps iDRAC firmware patched. Verify the current iDRAC firmware version:

```bash
racadm getversion -f idrac
# Compare against the expected version for the installed VxRail bundle
```

**5 — Verify Secure Boot**

```bash
# Check Secure Boot status
racadm get BIOS.SysProfileSettings.SecureBoot
# Expected: SecureBoot=Enabled

# If disabled, enable it (node will reboot to apply)
racadm set BIOS.SysProfileSettings.SecureBoot Enabled
racadm jobqueue create BIOS.Setup.1-1 -r pwrcycle -s TIME_NOW
```

**6 — Enforce HTTPS, disable HTTP and Telnet**

```bash
# Disable HTTP, leave HTTPS on port 443
racadm set iDRAC.Webserver.HttpPort 0
racadm set iDRAC.Webserver.HttpsPort 443
racadm set iDRAC.Serial.Enable 0
```

---

## vSphere/ESXi Hardening

### Checklist

- [ ] Normal Lockdown Mode enabled on all VxRail ESXi hosts
- [ ] SSH disabled on all hosts (`TSM-SSH` service stopped and startup type set to off)
- [ ] ESXi Shell disabled on all hosts (`TSM` service stopped and startup type set to off)
- [ ] Host profiles applied to all VxRail hosts and compliance check is green
- [ ] vSAN data-at-rest encryption enabled (required if data classification mandates it)
- [ ] vSAN in-transit encryption enabled
- [ ] vCenter file-based backup current (VAMI, daily schedule)
- [ ] NKP backup downloaded and stored in vault (if using Native Key Provider)
- [ ] vCenter administrator@vsphere.local password changed from default and vaulted
- [ ] AD identity source added to vCenter SSO; AD groups assigned vCenter roles

### Step-by-Step Procedure

**1 — Enable Normal Lockdown on all hosts**

```powershell
# Enable Normal Lockdown on all VxRail cluster hosts (PowerCLI)
Get-Cluster "VxRail-Cluster" | Get-VMHost | ForEach-Object {
    $_.ExtensionData.EnterLockdownMode()
    Write-Host "Lockdown enabled: $($_.Name)"
}
```

**2 — Disable SSH and ESXi Shell**

```powershell
# Stop and disable SSH and ESXi Shell on all VxRail hosts (PowerCLI)
Get-Cluster "VxRail-Cluster" | Get-VMHost | ForEach-Object {
    $vmhost = $_
    Get-VMHostService -VMHost $vmhost | Where-Object { $_.Key -in "TSM-SSH","TSM" } |
        ForEach-Object {
            Stop-VMHostService -HostService $_ -Confirm:$false
            Set-VMHostService -HostService $_ -Policy Off
            Write-Host "Service $($_.Key) stopped and disabled on $($vmhost.Name)"
        }
}
```

**3 — Apply host profiles**

Create a reference host profile from a known-good VxRail host:

**vCenter → Policy and Profiles → Host Profiles → Extract Host Profile → Select reference host**

Apply the profile to all VxRail hosts:

```powershell
# Apply host profile to all VxRail hosts and check compliance (PowerCLI)
$profile = Get-VMHostProfile -Name "VxRail-Baseline"

Get-Cluster "VxRail-Cluster" | Get-VMHost | ForEach-Object {
    Apply-VMHostProfile -Entity $_ -Profile $profile -Confirm:$false
}

# Check compliance for all hosts
Get-Cluster "VxRail-Cluster" | Get-VMHost | Test-VMHostProfileCompliance |
    Select-Object VMHost, ComplianceStatus, @{N="Issues"; E={$_.IncomplianceElementList.Count}}
```

**4 — Enable vSAN encryption**

Refer to the [Encryption](encryption/) page for the full vSAN at-rest and in-transit encryption procedures, including the pre-enable checklist and rebuild warning.

**5 — Configure vCenter backup**

**vCenter VAMI (port 5480) → Backup → Configure → Schedule**

```yaml
Protocol: SFTP
Backup location: sftp://backup.example.local/vcentre/
Username: svc-vcenter-backup
Frequency: Daily
Retain: 14 backups
Encrypt backup: Yes (set a password stored in vault)
```

---

## Network Hardening

### Checklist

- [ ] Management VLAN segregated from VM data VLANs (separate VLANs, no routing between them)
- [ ] vSAN VMkernel VLAN not reachable from VM subnets or application networks
- [ ] iDRAC on dedicated OOB VLAN — not routable from VM subnets or internet
- [ ] vCenter VAMI port 5480 restricted to admin subnets at firewall
- [ ] NSX Distributed Firewall rules applied if NSX is deployed on the VxRail cluster
- [ ] vMotion VLAN not reachable from VM subnets (vMotion traffic is unencrypted unless vSphere 7.0+)
- [ ] No split tunnelling on admin VPN that would allow routing from user devices to vSAN or iDRAC VLANs

### VLAN Segregation Architecture

The following VLANs must be present and isolated in a correctly hardened VxRail deployment:

| VLAN | Purpose | Routable from VM subnets? | Internet access? |
|---|---|---|---|
| Management | ESXi VMkernel mgmt, vCenter, VxRail Manager | No | No |
| vSAN | vSAN replication traffic between nodes | No | No |
| vMotion | VM live migration traffic | No | No |
| OOB (iDRAC) | iDRAC management interfaces, OOB only | No | No |
| VM Networks | Guest VM traffic — application workloads | N/A | As required |

**Verify VLAN isolation on the vDS:**

```powershell
# List all port groups and their VLAN IDs on the VxRail vDS (PowerCLI)
Get-VDSwitch | Get-VDPortgroup |
    Select-Object Name, VlanConfiguration, @{N="Ports"; E={$_.NumPorts}} |
    Sort-Object Name
```

Confirm no VM port group has the same VLAN ID as the management, vSAN, vMotion, or OOB VLANs.

### NSX Distributed Firewall Rules (if NSX deployed)

If NSX is deployed on the VxRail cluster, apply DFW rules to enforce micro-segmentation between workload tiers. At minimum, apply the following rules to the VxRail management VMs:

| Rule | Source | Destination | Port | Action |
|---|---|---|---|---|
| Allow VxRail Mgr API from jump hosts | Jump host SG | VxRail Manager SG | 443 | Allow |
| Allow vCenter from admin | Admin SG | vCenter SG | 443, 902 | Allow |
| Block inter-VM traffic to management | Any | VxRail Manager SG | Any | Drop |
| Block VM access to iDRAC VLAN | VM SG | OOB SG | Any | Drop |

Apply DFW rules as NSX Security Groups scoped to the relevant VMs — do not use IP-based rules that can be bypassed by changing a VM's IP address.

---

## SupportAssist Security Considerations

Dell SupportAssist provides proactive monitoring and automated case creation for VxRail hardware faults. When enabled, iDRAC sends hardware telemetry to Dell's cloud for proactive support.

### Security Profile

| Aspect | Detail |
|---|---|
| Connection direction | Outbound only from iDRAC to Dell cloud — no inbound connections required |
| Transport | TLS 1.2+ encrypted; Dell uses certificate pinning |
| Data sent | Hardware health telemetry: temperatures, fan speeds, power, disk SMART data |
| Data NOT sent | VM names, application data, guest OS data, user data |
| Dell access | Dell support staff can view hardware telemetry; no remote access to ESXi or VMs |

### Configuration

**Enable SupportAssist:** VxRail Plugin → Support → SupportAssist → Enable

```bash
# Check SupportAssist status via VxRail Manager API
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxrail-manager-ip>/rest/vxm/v1/support-assist/status"
```

### Hardening Actions

- [ ] Review the data sharing scope in VxRail Plugin → Support → SupportAssist → Data Privacy settings before enabling
- [ ] Confirm data sharing is limited to hardware health only — disable application-level data collection if present
- [ ] For regulated environments (PCI-DSS, HIPAA): obtain written approval from compliance team before enabling; document the data types shared and Dell's data handling commitments
- [ ] Verify SupportAssist traffic only routes to Dell's known cloud endpoints — check firewall logs after enabling to confirm no unexpected outbound connections
- [ ] Confirm iDRAC firmware is current before enabling SupportAssist — older iDRAC firmware versions have had vulnerabilities in the SupportAssist agent

### Regulated Environments (PCI, HIPAA)

In regulated environments, SupportAssist telemetry may need to be reviewed against compliance requirements before enabling. Key questions:

1. Does the telemetry include any data that could be classified as cardholder data or protected health information? (Answer: No — hardware telemetry only. Confirm with Dell's data handling documentation.)
2. Does enabling SupportAssist constitute a third-party data sharing agreement that requires DPA execution with Dell? (Check with your compliance officer.)
3. Can SupportAssist be scoped to specific clusters or nodes to avoid telemetry from systems storing regulated data?

If SupportAssist cannot be approved for regulated clusters, disable it on those clusters and rely on VxRail Manager's proactive health monitoring and manual support case creation for hardware issues.
