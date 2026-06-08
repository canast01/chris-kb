---
title: vSphere Lifecycle Management
---

# vSphere Lifecycle Management — vLCM, Host Profiles, and Upgrades

<div class="kb-summary">
Reference for managing ESXi host lifecycle at scale. Covers vSphere Lifecycle Manager (vLCM) image-based and baseline-based management, cluster images, Quick Boot, Secure Boot, host profiles and compliance, Content Library for VM templates, and the Cluster Quickstart workflow. Includes upgrade planning with Update Planner.
</div>

```text
┌──────────────────────── vSphere Lifecycle Manager — Desired State ────────────────────────────────────┐
│                                                                                                       │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐         │
│  │  Cluster Image (Desired State)                                                           │         │
│  │  ESXi base version · Vendor add-ons (HPE, Dell, Lenovo) · Firmware packages             │          │
│  │  Components: VIBs, drivers, management agents — locked to specific versions              │         │
│  └────────────────────────────────────┬─────────────────────────────────────────────────────┘         │
│                                       │ Remediation                                                   │
│              ┌────────────────────────▼────────────────────────┐                                      │
│              │  ESXi Host 1   │  ESXi Host 2   │  ESXi Host 3  │                                      │
│              │  Compliant     │  Non-Compliant  │  Compliant    │                                     │
│              │                │  → Auto-patch   │               │                                     │
│              └────────────────────────────────────────────────┘                                       │
│                                                                                                       │
│  vLCM pulls updates from VMware Depot or custom depot (HTTPS/local)                                   │
│  Remediation: Enter maintenance mode → update → Quick Boot (if eligible) → exit maintenance           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

### Version Management

VM templates in Content Library support versioning. When you update a template (e.g., apply OS patches), a new version is created. Subscribed libraries sync the latest version automatically (if configured for immediate sync) or on demand.

> **VCP-DCV Exam Note:** **Published vs Subscribed** is a key exam topic. A **published** library makes content available to others — it acts as the source. A **subscribed** library consumes content from a published library. A subscribed library can be set to **sync on demand** (items are downloaded only when needed) or **sync immediately** (all content is pre-downloaded). Subscribed libraries are read-only — you cannot add content to a subscribed library.

---

## Related Pages

- [vSphere Networking Concepts](../vsphere-networking/)
- [Cluster Services — DRS, HA, and FT](../cluster-services/)
- [vSphere Security Concepts](../vsphere-security/)
- [ESXi Host Operations](../../esxi/)
- [vCenter Architecture](../../vcenter/architecture/)
