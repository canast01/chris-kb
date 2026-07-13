---
tags:
  - scenarios
  - vmware
description: "Time synchronisation failures across VMware products cause a cascade of symptoms: SSO login failures, SSL handshake errors, vCenter showing hosts as 'Not..."
---
# NTP Drift Causing SSO or Certificate Errors

<div class="kb-summary">
Time synchronisation failures across VMware products cause a cascade of symptoms: SSO login failures,
SSL handshake errors, vCenter showing hosts as "Not Responding", and vSAN health warnings. This scenario
covers identifying which components have drifted, correcting NTP on ESXi hosts, VCSA, and NSX Manager,
and recovering SSO and certificate services after time is fixed.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_understand_why_ntp_matters_in_vmwa: "1. Understand Why NTP Matters in VMware" {shape: rectangle}
2_check_time_on_vcenter_vcsa: "2. Check Time on vCenter VCSA" {shape: rectangle}
3_check_time_on_esxi_hosts: "3. Check Time on ESXi Hosts" {shape: rectangle}
4_check_time_on_nsx_manager: "4. Check Time on NSX Manager" {shape: rectangle}
5_fix_ntp_on_esxi_hosts: "5. Fix NTP on ESXi Hosts" {shape: rectangle}

products_involved -> 1_understand_why_ntp_matters_in_vmwa: uses
1_understand_why_ntp_matters_in_vmwa -> 2_check_time_on_vcenter_vcsa: uses
2_check_time_on_vcenter_vcsa -> 3_check_time_on_esxi_hosts: uses
3_check_time_on_esxi_hosts -> 4_check_time_on_nsx_manager: uses
4_check_time_on_nsx_manager -> 5_fix_ntp_on_esxi_hosts: uses
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| ESXi | NTP client on each host; drift causes disconnection from vCenter and vSAN health warnings |
| vCenter VCSA | NTP client; SSO token validity and TLS certificates are time-bound |
| NSX Manager | NTP client; drift causes control plane instability and API authentication failures |
| Aria Operations | NTP client; metric gaps and false-positive alerts when time diverges from vCenter |
| vSAN | Uses timestamps for component reconciliation; "time divergence" health check flags skew |

---

## 1. Understand Why NTP Matters in VMware

Every VMware product validates time before accepting connections — the 60-second threshold comes from the SAML token validity window used by SSO.

| Mechanism | Time dependency | Symptom of drift |
|---|---|---|
| SSO tokens (SAML) | Token validity window is clock-based | "Token expired" at login even with correct credentials |
| TLS certificates | notBefore / notAfter fields are clock-checked | SSL handshake failure; "certificate not yet valid" |
| vSAN component heartbeats | Reconciliation uses timestamps | vSAN health "time divergence" warning; resync anomalies |

---

## 2. Check Time on vCenter VCSA

SSH to the VCSA and check current synchronisation state.

```bash
timedatectl status
chronyc tracking
```


```text title="Expected output"
Local time: Wed 2024-01-17 14:32:45 UTC
           Universal time: Wed 2024-01-17 14:32:45 UTC
                 RTC time: Wed 2024-01-17 14:32:45
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
           RTC in local TZ: no

Reference ID    : 91F20D03 (ntp.ubuntu.com)
Stratum         : 2
Ref time (UTC)  : Wed Jan 17 14:32:40 2024
System time offset : 0.000234567 seconds
Last update     : 12 seconds ago
RMS offset      : 0.001234 seconds
Frequency       : -2.456 ppm
Residual freq   : +0.002 ppm
Skew            : 0.156 ppm
Root delay      : 0.045678 seconds
Root dispersion : 0.012345 seconds
Update interval : 1024.0 seconds
Leap status     : Normal
```

!!! warning "Common errors"
    **`command not found: timedatectl`** — Install systemd-container or ensure systemd is available on the system.
    **`command not found: chronyc`** — Install chrony package using `apt-get install chrony` or `yum install chrony`.
Expected output:

```text
Reference ID    : 10.0.0.1 (ntp1.domain.local)
Stratum         : 3
System time     : 0.000123456 seconds fast of NTP time
Last offset     : +0.000234567 seconds
RMS offset      : 0.000345678 seconds
Frequency       : 12.345 ppm slow
Residual freq   : -0.001 ppm
Skew            : 0.012 ppm
Root delay      : 0.003456 seconds
Root dispersion : 0.001234 seconds
```

Look for: System time offset beyond ±60 seconds. An offset beyond ±300 seconds means chrony will not self-correct and `chronyc makestep` is required.

---

