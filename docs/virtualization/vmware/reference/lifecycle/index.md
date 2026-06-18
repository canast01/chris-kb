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

```text
┌───────────────────────── VMware Product Lifecycle — EOGS and EOTG Reference ──────────────────────────┐
│                                                                                                       │
│  EOGS = no new patches; EOTG = no technical guidance; use Broadcom lifecycle                          │
│  policy page to plan upgrades and assess risk of running unsupported versions.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Support Phases                │  │                Risk by Phase                │   │
│   │          GA: full support + patches          │  │          GA: all patches + guidance         │   │
│   │        EOGS: no new security patches         │  │          EOGS: unpatched CVEs risk          │   │
│   │         EOTG: no technical guidance          │  │          EOTG: no support available         │   │
│   │          EOL: product discontinued           │  │             EOL: plan migration             │   │
│   │        Extended support: paid option         │  │          Extended: CVE patches only         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Run unsupported version = accept CVE risk; regulatory compliance may prohibit.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Key Product Lifecycles            │  │               Upgrade Planning              │   │
│   │           vSphere 7: EOGS Oct 2025           │  │         Verify: support.broadcom.com        │   │
│   │          vSphere 8: GA 2022, active          │  │            Lead time: 6-12 months           │   │
│   │           NSX-T 3.x: EOGS Oct 2025           │  │          Test: staging before prod          │   │
│   │           NSX 4.x: active support            │  │           Change freeze: avoid Q4           │   │
│   │           VCF 5.x: active support            │  │        Rollback plan: snapshot first        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Hardware lifecycle runs parallel — server EoL affects OS/hypervisor support;                         │
│  plan hardware refresh alongside software upgrade to avoid stranded costs.                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  EOGS          = End of General Support; last day new patches released                                │
│  EOTG          = End of Technical Guidance; no more support responses                                 │
│  EOL           = End of Life; product discontinued; migrate off                                       │
│  GA            = General Availability; release date of version                                        │
│  CVE           = Common Vulnerabilities and Exposures; tracked by NVD                                 │
│  Extended support= paid programme; CVE patches only; higher cost                                      │
│  Lifecycle page = support.broadcom.com/lifecycle-policy; authoritative                                │
│  Version N-2   = two major versions behind current; approaching EOGS                                  │
│  Security patch = CVE fix; critical patches issued after EOGS is rare                                 │
│  Upgrade window= planned maintenance; verify compat matrix first                                      │
│  Staging test  = validate upgrade path in non-production first                                        │
│  Change freeze = period where no upgrades allowed; typically Q4 retail                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
