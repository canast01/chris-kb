# FlashArray Troubleshooting
## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Drive in `failed` or `recovering` state | NVMe or SAS SSD failure; Purity begins automatic rebuild | Run `puredrive list` to confirm state; monitor rebuild with `puredrive list --progress`; open Pure support case if rebuild stalls or multiple drives fail |
| Host loses all paths to volumes | FC zone misconfiguration, iSCSI network outage, or both HBAs failed | Run `purehost list` and `pureport list`; verify FC zoning on switches; confirm iSCSI connectivity and routing; check host HBA status |
| Host loses one path (single-path warning) | One HBA, port, or FC switch path failed | Identify the failed path via `purehost list --connection`; check the physical port and cable on the affected array port; investigate FC switch or iSCSI switch for port errors |
| ActiveCluster pod mediator unreachable | Network change between arrays and Purity Mediator service | Run `purepod list`; verify Mediator IP is reachable from both arrays on port 443; pods continue replicating across the inter-array link even without Mediator — Mediator is only required for tiebreaker during split-brain |
| ActiveCluster pod out of sync (`unhealthy` or `paused`) | Inter-array replication link down or overloaded | Run `purepod list` for pod status; check replication network path; confirm replication interface is `up` on both arrays with `pureport list`; check for bandwidth saturation |
| Unexpected capacity growth | Snapshot retention not expiring old snaps; volume over-provisioning | Run `puresnap list --space` to identify largest consumers; check protection group schedules with `purepgroup list --schedule`; expire or eradicate stale snapshots |
| Purity upgrade hangs or fails mid-way | Pre-check condition not met; drive fault during upgrade | Check `purearray upgrade --status`; review upgrade logs; contact Pure Support with upgrade log output — do not reboot controllers manually |
| Volume not visible on host after provisioning | Volume connected to host but not to the correct host group, or host WWN/IQN not registered | Run `purehost list --connection` and `purehgroup list --connection`; confirm the host's WWN or IQN is registered; confirm volume is connected to the host or its host group; rescan HBA on the host side |
| Array reporting high latency (> 1 ms reads) | Workload spike, QoS limit, or drive rebuild consuming controller resources | Run `purearray monitor` for real-time latency/IOPS; run `purevol list --monitor` to identify top consumers; check for active drive rebuilds with `puredrive list` |
| Controller shows `not ready` or missing | Controller hardware failure or Purity process crash | Run `purearray list --controller`; confirm the surviving controller is serving I/O; open a P1 Pure support case immediately |

## Diagnostic Commands

```bash
# Overall array health and Purity version
purearray list
purearray list --controller

# Active alerts (all severities)
purealert list

# Drive health and rebuild status
puredrive list
puredrive list --progress

# Array capacity and data reduction
purearray list --space

# Real-time performance (latency, IOPS, bandwidth)
purearray monitor

# Per-volume performance
purevol list --monitor

# Host path and connection status
purehost list
purehost list --connection
purehgroup list
purehgroup list --connection

# FC/iSCSI/NVMe port status
pureport list

# Protection group schedules and replication status
purepgroup list
purepgroup list --schedule

# ActiveCluster pod status and failover preference
purepod list
purepod list --replicating
purepod list --failover-preference

# Snapshot space usage
puresnap list --space

# Collect diagnostic bundle for support
purediag --send     # sends to Pure Support directly if phone-home is active
purediag --output /tmp/diag.tgz   # saves locally if phone-home is unavailable
```

## Log Locations

| Log | Location / Command |
|---|---|
| Purity system log (controller events, upgrades) | `purearray list --log` or `/var/log/purity/` on the controller via SSH |
| Alert history | `purealert list --flagged true` (flagged/resolved alerts) |
| Audit log (admin actions) | `pureadmin list --audit` |
| Replication log | `purepgroup list --replication` |
| Diagnostic bundle | `purediag --output <path>` — includes all logs, configs, and metrics |
| Drive event log | `puredrive list` — per-drive state history visible in diagnostic bundle |
| Pure1 event timeline | Pure1 portal > Arrays > select array > Events |

## Before Calling Support

Collect the following before opening a Pure support case to accelerate triage:

- [ ] Array name and serial number: `purearray list`
- [ ] Purity//FA version: `purearray list` (Version field)
- [ ] Active alerts: `purealert list` — copy full output
- [ ] Drive status: `puredrive list` — copy full output
- [ ] Controller status: `purearray list --controller`
- [ ] Relevant performance data: `purearray monitor` output at time of issue
- [ ] Host connection details if the issue is host-facing: `purehost list --connection`
- [ ] Pod status for ActiveCluster issues: `purepod list`
- [ ] Diagnostic bundle: `purediag --output /tmp/diag_<date>.tgz` and upload to case
- [ ] Symptom description: what changed before the issue, when it started, and business impact
- [ ] Change log: any changes made in the 24 hours before the issue (firmware, zoning, network, OS patching)
