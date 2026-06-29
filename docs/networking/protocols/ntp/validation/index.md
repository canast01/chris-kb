---
tags:
  - networking
---
# NTP Validation

<div class="kb-summary">
NTP Validation reference covering Validation Checklist, Validation Commands, Post-Config Convergence, Validating NTP on Multiple Hosts, Common Validation Failures.
</div>

Use these checks after configuring NTP on a new system, after a maintenance window, or when time-sensitive services (Kerberos, TLS, log correlation) report failures.

```d2
direction: down

validation_checklist: "Validation Checklist" {shape: rectangle}
validation_commands: "Validation Commands" {shape: rectangle}
postconfig_convergence: "Post-Config Convergence" {shape: rectangle}
validating_ntp_on_multiple_hosts: "Validating NTP on Multiple Hosts" {shape: rectangle}
common_validation_failures: "Common Validation Failures" {shape: rectangle}

validation_checklist -> validation_commands: uses
validation_commands -> postconfig_convergence: uses
postconfig_convergence -> validating_ntp_on_multiple_hosts: uses
validating_ntp_on_multiple_hosts -> common_validation_failures: uses
```

## Validation Checklist

| Check | Command | Pass Criteria |
|---|---|---|
| Sync state | `chronyc tracking` | Leap status: Normal |
| Offset | `chronyc tracking` | System time < 100ms from NTP |
| Sources reachable | `chronyc sources` | At least one source marked `*` |
| Reach register | `chronyc sources` | Reach = `377` (all polls received) |
| Stratum | `chronyc tracking` | Stratum 2–4 |
| No firewall block | `ntpdate -q <server>` | Returns offset and delay |

## Validation Commands

### Linux — chrony

```bash
# Full sync summary
chronyc tracking

# Source states (* = selected, + = acceptable, ? = unreachable)
chronyc sources -v

# Detailed per-source statistics
chronyc sourcestats -v

# Watch sync converge (useful after first config)
watch -n 5 'chronyc tracking | grep -E "System time|Stratum|Leap"'

# Check daemon is running
systemctl is-active chronyd
```


```text title="Expected output"
reference id : 91F20D03 (ntp.ubuntu.com)
stratum : 2
ref time (UTC) : Fri Jan 17 14:32:18 2025
system time : 0.000234567 seconds slow of NTP time
last offset : +0.000145234 seconds
rms offset : 0.000089123 seconds
frequency : -2.456 ppm fast
residual freq : +0.012 ppm
skew : 0.087 ppm
root delay : 0.031456 seconds
root dispersion : 0.015234 seconds
max error : 0.018567 seconds
leap status : Normal

MS Name/IP address Stratum Poll Reach LastRx Last sample
===============================================================================
^* ntp.ubuntu.com 1 6 377 12 -145us[ -145us] +/- 15ms
^+ 91.189.89.199 2 6 377 18 +234us[ +234us] +/- 18ms
^+ time.cloudflare.com 2 6 377 25 +89us[ +89us] +/- 12ms
^? 192.168.1.1 16 6 0 - +0ns[ +0ns] +/- 0ns

Name/IP Address NP NR Span Frequency Freq Skew Offset Std Dev
===============================================================================
ntp.ubuntu.com 64 62 1023 -2.456ppm 0.089ppm -145us 12us
91.189.89.199 64 63 1023 +1.234ppm 0.076ppm +234us 15us
time.cloudflare.com 64 61 1023 -0.567ppm 0.095ppm +89us 18us
192.168.1.1 0 0 0 0.000ppm 0.000ppm +0ns 0ns

Every 5.0s: chronyc tracking | grep -E "System time|Stratum|Leap"
system time : 0.000012345 seconds slow of NTP time
Stratum : 2
Leap status : Normal

active
```

!!! warning "Common errors"
    **`506 Cannot talk to daemon`** — Ensure chronyd is running with `systemctl start chronyd` and listening on localhost.
    **`Stratum : 16` and `Reach : 0`** — Check network connectivity to NTP servers and verify firewall allows UDP port 123 outbound.
    **`system time : X seconds fast/slow of NTP time` (consistently >1 second)** — Run `chronyc makestep` to force immediate clock correction, or check for hardware clock drift.
### Linux — systemd-timesyncd

```bash
timedatectl status
timedatectl show-timesync --all
```


```text title="Expected output"
Local time: Wed 2024-01-17 14:32:47 UTC
           Universal time: Wed 2024-01-17 14:32:47 UTC
                 RTC time: Wed 2024-01-17 14:32:47
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
                RTC in local TZ: no

       Server: 91.189.89.199 (ntp.ubuntu.com)
Poll interval: 34min 8s (min: 32s; max 34min 8s)
         Leap: normal
      Version: 4
      Stratum: 2
    Reference: CDMA
    Precision: 1us
Root distance: 47.619ms (max: 5s)
       Offset: +1.234ms
    Delay: 18.329ms
    Jitter: 892us
 Packet count: 18
    Frequency: -500.123ppm
```

!!! warning "Common errors"
    **`Failed to get properties: Unit systemd-timesyncd.service not found.`** — Install systemd-timesyncd with `apt install systemd-timesyncd` or enable an alternative NTP daemon like chrony.
    **`System clock synchronized: no`** — Wait 5+ minutes for NTP synchronization to complete, or manually sync with `ntpdate -s <ntp-server>` if available.
### Windows

```powershell
# Sync status
w32tm /query /status

# Peer information
w32tm /query /peers

# Force resync and verify
w32tm /resync /force
w32tm /query /status | Select-String "Source|Stratum|Last Successful"
```

### Network Devices

