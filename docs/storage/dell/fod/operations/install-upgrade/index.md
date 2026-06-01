# FOD — Install & Upgrade


<div class="kb-summary">
> Part of the [Flex on Demand](../../index.md) reference.
</div>

---

FOD billing is managed by Dell — there is no on-premises software upgrade for the FOD metering system itself. Lifecycle tasks focus on:

| Step | Action |
|---|---|
| 1 | FOD billing is unaffected by firmware upgrades, but confirm CloudIQ telemetry resumes promptly after any maintenance that takes the array offline |
| 2 | After adding physical burst capacity under a FOD agreement, confirm CloudIQ reflects the new total installed capacity |
| 3 | If the array is migrated or replaced, work with Dell to transfer the FOD contract to the new system SID |

## License Key Management

```bash
# --- List all license entitlements (identifies FOD base and burst tiers) ---
symcfg -sid <sid> list -license

# Common FOD-related license feature names:
#   PowerMax FOD Base Capacity      – Committed base TB
#   PowerMax FOD Burst Capacity     – Burst ceiling TB
#   VMAX3 Flex on Demand Base       – Legacy VMAX3 FOD base

# --- Import an updated license file ---
symlmf -sid <sid> import -file /tmp/new_fod_license.dat

# Verify the import updated the licensed capacity
symcfg -sid <sid> list -license
```
