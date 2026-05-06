# FlashArray Standards

## Naming Conventions

| Object | Pattern | Example |
|---|---|---|
| Volume | `<env>-<app>-<function>-<seq>` | `prod-oracle-data-01` |
| Volume (boot) | `<env>-<hostname>-boot` | `prod-esxi01-boot` |
| Host | `<hostname>` (match server hostname exactly) | `prod-esxi-01` |
| Host group | `<env>-<cluster>` | `prod-vcenter-cluster01` |
| Protection group (local) | `<env>-<app>-pg` | `prod-oracle-pg` |
| Protection group (remote) | `<env>-<app>-pg-to-<remote>` | `prod-oracle-pg-to-dr` |
| Pod (ActiveCluster) | `<app>-pod` | `oracle-pod` |
| Snapshot (on-demand) | `<volname>.<purpose>.<date>` | `prod-oracle-data-01.premigration.20260501` |
| Array name | `<site>-fa-<seq>` | `lon-fa-01` |

## Build Baseline

Required settings to configure on every new FlashArray before it enters production:

- [ ] Set array name to match naming convention (`purearray setattr --name <name>`)
- [ ] Configure DNS servers (`puredns setattr --domain <domain> --nameservers <ip1>,<ip2>`)
- [ ] Configure NTP servers (`purentpserver list` / `purentpserver add <server>`)
- [ ] Set timezone (`purearray setattr --timezone <tz>`)
- [ ] Configure syslog forwarding to central log aggregator
- [ ] Configure SMTP alert relay (`puresmtp create --username <> --password <> --relay-host <> --sender-domain <> default`)
- [ ] Set array-wide email alert recipients (`purealert create --email <addr> <name>`)
- [ ] Join Active Directory or configure LDAP for admin authentication
- [ ] Create local break-glass admin account with strong password stored in PAM vault
- [ ] Disable default `pureuser` account after AD/LDAP is validated
- [ ] Configure SNMP v3 community or trap destination if SNMP monitoring is required
- [ ] Enable Pure1 phone-home and verify connectivity
- [ ] Configure management interface on dedicated management VLAN
- [ ] Configure replication interfaces on dedicated replication VLAN
- [ ] Set Safe Mode (immutable snapshots) — engage Pure Support to enable
- [ ] Apply SSL certificate from internal CA or public CA on management interface
- [ ] Document array serial number, management IP, Purity version, and FC/iSCSI port WWNs/IQNs in CMDB

## Configuration Checklist

Ordered steps for initial FlashArray setup:

1. **Rack and cable** — install chassis, connect power (dual PSU to separate PDUs), connect management Ethernet, connect data fabric (FC or iSCSI), connect replication Ethernet
2. **Initial CLI access** — connect serial console or management Ethernet; access Purity setup wizard at first boot
3. **Set array name and network** — assign management IP, gateway, and DNS; set array name and timezone
4. **Activate licensing** — register the array in Pure1 using the array serial number to activate the license and enable Pure1 monitoring
5. **Configure NTP** — add at least two NTP servers; verify time sync before proceeding
6. **Configure alert notifications** — set SMTP relay and add admin email addresses for alerts
7. **Configure syslog** — forward to central SIEM or log aggregator
8. **Configure authentication** — join AD or configure LDAP; create role-mapped admin groups; disable default `pureuser` once validated
9. **Apply security hardening** — see security/index.md for ordered hardening steps
10. **Zone FC fabric** — create initiator zones for each host HBA to array target ports (single-initiator, single-target per zone); or configure iSCSI discovery portals
11. **Register hosts** — create host entries and add WWNs or IQNs: `purehost create <hostname>`, `purehost setifs --wwn <wwn> <hostname>`
12. **Create host groups** — group hosts into clusters: `purehgroup create <hgroupname>`, `purehgroup addhosts --hostlist <hosts> <hgroupname>`
13. **Provision volumes** — create volumes using naming convention: `purevol create --size <size> <volname>`
14. **Connect volumes** — connect volumes to host group: `purehgroup addvol --vollist <volname> <hgroupname>`
15. **Verify host connectivity** — on each host, rescan HBA bus and confirm volumes are visible via multipath driver
16. **Configure protection groups** — create protection group, add volumes, set snapshot schedule and replication targets
17. **Enable replication** (if required) — configure connection to remote array; add replication target to protection group
18. **Configure ActiveCluster** (if required) — create pod, stretch to remote array, move volumes into pod
19. **Validate and document** — run `purearray list`, `puredrive list`, `purealert list`; document build in CMDB and handover checklist
