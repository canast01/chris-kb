---
tags:
  - servicenow
---
# Inventory — Hardware Lifecycle

```bash
# Dell — check and update firmware via iDRAC
racadm getversion                        # current firmware versions
racadm fwupdate -g -u -a <tftp-server>  # update all components

# HPE iLO — firmware inventory
hponcfg -f get_fw_version.xml

# Check vendor EoS dates
# Dell: https://www.dell.com/support/lifecycle/
# HPE: https://support.hpe.com/hpesc/public/home

# Linux — check BIOS version
dmidecode -t bios | grep -E "Version|Release Date"

# Check if fwupd supports the device
fwupdmgr get-devices
fwupdmgr refresh && fwupdmgr update  # update via LVFS
```


```text title="Expected output"
Dell iDRAC Firmware Information:
Firmware Version: 2.63.60.00
System BIOS: 2.14.2
Baseboard Management Controller: 2.63.60.00
Lifecycle Controller: 2.14.2

HPE iLO Firmware Inventory:
iLO Firmware Version: 2.78
System ROM Version: U32 v2.14 (06/15/2023)

Linux BIOS Information:
	Version: F12
	Release Date: 03/21/2023

Available Devices:
 1. Dell System Update (com.dell.idrac)
    Current version: 2.63.60.00
    Upgradable: Yes
 2. System Firmware (org.uefi.capsule)
    Current version: 2.14.2
    Upgradable: Yes

Refreshing metadata from LVFS...
Successfully refreshed 3 remotes
Updating firmware...
Dell System Update: 2.63.60.00 → 2.64.10.00 [████████████████] 100%
System Firmware: 2.14.2 → 2.15.1 [████████████████] 100%
```

!!! warning "Common errors"
    **`racadm: ERROR: DRAC IP <192.168.1.100> is not reachable`** — Verify iDRAC network connectivity and ensure the IP address is correct with `ping <drac-ip>`.
    **`hponcfg: ERROR: Unable to locate iLO interface`** — Confirm HPE iLO is enabled in BIOS and accessible via the management network interface.
    **`fwupdmgr: No devices found that support firmware updates`** — Install the appropriate firmware plugin package (e.g., `fwupd-plugin-dell` or `fwupd-plugin-hpe`) for your hardware vendor.
```bash
# Secure erase a drive (ATA)
hdparm -I /dev/sda | grep -i "security"  # check if security-erase supported
hdparm --security-set-pass Erase /dev/sda
hdparm --security-erase Erase /dev/sda

# shred overwrite (for drives without ATA secure erase)
shred -vzn 3 /dev/sda  # 3-pass overwrite + verify
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
