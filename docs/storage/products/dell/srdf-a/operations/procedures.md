---
tags:
  - dell
  - operations
---
# SRDF/A — Procedures

<div class="kb-summary">
SRDF/A procedures: establishing SRDF/A groups, cycle time tuning, DSE (Delta Set Extension) management, failover and failback, and link fault recovery.

*Applies to: SRDF/A*
</div>

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Change Readiness

- [ ] All SRDF/A pairs are in Consistent state before beginning any storage changes on R1 or R2 devices
- [ ] SRDF/A link bandwidth headroom has been confirmed — check current utilization is not at saturation
- [ ] SYMCLI host access to both R1 and R2 arrays is confirmed and credentials are available
- [ ] RDF group configuration is documented (RDF group number, R1 SID, R2 SID, cycle time)
- [ ] DR site personnel are available and contactable during the maintenance window
- [ ] If the change involves R2 devices, confirm that activating R2 (failover) is not required during the window

| Item | Status | Notes |
|---|---|---|
| All SRDF/A pairs in Consistent state | | |
| SRDF link bandwidth headroom confirmed | | |
| SYMCLI access to R1 and R2 confirmed | | |
| RDF group number and SIDs documented | | |
| DR site personnel available | | |
| R2 activation not required during window | | |

---

## Maintenance Window

**Safe suspend procedure for SRDF/A (e.g., before a storage upgrade affecting R1 or R2):**

1. Confirm all pairs are in Consistent state
2. Suspend SRDF/A replication for the RDF group:
   ```bash
   symrdf suspend -sid <r1_sid> -rdfg <rdf_group_number> -type RDF/A -force
   ```
3. Confirm pairs are now in the Suspended state:
   ```bash
   symrdf list -sid <r1_sid> -rdfg <rdf_group_number>
   ```
4. Perform the planned maintenance on R1 or R2 devices
5. Resume SRDF/A replication after maintenance:
   ```bash
   symrdf resume -sid <r1_sid> -rdfg <rdf_group_number> -type RDF/A
   ```
6. Monitor resync — delta marks should decrease; pairs should return to Consistent state

---

## Failover Procedure

### Overview

![Overview](../../../../../assets/srdf-a-proc-overview.svg)

SRDF/A failover promotes R2 volumes to read/write. Because SRDF/A is asynchronous, R2 is consistent to the last **completed cycle** rather than the last write, so there is an inherent RPO equal to the lag at the moment of failure. Before failing over, always check the cycle state and lag to understand the data exposure window.

Planned failover (site still accessible) uses `-establish` to immediately reverse replication after the split. Unplanned failover (primary site down) uses the standard `failover` command and requires a separate restore+establish sequence to recover replication.

### Failover Decision Flow

![Failover Decision Flow](../../../../../assets/srdf-a-proc-failover-decision-flow.svg)

```d2
direction: right

incident: "Incident: Primary Site Issue Reported" {shape: rectangle}
primaryReachable: "primaryReachable" {shape: rectangle}
checkCycleState: "Check Cycle State and Lag\nsymrdf -g 20 -type A query -detail" {shape: rectangle}
stakeholderBriefing: "Brief Stakeholders on RPO\n(lag = data exposure window" {shape: rectangle}
r2Consistent: "r2Consistent" {shape: rectangle}
managementAuth: "managementAuth" {shape: rectangle}
plannedFO: "Planned Failover\nsymrdf -g 20 -type A failover -establish -noprompt" {shape: rectangle}
unplannedFO: "Unplanned Failover\nsymrdf -g 20 -type A failover -noprompt" {shape: rectangle}
waitSite: "Continue Monitoring\nWait for Site Recovery" {shape: rectangle}
presentR2: "Present R2 Volumes\nto DR Hosts" {shape: rectangle}
validateApp: "Validate Application\nat DR Site" {shape: rectangle}
failback: "When Primary Recovers:\nRestore + Establish\nsymrdf restore → establish" {shape: rectangle}

incident -> primaryReachable
primaryReachable -> checkCycleState
primaryReachable -> stakeholderBriefing
checkCycleState -> r2Consistent
r2Consistent -> stakeholderBriefing
stakeholderBriefing -> managementAuth
managementAuth -> plannedFO
managementAuth -> unplannedFO
managementAuth -> waitSite
plannedFO -> presentR2
unplannedFO -> presentR2
presentR2 -> validateApp
validateApp -> failback
```