## 3. Check Time on ESXi Hosts

Check each ESXi host that vCenter reports as "Not Responding" or that shows vSAN time warnings.

```bash
esxcli system ntp get
ntpq -p
date
```


```text title="Expected output"
NTP Enabled: true
NTP Servers: 10.20.30.40, 10.20.30.41
NTP Service Running: true

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 10.20.30.40     129.6.15.28      2 u   64  128  377   12.543    2.341   1.234
 10.20.30.41     129.6.15.29      2 u   32  128  377   11.892   -1.876   0.987
 LOCAL(0)        .LOCL.          10 l  987 1024    1    0.000    0.000   0.001

Thu Oct 12 14:23:47 UTC 2024
```

!!! warning "Common errors"
    **`NTP Enabled: false`** — Enable NTP with `esxcli system ntp set --enabled=true` and start the service with `service ntpd start`.
    **`ntpq: read: Connection refused`** — Start the NTP daemon with `service ntpd start` and verify it is listening on port 123.
    **`Error: Unable to connect to Management Agent`** — Ensure the ESXi host management network is configured and the management vmkernel interface is active with `esxcli network ip interface list`.
Expected `ntpq -p` output:

```text
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ntp1.domain.loca .GPS.            1 u   45   64  377    0.832   -0.245   0.187
+ntp2.domain.loca .GPS.            1 u   47   64  377    1.123    0.398   0.211
```

Look for: offset column beyond ±60,000 ms (60 seconds). The `*` prefix marks the currently selected NTP peer; if no peer has `*`, the host has no active time source.

---

## 4. Check Time on NSX Manager

SSH to NSX Manager (admin credentials) and check current time and NTP configuration.

```bash
get system clock
get ntp-server
```


```text title="Expected output"
System Clock:
  Current Time: 2024-01-15 14:32:47 UTC
  Timezone: UTC
  NTP Synchronized: yes
  Last Sync: 2024-01-15 14:32:15 UTC

NTP Server:
  Primary: ntp.vmware.com (216.239.35.0)
  Secondary: time.google.com (216.239.35.4)
  Tertiary: pool.ntp.org (203.0.113.42)
  Status: synchronized
  Stratum: 2
  Offset: +0.002ms
```

!!! warning "Common errors"
    **`command not found: get`** — Use the correct CLI tool (e.g., `timedatectl` on Linux or `ntpq -p` for NTP queries) or access the management interface with proper credentials.
    **`Permission denied`** — Run the command with appropriate privileges using `sudo` or log in as a user with administrative access to the system.
Look for: system clock time matching vCenter within 60 seconds, and NTP servers matching the environment's authoritative sources.

---

## 5. Fix NTP on ESXi Hosts

Configure NTP and force an immediate sync on each drifted host.

```bash
esxcli system ntp set --enabled false
esxcli system ntp set --server ntp1.domain.local --server ntp2.domain.local
esxcli system ntp set --enabled true
ntpdate -u ntp1.domain.local
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
21 Nov 12:34:56 ntpdate[2048]: adjust time server 10.42.8.15 offset 0.002341 sec
```

!!! warning "Common errors"
    **`ntpdate: no servers can be used, exiting`** — Verify NTP server hostnames resolve correctly with `nslookup ntp1.domain.local` and confirm network connectivity to the NTP servers.
    **`Error: Unknown option or flag '--server'`** — Use `esxcli system ntp set --servers=ntp1.domain.local --servers=ntp2.domain.local` (with `=` syntax) on ESXi 6.5+, or check your ESXi version with `vmware -v`.
Confirm the fix:

```bash
ntpq -p
date
```


```text title="Expected output"
remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ntp.ubuntu.com  17.253.34.125    2 u   64  128  377   45.234   -2.341   1.203
+time.google.com 216.239.35.12    2 u   32  128  377   38.921    1.456   0.892
-ntp.nist.gov    132.163.96.1     2 u  102  128  377   52.103   -5.234   2.145
+pool.ntp.org    203.0.113.45      3 u   48  128  377   61.234    0.789   1.567
Thu Mar 14 09:47:23 UTC 2024
```

!!! warning "Common errors"
    **`ntpq: read: Connection refused`** — Ensure ntpd or systemd-timesyncd is running with `systemctl start ntp` or `systemctl start systemd-timesyncd`.
    **`command not found: ntpq`** — Install ntp utilities with `apt-get install ntp` or `yum install ntp`.
Repeat for every ESXi host in the cluster — NTP must be applied per host unless a Host Profile enforces it cluster-wide.

---

## 6. Fix NTP on VCSA

