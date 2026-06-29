---
tags:
  - dell
  - operations
---
# FOD — Install & Upgrade

<div class="kb-summary">
Dell FoD install and upgrade: SCG registration for automatic telemetry, FoD licence activation procedure, and upgrade path for capacity tier changes.

*Applies to: Dell FOD*
</div>
![FOD — Install & Upgrade](../../../../assets/storage-dell-fod-operations-install-upgrade.svg)

---

FOD billing is managed by Dell — there is no on-premises software upgrade for the FOD metering system itself. Lifecycle tasks focus on:

| Step | Action |
|---|---|
| 1 | FOD billing is unaffected by firmware upgrades, but confirm CloudIQ telemetry resumes promptly after any maintenance that takes the array offline |
| 2 | After adding physical burst capacity under a FOD agreement, confirm CloudIQ reflects the new total installed capacity |
| 3 | If the array is migrated or replaced, work with Dell to transfer the FOD contract to the new system SID |

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

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


```text title="Expected output"
Symmetrix ID: 000297123456789

License Information:
Feature Name                          Capacity    Expiration Date
PowerMax FOD Base Capacity            50.00 TB    2025-12-31
PowerMax FOD Burst Capacity           25.00 TB    2025-12-31
VMAX3 Flex on Demand Base             0.00 TB     Expired

License file /tmp/new_fod_license.dat imported successfully.
Import timestamp: 2024-01-15 14:32:47 UTC
License ID: LIC-4A9F2E8B1C7D5F3A

Symmetrix ID: 000297123456789

License Information:
Feature Name                          Capacity    Expiration Date
PowerMax FOD Base Capacity            75.00 TB    2026-12-31
PowerMax FOD Burst Capacity           40.00 TB    2026-12-31
VMAX3 Flex on Demand Base             0.00 TB     Expired
```

!!! warning "Common errors"
    **`symcfg: Cannot open Symmetrix <sid>`** — Verify the SID is correct and the array is reachable via `symcfg -sid <sid> list -director`.
    **`symlmf: License file format invalid or corrupted`** — Ensure the license file is not truncated and was obtained directly from Dell EMC licensing portal.
    **`symlmf: Permission denied on /tmp/new_fod_license.dat`** — Run the import command with appropriate privileges (sudo) or move the file to a readable location.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Fod — Procedures](../procedures/)
- [Fod — Health Checks](../health-checks/)
