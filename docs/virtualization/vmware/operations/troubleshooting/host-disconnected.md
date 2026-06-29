---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
---
# Host Disconnected / Not Responding

<div class="kb-summary">
Diagnosing ESXi hosts showing disconnected or not responding in vCenter — management network failures, HA isolation, hostd/vpxa agent issues, and reconnect procedures.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
quick_triage: "Quick Triage" {shape: rectangle}
host_disconnected_in_vcenter: "Host Disconnected in vCenter" {shape: rectangle}
management_agent_reset: "Management Agent Reset" {shape: rectangle}
management_network_down: "Management Network Down" {shape: rectangle}
host_not_responding_psod_or_hung_ker: "Host Not Responding (PSOD or Hung Kernel)" {shape: rectangle}
host_cannot_enter_maintenance_mode: "Host Cannot Enter Maintenance Mode" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> quick_triage: investigate
symptom -> host_disconnected_in_vcenter: investigate
symptom -> management_agent_reset: investigate
symptom -> management_network_down: investigate
symptom -> host_not_responding_psod_or_hung_ker: investigate
symptom -> host_cannot_enter_maintenance_mode: investigate
quick_triage -> resolution
host_disconnected_in_vcenter -> resolution
management_agent_reset -> resolution
management_network_down -> resolution
host_not_responding_psod_or_hung_ker -> resolution
host_cannot_enter_maintenance_mode -> resolution
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Quick Triage

First, establish whether the host is truly unreachable or just disconnected in vCenter.

```bash
# Ping the host management IP from your workstation or jump host
ping <esxi-mgmt-ip>

# Try SSH directly — if this works, the host is up and it's a vCenter-to-host agent issue
ssh root@<esxi-mgmt-ip>

# Check DNS resolution for the host FQDN
nslookup <esxi-fqdn>
```


```text title="Expected output"
PING 192.168.1.42 (192.168.1.42) 56(84) bytes of data.
64 bytes from 192.168.1.42: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 192.168.1.42: icmp_seq=2 ttl=64 time=1.89 ms
64 bytes from 192.168.1.42: icmp_seq=3 ttl=64 time=2.12 ms
^C
--- 192.168.1.42 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/stddev = 1.89/2.11/2.34/0.19 ms

Connected to 192.168.1.42.
Escape character is '^]'.

ESXi 7.0.3 (Releasebuild-19482429)
root@esxi-prod-01:~]

Server:		192.168.1.10
Address:	192.168.1.10#53

Name:	esxi-prod-01.corp.local
Address:	192.168.1.42
```

!!! warning "Common errors"
    **`ping: unknown host <esxi-mgmt-ip>`** — Verify the IP address is correct and the host is reachable on the network; check firewall rules blocking ICMP.
    **`ssh: connect to host 192.168.1.42 port 22: Connection refused`** — Confirm SSH is enabled on the ESXi host (Configuration > Security Profile > Services > SSH) and the management network is properly configured.
    **`** server can't find <esxi-fqdn>: NXDOMAIN`** — Add the ESXi host FQDN to your DNS server or /etc/hosts file on the jump host.
