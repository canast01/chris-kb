# NTP Sync State

The sync state tells you whether a system's clock is actively tracking an NTP source and how closely. A drifting or unsynchronised clock causes authentication failures, log correlation errors, and Kerberos breakage.

## Reading `chronyc tracking` (Linux)

```bash
chronyc tracking
```

```
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

```
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
