# Unity — Common Issues

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| LUN not visible to FC host | Host not registered in Unisphere, or FC zoning incomplete | Register the host and its initiator WWNs in Unisphere > Hosts; confirm FC zone is active and contains both host and Unity SP ports |
| LUN not visible to iSCSI host | iSCSI IQN not registered in Unisphere, or iSCSI portal unreachable | Add host IQN in Unisphere > Hosts; verify iSCSI portal IP is reachable from host; confirm iSCSI initiator login |
| Replication session in Error or Paused state | Network interruption between source and destination arrays, or destination pool full | Check `uemcli /rep/session show`; verify network reachability; resolve capacity issue; resume with `uemcli /rep/session -id <id> resume` |
| NAS server not responding | SP failover in progress, NAS server in error state, or network interface issue | Check Unisphere health dashboard; verify NAS server status with `uemcli /net/nas show`; confirm the NAS server IP is on the active SP |
| Pool approaching capacity | Snapshot accumulation, or thin LUNs consuming more than expected | Run `uemcli /stor/pool show -detail`; delete unneeded snapshots with `uemcli /stor/snap delete`; expand pool or thin-provision additional capacity |
| SP fault (SP offline) | Hardware failure — memory, CPU, SSD, or power module | Check fault LED on SP chassis; run `uemcli /env/health show -filter "health.value ne OK"`; peer SP takes over automatically; open Dell support case immediately |
| Write cache dirty warning | SP peer communication lost; cache cannot mirror to partner | Verify both SPs are online and the SP interconnect link is healthy; resolve SP communication fault before further I/O accumulates |
| Disk fault in pool | Physical drive failure | Check `uemcli /env/health show -filter "health.value ne OK"`; identify faulted drive; replace physical drive; Unity automatically rebuilds if a hot spare or free drive is available |
| Unisphere GUI unreachable | SP management NIC fault, or management service crashed | Try the peer SP's management IP; restart the Unisphere service via `uemcli /sys/service start -svc unisphere` if accessible via uemcli |

## Incident Triage

When a host reports I/O errors or a LUN is inaccessible, work through this sequence before escalating:

- [ ] Check Unisphere health dashboard for any active alerts in the last 30 minutes
- [ ] Run `uemcli /env/health show -filter "health.value ne OK"` to identify any faulted components
- [ ] Verify both SP A and SP B are active: `uemcli /env/sp show`
- [ ] Check pool health and capacity: `uemcli /stor/pool show -detail`
- [ ] Review replication session state: `uemcli /rep/session show`
- [ ] Check host registration and LUN access: `uemcli /remote/host show` and `uemcli /stor/config/lunacl show`
- [ ] Review the Unisphere event log: System → Events → filter by time of incident

| Question | Answer |
|---|---|
| Which hosts are affected and what LUN names? | |
| Are both SPs online? | |
| Is the pool healthy and have capacity? | |
| Are there active alerts at the time of the incident? | |
| Has the replication session state changed? | |
