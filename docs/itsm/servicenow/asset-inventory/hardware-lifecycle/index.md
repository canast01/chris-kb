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

```bash
# Secure erase a drive (ATA)
hdparm -I /dev/sda | grep -i "security"  # check if security-erase supported
hdparm --security-set-pass Erase /dev/sda
hdparm --security-erase Erase /dev/sda

# shred overwrite (for drives without ATA secure erase)
shred -vzn 3 /dev/sda  # 3-pass overwrite + verify
```
