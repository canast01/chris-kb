# Distributed Firewall (DFW)

> Part of the [NSX-T CLI Reference](../).

---

## Distributed Firewall (DFW) — NSX Manager

```bash
# DFW rules overview (via NSX Manager shell)
nsxcli
get firewall stats
get dfw stats

# From ESXi host — inspect DFW
summarize-dvfilter
vsipioctl getrules -f <filter_name>
vsipioctl getaddrsets -f <filter_name>
vsipioctl getstats -f <filter_name>
```
