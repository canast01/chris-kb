# Dell Unity Troubleshooting
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

## Diagnostic Commands

```bash
# Show all components not in an OK health state
uemcli -d <sp_ip> -u admin -p <password> /env/health show -filter "health.value ne OK"

# Show system-wide general health and software version
uemcli -d <sp_ip> -u admin -p <password> /sys/general show

# Show all active system alerts
uemcli -d <sp_ip> -u admin -p <password> /sys/alert show

# Show detailed pool capacity, health, and FAST Cache status
uemcli -d <sp_ip> -u admin -p <password> /stor/pool show -detail

# Show all LUNs with pool assignment and capacity
uemcli -d <sp_ip> -u admin -p <password> /stor/prov/luns show

# Show all replication sessions and their current state
uemcli -d <sp_ip> -u admin -p <password> /rep/session show

# Show all snapshots and their parent resource
uemcli -d <sp_ip> -u admin -p <password> /stor/snap show

# Show both SP states
uemcli -d <sp_ip> -u admin -p <password> /env/sp show

# Show all NAS servers and their SP assignment
uemcli -d <sp_ip> -u admin -p <password> /net/nas show

# Show alert history (most recent 50 events)
uemcli -d <sp_ip> -u admin -p <password> /sys/alert/hist show
```

## Log Locations

| Log / Bundle | Location | How to Access |
|---|---|---|
| Support bundle (SP logs) | Collected from the array on demand | Unisphere: **System > Support > Collect Service Information**; or `uemcli /sys/serviceinfo collect` |
| Unisphere event log | Unisphere GUI | **Unisphere > System > Events** |
| Replication session log | Embedded in the replication session detail | `uemcli /rep/session show -detail` |
| Hardware event log | Embedded in hardware component health | `uemcli /env/health show` |

The support bundle (`collect service information`) gathers SP logs, configuration snapshots, and hardware data into a single file for upload to a Dell support case.

## Before Calling Support

Collect the following before or when opening a Dell support case:

- **SP serial numbers**: visible on the chassis label and in Unisphere under **System > Hardware**.
- **Unity OE version**: `uemcli /sys/sw show` or Unisphere > **System > Software**.
- **Support bundle**: collected via Unisphere > **System > Support > Collect Service Information**; upload directly to the Dell case via the secure upload link.
- **Health page screenshot**: Unisphere health dashboard showing the fault status.
- **Alert history**: `uemcli /sys/alert/hist show` output.
- **Timeline of events**: when the issue started, any changes made in the preceding 24 hours, and client impact.
