# Superna Eyeglass Integration

Eyeglass's primary integration is with NetApp PowerScale SyncIQ — it uses the OneFS REST API to discover, monitor, and orchestrate SyncIQ replication policies. Active Directory integration is required to ensure shares on the DR cluster are accessible to the correct AD security groups immediately after failover, without manual re-permission steps.

DNS server integration enables automated zone cutover during failover. Eyeglass supports Windows DNS (via WMI/DNS API) and BIND for this purpose. Monitoring integration via syslog or SNMP allows Eyeglass events and alerts to flow into Aria Operations, Splunk, or other SIEM/monitoring platforms.

| Integration | Method | Purpose |
|---|---|---|
| NetApp PowerScale SyncIQ | OneFS REST API | Policy discovery, monitoring, failover orchestration |
| Active Directory | LDAP / AD APIs | Share authentication after failover (no re-permissioning) |
| Windows DNS | WMI / DNS server API | Automated DNS zone cutover during failover |
| BIND DNS | DNS zone transfer / nsupdate | Automated DNS cutover for Linux DNS environments |
| Aria Operations | SNMP / syslog | Eyeglass health and DR readiness alerts |
| Splunk | Syslog forwarding | Centralised event log and failover audit trail |
