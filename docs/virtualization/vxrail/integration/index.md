# VxRail Integration

VxRail integrates natively with vCenter as a plugin, providing lifecycle management, cluster health, and hardware visibility directly within the vSphere UI. NSX-T integration enables software-defined networking for VxRail workloads, while Aria Operations (formerly vROps) with the VxRail management pack provides performance monitoring and capacity analytics. Dell SRS/SupportAssist enables proactive remote support by automatically opening service requests for hardware faults detected by iDRAC.

- **vCenter plugin:** VxRail Manager registers as a vCenter plugin; all cluster management is surfaced in the vSphere Client
- **NSX-T:** Overlay networking for VM traffic; NSX Manager points to VxRail-hosted vCenter
- **Aria Operations:** VxRail management pack pulls cluster, node, and vSAN metrics
- **Dell OpenManage:** Hardware inventory and alerting for node-level components (fans, PSUs, drives)
- **SRS/SupportAssist:** Configured during initial deployment; monitors iDRAC events and auto-opens Dell SRs
