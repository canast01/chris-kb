---
tags:
  - networking
description: "NTP Sources reference covering Stratum Hierarchy, Viewing Sources — chrony (Linux), Source Statistics, Configuring Sources (chrony), Windows — w32tm..."
---
# NTP Sources

<div class="kb-summary">
NTP Sources reference covering Stratum Hierarchy, Viewing Sources — chrony (Linux), Source Statistics, Configuring Sources (chrony), Windows — w32tm Source Config and 2 more sections.
</div>

An NTP source is a time server that the local daemon polls to correct the system clock. Source quality determines how accurate the local clock can be.

```d2
direction: down

stratum_hierarchy: "Stratum Hierarchy" {shape: rectangle}
viewing_sources_chrony_linux: "Viewing Sources — chrony (Linux)" {shape: rectangle}
source_statistics: "Source Statistics" {shape: rectangle}
configuring_sources_chrony: "Configuring Sources (chrony)" {shape: rectangle}
windows_w32tm_source_config: "Windows — w32tm Source Config" {shape: rectangle}
cisco_arista_sources: "Cisco / Arista Sources" {shape: rectangle}

stratum_hierarchy -> viewing_sources_chrony_linux: uses
viewing_sources_chrony_linux -> source_statistics: uses
source_statistics -> configuring_sources_chrony: uses
configuring_sources_chrony -> windows_w32tm_source_config: uses
windows_w32tm_source_config -> cisco_arista_sources: uses
```

## Stratum Hierarchy

```text
Stratum 0 — atomic clock / GPS receiver (hardware reference)
Stratum 1 — directly connected to stratum 0 (public NTP servers)
Stratum 2 — synced from stratum 1 (most enterprise NTP servers)
Stratum 3 — synced from stratum 2 (internal hosts syncing from internal NTP)
```

Production servers should sync to internal stratum 2 servers. Stratum 10+ or `unsynchronised` is a problem.

## Viewing Sources — chrony (Linux)

```bash
# Source list with reach, offset, and jitter
chronyc sources -v

# Output interpretation:
# M — mode: * = current best, + = acceptable, - = excluded, ? = not reached
# Name/IP — source address
# Stratum — source stratum
# Poll — current poll interval (log2 seconds)
# Reach — 8-bit shift register (377 = all 8 polls reached)
# Last Rx — seconds since last sample
# Last sample — offset and error estimate
```

```text
MS Name/IP address         Stratum Poll Reach Last Rx Last sample
==================================================================
^* ntp1.example.com              2   6   377    23   -1.2ms[  -1.1ms] +/- 4.5ms
^+ ntp2.example.com              2   6   377    24   +0.3ms[  +0.3ms] +/- 6.1ms
^- ntp3.example.com              3   6   377    25   +2.1ms[  +2.1ms] +/- 9.0ms
```

| Symbol | Meaning |
|---|---|
| `*` | Currently selected source |
| `+` | Acceptable alternative (will be used if `*` fails) |
| `-` | Discarded by the selection algorithm |
| `?` | Source not reachable |
| `x` | Falseticker (clock appears wrong) |

## Source Statistics

```bash
# Per-source frequency offset and jitter history
chronyc sourcestats -v

# Show reference ID and source details
chronyc tracking
```


```text title="Expected output"
210 Number of sources = 4
                                      .- Number of sample points in measurement set.
                                     /    .- Number of residual runs.
                                    |    /    .- Length of measurement set (time).
                                    |   |    /      .- Estimated skew on measurement.
                                    |   |   |      /     .- Estimated frequency offset of source.
                                    |   |   |     |      /    .- Estimated offset of source.
                                    |   |   |     |     |    /  .- Estimate of source standard deviation.
                                    |   |   |     |     |   |   /
Name/IP Address            NP  NR  Span Frequency Freq Skew Offset Std Dev
===============================================================================
ntp.ubuntu.com              8   4   127     +0.000ppm  +0.000ppm  0.000us    1.234ms
time.google.com             6   3    63     -0.015ppm  +0.005ppm  0.001us    2.456ms
pool.ntp.org                7   5    95     +0.008ppm  -0.002ppm  0.002us    1.890ms
169.254.169.123             5   2    31     +0.100ppm  +0.050ppm  0.005us    5.678ms

Reference ID    : C0248F97 (169.254.169.123)
Leap status     : Normal
RMS offset      : 0.001234 seconds
Frequency       : 0.015 ppm fast
Residual freq   : +0.000 ppm
Skew            : 0.012 ppm
Root delay      : 0.015432 seconds
Root dispersion : 0.003456 seconds
Update interval : 1024.0 seconds
Leap second     : 0
```

