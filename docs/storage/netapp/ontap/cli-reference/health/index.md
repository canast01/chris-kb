# System Health & Events

> Part of the [NetApp ONTAP CLI Reference](../).

---

## System Health & Events

```bash
# Health
system health status show
system health alert show
system health subsystem show
system health node-connectivity show

# Event log
event log show
event log show -severity emergency
event log show -severity alert
event log show -node <node>
event log show -time >1h

# Firmware / images
system node image show
system node image update -node <node> -package <pkg>
system node upgrade-revert show
```
