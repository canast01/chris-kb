# Nexus Dashboard Standards


<div class="kb-summary">
Nexus Dashboard Standards reference covering Cluster Sizing Standards, Node Naming Convention, Fabric Naming Convention, Alert Policy Standards, RBAC Standards and 1 more sections.
</div>

```
┌───────────────────────────────── Nexus Dashboard — Design Standards ──────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Platform Standards              │  │             Monitoring Standards            │   │
│   │               3 physical nodes               │  │            All fabrics onboarded            │   │
│   │               SSD 500+ GB/node               │  │             MDT on all switches             │   │
│   │             Dedicated mgmt/data              │  │               ITSM integration              │   │
│   │               ND backup daily                │  │            Weekly anomaly review            │   │
│   │             RBAC: role per team              │  │             Compliance schedule             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  3 physical nodes minimum · SSD storage · dual-network (mgmt + data)                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Physical nodes = Bare-metal ND for production; 3 nodes for quorum                                    │
│  SSD 500 GB = Flash per node for streaming telemetry time-series write                                │
│  Dedicated networks = ND requires separate management and data network interfaces                     │
│  MDT on all switches = Model-Driven Telemetry enabled on all fabric switches                          │
│  ITSM integration = ServiceNow webhook configured in ND for all NDI events                            │
│  Compliance schedule = NDI running assurance checks on defined cadence                                │
│  RBAC = Role-Based Access Control; Admin/Operator/Viewer per team                                     │
│  Weekly review = Calendar event for NDI anomaly and health score review                               │
│  Backup daily = acs backup create scheduled and archived off-node                                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
