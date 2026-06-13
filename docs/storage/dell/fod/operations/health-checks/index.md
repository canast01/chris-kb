---
tags:
  - dell
  - operations
---
# FOD — Health Checks


<div class="kb-summary">
Part of the [Flex on Demand](../../index.md) reference.
</div>
```text
┌────────────────────────────────────── Dell FoD — Health Checks ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         FoD health checks: routine verification of operational status and performance         │   │
│   │         Checks include: controller status, drive health, replication lag, and capacity        │   │
│   │         Frequency: daily quick checks; weekly detailed review; monthly capacity report        │   │
│   │        Configure threshold-based alerts for proactive incident prevention and awareness       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check status → review alerts → verify replication → capacity → log                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │         License type        │  │        Permanent/Term       │  │       Feature-specific      │   │
│   │          Activation         │  │         Key → array         │  │        Instant unlock       │   │
│   │            Scope            │  │         Per-array SN        │  │       Non-transferable      │   │
│   │           Features          │  │       Replication/Tier      │  │       Product-defined       │   │
│   │            Audit            │  │        License report       │  │          Compliance         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Check area    │  How to verify   │   Pass criteria   │    Frequency     │       Tool       │   │
│   │   Controllers    │   show status    │    All healthy    │      Daily       │     CLI/GUI      │   │
│   │      Drives      │   show drives    │  No failed/pred.  │      Daily       │     CLI/GUI      │   │
│   │   Replication    │ show replication │  Lag < threshold  │      Daily       │     CLI/GUI      │   │
│   │     Capacity     │  show capacity   │     < 80% used    │      Daily       │     CLI/GUI      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell array with FoD-capable firmware · Dell licensing portal · array management          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FoD                = Feature on Demand; software capabilities locked in firmware, unlocked by li...│
│    License key        = alphanumeric string generated at purchase; applied via GUI, CLI, or REST API  │
│    Permanent license  = perpetual feature unlock; tied to specific array serial number                │
│    Term license       = time-limited feature unlock; expires unless renewed through Dell portal       │
│    Entitlement        = purchased right to use a feature; tracked in Dell software licensing portal   │
│    License transfer   = FoD licenses are non-transferable between different array serial numbers      │
│    Replication FoD    = unlocks synchronous or asynchronous array replication features                │
│    Tier FoD           = unlocks FAST VP or cloud tiering between performance and capacity tiers       │
│    License audit      = periodic reconciliation of active features versus licensed entitlements       │
│    LicenseManager     = Dell tool for bulk license management across multiple array systems           │
│    Array serial       = unique array identifier; FoD licenses are cryptographically bound to it       │
│    FoD portal         = licensing.dell.com; purchase, download, and track all FoD license keys        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Enabled features:** `symcfg -sid <sid> list -fod` — review all enabled FOD features
2. **Feature licence expiry:** check FOD licence expiry dates — flag any expiring in <90 days
3. **Feature utilisation:** verify FOD-enabled features are actually in use (to justify renewal)
4. **Licence compliance:** confirm number of licensed features does not exceed entitlement
5. **Renew pending:** check for FOD features with upcoming renewal dates in Unisphere
6. **Audit log:** review FOD activation/deactivation log for unauthorised changes

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Check if FOD burst is currently active on any array | | burst should only be active if a planned workload increase justified it |
| [ ] Review what percentage of the burst ceiling is consumed | | flag if above 80% of the burst allowance |
| [ ] Confirm whether the current month's consumption report is available | | |
| [ ] Check that base capacity allocation has not changed unexpectedly | | |

## Health Check Commands

```bash
# Authenticate to Unisphere REST API
TOKEN=$(curl -s -k -X POST \
  "https://<unisphere_ip>:8443/univmax/restapi/version/system/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"<user>","password":"<password>"}' | jq -r '.token')

# Get FOD/flex capacity status for the array
curl -s -k \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://<unisphere_ip>:8443/univmax/restapi/100/sloprovisioning/symmetrix/<sid>" | \
  jq '{sid: .symmetrixId, total_usable_cap_gb: .total_usable_cap_gb, total_subscribed_cap_gb: .total_subscribed_cap_gb}'

# Get SRP details to review burst and allocated capacity
curl -s -k \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://<unisphere_ip>:8443/univmax/restapi/100/sloprovisioning/symmetrix/<sid>/srp/<srp_id>" | \
  jq '{srp: .srpId, reserved_cap_percent: .reserved_cap_percent, total_usable_cap_gb: .srp_capacity.usable_total_tb}'
```

## Change Readiness

- [ ] Estimate expected capacity growth from the planned workload increase (in TB)
- [ ] Confirm the FOD burst ceiling is sufficient to cover the planned increase without being exceeded
- [ ] If the planned increase is expected to be sustained (not a temporary burst), notify the Dell account team to discuss adjusting the base contracted capacity
- [ ] Confirm the billing implications are understood — sustained burst usage is charged at the burst rate
- [ ] Document the current base and burst consumption figures before the workload change

## Post-Change Validation

- [ ] FOD burst consumption returns to the pre-change baseline after any temporary workload increase
- [ ] Burst is not active where it was not expected to be
- [ ] Monthly consumption report updated to reflect any intentional capacity changes
- [ ] Dell account team notified if sustained capacity increase is expected to exceed the contracted base
- [ ] Capacity planning records updated with new baseline figures
