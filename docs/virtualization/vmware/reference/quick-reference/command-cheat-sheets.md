---
tags:
  - reference
description: "Command Cheat Sheet reference covering ESXi Host Commands, vSAN Commands, Network Checks, Log Locations."
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


```text title="Expected output"
VMware ESXi 7.0.3 build-19482429
 10:42:33 up 187 days, 14:23, 0 users, load average: 0.45, 0.38, 0.41
Running (/etc/init.d/hostd): hostd
Running (/etc/init.d/vpxa): vpxa
Running (/etc/init.d/hostd): hostd
Running (/etc/init.d/vpxa): vpxa
Services restarted.
Name    PCI Driver      Admin Status  Runtime Status  MTU  Enabled
vmnic0  0000:02:00.0   up            up               1500 true
vmnic1  0000:02:00.1   up            up               1500 true
vmnic2  0000:03:00.0   down          down             1500 false
vmnic3  0000:03:00.1   down          down             1500 false
Name           IPV4 Address      IPV4 Netmask      IPV6 Address  Enabled
vmk0           192.168.1.50      255.255.255.0     ::1/128        true
vmk1           10.0.0.50         255.255.255.0     -              true
Adapter  Driver     State  UID
vmhba0   lpfc       link-n/a urn:esx:nic:vmhba0
vmhba1   megaraid_sas link-n/a urn:esx:nic:vmhba1
vmhba2   ahci       link-n/a urn:esx:nic:vmhba2
Name                   Runtime Name  Device  Adapter  Channel  Target  LUN  State
vmhba0:C0:T0:L0        naa.50001fe1  /dev/sda vmhba0   0        0       0    active
vmhba0:C0:T1:L0        naa.50001fe2  /dev/sdb vmhba0   0        1       0    active
vmhba1:C0:T0:L0        naa.50001fe3  /dev/sdc vmhba1   0        0       0    active
Name                          Type  Size      Free Space  Accessible
VMFS-6 (datastore1)           VMFS  2.0 TB    1.2 TB      true
NFS (nfs-backup)              NFS   5.0 TB    3.8 TB      true
VFFS (LOCKER)                 VFFS  4.0 GB    2.1 GB      true
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `services.sh: command not found` | Use the full path `/sbin/services.sh status` or verify the script exists in the current ESXi version. |
    | `Unable to connect to the local hostd agent` | Wait 30 seconds after restart before running commands, as hostd takes time to fully initialize. |
    | `Permission denied` | Run all commands as root or with appropriate sudo privileges; standard users cannot access ESXi management commands. |
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


```text title="Expected output"
Cluster UUID: 52d4a8f1-7c2e-4a9b-b1d2-8e3f9c5a2b7d
Cluster Dominance: 1
Node UUID: 4f8c9a2b-3d1e-5f7a-9c4b-2e6d8f1a3c5b
Subcluster Master UUID: 52d4a8f1-7c2e-4a9b-b1d2-8e3f9c5a2b7d
Subcluster Master Mode: ELECTED
Health State: HEALTHY

Interface vmk1 is used for vSAN traffic
Interface vmk2 is used for vSAN traffic
Multicast: enabled
Unicast: enabled

Disk Group 1:
  Cache Tier: naa.5001405a1b2c3d4e (SSD, 400GB)
  Capacity Tier: naa.5001405a1b2c3d4f (HDD, 2TB)
  Status: HEALTHY

Disk Group 2:
  Cache Tier: naa.5001405a1b2c3d50 (SSD, 400GB)
  Capacity Tier: naa.5001405a1b2c3d51 (HDD, 2TB)
  Status: HEALTHY

Resync Summary:
  Objects pending resync: 0
  Bytes pending resync: 0
  Estimated time to completion: 0 seconds
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vSAN cluster is not enabled on this host` | Enable vSAN on the host through vCenter or run `esxcli vsan cluster new` to initialize the cluster. |
    | `Unable to connect to vSAN cluster` | Verify vSAN network connectivity on vmk interfaces and ensure all hosts have matching cluster UUIDs with `esxcli vsan cluster get`. |
    | `Permission denied` | Run the command as root or with appropriate vSAN administrator privileges on the ESXi host. |
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


```text title="Expected output"
PING 192.168.1.100 (192.168.1.100): 56 data bytes
64 bytes from 192.168.1.100: icmp_seq=0 time=2.345 ms
64 bytes from 192.168.1.100: icmp_seq=1 time=2.156 ms
64 bytes from 192.168.1.100: icmp_seq=2 time=2.289 ms
--- 192.168.1.100 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 2.156/2.263/2.345 ms

Name    PCI Driver    Link Speed Duplex MAC Address         MTU Description
vmnic0  0000:02:00.0 e1000  Up   1000  Full   00:50:56:c0:00:08 1500 Intel Corporation 82545EM Gigabit Ethernet Controller
vmnic1  0000:02:01.0 e1000  Up   1000  Full   00:50:56:c0:00:09 1500 Intel Corporation 82545EM Gigabit Ethernet Controller

Name            Portgroups Uplinks
vSwitch0        Management Network,VM Network vmnic0,vmnic1
vSwitch1        iSCSI vmnic2
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vmkping: Unknown host <target-ip>` | Verify the target IP address is reachable and correctly formatted (e.g., 192.168.1.100). |
    | `Network adapter vmk1 not found` | Confirm the VMkernel adapter exists by running `esxcli network ip interface list` and use the correct interface name. |
    | `PING 192.168.1.100 (192.168.1.100): 56 data bytes ... 100% packet loss` | Check physical network connectivity, verify the target host is online, and confirm firewall rules allow ICMP traffic. |
## Log Locations

```bash
/var/log/hostd.log
/var/log/vpxa.log
/var/log/vmkernel.log
/var/log/vobd.log
/var/log/syslog.log
/var/log/auth.log
```


```text title="Expected output"
(no output — these are file paths listed for reference, not commands to execute)
```