```bash
# Cisco IOS
show ntp status          # synchronized: yes
show ntp associations    # peer table with offsets

# Arista EOS
show ntp status
show ntp associations

# Expected: "system clock is synchronized"
```


```text title="Expected output"
# Cisco IOS
Clock is synchronized
Stratum 2, Reference is 10.45.128.1
Nominal freq is 1000.0000 Hz, Actual freq is 1000.0000 Hz, Slew 0.000 ppm
Reference time is E8A3F2C1.2F4B8A00 (14:32:45.186 UTC Mon Jan 15 2024)
Clock offset is 2.341 msec, Root delay is 45.231 msec
Root dispersion is 18.567 msec, Peer dispersion is 3.421 msec
Loopfilter state is 'CTRL_FLL', drift is 0.000000000 s/s
System poll interval is 64, last update was 42 sec ago

     remote           refid      st t when poll reach   delay   offset  disp
*10.45.128.1     132.163.96.1     1 u   38   64  377   45.231    2.341  3.421
+10.45.128.2     132.163.96.2     1 u   41   64  377   52.104    3.127  4.156

# Arista EOS
NTP is enabled
Clock is synchronized
Stratum 2, Reference is 10.45.128.1
Nominal freq is 1000.0000 Hz, Actual freq is 1000.0000 Hz
Reference time is E8A3F2C1.2F4B8A00 (14:32:45.186 UTC Mon Jan 15 2024)
Clock offset is 1.892 msec, Root delay is 48.567 msec
Root dispersion is 16.234 msec, Peer dispersion is 2.891 msec

     remote           refid      st t when poll reach   delay   offset  disp
*10.45.128.1     132.163.96.1     1 u   35   64  377   48.567    1.892  2.891
+10.45.128.3     132.163.96.3     1 u   39   64  377   51.234    2.456  3.678
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the exact command syntax for your device OS version; use `show ntp ?` to list available subcommands.
    **`NTP is disabled`** — Enable NTP with `ntp enable` (Arista) or `ntp enable` (Cisco) and configure at least one server.
    **`Clock is unsynchronized, Stratum 16`** — Verify NTP server reachability with `ping <ntp-server>` and check that the reach value is non-zero in the associations table.
## Post-Config Convergence

After adding NTP sources, allow up to 5 minutes for chrony to:
1. Poll sources (`iburst` accelerates this to ~2 minutes)
2. Build offset history
3. Select the best source
4. Slew or step the clock

Force immediate convergence:

```bash
# Immediate step if offset is large
chronyc makestep

# Then verify
chronyc tracking | grep "System time"
```


```text title="Expected output"
200 OK
System time : 0.000000000 seconds fast of NTP time
```

!!! warning "Common errors"
    **`506 Cannot talk to daemon`** — Ensure chronyd is running with `systemctl start chronyd` and listening on the local socket.
    **`System time : [large offset] seconds fast of NTP time`** — The makestep command failed to correct the offset; check that chronyd has NTP sources available with `chronyc sources` and verify network connectivity.
## Validating NTP on Multiple Hosts

```bash
# Quick check across inventory via Ansible
ansible all -i inventory/production/ -m command \
  -a "chronyc tracking | grep -E 'Leap|System time|Stratum'"

# Or via SSH loop
for host in server{01..10}.example.com; do
  echo -n "$host: "
  ssh "$host" "chronyc tracking | grep 'Leap status'"
done
```


```text title="Expected output"
server01.example.com | SUCCESS | rc=0 >>
Leap status     : Normal
System time     : 0.000000123 seconds fast of NTP time
Stratum         : 2

server02.example.com | SUCCESS | rc=0 >>
Leap status     : Normal
System time     : -0.000000456 seconds slow of NTP time
Stratum         : 2

server03.example.com | SUCCESS | rc=0 >>
Leap status     : Normal
System time     : 0.000000089 seconds fast of NTP time
Stratum         : 3

server04.example.com | FAILED! rc=1 >>
(stderr) 500 EEE Command failed

server05.example.com | SUCCESS | rc=0 >>
Leap status     : Normal
System time     : -0.000000234 seconds slow of NTP time
Stratum         : 2

server01.example.com: Leap status     : Normal
server02.example.com: Leap status     : Normal
server03.example.com: Leap status     : Normal
server04.example.com: ssh: connect to host server04.example.com port 22: Connection timed out
server05.example.com: Leap status     : Normal
server06.example.com: Leap status     : Normal
server07.example.com: Leap status     : Normal
server08.example.com: Leap status     : Normal
server09.example.com: Leap status     : Normal
server10.example.com: Leap status     : Normal
```

!!! warning "Common errors"
    **`500 EEE Command failed`** — Verify chrony daemon is running on the target host with `systemctl status chronyd` and restart if necessary.
    **`ssh: connect to host server04.example.com port 22: Connection timed out`** — Check network connectivity and SSH access to the host with `ping server04.example.com` and verify firewall rules allow port 22.
    **`Permission denied (publickey,password)`** — Ensure your SSH key is deployed to the target host or add `-u <username>` to the Ansible command if using a non-default user account.
## Common Validation Failures

| Failure | Cause | Fix |
|---|---|---|
| `Not synchronised` | No sources reachable | Check firewall (UDP 123), source IPs |
| Offset > 1 second | Clock drifted heavily or stepped | `chronyc makestep` then monitor |
| Stratum 16 | No upstream source | chronyd running but all sources failed |
| Reach not `377` | Packet loss to NTP server | Check network path, DNS resolution of server name |
| Kerberos failure after fix | System clock now correct but Kerberos tickets old | `klist -k` / `kinit` to refresh |
