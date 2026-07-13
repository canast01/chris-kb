---
tags:
  - dell
  - operations
description: "Procedures reference covering Change Readiness, Maintenance Window, Post-Change Validation."
---
# PowerPath — Procedures

<div class="kb-summary">
Procedures reference covering Change Readiness, Maintenance Window, Post-Change Validation.

*Applies to: PowerPath*
</div>

```d2
direction: right

change_readiness: "Change Readiness" {shape: rectangle}
maintenance_window: "Maintenance Window" {shape: rectangle}
postchange_validation: "Post-Change Validation" {shape: rectangle}
verify_all_paths_are_active: "Verify All Paths Are Active" {shape: rectangle}
restore_dead_paths: "Restore Dead Paths" {shape: rectangle}
change_load_balancing_policy: "Change Load Balancing Policy" {shape: rectangle}

change_readiness -> maintenance_window
maintenance_window -> postchange_validation
postchange_validation -> verify_all_paths_are_active
verify_all_paths_are_active -> restore_dead_paths
restore_dead_paths -> change_load_balancing_policy
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

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


```text title="Expected output"
Symmetrix ID: 000297900001
Logical Device ID: 0001
state=alive; policy=SymmOpt; priority=0; owner=SP A
------------ Host ---------------  -- Logical Device --  -- Dev --  --- Host ---
 Initiator Name         Logical ID    LUN    Attr    Ident  Sequence  Flags
c0t5000097000001234d0s2 SP A          0001   RW      on     0         alive
c0t5000097000001235d0s2 SP B          0001   RW      on     1         alive
c0t5000097000001236d0s2 SP A          0001   RW      on     2         alive
c0t5000097000001237d0s2 SP B          0001   RW      on     3         alive

Symmetrix ID: 000297900002
Logical Device ID: 0002
state=alive; policy=SymmOpt; priority=0; owner=SP B
------------ Host ---------------  -- Logical Device --  -- Dev --  --- Host ---
 Initiator Name         Logical ID    LUN    Attr    Ident  Sequence  Flags
c0t5000097000002234d0s2 SP A          0002   RW      on     0         alive
c0t5000097000002235d0s2 SP B          0002   RW      on     1         alive
...
```

!!! warning "Common errors"
    **`powermt: Command not found`** — Install EMC PowerPath software or verify the installation path is in your system's $PATH environment variable.
    **`powermt: insufficient privileges`** — Run the command with sudo or as root user, as PowerPath requires elevated permissions.
    **`No Symmetrix devices found`** — Verify that PowerPath is initialized and storage arrays are properly zoned and discovered by running `powermt config`.
Check that every path for every device shows `alive`. The path count per device should match the site baseline (typically 4 or 8 paths for dual-fabric FC environments). Any path showing `dead` or `unlic` requires investigation before proceeding with changes.

## Restore Dead Paths

```bash
# Attempt to restore all dead paths
powermt restore dev=all

# Re-check path state after restore
powermt display dev=all
```


```text title="Expected output"
Restoring devices...
Device Name             Paths Dead Paths
emc0                    4     0
emc1                    8     2
emc2                    4     0
emc3                    6     1

Device Name             Paths Dead Paths
emc0                    4     0
emc1                    8     0
emc2                    4     0
emc3                    6     0
```

!!! warning "Common errors"
    **`powermt: Command not found`** — Install EMC PowerPath software or verify the installation path is in your $PATH environment variable.
    **`powermt: Permission denied`** — Run the command with sudo or as root user, as PowerPath operations require elevated privileges.
    **`powermt restore: Device emc1 failed - path recovery timeout`** — Check physical SAN connectivity and verify the storage array is online and accessible before retrying the restore.
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


```text title="Expected output"
Symmetrix devices:
  Device Number:  000196701234
    Symmetrix ID:  000000000000001
    Device Type:   VRAID
    Megabytes:     2048000
    SymmWWN:       60000970000001234567890abcdef01
    Policy:        ServiceTime
    
  Device Number:  000196701235
    Symmetrix ID:  000000000000001
    Device Type:   VRAID
    Megabytes:     2048000
    SymmWWN:       60000970000001234567890abcdef02
    Policy:        ServiceTime

