# COD — Health Checks

```
┌─────────────────────────────────────── Dell COD Health Checks ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Monthly COD health check: verify remaining unlocked capacity, plan next activation      │   │
│   │                Alert when COD remaining < 20%; track activation history in CMDB               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                What to Check                 │  │                Pass Criteria                │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           COD remaining per array            │  │       > 20% of purchased COD available      │   │
│   │               License validity               │  │        All licenses valid, no expiry        │   │
│   │                CMDB currency                 │  │       CMDB matches array license state      │   │
│   │               Key store entry                │  │           All keys stored in vault          │   │
│   │              Growth projection               │  │      > 90 days runway with current COD      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │      Check       │    Frequency     │        Tool       │ Alert threshold  │      Action      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │  COD remaining   │     Monthly      │     CMDB/array    │      < 20%       │  Order more COD  │   │
│   │   Growth rate    │     Monthly      │      CloudIQ      │    < 90 days     │   Activate COD   │   │
│   │  License valid   │    Quarterly     │     Array GUI     │   Any invalid    │   Re-issue key   │   │
│   │    CMDB sync     │     Monthly      │       Manual      │     Mismatch     │   Update CMDB    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    COD remaining = Total COD purchased minus COD already activated; stored in CMDB                    │
│    Growth rate   = Monthly capacity consumption rate; used to project activation trigger date         │
│    90-day runway = If current rate consumes remaining COD in < 90 days, activate more now             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [COD](../../index.md) reference.

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Review current COD utilization vs licensed capacity using SYMCLI or Unisphere | `symcfg -sid <sid> show -capacity -gb` | confirm no unexpected consumption increase |
| [ ] Confirm no new COD activations have occurred without an associated change ticket | `symaudit -sid <sid> list -action "license"` | |
| [ ] Check system capacity headroom | `symcfg -sid <sid> list -srp -detail` | flag if utilized capacity exceeds 80% of licensed capacity |
| [ ] Verify Unisphere connectivity to Dell (required for COD activation) | | |

## Health Check Commands

```bash
# Show current array capacity state including licensed vs consumed
symcfg -sid <sid> show -capacity -gb

# Show COD license entitlement and activation status
symlmf -sid <sid> list

# Show storage resource pool (SRP) utilization — confirms physical capacity consumed
symcfg -sid <sid> list -srp -detail

# Show total raw, subscribed, and usable capacity
symcfg -sid <sid> show -tb

# Check if COD capacity pools are available and their current state
symcfg -sid <sid> list -demand -demand_type cod
```

## Change Readiness

- [ ] Current utilization has been reviewed and is approaching the threshold requiring COD activation (typically >80% of licensed capacity)
- [ ] A change ticket has been raised and approved before initiating the COD activation request
- [ ] Unisphere has confirmed connectivity to Dell's licensing backend (check Unisphere > Settings > License)
- [ ] The Dell account team or support portal has been engaged if the activation requires a new entitlement rather than an existing COD pool
- [ ] Post-activation capacity headroom has been calculated to confirm the activation resolves the constraint

| Item | Status | Notes |
|---|---|---|
| Current utilization reviewed and at threshold | | |
| Change ticket raised and approved | | |
| Unisphere connectivity to Dell confirmed | | |
| Dell account/support engaged if new entitlement needed | | |
| Post-activation headroom calculated | | |

## Post-Change Validation

- [ ] New capacity is visible in `symcfg -sid <sid> show -capacity -gb` output
- [ ] Licensed capacity now reflects the activated COD amount in `symlmf -sid <sid> list`
- [ ] SRP utilization percentage has dropped to reflect the additional capacity
- [ ] No performance or availability impact to existing workloads (check I/O stats in Unisphere)
- [ ] CloudIQ health score for the array is unchanged or improved
- [ ] Change ticket updated and closed with post-activation capacity figures
