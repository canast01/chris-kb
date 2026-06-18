---
tags:
  - esxi
  - operations
---
# ESXi Cheat Sheet

<div class="kb-summary">
Top-10 ESXi shell commands for host management, networking, storage, and VM control via <code>esxcli</code>.
</div>

```text
┌─────────────────────────────────────── ESXi Cheat Sheet ──────────────────────────────────────────────┐
│  CLI: esxcli (local shell or remote with --server)  ·  Also: vim-cmd, esxcfg-*                        │
│  Categories: Network · Storage · VMs · System · NIC · Maintenance                                     │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Common commands

```bash
# System info
esxcli system version get                      # ESXi build and version
esxcli system hostname get                     # FQDN and domain
esxcli hardware platform get                   # hardware vendor and model

# Network
esxcli network nic list                        # physical NICs: link state, speed, driver
esxcli network ip interface list               # VMkernel adapters and IPs
esxcli network vm list                         # VMs with active network connections

# Storage
esxcli storage nmp device list                 # NMP multipath devices
esxcli storage core adapter list               # HBAs: FC, iSCSI, NVMe
esxcli storage filesystem list                 # mounted datastores with capacity

# VMs
vim-cmd vmsvc/getallvms                        # all registered VMs with vmid
vim-cmd vmsvc/power.getstate <vmid>            # power state of a VM
vim-cmd vmsvc/power.on <vmid>                  # power on VM by vmid
vim-cmd vmsvc/snapshot.create <vmid> snap1     # create snapshot

# Maintenance
esxcli system maintenanceMode set --enable true   # enter maintenance mode
esxcli system maintenanceMode set --enable false  # exit maintenance mode
esxcli system shutdown poweroff --reason "hw fix" # power off host (with reason)
```

## Quick diagnostics

```bash
esxcli system syslog config get                # syslog target and rotation config
esxcli network diag ping -H 8.8.8.8 -c 3      # ICMP ping from VMkernel
esxcli storage core device list | grep -i ssd # list SSD-flagged devices
esxtop -b -n 2 -d 2 > /tmp/esxtop.csv         # batch esxtop snapshot (2 iterations)
```

## See also

- [ESXi Operations](../../virtualization/vmware/esxi/operations/procedures/)
- [ESXi Troubleshooting](../../virtualization/vmware/esxi/troubleshooting/common-issues/)
- [PowerCLI Cheat Sheet](powercli/)
