---
title: NTP
tags:
  - networking
---

# NTP

<div class="kb-summary">
Network Time Protocol (NTP) synchronises system clocks over UDP port 123 using a hierarchical stratum model. Clock skew breaks Kerberos auth, TLS validity, and log correlation. Coverage includes chrony/ntpd/w32tm configuration, stratum selection, sync health metrics, and VMware time sync rules.
</div>

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="sources/">
  <strong>Sources</strong>
  <span>Configuring NTP servers, pool.ntp.org, GPS reference clocks, and upstream stratum selection.</span>
</a>

<a class="kb-card" href="sync-state/">
  <strong>Sync State</strong>
  <span>Offset, stratum, jitter, and reference source status — reading chronyc tracking and w32tm /query output.</span>
</a>

<a class="kb-card" href="drift/">
  <strong>Drift</strong>
  <span>Clock drift measurement, frequency error (ppm), drift file management, and hardware clock tuning.</span>
</a>

<a class="kb-card" href="firewalls/">
  <strong>Firewalls</strong>
  <span>Firewall rules for UDP/123, bidirectional NTP traffic, and ACL patterns for enterprise environments.</span>
</a>

<a class="kb-card" href="validation/">
  <strong>Validation</strong>
  <span>Validating NTP sync health, confirming stratum, and verifying time accuracy post-deployment.</span>
</a>

</div>

## Quick Reference

**Stratum levels:**

| Stratum | Description |
|---|---|
| 0 | Reference clock (GPS, atomic, radio) — not directly on network |
| 1 | Server directly attached to stratum-0 device |
| 2 | Server synced from stratum-1 |
| 3–14 | Cascading sync hierarchy |
| 15 | Unsynchronised / unreachable |
| 16 | Clock unsynchronised (NTP sentinel value) |

**Key time metrics:**

| Metric | Description | Acceptable range |
|---|---|---|
| Offset | Difference between local clock and NTP source | < 1 ms (LAN), < 50 ms (WAN) |
| Drift | Clock frequency error (ppm) | < 100 ppm |
| Jitter | Variation in offset over time | < 10 ms |
| Stratum | Hops from reference clock | ≤ 3 for servers |

**Implementation comparison:**

| Platform | NTP daemon | Config file | Status command |
|---|---|---|---|
| Linux (modern) | chrony | `/etc/chrony.conf` | `chronyc tracking` |
| Linux (legacy) | ntpd | `/etc/ntp.conf` | `ntpq -p` |
| Windows Server | Windows Time (w32tm) | Registry / GPO | `w32tm /query /status` |
| VMware ESXi | vmtools / host time | vSphere config | `esxcli system time get` |

**VMware time sync rules:**

| Scenario | Recommendation |
|---|---|
| VM with VMware Tools | Disable NTP in guest; use host time sync via VMware Tools OR use external NTP — not both |
| ESXi host | Sync to external NTP servers; disable VMware Tools time sync in guest VMs that have their own NTP |
| Domain controllers (VM) | Use external NTP; disable VMware Tools time sync; PDC emulator syncs to external source |

## Common Commands / Config

```bash
# chrony: Show current sync status (offset, stratum, reference)
chronyc tracking

# chrony: Show all configured sources and their state
chronyc sources -v

# chrony: Show source statistics (jitter, drift)
chronyc sourcestats

# chrony: Force immediate time sync
chronyc makestep

# systemd-timesyncd / timedatectl: Check sync status
timedatectl status
timedatectl show-timesync --all

# ntpd: Show configured peers and sync status
ntpq -p

# ntpd: Force time sync (step mode)
ntpd -gq

# Windows: Check time sync status
w32tm /query /status

# Windows: Show configured NTP source
w32tm /query /source

# Windows: Resync time immediately
w32tm /resync /force

# Windows: Configure NTP server (run as admin)
w32tm /config /manualpeerlist:"pool.ntp.org" /syncfromflags:manual /reliable:yes /update

# VMware: Check ESXi time sync
esxcli system time get
esxcli network firewall ruleset list | grep ntpClient
```


