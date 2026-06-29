---
tags:
  - reference
  - vmware
---
# VMware Editions

<div class="kb-summary">
VMware licensing changed significantly in 2024 following the Broadcom acquisition. Perpetual
licences were discontinued and replaced with subscription-only, per-core pricing. This page
covers the current edition structure — vSphere Foundation (VVF) and VMware Cloud Foundation (VCF)
— what each includes, the add-on bundles, and key considerations when migrating from legacy licences.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

edition_comparison: "Edition Comparison" {shape: rectangle}
pricing_model: "Pricing Model" {shape: rectangle}
legacy_licence_migration: "Legacy Licence Migration" {shape: rectangle}
vcf_vs_vvf_decision_guide: "VCF vs VVF — Decision Guide" {shape: rectangle}
addon_skus: "Add-On SKUs" {shape: rectangle}
licence_consumption_and_compliance: "Licence Consumption and Compliance" {shape: rectangle}

edition_comparison -> pricing_model: uses
pricing_model -> legacy_licence_migration: uses
legacy_licence_migration -> vcf_vs_vvf_decision_guide: uses
vcf_vs_vvf_decision_guide -> addon_skus: uses
addon_skus -> licence_consumption_and_compliance: uses
```

## Edition Comparison

| Feature | vSphere Foundation (VVF) | VMware Cloud Foundation (VCF) |
|---|---|---|
| vSphere (ESXi + vCenter) | Enterprise Plus | Enterprise Plus |
| vSAN | vSAN Enterprise | vSAN Enterprise |
| NSX | — | NSX Enterprise Plus |
| SDDC Manager | — | Included |
| Tanzu (Kubernetes) | — | Included |
| Aria Operations | Essentials | Standard |
| Aria Operations for Logs | Essentials | Standard |
| Aria Automation | — | Standard |
| Pricing model | Per core, subscription | Per core, subscription |
| Minimum core pack | 16 cores per CPU | 16 cores per CPU |
| vLCM (cluster images) | Included | Included |
| Distributed Switch (vDS) | Included | Included |

### What Does "Enterprise Plus" Include?

vSphere Enterprise Plus (included in both VVF and VCF) covers:

```text
vSphere Enterprise Plus features:
  vDS (Distributed Switch) with NIOC, LACP, port mirroring
  Host Profiles
  Storage I/O Control (SIOC)
  vSphere Replication (basic)
  DRS / HA / FT / vMotion
  vLCM (Lifecycle Manager)
  vCLS (Cluster Services)
  Content Library
  VMware Tools
```

---

## Pricing Model

### Per-Core Subscription

All VMware subscriptions since 2024 are priced per physical CPU core, sold in packs.

```text
Minimum purchase: 16 cores per CPU socket
  Example: Server with 2 × 32-core CPUs = 64 physical cores
  Minimum licences = 4 × 16-core packs = 64 licensed cores

Pricing tiers (indicative — verify with Broadcom or reseller):
  VVF:  ~$50–80 per core per year (subscription)
  VCF:  ~$100–160 per core per year (subscription)
  VCF+: ~$130–200 per core per year (adds cloud services)
```

> **Note:** Broadcom pricing changes frequently and is negotiated per deal. The figures above are indicative. Always verify current pricing with a Broadcom partner or through the Broadcom portal.

### What Changed From Legacy Pricing

| Legacy model | New model |
|---|---|
| Per-VM (vSphere Essentials Kit) | No longer available |
| Per-CPU socket perpetual | Per core, subscription only |
| vSAN licensed separately | Included in VVF and VCF |
| NSX licensed separately | Included in VCF only |
| Aria products licensed separately | Included (essentials/standard tier) in VVF/VCF |

---

## Legacy Licence Migration

If migrating from perpetual licences (purchased before 2024):

```text
Legacy licence → New edition mapping:
  vSphere Enterprise Plus perpetual    → VVF (includes equivalent feature set)
  vSphere + vSAN separately            → VVF (bundles both)
  vSphere + vSAN + NSX separately      → VCF (most cost-effective if all three in use)
  vSphere Standard perpetual           → VVF (downgrade from Standard; no Standard equivalent)

Key dates:
  General Support end (Enterprise Plus):    October 2025
  Technical Guidance (limited support):     2027
