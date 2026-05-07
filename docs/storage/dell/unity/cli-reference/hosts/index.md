# Hosts & Access

> Part of the Dell Unity CLI Reference (Unisphere CLI).
## Hosts

Hosts represent servers that access Unity storage. Each host has associated initiators (WWNs or IQNs).

```bash
# List all hosts
uemcli -d <ip> -u admin /remote/host show

# Detailed host view — name, OS type, initiators, LUN access
uemcli -d <ip> -u admin /remote/host show -detail

# Specific host
uemcli -d <ip> -u admin /remote/host -id <host_id> show -detail

# Create a host
uemcli -d <ip> -u admin /remote/host create \
    -name <hostname> \
    -type Initiator \
    -osType Linux
```

## Host OS Types

| OS Type | Value |
|---|---|
| Linux | `Linux` |
| Windows | `Windows` |
| VMware | `VMware` |
| AIX | `AIX` |
| HP-UX | `HPUX` |

## Initiators

Each HBA port or iSCSI IQN is a separate initiator:

```bash
# List all initiators
uemcli -d <ip> -u admin /remote/initiator show

# Initiator detail — WWN/IQN, health, host association
uemcli -d <ip> -u admin /remote/initiator show -detail

# Register a Fibre Channel initiator (WWN)
uemcli -d <ip> -u admin /remote/initiator create \
    -host <host_id> \
    -uid 20:00:00:90:fa:12:34:56 \
    -type FC

# Register an iSCSI initiator (IQN)
uemcli -d <ip> -u admin /remote/initiator create \
    -host <host_id> \
    -uid iqn.2024-01.com.example:host01 \
    -type iSCSI

# Delete an initiator
uemcli -d <ip> -u admin /remote/initiator -id <initiator_id> delete
```

## LUN Access Control (Host Access)

LUN access grants a host access to a LUN:

```bash
# List all LUN access control entries
uemcli -d <ip> -u admin /stor/config/lunacl show

# Access for a specific LUN
uemcli -d <ip> -u admin /stor/config/lunacl show | grep <lun_id>

# Grant a host access to a LUN
uemcli -d <ip> -u admin /stor/config/lunacl create \
    -lun <lun_id> \
    -host <host_id>

# With specific access type (production = read-write)
uemcli -d <ip> -u admin /stor/config/lunacl create \
    -lun <lun_id> \
    -host <host_id> \
    -accessType production

# Revoke LUN access
uemcli -d <ip> -u admin /stor/config/lunacl -id <acl_id> delete
```

## End-to-End LUN Presentation

```bash
# Step 1 — create or identify host
uemcli -d <ip> -u admin /remote/host create -name server01 -type Initiator -osType Linux

# Step 2 — register initiators
uemcli -d <ip> -u admin /remote/initiator create -host <host_id> -uid <wwn> -type FC

# Step 3 — grant LUN access
uemcli -d <ip> -u admin /stor/config/lunacl create -lun <lun_id> -host <host_id>

# Step 4 — on the host, rescan HBAs and confirm device appears
# Linux: rescan-scsi-bus.sh or echo "- - -" > /sys/class/scsi_host/host*/scan
```
