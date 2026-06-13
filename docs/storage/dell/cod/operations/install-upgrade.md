---
tags:
  - dell
  - operations
---
# COD — Lifecycle

<div class="kb-summary">
Lifecycle reference covering Entitlement Lifecycle, COD Entitlement Review Cadence, Frame Decommission — COD Implications, COD vs. Standard Capacity Purchase.

*Applies to: Cloud for Desktop (COD)*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Entitlement Lifecycle

COD entitlements are tracked in the Dell License Management Portal and are tied to a specific PowerMax frame serial number (SID). The lifecycle of a COD entitlement follows this path:

```text
┌───────────────────────────────────── Dell COD Install / Upgrade ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     COD install: order COD with array; verify hardware at delivery; register license keys     │   │
│   │    COD upgrade: purchase additional COD for existing array; apply keys via licensing portal   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      New array with COD:                                      │   │
│   │        1. Verify COD hardware visible in array management (locked drives/nodes listed)        │   │
│   │                2. Log in to Dell Licensing Portal; find array by serial number                │   │
│   │                                3. Download COD license key file                               │   │
│   │                         4. Store key in password vault before applying                        │   │
│   │                       5. Apply via array Settings > Licenses or REST API                      │   │
│   │                          6. Confirm unlocked capacity appears in pool                         │   │
│   │                        7. Update CMDB: total COD, activated, remaining                        │   │
│   │                                                                                               │   │
│   │                                    Upgrading existing COD:                                    │   │
│   │                      1. Purchase additional COD through Dell account team                     │   │
│   │                          2. Dell issues updated key for array serial                          │   │
│   │                      3. Apply new key; previous activations remain active                     │   │
│   │                               4. Update CMDB with new COD total                               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dell Licensing Portal = licensing.dell.com; manage COD/FOD keys per serial number                  │
│    Updated key           = New COD key includes all previous + new units; apply to replace old        │
│    Locked drives visible = Array shows reserved drives in inventory before COD applied                │
│    CMDB update           = Record activation date, TB added, cumulative totals per array              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Cross-reference this output against the Dell License Management Portal to confirm the portal record matches what the array reports. Discrepancies must be resolved with Dell before the next capacity review.

## COD Entitlement Review Cadence

| Review | Frequency | Action |
|---|---|---|
| Inventory reconciliation | Every 6 months | Compare symcli license output to Dell portal and CMDB |
| Growth trend review | Monthly | Check CloudIQ capacity forecast against COD headroom |
| COD procurement planning | Annually (or when within 6 months of exhausting COD headroom) | Engage Dell account team for next COD increment |

## Frame Decommission — COD Implications

When decommissioning a PowerMax array:

1. Migrate all data from the array before decommissioning
2. Remove all storage groups and thin pools
3. Contact the Dell account team to discuss COD entitlement disposition:
   - If replacing with a new frame: transfer entitlements to the new SID
   - If reducing capacity: COD licenses expire with the frame (generally not refundable)
4. Remove the array from Unisphere and Solutions Enabler management
5. Deregister from SCG and Dell Support portal
6. Physical decommission or return to Dell (if on a leased/COD subscription)

## COD vs. Standard Capacity Purchase

Understanding when COD makes more sense than buying standard licensed capacity upfront:

| Scenario | Recommended Approach |
|---|---|
| Growth is predictable and sustained | Purchase standard capacity — lower unit cost |
| Growth is uncertain or seasonal | COD — pay only when activated; avoids stranded spend |
| DR site headroom for failover | COD — DR capacity rarely needed at full scale, but must be available instantly |
| Cloud migration (temporary scale-up) | COD — activate for the migration period; headroom not needed after migration completes |
| Service provider burst capacity | COD — provision tenant capacity rapidly without procurement delays |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
