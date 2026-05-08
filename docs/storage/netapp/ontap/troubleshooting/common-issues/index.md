# ONTAP — Common Issues

## Quick Reference

| Symptom | Likely Cause | Action |
|---|---|---|
| Volume full / write errors to hosts | Volume space exhausted; autogrow not configured or hit max | `volume show -fields used-percent,autosize-mode`; increase max-autosize or delete old snapshots with `snapshot delete` |
| Aggregate nearly full (>90%) | Thin-provisioned volumes grew beyond aggregate free space | `storage aggregate show`; move volumes with `volume move start` or reduce snapshot reserves |
| SnapMirror lag exceeding RPO | Network bandwidth contention, dedupe/SnapMirror scheduling conflict, or throttle active | `snapmirror show -fields lag-time,transfer-bytes`; adjust schedule; check `snapmirror config-replication show` |
| NFS mount hangs after SP takeover | Stale NFS lock; automount not recovering after LIF migration | Verify LIF on correct port: `network interface show`; unmount and remount on client; check NFS grace period |
| iSCSI session dropped | LIF failover changed IP; host iSCSI initiator did not reconnect | `iscsi session show`; confirm LIF IP stability; rescan iSCSI on host; verify multipath (`multipath -ll` on Linux) |
| Node takeover not auto-triggering | Storage failover disabled or partner unreachable | `storage failover show`; check cluster interconnect with `cluster ping-cluster -node <node>`; verify `options cf.mode` |
| SMB/CIFS shares inaccessible | CIFS server stopped or Kerberos ticket issue with Active Directory | `vserver cifs show`; `vserver cifs domain info -vserver <svm>`; verify AD connectivity and DNS resolution |
| Slow NFS performance | Jumbo frames not configured end-to-end, or QoS ceiling throttling workload | Check MTU on ONTAP ports (`network port show -fields mtu`) and switches; review QoS stats: `qos statistics performance show` |
| Volume move failing mid-way | Destination aggregate too full, or a cutover window was missed | `volume move show`; check destination aggregate space; re-run `volume move start` with `-cutover-window` extended |
| EMS callhome alerts firing | Disk failure, RAID degraded, or hardware fault | `storage disk show -broken`; `storage aggregate show -state degraded`; check `system health alert show` |

## Before Calling Support

1. Capture current cluster state: `cluster show`, `storage failover show`, `system health alert show`
2. Collect EMS events for the relevant timeframe: `event log show -time-range <start>..<end>`
3. Generate an AutoSupport: `system node autosupport invoke -node * -type all -message "case <number>"`
4. Note the exact ONTAP version: `system image show`
5. Record the hardware platform and serial numbers: `system node show -fields model,serial-number`
6. Describe the timeline of the issue — when it started, what changed (upgrade, config change, load change)
7. Have the NetApp support site login ready: [https://mysupport.netapp.com](https://mysupport.netapp.com)
