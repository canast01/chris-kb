---
tags:
  - reference
  - vmware
  - interoperability
  - compatibility
description: "Interoperability reference for VMware product combinations. Use this page before planning upgrades or deploying new products to confirm component..."
---
# VMware Interoperability and Compatibility Matrix

<div class="kb-summary">
Interoperability reference for VMware product combinations. Use this page before planning upgrades or deploying new products to confirm component compatibility. The authoritative source is the [VMware Product Interoperability Matrix](https://interopmatrix.vmware.com/) — always verify before purchasing or deploying.

*Applies to: vSphere 7.x / 8.x, NSX 4.x, VCF 5.x, Aria Suite 8.x*
</div>

```d2
direction: down

vsphere_80_component_compatibility: "vSphere 8.0 — Component Compatibility" {shape: rectangle}
vsphere_70_component_compatibility: "vSphere 7.0 — Component Compatibility" {shape: rectangle}
vcf_5x_bom_bill_of_materials: "VCF 5.x BOM (Bill of Materials)" {shape: rectangle}
nsx_interoperability: "NSX Interoperability" {shape: rectangle}
hardware_compatibility_hcl: "Hardware Compatibility (HCL)" {shape: rectangle}
key_interoperability_rules: "Key Interoperability Rules" {shape: rectangle}

vsphere_80_component_compatibility -> vsphere_70_component_compatibility: uses
vsphere_70_component_compatibility -> vcf_5x_bom_bill_of_materials: uses
vcf_5x_bom_bill_of_materials -> nsx_interoperability: uses
nsx_interoperability -> hardware_compatibility_hcl: uses
hardware_compatibility_hcl -> key_interoperability_rules: uses
```

## Before you begin

- **Always verify on the official tool:** [interopmatrix.vmware.com](https://interopmatrix.vmware.com/) — the matrix below is a reference snapshot and may not reflect latest patches.
- When upgrading one component, check all dependent products in the matrix before proceeding.
- VCF bundles validated component versions — use VCF BOM for VCF deployments rather than mixing versions independently.

## Component Compatibility by Version

=== "vSphere 8.0"

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

=== "vSphere 7.0"

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
- [VCF — Architecture](../../products/vmware-cloud-foundation/architecture/how-it-works/)
