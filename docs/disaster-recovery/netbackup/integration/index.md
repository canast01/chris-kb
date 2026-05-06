# NetBackup Integration

NetBackup integrates with a wide range of infrastructure platforms via supported agents and APIs. Dell Data Domain integration uses the OpenStorage Technology (OST) plugin installed on media servers, enabling inline deduplication and replication directly between Data Domain appliances. VMware integration leverages the NetBackup for VMware agent and VMware VADP (vStorage APIs for Data Protection) for agentless snapshot-based backups of VMs without guest-level agents.

| Integration | Method | Notes |
|---|---|---|
| Dell Data Domain | OST plugin on media server | Enables dedup, DD Boost, AIR replication |
| VMware vSphere | NBU for VMware agent, VADP | Agentless; vCenter credentials required |
| Pure FlashArray | NetBackup Snapshot Client + Pure plugin | Hardware snapshot integration for near-zero RPO |
| AWS S3 | Cloud storage unit (CSU) | Long-term retention tier; configure lifecycle rules |
| Azure Blob | Cloud storage unit (CSU) | Requires Azure credentials stored in NBU |
| SIEM (Splunk, etc.) | Audit log export / syslog | Configure `/usr/openv/netbackup/logs/audit/` forwarding |
| CyberArk | AAM / Central Credential Provider | Service account passwords retrieved at runtime |
