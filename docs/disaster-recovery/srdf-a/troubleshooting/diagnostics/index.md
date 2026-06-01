# SRDF/A — Diagnostics


<div class="kb-summary">
Diagnostics reference covering On-Call Triage — SRDF/A Lag Alert, Diagnostic Command Reference.
</div>

```text
┌──────────────────────────────────────── SRDF/A — Diagnostics ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  SRDF/A — Diagnostic Commands                                 │   │
│   │                       Collect these before opening a vendor support case                      │   │
│   │                                           symrdf query                                        │   │
│   │                                     symrdf suspend / resume                                   │   │
│   │                       Check system logs: /var/log/ or Windows Event Viewer                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Log Collection                │  │               Live Diagnostics              │   │
│   │            Application log bundle            │  │             Network connectivity            │   │
│   │            OS syslog (journalctl)            │  │              Storage path check             │   │
│   │             Core dump if crashed             │  │              Process list check             │   │
│   │             Config export/backup             │  │              Port reachability              │   │
│   │                 symrdf query                 │  │           symrdf suspend / resume           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports      │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology               │
│  R1            = source SRDF volume on production array; host writes flow here                        │
│  R2            = target SRDF volume on DR array; receives replicated data asynchronously              │
│  Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically          │
│  Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO                  │
│  symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore       │
│  SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth             │
│  Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle            │
│  Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts                   │
│  Restore       = after failover resolution, re-establishes replication with R1 as source              │
│  Establish     = initial sync or re-sync operation that copies R1 to R2 in full                       │
│  Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication                 │
│  FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link                      │
│  Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [SRDF/A](../../index.md) reference.

---

## On-Call Triage — SRDF/A Lag Alert

When an SRDF/A lag alert fires:

1. SSH to a host with SYMCLI access and run `symrdf -g <dgname> -sid <r1_sid> query` — confirm current pair state.
2. Check if the WAN link is up (network team or monitoring dashboard).
3. Identify whether this is a transient spike or sustained lag:
   - Transient (< 5 minutes, recovering) — monitor and document.
   - Sustained (> 10 minutes, growing delta queue) — engage storage and network teams.
4. If RPO has breached the agreed threshold, escalate to the change/incident management process.
5. Document the lag window, peak RPO exposure, and resolution in the incident ticket.

---

## Diagnostic Command Reference

```bash
# Check SRDF group and pair states
symrdf -g <dgname> -sid <r1_sid> query

# Detailed view including cycle time, lag, and DSE state
symrdf -g <dgname> -sid <r1_sid> query -detail

# Check SRDF group connectivity and link detail
symcfg -sid <r1_sid> list -rdfg <group_num> -v

# Check SRDF director port state on R1 array
symcfg -sid <r1_sid> list -dir all -v | grep -E "RDF|Port"

# Show delta marks and cycle lag for a group
symrdf -sid <r1_sid> -rdfg <group_num> list -delta

# Review array events (last 30 events filtered to SRDF)
symevent -sid <r1_sid> list -last 30 | grep -i "SRDF\|suspend"

# Check target array thin pool utilisation
symcfg -sid <r2_sid> list -pool -thin -v | grep -E "Pool|Used|Free"
```
