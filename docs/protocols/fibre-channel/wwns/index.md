# WWNs — World Wide Names

A World Wide Name (WWN) is a 64-bit globally unique identifier assigned to every Fibre Channel device.

```text
        WWNN vs WWPN STRUCTURE
┌──────────────────────────────────────────────────────────────┐
│  HBA Card (Node)                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  WWNN (Node Name) — identifies the HBA card itself   │   │
│  │  50:00:d3:10:00:5e:c8:00  ◄── 8-byte hex, one per card│  │
│  │                                                       │   │
│  │  ┌─────────────────┐  ┌─────────────────┐            │   │
│  │  │  Port 0 (WWPN)  │  │  Port 1 (WWPN)  │            │   │
│  │  │50:00:d3:10:00:  │  │50:00:d3:10:00:  │            │   │
│  │  │   5e:c8:a1      │  │   5e:c8:a2      │            │   │
│  │  │  ► used for     │  │  ► used for     │            │   │
│  │  │    zoning &     │  │    zoning &     │            │   │
│  │  │    masking      │  │    masking      │            │   │
│  │  └─────────────────┘  └─────────────────┘            │   │
│  └──────────────────────────────────────────────────────┘   │
│   NAA(5) + OUI + vendor-assigned bits = 64-bit unique ID     │
└──────────────────────────────────────────────────────────────┘
``` WWNs are used for zoning, host masking, and fabric registration.

## WWN Types

| Type | Full Name | Purpose |
|---|---|---|
| **WWPN** | World Wide Port Name | Identifies a specific FC port — used for zoning and LUN masking |
| **WWNN** | World Wide Node Name | Identifies the HBA or array controller — not used for zoning |

WWPNs are what matter operationally. Always zone and mask by WWPN, not WWNN.

## WWN Format

```text
50:00:d3:10:00:5e:c8:a1
│   │         │
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

### Brocade switch (nameserver)

```bash
nsshow          # all logged-in ports on this switch
nsallshow       # nameserver entries across entire fabric
```

### Cisco MDS

```bash
show flogi database          # fabric login table
show fcns database vsan 10   # name server for VSAN 10
```

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
