---
tags:
  - networking
description: "NTP Sync State reference covering Reading chronyc tracking (Linux), Reading timedatectl (Linux — systemd-timesyncd), Windows — w32tm, Network Devices..."
---
# NTP Sync State

<div class="kb-summary">
NTP Sync State reference covering Reading `chronyc tracking` (Linux), Reading `timedatectl` (Linux — systemd-timesyncd), Windows — w32tm, Network Devices, States and Meanings and 1 more sections.
</div>

The sync state tells you whether a system's clock is actively tracking an NTP source and how closely. A drifting or unsynchronised clock causes authentication failures, log correlation errors, and Kerberos breakage.

```d2
direction: down

reading_chronyc_tracking_linux: "Reading `chronyc tracking` (Linux)" {shape: rectangle}
reading_timedatectl_linux_systemdtim: "Reading `timedatectl` (Linux — systemd-timesyncd)" {shape: rectangle}
windows_w32tm: "Windows — w32tm" {shape: rectangle}
network_devices: "Network Devices" {shape: rectangle}
states_and_meanings: "States and Meanings" {shape: rectangle}
force_immediate_sync: "Force Immediate Sync" {shape: rectangle}

reading_chronyc_tracking_linux -> reading_timedatectl_linux_systemdtim: uses
reading_timedatectl_linux_systemdtim -> windows_w32tm: uses
windows_w32tm -> network_devices: uses
network_devices -> states_and_meanings: uses
states_and_meanings -> force_immediate_sync: uses
```

## Reading `chronyc tracking` (Linux)

```bash
chronyc tracking
```

```text
Reference ID    : C0A80001 (ntp1.example.com)
Stratum         : 3
Ref time (UTC)  : Sun May 10 00:00:00 2026
System time     : 0.000123456 seconds fast of NTP time
Last offset     : +0.000001234 seconds
RMS offset      : 0.000005678 seconds
Frequency       : 12.345 ppm fast
Residual freq   : +0.001 ppm
Skew            : 0.123 ppm
Root delay      : 0.001234567 seconds
Root dispersion : 0.000567890 seconds
Update interval : 64.4 seconds
Leap status     : Normal
```

| Field | Healthy value | Investigate if |
|---|---|---|
| Reference ID | Shows server name/IP | `(0.0.0.0)` — not synced |
| Stratum | 2–4 | > 10 or `unsynchronised` |
| System time | < 100ms | > 1 second |
| Last offset | < 10ms | > 500ms |
| Leap status | `Normal` | `Not synchronised` |

## Reading `timedatectl` (Linux — systemd-timesyncd)

```bash
timedatectl status
```

```text
               Local time: Sun 2026-05-10 00:00:00 UTC
           Universal time: Sun 2026-05-10 00:00:00 UTC
                 RTC time: Sun 2026-05-10 00:00:00
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes        ← key field
              NTP service: active
          RTC in local TZ: no
```

## Windows — w32tm

```powershell
# Check sync status
w32tm /query /status

# Resync immediately
w32tm /resync /force

# Show peer list
w32tm /query /peers
```

## Network Devices

```bash
# Cisco IOS
show ntp status
show ntp associations

# Arista EOS
show ntp status
show ntp associations

# Expected: system clock is synced to <ntp-server>, stratum 3
```


```text title="Expected output"
Clock is synchronized
system peer 203.0.113.45, stratum 3
ref time is e5a3c2f1.8b4d2a19  (13:42:33.545 UTC Mon Jan 15 2024)
clock offset is 2.341 ms, root delay is 18.523 ms
root dispersion is 45.821 ms, peer dispersion is 12.456 ms

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*203.0.113.45    192.0.2.100      2 u   64 1024  377   18.523    2.341  11.234
+198.51.100.22   192.0.2.101      2 u  128 1024  377   22.145    5.678   9.876
-192.0.2.50      .POOL.           16 p    -   64    0    0.000    0.000   0.000

NTP is enabled
```

!!! warning "Common errors"
    **`Clock is unsynchronized`** — Verify NTP server reachability with `ping <ntp-server>` and check that NTP is enabled with `ntp enable` on Arista or `ntp enable` on Cisco IOS.
    **`stratum 16 (unsynchronized)`** — Confirm the NTP server is reachable and responding; check firewall rules allowing UDP port 123 bidirectionally.
    **`reach 0`** — Verify the NTP server IP address is correct and the network path is not blocked; check `show ntp associations detail` for timeout or authentication errors.
## States and Meanings

| State | Meaning | Action |
|---|---|---|
| `synchronized` | Clock is tracking NTP source | None — healthy |
| `unsynchronised` | No usable source found | Check sources, firewall (UDP 123), server reachability |
| `stepping` | Large offset corrected by step | Normal after first sync; investigate if recurring |
| `Not synchronised` (w32tm) | Windows has no valid peer | Check w32tm config and network |

## Force Immediate Sync

```bash
# chronyd — step clock immediately
chronyc makestep

# systemd-timesyncd
systemctl restart systemd-timesyncd

# ntpd
ntpdate -u <ntp-server>
```


```text title="Expected output"
200 OK
(no output — command completes silently)
 4 Jan 2024 14:32:18 ntpdate[2847]: adjust time server 203.0.113.42 offset -0.127456 sec
```

!!! warning "Common errors"
    **`506 Cannot talk to daemon`** — Ensure chronyd is running with `systemctl start chronyd` before executing makestep.
    **`ntpdate[3124]: no server suitable for synchronization found`** — Verify the NTP server is reachable and responsive with `ntpdate -q <ntp-server>` first, and confirm network connectivity.