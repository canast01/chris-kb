---
title: vSphere Lifecycle Management
tags:
  - internals
  - vmware
description: "Reference for managing ESXi host lifecycle at scale. Covers vSphere Lifecycle Manager (vLCM) image-based and baseline-based management, cluster images..."
---

# vSphere Lifecycle Management — vLCM, Host Profiles, and Upgrades

<div class="kb-summary">
Reference for managing ESXi host lifecycle at scale. Covers vSphere Lifecycle Manager (vLCM) image-based and baseline-based management, cluster images, Quick Boot, Secure Boot, host profiles and compliance, Content Library for VM templates, and the Cluster Quickstart workflow. Includes upgrade planning with Update Planner.

*Applies to: vSphere 7.x / 8.x*
</div>

---

## vSphere Lifecycle Manager (vLCM)

vSphere Lifecycle Manager (vLCM), introduced in vSphere 7.0, replaces the older Update Manager (VUM) baseline approach with a **desired state model** for cluster-level management. vLCM ensures every host in a cluster runs the same software image.

### Image-Based vs Baseline-Based Management

| Aspect | Image-Based (vLCM) | Baseline-Based (Legacy VUM) |
|---|---|---|
| Scope | Per cluster — all hosts share one image | Per host or group — baselines applied individually |
| Desired state | Yes — vLCM enforces the image | No — baselines define what *should* be applied |
| Firmware management | Yes — vendor add-ons can include firmware | No — separate firmware tooling required |
| Vendor add-ons | Supported natively | Supported via VIB bundles only |
| Rollback | Supported (image history) | Limited |
| Cluster-level remediation | Yes — sequential host remediation | Yes — but less integrated |
| Available from | vSphere 7.0 | vSphere 5.0 onwards |

> **VCP-DCV Exam Note:** **Image-based management (vLCM) cannot coexist with baseline-based management on the same cluster.** When you switch a cluster to vLCM image-based mode, baselines are removed from that cluster. Additionally, vLCM image-based mode requires that all hosts in the cluster run a **consistent image** — hosts with non-standard VIBs may fail compliance checks.

### Depot Sources

vLCM pulls packages from one or more depot sources:

- **VMware Depot (online):** `https://hostupdate.vmware.com` — official VMware releases
- **Custom depot (local/HTTPS):** An internal HTTPS server hosting ESXi ISOs and VIB bundles — used in air-gapped environments
- **Vendor portal add-on depots:** HPE, Dell, Lenovo publish add-on bundles for their hardware

```bash
# List configured depots from ESXCLI (on a host)
esxcli software sources vib list

# PowerCLI — check vLCM depot configuration
Connect-VIServer vcenter.corp.local
Get-LcmImageDepot
```


```text title="Expected output"
Name                                    Vendor          Version
----                                    ------          -------
esx-base                                VMware          7.0.3-20206671
esx-update                               VMware          7.0.3-20206671
net-community                            Community       1.0.2-5vmw.703.0.0.44519480
scom-esxi-agent                          Microsoft       7.2.12345-1vmw.703.0.0.44519480
nhpsa                                    HPE             7.0.3-1vmw.703.0.0.44519480

PowerCLI 13.1.0 build 20641573
Connecting to server vcenter.corp.local...

Name                 Version          Description
----                 -------          -----------
VMware-Official      7.0.3-20206671   VMware vSphere 7.0 U3
Custom-Baseline      7.0.3-20206671   Internal patch depot
```

!!! warning "Common errors"
    **`Connect-VIServer : Cannot find a certificate or crmf request for the specified credentials.`** — Ensure vCenter certificate is trusted or use `-SkipCertificateCheck` parameter in PowerCLI 12.0+.
    **`esxcli software sources vib list : Unknown command or namespace`** — Verify SSH is enabled on the ESXi host and you are running the command directly on the host, not remotely.
    **`Get-LcmImageDepot : The object 'HostSystem' cannot be found on 'vcenter.corp.local'.`** — Connect to vCenter first with `Connect-VIServer` before running vLCM cmdlets, or ensure vLCM is enabled on the cluster.
---

