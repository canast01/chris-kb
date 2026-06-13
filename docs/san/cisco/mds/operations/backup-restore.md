---
tags:
  - operations
  - san
---
# Cisco MDS 9000 — Backup and Restore

```bash
# Save running to startup config
copy running-config startup-config

# Copy running config off-switch via SCP
copy running-config scp://<user>@<server>/<path>/<filename>

# Copy running config off-switch via TFTP
copy running-config tftp://<server>/<filename>

# Display full running config (for manual capture)
show running-config
```
```text
┌───────────────────────────────── Cisco MDS 9000 — Backup and Restore ─────────────────────────────────┐
│                                                                                                       │
│  MDS backup: running-config, zone set, startup-config to SCP/TFTP; restore sequence.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Configuration Backup             │  │             Zone Database Backup            │   │
│   │          copy run scp://server/path          │  │            show zone status VSAN            │   │
│   │          copy startup scp://server           │  │          copy run scp: zone backup          │   │
│   │          DCNM: archive config auto           │  │          Zone set export: text file         │   │
│   │          Schedule: nightly via DCNM          │  │          Pre-change snapshot always         │   │
│   │          Retention: 30 days minimum          │  │            CFS: verify zone sync            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Config backup and zone snapshot before every change; DCNM automates nightly.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Config Restore Procedure           │  │            Zone Restore Procedure           │   │
│   │         1. copy scp: startup-config          │  │          1. Enter zone config mode          │   │
│   │           2. reload: apply startup           │  │           2. Import zone set file           │   │
│   │           3. Verify: show run diff           │  │           3. zoneset activate VSAN          │   │
│   │         4. Check: show interface fc          │  │         4. Verify: show zone active         │   │
│   │           5. Test: host I/O access           │  │           5. CFS commit: propagate          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS switch chassis · management Ethernet · SCP/TFTP backup server                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  copy run scp    = NX-OS; copies running config to SCP destination server                             │
│  startup-config  = config loaded on boot; always save running to startup                              │
│  copy run start  = NX-OS; saves running config to startup; required after change                      │
│  DCNM archive    = DCNM automatically archives per-switch config on schedule                          │
│  Zone set export = show zone all export; text file backup of zone database                            │
│  CFS             = Cisco Fabric Services; verify zone sync: show cfs merge status                     │
│  reload          = switch reload; applies startup-config after restore                                │
│  show run diff   = compare restored config to expected baseline                                       │
│  zoneset activate= activates the imported zone set in specified VSAN                                  │
│  show zone active= verify zone members are correct after restore                                      │
│  CFS commit      = CFS zone database push to all fabric switches                                      │
│  Pre-change snap = always capture zone set before making any zone changes                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

- [Mds — Procedures](procedures/)
- [Mds — Health Checks](health-checks/)
- [Mds — Common Issues](../troubleshooting/common-issues/)
