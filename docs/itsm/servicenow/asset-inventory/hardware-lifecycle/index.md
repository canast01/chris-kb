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
```text
┌─────────────────────────────────── Inventory — Hardware Lifecycle ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Track hardware from purchase through active use to end-of-life and decommission        │   │
│   │       EOL: no more patches; EOSL: no more support calls — both require replacement plan       │   │
│   │        Refresh: budget cycle (18-24 months lead); decommission: secure wipe + disposal        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Lifecycle Phases               │  │             EOL/Refresh Actions             │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │             Plan: spec + budget              │  │            Query vendor EOL dates           │   │
│   │            Procure: PO + delivery            │  │            Flag 18-month warning            │   │
│   │            Deploy: rack + config             │  │            Raise refresh project            │   │
│   │          Operate: maintain + patch           │  │           Migrate workloads first           │   │
│   │         Decommission: wipe + retire          │  │           Secure wipe certificate           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    EOL      = End of Life; vendor stops selling and developing the product                            │
│    EOSL     = End of Service Life; vendor stops providing support and security patches                │
│    Refresh  = Replace ageing hardware with current generation before EOSL                             │
│    Secure wipe= Cryptographic erasure or DoD overwrite before disposal to prevent data recovery       │
│    ITAD     = IT Asset Disposition; certified disposal with chain-of-custody and destruction cert     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Secure erase a drive (ATA)
hdparm -I /dev/sda | grep -i "security"  # check if security-erase supported
hdparm --security-set-pass Erase /dev/sda
hdparm --security-erase Erase /dev/sda

# shred overwrite (for drives without ATA secure erase)
shred -vzn 3 /dev/sda  # 3-pass overwrite + verify
```
