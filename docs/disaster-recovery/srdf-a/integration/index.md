# SRDF/A Integration

SRDF/A integrates with VMware Site Recovery Manager via the Dell EMC Storage Replication Adapter (SRA), enabling automated failover orchestration of SRDF-protected datastores. Aria Operations for Storage includes a PowerMax management pack that surfaces SRDF health, lag, and cycle state metrics. RecoverPoint can co-exist on the same PowerMax array using separate device groups, provided port zoning and volume assignments do not overlap.

- **VMware SRM + Dell SRA**: Register SRA on both SRM servers; map SRDF groups to SRM protection groups.
- **Aria Operations**: PowerMax management pack provides SRDF/A lag alerts and consistency group dashboards.
- **RecoverPoint co-existence**: Segregate RecoverPoint journal volumes from SRDF device groups.
- **DataDomain/backup integration**: Target site SRDF replicas can be mounted read-only for backup offload using `symrdf -type R2` device access.