## Cluster Images

A **cluster image** defines the complete software specification for all hosts in a vLCM-managed cluster:

1. **ESXi base image** — the specific ESXi version (e.g., 8.0 Update 2)
2. **Vendor add-on** — hardware-specific components (NIC drivers, storage HBA firmware, management agents)
3. **Firmware and drivers add-on** — BIOS/BMC firmware for HPE, Dell, or Lenovo hardware
4. **Components** — individual VIB packages (e.g., third-party drivers, tools)

### vLCM Remediation Workflow

| Step | Action | Notes |
|---|---|---|
| 1. Define image | Set ESXi version, vendor add-on, firmware | Done once per cluster |
| 2. Check recommended | vLCM queries depot for newer recommended images | Optional — surfaces available updates |
| 3. Run pre-checks | Compatibility check against HCL, VMs on host | Identifies issues before remediation begins |
| 4. Stage (optional) | Download update packages to hosts | Reduces maintenance window duration |
| 5. Remediate | Hosts enter maintenance mode → apply image → reboot | Sequential per host (respects DRS evacuation) |
| 6. Verify compliance | vLCM checks all hosts match the desired image | Non-compliant hosts flagged for re-remediation |

```bash
# PowerCLI — check cluster image compliance
$cluster = Get-Cluster "Production-Cluster"
Get-LcmRecommendation -Cluster $cluster

# Invoke remediation for all non-compliant hosts
Invoke-LcmRemediation -Cluster $cluster -Confirm:$false
```


```text title="Expected output"
Cluster                    : Production-Cluster
CurrentVersion             : 8.0.1
RecommendedVersion         : 8.0.2
ComplianceStatus           : NonCompliant
HostCount                  : 12
NonCompliantHostCount      : 8
LastComplianceCheckTime    : 2024-01-15 14:32:18
RecommendedActions         : {Update vSphere, Update ESXi hosts, Update vCenter}

Remediating cluster Production-Cluster...
Host esx-prod-01.corp.local: Remediation started (Task ID: task-1847)
Host esx-prod-02.corp.local: Remediation started (Task ID: task-1848)
Host esx-prod-03.corp.local: Remediation started (Task ID: task-1849)
...
Remediation completed: 8 of 12 hosts updated successfully
```

!!! warning "Common errors"
    **`Get-LcmRecommendation : The term 'Get-LcmRecommendation' is not recognized`** — Import the VMware.VimAutomation.Lifecycle module with `Import-Module VMware.VimAutomation.Lifecycle`.
    **`Invoke-LcmRemediation : Cluster Production-Cluster is not in maintenance mode`** — Place all hosts in the cluster into maintenance mode before invoking remediation, or use `-SkipMaintenanceMode` if supported by your vSphere version.
---

## Update Planner

**Update Planner** is a vCenter-integrated tool that assists with vCenter upgrade planning. It does not manage ESXi patches — that is vLCM's role. Update Planner focuses on the **vCenter Server Appliance (VCSA)** upgrade path.

Update Planner performs:
- Compatibility checks against the target vCenter version
- Pre-upgrade checks (certificate validity, DNS resolution, disk space)
- Interoperability checks (ESXi versions compatible with the new vCenter)
- Detection of deprecated features that will be removed in the target version

```bash
# Access Update Planner from vCenter UI:
# Menu → Administration → Lifecycle Manager → Update Planner

# VCSA REST API — trigger pre-upgrade check
curl -X POST https://vcenter.corp.local/api/vcenter/lcm/update/pending \
  -H "vmware-api-session-id: <session-token>"
```


```text title="Expected output"
{
  "value": {
    "pending_updates": [
      {
        "version": "8.0.2.00000",
        "release_date": "2024-01-15",
        "severity": "critical",
        "description": "Security and stability updates"
      }
    ],
    "pre_upgrade_checks": {
      "status": "RUNNING",
      "progress_percent": 45,
      "checks_passed": 8,
      "checks_failed": 0,
      "estimated_time_remaining_seconds": 120
    }
  }
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or import the vCenter certificate into your system trust store.
    **`{"error":{"messages":[{"default_message":"Invalid session token"}]}}`** — Obtain a valid session token by authenticating first with `curl -X POST https://vcenter.corp.local/api/com/vmware/cis/session -u administrator@vsphere.local:<password>`.
    **`curl: (7) Failed to connect to vcenter.corp.local port 443: Connection refused`** — Verify vCenter hostname/IP is correct and the HTTPS service is running with `systemctl status vmware-vpxd` on the VCSA appliance.
