# ONTAP — Diagnostics

> Diagnostic procedures and log analysis for NetApp ONTAP.

## Diagnostic Commands

```bash
# Cluster and node health
cluster show
system node show
storage failover show

# Aggregate and disk health
storage aggregate show
storage aggregate show -state degraded
storage disk show -broken
storage disk show -raid-state reconstructing

# Volume capacity and status
volume show -fields used-percent,autosize-mode,space-guarantee
volume show -state offline

# Network interface health
network interface show
network interface show -status-oper down
network port show -fields health-status,mtu

# SnapMirror relationship health and lag
snapmirror show -fields lag-time,healthy,relationship-status
snapmirror show -relationship-status broken-off

# EMS event log — recent errors and warnings
event log show -severity error
event log show -severity warning -time-range 24h
event log show -messagename callhome.*

# Active health alerts
system health alert show
system health subsystem show

# iSCSI session and initiator status
iscsi session show
iscsi initiator show

# QoS policy and statistics
qos policy-group show
qos statistics performance show

# AutoSupport status
system node autosupport show
system node autosupport history show
```

## Log Locations

| Log Source | Location / Command |
|---|---|
| EMS event log | `event log show` (CLI); `/mroot/etc/log/ems` (node shell) |
| AutoSupport history | `system node autosupport history show -node <node>` |
| Audit log (admin actions) | `security audit log show` |
| CIFS/SMB audit | SVM-level audit log configured to NAS volume via `vserver audit` commands |
| Crash dumps / core files | `system node coredump show`; files on `/mroot/etc/crash/` |
| Disk firmware log | `storage disk show -fields firmware-revision`; firmware log in AutoSupport |
| Node syslog | `system node run -node <node> syslog` (node shell) |
| SP / BMC logs | `system service-processor log show -node <node>` |

## AutoSupport Bundle

AutoSupport bundles are the primary support artifact. Generate one before calling support:

```bash
system node autosupport invoke -node * -type all -message "case <number> - <description>"
```

## Performance Diagnostics

```bash
# Statistics collection (requires start/stop cycle)
statistics start -object volume -sample-id perf_check
# wait 10–30 seconds
statistics stop -sample-id perf_check
statistics show -sample-id perf_check

# Filter for latency and IOPS
statistics show -sample-id perf_check | grep -E "total_latency|read_latency|write_latency"
statistics show -sample-id perf_check | grep -E "total_ops|read_ops|write_ops"

# QoS workload statistics
qos statistics performance show

# Node-level sysstat (node shell)
system node run -node <node> sysstat -c 5 -x 2
```

## Network Diagnostics

```bash
# Ping from a LIF
network ping -lif <lif> -vserver <svm> -destination <ip>

# Check port health
network port show -fields node,port,health-status,link-status,mtu

# Check cluster interconnect
cluster ping-cluster -node <node>
```
