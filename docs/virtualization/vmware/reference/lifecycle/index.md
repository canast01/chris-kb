---
tags:
  - reference
  - vmware
  - lifecycle
  - eol
  - versioning
---
# VMware Product Lifecycle and End of Life Reference

<div class="kb-summary">
Version lifecycle and End of General Support (EOGS) / End of Technical Guidance (EOTG) reference for VMware / Broadcom products. Use this page to plan upgrades, assess risk from running unsupported versions, and identify which versions receive security patches.

*Source: [Broadcom Product Lifecycle Policy](https://support.broadcom.com/lifecycle-policy) — verify dates before planning upgrades.*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
lifecycle_phase_definitions: "Lifecycle Phase Definitions" {shape: rectangle}
vsphere_esxi_vcenter: "vSphere (ESXi + vCenter)" {shape: rectangle}
vsan: "vSAN" {shape: rectangle}
nsxt_nsx: "NSX-T / NSX" {shape: rectangle}
vmware_cloud_foundation_vcf: "VMware Cloud Foundation (VCF)" {shape: rectangle}
aria_suite: "Aria Suite" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> lifecycle_phase_definitions
lifecycle_phase_definitions -> vsphere_esxi_vcenter
vsphere_esxi_vcenter -> vsan
vsan -> nsxt_nsx
nsxt_nsx -> vmware_cloud_foundation_vcf
vmware_cloud_foundation_vcf -> aria_suite
aria_suite -> validate
```

## Lifecycle Phase Definitions

| Phase | What it means |
|---|---|
| **General Support** | Full patches, security fixes, bug fixes, phone support |
| **Technical Guidance** | Security patches only; no new features; limited support |
| **End of Life (EOL)** | No patches, no support — upgrade required |

## vSphere (ESXi + vCenter)

| Version | GA Date | End of General Support | End of Technical Guidance | Notes |
|---|---|---|---|---|
| vSphere 8.0 | Oct 2022 | Oct 2027 | Oct 2029 | Current major version |
| vSphere 7.0 | Apr 2020 | Apr 2025 | Apr 2027 | In Technical Guidance phase as of Apr 2025 |
| vSphere 6.7 | Apr 2018 | Oct 2022 | Oct 2023 | **EOL** — upgrade required |
| vSphere 6.5 | Nov 2016 | Oct 2021 | Oct 2022 | **EOL** |

> **Upgrade priority:** Any environment on 6.7 or earlier is out of support and should be planned for upgrade to 8.0 immediately.

## vSAN

| Version | Lifecycle follows | Notes |
|---|---|---|
| vSAN 8.0 | vSphere 8.0 | ESA (Express Storage Architecture) introduced |
| vSAN 7.0 | vSphere 7.0 | OSA only |
| vSAN 6.7 | vSphere 6.7 | **EOL** |

## NSX-T / NSX

| Version | GA Date | End of General Support | End of Technical Guidance | Notes |
|---|---|---|---|---|
| NSX 4.x | 2022 | ~2027 (estimated) | ~2029 | Current; rebranded from NSX-T |
| NSX-T 3.2 | Jan 2022 | Jan 2025 | Jan 2027 | In Technical Guidance |
| NSX-T 3.1 | Sep 2021 | Sep 2023 | Sep 2024 | **EOL** |
| NSX-T 2.x | 2018–2020 | Various | **EOL** | |

## VMware Cloud Foundation (VCF)

| Version | GA Date | End of General Support | Notes |
|---|---|---|---|
| VCF 5.2 | 2024 | ~2027 | Current |
| VCF 5.0 | Apr 2023 | Apr 2026 | |
| VCF 4.5 | 2022 | Oct 2024 | **EOL** |
| VCF 4.4 | 2022 | May 2024 | **EOL** |

## Aria Suite

| Product | Current Version | End of General Support |
|---|---|---|
| Aria Automation | 8.16 | ~2027 |
| Aria Operations | 8.16 | ~2027 |
| Aria Operations for Logs | 8.16 | ~2027 |
| Aria Suite Lifecycle | 8.16 | ~2027 |

## vSphere Replication and SRM

| Product | Version | End of General Support |
|---|---|---|
| SRM 8.8 | 2023 | ~2026 |
| SRM 8.6 | 2022 | ~2025 |
| vSphere Replication 8.8 | 2023 | ~2026 |

## Horizon

| Version | End of General Support | Notes |
|---|---|---|
| Horizon 8 (2306+) | ~2026 | Current release train — semi-annual updates |
| Horizon 7.13 | Apr 2023 | **EOL** |

## VxRail

| Version | Notes |
|---|---|
| VxRail 8.x | Follows vSphere 8.0 lifecycle |
| VxRail 7.x | Follows vSphere 7.0 — Technical Guidance phase |

## Supported Upgrade Paths

| From | To | Supported |
|---|---|---|
| vSphere 6.7 | vSphere 8.0 | No — requires intermediate 7.0 upgrade |
| vSphere 7.0 U1+ | vSphere 8.0 | Yes |
| NSX-T 3.x | NSX 4.x | Yes — in-place upgrade supported |
| VCF 4.x | VCF 5.x | Yes — via SDDC Manager LCM |

## See also

- [VMware Interoperability Matrix](../interoperability/)
- [VMware Upgrade Readiness](../upgrade-readiness/)
- [VMware Design Standards](../../vcenter/architecture/design-standards/)
