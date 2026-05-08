# Unity — Diagnostics

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