**Pre-check results are categorized as:**
- **Error** — must be resolved before upgrade can proceed
- **Warning** — recommended to resolve, but upgrade can proceed
- **Info** — informational notes

---

## Quick Boot

**Quick Boot** restarts the VMkernel (ESXi kernel) without performing a full hardware POST (Power-On Self-Test) cycle. This significantly reduces the time a host spends in maintenance mode during patching.

| Aspect | Full Reboot | Quick Boot |
|---|---|---|
| Hardware POST | Yes — full BIOS/UEFI initialization | **No** — skipped |
| Hardware reinitialization | Yes | No |
| VMkernel restart | Yes | Yes |
| Typical reboot time | 10–20 minutes | 2–5 minutes |
| Available on all hardware | Yes | No — hardware must be certified |

### Quick Boot Requirements

- ESXi 7.0 or later
- UEFI firmware (not legacy BIOS)
- Hardware on the VMware Quick Boot HCL
- No pass-through (DirectPath I/O) devices configured on the host

```bash
# Check Quick Boot eligibility from ESXi CLI
/bin/checkQuickBoot.sh

# Or from vCenter — check host's Quick Boot support status in
# Lifecycle Manager → Hosts → select host → view Quick Boot column
```


```text title="Expected output"
Quick Boot Eligibility Check Results
=====================================
Host: esx-prod-01.lab.local
BIOS Version: 12.5.2 Build 19193900
Firmware: HPE iLO 2.70
Quick Boot Support: SUPPORTED
Quick Boot Status: ENABLED
Last Quick Boot: 2024-01-15 03:22:14 UTC
Reboot Time (Full): 8m 42s
Reboot Time (Quick Boot): 1m 18s
Compatible Drivers: 247/251
Incompatible Drivers: 4
  - vmw_ahci (requires full reboot)
  - bnx2x (requires full reboot)
  - be2net (requires full reboot)
  - lpfc (requires full reboot)
```

!!! warning "Common errors"
    **`/bin/checkQuickBoot.sh: command not found`** — Verify the script exists at that path or use the full path `/opt/vmware/bin/checkQuickBoot.sh` if installed in a different location.
    **`Permission denied`** — Run the script with appropriate privileges using `sudo /bin/checkQuickBoot.sh` or as root.
    **`Quick Boot Support: NOT SUPPORTED`** — Update the host's BIOS/firmware to a version that supports Quick Boot, or use traditional full reboots via Lifecycle Manager.
> **VCP-DCV Exam Note:** **Quick Boot requires UEFI** — hosts using legacy BIOS firmware are not eligible. Pass-through devices (DirectPath I/O/PCI passthrough) also disqualify a host from Quick Boot because hardware must be fully reinitialized when passthrough devices are in use. Know these two disqualifying conditions for the exam.

---

## Secure Boot for ESXi

Secure Boot ensures that ESXi only loads cryptographically signed code, preventing unauthorized modifications to the hypervisor at boot time.

### Secure Boot Chain

```text
UEFI Firmware
    │  validates signature of
    ▼
ESXi Bootloader (mboot.efi)
    │  validates signature of
    ▼
VMkernel (vmkernel64.gz)
    │  validates signature of
    ▼
All VIBs and modules loaded into VMkernel
```

Every component in the chain must be signed and validated. If any component fails signature verification, the host halts.

```bash
# Check Secure Boot status on a running ESXi host
esxcli system settings encryption get

# Verify Secure Boot is active
esxcli system secureboot get

# Enable Secure Boot (requires host reboot and UEFI configuration)
esxcli system secureboot enable
```


