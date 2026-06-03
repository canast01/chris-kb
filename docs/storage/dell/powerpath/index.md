# Dell PowerPath

<div class="kb-summary">
Host-based multipath I/O software — automatic path failover, dynamic load balancing, and LUN path management for Dell/EMC arrays across Linux, Windows, AIX, HP-UX, and Solaris.
</div>

```text
┌──────────────────────────────────── Dell PowerPath Multipath I/O ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       PowerPath: Dell host-side multipath driver; load balancing and automatic failover       │   │
│   │         Policies: CLAROpt (adaptive LB), Adaptive (round-robin), Basic (failover-only)        │   │
│   │            Supports: PowerMax, Unity, VNX, XtremIO, ECS; FC, iSCSI, FCoE transports           │   │
│   │              Managed via powermt CLI; PowerPath/VE edition for VMware ESXi hosts              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Host HBAs → multiple FC/iSCSI paths → PowerPath load-balances I/O → array FA ports                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Path Policies        │  │          Operations         │  │       Platform Support      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      CLAROpt (default)      │  │       powermt display       │  │         RHEL / SLES         │   │
│   │         Adaptive LB         │  │       powermt restore       │  │        Windows Server       │   │
│   │        Basic failover       │  │         powermt save        │  │       VMware ESXi /VE       │   │
│   │          Optimized          │  │         powermt set         │  │        AIX / Solaris        │   │
│   │        Per-LUN policy       │  │        powermt check        │  │          Ubuntu LTS         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Path failure detected → I/O rerouted to live paths → dead path polled → re-enabled on recovery     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │      Policy      │   Description    │      Best for     │    Array type    │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     CLAROpt      │  Array-aware LB  │    Unity / VNX    │  CLARiiON-class  │  Default policy  │   │
│   │     Adaptive     │  Round-robin LB  │   Mixed workload  │    All arrays    │ Per-I/O balance  │   │
│   │      Basic       │  Failover only   │    Low I/O apps   │    All arrays    │ One active path  │   │
│   │    Optimized     │  Perf-aware LB   │      PowerMax     │ Symmetrix-class  │ Preferred paths  │   │
│                                                                                                       │
│    Physical: HBA ports in host → FC fabric or iSCSI network → array FA director ports                 │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CLAROpt        = CLARiiON Optimized; array-aware load balancing for Unity/VNX arrays               │
│    powermt        = PowerPath management CLI; primary tool for all path and policy operations         │
│    powermt display= Show all multipath devices, paths, and states on the host                         │
│    powermt restore= Re-apply saved PowerPath configuration after host reboot                          │
│    powermt save   = Persist current path policy and config to disk for restore after reboot           │
│    powermt set    = Set path policy or other parameter: powermt set policy=adaptive dev=all           │
│    Dead path      = Path that failed I/O; PowerPath polls it for recovery every few seconds           │
│    Emulation      = Array class identifier in PowerPath config (emc_symm, emc_clariion, etc.)         │
│    PowerPath/VE   = PowerPath Virtual Edition for VMware ESXi; replaces native NMP PSP                │
│    Registration   = License key bound to host system; verified via powermt check_registration         │
│    Trespass       = Ownership transfer of LUN between array SPs in active/passive arrays              │
│    ALUA           = Asymmetric Logical Unit Access; standard for preferred/non-preferred paths        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>

## Overview

Dell PowerPath is host-based multipath I/O software that manages multiple physical paths between a host and storage arrays from Dell/EMC, providing automatic path failover and dynamic load balancing. It runs on Linux, Windows, AIX, HP-UX, and Solaris, and is controlled via the `powermt` CLI. PowerPath presents a single pseudo device per LUN to the OS, abstracting the underlying physical paths.

## Where It Fits

| Use Case |
|---|
| Hosts connected to Dell/EMC arrays (PowerMax, VMAX, Unity, PowerStore) over Fibre Channel or iSCSI |
| Production environments requiring automatic path failover without host-side intervention |
| Performance-sensitive workloads that benefit from intelligent load balancing across multiple HBA paths |
| Environments with zoning changes or fabric maintenance where path counts change dynamically |
| Any host where native OS multipath (DM-Multipath) is being replaced or supplemented with a vendor-managed solution |

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Run `powermt display dev=all` and scan for paths in `dead` or `unlic` | `powermt display dev=all` |  |
| Verify all pseudo devices show the expected number of active paths |  |  |
| Check that load balancing policy is set to CLAROpt (not RoundRobin or |  |  |
| Confirm `powermt check_registration` shows a valid, non-expired licens | `powermt check_registration` |  |
| Review OS system logs (`/var/log/messages` on Linux) for HBA or path e | `/var/log/messages` |  |
| After any fabric or zoning change, recount paths per device and compar |  |  |
| Verify `powermt display ports class=all` shows all HBA ports in an `al | `powermt display ports class=all` |  |

