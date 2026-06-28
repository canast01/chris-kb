---
tags:
  - reference
---
# Command Cheat Sheet

<div class="kb-summary">
Command Cheat Sheet reference covering ESXi Host Commands, vSAN Commands, Network Checks, Log Locations.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

esxi_host_commands: "ESXi Host Commands" {shape: rectangle}
vsan_commands: "vSAN Commands" {shape: rectangle}
network_checks: "Network Checks" {shape: rectangle}
log_locations: "Log Locations" {shape: rectangle}

esxi_host_commands -> vsan_commands: uses
vsan_commands -> network_checks: uses
network_checks -> log_locations: uses
```

## ESXi Host Commands

```bash
# Check ESXi version
vmware -v

# Check uptime
uptime

# Check services
services.sh status

# Restart management agents
/etc/init.d/hostd restart
/etc/init.d/vpxa restart

# Restart all management services
services.sh restart

# List network adapters
esxcli network nic list

# List VMkernel interfaces
esxcli network ip interface list

# List storage adapters
esxcli storage core adapter list

# List paths
esxcli storage core path list

# List mounted filesystems
esxcli storage filesystem list
```

## vSAN Commands

```bash
# Check vSAN cluster info
esxcli vsan cluster get

# Check vSAN network
esxcli vsan network list

# Check vSAN disks
esxcli vsan storage list

# Check resync summary
esxcli vsan debug resync summary get
```

## Network Checks

```bash
# Ping from ESXi
vmkping <target-ip>

# Ping using a specific VMkernel adapter
vmkping -I vmk1 <target-ip>

# Test jumbo frames
vmkping -I vmk1 -s 8972 -d <target-ip>

# List physical NICs
esxcli network nic list

# List standard switches
esxcli network vswitch standard list
```

## Log Locations

```bash
/var/log/hostd.log
/var/log/vpxa.log
/var/log/vmkernel.log
/var/log/vobd.log
/var/log/syslog.log
/var/log/auth.log
```