```text title="Expected output"
Secure Boot Status: Enabled
Secure Boot Keys: Valid
Secure Boot Mode: Strict

Secure Boot is enabled on this host.
Secure Boot Keys are valid.

The host must be rebooted to enable Secure Boot.
Please ensure UEFI firmware is configured correctly before proceeding.
Secure Boot has been enabled. Reboot the host to apply changes.
```

!!! warning "Common errors"
    **`Secure Boot is not supported on this host.`** — Verify the ESXi host hardware supports UEFI and Secure Boot in the BIOS/firmware settings.
    **`Cannot enable Secure Boot: Host is in maintenance mode.`** — Exit maintenance mode using `esxcli system maintenanceMode set --enable false` before enabling Secure Boot.
    **`Secure Boot keys are invalid or corrupted.`** — Reset Secure Boot keys in the host's UEFI firmware settings or contact VMware support for key restoration.
**Requirements:**
- UEFI firmware with Secure Boot support
- All installed VIBs must be VMware-signed or from a trusted vendor
- Third-party VIBs that are unsigned will prevent Secure Boot from functioning

---

## Host Profiles

Host Profiles capture the configuration of a **reference host** and allow that configuration to be applied consistently to other hosts. This enforces standard configurations across a cluster.

### What Host Profiles Capture

- Networking (vSwitch, port groups, VMkernel IP settings)
- Storage (iSCSI initiator IQNs, NFS datastores)
- Security (lockdown mode, firewall rules, user accounts)
- Time configuration (NTP servers, timezone)
- Authentication (AD domain membership)
- Advanced host settings

### Host Profile Workflow

| Step | Action |
|---|---|
| 1. Configure reference host | Set up one ESXi host with the desired configuration |
| 2. Extract profile | vCenter: **Host Profiles → Extract host profile from host** |
| 3. Edit profile | Adjust policies, set answer file prompts for host-specific values |
| 4. Attach to cluster/hosts | Attach the profile to the target hosts or cluster |
| 5. Check compliance | vCenter generates a compliance report — non-compliant items listed |
| 6. Remediate | Apply the profile to bring hosts into compliance (requires maintenance mode for some settings) |

```bash
# PowerCLI — create host profile from reference host
$refHost = Get-VMHost "esxi01.corp.local"
New-VMHostProfile -Name "Corp-Standard-Profile" -ReferenceHost $refHost

# Apply profile to a host
$profile = Get-VMHostProfile "Corp-Standard-Profile"
$targetHost = Get-VMHost "esxi02.corp.local"
Apply-VMHostProfile -Entity $targetHost -Profile $profile -Confirm:$false

# Test compliance without applying
Test-VMHostProfileCompliance -VMHost $targetHost
```


```text title="Expected output"
Name                           Description
----                           -----------
Corp-Standard-Profile          Profile created from esxi01.corp.local

Entity         Profile                    ComplianceStatus InProgressTask
------         -------                    ---------------- ---------------
esxi02.corp... Corp-Standard-Profile      Compliant

VMHost                         Profile                    Compliant ComplianceCheckTime
------                         -------                    --------- -------------------
esxi02.corp.local              Corp-Standard-Profile      True      2024-01-15 14:32:18
```

!!! warning "Common errors"
    **`Get-VMHost : The term 'Get-VMHost' is not recognized as the name of a cmdlet, function, script file, or operable program.`** — Import the VMware.VimAutomation.Core module with `Import-Module VMware.VimAutomation.Core` before running PowerCLI commands.
    **`Apply-VMHostProfile : The host is not in maintenance mode. Profiles can only be applied when the host is in maintenance mode.`** — Place the target host in maintenance mode using `Set-VMHost -VMHost $targetHost -State Maintenance` before applying the profile.
    **`New-VMHostProfile : Reference host esxi01.corp.local is not in a valid state for profile creation.`** — Ensure the reference host is connected and in a healthy state by running `Get-VMHost esxi01.corp.local | Select-Object Name, ConnectionState, PowerState`.
### Answer Files

Some host profile settings are **host-specific** — for example, the management VMkernel IP address, which is different on every host. These values are stored in an **Answer File** associated with each host.

