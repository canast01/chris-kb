---
tags:
  - architecture
  - esxi
  - vmware
  - vsphere-8
---
# ESXi — Architecture

<div class="kb-summary">
ESXi is VMware's Type-1 hypervisor. It is deployed in standalone, standard cluster, vSAN cluster, or stretched cluster configurations depending on resilience, storage, and scale requirements.
</div>

![ESXi Cluster Deployment Models](../../../../assets/esxi-architecture-overview.svg)

| Cluster Type | Min Hosts | Storage | HA / DRS |
|---|---|---|---|
| Standalone | 1 | Local / external | No |
| Standard Cluster | 3+ | Shared SAN or NAS | Yes |
| vSAN Cluster | 3+ | Pooled from hosts (HCI) | Yes |
| Stretched Cluster | 4+ (2 per site) | vSAN stretched | Yes (site-level) |

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>VMkernel, networking, storage paths, CPU/memory scheduling, HA/DRS, and boot architecture.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>vCenter, storage, network, backup, and monitoring integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Host naming, BIOS baseline, vmkernel layout, NTP, VIB policy, and cluster sizing.</span></a>
</div>

