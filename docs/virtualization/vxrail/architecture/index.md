# VxRail Architecture

VxRail is a hyper-converged appliance built on Dell PowerEdge nodes running VMware vSphere and vSAN, where each node contributes compute, flash cache, and NVMe capacity storage to a unified cluster managed by VxRail Manager. Cluster topology supports 3 to 64 nodes with optional dedicated management domain nodes, and NSX-T handles software-defined networking across the fabric. VxRail Manager runs as a VM on the cluster itself and communicates with vCenter to orchestrate all lifecycle and configuration operations.

- **Cluster size:** 3–64 nodes (minimum 3 for FTT=1 vSAN policy)
- **Node roles:** All-flash, hybrid, or NVMe; optional dedicated management nodes
- **Networking:** Management, vMotion, vSAN, and VM traffic on separate VLANs
- **Storage:** vSAN distributed datastore across all participating nodes
- **Management plane:** VxRail Manager (appliance VM) + embedded vCenter or external vCenter
