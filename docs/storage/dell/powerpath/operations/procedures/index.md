---
tags:
  - dell
  - operations
---
# PowerPath — Procedures


<div class="kb-summary">
Procedures reference covering Change Readiness, Maintenance Window, Post-Change Validation.
</div>

```text
┌──────────────────────────────── Dell PowerPath Operational Procedures ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Standard procedures: install, upgrade, policy change, decommission, path failover test    │   │
│   │      Install: kernel driver + powermt registration key; reboot required on Linux/Windows      │   │
│   │     Upgrade: uninstall old version → install new → re-register → powermt restore → verify     │   │
│   │       Decommission: powermt remove dev=X → unmap LUN from array → verify no ghost paths       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Pre-check path count → execute procedure → powermt display → powermt save → sign-off               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Install Steps        │  │        Policy Change        │  │         Decommission        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       Install package       │  │        Check current        │  │          Drain I/O          │   │
│   │       Register license      │  │        Set new policy       │  │        powermt remove       │   │
│   │         Reboot host         │  │         powermt save        │  │        Unmap at array       │   │
│   │       powermt restore       │  │        Verify balance       │  │        Verify ghost=0       │   │
│   │      Verify path count      │  │        Failover test        │  │         Update CMDB         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Procedure complete → powermt display dev=all → confirm all paths alive → save and document         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │    Procedure     │     Duration     │   Reboot needed   │     Rollback     │       Risk       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     Install      │      30 min      │  Yes (Linux/Win)  │  Uninstall pkg   │    I/O pause     │   │
│   │     Upgrade      │      45 min      │        Yes        │  Re-install old  │  I/O disruption  │   │
│   │  Policy change   │      5 min       │         No        │ powermt set old  │  Rebalance lag   │   │
│   │   Decommission   │      15 min      │         No        │    Re-map LUN    │   Ghost paths    │   │
│                                                                                                       │
│    Physical: package installed on host OS; kernel module loaded; no network required for config       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    powermt remove = Remove a device from PowerPath management; stops multipath tracking for LUN       │
│    Ghost path     = Stale path entry after LUN unmapped; appears as Dead in powermt output            │
│    powermt restore= Re-apply /etc/powermt.custom after reboot; part of standard boot sequence         │
│    Drain I/O      = Gracefully stop application I/O before decommissioning a path or LUN              │
│    CMDB           = Configuration Management Database; record device removal for asset tracking       │
│    Kernel module  = PowerPath loads as a kernel driver; requires compatible kernel version            │
│    Rebalance lag  = Brief period after policy change while I/O re-distributes to new path order       │
│    Failover test  = Manually disable a path and verify I/O continues on remaining paths               │
│    Sign-off       = Post-procedure verification step; document path count and policy in record        │
│    Uninstall pkg  = Remove PowerPath package (rpm -e / dpkg -r / msiexec /x) then reinstall old       │
│    Re-register    = After upgrade, re-run powermt check_registration with existing license key        │
│    Ghost=0        = Confirmation that no stale path entries remain after LUN decommission             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Change Readiness

Verify these items before performing any SAN fabric maintenance, array-side masking change, or PowerPath upgrade on a host.

- [ ] `powermt display dev=all` confirms all paths are alive and path count matches the site baseline — do not start a SAN change with dead paths already present
- [ ] Save current PowerPath configuration before any change: `powermt save` — this persists the policy and path state so it can be reviewed or restored if the change causes issues
- [ ] `powermt check_registration` confirms the license is valid — an expired license will degrade paths to `unlic` state after a reboot
- [ ] Confirm the expected post-change path count per device — for a single SAN port maintenance event, each device should retain at least half its paths
- [ ] If this is a PowerPath version upgrade: confirm OS and kernel version compatibility against the Dell PowerPath support matrix before installing
- [ ] Quiesce or verify host I/O is healthy before the change — confirm the application is not in a high-latency state that would be worsened by temporarily reduced path count
- [ ] Notify the application team that SAN maintenance will temporarily reduce available paths; confirm their application can tolerate this
- [ ] Document the current `powermt display dev=all` output as the pre-change baseline for post-change comparison

| Item | Status | Notes |
|---|---|---|
| All paths alive, count matches baseline | | |
| powermt save completed | | |
| License valid (check_registration) | | |
| Post-change minimum path count acceptable | | |
| OS/kernel compatibility verified (if upgrade) | | |

## Maintenance Window

Steps for SAN port or fabric maintenance that will temporarily reduce the active path count on PowerPath hosts.

1. Identify all hosts with paths through the port or fabric component being maintained — run `powermt display dev=all` on each host and record the pre-change path count per device
2. Run `powermt save` on each affected host to persist the current policy and path configuration
3. Confirm each device will retain at least half its active paths during the maintenance — do not proceed if a device would drop to a single path or zero paths
4. Notify application owners that path count will be temporarily reduced; confirm applications can tolerate the reduced redundancy
5. Remove or disable the target SAN port or fabric component per the approved runbook
6. On affected hosts, run `powermt display dev=all` to confirm remaining paths are alive and I/O is continuing via the surviving paths
7. Complete the maintenance on the SAN port or fabric component; restore the port to service
8. Run `powermt restore` on each affected host to bring the returned paths back online, then run `powermt display dev=all` to confirm the original path count has been restored

## Post-Change Validation

Run these checks after any SAN, fabric, or PowerPath change to confirm multipath health is fully restored.

- [ ] `powermt display dev=all` — all paths are alive and path count per device matches the pre-change baseline; no dead paths remain
- [ ] `powermt display ports class=all` — all HBA ports show `alive`; no ports stuck in `dead` state
- [ ] `powermt display options` — Policy is `CLAROpt` for all device classes; no policy drift occurred during the change
- [ ] `powermt check_registration` — license remains valid post-change
- [ ] No path flap entries in host OS logs in the 30 minutes following the maintenance window
- [ ] Application owners confirm I/O has resumed normally and no elevated latency is observed
- [ ] `powermt save` run after the change to persist the restored configuration state

---

## Verify All Paths Are Active

```bash
# Display all PowerPath-managed devices and path states
powermt display dev=all
```

Check that every path for every device shows `alive`. The path count per device should match the site baseline (typically 4 or 8 paths for dual-fabric FC environments). Any path showing `dead` or `unlic` requires investigation before proceeding with changes.

## Restore Dead Paths

```bash
# Attempt to restore all dead paths
powermt restore dev=all