```text title="Expected output"
Reference ID    : C0A80101 (192.168.1.1)
Stratum         : 2
Ref time (UTC)  : Fri Nov 17 14:32:45 2023
System time     : 0.000234567 seconds fast of NTP time
Latest offset   : +0.000145 seconds
RMS offset      : 0.000089 seconds
Frequency       : -12.456 ppm fast
Residual freq   : +0.002 ppm
Skew            : 0.156 ppm
Root delay      : 0.031250 seconds
Root dispersion : 0.005371 seconds
Update interval : 64.8 seconds
Leap status     : Normal

MS Name/IP Address         Stratum Poll Reach LastRx Last sample
===============================================================
^* 192.168.1.1              1      6   377    12   -234us[ -198us] +/-   15ms
^- 10.0.0.5                 2      6   377    45   +1.2ms[+1.3ms] +/-   32ms
^? 203.0.113.42             0      -     0     -     +0ns[   +0ns] +/-    0ns
^x 198.51.100.8             3      6   377   128   +8.5ms[+8.6ms] +/-   48ms

Name/IP Address            NP  NR  Span  Frequency  Freq Skew  Offset  Std Dev
==============================================================================
192.168.1.1                64  62  4096  -12.456    0.234     -198us   145us
10.0.0.5                   64  61  4096   +5.123    0.567     +1.2ms   234us

200 OK
               remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ntp.ubuntu.com  .GPS.            1 u   64   64  377    8.234   -0.234   0.145
+time.google.com .GOOG.           1 u  128  128  377   12.567   +0.456   0.289
-ntp.nist.gov    .NIST.           1 u  256  256  377   45.123   +2.134   1.234

                      Local time: Fri 2023-11-17 14:32:45 UTC
                  Universal time: Fri 2023-11-17 14:32:45 UTC
                        RTC time: Fri 2023-11-17 14:32:45
                       Time zone: UTC (UTC, +0000)
       System clock synchronized: yes
systemd-timesyncd.service active: yes
                 RTC in local TZ: no

       Server: 91.189.89.199 (ntp.ubuntu.com)
Poll interval: 34min 8s (min: 32s; max 34min 8s)
         Leap: normal
      Version: 4
      Stratum: 1
    Reference: GPS
    Precision: 1us
Root distance: 8.234ms
       Offset: -0.234ms
Frequency: -12.456ppm

Stratum :
```
**chrony configuration example (/etc/chrony.conf):**
```bash
# Use regional NTP pool
pool 2.pool.ntp.org iburst maxsources 4

# Allow local subnet to use this server as NTP source
allow 192.168.0.0/16

# Serve time even when not sync'd (for local clients)
local stratum 10

# Log measurements
logdir /var/log/chrony
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`chrony: /etc/chrony/chrony.conf:1: Unknown command 'pool'`** — Ensure you are editing the correct chrony configuration file (/etc/chrony/chrony.conf) and not ntpd's ntp.conf, as syntax differs between the two daemons.
    **`chrony: /var/log/chrony: Permission denied`** — Create the logdir with appropriate permissions using `mkdir -p /var/log/chrony && chown chrony:chrony /var/log/chrony && chmod 755 /var/log/chrony` before restarting chronyd.
## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Kerberos authentication failing | Clock skew > 5 minutes | Run `chronyc makestep` or `w32tm /resync /force`; verify NTP source is reachable |
| `chronyc tracking` shows large offset | NTP source unreachable; firewall blocking 123/udp | Test with `ntpdate -d <ntp-server>`; open 123/udp outbound; check `chronyc sources` for unreachable peers |
| Stratum 16 (unsynchronised) | No reachable NTP sources; all sources marked falseticker | Verify at least 3 sources configured; check network path to NTP servers; `chronyc sources -v` for per-source state |
| Time jumps backwards in VM | VMware Tools + guest NTP both active | Disable one: either turn off VMware Tools time sync (`vmware-toolsd --cmd "vmx.set_option synctime 0"`) or remove NTP from guest |
| w32tm shows wrong source | PDC emulator not syncing externally | On PDC: `w32tm /config /manualpeerlist:"<ntp-server>" /syncfromflags:manual`; other DCs sync from PDC |
| NTP drift increasing over time | Large drift file; hardware clock issues | Check `/var/lib/chrony/drift`; if drift > 1000 ppm, hardware clock may be failing; consider virtual hardware clock tuning |
