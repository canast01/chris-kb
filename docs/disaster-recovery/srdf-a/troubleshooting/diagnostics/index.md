# SRDF/A — Diagnostics

> Part of the [SRDF/A](../../) reference.

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

---

## Collecting Diagnostics Before Engaging Support

Always collect the following before opening a Dell support case or escalating:

| Item | Command |
|---|---|
| Current pair states | `symrdf -g <dgname> -sid <r1_sid> query` |
| Detailed cycle/lag output | `symrdf query -g <group> -v` |
| Array event log | `symevent -sid <SID> list -last 100` |
| RDF group configuration | `symcfg -sid <SID> list -rdfg <group_num> -v` |
| Solutions Enabler version | `symcli -version` |
| Array serial numbers | `symcfg list` |

Save all output to a timestamped file:

```bash
symrdf -g <dgname> -sid <r1_sid> query -detail > /tmp/srdf_diag_$(date +%Y%m%d_%H%M%S).txt
```
