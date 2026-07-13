---
tags:
  - networking
  - troubleshooting
search:
  boost: 1.5
description: "iSCSI Troubleshooting reference covering Diagnostic Flow, Quick Diagnostics, Common Issues Reference, MTU Troubleshooting, Log Locations and 1 more..."
---
# iSCSI Troubleshooting

<div class="kb-summary">
iSCSI Troubleshooting reference covering Diagnostic Flow, Quick Diagnostics, Common Issues Reference, MTU Troubleshooting, Log Locations and 1 more sections.
</div>

        TRIAGE: HOST CANNOT SEE iSCSI LUN

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
quick_diagnostics: "Quick Diagnostics" {shape: rectangle}
common_issues_reference: "Common Issues Reference" {shape: rectangle}
mtu_troubleshooting: "MTU Troubleshooting" {shape: rectangle}
log_locations: "Log Locations" {shape: rectangle}
kernel_messages_linux: "Kernel Messages (Linux)" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> quick_diagnostics: investigate
symptom -> common_issues_reference: investigate
symptom -> mtu_troubleshooting: investigate
symptom -> log_locations: investigate
symptom -> kernel_messages_linux: investigate
diagnostic_flow -> resolution
quick_diagnostics -> resolution
common_issues_reference -> resolution
mtu_troubleshooting -> resolution
log_locations -> resolution
kernel_messages_linux -> resolution
```

## Before you begin

- **Access:** Network admin credentials; console or SSH to devices
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Diagnostic Flow

```d2
direction: right

B: "B" {shape: rectangle}
C: "Check firewall, VLAN, routing" {shape: rectangle}
D: "D" {shape: rectangle}
E: "Run SendTargets discovery, check target IP" {shape: rectangle}
F: "F" {shape: rectangle}
G: "Check CHAP, initiator IQN, target config" {shape: rectangle}
H: "H" {shape: rectangle}
I: "Check host group / initiator group mapping on array" {shape: rectangle}
J: "J" {shape: rectangle}
K: "Check second path — NIC, VLAN, session" {shape: rectangle}
L: "Check filesystem / volume manager layer" {shape: rectangle}
A: "Host cannot see iSCSI LUN" {shape: rectangle}

B -> C
D -> E
F -> G
H -> I
J -> K
J -> L
```

## Quick Diagnostics

```bash
# Test TCP connectivity to target portal
nc -zv <target-ip> 3260

# Run discovery
iscsiadm -m discovery -t sendtargets -p <target-ip>:3260

# List active sessions
iscsiadm -m session

# Detailed session + path info
iscsiadm -m session -P 3

# Session statistics (errors, retries)
iscsiadm -m session -s

# Multipath device state
multipath -ll

