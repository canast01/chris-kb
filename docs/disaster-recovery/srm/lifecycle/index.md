# SRM Lifecycle

SRM version must be aligned with the deployed vCenter version; Broadcom publishes a compatibility matrix that must be checked before any upgrade. vSphere Replication version must also match within the supported range for the SRM release in use. SRM licenses are per-VM and must be inventoried against the protected VM count; growth planning should trigger license reviews at 80% utilisation.

- **Upgrade sequence**: Upgrade vCenter → upgrade SRM Server → upgrade vSphere Replication appliance → update SRA plugins.
- **Compatibility matrix**: Check VMware Product Interoperability Matrix at interopmatrix.vmware.com before any upgrade.
- **License model**: Per protected VM; perpetual with SnS or subscription via Broadcom Advantage portal.
- **EOL tracking**: SRM 8.x aligned to vSphere 8 lifecycle; track EOS dates in CMDB.
- **Migration — array to vSphere Replication**: Remove array-based protection group → create vSphere Replication group → re-add VMs; plan for initial sync window.
