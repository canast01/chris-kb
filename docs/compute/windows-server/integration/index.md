# Windows Server Integration

Windows Server systems are domain-joined to Active Directory during provisioning, with Group Policy used to enforce baseline configurations and role-specific settings across server types. Patch management is delivered via WSUS or SCCM, with servers assigned to the appropriate patch ring based on environment (dev, staging, production). Monitoring agents (SCOM or Aria Operations agent) and backup agents (Veeam or NetBackup) are deployed post-build as part of the standard server onboarding workflow.

- **Active Directory:** Domain join via `Add-Computer`; GPO applied at OU level by server role
- **WSUS/SCCM:** Servers assigned to patch group; maintenance windows control reboot scheduling
- **SCOM/Aria agent:** Installed post-build; management server and resource pool assigned during configuration
- **Veeam agent:** Veeam Agent for Windows installed; backup job assigned from Veeam Backup & Replication console
- **NetBackup client:** nbclient installed; policy assigned by NetBackup master server
- **iSCSI/MPIO:** iSCSI initiator configured with target IQNs; MPIO with DSM installed for multipath storage
- **FC HBA:** Driver version pinned to vendor HCL; zoning confirmed with storage team before enabling