!!! warning "Common errors"
    **`506 Cannot talk to daemon`** — Ensure chronyd is running with `sudo systemctl start chronyd` and listening on localhost.
    **`No sources present in sourcestats output`** — Wait 30+ seconds after chronyd startup for sources to be polled and added to the measurement set.
## Configuring Sources (chrony)

```bash
# /etc/chrony.conf
server ntp1.example.com iburst prefer
server ntp2.example.com iburst
server ntp3.example.com iburst

# iburst — sends 4 packets immediately on startup for faster initial sync
# prefer — prefer this source over others of similar quality
# minpoll/maxpoll — override default polling interval (log2 seconds)
server ntp1.example.com iburst minpoll 4 maxpoll 8

# Reload without restarting
chronyc reload sources
```


```text title="Expected output"
200 OK
Reloading sources.
  .d/m/y h:m:s     *.ntp1.example.com  8 -1024   377   100   9.123ms[  9.123ms] +/-  12.456ms
  .d/m/y h:m:s     + ntp2.example.com  8  -512   289    99   4.567ms[  4.567ms] +/-   8.234ms
  .d/m/y h:m:s     + ntp3.example.com  8  -256   156    98  15.892ms[ 15.892ms] +/-  18.901ms
```

!!! warning "Common errors"
    **`506 Cannot talk to daemon`** — Ensure chronyd is running with `systemctl start chronyd` and listening on the socket.
    **`Invalid minpoll/maxpoll value`** — Use values between 3 and 17 (representing 2³ to 2¹⁷ seconds); minpoll must be less than maxpoll.
## Windows — w32tm Source Config

```powershell
# Set NTP sources
w32tm /config /manualpeerlist:"ntp1.example.com,0x8 ntp2.example.com,0x8" \
  /syncfromflags:manual /update

# Show current peers and their offsets
w32tm /query /peers

# Force sync
w32tm /resync /force
```

## Cisco / Arista Sources

```bash
# Cisco IOS
ntp server ntp1.example.com prefer
ntp server ntp2.example.com

show ntp associations     # sync status per peer
show ntp status           # current stratum and sync state

# Arista EOS
ntp server ntp1.example.com prefer
ntp server ntp2.example.com

show ntp status
show ntp associations
```


```text title="Expected output"
# Cisco IOS output:
ntp1.example.com configured as preferred peer
ntp2.example.com configured as peer

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ntp1.example.com 10.0.0.1     2 u   64 1024  377   12.543    2.156   1.234
+ntp2.example.com 10.0.0.2     2 u   32 1024  377   15.821   -1.043   2.891

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ntp1.example.com 10.0.0.1     2 u   64 1024  377   12.543    2.156   1.234

Clock is synchronized
Stratum is 3
Reference ID is 10.0.0.1
Precision is 2^-24
Root delay is 28.364 msec
Root dispersion is 45.291 msec
RTC is synchronized
System poll interval is 1024 seconds

# Arista EOS output:
Clock is synchronized
Stratum: 3
Reference ID: 10.0.0.1
Precision: 2^-24
Root delay: 28.364 ms
Root dispersion: 45.291 ms
Update interval: 1024 seconds
Leap indicator: 0

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ntp1.example.com 10.0.0.1     2 u   64 1024  377   12.543    2.156   1.234
+ntp2.example.com 10.0.0.2     2 u   32 1024  377   15.821   -1.043   2.891
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the NTP server hostname is resolvable; if DNS fails, use the IP address directly instead.
    **`NTP is not enabled`** — Enable NTP globally with `ntp enable` (Arista) or ensure `ntp enable` is configured before adding servers on Cisco.
    **`reach value is 0 and associations show no asterisk or plus sign`** — Check network connectivity to the NTP server and verify firewall rules allow UDP port 123 bidirectionally.
## Common Source Issues

| Symptom | Cause | Check |
|---|---|---|
| All sources `?` | UDP 123 blocked | Firewall rules; `nc -u <ntp-ip> 123` |
| `x` (falseticker) | Source clock is wrong | Remove source; investigate server |
| Reach not `377` | Intermittent packet loss | Check network path to NTP server |
| Only one source available | Other sources unreachable | Ensure minimum 3 sources for proper selection |
