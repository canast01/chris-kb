---
tags:
  - networking
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