## Health Commands

```bash
# Display all PowerPath managed devices and their path states
powermt display dev=all

# Display all HBA port states
powermt display ports class=all

# Show current load balancing policy and PowerPath options
powermt display options

# Check PowerPath license registration status
powermt check_registration

# Show installed PowerPath version
powermt version

# Test and restore all paths (marks dead paths for retry)
powermt restore
```

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Path shown as `dead` in `powermt display dev=all` | FC cable/SFP failure, switch port error, or zoning misconfiguration | Check fabric switch logs and HBA port state; run `powermt restore` after fix |
| Devices showing as `pseudo` with no paths | LUN not presented to host, or `powermt config` not run after new LUN mapping | Verify LUN masking at array; run `powermt config` to discover new devices |
| Policy shown as `BasicFailover` instead of CLAROpt | License expired or not properly applied | Run `powermt check_registration`; reapply license and run `powermt config` |
| Path state `unlic` | License missing or configured after LUN was already under PowerPath management | Confirm license with `powermt check_registration`; rerun `powermt config` |
| Path thrashing (intermittent dead/alive cycling) | Flapping SFP, marginal FC cable, or oversubscribed switch port | Inspect physical layer; check switch error counters; replace suspect hardware |
| Configuration lost after reboot | `powermt save` was not run after last policy or path change | Always run `powermt save` after any configuration change to persist settings |

## Operational Tasks

| Task | Command |
|---|---|
| After any LUN is added or removed, run `powermt config` followed by `powermt dis |  |
| Change load balancing policy with `powermt set policy=CLAROpt class=all` and per | `powermt save` |
| After fabric maintenance or zoning changes, run `powermt restore` to bring dead |  |
| Verify path counts per device against site baseline documentation after any SAN |  |
| Check registration and license validity with `powermt check_registration` after |  |
| Use `powermt display dev=<device>` to investigate a specific pseudo device in de |  |
| Decommission a device cleanly by removing LUN masking at the array, then running | `powermt remove dev=<device>` |

## Upgrade Notes

| Step | Action |
|---|---|
| 1 | Record the current state before upgrade: run `powermt display dev=all` and `powermt display options` and save the output |
| 2 | Confirm OS and kernel version compatibility against the Dell PowerPath support matrix for the target version |
| 3 | Run `powermt save` to persist current configuration so it can be restored if the upgrade needs to be rolled back |
| 4 | Stop applications or quiesce I/O if the upgrade requires unloading the PowerPath kernel module (check release notes) |
| 5 | Install the new PowerPath package using the OS package manager (e.g., `rpm -Uvh` on RHEL/SLES) |
| 6 | After installation, run `powermt check_registration` to confirm the license is recognised under the new version |
| 7 | Run `powermt display dev=all` and compare path counts and policy against the pre-upgrade baseline; run `powermt restore` if any paths are in `dead` state |

## Best Practices

| Recommendation | Detail |
|---|---|
| Always use the CLAROpt (`co`) policy for Dell/EMC CLARiiON, Unity, and mid-range arrays | do not use RoundRobin, which ignores array-side optimisation |
| Run `powermt save` immediately after every policy change, | Run `powermt save` immediately after every policy change, path addition, or `powermt config` operation to ensure settings persist across reboots |
| Maintain a documented baseline of expected path counts per host and device | compare after every fabric or zoning change |
| Run `powermt check_registration` after any OS upgrade or | Run `powermt check_registration` after any OS upgrade or kernel update to confirm the license is still valid |
| After any fabric change, run `powermt restore` before checking path state | this instructs PowerPath to retry paths marked dead |
| Do not mix PowerPath and DM-Multipath managing the same devices on the same host | disable DM-Multipath for devices managed by PowerPath |
| Review the Dell PowerPath release notes and support matrix | Review the Dell PowerPath release notes and support matrix before any kernel or OS upgrade to confirm compatibility |
