# Nutanix — Architecture

<div class="kb-summary">
AOS distributed architecture, AHV hypervisor, Prism management plane, and cluster design standards. Foundation for understanding how Nutanix HCI works and how to design clusters for production workloads.

*Applies to: AOS 6.x · AHV*
</div>

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                       NUTANIX CLUSTER ARCHITECTURE                                                    │
│                                                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                                        │
│  │   NODE 1        │  │   NODE 2        │  │   NODE N        │                                        │
│  │                 │  │                 │  │                 │                                        │
│  │  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │                                        │
│  │  │  AHV Host │  │  │  │  AHV Host │  │  │  │  AHV Host │  │                                        │
│  │  │  (KVM)    │  │  │  │  (KVM)    │  │  │  │  (KVM)    │  │                                        │
│  │  │  VMs  VM  │  │  │  │  VMs  VM  │  │  │  │  VMs  VM  │  │                                        │
│  │  └─────┬─────┘  │  │  └─────┬─────┘  │  │  └─────┬─────┘  │                                        │
│  │        │        │  │        │        │  │        │        │                                        │
│  │  ┌─────▼─────┐  │  │  ┌─────▼─────┐  │  │  ┌─────▼─────┐  │                                        │
│  │  │    CVM    │  │  │  │    CVM    │  │  │  │    CVM    │  │                                        │
│  │  │ Stargate  │◄─┼──┼─►│ Stargate  │◄─┼──┼─►│ Stargate  │  │                                        │
│  │  │ Cassandra │  │  │  │ Cassandra │  │  │  │ Cassandra │  │                                        │
│  │  │ Curator   │  │  │  │ Curator   │  │  │  │ Curator   │  │                                        │
│  │  │ Zeus      │  │  │  │ Zeus      │  │  │  │ Zeus      │  │                                        │
│  │  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │                                        │
│  │                 │  │                 │  │                 │                                        │
│  │  SSD ████ HDD   │  │  SSD ████ HDD   │  │  SSD ████ HDD   │                                        │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                                        │
│             │                  │                    │                                                 │
│             └──────────────────┴────────────────────┘                                                 │
│                         10GbE / 25GbE Fabric                                                          │
│                                                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐                                      │
│  │  PRISM ELEMENT (per cluster)   PRISM CENTRAL (multi-cluster)│                                      │
│  │  Cluster VIP: 9440             PC VIP: 9440/9443            │                                      │
│  └─────────────────────────────────────────────────────────────┘                                      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="how-it-works/">
    <strong>How It Works</strong>
    <span>AOS data path, CVM role, Stargate I/O, replication factor, and storage tiers. Start here.</span>
  </a>
  <a class="kb-card" href="design-standards/">
    <strong>Design Standards</strong>
    <span>Node selection, cluster sizing, RF2 vs RF3, container design, network layout, and block awareness.</span>
  </a>
  <a class="kb-card" href="integrations/">
    <strong>Integrations</strong>
    <span>Prism Central registration, AD/LDAP, Veeam, HYCU, Zerto, Prometheus, Nutanix Files, and Calm.</span>
  </a>
</div>
