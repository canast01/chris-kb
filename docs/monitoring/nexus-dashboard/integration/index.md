# Nexus Dashboard Integration

Cisco ACI APIC integration is the primary use case, providing policy management, fabric health, and fault visibility for ACI-based data centre fabrics. NX-OS fabrics are managed via NDFC, which replaces DCNM as the fabric controller. Fabric events and faults are forwarded to Splunk via syslog for security correlation and long-term retention. ServiceNow ITSM integration creates incidents for P1/P2 faults automatically. The Aria Operations Cisco management pack correlates fabric health with the broader VMware infrastructure view. Syslog forwarding to SIEM captures all ND admin and policy change events.

| Integration | Type | Purpose |
|---|---|---|
| ACI APIC | Inbound | Policy management and fabric visibility |
| NX-OS / NDFC | Inbound | NX-OS fabric management |
| Splunk | Outbound | Fabric event forwarding via syslog |
| ServiceNow ITSM | Outbound | P1/P2 fault ticketing |
| Aria Operations | Outbound | Correlated VMware + Cisco visibility |
| SIEM (syslog) | Outbound | Admin and policy change audit events |
