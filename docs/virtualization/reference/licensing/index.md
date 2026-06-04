# VMware / Broadcom Licensing Reference

Quick reference for determining which licence tier is required to enable a specific capability. Use this page to answer "do I need to buy more licences to enable X?" before raising a change or procurement request.

---

## Overview — Post-Broadcom Licensing Model

As of 2024, Broadcom restructured VMware's entire licensing portfolio. The key changes:

- **Perpetual licences ended.** All new purchases are subscription-based (annual or multi-year terms).
- **Two primary bundles** replace the old à-la-carte SKU list: **VMware Cloud Foundation (VCF)** and **vSphere Foundation (VVF)**.
- **Standalone products** still exist but are positioned as add-ons or for customers with narrow requirements.
- **Per-core pricing** replaces per-CPU pricing across most products — host core count now directly drives licence cost.
- Existing perpetual licences remain valid under active support contracts but cannot be renewed; customers must migrate to subscription on renewal.
- **Product names changed.** vRealize Operations → Aria Operations; vRealize Automation → Aria Automation; vRealize Log Insight → Aria Operations for Logs; NSX-T → NSX.

**Pricing model summary:**

| Metric | Old model (pre-2024) | New model (post-2024) |
|---|---|---|
| Licence type | Perpetual + annual support (SnS) | Subscription (annual or multi-year) |
| Pricing unit | Per CPU socket | Per core |
| Bundle structure | À-la-carte SKUs | VCF / VVF bundles |
| Minimum commitment | Single product | Full bundle (for bundle pricing) |
| Renewal path | Renew SnS annually | Renew subscription annually |

Broadcom's intent is to push customers toward VCF (the full-stack bundle) as the preferred deployment model. Standalone SKUs remain available but are priced to make bundles attractive for environments using more than one VMware product.

---

## VMware Cloud Foundation (VCF)

VCF is the full-stack Software-Defined Data Centre (SDDC) bundle. It is the highest-tier offering and Broadcom's strategic focus.

**What is included:**

| Component | Detail |
|---|---|
| vSphere (ESXi + vCenter) | Full Enterprise Plus feature set |
| vSAN | Enterprise tier; all features unlocked |
| NSX | Data Centre Enterprise Plus |
| SDDC Manager | Lifecycle management for the full SDDC stack |
| Aria Suite | Operations, Automation, Log Insight, Network Insight |

**Deployment model:**

- Managed through SDDC Manager, which handles bring-up, domain creation, and lifecycle (patching, upgrades).
- Workload domains separate management and compute workloads.
- VI Workload Domains and VCF on VxRail are the two primary deployment variants.

**Who it is for:**

- Customers running an integrated VMware stack at scale who need NSX, vSAN, and Aria together.
- Environments where SDDC Manager lifecycle automation reduces operational overhead.
- Customers who previously held Enterprise Plus + vSAN Ent + NSX DC individually — VCF may be cost-neutral or cheaper at scale.

**Key point:** Once on VCF, NSX and vSAN are included at their highest tiers. No separate licence is required for either. Aria Suite components are also included — no additional Aria Operations or Aria Automation licence purchase needed.

---

## vSphere Foundation (VVF)

VVF is the mid-tier bundle, providing compute and basic networking without the full VCF commitment.

**What is included:**

| Component | Detail |
|---|---|
| vSphere (ESXi + vCenter) | Enterprise Plus feature set |
| vSAN | Standard tier (basic features; see vSAN table below) |
| Tanzu | Basic Kubernetes integration |

**What is NOT included:**

| Component | Status |
|---|---|
| NSX | Not included — must be purchased separately |
| Full Aria Suite | Limited subset only; Aria Operations for Networks not included |
| SDDC Manager | Not included — lifecycle managed manually or via vLCM |
| Advanced vSAN features | Stretched cluster, dedup/compression, encryption require Enterprise tier |

**Who it is for:**

- Customers who want vSphere with basic HCI (vSAN) but are not ready for VCF.
- Environments that do not require NSX overlay networking.
- Smaller deployments where SDDC Manager overhead is not justified.

---

## Standalone / Add-on Licences

Products available for purchase individually, outside of VCF or VVF bundles.

