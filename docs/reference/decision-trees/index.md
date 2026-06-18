---
tags:
  - vsphere
  - architecture
  - operations
---
# Decision Trees

<div class="kb-summary">
Flowcharts for common VMware infrastructure design decisions — storage policy, NSX topology, DR tool selection, and Aria product selection.
</div>

```text
┌─────────────────────────────────────── Decision Trees ────────────────────────────────────────────────┐
│  Interactive flowcharts for design and tool selection decisions                                       │
│  vSAN Policy · NSX Topology · DR Tool · Aria Product Selection                                        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
<a class="kb-card" href="vsan-policy/">
<strong>vSAN Storage Policy</strong><br>
Choose FTT level, RAID type, encryption, and dedup/compression based on cluster size and requirements.
</a>
<a class="kb-card" href="nsx-topology/">
<strong>NSX Topology</strong><br>
Select overlay vs VLAN, T0/T1 placement, Edge sizing, HA model, and north-south routing type.
</a>
<a class="kb-card" href="dr-tool/">
<strong>DR Tool Selection</strong><br>
SRM vs vSphere Replication vs backup-based DR — choose based on RPO, RTO, and licensing.
</a>
<a class="kb-card" href="aria-selection/">
<strong>Aria Product Selection</strong><br>
Which Aria product fits your need — monitoring, logging, automation, network visibility, or lifecycle.
</a>
</div>
