# Performance & QoS

> Part of the [NetApp ONTAP CLI Reference](../).

---

## Performance & QoS

```bash
# Statistics
statistics show
statistics start -object volume -sample-id perf_check
statistics stop -sample-id perf_check

# QoS policy groups
qos policy-group show
qos policy-group create -policy-group <name> -vserver <svm> -max-throughput <iops>IOPS
qos policy-group modify -policy-group <name> -max-throughput <iops>IOPS
qos workload show
qos statistics performance show
```
