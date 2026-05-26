# SRDF/A — CLI Reference

> Part of the [SRDF/A](../../index.md) reference.
---

## Overview

SRDF/A (Asynchronous) is managed via SYMCLI on a Solutions Enabler (SE) host that has access to the PowerMax/VMAX gatekeeper devices. All commands require `-sid <SymmID>` and typically `-rdfg <rdfg_number>`.

Run `symcfg list` to identify your SID. Run `symrdf -sid <sid> list` to identify RDF group numbers.

---

## SRDF/A Command Decision Map

```mermaid
flowchart TD
    need["What do you need?"]
    checkHealth["Check health / pair state"]
    checkLag["Check lag / cycle time"]
    maintain["Planned maintenance"]
    drOps["DR failover / failback"]
    addRemove["Add or remove devices"]

    cmdHealth["symrdf -sid sid -rdfg rdfg list -type srdf_a\nsymrdf -sid sid -rdfg rdfg queryall\nsymcfg -sid sid list -rdfgrp"]
    cmdLag["symrdf -sid sid -rdfg rdfg list -delta\nsymstat -sid sid -type rdfg -rdfg rdfg"]
    cmdSuspend["symrdf -sid sid -rdfg rdfg -cg cg suspend\n(then resume after maintenance)"]
    cmdFailover["symrdf -sid sid -rdfg rdfg -cg cg failover\nor failover -nop for unplanned"]
    cmdEstablish["symrdf -g dgname -sid sid establish -noprompt\nMonitor SyncInProg → Consistent"]

    need --> checkHealth
    need --> checkLag
    need --> maintain
    need --> drOps
    need --> addRemove

    checkHealth --> cmdHealth
    checkLag --> cmdLag
    maintain --> cmdSuspend
    drOps --> cmdFailover
    addRemove --> cmdEstablish

    style need fill:#2563eb,color:#fff
    style cmdFailover fill:#be123c,color:#fff
```
```

---

## Cycle Time and Delta Mark (Lag Monitoring)

SRDF/A replication proceeds in cycles. The cycle time and delta marks indicate how far behind the secondary is.

```bash
# Show delta marks and cycle lag for a group
symrdf -sid 000123456789 -rdfg 10 list -delta

# Verbose output including cycle time and marks
symrdf -sid 000123456789 -rdfg 10 list -v

# RDF group performance and cycle statistics
symstat -sid 000123456789 -type rdfg -rdfg 10

# Check minimum cycle time configured for SRDF/A
symcfg -sid 000123456789 show -rdfgrp 10 | grep -i cycle

# Monitor lag continuously (poll every 60 seconds)
watch -n 60 'symrdf -sid 000123456789 -rdfg 10 list -delta | grep -E "Lag|Cycle|Delta"'
```

---

## Operations on Storage Groups (CG-based)

SRDF/A operations are performed on Composite Groups (CG) or Storage Groups (SG). Using `-cg` is recommended for SRDF/A to ensure consistency across all devices.

```bash
# Suspend SRDF/A (pause replication — hold at DR site)
symrdf -sid 000123456789 -rdfg 10 -cg cg_oracle_prod suspend

# Resume SRDF/A after suspend
symrdf -sid 000123456789 -rdfg 10 -cg cg_oracle_prod resume

# Update (force a manual sync cycle)
symrdf -sid 000123456789 -rdfg 10 -cg cg_oracle_prod update

# Failover — activate R2 devices for production use at DR site
symrdf -sid 000123456789 -rdfg 10 -cg cg_oracle_prod failover

# Failover without establishing reverse replication
symrdf -sid 000123456789 -rdfg 10 -cg cg_oracle_prod failover -nop

# Failback — return to normal after failover (resync R2 to R1)
symrdf -sid 000123456789 -rdfg 10 -cg cg_oracle_prod failback

# Establish / re-establish SRDF/A pair (from scratch or after failover)
symrdf -sid 000123456789 -rdfg 10 -cg cg_oracle_prod establish

# Split (break mirror, R1 and R2 both R/W — for maintenance)
symrdf -sid 000123456789 -rdfg 10 -cg cg_oracle_prod split

# Swap personalities (R1 becomes R2, DR site becomes source)
symrdf -sid 000123456789 -rdfg 10 -cg cg_oracle_prod swap
```

---

## Device-Level Operations

For per-device inspection or scripted operations:

```bash
# List devices in an RDF group with their state
symdev -sid 000123456789 list -rdfg 10 -rdf

# Show specific device SRDF/A detail
symdev -sid 000123456789 show 00B5 -rdf

# Query a specific device pair
symrdf -sid 000123456789 -rdfg 10 query dev 00B5

# Verify device states match expected (exits non-zero on mismatch)
symrdf -sid 000123456789 -rdfg 10 verify dev 00B5

# Device group operations (legacy — prefer SG-based operations above)
symdg show cg_oracle_prod
symrdf -g cg_oracle_prod -sid 000123456789 query
```

---

## SRDF/A Consistency Protection

SRDF/A uses transmit idle to ensure consistency. Monitor with:

```bash
# Show SRDF/A consistency state per group
symrdf -sid 000123456789 -rdfg 10 list -v | grep -E "Consistency|SRDF/A|Mode"

# Check if any devices are in "Not Ready" or "Failed Over" state
symrdf -sid 000123456789 -rdfg 10 queryall | grep -v "Synchronized\|SyncInProg"
```

---

## Unisphere REST API

Base URL: `https://<unisphere-host>:8443/univmax/restapi`  
Authentication: HTTP Basic.

```bash
UNISPHERE="https://unisphere.example.com:8443/univmax/restapi"
SID="000123456789"
AUTH="-u smc:password --insecure"

# List all RDF groups for an array
curl -s $AUTH "$UNISPHERE/100/replication/symmetrix/${SID}/rdf_group" | \
  python3 -m json.tool

# Get details of a specific RDF group
RDFG=10
curl -s $AUTH "$UNISPHERE/100/replication/symmetrix/${SID}/rdf_group/${RDFG}" | \
  python3 -m json.tool

# List replication volumes (SRDF device pairs) in a group
curl -s $AUTH "$UNISPHERE/100/replication/symmetrix/${SID}/rdf_group/${RDFG}/volume" | \
  python3 -m json.tool

# SRDF/A group state summary
curl -s $AUTH "$UNISPHERE/100/replication/symmetrix/${SID}/rdf_group/${RDFG}" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
print('Mode:        ', data.get('remoteSymmetrix','?'))
print('SRDF/A State:', data.get('states','?'))
print('Label:       ', data.get('label','?'))
"

# StorageGroup-level replication details
SG="sg_oracle_prod"
curl -s $AUTH "$UNISPHERE/100/replication/symmetrix/${SID}/storagegroup/${SG}/rdf_group" | \
  python3 -m json.tool

# Performance metrics for an RDF group (KPIs)
curl -s $AUTH "$UNISPHERE/performance/RDFGroup/metrics" \
  -H "Content-Type: application/json" \
  -d "{
    \"symmetrixId\": \"${SID}\",
    \"rdfgNumber\": ${RDFG},
    \"dataFormat\": \"Average\",
    \"metrics\": [\"MBSentPerSec\",\"MBReceivedPerSec\",\"AvgCycleTime\",\"CyclesPerSec\"]
  }" | python3 -m json.tool
```