2 Symmetrix devices updated with ServiceTime policy.
Saving EMC PowerPath configuration...
Configuration saved successfully to /etc/powerpath/powerpath.conf
```

!!! warning "Common errors"
    **`powermt: Command not found`** — Verify EMC PowerPath is installed with `rpm -qa | grep PowerPath` and ensure `/opt/emc/powerpath/bin` is in your PATH.
    **`powermt: You must be root to run this command`** — Execute the command with `sudo` or switch to root user with `sudo su -`.
    **`powermt set policy=ServiceTime dev=all: No devices found`** — Ensure storage arrays are properly discovered and multipathed by running `powermt display` to verify device visibility.
After changing the policy, monitor `powermt display dev=all` for a few minutes to confirm I/O is distributing across paths as expected. A brief rebalance lag is normal.

## Save Current PowerPath Configuration

```bash
# Save current path configuration and policy to disk
powermt save
```


```text title="Expected output"
PowerPath(R) for Linux Version 6.2.0.0 (build 1234)
Copyright (C) 2023 Dell Inc. All rights reserved.

Saving PowerPath configuration...
Configuration saved to /etc/powerpath/powerpath.conf
Policy saved to /etc/powerpath/powerpath.policy
Timestamp: 2024-01-15 14:32:47 UTC
Save completed successfully.
```

!!! warning "Common errors"
    **`powermt: command not found`** — Install PowerPath software or ensure the powermt binary is in your PATH; verify with `which powermt`.
    **`Permission denied`** — Run the command with sudo or as root since PowerPath configuration files require elevated privileges.
    **`Cannot write to /etc/powerpath/: Read-only file system`** — Remount the filesystem as read-write using `mount -o remount,rw /` or check disk space with `df -h`.
Run `powermt save` after any path change, policy change, or new LUN discovery to ensure the configuration persists across reboots. The saved configuration is written to `/etc/powermt.custom` (Linux) and is automatically loaded at boot by `powermt restore`.

## Remove a Dead Device Entry

```bash
# Remove a stale PowerPath device entry (use after LUN has been unmapped at the array)
powermt remove dev=<device-id>

# Verify the device no longer appears in the device list
powermt display dev=all
```


```text title="Expected output"
Logical device removed successfully.
Device Name            Symmetrix ID     State    Avail  Ckd  Unckd
dev-001                000123456789ABC  OK       Yes    Yes  No
dev-002                000123456789ABC  OK       Yes    Yes  No
dev-004                000123456789ABC  OK       Yes    Yes  No
dev-005                000123456789DEF  OK       Yes    Yes  No
dev-006                000123456789DEF  OK       Yes    Yes  No
```

!!! warning "Common errors"
    **`Device dev-003 is in use by an active I/O path`** — Ensure all applications and mount points using the device are stopped before removal.
    **`powermt: Command not found`** — Install EMC PowerPath or add its bin directory to your PATH environment variable.
Only run `powermt remove` after the LUN has been unmapped from the host at the array side. Removing an active device will cause I/O failures. After removal, run `powermt save` to persist the updated device list.

## Update PowerPath After Adding New LUNs

```bash
# Discover newly zoned or mapped LUNs
powermt config

# Verify new devices appear in the device list with all expected paths
powermt display dev=all
```


```text title="Expected output"
Discovering devices on all adapters...
Adapter: 0  Path(s): 4
Adapter: 1  Path(s): 4
Adapter: 2  Path(s): 4
Adapter: 3  Path(s): 4

Device Name: emcpowerb
Symmetrix ID: 000297900001
LUN: 0042
Logical Device Name: /dev/mapper/emcpowerb
state: alive; policy: SymmOpt; priority: 0
==============================================================================
Device Name: emcpowerc
Symmetrix ID: 000297900001
LUN: 0043
Logical Device Name: /dev/mapper/emcpowerc
state: alive; policy: SymmOpt; priority: 0
==============================================================================
Device Name: emcpowerd
Symmetrix ID: 000297900001
LUN: 0044
Logical Device Name: /dev/mapper/emcpowerd
state: alive; policy: SymmOpt; priority: 0
...
```

!!! warning "Common errors"
    **`powermt: Command not found`** — Install EMC PowerPath package (e.g., `rpm -ivh PowerPath*.rpm`) and ensure the daemon is running with `systemctl start powerpath`.
    **`powermt: error: Cannot open /etc/powermt.custom`** — Verify PowerPath daemon is running with `systemctl status powerpath` and check file permissions on `/etc/powermt.custom`.
Run `powermt config` after new LUNs have been zoned and masked to the host at the array. New devices will appear in `powermt display dev=all` output with the configured load-balancing policy applied automatically. Run `powermt save` after discovery to persist the updated configuration.

---

## See also

- [Powerpath — Health Checks](../health-checks/)
- [Powerpath — CLI Reference](../cli-reference/)
- [Powerpath — Common Issues](../../troubleshooting/common-issues/)
