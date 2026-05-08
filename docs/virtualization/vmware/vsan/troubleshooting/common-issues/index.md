# vSAN — Common Issues

## Quick Diagnostics

### Cluster Health

```bash
esxcli vsan cluster get
esxcli vsan health cluster list
esxcli vsan health cluster get -t "Overall cluster health"
```

### Object Health

```bash
esxcli vsan debug object list | grep -v "healthy"
esxcli vsan debug object get -u <object-uuid>
esxcli vsan debug resync list
esxcli vsan debug resync summary
```

### Disk and Host Diagnostics

```bash
esxcli vsan storage list
esxcli vsan storage check
```

## Common Issue Reference

| Symptom | First Check | Action |
|---|---|---|
| Object degraded | `esxcli vsan debug object list` | Check disk group health; confirm policy compliance |
| Resync not completing | Capacity headroom | Ensure > 30% free; check for disk failures |
| Disk group absent | Hardware health | Replace failed disk; reconfigure disk group |
| Health test yellow/red | Skyline Health details | Follow remediation steps in KB article linked in test |
| Capacity spike | Snapshots, delta disks | Identify VMs with large snapshots; consolidate |
