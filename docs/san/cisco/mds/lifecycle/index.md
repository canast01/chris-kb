# Cisco MDS Lifecycle

> Part of the [Cisco MDS](../) reference.

---
## Version Tracking

NX-OS versions for MDS 9000 are tracked on the Cisco Software Advisor. Version selection is driven by:

- HCL requirements of connected host HBA drivers
- HCL requirements of connected storage array microcode (PowerMax, Pure, NetApp)
- Cisco TAC recommended releases (listed per platform on the software download page)
- End-of-support dates for the current NX-OS train

End-of-sale and end-of-support dates are tracked in the CMDB. Alerts are triggered 18 months before end-of-support to allow adequate planning.

---

## Upgrade Methods

| Method | Applicability | Disruption |
|---|---|---|
| `install all` | All platforms | Reloads the switch — disruptive |
| ISSU | Directors (9706/9710) | Non-disruptive if prerequisites met |
| EPLD upgrade | All platforms | Separate from NX-OS; may require reload |

**ISSU prerequisites (9706/9710):**

- Dual supervisors must be installed and in sync
- Both supervisors must be running the same NX-OS version
- No ongoing configuration sessions
- No in-service diagnostics running
- No ports in error-disabled state on the upgrade path

If ISSU prerequisites are not met, fall back to `install all` in a maintenance window.

---

## Upgrade Procedure (`install all`)

**Pre-upgrade checklist:**

- [ ] Current NX-OS version noted: `show version`
- [ ] Running config saved: `copy running-config startup-config`
- [ ] Config backed up off-switch via SCP
- [ ] HCL compatibility confirmed for target NX-OS version
- [ ] EPLD upgrade required? Check Cisco release notes for the target version
- [ ] Maintenance window booked — `install all` reloads the switch
- [ ] Dual-fabric confirmed — the other fabric will carry all I/O during the reload

**Upgrade steps:**

```
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

---

## EPLD Upgrade

EPLD (FPGA firmware) upgrades are required for some major NX-OS version transitions and for hardware compatibility.

```
# Check current EPLD versions
show version module all  # includes module EPLD version

# Upgrade EPLD (requires switch reload)
upgrade epld bootflash:<epld-image>.img module all
```

EPLD upgrades are always disruptive — they require a module reload or full switch reload depending on the platform.

---

## Adding a New Switch to the Fabric

When adding a new MDS switch to an existing fabric:

1. Configure the new switch with a unique domain ID before connecting ISLs.
2. Pre-configure NTP, AAA (TACACS+/RADIUS), SNMP, and syslog from the baseline template.
3. Connect the ISL — the new switch will join the fabric.
4. Verify the new switch appears in `show topology`:

```
show topology
show fcdomain domain-list vsan 10
```

5. Configure VSANs on the ISL trunk port to allow only the required VSANs.
6. Update CMDB and SAN design register with the new switch domain ID and port allocation.

---

## Decommission Procedure

When removing a switch from the fabric:

```
# Step 1 — Move all host and storage ports to other switches
# Step 2 — Disable the ISL port-channels to isolate the switch from the fabric
interface port-channel1
  shutdown

# Step 3 — Confirm no devices are still logged in
show flogi database

# Step 4 — Physically remove the switch
# Step 5 — Update CMDB and domain ID register
```
