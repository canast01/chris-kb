# Brocade SAN

<div class="kb-summary">
Brocade SAN knowledge base articles, operational procedures, troubleshooting notes, and command references.
</div>

## SAN Fabric Topology

```
  Site A                                          Site B
  ─────────────────────────────────               ──────────────────────────────
  ┌──────────────┐   ┌──────────────┐             ┌──────────────┐   ┌──────────────┐
  │  ESXi-01     │   │  ESXi-02     │             │  ESXi-03     │   │  ESXi-04     │
  │  HBA0  HBA1  │   │  HBA0  HBA1  │             │  HBA0  HBA1  │   │  HBA0  HBA1  │
  └──┬──────┬────┘   └──┬──────┬────┘             └──┬──────┬────┘   └──┬──────┬────┘
     │      │           │      │                     │      │           │      │
  Fab-A   Fab-B       Fab-A   Fab-B               Fab-A   Fab-B       Fab-A   Fab-B
     │      │           │      │                     │      │           │      │
  ┌──▼──────▼───────────▼──┐  ┌▼────────────────────▼──────▼───────────▼──┐
  │  Brocade Director A    │  │  Brocade Director B                        │
  │  (Fabric A — primary)  │  │  (Fabric B — secondary)                    │
  └──────────┬─────────────┘  └───────────┬────────────────────────────────┘
             │  E_Port ISL (10/40 Gbps)   │  E_Port ISL
             │                            │
  ┌──────────▼─────────────┐  ┌───────────▼────────────────────────────────┐
  │  Brocade Director C    │  │  Brocade Director D                        │
  │  (Fabric A — DR site)  │  │  (Fabric B — DR site)                      │
  └──────┬─────────────────┘  └────────┬───────────────────────────────────┘
         │  FC                         │  FC
  ┌──────▼──────┐               ┌──────▼──────┐
  │ FlashArray  │               │  PowerMax   │
  │  (FA-DR-1)  │               │  (PM-DR-1)  │
  └─────────────┘               └─────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="fabric-os/">
  <strong>Fabric OS</strong>
  <span>Switch CLI, zoning, ports, ISLs, firmware, and diagnostics.</span>
</a>

<a class="kb-card" href="sannav/">
  <strong>SANnav</strong>
  <span>Fabric management, alerts, inventory, monitoring, and reporting.</span>
</a>

</div>
