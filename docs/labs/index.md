---
tags:
  - vsphere
  - vsan
  - nsx
  - vcf
description: "Hands-on walkthroughs for building a VMware nested homelab from bare metal through vSAN, NSX-T, and VCF. Each lab builds on the previous one — start with..."
---
# Lab Guides

<div class="kb-summary">
Hands-on walkthroughs for building a VMware nested homelab from bare metal through vSAN, NSX-T, and VCF. Each lab builds on the previous one — start with Lab 1 if you are new to nested virtualisation.
</div>

<div class="kb-grid">
<a class="kb-card" href="nested-esxi/">
<strong>Lab 1 — Nested ESXi Homelab</strong><br>
Physical host → 2 nested ESXi VMs → vCenter. Foundation for all other labs. Requires 32 GB RAM.
</a>
<a class="kb-card" href="vsan-2node/">
<strong>Lab 2 — vSAN 2-node + Witness</strong><br>
Adds vSAN shared storage to Lab 1. Builds a 2-node cluster with a witness VM. Requires Lab 1.
</a>
<a class="kb-card" href="nsx-nested/">
<strong>Lab 3 — NSX-T in Nested ESXi</strong><br>
Deploys NSX Manager, prepares transport nodes, creates segments and basic DFW rules. Requires Lab 1.
</a>
<a class="kb-card" href="vcf-nested/">
<strong>Lab 4 — VCF on Nested ESXi</strong><br>
Full VCF management domain using Cloud Builder. Requires 256 GB+ RAM. Most demanding lab.
</a>
</div>

## Hardware sizing summary

| Lab | Min RAM | Min vCPU | Min Storage | Builds on |
|---|---|---|---|---|
| Lab 1: Nested ESXi | 32 GB | 8 cores | 500 GB | — |
| Lab 2: vSAN 2-node | 48 GB | 8 cores | 700 GB | Lab 1 |
| Lab 3: NSX-T nested | 64 GB | 12 cores | 500 GB | Lab 1 |
| Lab 4: VCF nested | 256 GB | 32 cores | 2 TB SSD | Lab 1 |

## Common requirements for all labs

- Physical ESXi host running **6.7 U3** or later (7.0+ recommended)
- Physical host must support nested virtualisation: **Intel VT-x / AMD-V + EPT / RVI**
- Parent port group (vSwitch/vDS) for nested VMs must have **Promiscuous Mode**, **Forged Transmits**, and **MAC address changes** all set to **Accept**
- DNS: at minimum, add `/etc/hosts` entries on vCenter and nested hosts. Full forward + reverse DNS is required for VCF (Lab 4)
- NTP: all hosts must point to the same NTP source. VCF deployment fails with clock drift
