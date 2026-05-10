# iSCSI Multipathing

iSCSI multipathing uses multiple network paths between initiator and target for redundancy and load distribution. On Linux, DM-Multipath handles this; on Windows, MPIO; on ESXi, NMP with PSP.

## Recommended Network Layout

```
Server NIC0 → Storage VLAN A (10.10.1.x) → Array Port A
Server NIC1 → Storage VLAN B (10.10.2.x) → Array Port B
```

Use separate NICs and separate switches (or VLANs at minimum) for each path. Never share iSCSI with management traffic.

## Linux — DM-Multipath

```bash
# Install
dnf install device-mapper-multipath

# Enable and start
systemctl enable --now multipathd

# View all multipath devices and path state
multipath -ll

# Sample output interpretation:
# mpatha (360000000000000) dm-0 PURE,FlashArray
# size=100G features='0' hwhandler='1 alua' wp=rw
# |-+- policy='service-time 0' prio=50 status=active
# | |- 33:0:0:1  sdb 8:16 active ready running
# | |- 34:0:0:1  sdd 8:48 active ready running
# +-+- policy='service-time 0' prio=10 status=enabled
#   |- 33:0:1:1  sdc 8:32 active ready running
#   |- 34:0:1:1  sde 8:64 active ready running

# Reload path config after changes
multipath -r

# Show multipath topology
multipath -t
```

### /etc/multipath.conf — Key Settings

```conf
defaults {
    find_multipaths  yes
    user_friendly_names yes
}

blacklist {
    devnode "^(ram|raw|loop|fd|md|dm-|sr|scd|st)[0-9]*"
    devnode "^hd[a-z]"
    devnode "^sda$"   # local OS disk — always blacklist
}
```

Most major arrays (Pure, NetApp, Dell) have well-known hardware handlers — use vendor-recommended multipath.conf from their support portal.

## Windows — MPIO

```powershell
# Install MPIO feature
Install-WindowsFeature -Name Multipath-IO

# Add iSCSI device support to MPIO
New-MSDSMSupportedHW -VendorId PURE -ProductId FlashArray

# View MPIO paths
Get-MpioDisk
Get-MpioAvailableDriveLetters

# Set load balance policy
Set-MSDSMGlobalDefaultLoadBalancePolicy -Policy RR   # Round Robin
```

## VMware ESXi — NMP

```bash
# Show PSP (path selection policy) per datastore
esxcli storage nmp device list

# Change PSP for a device
esxcli storage nmp device set \
  -d naa.<id> \
  --psp VMW_PSP_RR

# View active paths
esxcli storage core path list -d naa.<id>

# Set Round Robin I/O operations limit (default 1000)
esxcli storage nmp psp roundrobin deviceconfig set \
  -d naa.<id> --type iops --iops 1
```

## Load Balance Policies

| Policy | Linux | Windows | ESXi | Best for |
|---|---|---|---|---|
| Round Robin | `round-robin 0` | `RR` | `VMW_PSP_RR` | Active-active arrays |
| Least Queue | `queue-length 0` | `LQD` | — | Mixed latency |
| Fixed / MRU | `failover` | `FO` | `VMW_PSP_MRU` | Active-passive arrays |

## Common Issues

| Symptom | Cause | Check |
|---|---|---|
| Single path only | Second NIC not bound to iSCSI | Verify both NICs have iSCSI sessions established |
| All paths failed | Network outage or array port down | `multipath -ll` — check path states |
| I/O pinned to one path | Round robin not configured | Set PSP to RR on ESXi; `multipath -ll` policy on Linux |
| Device shows as `dm-N` but no multipath | OS disk accidentally included | Add to `blacklist` in multipath.conf |
