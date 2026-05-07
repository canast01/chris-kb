# SRDF/S Resync

## Overview

Resynchronization restores a fully synchronized SRDF/S pair after the pair has been suspended, split, or failed over. The resync process copies changed tracks from one volume back to the other, making both sides identical again. The direction of the copy depends on which operation preceded the resync.

- After **Suspend/Resume**: pairs re-sync R1 to R2 automatically on `resume`.
- After **Failover** (unplanned): use `restore` to copy R2 back to R1, then `establish` or `failover -establish` to reverse replication.
- After **Split**: use `establish` to restart replication from R1 to R2.

## Pre-Resync Checks

```bash
# Confirm current pair state before deciding resync direction
symrdf -g 10 query -detail

# Check how many invalid tracks need to be copied
symrdf -g 10 query -detail | grep -E "Invalid|Tracks"

# Confirm the RDF link is healthy before initiating
symcfg list -rdfg 10 -detail

# Estimate resync duration based on track count and link bandwidth
symstat -rdf -dir RF-1F -i 5 -c 2
```

Plan the resync during low-utilization periods when possible. A resync under heavy host I/O extends completion time and increases link saturation.

## Resync Operations

```bash
# Resume from Suspended (incremental resync R1 -> R2)
symrdf -g 10 -type S resume -noprompt

# Establish from Split or after manual intervention (R1 -> R2 full/incremental)
symrdf -g 10 -type S establish -noprompt

# Restore after Failed Over (copy R2 data back to R1)
symrdf -g 10 -type S restore -noprompt

# Monitor resync progress in real time
watch -n 10 'symrdf -g 10 query -detail | grep -E "Pair State|Tracks|SyncInProg"'

# Resume a single device rather than the full group
symrdf -sid 0001 -dev 0A1 -type S resume -noprompt
```

## Monitoring Resync Progress

```bash
# Poll pair state until all pairs show Synchronized
symrdf -g 10 query | grep -v Synchronized

# Track percentage complete (shown in SyncInProg state)
symrdf -g 10 query -detail

# Check link throughput during resync
symstat -rdf -i 10 -c 6

# Confirm completion: all pairs Synchronized, 0 tracks
symrdf -g 10 query -detail | grep "Invalid Tracks"
```

Expected output during active resync:

```
Dev    Pair State    % Synced    Invalid Tracks
---    ----------    --------    --------------
0A1    SyncInProg    73%         2,450
0A2    SyncInProg    81%         1,102
```

Expected output after completion:

```
Dev    Pair State     % Synced    Invalid Tracks
---    ----------     --------    --------------
0A1    Synchronized   100%        0
0A2    Synchronized   100%        0
```

## Resync Duration Estimation

| Data Volume | Link Speed | Estimated Duration |
|---|---|---|
| 100 GB changed | 4 Gbps FC | ~4-6 minutes |
| 1 TB changed | 4 Gbps FC | ~35-50 minutes |
| 5 TB changed | 8 Gbps FC | ~90-120 minutes |
| 10 TB changed | 8 Gbps FC | ~3-4 hours |

Times are approximate and depend on concurrent host I/O and array cache state.

## Known Issues and Field Notes

- **Resync stalls with "Transmit Idle"**: The array has temporarily paused sending tracks due to back-pressure on the remote cache. Usually self-resolves. If it persists > 15 minutes, check remote array cache utilization and free cache percentage.
- **Establish fails with "Device in use"**: The R1 device has active host I/O that cannot be quiesced. Schedule the establish during a maintenance window or use `symrdf -g <rdfg> establish -force` after confirming the application is quiesced.
- **Resync repeatedly restarts from 0%**: Indicates the link is dropping mid-resync. Review WAN circuit stability and check for packet loss on the RDF path. Solutions Enabler logs under `/var/symapi/log/` will show disconnect events.
- **Post-restore R1 not coming online**: After a `restore` command the R1 host may need a SCSI bus rescan and possibly a filesystem check before mounting. Never mount R1 volumes before confirming the restore is 100% complete.