Configure NTP via VAMI (`https://vcenter-fqdn:5480` → **Time → Edit NTP Servers**) for persistence across reboots.

To fix immediately via SSH:

```bash
timedatectl set-ntp true
chronyc makestep
```


```text title="Expected output"
System clock synchronized.
200 sources online.
Leap status: normal.
```

!!! warning "Common errors"
    **`Failed to set ntp: Permission denied`** — Run the commands with `sudo` or as root user.
    **`chronyd is not running`** — Start the chrony service with `sudo systemctl start chronyd` before running `chronyc makestep`.
`chronyc makestep` forces an immediate step adjustment rather than the gradual slew — without this, SSL failures continue for minutes or hours while drift corrects naturally.

Confirm:

```bash
chronyc tracking
timedatectl status
```


```text title="Expected output"
reference id    : 91.189.89.198 (ntp.ubuntu.com)
stratum         : 2
ref time (UTC)  : Fri Dec 15 14:32:18 2023
system time     : 0.000234567 seconds fast of NTP time
last update     : 42 seconds ago
RMS offset      : 0.001234 seconds
frequency       : -12.345 ppm
residual freq   : +0.123 ppm
skew            : 0.456 ppm
root delay      : 0.045678 seconds
root dispersion : 0.123456 seconds
update interval : 64.0 seconds
leap status     : Normal

               Local time: Fri 2023-12-15 14:32:18 UTC
           Universal time: Fri 2023-12-15 14:32:18 UTC
                 RTC time: Fri 2023-12-15 14:32:18
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
           RTC in local TZ: no
```

!!! warning "Common errors"
    **`chronyc: command not found`** — Install chrony with `apt-get install chrony` or `yum install chrony` depending on your distribution.
    **`System clock synchronized: no`** — Wait for NTP synchronization to complete (typically 1-5 minutes) or check that your NTP server is reachable with `chronyc sources`.
---

## 7. Fix NTP on NSX Manager

SSH to NSX Manager and reconfigure NTP, then force synchronisation.

```bash
set ntp-server ntp1.domain.local
set ntp-server ntp2.domain.local
restart service ntpd
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Unknown command: set`** — Use the correct CLI context (e.g., `configure` mode in vSphere or ESXi) before issuing `set` commands.
    **`Unknown command: restart`** — Use the correct restart syntax for your platform, such as `service ntpd restart` on ESXi or `/etc/init.d/ntpd restart` on Linux.
Verify:

```bash
get system clock
```


```text title="Expected output"
System clock information:
Current time: 2024-01-15 14:32:47 UTC
Hardware clock: 2024-01-15 14:32:45 UTC
Time zone: UTC
NTP status: synchronized
Last NTP sync: 2024-01-15 14:32:10 UTC
Clock source: kvm-clock
Frequency adjustment: +0.000 ppm
```

!!! warning "Common errors"
    **`command not found: get`** — Use the correct system command such as `timedatectl`, `date`, or `hwclock` depending on your OS and what clock information you need.
    **`timedatectl: command not found`** — Install the systemd package or use alternative commands like `date` for software clock or `hwclock` for hardware clock on systems without timedatectl.
Look for: clock time within 60 seconds of vCenter after `ntpd` restarts.

---

## 8. Restart SSO After Time Is Fixed

If SSO token errors persist after NTP is corrected, stale tokens remain invalid until the STS service is restarted.

```bash
service-control --restart vmware-stsd
```


```text title="Expected output"
Stopping VMware Security Token Service...
Waiting for services to stop...
Starting VMware Security Token Service...
VMware Security Token Service started successfully.
```

!!! warning "Common errors"
    **`service-control: command not found`** — Ensure you are running this command on a vCenter Server or ESXi host where VMware tools are installed, or use the full path `/usr/lib/vmware-vmafd/bin/service-control`.
    **`Error: Failed to stop service vmware-stsd`** — Check that the service exists and is running with `service-control --status vmware-stsd`, and verify you have root or sudo privileges.
Wait 60–90 seconds after restart before attempting login — STS generates new signing keys on startup, which invalidates all cached tokens; this is expected behaviour.

---

## 9. Verify vSAN Time Skew Health Check

Re-run the vSAN health check after fixing NTP on all hosts to confirm the cluster is clean.

Navigate in vCenter to **Cluster → Monitor → vSAN → Skyline Health** and re-run the
**"vSAN cluster member hosts time divergence"** check.

If a host still fails after NTP is configured, force a sync:

```bash
ntpdate -u ntp1.domain.local
```


