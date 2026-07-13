---
tags:
  - dell
  - operations
description: "SRDF/A CLI reference: symrdf list, symrdf query, symrdf establish, symrdf resume, symrdf suspend, and cycle time monitoring commands."
---
# SRDF/A — CLI Reference

<div class="kb-summary">
SRDF/A CLI reference: `symrdf list`, `symrdf query`, `symrdf establish`, `symrdf resume`, `symrdf suspend`, and cycle time monitoring commands.

*Applies to: SRDF/A*
</div>
![SRDF/A — CLI Reference](../../../../../assets/storage-dell-srdf-a-operations-cli-reference.svg)

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Overview

SRDF/A (Asynchronous) is managed via SYMCLI on a Solutions Enabler (SE) host that has access to the PowerMax/VMAX gatekeeper devices. All commands require `-sid <SymmID>` and typically `-rdfg <rdfg_number>`.

Run `symcfg list` to identify your SID. Run `symrdf -sid <sid> list` to identify RDF group numbers.

---

## SRDF/A Command Decision Map

```d2
direction: right

need: "What do you need?" {shape: rectangle}
checkHealth: "Check health / pair state" {shape: rectangle}
checkLag: "Check lag / cycle time" {shape: rectangle}
maintain: "Planned maintenance" {shape: rectangle}
drOps: "DR failover / failback" {shape: rectangle}
addRemove: "Add or remove devices" {shape: rectangle}
cmdHealth: "symrdf -sid sid -rdfg rdfg list -type srdf_a\nsymrdf -sid sid -rdfg rdfg queryall\nsymcfg -sid sid list -rdfgrp" {shape: rectangle}
cmdLag: "symrdf -sid sid -rdfg rdfg list -delta\nsymstat -sid sid -type rdfg -rdfg rdfg" {shape: rectangle}
cmdSuspend: "symrdf -sid sid -rdfg rdfg -cg cg suspend\n(then resume after maintenance" {shape: rectangle}
cmdFailover: "symrdf -sid sid -rdfg rdfg -cg cg failover\nor failover -nop for unplanned" {shape: rectangle}
cmdEstablish: "symrdf -g dgname -sid sid establish -noprompt\nMonitor SyncInProg → Consistent" {shape: rectangle}

need -> checkHealth
need -> checkLag
need -> maintain
need -> drOps
need -> addRemove
checkHealth -> cmdHealth
checkLag -> cmdLag
maintain -> cmdSuspend
drOps -> cmdFailover
addRemove -> cmdEstablish
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


```text title="Expected output"
Symmetrix ID: 000123456789

Device        Sym       Cap(MB) Ident       RDF State  RDF Type
--------      ---       ------- -----       ---------  --------
00B5          0001      102400 RDF1A       Ready      SRDF/A
00B6          0002      102400 RDF1A       Ready      SRDF/A
00B7          0003      102400 RDF1A       Ready      SRDF/A
00B8          0004      102400 RDF1A       Ready      SRDF/A
00B9          0005      102400 RDF1A       Ready      SRDF/A

Symmetrix ID: 000123456789
Device Name:                    00B5
Identifier:                     RDF1A
RDF Group Number:               10
RDF Type:                       SRDF/A
RDF State:                      Ready
Mirror State:                   Synchronized
Pair State:                     Synchronized
Remote Symmetrix:               000987654321
Remote Device:                  00B5

Symmetrix ID: 000123456789
RDF Group:    10
Device Pair:  00B5 <-> 00B5 (Remote SID: 000987654321)
State:        Synchronized
Link State:   Online
Hop ID:       1
Last Update:  2024-01-15 14:32:18

Verify Device Pair: 00B5
State Check:        PASS
Consistency Check:  PASS
Link Verification:  PASS

Device Group: cg_oracle_prod
Symmetrix ID: 000123456789
Type:         Consistency Group
Devices:      12
RDF State:    Ready