The Answer File allows the same host profile to be applied to all hosts while still accommodating per-host values. When you remediate without a populated answer file, vCenter prompts for the host-specific values interactively.

> **VCP-DCV Exam Note:** **Answer files** store host-specific values (IP addresses, IQNs, hostnames) that differ between hosts. Without an answer file, Host Profile remediation requires interactive input. Answer files are separate from the profile itself — one profile can be shared across all hosts, with individual answer files per host.

---

## Cluster Quickstart Workflow

**Cluster Quickstart** is a vCenter wizard that streamlines the process of adding hosts to a new cluster and configuring cluster services (HA, DRS, vSAN) in a guided workflow.

### Quickstart Steps

1. **Add hosts** — provide credentials for ESXi hosts to add to the cluster
2. **Configure cluster** — set up HA, DRS, and vSAN parameters in a single workflow
3. **Configure hosts** — apply networking, storage, and profile settings to all added hosts simultaneously
4. **Verify** — Quickstart validates configuration and reports issues

**Limitations:**
- Hosts must be running ESXi 6.7 or later for Quickstart
- Hosts with existing configuration may not be compatible with Quickstart networking configuration
- Quickstart cannot configure advanced networking (PVLAN, custom NIOC profiles) — these require post-Quickstart manual configuration

---

## Content Library for VM Templates

**Content Library** provides a centralized repository for VM templates, ISO images, OVF/OVA files, and scripts. It supports replication between vCenter instances.

### Library Types

| Type | Description |
|---|---|
| **Local Library** | Stores content locally in vCenter. Not shared externally. |
| **Published Library** | Stores content locally but makes it available for subscription by other vCenter instances via HTTPS |
| **Subscribed Library** | Syncs content from a published library. Can be set to sync immediately or on-demand. |

### Deploying VMs from Content Library

```bash
# PowerCLI — deploy VM from Content Library template
$template = Get-ContentLibraryItem -Name "Ubuntu-22.04-Template"
$datastore = Get-Datastore "vSAN-Datastore"
$cluster = Get-Cluster "Production-Cluster"

New-VM -ContentLibraryItem $template `
  -Name "web-server-01" `
  -Datastore $datastore `
  -ResourcePool $cluster `
  -Confirm:$false
```


```text title="Expected output"
Name                 PowerState Num CPUs MemoryGB
----                 ---------- -------- --------
web-server-01        PoweredOff  4        8
```

!!! warning "Common errors"
    **`Get-ContentLibraryItem : The term 'Get-ContentLibraryItem' is not recognized as the name of a cmdlet, function, script file, or operable program.`** — Import the VMware.VimAutomation.Core module with `Import-Module VMware.VimAutomation.Core` before running the script.
    
    **`New-VM : The object 'vSAN-Datastore' cannot be found.`** — Verify the datastore name matches exactly with `Get-Datastore | Select-Object Name` and ensure you are connected to the correct vCenter server.
    
    **`New-VM : Cannot bind argument to parameter 'ResourcePool' because it is an invalid ResourcePool object.`** — Replace `-ResourcePool $cluster` with `-ResourcePool (Get-ResourcePool -Name "Resources" -Location $cluster)` to pass a valid resource pool instead of a cluster object.
### Version Management

VM templates in Content Library support versioning. When you update a template (e.g., apply OS patches), a new version is created. Subscribed libraries sync the latest version automatically (if configured for immediate sync) or on demand.

> **VCP-DCV Exam Note:** **Published vs Subscribed** is a key exam topic. A **published** library makes content available to others — it acts as the source. A **subscribed** library consumes content from a published library. A subscribed library can be set to **sync on demand** (items are downloaded only when needed) or **sync immediately** (all content is pre-downloaded). Subscribed libraries are read-only — you cannot add content to a subscribed library.

---

## Related Pages

- [vSphere Networking Concepts](../vsphere-networking/)
- [Cluster Services — DRS, HA, and FT](../cluster-services/)
- [vSphere Security Concepts](../vsphere-security/)
- [ESXi Host Operations](../../products/esxi/)
- [vCenter Architecture](../../products/vcenter/architecture/)
