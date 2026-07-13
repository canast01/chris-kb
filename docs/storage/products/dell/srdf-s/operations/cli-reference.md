---
tags:
  - dell
  - operations
description: "SRDF/S CLI reference: symrdf establish, symrdf query -synchronous, symrdf suspend, symrdf resume, symrdf failover -establish, and link status commands."
---
# SRDF/S — CLI Reference

<div class="kb-summary">
SRDF/S CLI reference: `symrdf establish`, `symrdf query -synchronous`, `symrdf suspend`, `symrdf resume`, `symrdf failover -establish`, and link status commands.

*Applies to: SRDF/S*
</div>
![SRDF/S — CLI Reference](../../../../../assets/storage-dell-srdf-s-operations-cli-reference.svg)

> Part of the [SRDF/S Operations](index.md) reference.

All SRDF/S management is performed via SYMCLI (Solutions Enabler). Commands require appropriate RBAC permissions and must be run from a Solutions Enabler host with connectivity to the array. Always specify `-g <group>` to scope operations to the correct SRDF group and `-sid <sid>` to target the correct array.

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## SRDF/S Operation Decision Map

```d2
direction: right

goal: "What do you need to do?" {shape: rectangle}
monitor: "Monitor pair health\nand link state" {shape: rectangle}
maintenance: "Planned maintenance\n(suspend replication" {shape: rectangle}
drTest: "DR test\n(non-disruptive" {shape: rectangle}
failover: "Actual failover\n(production use of R2" {shape: rectangle}
failback: "Return to normal\nafter failover" {shape: rectangle}
cmdQuery: "symrdf -sid sid -g grp query\nsymcfg -sid sid list -rdfg\nsymstat -rdf" {shape: rectangle}
cmdSuspend: "symrdf -sid sid -g grp suspend -noprompt\n(then resume after maintenance" {shape: rectangle}
cmdSplit: "symrdf -sid sid -g grp split -noprompt\n(R2 accessible for testing" {shape: rectangle}
cmdFailover: "symrdf -sid sid -g grp failover -noprompt" {shape: rectangle}
cmdFailback: "symrdf -sid sid -g grp failback -noprompt\nor: restore → establish" {shape: rectangle}

goal -> monitor
goal -> maintenance
goal -> drTest
goal -> failover
goal -> failback
monitor -> cmdQuery
maintenance -> cmdSuspend
drTest -> cmdSplit
failover -> cmdFailover
failback -> cmdFailback
```

---

## Failover & Failback

Failover makes R2 the new production side. Always run in a maintenance window except during a real DR event.

```bash
# Planned failover (splits pairs, R2 becomes R/W)
symrdf -sid <sid> -g <group> failover -noprompt

# Verify R2 is now active
symrdf -sid <sid> -g <group> query

# Failback to original R1 (after restoring R1 site)
symrdf -sid <sid> -g <group> failback -noprompt

# Resynchronise after failover or split
symrdf -sid <sid> -g <group> resync -noprompt
```


```text title="Expected output"
Symmetrix ID: 000123456789012
Director: 4e
RDF group: 001
Local device: 000AA
Remote device: 000BB
Pair state: Synchronized
RDF mode: Synchronous
Failover completed successfully.
R2 (Remote) is now Read/Write.
R1 (Local) is now Read-Only.

Pair state: Failed Over
R2 state: R/W
R1 state: R/O
Last update: 2024-01-15 14:32:18

Failback initiated for group 001.
R1 resuming R/W role.
R2 reverting to R/O.
Failback completed successfully.

Resynchronization started for group 001.
Synchronizing 2 pairs...
Progress: 100%
Resynchronization completed successfully.
```

!!! warning "Common errors"
    **`RDF pair not in a valid state for failover`** — Verify pair state is Synchronized using `symrdf -sid <sid> -g <group> query` before attempting failover.
    **`RDF group <group> not found for Symmetrix <sid>`** — Confirm the correct SID and group number with `symrdf -sid <sid> list` and verify RDF licensing is enabled.
    **`Cannot failback: R1 site is not accessible`** — Ensure R1 array is online and network connectivity between sites is restored before issuing failback.