```text title="Expected output"
4 Dec 12:34:56 ntpdate[2847]: adjust time server 192.168.1.50 offset 0.045821 sec
```

!!! warning "Common errors"
    **`ntpdate[2847]: no server suitable for synchronization found`** — Verify the NTP server hostname resolves and is reachable with `ping ntp1.domain.local` and `nc -zv ntp1.domain.local 123`.
    **`ntpdate: command not found`** — Install NTP utilities with `apt-get install ntp` (Debian/Ubuntu) or `yum install ntp` (RHEL/CentOS), or use `chronyc makestep` on systems with chrony instead.
Then re-run the health check from vCenter.

---

## NTP Requirement Reference

| Product | Max Allowed Skew | Consequence of Drift |
|---|---|---|
| ESXi | 60 seconds from vCenter | Host disconnects from vCenter; vpxa SSL failure |
| vCenter VCSA | 60 seconds from all hosts | SSO tokens invalid; hosts show "Not Responding" |
| vSAN | 60 seconds between nodes | Component health warnings; resync anomalies |
| NSX Manager | 60 seconds from controllers | Control plane instability; API auth failures |
| Aria Operations | 60 seconds from vCenter | Metric collection gaps; false-positive alerts |

---

## Key Terms

| Term | Definition |
|---|---|
| NTP | Network Time Protocol — the standard protocol used to synchronise clocks across hosts, appliances, and network devices to a common time source |
| chronyc | Command-line client for the chrony NTP daemon used on the VCSA; `chronyc tracking` shows current offset and `chronyc makestep` forces an immediate clock correction |
| VCSA | vCenter Server Appliance — the Linux-based virtual appliance that runs vCenter; hosts the SSO domain and issues certificates whose validity depends on accurate appliance time |
| timedatectl | Linux systemd utility on the VCSA for displaying and configuring the system clock, NTP status, and timezone |
| SSO | Single Sign-On — VMware's authentication service that issues SAML tokens for all vSphere and NSX logins; token validity is clock-bound, so any time skew invalidates active sessions |
| STS | Security Token Service — the component within SSO (vmware-stsd) that generates and validates SAML tokens; must be restarted after large time corrections to clear stale in-memory token state |
| vmware-stsd | The systemd service name for the VMware Security Token Service on the VCSA; restarting it forces new signing key generation and clears invalid token caches |
| Time skew | The measured difference between a system's local clock and the NTP reference time; skew beyond 60 seconds breaks VMware TLS and SSO validation |
| ntpdate | Command-line tool used on ESXi hosts to force an immediate one-shot time synchronisation, bypassing the gradual correction that the NTP daemon applies |
| NTP stratum | A number indicating how many hops away a time source is from a hardware reference clock; stratum 1 = GPS/atomic clock, stratum 2 = synced to stratum 1; lower stratum = higher accuracy |
| Certificate validity window | The time range between a certificate's notBefore and notAfter fields; if the system clock is outside this window, TLS handshakes fail with "not yet valid" or "expired" errors |
| Aria Operations | VMware's observability and monitoring platform; also an NTP client — if its clock drifts, metric timestamps diverge from vCenter and trigger false-positive connectivity alerts |
| NSX Manager | The NSX control plane appliance that manages overlay networking and security policy; NTP drift on NSX Manager causes API authentication failures and control plane instability |

---

## Common Mistakes

- **Fixing NTP on vCenter but not on ESXi hosts.** vCenter and ESXi must both be synced. Fixing only
  one side does not resolve SSL handshake failures between them.
- **Not running `chronyc makestep` after configuring NTP on VCSA.** Without a forced step, chrony
  corrects large drift gradually over minutes or hours. Errors continue during the slew period.
- **Not restarting SSO after time is fixed.** Stale tokens in the SSO service memory remain invalid
  even after the clock is corrected. Restart `vmware-stsd` to clear them.
- **Applying NTP to only one ESXi host in the cluster.** vSAN time skew is measured between all
  cluster members. All hosts must be synced, not just the one flagged in the initial alert.

---

## Related Scenarios

- [ESXi Host Disconnected from vCenter](esxi-host-disconnected.md) — NTP drift is one of the
  silent causes of host disconnection covered in Step 7 of that scenario.
- [vCenter Down / Unreachable](vcenter-down.md) — if the VCSA itself has drifted severely,
  vpxd refuses to start and the full vCenter recovery procedure applies.
- [VxRail LCM Upgrade Failure](vxrail-lcm-upgrade-failure.md) — NTP skew is one of the
  pre-check failures that blocks a VxRail LCM upgrade from starting.
