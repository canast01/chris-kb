# Aria Suite Lifecycle Security

Certificate rotation for LCM-managed products is performed through the Locker, which stores certificates and private keys encrypted at rest; certificates should be replaced via LCM (not directly on appliances) to ensure consistent tracking and avoid configuration drift. LCM RBAC defines two primary roles — `LCM Admin` (full access including product deployment and upgrades) and `LCM Content Developer` (read-only plus content library access) — and roles are assigned via Workspace ONE Access groups rather than individual user accounts. SSH access to the LCM appliance should be restricted to jump-host source IPs via firewall rules, and root login should be audited through a PAM-based session logger or a bastion host with session recording.

**Security hardening checklist:**
- [ ] Default `admin` password changed at first login; stored in enterprise password vault
- [ ] Locker master password set and documented in vault — loss requires full re-import of all certs
- [ ] SSH restricted to management jump-host CIDR via host firewall (`/etc/sysconfig/iptables` or NSX micro-segmentation)
- [ ] LCM RBAC roles assigned to AD/LDAP groups, not individual accounts
- [ ] Audit log retention: configure syslog forwarding to SIEM under LCM Settings > Log Management
- [ ] Certificate private keys never exported outside LCM Locker except for documented break-glass scenarios
- [ ] Review LCM access logs monthly: `/var/log/lcm/access.log`