| RPO Factor | How to Check | Acceptable Threshold |
|---|---|---|
| Cycle lag at failover | `query -detail` Lag field | Depends on SLA; typical < 30 s |
| Cycles lost (in-flight) | Transmitting state at failover | 0-1 cycles |
| DSE overflow data | DSE utilization at failover | Ideally 0% |
| Time since last Consistent | Last Consistent timestamp | Per business RPO agreement |

### Post-Failover Steps

![Post-Failover Steps](../../../../../assets/srdf-a-proc-post-failover-steps.svg)

```bash
# Verify R2 devices are Failed Over and accessible
symrdf -g 20 -type A query

# Confirm write access on R2 (run from DR host)
dd if=/dev/zero of=/dev/sdX bs=1M count=10 oflag=direct

# Confirm no unexpected devices still in Consistent/Transmitting
symrdf -g 20 -type A query | grep -v "Failed Over"
```


```text title="Expected output"
R2 Devices Status:
  Device Name       R1 Status        R2 Status        Link Status
  SymDev_001       Write Disabled   Failed Over      OK
  SymDev_002       Write Disabled   Failed Over      OK
  SymDev_003       Write Disabled   Failed Over      OK
  SymDev_004       Write Disabled   Failed Over      OK
  SymDev_005       Write Disabled   Failed Over      OK

10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.847234 s, 12.4 MB/s

R2 Devices Status:
  Device Name       R1 Status        R2 Status        Link Status
  (no devices in Consistent or Transmitting state)
```

!!! warning "Common errors"
    **`dd: failed to open '/dev/sdX': No such file or directory`** — Replace `/dev/sdX` with the actual device name (e.g., `/dev/sdb1`) discovered via `lsblk` or `fdisk -l` on the DR host.
    **`SYMAPI_C_DEVICE_NOT_FOUND: Device group 20 not found`** — Verify the device group number with `symcfg list -g` and use the correct group ID in the `-g` parameter.
    **`Permission denied`** — Run the commands with `sudo` or ensure the user has appropriate Symmetrix administrator privileges via `symacl` configuration.
### Failback and Replication Restoration

![Failback and Replication Restoration](../../../../../assets/srdf-a-proc-failback-and-replication-restoration.svg)

```d2
direction: right

primaryRestored: "Primary Site Restored" {shape: rectangle}
drHostsOff: "Quiesce DR Applications\nUnmount R2 Volumes from DR Hosts" {shape: rectangle}
restoreR1: "Restore R1 from R2\nsymrdf -g 20 -type A restore -noprompt" {shape: rectangle}
waitRestore: "Wait for Restore Complete\nMonitor: symrdf -g 20 -type A query -detail" {shape: rectangle}
establishAsync: "Re-establish SRDF/A Replication\nsymrdf -g 20 -type A establish -noprompt" {shape: rectangle}
verifyConsistent: "Verify Consistent State\nsymrdf -g 20 -type A query" {shape: rectangle}
done: "SRDF/A Replication Restored\nRPO Protection Active" {shape: rectangle}

primaryRestored -> drHostsOff
drHostsOff -> restoreR1
restoreR1 -> waitRestore
waitRestore -> establishAsync
establishAsync -> verifyConsistent
verifyConsistent -> done
```