# Re-check path state after restore
powermt display dev=all
```

If paths remain `dead` after `powermt restore`, investigate the underlying cause: check SAN switch port state, array-side masking, and HBA port state on the host. Dead paths that do not recover after restore indicate a connectivity or zoning issue that must be resolved before the host is considered fully healthy.

## Change Load Balancing Policy

```bash
# Apply ServiceTime policy to all devices (recommended for most arrays)
powermt set policy=ServiceTime dev=all

# Other supported policies:
# powermt set policy=CLARiiON dev=all      (legacy optimised round-robin)
# powermt set policy=LeastBlocks dev=all   (routes to path with fewest pending blocks)
# powermt set policy=RoundRobin dev=all    (distributes I/O evenly across all paths)

# Save the new policy so it persists across reboots
powermt save
```

After changing the policy, monitor `powermt display dev=all` for a few minutes to confirm I/O is distributing across paths as expected. A brief rebalance lag is normal.

## Save Current PowerPath Configuration

```bash
# Save current path configuration and policy to disk
powermt save
```

Run `powermt save` after any path change, policy change, or new LUN discovery to ensure the configuration persists across reboots. The saved configuration is written to `/etc/powermt.custom` (Linux) and is automatically loaded at boot by `powermt restore`.

## Remove a Dead Device Entry

```bash
# Remove a stale PowerPath device entry (use after LUN has been unmapped at the array)
powermt remove dev=<device-id>

# Verify the device no longer appears in the device list
powermt display dev=all
```

Only run `powermt remove` after the LUN has been unmapped from the host at the array side. Removing an active device will cause I/O failures. After removal, run `powermt save` to persist the updated device list.

## Update PowerPath After Adding New LUNs

```bash
# Discover newly zoned or mapped LUNs
powermt config

# Verify new devices appear in the device list with all expected paths
powermt display dev=all
```

Run `powermt config` after new LUNs have been zoned and masked to the host at the array. New devices will appear in `powermt display dev=all` output with the configured load-balancing policy applied automatically. Run `powermt save` after discovery to persist the updated configuration.
