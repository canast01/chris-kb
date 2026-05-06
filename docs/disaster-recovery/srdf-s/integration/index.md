# SRDF/S Integration

SRDF/S integrates with VMware SRM via the Dell EMC Storage Replication Adapter to enable automated planned migration and disaster recovery of synchronously replicated datastores. For zero-downtime stretch cluster designs, vSphere Metro Storage Cluster (vMSC) can use SRDF/S as the underlying replication layer, with vSphere HA restarting VMs at the surviving site on storage failure. The Solutions Enabler REST API enables programmatic pair management from orchestration platforms such as Ansible or Terraform.

- **SRM + Dell SRA**: Register SRA v5.x+ on both SRM servers; configure SRDF group-to-protection-group mapping.
- **vMSC with SRDF/S**: Both sites present volumes to ESXi hosts; vSphere HA uses SRDF/S RPO=0 guarantee for zero-data-loss VM restart.
- **Aria Operations**: PowerMax management pack surfaces SRDF/S pair state, write latency impact, and link health dashboards.
- **Solutions Enabler REST API**: Authenticate via `/univmax/restapi`; use `POST /replication/symmetrix/{sid}/rdf_group/{rdfgNumber}/volume` for programmatic pair management.
