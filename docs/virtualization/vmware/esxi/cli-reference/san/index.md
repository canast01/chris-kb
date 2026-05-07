# SAN Connectivity (iSCSI / FC)

> Part of the [VMware ESXi CLI Reference](../).
## Fibre Channel

```bash
# List HBAs and WWPNs
esxcli storage san fc list

# FC HBA stats (errors, logins)
esxcli storage san fc stats get -A vmhba0
esxcli storage san fc stats get -A vmhba1

# FC device paths
esxcli storage nmp device list | grep vmhba

# Path status to all LUNs
esxcli storage nmp path list

# Paths to a specific device
esxcli storage nmp path list -d <naa.xxx>

# Dead paths
esxcli storage core path list | grep "dead\|Dead"
```

## iSCSI

```bash
# List iSCSI adapters
esxcli iscsi adapter list

# iSCSI adapter details (IQN, status)
esxcli iscsi adapter get -A vmhba64

# List discovery targets
esxcli iscsi adapter discovery sendtarget list -A vmhba64

# Add a send-target (static discovery)
esxcli iscsi adapter discovery sendtarget add \
    --address <iscsi_target_ip>:3260 -A vmhba64

# Remove a send-target
esxcli iscsi adapter discovery sendtarget remove \
    --address <iscsi_target_ip>:3260 -A vmhba64

# List active iSCSI sessions
esxcli iscsi session list

# iSCSI network portals (bound VMkernel adapters)
esxcli iscsi logicalnetworkportal list -A vmhba64
```

## Storage Paths and Multipathing

```bash
# List all LUN paths with state
esxcli storage core path list

# NMP (Native Multipath Plugin) device list
esxcli storage nmp device list

# PSP (Path Selection Policy) per device
esxcli storage nmp device list | grep -E "Device:|PSP:"

# Set PSP for a device (e.g., Round Robin for PowerMax)
esxcli storage nmp device set -d <naa.xxx> -P VMW_PSP_RR

# Force rescan of all adapters
esxcli storage core adapter rescan --all

# Rescan a specific adapter
esxcli storage core adapter rescan -A vmhba0
```

## LUN and Device Info

```bash
# List all storage devices
esxcli storage core device list

# Device details (vendor, model, size, queue depth)
esxcli storage core device list -d <naa.xxx>

# VAAI (XCOPY/ATS) support on a device
esxcli storage core device vaai status get -d <naa.xxx>

# Queue depth per device
esxcli storage core device list | grep "Queue Full Threshold"

# Set queue depth for a device
esxcli storage core device set --device <naa.xxx> -O MaxQueueDepth=64
```

## Troubleshooting

```bash
# Check for APD (All Paths Down) or PDL (Permanent Device Loss)
grep -i "APD\|PDL\|lost path" /var/log/vmkernel.log | tail -20

# Dead path detail
esxcli storage core path list | grep -A 5 "State: dead"

# Rescan and verify paths recovered
esxcli storage core adapter rescan --all
esxcli storage core path list | grep -c "State: active"
```
