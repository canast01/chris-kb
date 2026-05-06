# Performance & Troubleshooting

> Part of the [VMware ESXi CLI Reference](../).

---

## Performance & Troubleshooting

```bash
# Interactive top
esxtop

# Kill a VM process
esxcli vm process list
esxcli vm process kill --type soft --world-id <id>
esxcli vm process kill --type hard --world-id <id>
esxcli vm process kill --type force --world-id <id>

# Kernel stats
vsish -e get /world/<worldid>/sched/statsSummary
vsish -e ls /vm/
vsish -e ls /net/pNics/

# Check for dropped packets
esxcli network nic stats get -n vmnic0 | grep -i drop

# CPU ready (via esxtop, or)
esxcli sched group list
```
