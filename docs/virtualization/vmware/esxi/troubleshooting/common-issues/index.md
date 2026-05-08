# ESXi — Common Issues

## Quick Reference

| Symptom | First Check | Key Command |
|---|---|---|
| Host disconnected from vCenter | vpxa / hostd service | `/etc/init.d/vpxa restart` |
| Host not responding | PSOD, mgmt network partition | IPMI/iLO console access |
| All paths down (APD) | Storage fabric, HBA | `esxcli storage core path list` |
| VMFS datastore inaccessible | APD/PDL state, rescan | `esxcli storage core adapter rescan` |
| High CPU ready | NUMA, DRS, overcommit | `esxtop` — `%CSTP`, `%RDY` |
| High balloon / swap | Memory overcommit | `esxtop` — `MCTLSZ`, `SWR/s` |
| NTP drift | Clock skew, auth failures | `esxcli system ntp get` |
| PSOD | Hardware fault, driver bug | `/var/core/` vmss/vmem dumps |
