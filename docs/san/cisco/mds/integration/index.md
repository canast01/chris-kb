# Cisco MDS Integration

Nexus Dashboard Fabric Controller (NDFC) provides centralised zone management, fabric topology visibility, and performance monitoring across all MDS switches, replacing the older DCNM tool. VMware FC connectivity is managed by ensuring ESXi host HBA WWPNs are registered in the correct VSAN and zoned to storage target ports. Pure FlashArray and Dell PowerMax target port WWPNs are registered as device aliases and added to zone member sets. SNMP traps and syslog messages are forwarded from each switch to the monitoring platform for alerting, trending, and audit trail.

- NDFC: centralised zone management, fabric discovery, performance dashboards
- VMware: ESXi HBA WWPNs in production VSAN, zoned to storage targets
- Pure FlashArray: target port device-aliases per array port, zoned per host
- Dell PowerMax: FA port WWPNs registered as device-aliases in each VSAN
- SNMP/syslog: forwarded to monitoring platform (SNMP trap v2c/v3, syslog UDP 514)
