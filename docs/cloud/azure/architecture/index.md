# Azure Architecture

Azure account structure is organised through Management Groups at the root, which contain Subscriptions (one per environment: dev, staging, production, shared-services), with Resource Groups providing logical boundaries for related workloads within each subscription. Core services include Virtual Machines and AKS for compute, Azure SQL and Cosmos DB for data, Azure Blob Storage for object storage, Entra ID for identity, and Virtual Networks for private connectivity. High availability is achieved using Availability Zones within a region, while disaster recovery leverages Azure region pairs with geo-redundant storage and Azure Site Recovery for VM replication.

- **Management Groups**: root → platform → workloads → per-environment subscriptions
- **Subscriptions**: dev, staging, prod, shared-services, identity, connectivity (hub-and-spoke via Azure Virtual WAN or hub VNet)
- **Resource Groups**: one per workload tier; locked in production to prevent accidental deletion
- **HA pattern**: Availability Zones for VMs, AKS, and Azure SQL; zone-redundant storage (ZRS)
- **DR pattern**: Region pairs (e.g., West Europe / North Europe); Azure Site Recovery for VM failover; geo-redundant storage for blob data