---

## Swap & Metro Operations

For SRDF/Metro or swap operations on bidirectional configurations.

```bash
# Swap R1/R2 roles
symrdf -sid <sid> -g <group> swap -noprompt

# Set SRDF mode to synchronous
symrdf -sid <sid> -g <group> setmode -sync -noprompt

# Set SRDF mode to asynchronous (temporary degraded mode)
symrdf -sid <sid> -g <group> setmode -acp_disk -noprompt
```


```text title="Expected output"
Swap R1/R2 roles
Swap operation initiated for group SRDF_GRP_001 on array 000123456789
Current R1: DF-SYS-PROD-01 (IP: 10.45.120.15)
Current R2: DF-SYS-DR-01 (IP: 10.45.120.45)
Swap completed successfully in 47 seconds
RDF link status: SYNCED

Set SRDF mode to synchronous
Mode change initiated for group SRDF_GRP_001
Previous mode: Asynchronous (ACP_DISK)
New mode: Synchronous
Mode transition completed in 12 seconds
All RDF pairs now in SYNCED state

Set SRDF mode to asynchronous (temporary degraded mode)
Mode change initiated for group SRDF_GRP_001
Previous mode: Synchronous
New mode: Asynchronous (ACP_DISK)
Mode transition completed in 8 seconds
RDF link latency: 45ms
```

!!! warning "Common errors"
    **`SRDF group SRDF_GRP_001 not found on array 000123456789`** — Verify the group name with `symrdf -sid <sid> list` and confirm the SID matches your target array.
    **`RDF link is not READY — cannot perform swap operation`** — Check RDF link status with `symrdf -sid <sid> -g <group> query` and wait for SYNCED state before retrying.
    **`User does not have privilege to execute SRDF operations`** — Ensure your Symmetrix user account has SRDF admin privileges in Solutions Enabler or contact your storage administrator.
---

## Common Health Check Sequence

```bash
# Full SRDF/S pre-change health check
symcfg -sid <sid> list -rdfg
symrdf -sid <sid> -g <group> query
symrdf -sid <sid> list -v
symdg show <group_name>
```


```text title="Expected output"
Symmetrix ID: 000123456789012
                                SRDF/S Group Information
Group Name         Group #  Type  Priority  Domino  Witness  State
PROD_RDF_GRP_01    1        RDF   1         No      Yes      Ready
PROD_RDF_GRP_02    2        RDF   2         No      Yes      Ready

Symmetrix ID: 000123456789012
                           SRDF/S Pair Information
PairName           Dev#  Type  TDEV  SDEV  State  Link  %Cpy  Domino
PROD_RDF_GRP_01    0001  RDF   Yes   Yes   Syncd  OK    100   No
PROD_RDF_GRP_01    0002  RDF   Yes   Yes   Syncd  OK    100   No

Symmetrix ID: 000123456789012
                    SRDF/S Link Information
Link ID  Local IP      Remote IP     State  Latency(ms)  Bandwidth(Mbps)
1        192.168.1.10  192.168.2.10  Ready  2.3          1000
2        192.168.1.11  192.168.2.11  Ready  2.1          1000

Symmetrix ID: 000123456789012
                    Device Group: PROD_RDF_GRP_01
Group Type: RDF/S
Symmetrix ID: 000123456789012
Number of Devices: 2
Device Name    Capacity(GB)  Type    Status
PROD_VOL_001   500           TDEV    Ready
PROD_VOL_002   250           TDEV    Ready
```

!!! warning "Common errors"
    **`SYMCFG-00001: Cannot find Symmetrix with ID <sid>`** — Verify the correct Symmetrix ID with `symcfg list` and ensure the array is accessible.
    **`SYMRDF-00456: RDF group <group> does not exist`** — Confirm the RDF group name exists using `symrdf -sid <sid> list` before querying.
    **`SYMDG-00789: Device group <group_name> not found`** — Check the exact device group name spelling with `symdg list` and retry.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Srdf S — Procedures](../procedures/)
- [Srdf S — Scripts](../scripts/)
- [Srdf S — Health Checks](../health-checks/)