```bash
# After primary site recovery: restore R1 from R2
symrdf -g 20 -type A restore -noprompt

# Wait for restore to complete (R1 returns to RW)
symrdf -g 20 -type A query -detail

# Re-establish SRDF/A replication (R1 -> R2)
symrdf -g 20 -type A establish -noprompt

# Confirm Consistent state restored
symrdf -g 20 -type A query
```


```text title="Expected output"
Executing restore for group 20, type A...
Restore completed successfully.
Group 20 is now in RW mode on R1.

Symmetrix ID: 000123456789012
Group Number: 20
SRDF Mode: Synchronous
R1 (Local) State: RW
R2 (Remote) State: RW
R1 Link State: Ready
R2 Link State: Ready
Last Update Time: 2024-01-15 14:32:18
Restore Status: Completed
Restore Completion Time: 2024-01-15 14:31:45

Executing establish for group 20, type A...
Establish completed successfully.
Replication link established: R1 -> R2

Group 20 SRDF/A Status:
Symmetrix ID: 000123456789012
Group Number: 20
SRDF Mode: Synchronous
R1 State: Consistent
R2 State: Consistent
Link State: Ready
Replication Status: Active
```

!!! warning "Common errors"
    **`SRDF group 20 is not in a valid state for restore operation`** — Verify R1 is in RW state and R2 is in RO state before attempting restore using `symrdf -g 20 -type A query`.
    **`Restore operation timed out after 3600 seconds`** — Increase the timeout or check for I/O bottlenecks on the primary array; monitor with `symrdf -g 20 -type A query -detail` in a separate terminal.
    **`Cannot establish replication: R1 and R2 data is not synchronized`** — Ensure the restore operation completed fully and both sides report Consistent state before running establish.
### Planned Failover via SYMCLI

![Planned Failover via SYMCLI](../../../../../assets/srdf-a-proc-planned-failover-via-symcli.svg)

```bash
# Confirm all R1 applications are quiesced or shut down
# Initiate planned failover:
symrdf failover -sid <r1_sid> -rdfg <rdf_group_number> -type RDF/A -planned

# Activate R2 volumes for host access at the DR site
# When failing back, follow the failback procedure: resync R2 to R1, then swap direction
```


