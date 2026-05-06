# RecoverPoint Integration

RecoverPoint for VMs (RP4VM) integrates with vCenter as a plugin, enabling per-VM replication policy assignment and consistency group management directly from the vSphere Client. VPLEX integration enables distributed consistency groups that span metro storage fabrics, providing continuous replication across sites without requiring a dedicated replication network. VMware Site Recovery Manager (SRM) integrates with RecoverPoint to orchestrate automated failover and failback workflows, replacing manual CG image access steps with runbook-driven recovery plans.

- **RP4VM (vCenter plugin):** vSphere replication splitter intercepts writes at the VMDK level; managed through vCenter plugin
- **VPLEX integration:** Distributed CGs span VPLEX metro/geo fabrics; RecoverPoint splitter installed on VPLEX director
- **Dell PowerMax/Unity:** Registered as production or replica volumes; array-based splitter (XIO/SRDF) or fabric splitter used
- **SRM integration:** RecoverPoint SRA (Site Recovery Adapter) installed on SRM server; recovery plans reference RecoverPoint CGs
- **Aria Operations:** RecoverPoint management pack collects RPA health, CG lag, journal utilization, and link state metrics
