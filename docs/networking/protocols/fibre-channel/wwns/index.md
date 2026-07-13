---
tags:
  - networking
description: "A World Wide Name (WWN) is a 64-bit globally unique identifier assigned to every Fibre Channel device."
---
# WWNs — World Wide Names

<div class="kb-summary">
A World Wide Name (WWN) is a 64-bit globally unique identifier assigned to every Fibre Channel device.
</div>

        WWNN vs WWPN STRUCTURE

WWNs are used for zoning, host masking, and fabric registration.

## WWN Types

| Type | Full Name | Purpose |
|---|---|---|
| **WWPN** | World Wide Port Name | Identifies a specific FC port — used for zoning and LUN masking |
| **WWNN** | World Wide Node Name | Identifies the HBA or array controller — not used for zoning |

WWPNs are what matter operationally. Always zone and mask by WWPN, not WWNN.

## WWN Format

```text
50:00:d3:10:00:5e:c8:a1
│   │                                                                                                   │
│   OUI       Vendor-assigned portion
└── NAA identifier (5 = IEEE registered)
```

Standard notation is 8 colon-separated hex byte pairs. Some tools display without colons (`5000d310005ec8a1`) — both refer to the same port.

## Finding WWPNs

### Linux (HBA)

```bash
# QLogic
cat /sys/class/fc_host/host*/port_name

# Emulex / Broadcom
systool -c fc_host -v | grep port_name

# General
ls /sys/class/fc_host/
cat /sys/class/fc_host/host0/port_name
cat /sys/class/fc_host/host1/port_name
```


```text title="Expected output"
0x500143800000001a
0x500143800000001b

port_name            = "0x500143800000001a"
port_name            = "0x500143800000001b"

host0  host1  host2
0x500143800000001a
0x500143800000001b
```

!!! warning "Common errors"
    **`cat: /sys/class/fc_host/host0/port_name: No such file or directory`** — Verify the FC HBA is installed and recognized with `lspci | grep -i fibre` before querying sysfs paths.
    **`systool: command not found`** — Install the sysfsutils package with `apt-get install sysfsutils` or `yum install sysfsutils`.
    **`cat: /sys/class/fc_host/host1/port_name: Permission denied`** — Run the command with `sudo` or as root to access sysfs FC host attributes.
### Windows (HBA)

```powershell
# Via Get-InitiatorPort
Get-InitiatorPort | Select-Object NodeAddress, PortAddress, ConnectionType

# QLogic SANsurfer / Emulex OneCommand Manager GUI also display WWPNs
```

### ESXi (vmkernel)

```bash
esxcli storage san fc list
# Shows WWPN, WWNN, speed, and port state for each HBA
```


```text title="Expected output"
HBA Name  WWPN                  WWNN                  Speed  Port State
vmhba0    50:00:14:40:5a:2b:c1:d3  50:00:14:40:5a:2b:c1:d0  16Gb   Online
vmhba1    50:00:14:40:5a:2b:c1:e5  50:00:14:40:5a:2b:c1:e0  16Gb   Online
vmhba2    50:00:14:40:5a:2b:c2:f7  50:00:14:40:5a:2b:c2:f0  8Gb    Online
vmhba3    50:00:14:40:5a:2b:c3:a9  50:00:14:40:5a:2b:c3:a0  4Gb    Offline
vmhba4    50:00:14:40:5a:2b:c4:b2  50:00:14:40:5a:2b:c4:b0  16Gb   Link Failure
```

!!! warning "Common errors"
    **`Could not get HBA information. Error: Unknown command or namespace`** — Verify esxcli is available and you are running this command on an ESXi host with Fibre Channel adapters installed.
    **`Error: The object has already been deleted or has not been completely created`** — Wait 30 seconds for the HBA driver to fully initialize after a recent reboot or adapter insertion.
### Brocade switch (nameserver)

```bash
nsshow          # all logged-in ports on this switch
nsallshow       # nameserver entries across entire fabric
```


```text title="Expected output"
R_A_Port_ID    Logged_In_Ports
0              50:00:09:73:00:1a:2b:4c
1              50:00:09:73:00:1a:2b:4d
2              50:00:09:73:00:1a:2b:4e
3              50:00:09:73:00:1a:2b:4f
4              50:00:09:73:00:1a:2b:50
...

Fabric Port Name Server
Switch_A:1     50:00:09:73:00:1a:2b:4c  storage-array-01
Switch_A:2     50:00:09:73:00:1a:2b:4d  storage-array-02
Switch_B:1     50:00:09:73:00:1a:2b:5c  host-server-01
Switch_B:2     50:00:09:73:00:1a:2b:5d  host-server-02
Switch_C:3     50:00:09:73:00:1a:2b:6e  backup-appliance-01
...
```

!!! warning "Common errors"
    **`nsshow: command not found`** — Verify you are logged into a Fibre Channel switch (Brocade/Cisco) with admin credentials, not a Linux host.
    **`Permission denied`** — Elevate to admin role using `roleshow` and `userconfig` or re-authenticate with appropriate fabric credentials.
### Cisco MDS

```bash
show flogi database          # fabric login table
show fcns database vsan 10   # name server for VSAN 10
```


```text title="Expected output"
FLOGI Database for VSAN 1:
 FCID           PORT NAME               NODE NAME               CLASS
 0x010001       50:00:09:4d:1a:2b:3c:4d 50:00:09:4d:1a:2b:3c:5e   3
 0x010002       50:00:09:4d:1a:2b:3c:4f 50:00:09:4d:1a:2b:3c:60   3
 0x010100       50:00:14:40:5a:6b:7c:8d 50:00:14:40:5a:6b:7c:9e   3

FCNS Database for VSAN 10:
 FCID           TYPE PWWN               NWWN               SYMBOLIC NAME
 0x0a0001       NX   50:00:1b:21:aa:bb:cc:dd 50:00:1b:21:aa:bb:cc:ee storage-array-01
 0x0a0002       NX   50:00:1b:21:aa:bb:cc:ff 50:00:1b:21:aa:bb:cc:11 storage-array-02
 0x0a0100       N    50:00:09:4d:1a:2b:3c:4d 50:00:09:4d:1a:2b:3c:5e hba-host-prod-01
 0x0a0101       N    50:00:09:4d:1a:2b:3c:4f 50:00:09:4d:1a:2b:3c:60 hba-host-prod-02
```

!!! warning "Common errors"
    **`VSAN 10 not found`** — Verify the VSAN exists with `show vsan` and confirm it is active.
    **`% Invalid command`** — Ensure you are in the correct switch CLI mode (some switches require `show fcns database` without the vsan parameter for older firmware versions).
## WWN Standards

- Document all server and storage WWPNs in CMDB at provisioning time
- Use the WWPN, not the WWNN, in all zoning and host group configurations
- Label cables with short WWN identifiers at both ends

## Common Issues

| Symptom | Cause | Action |
|---|---|---|
| WWPN not in fabric nameserver | HBA not logged into fabric (FLOGI failed) | Check link, SFP, speed negotiation |
| Wrong WWPN zoned | WWNN used instead of WWPN | Confirm with `nsshow` — use port_name not node_name |
| WWPN changed after reboot | Virtualised WWN in software HBA (rare) | Check HBA driver settings; prefer burned-in WWN |
