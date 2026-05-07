# Operations

> Part of the [SRDF/A](../) reference.

---
## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] All SRDF/A pairs are in Consistent or Synchronized state |  | no pairs in Transmit Idle, Split, or Mixed state without an open change ticket |
| [ ] Delta mark count is stable |  | a steadily growing delta mark count indicates the link cannot keep pace with writes |
| [ ] Cycle time is within the expected range (default 30 seconds) |  | confirm via `symrdf queryall` |
| [ ] No pairs in Transmit Idle state (indicates link saturation or band |  |  |
| [ ] SRDF/A link utilization is below saturation threshold |  | check that bandwidth headroom exists for peak write periods |

## Health Check

```bash
# List all SRDF/A pairs for a specific RDF group and show their state
symrdf list -sid <r1_sid> -rdfg <rdf_group_number> -type RDF/A

# Query full SRDF/A pair state including cycle time, delta marks, and link state
symrdf queryall -sid <r1_sid> -rdfg <rdf_group_number>

# Show SRDF/A link status and bandwidth utilization for the RDF group
symrdf -sid <r1_sid> -rdfg <rdf_group_number> verify

# Show RDF group configuration (pair count, link ports, cycle time setting)
symrdf -sid <r1_sid> -rdfg <rdf_group_number> -type RDF/A -i 60 -c 5

# Check for any SRDF/A pairs in degraded states across all RDF groups
symrdf list -sid <r1_sid> -state Transmit_Idle
symrdf list -sid <r1_sid> -state Mixed
symrdf list -sid <r1_sid> -state Split

# Check R2 side (run on DR host connected to R2 array)
symrdf list -sid <r2_sid> -rdfg <rdf_group_number> -type RDF/A

# Show delta marks for SRDF/A group (growing delta = link keeping up issue)
symrdf -sid <r1_sid> -rdfg <rdf_group_number> -type RDF/A -delta
```

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

**Planned failover to R2:**

1. Confirm all R1 applications are quiesced or shut down
2. Initiate planned failover:
   ```bash
   symrdf failover -sid <r1_sid> -rdfg <rdf_group_number> -type RDF/A -planned
   ```
3. Activate R2 volumes for host access at the DR site
4. When failing back, follow the failback procedure: resync R2 to R1, then swap direction

## Post-Change Validation

- [ ] All SRDF/A pairs have returned to Consistent state (`symrdf list -sid <r1_sid> -rdfg <rdf_group_number>`)
- [ ] Delta mark count is stable and trending down to zero after resync
- [ ] Cycle time has returned to the configured default (typically 30 seconds)
- [ ] No pairs remain in Transmit Idle, Split, or Mixed state
- [ ] SRDF/A link utilization has returned to normal operating levels
- [ ] Application-level data integrity test confirms no data loss (e.g., confirm last transaction on R2 matches R1)
