# VxRail Vendor Support

Dell support for VxRail is accessed via the Dell support portal at support.dell.com, where service requests are opened against the cluster service tag or individual node service tags. Before opening an SR, collect the VxRail support bundle from VxRail Manager (System > Support > Generate Support Bundle), which includes logs from all nodes, vCenter, and VxRail Manager itself. SRS/SupportAssist should be configured to auto-generate SRs for hardware faults, reducing time to detection for physical component failures.

- **Support portal:** [support.dell.com](https://support.dell.com)
- **SR creation:** Use cluster service tag or node service tag; select VxRail product line
- **Log bundle:** VxRail Manager > System > Support > Generate Support Bundle
- **Bundle contents:** VxRail Manager logs, ESXi host logs, vSAN traces, vCenter events
- **SRS/SupportAssist:** Proactive SR creation for iDRAC hardware events; verify configuration post-deployment
- **Version matrix:** VxRail compatibility matrix available at Dell's interoperability matrix tool (IMT)
- **Escalation:** Request Engineering Escalation in the SR if the issue is blocking production
