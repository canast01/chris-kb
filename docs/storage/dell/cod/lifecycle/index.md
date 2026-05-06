# COD — Lifecycle

## Entitlement Lifecycle

COD entitlements are tracked in the Dell License Management Portal and are tied to a specific PowerMax frame serial number (SID). The lifecycle of a COD entitlement follows this path:

```
Purchase order confirmed
        │
        ▼
Dell issues license key → available in Dell License Management Portal
        │
        ▼
License key applied to array via SYMCLI or Unisphere
        │
        ▼
Capacity active — in use by thin pools and storage groups
        │
        ▼
Frame upgrade or replacement?
        │
        ├── YES → Entitlement transfer to new frame SID (work with Dell account team)
        └── NO  → Entitlement remains active until frame decommission
```

## COD and PowerMax Frame Upgrades

When a PowerMax frame is upgraded (e.g., PowerMax 2000 → PowerMax 8000), COD entitlements are transferred to the new frame's SID. This is not automatic — it requires a formal request to Dell:

1. Raise a request via Dell Support or the account team to transfer entitlements
2. Provide old and new frame serial numbers
3. Dell issues new license files tied to the new SID
4. Apply new license files to the replacement frame
5. Retire the old license files — they are no longer valid

**Never apply a license file to a different SID than it was issued for** — it will fail and may trigger a support case.

## Reviewing COD Entitlement

```bash
# List all license entitlements for an array
symlicense -sid <SID> list

# Show detail for COD-specific licenses
symlicense -sid <SID> show -feature COD

# Compare installed vs licensed capacity
symcfg -sid <SID> list -capacity
symcfg -sid <SID> show -detail
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
