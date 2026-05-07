# FLOGI & Name Server

> Part of the Cisco MDS NX-OS CLI Reference.
## FLOGI Database

```bash
# All logged-in initiators and targets
show flogi database

# Filter to a specific VSAN
show flogi database vsan <id>

# Confirm a specific WWN is logged in
show flogi database | grep <wwn>
```

FLOGI (Fabric Login) shows every device that has registered with the fabric. If a host HBA or storage target port is missing here, it has not successfully logged into the fabric.

## FC Name Server

```bash
# All registered devices in the fabric
show fcns database
show fcns database vsan <id>
show fcns database detail         # includes port type, symbolic name

# Name server statistics
show fcns statistics

# Look up a specific WWN
show fcns database | grep <wwn>
```

## Interpreting FLOGI Output

| Field | Meaning |
|---|---|
| Interface | Which MDS port the device logged into |
| VSAN | VSAN the device is in |
| FCID | Fabric-assigned address (N_Port ID) |
| Port Name (PWWN) | Port WWN of the device |
| Node Name (NWWN) | Node WWN of the device |

## Verifying Host-to-Storage Visibility

```bash
# Find the host HBA WWN in FLOGI
show flogi database | grep <host_wwn>

# Confirm storage port is in the name server
show fcns database | grep <storage_wwn>

# Confirm both are in the same VSAN
show vsan membership
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Host WWN not in FLOGI | HBA link, VSAN membership | Check port state; verify VSAN assignment |
| Storage target not visible | FLOGI and FCNS | Check array port and zoning |
| FCID missing | FLOGI failed | Check port state, VSAN config |
| Duplicate FCID | Fabric merge conflict | Investigate VSAN merges |
