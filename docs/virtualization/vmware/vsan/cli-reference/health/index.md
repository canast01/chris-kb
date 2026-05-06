# Health & Diagnostics

> Part of the [vSAN CLI Reference](../).

---

## Health & Diagnostics

```bash
# Summary health
esxcli vsan health cluster get
esxcli vsan health summary get

# Trace
esxcli vsan trace get

# VM objects
esxcli vsan debug object list
esxcli vsan debug object list | grep -i unhealthy
esxcli vsan debug object list | grep -i absent

# Resync
esxcli vsan debug resync list
esxcli vsan debug resync summary get

# Component status
esxcli vsan debug component list
```