If ping works but vCenter shows "Not Responding", skip to [Management Agent Reset](#management-agent-reset).

If ping fails entirely, skip to [Management Network Down](#management-network-down).

---

## Host Disconnected in vCenter

The host is reachable but vCenter has lost its agent connection (vpxa). Common causes: vpxa crash, certificate mismatch, or a vCenter restart while the host was isolated.

**Step 1 — Right-click the host in vCenter → Connect.** If this resolves it immediately, the connection was dropped by a transient event.

**Step 2 — If reconnect fails**, SSH to the host and check services:

```bash
# Check vpxa and hostd status
/etc/init.d/vpxa status
/etc/init.d/hostd status

# Restart vpxa (the vCenter agent — safe to restart, no VM impact)
/etc/init.d/vpxa restart

# If vpxa alone does not fix it, restart hostd too
/etc/init.d/hostd restart

# Check for errors in logs
tail -100 /var/log/vpxa.log
tail -100 /var/log/hostd.log
```


```text title="Expected output"
vpxa (pid 2847) is running
hostd (pid 1923) is running
Stopping vpxa...                                           [  OK  ]
Starting vpxa...                                           [  OK  ]
Stopping hostd...                                          [  OK  ]
Starting hostd...                                          [  OK  ]
2024-01-15T09:42:31.847Z [7F2A1C] [vpxa] [info] vpxa started (build-19193900)
2024-01-15T09:42:32.104Z [7F2A1C] [vpxa] [info] Connecting to hostd on localhost:902
2024-01-15T09:42:33.221Z [7F2A1C] [vpxa] [info] Connected to hostd successfully
2024-01-15T09:42:45.556Z [7F2A1C] [vpxa] [info] vCenter registration complete: esx-prod-01.lab.local
2024-01-15T09:42:46.112Z [7F2A1C] [hostd] [info] hostd started (build-19193900)
2024-01-15T09:42:47.334Z [7F2A1C] [hostd] [info] Listening on port 902
```

!!! warning "Common errors"
    **`vpxa (pid XXXX) is not running`** — Run `/etc/init.d/vpxa start` to restart the service, then check `/var/log/vpxa.log` for startup errors.
    **`hostd (pid XXXX) is not running`** — Run `/etc/init.d/hostd start` and verify the service started with `/etc/init.d/hostd status`.
    **`tail: cannot open '/var/log/vpxa.log' for reading: Permission denied`** — Run the tail commands with `sudo` or as root user to access ESXi system logs.
**Step 3 — Re-add the host in vCenter** if the agent restart does not help. In vCenter, right-click the host → Disconnect → Remove from Inventory → Re-add with Add Host wizard.

---

## Management Agent Reset

Use this when the host is reachable over the network but management services are unresponsive or looping.

```bash
# Full management agent restart (safe — does not affect running VMs)
services.sh restart

# Or restart individual services
/etc/init.d/hostd restart
/etc/init.d/vpxa restart
/etc/init.d/ntpd restart

# Verify services are running
services.sh status | grep -E "hostd|vpxa|ntpd"

# Check for stuck or looping processes
ps -c | grep hostd
ps -c | grep vpxa
```


```text title="Expected output"
Restarting services...
hostd stopped
hostd started
vpxa stopped
vpxa started
ntpd stopped
ntpd started

hostd                running
vpxa                 running
ntpd                 running

PID   COMMAND
2847  hostd
2891  hostd
PID   COMMAND
3124  vpxa
3156  vpxa
```

!!! warning "Common errors"
    **`hostd stopped (timeout)`** — Increase the timeout or check for hung processes with `lsof -p <PID>` before forcing a kill.
    **`vpxa: error while loading shared libraries: libssl.so.1.0.0: cannot open shared object file`** — Install the missing OpenSSL library with `esxcli software vib install -d /path/to/openssl-vib.zip`.
If hostd is repeatedly crashing, check disk space — a full `/` or `/scratch` partition prevents hostd from writing its state file:

```bash
df -h
vdf -h
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G   45G   55G  45% /
/dev/sda2       200G  120G   80G  60% /home
tmpfs           16G      0   16G   0% /dev/shm
/dev/sdb1       500G  380G  120G  76% /vmfs/volumes/datastore1
/dev/sdc1       1.0T  850G  150G  85% /vmfs/volumes/datastore2

vdf: command not found
```

!!! warning "Common errors"
    **`vdf: command not found`** — Replace `vdf` with `df` (the correct command for disk free space); if you need VMware-specific storage info, use `esxcli storage filesystem list` on ESXi hosts instead.
    **`Permission denied`** — Run the command with `sudo df -h` if you lack read permissions on mounted filesystems.
---

## Management Network Down

The host is not reachable at all. Check in this order:

1. **Physical layer** — Is the management NIC connected? Check iDRAC/iLO for NIC link state.
2. **VLAN configuration** — Was a switch or port-group change recently made?
3. **IP configuration** — Verify via iDRAC/iLO console or direct keyboard/monitor:

```bash
# From ESXi direct console (DCUI) — check VMkernel adapter
esxcli network ip interface list
esxcli network ip interface ipv4 get -i vmk0

# Check default gateway
esxcli network ip route list

# Verify basic network reachability
esxcli network diag ping -H <vcenter-ip>
```


```text title="Expected output"
Name  MAC Address        MTU  Enabled  Netstack
----  -----------------  ----  -------  --------
vmk0  00:50:56:c0:00:01  1500  true     defaultTcpipStack
vmk1  00:50:56:c0:00:02  1500  false    defaultTcpipStack

Interface  IPv4 Address      Netmask         Broadcast       Address Type
---------  ----------------  ---------------  ---------------  ----------------
vmk0       192.168.1.42      255.255.255.0    192.168.1.255    STATIC

Route                 Destination       Netmask           Gateway          MTU  TSO MSS  iface
-----                 ---------------   ---------------   ---------------  ---  -------  -----
0                     0.0.0.0           0.0.0.0           192.168.1.1      1500  65535   vmk0
1                     192.168.1.0       255.255.255.0     0.0.0.0          1500  65535   vmk0
2                     192.168.1.42      255.255.255.255   0.0.0.0          1500  65535   vmk0

PING 192.168.100.15 (192.168.100.15): 56 data bytes
64 bytes from 192.168.100.15: icmp_seq=0 time=2.341 ms
64 bytes from 192.168.100.15: icmp_seq=1 time=2.156 ms
64 bytes from 192.168.100.15: icmp_seq=2 time=2.289 ms
64 bytes from 192.168.100.15: icmp_seq=3 time=2.401 ms

--- 192.168.100.15 statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 2.156/2.297/2.401 ms
```

!!! warning "Common errors"
    **`Network error: Unable to resolve host <vcenter-ip>`** — Verify vCenter IP is correct and DNS resolution is working with `esxcli network ip dns server list`.
    **`PING: sendto: No route to host`** — Confirm the default gateway in the route table matches your network configuration and vmk0 is on the correct VLAN.
    **`Interface vmk0 is not enabled`** — Enable vmk0 with `esxcli network ip interface set -i vmk0 -e true` if it shows `Enabled: false`.
4. **Firewall** — Confirm the management VLAN firewall rules allow TCP 443, 902, and 8080 from vCenter to the host.

---

## Host Not Responding (PSOD or Hung Kernel)

A "Not Responding" state that persists after network checks usually means the host kernel has halted (PSOD — Purple Screen of Death) or the host is completely hung.

1. Open **iDRAC/iLO virtual console** — if you see a purple screen with a backtrace, the host has crashed.
2. Capture a photo of the PSOD (contains crash address and module name — needed for VMware GSS).
3. If the PSOD does not auto-reboot: trigger a hard reset via iDRAC/iLO.
4. After reboot, collect the **vm-support bundle** before further investigation:

```bash
# Generate support bundle from host
vm-support -w /tmp
# SCP the bundle off before it is potentially overwritten by another crash
```


```text title="Expected output"
Generating support bundle, this may take a few minutes...
Gathering system logs...
Gathering performance data...
Gathering configuration files...
Creating bundle archive...
Support bundle created successfully: /tmp/esx-bundle-2024-01-15-14-32-18.tgz
Bundle size: 487 MB
```

!!! warning "Common errors"
    **`vm-support: error writing to /tmp: No space left on device`** — Free up disk space on the host or specify an alternate writable directory with sufficient capacity (e.g., `/var/log` or a mounted datastore).
    **`vm-support: Permission denied`** — Run the command with root privileges using `sudo` or ensure your user account has write permissions to the target directory.
5. Review `/var/log/vmkernel.log` and `/var/log/vobd.log` for hardware errors preceding the crash.

---

## Host Cannot Enter Maintenance Mode

Common blockers and resolutions:

| Blocker | Check | Resolution |
|---|---|---|
| Running VMs cannot be migrated | DRS disabled or VMs pinned | Enable DRS or manually vMotion VMs first |
| vSAN evacuation failing | Insufficient vSAN capacity | Ensure cluster can absorb evacuated objects; check vSAN health |
| Template or ISO locked to host | Storage affinity rules | Move templates to a shared datastore not tied to the host |
| HA reconfiguration pending | HA agent failure | Reconfigure HA on the cluster before placing host in maintenance |
| Witness appliance on host | Cannot evacuate witness | Handle witness in its own maintenance window |

```powershell
# Check which VMs are on the host
Get-VMHost "esxi-host-fqdn" | Get-VM | Select Name, PowerState

# Force maintenance mode without vMotion (only if VMs are confirmed powered off)
Set-VMHost "esxi-host-fqdn" -State Maintenance -Evacuate $false
```

---

## Host Hardware Warning

Hardware alerts surface as vCenter alarms (yellow/red) on the host object. Correlate with the physical hardware management console.

```bash
# Check hardware health from ESXi CLI
esxcli hardware platform get
esxcli hardware memory get
esxcli hardware cpu list

# Check physical disk health
esxcli storage hba list

# Review system event log for hardware errors
vim-cmd hostsvc/firmware/sync_config
```


```text title="Expected output"
System UUID: 4a5b6c7d-8e9f-0a1b-2c3d-4e5f6a7b8c9d
System Product Name: ProLiant DL380 Gen10
Vendor: HPE
BIOS Version: U30 11/15/2023
Memory Size: 786432 MB
Memory Type: DDR4
Memory Speed: 2933 MHz
Processor: Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz
Core Count: 20
Thread Count: 40
Processor 0: Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz
Processor 1: Intel(R) Xeon(R) Gold 6248 CPU @ 2.50GHz

HBA Name: vmhba0
Driver: lpfc
Status: online
Model: Emulex OneConnect OCe14402-NX-L

HBA Name: vmhba1
Driver: lpfc
Status: online
Model: Emulex OneConnect OCe14402-NX-L

Syncing firmware configuration...
Sync completed successfully.
```

!!! warning "Common errors"
    **`vim-cmd: Unknown command 'hostsvc/firmware/sync_config'`** — Verify the correct vim-cmd syntax with `vim-cmd hostsvc/firmware/sync_config` or use `esxcli system firmware get` instead for firmware information.
    **`esxcli: Unknown command or namespace 'hardware platform'`** — Use `esxcli hardware platform get` only on ESXi 6.5+; for older versions, use `esxcli system hardware get` instead.
From iDRAC/iLO, review:
- PSU status
- Memory DIMM errors
- Physical disk and RAID state
- NIC link state
- Thermal / fan status

---

## Host NTP Drift

Certificate validation, HA heartbeats, and vSAN all depend on time sync. A drifting host can cause cascading issues.

```bash
# Check NTP status on ESXi
esxcli system ntp get
ntpq -p

# If NTP is not configured, set it
esxcli system ntp set --server <ntp-server-ip>
esxcli system ntp set --enabled true

# Force time sync immediately
/etc/init.d/ntpd restart

# Verify sync — look for * or + prefix next to a time source
ntpq -p
```


```text title="Expected output"
enabled: true
server: 0.pool.ntp.org
server: 1.pool.ntp.org

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 ntp.ubuntu.com  .POOL.          16 p    -   64    0    0.000    0.000   0.000
 time.google.com 216.239.35.0     2 u   52   64  377   18.234   -2.145   3.821
*ntp.ubuntu.com  132.163.96.1     2 u   48   64  377   22.156    1.032   2.456

NTP configuration updated.
NTP enabled.

Stopping ntpd: [  OK  ]
Starting ntpd: [  OK  ]

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*time.google.com 216.239.35.0     2 u   12   64  377   19.845    0.234   1.923
+ntp.ubuntu.com  132.163.96.1     2 u   18   64  377   21.567   -0.891   2.134
 0.pool.ntp.org  .POOL.          16 p    -   64    0    0.000    0.000   0.000
```

!!! warning "Common errors"
    **`Connection refused`** — Verify the NTP server IP is reachable from the ESXi host using `ping <ntp-server-ip>` and check firewall rules allowing UDP port 123.
    **`ntpq: read: Connection refused`** — Restart the NTP daemon with `/etc/init.d/ntpd restart` and wait 10-15 seconds before running `ntpq -p` again.
    **`Error: Unable to set NTP server`** — Ensure you have root privileges and the NTP server parameter uses valid IP format without extra spaces.
Hosts more than 5 minutes out of sync with vCenter will trigger authentication errors and HA isolation warnings.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Certificate Issues](certificate-issue.md)
- [Datastore Issues](datastore-inaccessible.md)
- [Known Issues and Fix Patterns](known-issues.md)
- [Virtualization Troubleshooting](index.md)
