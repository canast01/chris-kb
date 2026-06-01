# Architecture

<div class="kb-summary">
Enterprise infrastructure architecture design guides covering high availability patterns, storage tiering, network topology, and disaster recovery design principles.
</div>

```
┌────────────────── Architecture — HA Design, Storage, Networking & Disaster Recovery ──────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Architecture design guides for enterprise infrastructure: HA, storage, network, DR      │   │
│   │    Design principles: eliminate single points of failure; automate failover; test recovery    │   │
│   │     All designs must state: RPO/RTO targets, failure domain boundaries, and recovery path     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Compute & HA        │  │      Storage & Network      │  │        DR & Recovery        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      N+1 host capacity      │  │       Storage tiering       │  │      RPO / RTO targets      │   │
│   │       DRS + vSphere HA      │  │       Redundant paths       │  │      Active-passive DR      │   │
│   │     Failure domain plan     │  │       L3 segmentation       │  │      Replication design     │   │
│   │     Anti-affinity rules     │  │     Spine-leaf topology     │  │       Failover runbook      │   │
│   │        Resource pools       │  │      BGP peering design     │  │       Recovery testing      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    N+1          = One more host than minimum required; one failure without service impact             │
│    Failure domain= Boundary within which a single failure has impact; AZ / rack / PDU                 │
│    Anti-affinity = Rule keeping workloads on different hosts for HA; opposite of affinity             │
│    Spine-leaf   = Data centre switching topology; spine = core, leaf = ToR; no STP needed             │
│    Active-passive= Primary handles all traffic; standby takes over on failure (vs active-active)      │
│    RPO/RTO      = Recovery Point/Time Objectives; quantify acceptable data loss and downtime          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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


