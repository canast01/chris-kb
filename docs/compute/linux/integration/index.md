# Linux Integration

Linux servers integrate with Active Directory via SSSD and Kerberos for centralised authentication, enabling AD users to log in with domain credentials without local account provisioning. Backup agents (Veeam Agent for Linux or NetBackup client) are deployed via Ansible at provisioning time and registered to the backup server. Monitoring agents include Prometheus `node_exporter` for metrics and the VMware Aria Operations agent where applicable. Storage connectivity uses the iSCSI initiator (`iscsiadm`) with `multipathd` for multipath failover on shared LUNs.

- AD/SSSD: `sssd`, `realmd`, `adcli` — domain join and Kerberos ticket management
- Backup: Veeam Agent for Linux (RHEL/Ubuntu), NetBackup client
- Monitoring: `node_exporter` (port 9100), Aria agent
- Storage: `iscsiadm` for iSCSI, `multipathd` for multipath, `/etc/multipath.conf`
