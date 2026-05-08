# Aria Operations — Common Issues

## Adapter Collection Failures

```bash
ssh admin@<vrops-node>
chkadapter --list
chkadapter --instance <adapter-instance-name>
chkadapter --test <adapter-instance-name>
service vmware-vcops-watchdog restart
```

## Log Locations

| Log File | Path | Purpose |
|---|---|---|
| Collector log | `/data/vcops/log/collector.log` | Adapter collection events |
| Adapter log | `/data/vcops/log/adapters/<adapter-name>/` | Per-adapter debug output |
| Casa log | `/data/vcops/log/casa.log` | Authentication and session events |
| Analytics log | `/data/vcops/log/analytics.log` | Metric processing pipeline |

```bash
tail -f /data/vcops/log/collector.log
tail -500 /data/vcops/log/collector.log | grep -i "error\|exception\|failed"
tail -200 /data/vcops/log/adapters/VMwareAdapter/adapter.log
```
