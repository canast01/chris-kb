# VMware Cloud Foundation Integration

VCF integrates natively with Aria Operations (formerly vRealize Operations) through the VCF Management Pack, which provides topology views of management and workload domains, vSAN health dashboards, and capacity analytics scoped to VCF constructs. Aria Automation integrates with VCF workload domains as cloud accounts, enabling infrastructure-as-code provisioning on top of SDDC Manager-managed clusters. NSX Federation is used when multiple VCF instances span sites and require a unified NSX policy plane across locations.

| Integration | Method | Notes |
|---|---|---|
| Aria Operations | Management Pack for VCF | Install MP on Aria Ops; add SDDC Manager as source |
| Aria Automation | Cloud Account (VCF type) | Requires vCenter and NSX credentials per domain |
| NSX Federation | Global Manager | Cross-site: deploy Global Manager outside VCF lifecycle |
| Third-party SIEM | Syslog from SDDC Manager | Configure under SDDC Manager > Administration > Syslog |
| Active Directory | SDDC Manager Identity | Add AD/LDAP under SDDC Manager > Administration > SSO |
| Backup Tools | VM-level via vCenter | VCF management VMs backed up at vCenter level (no native integration) |
