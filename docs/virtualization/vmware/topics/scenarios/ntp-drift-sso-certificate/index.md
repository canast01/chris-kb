# NTP Drift Causing SSO or Certificate Errors

<div class="kb-summary">
Time synchronisation failures across VMware products cause a cascade of symptoms: SSO login failures,
SSL handshake errors, vCenter showing hosts as "Not Responding", and vSAN health warnings. This scenario
covers identifying which components have drifted, correcting NTP on ESXi hosts, VCSA, and NSX Manager,
and recovering SSO and certificate services after time is fixed.
</div>

```text
┌──────────────────────────── NTP Drift — Investigation and Remediation Flow ─────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│   │  SYMPTOM: SSO login fails / "token expired" / SSL error / host "Not Responding" / vSAN skew    │  │
│   └──────────────────────────────────────────┬──────────────────────────────────────────────────────┘ │
│                                              │                                                        │
│              ┌───────────────────────────────┼───────────────────────────────┐                        │
│              ▼                               ▼                               ▼                        │
│   ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐               │
│   │ Check VCSA time     │        │ Check ESXi hosts    │        │ Check NSX Manager   │               │
│   │ timedatectl         │        │ ntpq -p (offset)    │        │ get system clock    │               │
│   │ chronyc tracking    │        │ date vs vCenter     │        │ get ntp-server      │               │
│   └────────┬────────────┘        └────────┬────────────┘        └─────────┬───────────┘               │
│            │                              │                               │                           │
│            ▼                              ▼                               ▼                           │
│   ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐               │
│   │ Fix VCSA NTP →      │        │ Fix ESXi NTP →      │        │ Fix NSX NTP →       │               │
│   │ chronyc makestep    │        │ ntpdate force sync  │        │ set ntp-server +    │               │
│   │                     │        │                     │        │ restart ntp svc     │               │
│   └────────┬────────────┘        └────────┬────────────┘        └─────────────────────┘               │
│            │                              │                                                           │
│            └──────────────────────────────▼──────────────────────────────────────────────────────────┐│
│                                           │  All components synced?                                   ││
│                                           ▼                                                           ││
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ ││
│   │  Restart vmware-stsd (SSO) if token errors persist; re-run vSAN health check for time skew     │ ││
│   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ ││
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
 └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

Every VMware product validates time before accepting connections. The three mechanisms that break
with time drift are:

| Mechanism | Time dependency | Symptom of drift |
|---|---|---|
| SSO tokens (SAML) | Token validity window is clock-based | "Token expired" at login even with correct credentials |
| TLS certificates | notBefore / notAfter fields are clock-checked | SSL handshake failure; "certificate not yet valid" |
| vSAN component heartbeats | Reconciliation uses timestamps | vSAN health "time divergence" warning; resync anomalies |

All products must agree on time within approximately 60 seconds of each other and of a common NTP
reference. The 60-second threshold comes from the SAML token validity window used by SSO.

---

## 2. Check Time on vCenter VCSA

SSH to the VCSA and check current time status:

```bash
timedatectl status
chronyc tracking
```

The `chronyc tracking` output shows:

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

A System time offset beyond ±60 seconds indicates a problem. An offset beyond ±300 seconds means chrony
will not correct automatically and `chronyc makestep` is required.

---

## 3. Check Time on ESXi Hosts

Check each ESXi host that vCenter reports as "Not Responding" or that shows vSAN time warnings:

```bash
esxcli system ntp get
ntpq -p
date
```

The `ntpq -p` output shows one line per NTP peer. The `offset` column is in milliseconds:

```text
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ntp1.domain.loca .GPS.            1 u   45   64  377    0.832   -0.245   0.187
+ntp2.domain.loca .GPS.            1 u   47   64  377    1.123    0.398   0.211
```

An offset beyond ±60,000 ms (60 seconds) in the offset column is the threshold for vCenter
disconnection. The `*` prefix marks the currently selected NTP peer.

---

## 4. Check Time on NSX Manager

SSH to NSX Manager (admin credentials) and check current time and NTP configuration:

```bash
get system clock
get ntp-server
```

Verify the NTP servers listed match the environment's authoritative NTP sources and that the system
clock output matches vCenter time.

---

## 5. Fix NTP on ESXi Hosts

If an ESXi host has drifted or has no NTP configured:

```bash
esxcli system ntp set --enabled false
esxcli system ntp set --server ntp1.domain.local --server ntp2.domain.local
esxcli system ntp set --enabled true
```

Force an immediate time synchronisation instead of waiting for gradual drift correction:

```bash
ntpdate -u ntp1.domain.local
```

Confirm the fix:

```bash
ntpq -p
date
```

Repeat for every ESXi host in the cluster. NTP configuration must be applied to each host individually
unless a Host Profile enforces NTP settings cluster-wide.

---

## 6. Fix NTP on VCSA

Configure NTP via VAMI (`https://vcenter-fqdn:5480` → **Time → Edit NTP Servers**) for a persistent
configuration that survives appliance reboots.

To fix via SSH immediately:

```bash
timedatectl set-ntp true
chronyc makestep
```

`chronyc makestep` forces an immediate step adjustment to the correct time, bypassing the gradual
slew correction that chrony normally applies. Without this, a large drift can take minutes or hours
to correct naturally — during which SSL failures continue.

Confirm:

```bash
chronyc tracking
timedatectl status
```

---

## 7. Fix NTP on NSX Manager

SSH to NSX Manager and reconfigure NTP:

```bash
set ntp-server ntp1.domain.local
set ntp-server ntp2.domain.local
```

Force time synchronisation:

```bash
restart service ntpd
```

Verify:

```bash
get system clock
```

---

## 8. Restart SSO After Time Is Fixed

If SSO token errors persist after NTP is corrected, stale tokens in memory remain invalid. Restart
the STS (Security Token Service) component:

```bash
service-control --restart vmware-stsd
```

Wait 60–90 seconds after restart before attempting login. The STS service generates new signing keys
on startup, which invalidates any cached tokens — this is expected behaviour.

---

## 9. Verify vSAN Time Skew Health Check

vSAN's built-in health check detects time skew between cluster members. After fixing NTP on all hosts,
navigate in vCenter to **Cluster → Monitor → vSAN → Skyline Health** and re-run the
**"vSAN cluster member hosts time divergence"** check.

The check passes when all hosts are within ±60 seconds of each other. If a host still fails after NTP
is configured, force a sync on that host:

```bash
ntpdate -u ntp1.domain.local
```

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

- [ESXi Host Disconnected from vCenter](../esxi-host-disconnected/index.md) — NTP drift is one of the
  silent causes of host disconnection covered in Step 7 of that scenario.
- [vCenter Down / Unreachable](../vcenter-down/index.md) — if the VCSA itself has drifted severely,
  vpxd refuses to start and the full vCenter recovery procedure applies.
- [VxRail LCM Upgrade Failure](../vxrail-lcm-upgrade-failure/index.md) — NTP skew is one of the
  pre-check failures that blocks a VxRail LCM upgrade from starting.
