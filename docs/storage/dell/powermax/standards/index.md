# PowerMax Standards
## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Symmetrix ID (SID) | 3–12 digit serial, used as-is | `000123456789` |
| Storage Group | `<site>-<app>-<tier>-SG` | `LON-ORACLE-P1-SG` |
| Device Group | `<site>-<app>-DG` | `LON-ORACLE-DG` |
| Port Group | `<site>-<fabric>-PG` | `LON-FAB-A-PG` |
| Initiator Group | `<hostname>-IG` | `db01-LON-IG` |
| Masking View | `<hostname>-<sg>-MV` | `db01-LON-LON-ORACLE-P1-MV` |
| SRDF Group | `RDFg<number>-<site-pair>` | `RDFg10-LON-AMS` |
| SnapVX Snapshot | `<app>-snap-<YYYYMMDD>` | `ORACLE-snap-20260501` |
| RDF Port Group | `<site>-RDF-PG` | `LON-RDF-PG` |

## Build Baseline

Every new PowerMax deployment should meet the following baseline before handover to operations:

- **Solutions Enabler** installed on at least two management hosts (primary and secondary) and pointing to the production SID.
- **Unisphere for PowerMax** deployed as a vApp or physical appliance; connected to the array and secondary SE host.
- **Embedded Management** enabled on the array for break-glass SYMCLI access without external SE.
- **PowerPath/VE** (VMware) or **PowerPath** (Linux/Windows) installed on all production hosts; multipath policy set to `Optimized`.
- **SRDF groups** defined with the remote array and tested for both SRDF/S (synchronous) and SRDF/A (asynchronous) pairs where required.
- **FAST VP** policies configured; at minimum one SLO assigned to production storage groups.
- **SnapVX** expiry policies configured on all storage groups to enforce maximum snapshot retention.
- **Alert thresholds** configured in Unisphere: response time >2 ms, port utilisation >70%, thin pool >75%.
- **Service Level Objectives (SLOs)** assigned to all production storage groups (`Diamond`, `Platinum`, `Gold`, `Silver`, `Bronze`, or `Optimized`).
- **Solutions Enabler symapi.db** backed up after initial configuration.

## Configuration Checklist

- [ ] Array registered in CMDB with SID, model, location, and owning team
- [ ] Solutions Enabler `netcnfg` file updated to include the array SID and IP
- [ ] Unisphere for PowerMax configured with LDAP/AD authentication and local admin account disabled
- [ ] All front-end director ports zoned correctly; zoning validated with `symcfg -sid <SID> show`
- [ ] Storage groups created per application with correct SLO assigned
- [ ] Masking views created and verified — hosts can see LUNs and I/O is confirming on both paths
- [ ] SRDF groups created, pairs established, and pair states confirmed `Synchronized` or `Consistent`
- [ ] SnapVX policy set on all production storage groups; first snapshot tested and linked
- [ ] FAST VP policy active; tier movement verified after 24 hours of production I/O
- [ ] Syslog and SNMP trap forwarding configured to monitoring platform
- [ ] Quarterly review schedule set for capacity, SRDF health, and SnapVX quota usage
