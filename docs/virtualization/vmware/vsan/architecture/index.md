---
tags:
  - architecture
  - vmware
  - vsan
  - vsphere-8
---
# vSAN — Architecture

<div class="kb-summary">
vSAN pools local NVMe and SSD disks across ESXi hosts into a shared distributed datastore. Storage policies (RAID-1/5/6, FTT) define per-VM resilience. vSAN ESA eliminates the separate cache tier on supported hardware.
</div>

![vSAN Architecture Models](../../../../assets/vsan-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Disk groups, RAID tiers, dedup/compression, vSAN ESA, and stretched cluster mechanics.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>vCenter, vSphere HA/DRS, NSX, file services, Aria Ops, and HCL compatibility.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Cluster sizing, host requirements, storage policy baseline, naming conventions, and capacity rules.</span>
</a>

<a class="kb-card" href="component-states/">
  <strong>Component States</strong>
  <span>ABSENT, DEGRADED, STALE, REBUILDING — what each state means and how to respond.</span>
</a>

<a class="kb-card" href="resync-mechanics/">
  <strong>Resync Mechanics</strong>
  <span>Why resyncs trigger, how CLOM places rebuilds, throttle settings, and the 30% headroom rule.</span>
</a>

</div>