| Product | Available standalone? | Pricing unit | Notes |
|---|---|---|---|
| vSphere Standard | Yes | Per core | ESXi + vCenter; no VDS, no NIOC |
| vSphere Enterprise Plus | Yes | Per core | Full VDS, NIOC, host profiles, Auto Deploy |
| vSAN | Yes | Per core | Requires vSphere; Standard or Enterprise tier |
| NSX | Yes | Per core | Data Centre Standard / Professional / Advanced / Enterprise Plus tiers |
| Aria Operations | Yes | Per OSI or per core | Formerly vRealize Operations |
| Aria Automation | Yes | Per OSI | Formerly vRealize Automation |
| Site Recovery Manager (SRM) | Yes | Per protected VM | Orchestrated DR failover and failback |
| vSphere Replication | Included | — | Bundled with all vSphere editions; no separate licence required |
| HCX | Yes | Per core or subscription | Used for live and cold VM migration between sites or to cloud |

---

## vSphere Feature — Licence Tier Requirements

Determines whether a vSphere feature is accessible at a given licence tier.

| Feature | Standard | Enterprise Plus | VVF | VCF |
|---|---|---|---|---|
| vSphere HA | ✓ | ✓ | ✓ | ✓ |
| vSphere DRS | ✓ | ✓ | ✓ | ✓ |
| vSphere Fault Tolerance | ✓ | ✓ | ✓ | ✓ |
| vSphere Lifecycle Manager (vLCM) | ✓ | ✓ | ✓ | ✓ |
| Encrypted vMotion | ✓ | ✓ | ✓ | ✓ |
| VM Encryption | ✓ | ✓ | ✓ | ✓ |
| vSphere Distributed Switch (VDS) | ✗ | ✓ | ✓ | ✓ |
| Network I/O Control (NIOC) | ✗ | ✓ | ✓ | ✓ |
| Host Profiles | ✗ | ✓ | ✓ | ✓ |
| Auto Deploy | ✗ | ✓ | ✓ | ✓ |
| vSphere with Tanzu (Kubernetes) | ✗ | ✗ | ✓ (basic) | ✓ |

**Notes:**

- Standard edition cannot use VDS — all port groups remain on vSS (vSphere Standard Switch). This means no NIOC, no LACP, and no per-port policies.
- Host Profiles and Auto Deploy both require Enterprise Plus or higher; both depend on VDS being available.
- Tanzu requires a Supervisor cluster, which in turn requires VDS and specific NSX or vSphere networking configuration depending on the deployment type.

---

## NSX Feature — Licence Tier Requirements

NSX Data Centre is available in four tiers. Features accumulate upward — each tier includes everything below it.

| Feature | Standard | Professional | Advanced | Enterprise Plus |
|---|---|---|---|---|
| Logical Switching and Routing | ✓ | ✓ | ✓ | ✓ |
| Distributed Firewall (DFW) | ✓ | ✓ | ✓ | ✓ |
| NAT, DHCP, DNS | ✓ | ✓ | ✓ | ✓ |
| Gateway Firewall | ✓ | ✓ | ✓ | ✓ |
| Load Balancing (basic) | ✗ | ✓ | ✓ | ✓ |
| VPN (L2 and L3) | ✗ | ✓ | ✓ | ✓ |
| Federation (multi-site NSX Manager) | ✗ | ✗ | ✓ | ✓ |
| Advanced Threat Prevention (IDS/IPS) | ✗ | ✗ | ✗ | ✓ |
| NSX Intelligence (traffic analysis) | ✗ | ✗ | ✗ | ✓ |
| Network Detection and Response (NDR) | ✗ | ✗ | ✗ | ✓ |

**Notes:**

- NSX is licenced per core across all hosts where NSX preparation (n-VDS or VDS with NSX) is applied.
- Federation requires Advanced or higher — if you are running multiple NSX Managers across sites and want unified policy, Standard and Professional are insufficient.
- IDS/IPS (Advanced Threat Prevention) requires Enterprise Plus. If security posture requires east-west threat detection, plan for the top tier from the outset.
- VCF includes NSX Data Centre Enterprise Plus — all features in the table are available under VCF with no additional licence.

---

## vSAN Feature — Licence Tier Requirements

vSAN features are split between Standard and Enterprise tiers. All-flash and hybrid configurations are supported at both tiers.

| Feature | vSAN Standard | vSAN Enterprise | Notes |
|---|---|---|---|
| All-Flash / HCI (OSA) | ✓ | ✓ | Original Storage Architecture |
| Hybrid (HDD + SSD cache) | ✓ | ✓ | |
| Storage Policy-Based Management (SPBM) | ✓ | ✓ | |
| vSAN Health Service | ✓ | ✓ | |
| Stretched Cluster | ✗ | ✓ | Requires witness appliance and low-latency inter-site link |
| Deduplication and Compression | ✗ | ✓ | All-flash only; significant capacity savings in dense environments |
| Encryption at Rest | ✗ | ✓ | Requires KMS integration |
| iSCSI Target Service | ✗ | ✓ | Expose vSAN datastore to non-vSphere workloads |
| File Services (vSAN File Share) | ✗ | ✓ | SMB/NFS file shares backed by vSAN |
| HCI Mesh (remote vSAN datastore) | ✗ | ✓ | Mount a remote cluster's vSAN datastore |
| vSAN ESA (Express Storage Architecture) | ✗ | ✓ | vSAN 8+; requires all-NVMe host configuration |

