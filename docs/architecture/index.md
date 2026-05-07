# Architecture

<div class="kb-summary">
Architecture knowledge base landing page.
</div>

## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="disaster-recovery-design/">
  <strong>Disaster Recovery Design</strong>
  <span>RPO/RTO targets, site topology, failover patterns, and DR architecture decision frameworks.</span>
</a>

<a class="kb-card" href="high-availability/">
  <strong>High Availability</strong>
  <span>Redundancy patterns, clustering options, failover design, and availability SLA considerations.</span>
</a>

<a class="kb-card" href="network-design/">
  <strong>Network Design</strong>
  <span>Topology, segmentation, routing, and naming standards for enterprise network architecture.</span>
</a>

<a class="kb-card" href="storage-design/">
  <strong>Storage Design</strong>
  <span>Tiering strategy, protocol selection, capacity planning, and array placement principles.</span>
</a>
</div>


## Enterprise Architecture Overview

```
  ┌────────────────────────────────────────────────────────────────────────────┐
  │                        Enterprise Data Centre                              │
  │                                                                            │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐     │
  │  │   Compute Tier   │  │   Storage Tier   │  │   Network Tier       │     │
  │  │                  │  │                  │  │                      │     │
  │  │  vSphere Cluster │  │  FlashArray      │  │  Core (leaf/spine)   │     │
  │  │  ESXi hosts      │  │  PowerMax        │  │  FC fabric (SAN)     │     │
  │  │  VCF / HCI       │  │  ONTAP AFF       │  │  NSX overlay         │     │
  │  └────────┬─────────┘  └────────┬─────────┘  └──────────┬───────────┘     │
  │           │                     │                       │                 │
  │  ┌────────▼─────────────────────▼───────────────────────▼───────────┐     │
  │  │                     Management Plane                              │     │
  │  │   vCenter   Pure1   CloudIQ   Aria Operations   NSX Manager      │     │
  │  └──────────────────────────────────────────────────────────────────┘     │
  │                                                                            │
  │  ┌──────────────────────────────────────────────────────────────────┐     │
  │  │                    DR / Data Protection                           │     │
  │  │   SRDF (PowerMax)  SnapMirror (ONTAP)  ActiveCluster (FlashArray)│     │
  │  │   Veeam / NetBackup / CommVault         SRM (VMware)             │     │
  │  └──────────────────────────────────────────────────────────────────┘     │
  └────────────────────────────────────────────────────────────────────────────┘
```
