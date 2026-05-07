# Cluster Status & Capacity

> Part of the [vSAN CLI Reference](../).
---

## Cluster Status

```bash
# From ESXi host shell
esxcli vsan cluster get
esxcli vsan storage list
esxcli vsan storage list | grep -i ssd
esxcli vsan storage list | grep -i hdd

# Disk groups
esxcli vsan storage list | grep -E "Display Name|Type|UUID"

# Network
esxcli vsan network list
esxcli vsan network ipconfig list
```

---

## Capacity & Objects

```bash
# Datastore info
esxcli vsan datastore list

# Object count
esxcli vsan debug object list | wc -l

# Inaccessible objects
esxcli vsan debug object list | grep -v "Healthy"
```

---

## Skyline Health (vSphere Client Context)

Accessed in vSphere Client → Cluster → Monitor → vSAN → Skyline Health

```bash
# From ESXi — equivalent checks
esxcli vsan health cluster get | grep -i fail
esxcli vsan health cluster get | grep -i warning

# vSAN performance service status
esxcli vsan perf get
```
