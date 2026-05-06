# SRM Architecture

VMware Site Recovery Manager is a DR orchestration platform deployed as a vCenter Server plugin on both the protected site and recovery site. Key components are: SRM Server (orchestration engine), vSphere Replication appliance or array-based Storage Replication Adapters (SRAs), a Site Pair (trust relationship between two SRM instances), Protection Groups (sets of VMs or datastores), and Recovery Plans (ordered failover workflows). SRM coordinates failover of VMs across vCenter instances without requiring manual intervention at the storage or compute layer.

- **Site Pair**: Bidirectional trust between two SRM servers; requires vCenter-to-vCenter connectivity on port 443.
- **Protection Groups**: Array-based (datastore-level) or vSphere Replication-based (per-VM granularity).
- **Recovery Plans**: Ordered steps including storage presentation, VM power-on sequence, IP customisation, and custom scripts.
- **SRA**: Vendor-supplied adapter translating SRM storage commands to array-specific APIs (e.g., Dell EMC SRA for PowerMax).
