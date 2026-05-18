# FlashArray — Design Standards

```
FlashArray Design Checklist — Key Areas
┌──────────────────────────────────────────────────────────┐
│  Naming         │  array / volume / host / pg conventions│
├──────────────────────────────────────────────────────────┤
│  Host Zones     │  1 initiator : 1 target per FC zone    │
├──────────────────────────────────────────────────────────┤
│  Multipath      │  Round-robin IOPS=1 (VMware/Linux)     │
├──────────────────────────────────────────────────────────┤
│  Protection     │  PGroup per app → snapshot + replicate │
├──────────────────────────────────────────────────────────┤
│  Capacity       │  < 80% used; account for snapshots     │
├──────────────────────────────────────────────────────────┤
│  Security       │  RBAC, SafeMode, SAML/LDAP, TLS syslog │
└──────────────────────────────────────────────────────────┘
```

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

## Sizing Guidelines

| Dimension | Guidance |
|---|---|
| Usable capacity | Account for effective capacity after deduplication and compression — Pure1 provides workload-specific data reduction estimates; typical all-flash workloads achieve 3:1 to 5:1 effective |
| Raw drive capacity | Size so that after a single drive failure and rebuild, usable headroom remains above 70% |
| IOPS | FlashArray //X: up to 2M+ IOPS per array depending on model; verify per-model datasheet for your workload block size |
| Latency | Sub-millisecond (typically 100–300 µs) for random 4K reads at normal utilisation; NVMe//X achieves sub-100 µs |
| Maximum volumes | Up to 500,000 volumes per array depending on model |
| Maximum hosts | Up to 10,000 host entries per array |
| ActiveCluster RTT | Maximum 5 ms round-trip time between arrays for synchronous replication |
| Controller upgrade | Evergreen controller upgrades do not require capacity changes — data stays in place |

## Build Baseline

Required settings to configure on every new FlashArray before production:

- [ ] Set array name to match naming convention (`purearray setattr --name <name>`)
- [ ] Configure DNS servers (`puredns setattr --domain <domain> --nameservers <ip1>,<ip2>`)
- [ ] Configure NTP servers (`purentpserver add <server>`) — at least two
- [ ] Set timezone (`purearray setattr --timezone <tz>`)
- [ ] Configure syslog forwarding to central log aggregator
- [ ] Configure SMTP alert relay and array-wide email alert recipients
- [ ] Join Active Directory or configure LDAP for admin authentication
- [ ] Create local break-glass admin account with strong password stored in PAM vault
- [ ] Disable default `pureuser` account after AD/LDAP is validated
- [ ] Configure SNMP v3 community or trap destination if SNMP monitoring is required
- [ ] Enable Pure1 phone-home and verify connectivity
- [ ] Configure management interface on dedicated management VLAN
- [ ] Configure replication interfaces on dedicated replication VLAN
- [ ] Enable SafeMode (immutable snapshots) — engage Pure Support to enable
- [ ] Apply SSL certificate from internal CA on management interface
- [ ] Document array serial number, management IP, Purity version, and FC/iSCSI port WWNs/IQNs in CMDB

## Configuration Checklist

Ordered steps for initial FlashArray setup:

1. **Rack and cable** — install chassis, connect power (dual PSU to separate PDUs), connect management Ethernet, connect data fabric (FC or iSCSI), connect replication Ethernet
2. **Initial CLI access** — connect serial console or management Ethernet; complete Purity setup wizard at first boot
3. **Set array name and network** — assign management IP, gateway, DNS; set array name and timezone
4. **Activate licensing** — register in Pure1 using the array serial number to activate the licence and enable monitoring
5. **Configure NTP** — add at least two NTP servers; verify time sync before proceeding
6. **Configure alert notifications** — set SMTP relay and admin email addresses
7. **Configure syslog** — forward to central SIEM or log aggregator
8. **Configure authentication** — join AD or configure LDAP; create role-mapped admin groups; disable default `pureuser` once validated
9. **Apply security hardening** — see [Security](../../security/)
10. **Zone FC fabric** — create single-initiator, single-target zones for each host HBA to array target ports; or configure iSCSI discovery portals
11. **Register hosts** — `purehost create <hostname>`, `purehost setifs --wwn <wwn> <hostname>`
12. **Create host groups** — `purehgroup create <hgroupname>`, `purehgroup addhosts --hostlist <hosts> <hgroupname>`
13. **Provision volumes** — `purevol create --size <size> <volname>`
14. **Connect volumes** — `purehgroup addvol --vollist <volname> <hgroupname>`
15. **Verify host connectivity** — rescan HBA bus on each host; confirm volumes visible via multipath driver
16. **Configure protection groups** — create protection group, add volumes, set snapshot schedule and replication targets
17. **Enable replication** — configure connection to remote array; add replication target to protection group
18. **Configure ActiveCluster** — create pod, stretch to remote array, move volumes into pod (if required)
19. **Validate and document** — `purearray list`, `puredrive list`, `purealert list`; document build in CMDB

## Multipath Configuration (VMware PSP)

For VMware hosts connected to FlashArray, set the Path Selection Policy to Round Robin with IOPS limit of 1:

```bash
esxcli storage nmp device set -d <naa_id> -P VMW_PSP_RR
esxcli storage nmp psp roundrobin deviceconfig set -d <naa_id> --type iops --iops 1
```

For Linux DM-Multipath, use the Pure Storage recommended `multipath.conf` settings (available from Pure Support): `path_grouping_policy multibus`, `path_checker tur`, `failback immediate`, `no_path_retry 18`.