```

**Important:** Organisations running perpetual licences need to migrate before General Support ends. After that date, security patches and official support are no longer provided under perpetual terms.

---

## VCF vs VVF — Decision Guide

Use VCF when:
- NSX is already in use or planned — NSX alone costs more than the VCF premium
- Running SDDC Manager (automated lifecycle management is required)
- Kubernetes/Tanzu workloads are part of the platform roadmap
- Large environments where unified upgrade orchestration justifies the cost

Use VVF when:
- No NSX requirement (IP-based networking only, or NSX deployed by another team)
- Smaller environments where SDDC Manager automation is not needed
- Budget-constrained; VVF provides the full compute and storage stack at lower cost

```text
Break-even analysis:
  If NSX is required and priced separately, VCF is typically cheaper
  than buying NSX Enterprise Plus + VVF separately.
  Ask your account team for a bundle comparison quote.
```

---

## Add-On SKUs

Products not included in VVF or VCF base editions, licensed separately:

| Product | What it provides | Typical use case |
|---|---|---|
| HCX | Hybrid cloud migration; workload mobility between sites/cloud | Migration projects; active-active stretched deployments |
| Horizon | Virtual desktop (VDI) and app publishing | End-user computing; remote workers |
| SRM + vSphere Replication | DR orchestration and VM replication | Disaster recovery with automated failover plans |
| Aria Universal | Full Aria Operations + Logs + Networks + Automation advanced | Large environments needing full observability stack |
| Advanced Security (EDR/NDR) | Carbon Black endpoint detection; NSX Intelligence | Regulated environments; threat detection |
| Tanzu Mission Control | Multi-cluster Kubernetes management (beyond built-in Tanzu) | Large Kubernetes estates; multi-cloud |

---

## Licence Consumption and Compliance

### Checking Licence Usage

```text
vCenter → Administration → Licensing → Assets
  View: licence edition applied to each host and vCenter
  Check: host count vs available capacity
  Alert: licence expiry date visible per key
```

### Common Compliance Issues

```text
1. Under-licensed cores
   — Physical hosts with more cores than licensed
   — Fix: ensure every physical core is covered; round up to 16-core packs

2. Feature use without licence
   — Using NSX DFW without VCF or NSX add-on
   — Using vDS without Enterprise Plus (now resolved in VVF/VCF)
   — Fix: run Broadcom licence audit tool or review feature usage in vCenter

3. Expired subscription
   — Subscription lapses: vCenter goes into "evaluation mode" and reverts features
   — Impact: features still work for 60 days in eval mode, then reduced functionality
   — Fix: renew before expiry; set a calendar alert at 90 days before licence expiry date
```

---

## Key Terms

| Term | Definition |
|---|---|
| VVF | VMware vSphere Foundation — the baseline subscription edition; includes vSphere Enterprise Plus, vSAN Enterprise, and Aria essentials |
| VCF | VMware Cloud Foundation — the full SDDC subscription; adds NSX Enterprise Plus, SDDC Manager, and Tanzu to the VVF stack |
| VCF+ | Cloud-connected VCF variant; adds SaaS-based management, cloud analytics, and Broadcom-hosted services |
| Per-core pricing | Licensing cost calculated per physical CPU core; sold in 16-core packs; replaces legacy per-socket perpetual model |
| Perpetual licence | Legacy one-time-purchase licence with ongoing annual support contracts; no longer sold by Broadcom for new purchases |
| General Support | The phase of VMware support providing full patches, updates, and technical assistance; ends October 2025 for legacy Enterprise Plus perpetual licences |
| SDDC Manager | VCF lifecycle orchestrator included only with VCF (not VVF); automates bringup, upgrades, and compliance |
| SRM | Site Recovery Manager — disaster recovery orchestration add-on; not included in VVF or VCF base; licensed separately |
| HCX | Hybrid Cloud Extension — live migration and network extension across sites; licensed separately; included in some VCF bundles |
| Tanzu | VMware Kubernetes platform; built-in to VCF; available as add-on for VVF environments |

---

## Related Pages

- [VMware Cloud Foundation](../../vmware-cloud-foundation/index.md) — VCF architecture, SDDC Manager, and workload domains.
- [vCenter](../../vcenter/index.md) — licensing assignment and compliance view in vCenter.
