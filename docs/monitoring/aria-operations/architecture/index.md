# Aria Operations Architecture

VMware Aria Operations (formerly vROps) is built on an Analytics Cluster comprising primary and replica nodes, with an optional Data Node cluster for scale-out collection and storage. Remote Collectors are deployed at distributed sites to reduce WAN collection overhead and isolate data collection from the analytics tier. Metrics are ingested from vCenter, NSX, storage adapters, and custom endpoints via management packs. Deployment options include OVA-based on-premises clusters or the SaaS offering (Aria Operations Cloud).

| Component | Role |
|---|---|
| Primary Analytics Node | Hosts UI, analytics engine, and master services |
| Replica Analytics Node | Provides HA failover for the primary node |
| Data Nodes | Scale-out storage and indexing tier |
| Remote Collectors | Distributed collection agents, no local analytics |
| Management Packs | Adapter plugins for third-party integrations |
