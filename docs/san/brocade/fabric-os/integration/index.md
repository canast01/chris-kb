# Brocade Fabric OS Integration

SANnav Management Portal provides fabric-wide monitoring, zoning management, and event correlation across all Brocade switches, replacing the older DCFM/Network Advisor tools. VMware vCenter integration is achieved through FC HBA zoning, ensuring each ESXi host's HBA ports are zoned to the correct storage target ports for datastore access. NetApp ONTAP and Pure FlashArray FC connectivity relies on accurate alias and zone configuration matching the array's target WWPNs. SNMP traps and syslog events are forwarded from each switch to the central monitoring platform for alerting and audit.

- SANnav: fabric-wide visibility, zone management, firmware orchestration
- VMware: FC HBA WWPNs zoned to storage targets per datastore
- NetApp ONTAP: SAN LIF WWPNs registered as aliases in each fabric
- Pure FlashArray: target port WWPNs zoned per host initiator
- SNMP/syslog: forwarded to monitoring platform (port 162 SNMP trap, UDP 514 syslog)
