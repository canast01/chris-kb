---
tags:
  - reference
  - vmware
  - interoperability
  - compatibility
---
# VMware Interoperability and Compatibility Matrix

<div class="kb-summary">
Interoperability reference for VMware product combinations. Use this page before planning upgrades or deploying new products to confirm component compatibility. The authoritative source is the [VMware Product Interoperability Matrix](https://interopmatrix.vmware.com/) — always verify before purchasing or deploying.

*Applies to: vSphere 7.x / 8.x, NSX 4.x, VCF 5.x, Aria Suite 8.x*
</div>

```text
┌────────────────────────── VMware Interoperability — Component Compatibility ──────────────────────────┐
│                                                                                                       │
│  Check interopmatrix.vmware.com before every upgrade; ordering matters — upgrade                      │
│  vCenter before ESXi; NSX must be supported by the target vCenter version.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            vSphere Compatibility             │  │              NSX Compatibility              │   │
│   │       vCenter must be >= ESXi version        │  │         NSX 4.x: requires vSphere 7+        │   │
│   │          ESXi N-2 back from vCenter          │  │            NSX 3.x: vSphere 6.7+            │   │
│   │       Hardware version: compat matrix        │  │          NSX + VCF: locked versions         │   │
│   │       HCL: CPU, NIC, storage per ESXi        │  │         NSX edge: ESXi version match        │   │
│   │       VxRail: interop matrix separate        │  │         Upgrade: NSX before vCenter         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  VCF locks all component versions together; do not upgrade components standalone.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Aria Suite Compatibility           │  │            Horizon Compatibility            │   │
│   │          LCM manages Aria versions           │  │          Horizon: locked to vSphere         │   │
│   │        Aria 8.x: vSphere 7+ required         │  │        Agent: match Connection Server       │   │
│   │          IDM: upgrade first in Aria          │  │         Composer: must match Horizon        │   │
│   │       Ops -> Logs -> Automation order        │  │          HV: guest OS compat matrix         │   │
│   │        Guest OS: VMware compat guide         │  │        VCF + Horizon: verified combos       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  All components run as VMs on ESXi; hardware HCL governs physical compatibility;                      │
│  verify CPU microcode and NIC firmware against VMware HCL before upgrade.                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Interop Matrix   = interopmatrix.vmware.com; authoritative compat check                              │
│  HCL              = Hardware Compatibility List; CPU/NIC/storage per ESXi                             │
│  N-2 support      = ESXi can be up to 2 major versions below vCenter                                  │
│  VCF version lock = all VCF components pinned to BOM; no standalone upgrade                           │
│  BOM              = Bill of Materials; VCF release defines exact versions                             │
│  IDM              = Identity Manager; must be upgraded first in Aria Suite                            │
│  Hardware version = VM hardware version; caps features; raise before upgrade                          │
│  VxRail matrix    = separate interop matrix on Dell support site                                      │
│  NSX edge compat  = NSX Edge VM must match NSX Manager version                                        │
│  Horizon agent    = must match Connection Server within N-1                                           │
│  Guest OS compat  = VMware guest OS guide; OS versions per ESXi/tools                                 │
│  EOGS             = End of General Support; no new patches after this date                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Before you begin

- **Always verify on the official tool:** [interopmatrix.vmware.com](https://interopmatrix.vmware.com/) — the matrix below is a reference snapshot and may not reflect latest patches.
- When upgrading one component, check all dependent products in the matrix before proceeding.
- VCF bundles validated component versions — use VCF BOM for VCF deployments rather than mixing versions independently.

## vSphere 8.0 — Component Compatibility

| Component | Min Supported Version | Notes |
|---|---|---|
| NSX-T / NSX | NSX-T 3.2.x / NSX 4.x | NSX 4.x is current; 3.2 supported on vSphere 8.0 |
| vSAN | 8.0 (same build as vSphere) | vSAN version always matches vSphere version |
| SRM | 8.6+ | SRM 8.5 and earlier not supported on vSphere 8.0 |
| vSphere Replication | 8.6+ | Must match or exceed SRM version |
| Aria Operations | 8.12+ | 8.10 and earlier not supported on vSphere 8.0 |
| Aria Automation | 8.12+ | Requires vCenter 8.0 plug-in compatibility |
| Horizon | 8 (2206+) | Horizon 7.x not compatible with vSphere 8.0 |
| VCF | 5.0+ | VCF 4.x uses vSphere 7.0; not compatible with 8.0 SDDC |
| Tanzu (TKG) | TKG 2.x | TKG 1.x not supported on vSphere 8.0 Supervisor |

## vSphere 7.0 — Component Compatibility

| Component | Supported Versions | Notes |
|---|---|---|
| NSX-T | 3.0 – 3.2, NSX 4.x | NSX 4.x backward-compatible with vSphere 7.0 |
| vSAN | 7.0 (same build) | |
| SRM | 8.3 – 8.8 | |
| Aria Operations | 8.6 – 8.16 | |
| Aria Automation | 8.6 – 8.16 | |
| VCF | 4.3 – 4.5 | |

## VCF 5.x BOM (Bill of Materials)

VCF 5.x bundles specific validated versions — mixing outside the BOM is unsupported:

| Component | VCF 5.2 BOM Version |
|---|---|
| ESXi | 8.0 U3 |
| vCenter | 8.0 U3 |
| NSX | 4.2.x |
| vSAN | 8.0 U3 (auto — same as vSphere) |
| Aria Automation | 8.16.x |
| Aria Operations | 8.16.x |
| Aria Ops for Logs | 8.16.x |

> For the exact build numbers, consult the [VCF Release Notes](https://docs.vmware.com/en/VMware-Cloud-Foundation/) for your version.

## NSX Interoperability

| NSX Version | vSphere Min | vSphere Max | VCF |
|---|---|---|---|
| NSX 4.2 | vSphere 7.0 U3 | vSphere 8.0 U3 | VCF 5.2 |
| NSX 4.1 | vSphere 7.0 U2 | vSphere 8.0 U2 | VCF 5.1 |
| NSX-T 3.2 | vSphere 6.7 U3 | vSphere 8.0 U1 | VCF 4.5 |

## Hardware Compatibility (HCL)

- **ESXi HCL:** [vmware.com/resources/compatibility](https://www.vmware.com/resources/compatibility/search.php)
- **vSAN HCL:** [Separate HCL tool](https://www.vmware.com/resources/compatibility/search.php?deviceCategory=vsan) — required for vSAN support
- **NSX HCL:** NIC models must be on NSX HCL for N-VDS / VDS 7 uplinks

## Key Interoperability Rules

| Rule | Detail |
|---|---|
| vSAN version = vSphere version | Always identical build; cannot mix |
| NSX Manager ≥ ESXi version | NSX must be at same or higher than ESXi when upgrading |
| SRM requires paired vSphere versions | Both sites must run compatible vSphere versions |
| Aria Suite Lifecycle manages upgrades | Use LCM for all Aria product upgrades to maintain compatibility |
| VCF BOM is authoritative for VCF | Never upgrade individual components outside VCF LCM |

## See also

- [VMware Product Lifecycle and EOL](../lifecycle/)
- [VMware Upgrade Readiness](../upgrade-readiness/)
- [VCF — Architecture](../../vmware-cloud-foundation/architecture/how-it-works/)