**Notes:**

- VVF includes vSAN Standard tier. Stretched cluster, encryption, dedup/compression, and ESA require upgrading to Enterprise tier or moving to VCF.
- VCF includes vSAN Enterprise — all features are available.
- vSAN ESA is an architectural change from OSA; hosts must meet all-NVMe requirements and the cluster must be built from scratch (no in-place upgrade from OSA to ESA).
- Encryption at Rest requires an external Key Management Server (KMS) integrated with vCenter. The licence unlocks the feature; the KMS infrastructure is a separate dependency.

---

## Bundle Comparison — Side by Side

High-level comparison of the four main licence tiers. Use this to quickly determine which tier meets a given environment's requirements.

| Capability | vSphere Standard | vSphere Ent+ | VVF | VCF |
|---|---|---|---|---|
| ESXi + vCenter | ✓ | ✓ | ✓ | ✓ |
| HA, DRS, FT | ✓ | ✓ | ✓ | ✓ |
| VM Encryption | ✓ | ✓ | ✓ | ✓ |
| vSphere Replication | ✓ | ✓ | ✓ | ✓ |
| vSphere Lifecycle Manager | ✓ | ✓ | ✓ | ✓ |
| VDS (Distributed Switch) | ✗ | ✓ | ✓ | ✓ |
| NIOC | ✗ | ✓ | ✓ | ✓ |
| Host Profiles | ✗ | ✓ | ✓ | ✓ |
| Auto Deploy | ✗ | ✓ | ✓ | ✓ |
| vSAN (any tier) | ✗ (add-on) | ✗ (add-on) | ✓ Standard | ✓ Enterprise |
| NSX | ✗ (add-on) | ✗ (add-on) | ✗ (add-on) | ✓ Ent+ |
| Tanzu / Kubernetes | ✗ | ✗ | ✓ (basic) | ✓ |
| Aria Suite (full) | ✗ | ✗ | ✗ (limited) | ✓ |
| SDDC Manager | ✗ | ✗ | ✗ | ✓ |
| Lifecycle automation | Manual / vLCM | Manual / vLCM | Manual / vLCM | SDDC Manager |

**Reading the table:**

- "Add-on" means the feature is not included in the base bundle but can be purchased separately.
- "Limited" means a restricted subset of the full product is available; check with Broadcom for the exact Aria Operations scope in VVF.
- VCF is the only tier where NSX and full Aria Suite are included without separate purchase.
- vSphere Standard is rarely the right choice for production environments — VDS is absent, which blocks NIOC, LACP, and host profiles.

---

## Common Licensing Scenarios — Quick Lookup

Use this table to map a common capability question directly to the minimum licence required.

| Question / Capability Needed | Minimum Licence Required |
|---|---|
| I need HA and DRS — what licence? | vSphere Standard (both included) |
| I want to use LACP on my virtual switch | vSphere Enterprise Plus (requires VDS) |
| I need to assign different port group policies per VM | vSphere Enterprise Plus (requires VDS) |
| I want to use Host Profiles to standardise host config | vSphere Enterprise Plus |
| I want to PXE-boot ESXi hosts via Auto Deploy | vSphere Enterprise Plus |
| I want vSAN on my cluster | vSAN Standard add-on (or VVF/VCF) |
| I want vSAN deduplication and compression | vSAN Enterprise add-on (or VCF) |
| I want vSAN stretched cluster across two sites | vSAN Enterprise add-on (or VCF) |
| I want to encrypt VM storage at rest | vSAN Enterprise + KMS (or VCF) |
| I need east-west micro-segmentation (DFW) | NSX Standard (DFW included in base tier) |
| I need a software load balancer in NSX | NSX Professional or higher |
| I need IPSec / L2VPN between sites via NSX | NSX Professional or higher |
| I need NSX Federation across multiple sites | NSX Advanced or higher |
| I need IDS/IPS for east-west traffic | NSX Enterprise Plus (or VCF) |
| I want to orchestrate DR failover | SRM (per protected VM) |
| I want to replicate VMs without SRM | vSphere Replication (free, included) |
| I want to run Kubernetes workloads on vSphere | VVF (basic Tanzu) or VCF |
| I need Aria Operations for monitoring | Aria Operations standalone or VCF |
| I need Aria Automation for self-service catalogue | Aria Automation standalone or VCF |
| I want everything with a single contract | VCF |