```text title="Expected output"
Symmetrix ID: 000123456789012
RDF Group: 3
RDF Type: RDF/A
Current R1 State: Ready
Current R2 State: Ready

Initiating planned failover...
Failover in progress: 45%
Failover in progress: 90%
Failover completed successfully.

R1 volumes are now in the Failed Over state.
R2 volumes are now in the Ready state and available for host access.
Failover completed at 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    **`SYMRDF ERROR (1): RDF group <rdf_group_number> is not in a valid state for failover`** — Verify all R1 applications are fully quiesced using `symrdf query -sid <r1_sid> -rdfg <rdf_group_number>` and check for pending I/O.
    **`SYMRDF ERROR (18): Symmetrix <r1_sid> is not reachable`** — Confirm network connectivity to the R1 array and verify the Symmetrix ID is correct with `symcfg list -v`.
    **`SYMRDF ERROR (28): RDF link is not synchronized`** — Wait for RDF synchronization to complete or force a full resync with `symrdf sync -sid <r1_sid> -rdfg <rdf_group_number> -full` before retrying failover.
### Known Issues — Failover

![Known Issues — Failover](../../../../../assets/srdf-a-proc-known-issues-failover.svg)

- **Failover refused when DSE is 100% full**: The array may block the failover operation if DSE is completely full and data has not been transmitted. Suspend the group first to stop accumulating writes, then failover.
- **R2 shows stale data at failover**: This is expected with SRDF/A — check the last completed cycle timestamp to determine the actual recovery point and communicate it to application owners.
- **Establish after failback fails with "Invalid device state"**: Ensure the restore has fully completed (pair state returns to Synchronized) before issuing the establish. Attempting establish while restore is in progress will fail.
- **Lag counter does not reset after planned failover with -establish**: After a planned failover that reverses replication, the new R1 (former R2) will show a brief lag as the first cycles are established. This is normal and should clear within 1-2 cycle periods.

---

## Incident Triage

**On alert or issue:**
1. Run `symrdf list -sid <r1_sid> -rdfg <rdf_group_number>` to identify the current pair states
2. Run `symrdf queryall -sid <r1_sid> -rdfg <rdf_group_number>` to get delta mark count, cycle time, and link state detail
3. Check SRDF/A link utilization and bandwidth — if the link is saturated, Transmit Idle is expected
4. Check the network/dark fibre/WAN path between R1 and R2 sites for outages or congestion
5. If pairs have entered Mixed state, identify which devices are inconsistent and do not activate R2 until consistency is restored or a failover decision is made
6. Escalate to DR site team if link restoration is not possible within the RPO SLA

| Symptom | Likely Cause | Action |
|---|---|---|
| Pair in Transmit Idle | Link saturation — write bandwidth exceeds SRDF/A link capacity | Check link utilization, reduce R1 write I/O during peak, or increase SRDF link bandwidth; run `symrdf queryall` to monitor delta marks |
| Delta mark count growing without bound | Link consistently under-provisioned for current write rate | Increase SRDF bandwidth, adjust cycle time, or implement write throttling on R1 |
| Pair in Mixed state | Partial consistency group inconsistency | Do NOT activate R2 — run `symrdf queryall`, identify inconsistent devices, check for link errors, attempt re-establish: `symrdf establish -sid <r1_sid> -rdfg <rdf_group_number> -type RDF/A` |
| Pair in Split state (unexpected) | Network interruption between R1 and R2 | Check inter-site network, restore connectivity, then re-establish: `symrdf resume -sid <r1_sid> -rdfg <rdf_group_number>` |
| R2 activation required (DR failover) | Production site failure | Follow DR failover runbook; activate R2: `symrdf failover -sid <r1_sid> -rdfg <rdf_group_number>` |
| Cycle time exceeding configured value | Write burst or link latency increase | Monitor cycle time via `symrdf queryall`, check inter-site latency with `ping` and `traceroute` |

---

## Query SRDF/A Group Status

Check the current state of all device pairs in an SRDF/A RDF group:

```bash
symrdf -sid <sid> -rdfg <group> query
```


```text title="Expected output"
Symmetrix ID: 000297123456789
RDF Group: 001
Local Device: 000AB
Remote Device: 000AB
Remote Symmetrix ID: 000297987654321
RDF Mode: Synchronous
Link Status: Ready
Pair State: Synchronized
Last Sync Time: 2024-01-15 14:32:18
Replication Rate: 2.5 MB/sec
Pending Writes: 0
```

!!! warning "Common errors"
    **`symrdf: Error: Invalid Symmetrix ID <sid>`** — Verify the Symmetrix ID with `symcfg list` and ensure it matches your target array.
    **`symrdf: Error: RDF group <group> not found`** — Confirm the RDF group number exists on the array using `symrdf -sid <sid> list` to enumerate all configured groups.
    **`symrdf: Error: Symmetrix not responding`** — Check network connectivity to the array and verify the Symmetrix Management Console (SMC) service is running on the management station.
The output shows each device pair, the RDF state (Synchronized, Consistent, Transmitting, Suspended), and the delta track count. Review the state column to confirm all pairs are in **Consistent** state under normal operations. High delta track counts indicate replication is falling behind.

---

## Suspend and Resume Replication

Use suspend and resume during planned maintenance to prevent delta accumulation while work is in progress.

**Suspend replication:**

```bash
symrdf -sid <sid> -rdfg <group> suspend
```


```text title="Expected output"
Symmetrix ID: 000123456789012
RDF Group: 001
RDF Mode: Synchronous
RDF Status: Suspended
Local Device: DEV001
Remote Device: DEV001
Suspend Time: 2024-01-15 14:32:47
```

!!! warning "Common errors"
    **`SYMRDF ERROR: RDF group <group> is not configured`** — Verify the RDF group number exists with `symrdf -sid <sid> list` and use the correct group ID.
    **`SYMRDF ERROR: RDF group <group> is already suspended`** — Check current RDF status with `symrdf -sid <sid> -rdfg <group> query` before attempting to suspend.
    **`SYMRDF ERROR: Cannot suspend RDF group - operation in progress`** — Wait for any ongoing RDF operations to complete and retry the suspend command.
**Resume replication after maintenance:**

```bash
symrdf -sid <sid> -rdfg <group> resume
```


```text title="Expected output"
Resuming RDF group 1 on array 000123456789ABCD...
RDF group 1 resume completed successfully.
Symmetrix ID: 000123456789ABCD
RDF Group: 1
RDF Mode: Synchronous
Link Status: Ready
```

!!! warning "Common errors"
    **`symrdf: Command not found`** — Ensure the EMC Solutions Enabler (SE) package is installed and the symcli binaries are in your PATH.
    **`SYMAPI_ERROR: The RDF group is not in a suspended state`** — Verify the RDF group status with `symrdf -sid <sid> -rdfg <group> query` before attempting to resume.
    **`SYMAPI_ERROR: Insufficient privileges to perform operation`** — Run the command with appropriate sudo privileges or as a user with EMC Symmetrix administrator credentials.
After resuming, monitor the delta track count — it should decrease as R2 catches up. Confirm pairs return to **Consistent** state before closing the maintenance window.

---

## Perform a Planned Failover

Initiate a planned failover when the production site is available and a controlled switchover is required:

```bash
symrdf -sid <sid> -rdfg <group> failover
```


```text title="Expected output"
Executing Failover for SRDF/A group...
Failover completed successfully.
RDF group 0 (sid: 000123456789ABCD) failover status: SUCCESS
Symmetrix ID: 000123456789ABCD
RDF Group: 0
Previous R1 (Local): FA-1E, FA-2E
Previous R2 (Remote): FA-3E, FA-4E
New R1 (Local): FA-3E, FA-4E
New R2 (Remote): FA-1E, FA-2E
Failover Time: 47 seconds
```

!!! warning "Common errors"
    **`SYMRDF Error: RDF group <group> is not in a valid state for failover`** — Verify the RDF group is in Synchronized or Consistent state using `symrdf -sid <sid> -rdfg <group> query` before attempting failover.
    **`SYMRDF Error: Invalid Symmetrix ID <sid>`** — Confirm the Symmetrix ID is correct and the array is accessible by running `symcfg list -v` to verify connectivity.
    **`SYMRDF Error: RDF group <group> not found`** — Check that the RDF group number exists for the specified Symmetrix ID using `symrdf -sid <sid> query`.
R2 becomes read/write; R1 I/O is suspended and hosts at the production site lose access to the devices. Confirm the failover completed successfully:

```bash
symrdf -sid <sid> -rdfg <group> query
```


```text title="Expected output"
Symmetrix ID: 000123456789012
RDF Group: 001
Local Device: 000_000_00A
Remote Device: 000_000_00A
Remote Symmetrix ID: 000987654321098
RDF Mode: Synchronous
Link Status: Ready
Pair State: Synchronized
Last Sync Time: 2024-01-15 14:32:18
Bytes Written: 1,234,567,890
Replication Lag: 0 ms
```

!!! warning "Common errors"
    **`symrdf: ERROR - Invalid SID <sid>`** — Replace `<sid>` with a valid Symmetrix ID (e.g., `000123456789012`).
    **`symrdf: ERROR - RDF group <group> not found`** — Verify the RDF group number exists on the array using `symrdf -sid <sid> list`.
    **`symrdf: ERROR - Symmetrix not responding`** — Ensure the Symmetrix array is reachable and the Solutions Enabler daemon is running with `symcfg list`.
Verify all pairs show **Failed Over** state before presenting R2 volumes to DR hosts.

---

## Fail Back After Recovery

After the production site is restored and the DR workload is ready to move back, re-establish normal R1→R2 async replication:

```bash
symrdf -sid <sid> -rdfg <group> failback
```


```text title="Expected output"
Executing Failback for SRDF group 000147...

