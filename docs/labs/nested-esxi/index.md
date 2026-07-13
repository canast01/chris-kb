---
tags:
  - esxi
  - vsphere
  - compute
description: "Deploy two nested ESXi VMs and a vCenter appliance on a single physical host. This is the foundation for Labs 2, 3, and 4. Estimated time: 2–3 hours."
---
# Lab 1 — Nested ESXi Homelab

<div class="kb-summary">
Deploy two nested ESXi VMs and a vCenter appliance on a single physical host. This is the foundation for Labs 2, 3, and 4. Estimated time: 2–3 hours.
</div>

## Prerequisites

| Requirement | Minimum | Recommended |
|---|---|---|
| Physical host RAM | 32 GB | 64 GB+ |
| Physical host CPU | 8 cores, VT-x/AMD-V + EPT/RVI | 16 cores |
| Physical host storage | 500 GB HDD | 1 TB SSD |
| Physical ESXi version | 6.7 U3 | 7.0 U3+ |
| Nested ESXi ISO | 7.0 U3 | 8.0 |
| vCenter VCSA OVA | 7.0 U3 | 8.0 |
| DNS / NTP | Hosts-file DNS acceptable | Dedicated DNS server |

All files are available on [VMware Customer Connect](https://customerconnect.vmware.com/) with a free account.

## Lab topology (suggested IPs)

| VM | IP | Role |
|---|---|---|
| Physical ESXi host | 192.168.1.1 | Physical hypervisor |
| vCenter VCSA | 192.168.1.10 | vCenter Server |
| Nested ESXi-01 | 192.168.1.11 | Nested host 1 |
| Nested ESXi-02 | 192.168.1.12 | Nested host 2 |
| Gateway / DNS | 192.168.1.1 | Physical router |

## Phases

<div class="kb-grid">
<a class="kb-card" href="guide/">
<strong>Full Step-by-Step Guide</strong><br>
All five phases in one page: prepare physical host, create nested VMs, install ESXi, deploy vCSA, create cluster.
</a>
</div>

## See also

- [Lab 2 — vSAN 2-node + Witness](../vsan-2node/) — next lab building on this one
- [ESXi Cheat Sheet](../../reference/cheat-sheets/esxi/)
- [vCenter Cheat Sheet](../../reference/cheat-sheets/vcenter/)
