---
tags:
  - vcf
  - vsphere
  - vsan
  - nsx
---
# Lab 4 — VCF on Nested ESXi

<div class="kb-summary">
Deploy a VMware Cloud Foundation management domain using Cloud Builder on nested ESXi. The most resource-intensive lab — requires 256 GB+ RAM on the physical host. Estimated time: 4–6 hours.
</div>

## Prerequisites

| Requirement | Minimum | Notes |
|---|---|---|
| Physical host RAM | 256 GB | NSX Manager cluster alone needs 3 × 24 GB = 72 GB |
| Physical host vCPU | 32 cores | Nested ESXi + control plane VMs are CPU-heavy |
| Physical host storage | 2 TB SSD | vSAN across 4 nested nodes; SSD strongly recommended |
| Nested ESXi count | 4 nodes | VCF management domain requires 4 ESXi hosts minimum |
| Nested ESXi version | 7.0 U3 (VCF 4.x) or 8.0 (VCF 5.x) | Must exactly match the VCF BOM |
| Cloud Builder OVA | Download from VMware Customer Connect | Version must match target VCF release |
| VCF configuration workbook | Excel file (.xlsx) from VMware | Provides network topology, IP, and naming scheme |
| DNS | Full forward + reverse DNS required | Cloud Builder validation fails without it |
| NTP | All hosts must use the same NTP source | Certificate errors if clocks drift |
| License keys | vSphere, vSAN, NSX-T, VCF | 60-day eval keys available on Customer Connect |

## VCF network requirements (5 port groups on physical host)

| Network | VLAN | Purpose |
|---|---|---|
| Management | Any (e.g., VLAN 10) | ESXi management vmk0, vCenter, NSX Manager, SDDC Manager |
| vMotion | Any (e.g., VLAN 11) | Live VM migration between nested hosts |
| vSAN | Any (e.g., VLAN 12) | vSAN storage traffic between nested hosts |
| Host TEP | Any (e.g., VLAN 13) | NSX Geneve tunnel endpoints on ESXi hosts |
| Edge TEP | Any (e.g., VLAN 14) | NSX Geneve tunnel endpoints on Edge VMs |

For a simplified nested lab, all VLANs can map to the **same physical portgroup** (no physical VLAN tagging required) as long as the portgroup has Promiscuous Mode + Forged Transmits enabled.

## Phases

<div class="kb-grid">
<a class="kb-card" href="guide/">
<strong>Full Step-by-Step Guide</strong><br>
Prepare networking, fill in the VCF workbook, deploy Cloud Builder, run validation, deploy the management domain.
</a>
</div>

## See also

- [Lab 1 — Nested ESXi Homelab](../nested-esxi/) — understand the nested ESXi foundation
- [Lab 2 — vSAN 2-node](../vsan-2node/) — understand vSAN before running VCF
- [Lab 3 — NSX-T nested](../nsx-nested/) — understand NSX before running VCF
- [VCF Architecture](../../virtualization/vmware/vmware-cloud-foundation/architecture/)
- [NSX Topology Decision Tree](../../reference/decision-trees/nsx-topology/)