# Rescan for new devices
iscsiadm -m node --rescan
echo "- - -" > /sys/class/scsi_host/host*/scan
multipath -r
```


```text title="Expected output"
Connection to 192.168.100.50 3260 port [tcp/*] succeeded!
192.168.100.50:3260,-1 iqn.2020-05.com.vendor:storage.target1
192.168.100.50:3260,-1 iqn.2020-05.com.vendor:storage.target2
tcp: [1] 192.168.100.50:3260,1 iqn.2020-05.com.vendor:storage.target1 (non-flash)
tcp: [2] 192.168.100.50:50 iqn.2020-05.com.vendor:storage.target2 (non-flash)
Target: iqn.2020-05.com.vendor:storage.target1
	Current Portal: 192.168.100.50:3260,1
	Iface Name: default
	Iface Transport: tcp
	Iface Initiator Name: iqn.1993-08.org.debian:01.a1b2c3d4e5f6
	Iface IPaddress: 192.168.100.10
	Iface HWaddress: 52:54:00:12:34:56
	Iface Netdev: eth0
	SID: 1
	iSCSI Connection State: LOGGED IN
	iSCSI Session State: LOGGED_IN
	Internal iscsid Session State: logged in
	*Current: OPERATIONAL
	*IP Address: 192.168.100.50
mpatha (360001405a1b2c3d4e5f6a7b8c9d0e1f) dm-0 VENDOR,STORAGE_LUN
size=500G features='0' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  `- 2:0:0:1 sdb 8:16 active ready running
mpathb (360001405a1b2c3d4e5f6a7b8c9d0e2f) dm-1 VENDOR,STORAGE_LUN
size=1.0T features='0' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  `- 3:0:0:1 sdc 8:32 active ready running
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `connect: Connection refused` | Verify the target IP and port are correct, and that the iSCSI target daemon is running on the target system. |
    | `iscsiadm: No records found` | Run discovery first with `iscsiadm -m discovery -t sendtargets -p <target-ip>:3260` before attempting to log in to sessions. |
    | `command not found: multipath` | Install the device-mapper-multipath package with `apt-get install multipath-tools` or `yum install device-mapper-multipath`. |
## Common Issues Reference

| Symptom | Probable cause | Resolution |
|---|---|---|
| `iscsiadm: No portals found` | Target IP wrong or portal down | Verify target IP; test with `nc -zv <ip> 3260` |
| `Login I/O error, rx -1, errno 111` | Connection refused — service not running or wrong port | Check target service; confirm port 3260 |
| CHAP auth failure | Username/password mismatch | Compare credentials on initiator (`iscsid.conf`) and array |
| Session established, no disks | IQN not in host group | Add initiator IQN to array host/initiator group |
| Disk appears but no multipath | One path only, multipath not configured | Verify second NIC has session; check multipathd |
| Intermittent I/O errors / session drops | MTU mismatch (jumbo frames) | Verify MTU 9000 end-to-end or reduce to 1500 consistently |
| Session drop during array maintenance | `replacement_timeout` exceeded | Extend timeout in `iscsid.conf` or coordinate maintenance window |
| Performance poor on iSCSI | Sharing NIC with management | Dedicate NICs to iSCSI; enable flow control |

## MTU Troubleshooting

```bash
# Test jumbo frame path (9000 byte MTU)
ping -M do -s 8972 <target-ip>   # 8972 + 28 byte header = 9000

# Check NIC MTU
ip link show <ethX>
ethtool <ethX> | grep -i mtu

# Set MTU
ip link set <ethX> mtu 9000
```


```text title="Expected output"
PING 192.168.100.50 (192.168.100.50) 8972(9000) bytes of data.
8980 bytes from 192.168.100.50: icmp_seq=1 ttl=64 time=0.842 ms
8980 bytes from 192.168.100.50: icmp_seq=2 ttl=64 time=0.756 ms
8980 bytes from 192.168.100.50: icmp_seq=3 ttl=64 time=0.891 ms
^C
--- 192.168.100.50 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 0.756/0.829/0.891/0.055 ms

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9000
    link/ether 00:0a:95:9d:68:16 brd ff:ff:ff:ff:ff:ff

	Speed: 10000Mb/s
	Duplex: Full
	Port: Twisted Pair
	PHYAD: 0
	Transceiver: internal
	Auto-negotiation: on
	MDI-X: on (auto)
	Current message level: 0x00000007 (7)
	Link detected: yes
	RX MTU: 9000
	TX MTU: 9000

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `PING: sendto: Message too long` | Verify target iSCSI portal and intermediate switch ports support 9000 MTU; check with `ethtool -i <ethX>` for driver limitations. |
    | `Cannot find device "<ethX>"` | Confirm the correct interface name with `ip link show` and replace `<ethX>` with the actual device (e.g., eth0, ens3). |
    | `RTNETLINK answers: Operation not permitted` | Run the MTU configuration command with `sudo` or as root user. |
## Log Locations

| Platform | Where to look |
|---|---|
| Linux | `journalctl -k | grep -i iscsi` / `/var/log/messages` |
| Windows | Event Viewer → System → iScsiPrt source |
| ESXi | `vmkwarning.log` / `vmkernel.log` in `/var/log/` |

## Kernel Messages (Linux)

```bash
# iSCSI kernel events
dmesg | grep -i iscsi

# Session recovery events
journalctl -k | grep -i "session recovery"

# SCSI device attach
dmesg | grep -i "Attached scsi"
```


```text title="Expected output"
[    2.847392] iSCSI transport class version 2.0-870
[    3.124561] iSCSI initiator name: iqn.1993-08.org.debian:01.a7f3c2e9d1b4
[   12.456789] iSCSI session established: sid=1 target=iqn.1991-05.com.example:storage.disk1
[   18.923401] iSCSI: Recovered session sid=2 after 45 seconds
[   45.671234] Attached scsi generic sg0 type 0
[   45.672145] sd 2:0:0:0: Attached scsi disk sdb at scsi2, channel 0, id 0, lun 0
[   45.673456] sd 2:0:0:1: Attached scsi disk sdc at scsi2, channel 0, id 1, lun 0
[   67.234567] iSCSI: connection recovery in progress for sid=1
[   89.456789] iSCSI session sid=1 recovered
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: (standard input): No such file or directory` | Ensure dmesg and journalctl commands are properly piped; check that the kernel ring buffer is accessible with `sudo dmesg`. |
    | `Hint: You are currently not seeing messages from other users and the system.` | Run journalctl with `sudo` to access full kernel logs: `sudo journalctl -k`. |
    | `(standard input): No such file or directory` | Verify iSCSI modules are loaded with `lsmod | grep iscsi`; if empty, load them with `sudo modprobe iscsi_tcp`. |
---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Initiators](../initiators/)
- [Multipathing](../multipathing/)
- [Sessions](../sessions/)
- [Targets](../targets/)
- [iSCSI — Overview](../)
