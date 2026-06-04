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
```text
┌──────────────────────────────────── Performance — Failure Testing ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Failure testing: deliberately inject faults to verify HA and DR actually work         │   │
│   │      Test in isolation first; graduate to production with maintenance window and rollback     │   │
│   │            Document hypothesis, expected result, actual result, and any gaps found            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Test Types                  │  │                   Process                   │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │        Node/host failure (power off)         │  │              Define hypothesis              │   │
│   │            Network partition test            │  │             Raise change ticket             │   │
│   │             Storage path failure             │  │                 Inject fault                │   │
│   │             Service kill / crash             │  │              Measure RTO actual             │   │
│   │             Resource exhaustion              │  │             Document gaps found             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Chaos engineering= Deliberate fault injection to reveal weaknesses before they cause incidents     │
│    Game day       = Scheduled failure testing exercise; all stakeholders notified; results shared     │
│    Blast radius   = Scope of failure; limit during tests by isolating to one component                │
│    Steady state   = Known-good performance baseline before fault injection begins                     │
│    Rollback       = Restore normal state after test; documented before injection starts               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
