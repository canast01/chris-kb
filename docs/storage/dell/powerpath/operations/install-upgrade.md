---
title: PowerPath — Install & Upgrade
tags:
  - dell
  - operations
---

# PowerPath — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering Version and Release Matrix, Upgrade and Update Paths, EOL and Renewal Tracking, Replacement and Decommission Planning.

*Applies to: PowerPath*
</div>
```text
┌──────────────────────────────── Dell PowerPath — Install and Upgrade ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerPath installation and upgrade: deployment and version management procedures       │   │
│   │         Pre-upgrade: back up configuration, check compatibility, review release notes         │   │
│   │      Upgrade: rolling upgrade preserves service; non-disruptive on dual-controller arrays     │   │
│   │           Post-upgrade: verify all services running; run health check; notify users           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Plan → backup config → upgrade staging → upgrade production → validate                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Driver           │  │        powermt daemon       │  │           OS-level          │   │
│   │            Paths            │  │        Active-active        │  │         ≥4 paths/LUN        │   │
│   │            Policy           │  │        Adaptive/ALUA        │  │        Array-specific       │   │
│   │           Failover          │  │         Auto reroute        │  │          <5 sec RTO         │   │
│   │          Management         │  │           pp_mgmt           │  │         Centralised         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Command      │      Notes       │    Frequency     │   │
│   │ powermt display  │ Show path state  │  powermt display  │   Active/dead    │   Daily check    │   │
│   │  powermt check   │  Refresh paths   │   powermt check   │  After changes   │   Post-zoning    │   │
│   │  powermt config  │  Apply license   │  powermt config l │     Per host     │   Install time   │   │
│   │     pp_mgmt      │ Central monitor  │       Web UI      │     Optional     │    Multi-host    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Host OS (Windows/Linux) · HBA or iSCSI NIC ports · FC/IP switches · Dell arrays          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerPath          = Dell multipath driver; manages multiple I/O paths to storage for HA/perform...│
│    powermt            = CLI utility; powermt display, powermt check, powermt save are core commands   │
│    Pseudo device      = virtual block device created by PowerPath aggregating physical I/O paths      │
│    Path health        = alive or dead status per path; dead paths trigger automatic I/O failover      │
│    Adaptive policy    = load-balancing that distributes I/O across all active paths evenly            │
│    CLARiiON policy    = active/passive policy for older VNX/CLARiiON arrays (one active path)         │
│    ALUA               = Asymmetric Logical Unit Access; array signals preferred vs. non-preferred p...│
│    Trespass           = LUN ownership movement between SP-A and SP-B on Unity or VNX arrays           │
│    Ghost path         = stale path entry in PowerPath no longer backed by a physical device           │
│    powermt check      = validates all paths and refreshes device table; run after fabric changes      │
│    pp_mgmt            = PowerPath Management Appliance; central monitoring for all PowerPath hosts    │
│    License key        = host-based license required per server; applied via powermt config license    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Version and Release Matrix

| PowerPath Version | Supported Platforms | Key Changes | Support Status |
|---|---|---|---|
| PowerPath 6.2.x | RHEL 7/8, SLES 12/15, Windows Server 2016/2019, AIX 7.1/7.2 | Kernel 4.x support, RHEL 8 GA | End of Life |
| PowerPath 6.3.x | RHEL 7/8/9, SLES 12/15, Windows Server 2019/2022 | RHEL 9 support, NVMe/FC | Active |
| PowerPath 6.4.x | RHEL 8/9, SLES 15, Windows Server 2022, AIX 7.2/7.3 | RHEL 9.x kernels, extended NVMe-oF | Active (Current) |

Always verify the specific OS and kernel version against the Dell PowerPath E-Lab Interoperability Navigator before upgrading the host OS or PowerPath. Support matrix is at: [https://elabnavigator.dell.com](https://elabnavigator.dell.com)

## Upgrade and Update Paths

PowerPath upgrades on Linux require stopping applications or quiescing I/O if the kernel module must be reloaded (check the release notes for the target version).

**Pre-upgrade steps:**
1. Run `powermt display dev=all > pre-upgrade-baseline.txt` and save
2. Run `powermt display options > pre-upgrade-options.txt` and save
3. Run `powermt save` to persist current configuration
4. Verify the target PowerPath version supports the current OS and kernel: check E-Lab Navigator
5. Check array firmware is within the supported range for the target PowerPath version

**Upgrade procedure (Linux RPM):**
```bash
# Check current version
powermt version

# Install new package (non-disruptive if no kernel module reload required)
rpm -Uvh PowerPath-<version>-<platform>.rpm

# After installation, verify registration
powermt check_registration

# Verify path state
powermt display dev=all
```

**Post-upgrade validation:** Compare path count and policy output against pre-upgrade baseline; run `powermt restore` if any paths show `dead`.

## EOL and Renewal Tracking

| Tracked Item | Where to Find | Action Trigger |
|---|---|---|
| PowerPath version EOS date | Dell Product Support Lifecycle page | Begin upgrade planning 6 months before EOS |
| OS kernel compatibility | E-Lab Interoperability Navigator | Check before any OS kernel update |
| PowerPath license expiry | `powermt check_registration` output | Renew with Dell account team before expiry |
| Support contract (covers PowerPath) | Dell Support portal → Contracts | Renew 90 days before expiry |

## Replacement and Decommission Planning

- PowerPath does not run on dedicated hardware; it is a host-side software component — "replacement" means version upgrades or platform migration
- When migrating a host from PowerPath to native DM-Multipath (Linux), the transition requires stopping I/O to all affected devices, removing PowerPath, configuring DM-Multipath, and validating device access — plan this as a maintenance window event
- When decommissioning a host, remove LUN masking at the array before removing PowerPath to avoid orphaned device entries
- When upgrading the underlying array (e.g., PowerMax to a new model), verify the new array model is in the PowerPath support matrix; some array firmware versions require a corresponding PowerPath update

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Powerpath — Procedures](procedures/)
- [Powerpath — Health Checks](health-checks/)
