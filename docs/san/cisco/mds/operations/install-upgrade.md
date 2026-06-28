---
tags:
  - operations
  - san
---
# Cisco MDS 9000 — Install and Upgrade
![Cisco MDS 9000 — Install and Upgrade](../../../../assets/san-cisco-mds-operations-install-upgrade.svg)

```bash
# Step 1 — Copy the target NX-OS image to the switch bootflash
copy scp://<server>/<path>/nxos.bin bootflash:

# Step 2 — Verify the image MD5 checksum
show file bootflash:nxos.bin md5sum

# Step 3 — Run the install all pre-check (non-disruptive)
install all nxos bootflash:nxos.bin

# Review the pre-check output — confirm no blocking issues

# Step 4 — Confirm and proceed (switch will reload)
# The install all command prompts for confirmation before rebooting

# Step 5 — After reload, verify
show version
show interface brief   # all ports up
show vsan             # all VSANs active
show zoneset active   # zoning intact
```

```bash
# Step 1 — Move all host and storage ports to other switches
# Step 2 — Disable the ISL port-channels to isolate the switch from the fabric
interface port-channel1
  shutdown

# Step 3 — Confirm no devices are still logged in
show flogi database

# Step 4 — Physically remove the switch
# Step 5 — Update CMDB and domain ID register
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Mds — Procedures](../procedures/)
- [Mds — Health Checks](../health-checks/)
- [Mds — Deploy](../../deploy/)
