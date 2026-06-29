---
tags:
  - dr
---
# Performance — Failure Testing

```bash
# Kill a process (simulate crash)
kill -9 $(pgrep nginx)

# CPU saturation (use with caution — runs until ^C)
stress-ng --cpu 4 --cpu-load 95 --timeout 60s

# Memory pressure
stress-ng --vm 2 --vm-bytes 80% --timeout 60s

# Disk I/O saturation
fio --name=fill --ioengine=posixaio --rw=randwrite --size=1G --numjobs=4 --runtime=60 --filename=/tmp/fio-test

# Network packet loss (requires tc/netem)
tc qdisc add dev eth0 root netem loss 20%
# Remove after test
tc qdisc del dev eth0 root
```


```text title="Expected output"
$ kill -9 $(pgrep nginx)
$ stress-ng --cpu 4 --cpu-load 95 --timeout 60s
stress-ng: info: [8742] defaulting to a 60 second run per stressor
stress-ng: info: [8742] dispatching hogs: 4 cpu
stress-ng: info: [8742] successful run completed in 60.02s
stress-ng: info: [8742] for a 60.02s run time:
stress-ng: info: [8742]    4,287,456 bogo ops
stress-ng: info: [8742] CPU: 95.2% user, 2.1% system, 2.7% idle
$ stress-ng --vm 2 --vm-bytes 80% --timeout 60s
stress-ng: info: [8751] defaulting to a 60 second run per stressor
stress-ng: info: [8751] dispatching hogs: 2 vm
stress-ng: info: [8751] successful run completed in 60.01s
stress-ng: info: [8751] for a 60.01s run time:
stress-ng: info: [8751]    156,892 bogo ops
$ fio --name=fill --ioengine=posixaio --rw=randwrite --size=1G --numjobs=4 --runtime=60 --filename=/tmp/fio-test
fill: (g=0): rw=randwrite, bs=(R) 4096B-4096B, (W) 4096B-4096B, ioengine=posixaio, iodepth=1
...
Run status group 0 (all jobs):
  WRITE: bw=287MiB/s, iops=73.4k, runt=3584msec
$ tc qdisc add dev eth0 root netem loss 20%
$ tc qdisc del dev eth0 root
```

!!! warning "Common errors"
    **`bash: pgrep: command not found`** — Install procps-ng package with `apt-get install procps-ng` or `yum install procps-ng`.
    **`stress-ng: error: cannot allocate 80% of memory (requested 6442450944 bytes)`** — Reduce the percentage or number of workers; system lacks sufficient free memory for the test.
    **`RTNETLINK answers: No such device`** — Verify the network interface name with `ip link show` and replace eth0 with the correct interface (e.g., ens0, wlan0).
```bash
# Test graceful shutdown
systemctl stop nginx
# Expected: requests in flight complete; no connection errors to load balancer

# Test reload without downtime
systemctl reload nginx
# Expected: zero downtime; access logs show no 502/503

# Test dependency failure (block outbound connection to DB port)
iptables -I OUTPUT -p tcp --dport 5432 -j DROP
# Expected: application returns 503 not 500; retries correctly; alerts fire
# Cleanup:
iptables -D OUTPUT -p tcp --dport 5432 -j DROP
```
```markdown
Test:           Storage path failure — multipath failover
Date:           2026-05-06
Environment:    Prod-like (UAT)
Scenario:       Disabled one FC path to array on host web-prod-01
Expected:       Multipath redirects I/O to surviving path; no I/O errors at application layer
Actual:         I/O redirected within 2 seconds; application logs show no errors
RTO observed:   2 seconds (path failover)
Alert fired:    Yes — "Storage path degraded" alert at 00:32
Recovery:       Re-enabled path; multipath rebalanced within 5 seconds
Pass/Fail:      Pass
Notes:          Alert was 45 seconds delayed — investigate alerting lag
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