---

## Licence Assignment — Step by Step

How to apply a licence key to vSphere hosts and solutions in vCenter.

**Assign a key to vCenter Server:**

1. Log in to vCenter as an account with Administrator role.
2. Go to **Administration → Licences → Licences**.
3. Click **Add** (the `+` icon) and paste the licence key.
4. Click **Next**, review product and quantity, then **Finish**.
5. Go to the **Assets** tab → select **vCenter Server instances**.
6. Select the vCenter instance → click **Assign Licence** → choose the new key.

**Assign a key to ESXi hosts:**

1. From the **Assets** tab, select **Hosts**.
2. Select one or more hosts (hold Ctrl/Shift for multiple).
3. Click **Assign Licence** → choose the applicable key.
4. Confirm the key edition matches the features required on those hosts.

**Assign a key to a vSAN cluster:**

1. From the **Assets** tab, select **vSAN clusters**.
2. Select the cluster → **Assign Licence** → choose the vSAN key.
3. The vSAN licence is applied at cluster level, not per-host — one key covers all hosts in that cluster.

**Assign a key to NSX Manager:**

1. Log in to NSX Manager UI.
2. Go to **System → Licences**.
3. Click **Add Licence** → paste the key → **Add**.
4. NSX applies the licence globally to the NSX Manager instance.

**Verify licence compliance:**

- Hosts tab shows **Licence Edition**, **Licence Expiry**, and a **Compliant** flag.
- Red icons indicate unlicensed or expired assets — resolve before the 60-day grace period ends.
- Export the asset list via **Export** (CSV) for audit or procurement records.

---

## Key Licensing Gotchas

- **vSphere Replication is always free** — it is bundled with every vSphere edition. There is no separate purchase required to use vSphere Replication for basic VM replication.
- **SRM is licenced per protected VM** — costs scale linearly with the number of VMs in a protection group. Factor this in before expanding DR scope.
- **NSX per-core pricing compounds quickly** — a 10-host cluster with 32 cores per host is 320 licensed cores. Larger environments should model total cost before committing to NSX standalone versus VCF.
- **VDS requires Enterprise Plus or higher** — Standard Switch (vSS) does not support NIOC, LACP, or per-port traffic shaping. If you need any of these, Standard edition is a blocker regardless of other considerations.
- **VCF may be cheaper than standalone at scale** — if your environment already needs vSphere Enterprise Plus + vSAN Enterprise + NSX Advanced or higher, VCF's per-core price can undercut the combined standalone cost. Model both options before procurement.
- **Perpetual licences cannot be renewed** — existing perpetual customers can continue running on existing keys under active support, but on expiry they must move to subscription. There is no path to renew perpetual.
- **Downgrading bundles removes features immediately** — if a cluster running VCF or VVF is downgraded to Standard at licence renewal, features like VDS, host profiles, and vSAN Enterprise capabilities become unavailable and VMs using those policies will be affected.
- **Grace period on licence expiry is 60 days** — after expiry, vCenter enters evaluation mode and some management features are restricted, but running VMs are not affected. Address licence gaps before the grace period ends.

---

## Useful References

- **VMware Product Interoperability Matrix** — search "VMware Product Interoperability Matrix" on the Broadcom support portal to validate version combinations between vCenter, ESXi, vSAN, NSX, and SRM.
- **Broadcom Licence Portal** — [support.broadcom.com](https://support.broadcom.com) — where subscription licences are assigned, downloaded, and managed. Requires a Broadcom Support account linked to your organisation's entitlement.
- **Broadcom Product Portfolio** — the complete list of post-acquisition product names, SKUs, and bundle contents is published at the Broadcom support portal under VMware Cloud Foundation portfolio.
- **Licence assignment in vCenter** — vCenter → Administration → Licences → Licences tab → Add → assign to assets.
- **Check current licence usage** — vCenter → Administration → Licences → Assets tab — shows each host, cluster, and solution with the currently assigned licence key and edition.
- **View licence expiry** — vCenter → Administration → Licences → Licences tab → select a key → expiration date shown in the detail panel.
- **NSX licence check** — NSX Manager UI → System → Licences — shows the active licence tier and features enabled.
- **vSAN licence check** — vCenter → cluster → Configure → vSAN → Licence — shows current vSAN licence tier applied to the cluster.
- **SRM licence check** — SRM UI → Summary — shows protected VM count against the licence limit.