Symmetrix ID: 000123456789
RDF Group:    10
Group State:  Synchronized
Device Count: 12
```

!!! warning "Common errors"
    **`SYMCLI_ERROR: Device 00B5 not found in RDF group 10`** — Verify the RDF group number with `symrdf -sid 000123456789 list` and confirm the device is enrolled in that group.
    **`SYMCLI_ERROR: Verify failed — State mismatch detected on device 00B5`** — Check remote array connectivity with `symrdf -sid 000123456789 -rdfg 10 query dev 00B5` and resynchronize if needed using `symrdf -sid 000123456789 -rdfg 10 set -dev 00B5 -state synchronized`.
---

## SRDF/A Consistency Protection

SRDF/A uses transmit idle to ensure consistency. Monitor with:

```bash
# Show SRDF/A consistency state per group
symrdf -sid 000123456789 -rdfg 10 list -v | grep -E "Consistency|SRDF/A|Mode"

# Check if any devices are in "Not Ready" or "Failed Over" state
symrdf -sid 000123456789 -rdfg 10 queryall | grep -v "Synchronized\|SyncInProg"
```


```text title="Expected output"
Consistency State: Synchronized
SRDF/A Mode: Synchronous
RDF Group: 10
Device: 000123456789_000F_00001 Consistency: Synchronized
Device: 000123456789_000F_00002 Consistency: Synchronized
Device: 000123456789_000F_00003 Consistency: Synchronized

RDF Group 10 - Device Status:
Device: 000123456789_000F_00004 State: Not Ready (Pending)
Device: 000123456789_000F_00005 State: SyncInProg (85%)
```

!!! warning "Common errors"
    **`SYMAPI Error: Could not connect to the Symmetrix`** — Verify the Symmetrix SID is correct and the SYMAPI daemon is running on the local host.
    **`Error: RDF Group 10 not found`** — Confirm the RDF group number exists on the array using `symrdf -sid 000123456789 list`.
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


```text title="Expected output"
{
  "rdf_group_list": [
    {
      "rdfGroupNumber": 10,
      "label": "SRDF-A-Primary",
      "remoteSymmetrix": "000987654321",
      "states": [
        "Synchronized"
      ]
    },
    {
      "rdfGroupNumber": 11,
      "label": "SRDF-A-Secondary",
      "remoteSymmetrix": "000987654321",
      "states": [
        "Synchronized"
      ]
    }
  ]
}
{
  "rdfGroupNumber": 10,
  "label": "SRDF-A-Primary",
  "remoteSymmetrix": "000987654321",
  "states": [
    "Synchronized"
  ],
  "type": "RDF1",
  "numDevices": 24,
  "reserved": false
}
{
  "volume_list": [
    {
      "volumeId": "00ABC",
      "rdfpairstate": "Synchronized",
      "localRdfGroupNumber": 10,
      "remoteRdfGroupNumber": 10,
      "remoteVolume": "00ABC"
    },
    {
      "volumeId": "00ABD",
      "rdfpairstate": "Synchronized",
      "localRdfGroupNumber": 10,
      "remoteRdfGroupNumber": 10,
      "remoteVolume": "00ABD"
    }
  ]
}
Mode:         000987654321
SRDF/A State: ['Synchronized']
Label:        SRDF-A-Primary
{
  "rdf_group_list": [
    {
      "rdfGroupNumber": 10,
      "storageGroupName": "sg_oracle_prod",
      "pairCount": 24
    }
  ]
}
{
  "resultList": {
    "result": [
      {
        "timestamp": 1704067200000,
        "MBSentPerSec": 245.67,
        "MBReceivedPerSec": 243.12,
        "AvgCycleTime": 18.4,
        "CyclesPerSec": 156
      }
    ]
  }
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Remove the `--insecure` flag only if using a valid CA-signed certificate, or ensure the Unisphere server certificate is trusted by the system.
    **`HTTP/1.1 401 Unauthorized`** — Verify the SMC credentials in the `AUTH` variable are correct and the user has REST API permissions in Unisphere.
    **`jq: command not found` or `ModuleNotFoundError: No module named 'json'`** — Install Python 3 with the json module (standard library) or use `jq` instead of `python3 -m json.tool` for JSON formatting.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Srdf A — Procedures](../procedures/)
- [Srdf A — Scripts](../scripts/)
- [Srdf A — Health Checks](../health-checks/)