Failback Operation Summary
==========================
Source Symmetrix ID    : 000196047623
Target Symmetrix ID    : 000196047624
RDF Group Number       : 47
RDF Mode               : Synchronous
Current State          : Synchronized
Failback Direction     : Target to Source

Initiating failback...
Failback completed successfully.
New RDF State          : Synchronized
Elapsed Time           : 2 minutes 34 seconds
```

!!! warning "Common errors"
    **`symrdf: Could not connect to the Symmetrix`** — Verify the Symmetrix ID is correct and the array is reachable via the SRDF network.
    **`symrdf: RDF group <group> is not in a valid state for failback`** — Ensure the RDF group is in Synchronized state before attempting failback using `symrdf -sid <sid> -rdfg <group> query`.
    **`symrdf: Invalid group number <group>`** — Confirm the RDF group number exists on the specified Symmetrix using `symrdf -sid <sid> list`.
This operation resynchronises R1 from R2 and restores the original replication direction. Monitor until all pairs return to **Consistent** state and confirm production applications resume normally on R1.

---

## Add Devices to an Existing SRDF/A Group

Add new R1/R2 device pairs to an established SRDF/A group:

```bash
symrdf addpair -sid <sid> -rdfg <group> -dev <R1-devs> -remote_dev <R2-devs>
```


```text title="Expected output"
Symmetrix ID: 000123456789012
RDF Group: 3
Local Device(s): 0001, 0002, 0003
Remote Device(s): 0101, 0102, 0103
RDF Mode: Synchronous
SRDF Link: SE-4E
Pair State: Ready
Consistency Group: CG_PROD_001
Operation completed successfully.
```

!!! warning "Common errors"
    **`SRDF pair already exists for device <dev>`** — Verify the device is not already configured in an SRDF pair using `symrdf query -sid <sid> -dev <dev>` before adding.
    **`RDF group <group> does not exist`** — Create the RDF group first with `symrdf creategroup -sid <sid> -rdfg <group>` or verify the group number is correct.
    **`Remote device <R2-dev> not found on remote array`** — Confirm the remote device exists on the target Symmetrix array and that the SRDF link is active using `symrdf query -sid <remote_sid> -dev <R2-dev>`.
After adding the pairs, establish replication for the new devices:

```bash
symrdf establish -sid <sid> -rdfg <group>
```


```text title="Expected output"
Establishing SRDF link for SID 000123456789 RDF Group 1...
Establishing SRDF link for SID 000123456789 RDF Group 1... (In Progress)
Establishing SRDF link for SID 000123456789 RDF Group 1... (In Progress)
SRDF link established successfully.
RDF Group 1 is now in Synchronized state.
Synchronization completed: 100%
```

!!! warning "Common errors"
    **`SRDF link is already established`** — Verify the current SRDF state with `symrdf query -sid <sid> -rdfg <group>` before attempting to establish.
    **`RDF Group <group> not found for SID <sid>`** — Confirm the SID and RDF group number are correct and exist in your Symmetrix configuration using `symcfg list -sid <sid>`.
    **`Insufficient cache resources available`** — Ensure adequate cache is available on both arrays and check array utilization with `symstat -sid <sid>` before retrying.
Monitor the establish operation until the new pairs reach **Consistent** state alongside the existing group members.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Srdf A — Health Checks](../health-checks/)
- [Srdf A — CLI Reference](../cli-reference/)
- [Srdf A — Common Issues](../../troubleshooting/common-issues/)
