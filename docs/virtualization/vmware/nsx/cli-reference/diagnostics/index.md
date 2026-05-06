# Diagnostics & Troubleshooting

> Part of the [NSX-T CLI Reference](../).

---

## Diagnostics & Troubleshooting

```bash
# Central CLI (run from NSX Manager against any node)
nsxcli -u admin

# Traceflow (Manager UI / API primarily, CLI helper)
get traceflows

# Packet capture on Edge
debug packet capture interface fp-eth0 count 500
debug packet capture interface nsx-geneve count 500

# Log levels
set service manager logging-level debug
set service manager logging-level info

# System logs
get logs
get log manager follow
```
