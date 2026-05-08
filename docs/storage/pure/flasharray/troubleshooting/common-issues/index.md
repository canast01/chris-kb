# FlashArray — Common Issues

## Quick Reference

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
