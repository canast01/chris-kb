# VxRail Security

BIOS and iDRAC hardening is applied per Dell PowerEdge security baseline, including disabling unused boot devices, enforcing iDRAC access controls, and enabling Secure Boot where supported. ESXi lockdown mode restricts direct host access and forces all management through vCenter, while vSAN data-at-rest encryption uses the vCenter Key Management Server (KMS) integration to protect stored data. Certificate management for VxRail Manager and ESXi hosts is handled through VxRail Manager's certificate workflow, replacing self-signed certificates with CA-signed ones during or after initial deployment.

- **BIOS/iDRAC:** Disable unused ports, enforce strong iDRAC credentials, enable iDRAC audit logging
- **ESXi lockdown mode:** Normal or strict lockdown enforced on all cluster nodes
- **vSAN encryption:** Data-at-rest encryption enabled via KMS; key rotation schedule defined
- **Certificate management:** VxRail Manager orchestrates ESXi and VxRail Manager certificate replacement
- **vCenter RBAC:** Dedicated VxRail operator role scoped to the VxRail cluster; no shared admin credentials
