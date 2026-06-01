# PowerPath — Standards


<div class="kb-summary">
Standards reference covering Naming Conventions, Sizing and Path Count Model, Build and Deployment Baseline, Configuration Checklist.
</div>

```
┌──────────────────────────── Dell PowerPath Architecture Design Standards ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Design standards: minimum 2 HBAs per host on separate fabrics; 4+ paths per LUN for HA    │   │
│   │     Policy: CLAROpt for Unity/VNX; Optimized for PowerMax; Adaptive for mixed environments    │   │
│   │    Path count rule: 4 paths minimum (2 per fabric); 8 paths for business-critical workloads   │   │
│   │          Mandatory: powermt save after config; failover test per LUN after deployment         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    HBA sizing → SAN zoning → PowerPath install → policy set → save config → failover test             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Path Standards       │  │       Policy Standards      │  │      Testing Standards      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       2+ HBAs per host      │  │      Match array class      │  │        Fail each path       │   │
│   │       Separate fabrics      │  │       CLAROpt → Unity       │  │       Verify I/O cont.      │   │
│   │       4 paths minimum       │  │       Optimized → PMAX      │  │       Confirm recovery      │   │
│   │      8 paths for crit.      │  │       Adaptive → mixed      │  │       powermt save req      │   │
│   │       No single fabric      │  │       Per-LUN override      │  │        Annual retest        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Design verified → failover test every path → powermt save → document path topology                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Standard     │     Minimum      │    Recommended    │   Anti-pattern   │       Risk       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │       HBAs       │    2 per host    │     4 per host    │    1 HBA only    │Single point fail │   │
│   │      Paths       │    4 per LUN     │     8 per LUN     │  2 same fabric   │   Fabric SPOF    │   │
│   │      Policy      │  Array-matched   │    Per workload   │    Basic all     │  No LB benefit   │   │
│   │     Failover     │  Test all paths  │   Quarterly test  │   No test done   │Untested failover │   │
│                                                                                                       │
│    Physical: dual-fabric SAN (A+B fabric); HBA 0 → Fabric A; HBA 1 → Fabric B per host                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SPOF           = Single Point of Failure; eliminated by dual HBA / dual fabric design              │
│    CLAROpt policy = Optimal for CLARiiON-class arrays (Unity, VNX); array-aware balancing             │
│    Optimized policy= Best for PowerMax; uses array preferred path information for I/O routing         │
│    Adaptive policy = Generic round-robin; suitable when array class is mixed or unknown               │
│    Per-LUN override= Set different policy on a specific device: powermt set policy=X dev=hdisk2       │
│    Fabric A/B     = Two independent FC fabrics; host HBAs split across both for redundancy            │
│    Path failover  = Automatic reroute of I/O when path goes down; no manual intervention needed       │
│    powermt save   = Writes current config to /etc/powermt.custom; survives reboot if used             │
│    Dead path poll = PowerPath probes dead paths at configurable interval to detect recovery           │
│    4-path rule    = Ensures one path loss from each fabric still leaves 2 active paths per LUN        │
│    Annual retest  = Periodic failover test to confirm path recovery still works in production         │
│    No single fabric= Both fabrics must carry paths; single-fabric design fails on ISL outage          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────── Dell PowerPath Architecture Design Standards ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Design standards: minimum 2 HBAs per host on separate fabrics; 4+ paths per LUN for HA    │   │
│   │     Policy: CLAROpt for Unity/VNX; Optimized for PowerMax; Adaptive for mixed environments    │   │
│   │    Path count rule: 4 paths minimum (2 per fabric); 8 paths for business-critical workloads   │   │
│   │          Mandatory: powermt save after config; failover test per LUN after deployment         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    HBA sizing → SAN zoning → PowerPath install → policy set → save config → failover test             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Path Standards       │  │       Policy Standards      │  │      Testing Standards      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       2+ HBAs per host      │  │      Match array class      │  │        Fail each path       │   │
│   │       Separate fabrics      │  │       CLAROpt → Unity       │  │       Verify I/O cont.      │   │
│   │       4 paths minimum       │  │       Optimized → PMAX      │  │       Confirm recovery      │   │
│   │      8 paths for crit.      │  │       Adaptive → mixed      │  │       powermt save req      │   │
│   │       No single fabric      │  │       Per-LUN override      │  │        Annual retest        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Design verified → failover test every path → powermt save → document path topology                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Standard     │     Minimum      │    Recommended    │   Anti-pattern   │       Risk       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │       HBAs       │    2 per host    │     4 per host    │    1 HBA only    │Single point fail │   │
│   │      Paths       │    4 per LUN     │     8 per LUN     │  2 same fabric   │   Fabric SPOF    │   │
│   │      Policy      │  Array-matched   │    Per workload   │    Basic all     │  No LB benefit   │   │
│   │     Failover     │  Test all paths  │   Quarterly test  │   No test done   │Untested failover │   │
│                                                                                                       │
│    Physical: dual-fabric SAN (A+B fabric); HBA 0 → Fabric A; HBA 1 → Fabric B per host                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SPOF           = Single Point of Failure; eliminated by dual HBA / dual fabric design              │
│    CLAROpt policy = Optimal for CLARiiON-class arrays (Unity, VNX); array-aware balancing             │
│    Optimized policy= Best for PowerMax; uses array preferred path information for I/O routing         │
│    Adaptive policy = Generic round-robin; suitable when array class is mixed or unknown               │
│    Per-LUN override= Set different policy on a specific device: powermt set policy=X dev=hdisk2       │
│    Fabric A/B     = Two independent FC fabrics; host HBAs split across both for redundancy            │
│    Path failover  = Automatic reroute of I/O when path goes down; no manual intervention needed       │
│    powermt save   = Writes current config to /etc/powermt.custom; survives reboot if used             │
│    Dead path poll = PowerPath probes dead paths at configurable interval to detect recovery           │
│    4-path rule    = Ensures one path loss from each fabric still leaves 2 active paths per LUN        │
│    Annual retest  = Periodic failover test to confirm path recovery still works in production         │
│    No single fabric= Both fabrics must carry paths; single-fabric design fails on ISL outage          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| PowerPath pseudo device (Linux) | Auto-assigned by PowerPath: `/dev/emcpower<letter>` | `/dev/emcpowera`, `/dev/emcpowerb` |
| PowerPath pseudo device (Windows) | Appears as a standard disk in Disk Management; label by LUN purpose | `DATA01`, `LOG01` |
| Path policy alias | Reference policy by name in documentation: `CLAROpt`, `RoundRobin`, `BasicFailover` | `CLAROpt` |
| Baseline file | `<hostname>-powermt-baseline-<YYYY-MM-DD>.txt` | `lon01-db01-powermt-baseline-2025-01-15.txt` |
| License registration key file | `powerpath-<hostname>-<YYYY>.reg` | `powerpath-lon01-db01-2025.reg` |

## Sizing and Path Count Model

PowerPath does not consume significant CPU or memory — it is a kernel module. The key sizing consideration is path count per host:

| Parameter | Guideline |
|---|---|
| Minimum paths per LUN | 2 (one per fabric / HBA) for redundancy |
| Recommended paths per LUN | 4 (two fabrics × two HBA ports per fabric) |
| Maximum paths per LUN | 32 (PowerPath supports up to 32 paths per pseudo device) |
| Baseline documentation | Record expected path count per device per host; compare after every fabric change |

A host with 2 dual-port HBAs connected to 2 storage ports per fabric typically has 4 paths per LUN. Confirm the expected count matches the array LUN masking configuration.

## Build and Deployment Baseline

- Verify OS and kernel version against the Dell PowerPath support matrix before installation; do not install an unsupported combination
- Install PowerPath before connecting additional HBA paths — installing with all paths present avoids a `powermt config` re-run
- Use the CLAROpt policy for all Dell/EMC arrays; set and persist immediately after installation: `powermt set policy=CLAROpt class=all && powermt save`
- Disable DM-Multipath (Linux `multipathd`) for all devices that will be managed by PowerPath — running both on the same device causes I/O corruption
- On Linux, add a `blacklist` entry in `/etc/multipath.conf` for all Dell/EMC array WWIDs to prevent DM-Multipath from claiming those devices
- Run `powermt check_registration` immediately after installation to confirm the license is valid
- Capture and store the baseline path count: `powermt display dev=all > <hostname>-powermt-baseline-<date>.txt`
- Confirm `powermt save` is run after all initial configuration; verify the configuration persists after a test reboot

## Configuration Checklist

- [ ] Dell PowerPath support matrix confirmed for OS version and kernel version
- [ ] DM-Multipath blacklisted for all Dell/EMC array devices (Linux only)
- [ ] PowerPath installed and `powermt version` returns the expected version
- [ ] License applied and `powermt check_registration` shows valid registration
- [ ] `powermt config` run after installation; all expected pseudo devices visible
- [ ] Load balancing policy set to CLAROpt: `powermt display options` confirms `policy=co`
- [ ] `powermt save` run to persist configuration
- [ ] Baseline path count per device captured and stored in the runbook
- [ ] All paths show `alive` in `powermt display dev=all`
- [ ] `powermt display ports class=all` shows all HBA ports `alive`
- [ ] Post-reboot validation: reboot the host and confirm path count and policy are intact
- [ ] Monitoring configured: script or tool alerting on `dead` or `unlic` paths
