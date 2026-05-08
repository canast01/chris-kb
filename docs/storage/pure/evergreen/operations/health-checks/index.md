# Evergreen — Health Checks

> Part of the [Evergreen Operations](../) reference.

---

> This page is a stub. Health check procedures for Evergreen FlashArray will be documented here.

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Apply standard FlashArray daily checks | `purealert list` | Evergreen is a subscription model; the underlying FlashArray or FlashBlade operations apply |
| [ ] Run `purearray list --hardware` | `purearray list --hardware` | confirm all hardware components are healthy |
| [ ] Run `purepod list` | `purepod list` | confirm ActiveCluster pods are stretched and replicating (if configured) |
| [ ] Verify subscription status is current in the Pure1 portal | | |
| [ ] Confirm Pure1 phone-home (support tunnel) is active | | Pure Support visibility depends on continuous telemetry |
| [ ] Check Pure Support contract status | | confirm support is active and the renewal date is tracked |
| [ ] Review Pure1 for any proactive recommendations or upgrade eligibility | | |

## Health Check

- [ ] No active hardware alerts in Pure1 or from `purealert list`
- [ ] All drives healthy: `puredrive list` — no `failed` or `recovering` drives
- [ ] Both controllers online and running the same Purity version: `purearray list --controller`
- [ ] ActiveCluster pods are stretched and `replicating: true`: `purepod list --replicating`
- [ ] Pure1 phone-home is active (Pure1 portal: Arrays → select array → Support → Phone Home)
- [ ] Purity software version is within Pure's supported N-2 release window
- [ ] Subscription expiry date is documented and renewal is tracked with sufficient lead time

```bash
# List array hardware status — controllers, chassis, power, fans
purearray list --hardware

# Review all active alerts
purealert list

# Array capacity, used space, and data reduction
purearray list --space

# Verify host and host group path status
purehost list
purehgroup list

# Review ActiveCluster pod and replication status
purepod list
purepod list --replicating
purepod list --failover-preference

# Check current Purity software version
purearray list

# List snapshot usage (to monitor ahead of controller upgrade)
puresnap list --space
```
