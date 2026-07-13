---
tags:
  - networking
description: "NTP Drift reference covering Drift Concepts, Reading Drift Values, Drift File, Interpreting Drift History, Drift After VM Operations and 1 more sections."
---
# NTP Drift

<div class="kb-summary">
NTP Drift reference covering Drift Concepts, Reading Drift Values, Drift File, Interpreting Drift History, Drift After VM Operations and 1 more sections.
</div>

Clock drift is the natural tendency of a system clock to run fast or slow relative to real time. NTP continuously corrects drift by applying small frequency adjustments (slewing) to keep the clock accurate.

```d2
direction: down

drift_concepts: "Drift Concepts" {shape: rectangle}
reading_drift_values: "Reading Drift Values" {shape: rectangle}
drift_file: "Drift File" {shape: rectangle}
interpreting_drift_history: "Interpreting Drift History" {shape: rectangle}
drift_after_vm_operations: "Drift After VM Operations" {shape: rectangle}
windows_drift: "Windows Drift" {shape: rectangle}

drift_concepts -> reading_drift_values: uses
reading_drift_values -> drift_file: uses
drift_file -> interpreting_drift_history: uses
interpreting_drift_history -> drift_after_vm_operations: uses
drift_after_vm_operations -> windows_drift: uses
```

## Drift Concepts

| Term | Definition |
|---|---|
| **Drift / Frequency error** | How many parts-per-million (ppm) the clock runs fast or slow |
| **Offset** | The current difference between local clock and NTP source |
| **Slewing** | Gradually adjusting the clock rate to correct offset (max ~500ppm) |
| **Stepping** | Abrupt clock jump — used only when offset is too large to slew |
| **Drift file** | Saved frequency correction so the daemon starts with a good estimate |

1 ppm ≈ 0.0864 seconds per day. A 100 ppm drift = ~8.6 seconds per day without NTP.

## Reading Drift Values

```bash
# chronyc — frequency offset and skew
chronyc tracking | grep -E "Frequency|Skew|System time|Last offset"

# Example output:
# System time     :  0.000012345 seconds fast of NTP time
# Last offset     : +0.000001234 seconds
# Frequency       : 12.345 ppm fast   ← clock runs 12.345 ppm fast
# Skew            :  0.123 ppm        ← uncertainty in the frequency estimate
```


```text title="Expected output"
System time     :  0.000012345 seconds fast of NTP time
Last offset     : +0.000001234 seconds
Frequency       : 12.345 ppm fast
Skew            :  0.123 ppm
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `506 Cannot talk to daemon` | Ensure chronyd is running with `systemctl start chronyd` and listening on the local socket. |
    | `No such file or directory` | Install chrony with `apt-get install chrony` (Debian/Ubuntu) or `yum install chrony` (RHEL/CentOS). |
| Value | Healthy range | Concern |
|---|---|---|
| Frequency | ±500 ppm | > ±1000 ppm — hardware issue |
| Skew | < 10 ppm | > 100 ppm — few or unstable sources |
| System time offset | < 100ms | > 1s — risk of auth/Kerberos failures |

## Drift File

The drift file stores the last known frequency correction. On startup, the NTP daemon loads this value to avoid large initial offsets.

```bash
# chronyd drift file location
cat /var/lib/chrony/drift

# ntpd drift file location
cat /var/lib/ntp/drift

# Example content: a single floating-point number (ppm)
# 12.345678
```


```text title="Expected output"
12.345678
cat: /var/lib/ntp/drift: No such file or directory
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cat: /var/lib/ntp/drift: No such file or directory` | The system is running chronyd instead of ntpd; check which NTP daemon is active with `systemctl status chronyd` or `systemctl status ntpd`. |
    | `Permission denied` | Run the command with `sudo` since drift files are typically readable only by the ntp/chrony service user. |
If the drift file is deleted or corrupt, the daemon will start from zero correction and take longer to converge.

## Interpreting Drift History

```bash
# chronyc — show drift over time (last N measurements)
chronyc sourcestats

# Output columns: Name/IP, N, Polls, Reach, Last_Rx, Last sample, Est offset, Est error
```


```text title="Expected output"
210 Number of sources = 4
                      .- Number of samples in measurement set.
                     /    .- Number of runner cycles in measurement set.
                    |    /     .- Number of measurements remaining in set.
                    |   |      /
Name/IP            NP  NR Span Frequency  Freq Skew Offset Std Dev
==============================================================================
ntp1.example.com   64  64  63m     +0.000ppm  ±0.020ppm  -2.345us   1.234us
ntp2.example.com   64  64  63m     +0.015ppm  ±0.018ppm  +1.892us   0.987us
time.google.com    32  32  31m     -0.008ppm  ±0.025ppm  -0.456us   1.567us
169.254.169.123    16  16  15m     +0.042ppm  ±0.035ppm  +3.210us   2.145us
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `506 Cannot talk to daemon` | Ensure chronyd is running with `sudo systemctl start chronyd` and listening on localhost. |
    | `No such file or directory` | Install chrony with `sudo apt-get install chrony` (Debian/Ubuntu) or `sudo yum install chrony` (RHEL/CentOS). |
## Drift After VM Operations

VMs commonly accumulate clock drift after:
- **Suspend/resume** — clock stops, then jumps on resume
- **vMotion** — minor timing discontinuity
- **High CPU load** — timer interrupts delayed

```bash
# Force immediate resync after VM resume
chronyc makestep

# Configure chrony to step on large offsets (in /etc/chrony.conf)
makestep 1.0 3   # step if offset > 1s on first 3 updates
```


```text title="Expected output"
200 OK
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `506 Cannot talk to daemon` | Ensure chronyd is running with `systemctl start chronyd` and listening on the local socket. |
    | `makestep: command not found` | The `makestep` directive belongs in `/etc/chrony.conf` configuration file, not executed directly; remove it from the command line and add it to the config file instead. |
## Windows Drift

```powershell
# Check frequency offset
w32tm /query /status | Select-String "Frequency"

# Adjust max drift allowed (registry)
# HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Config\MaxPosPhaseCorrection
# HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Config\MaxNegPhaseCorrection
# Default 54000 seconds (15 hours) — reduce for stricter environments
```
