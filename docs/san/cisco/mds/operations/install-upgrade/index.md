# MDS — Install & Upgrade


<div class="kb-summary">
> Part of the [Cisco MDS](../../index.md) reference.
</div>

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
```text
┌──────────────────────────────── Cisco MDS 9000 — Install and Upgrade ─────────────────────────────────┐
│                                                                                                       │
│  MDS initial setup: rack, cable, NX-OS boot, initial config; ISSU upgrade procedure.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Initial Setup                 │  │         NX-OS Initial Configuration         │   │
│   │           1. Rack and cable switch           │  │          1. Set hostname + IP mgmt          │   │
│   │          2. Console: 9600 baud 8N1           │  │           2. Configure NTP servers          │   │
│   │          3. Power on: boot sequence          │  │            3. Set admin password            │   │
│   │           4. Initial config wizard           │  │           4. Configure TACACS+ ISE          │   │
│   │          5. Set management IP + SSH          │  │            5. Add to DCNM fabric            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Console access required for initial setup; TACACS+ and NTP before adding to fabric.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            ISSU Upgrade Procedure            │  │           Post-Upgrade Validation           │   │
│   │         1. Backup config + zone set          │  │          1. show version: new NX-OS         │   │
│   │          2. Copy NX-OS to bootflash          │  │          2. show system health: OK          │   │
│   │          3. show install all impact          │  │         3. show interface: no errors        │   │
│   │         4. install all nxos <image>          │  │          4. Host I/O: verify access         │   │
│   │           5. copy run start after            │  │           5. DCNM: verify version           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS director chassis · console cable · management Ethernet · SFP transceivers                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ISSU            = In-Service Software Upgrade; NX-OS upgrade without traffic drop                    │
│  show install all impact= previews ISSU upgrade impact; shows module reloads                          │
│  install all     = ISSU trigger; upgrades standby supervisor first then failover                      │
│  bootflash       = switch internal flash storage; holds NX-OS images                                  │
│  copy run start  = saves running config to startup; required after every change                       │
│  Console         = serial connection; 9600 baud 8N1; required for initial setup                       │
│  Initial config wizard= first-boot setup; sets admin password and IP                                  │
│  TACACS+         = configure before adding to fabric; ISE must be reachable                           │
│  NTP             = configure before DCNM discovery; event timestamps must sync                        │
│  DCNM            = add switch to DCNM after SSH is configured; enables zone mgmt                      │
│  show version    = verify NX-OS version after ISSU upgrade completes                                  │
│  show system health= post-upgrade health check; all modules should be online                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

5. Configure VSANs on the ISL trunk port to allow only the required VSANs.
6. Update CMDB and SAN design register with the new switch domain ID and port allocation.

---

## Decommission Procedure

When removing a switch from the fabric:

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
