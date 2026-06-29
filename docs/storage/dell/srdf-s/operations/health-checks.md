---
tags:
  - dell
  - operations
---
# SRDF/S — Health Checks

<div class="kb-summary">
SRDF/S health checks: `symrdf query -synchronous` link status, invalid track count review, SRDF pair consistency validation, and RDF group hop count check.

*Applies to: SRDF/S*
</div>

> Part of the [SRDF/S Operations](index.md) reference.

Regular health checks on SRDF/S replication confirm that all device pairs are synchronized, RDF directors and links are operational, and no track backlogs exist. These checks should run daily as part of infrastructure monitoring and immediately before any planned failover or maintenance activity.

Health checks cover four layers: pair state, link/director status, performance metrics, and array-level configuration consistency.

```d2
direction: right

dailyStart: "Daily Health Check" {shape: rectangle}
pairState: "Check Pair State\nsymrdf query -g dgname" {shape: rectangle}
allSynced: "allSynced" {shape: rectangle}
checkRTT: "Check WAN RTT\nping -c 20 dr-site-ip" {shape: rectangle}
investigatePairs: "Investigate Pair State\nCheck invalid tracks" {shape: rectangle}
rttOk: "rttOk" {shape: rectangle}
checkDirector: "Check RDF Director\nsymcfg list -dir all -rdf" {shape: rectangle}
investigateRTT: "Report to Network Team\nRTT exceeds SRDF/S budget" {shape: rectangle}
dirOnline: "dirOnline" {shape: rectangle}
checkLink: "Check Link Utilization\nsymstat -rdf -dir RF-1F -i 5 -c 3" {shape: rectangle}
investigateDir: "Check Director Port\nPhysical link and configuration" {shape: rectangle}
linkOk: "linkOk" {shape: rectangle}
healthy: "Health Check PASSED\nDocument results" {shape: rectangle}
investigateLink: "Investigate Link Saturation\nEngage network team" {shape: rectangle}

dailyStart -> pairState
pairState -> allSynced
allSynced -> checkRTT
allSynced -> investigatePairs
checkRTT -> rttOk
rttOk -> checkDirector
rttOk -> investigateRTT
checkDirector -> dirOnline
dirOnline -> checkLink
dirOnline -> investigateDir
checkLink -> linkOk
linkOk -> healthy
linkOk -> investigateLink
```

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "Health Checks \u2014 Thresholds",
    "fontSize": 13,
    "fontWeight": "normal"
  },
  "width": 480,
  "height": {
    "step": 26
  },
  "data": {
    "values": [
      {
        "metric": "Link utilization",
        "zone": "Safe",
        "val": 80
      },
      {
        "metric": "Link utilization",
        "zone": "Alert",
        "val": 20
      }
    ]
  },
  "mark": {
    "type": "bar",
    "cornerRadiusEnd": 3
  },
  "encoding": {
    "y": {
      "field": "metric",
      "type": "nominal",
      "axis": {
        "title": null,
        "labelLimit": 200
      },
      "sort": null
    },
    "x": {
      "field": "val",
      "type": "quantitative",
      "stack": "normalize",
      "axis": {
        "title": "Threshold boundary",
        "format": ".0%"
      }
    },
    "color": {
      "field": "zone",
      "type": "nominal",
      "scale": {
        "domain": [
          "Safe",
          "Alert"
        ],
        "range": [
          "#15803d",
          "#dc2626"
        ]
      },
      "legend": {
        "title": "Zone"
      }
    },
    "order": {
      "field": "zone",
      "sort": [
        "Safe",
        "Alert"
      ]
    },
    "tooltip": [
      {
        "field": "metric",
        "type": "nominal",
        "title": "Metric"
      },
      {
        "field": "zone",
        "type": "nominal",
        "title": "Zone"
      },
      {
        "field": "val",
        "type": "quantitative",
        "title": "Segment %",
        "format": ".0f"
      }
    ]
  }
}
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **SRDF group state:** `symrdf -g <group> query` — all pairs must show RDF State: Synchronized
2. **Write latency overhead:** `symstat -sid <sid> -rdfg <group> -type rdf` — check write penalty vs threshold (<10ms addition)
3. **WAN RTT:** measure round-trip to DR site — SRDF/S requires <10ms RTT for acceptable performance
4. **Link health:** `symrdf -g <group> verifylink` — all paths healthy, no single-path warning
5. **Director status:** `symmaskdb -sid <sid> list -dir` — all RDF directors Online
6. **Pair count:** `symrdf -g <group> query | grep -c Synchronized` — should equal total device count
7. **Failed over pairs (none expected in normal ops):** `symrdf -g <group> query | grep -v Synchronized` — should be empty
8. **SRDF/Star check (if 3-site configured):** `symrdf -star -g <group> query` — all hops synchronized
9. **Bias setting (for split-brain protection):** `symrdf -g <group> query | grep -i bias` — verify correct site has bias
10. **PowerPath multipath status on hosts:** `powermt display dev=all | grep -i dead` — should return empty

**WAN Latency Impact on Write Performance:**

SRDF/S adds one WAN round trip to every host write. The relationship is approximately:

```text
Effective write latency = local array write time + (WAN RTT / 2) + remote commit time
```

```bash
# Continuous WAN RTT check from primary site to DR site storage port
ping -i 5 -c 60 <dr_storage_port_ip> | tee /tmp/srdf_rtt_$(date +%Y%m%d).log

# Check SRDF link bandwidth utilisation via Unisphere REST API
UNISPHERE="https://unisphere.example.com:8443/univmax/restapi"
SID="000123456789"
RDFG=10
AUTH="-u smc:password --insecure"

curl -s $AUTH \
  "$UNISPHERE/performance/RDFGroup/metrics" \
  -H "Content-Type: application/json" \
  -d "{
    \"symmetrixId\": \"${SID}\",
    \"rdfgNumber\": ${RDFG},
    \"dataFormat\": \"Average\",
    \"metrics\": [\"MBSentPerSec\",\"MBReceivedPerSec\",\"WriteResponseTime\",\"AvgIOServiceTime\"]
  }" | python3 -m json.tool

# From SE host: check SRDF group statistics
symstat -sid 000123456789 -type rdfg -rdfg 10

# Monitor write latency continuously at 60-second intervals
watch -n 60 'symrdf -sid 000123456789 -rdfg 10 list -v | grep -E "Latency|WriteResp|State"'
```


```text title="Expected output"
PING 192.168.100.45 (192.168.100.45) 56(84) bytes of data.
64 bytes from 192.168.100.45: icmp_seq=1 time=8.234 ms
64 bytes from 192.168.100.45: icmp_seq=2 time=8.156 ms
64 bytes from 192.168.100.45: icmp_seq=3 time=8.412 ms
64 bytes from 192.168.100.45: icmp_seq=4 time=8.289 ms
64 bytes from 192.168.100.45: icmp_seq=5 time=8.367 ms
...
--- 192.168.100.45 statistics ---
60 packets transmitted, 60 received, 0% packet loss, time 299456ms
rtt min/avg/max/stddev = 8.156/8.301/9.847/0.412 ms

{
  "resultList": {
    "result": [
      {
        "symmetrixId": "000123456789",
        "rdfgNumber": 10,
        "MBSentPerSec": 245.67,
        "MBReceivedPerSec": 238.92,
        "WriteResponseTime": 12.34,
        "AvgIOServiceTime": 11.89
      }
    ]
  }
}

Symmetrix ID: 000123456789
RDFG Number: 10
State: Synchronized
Write Pending: 0
Read Pending: 0
Latency (ms): 12.34
WriteResponseTime (ms): 12.34
MBSentPerSec: 245.67
MBReceivedPerSec: 238.92

Every 60s: symrdf -sid 000123456789 -rdfg 10 list -v | grep -E "Latency|WriteResp|State"
State: Synchronized
WriteResponseTime: 12.34 ms
Latency: 12.34 ms
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `--insecure` flag or import the Unisphere CA certificate into your system trust store.
    **`symstat: Command not found`** — Ensure the Symmetrix CLI (Solutions Enabler) is installed and the `$PATH` includes `/opt/emc/SYMCLI/bin` or equivalent.
    **`Authentication failed: Invalid credentials`** — Verify the SMC user credentials in the `AUTH` variable match the Unisphere account and that the account has RDF metrics API permissions.
**Thresholds:**

| Metric | Normal | Investigate | Escalate | Why |
|---|---|---|---|---|
| WAN RTT (ping) | ≤5 ms | 5–10 ms | >10 ms | Every 1ms of RTT adds ~2ms to host write latency |
| Write response time vs baseline | ±10% | +10–25% | >25% or application SLA breach | SRDF/S latency penalty is directly visible to application users |
| SRDF link utilisation | <70% | 70–85% | >85% | Saturation causes write pending buildup and possible Write Disabled state |

A sustained WAN RTT increase of more than 2 ms above baseline should be reported to the network team before it impacts application SLAs.

---

## Configuration Consistency Check

![Configuration Consistency Check](../../../../assets/storage-dell-srdf-s-hc-configuration-consistency-check.svg)

![Configuration Consistency Check](../../../../assets/storage-dell-srdf-s-hc-configuration-consistency-check.svg)

```bash
# Confirm RDFG group membership matches expected device list
symrdf -g 10 list -v

# Verify OLPAIRS (Online Pair) configuration
symrdf -g 10 query -detail | grep OLPAIRS

# Check SRDF/S mode is correctly set (not accidentally changed to /A)
symcfg list -rdfg 10 -detail | grep "SRDF Mode"

# Confirm both arrays have matching group numbers
symcfg list -rdfg all
```


```text title="Expected output"
Symmetrix ID: 000296802151
RDFG Number: 10
Local SymmID: 000296802151
Remote SymmID: 000296802152
SRDF Mode: Synchronous
RDF Link: RF-1A (Online)
RDF Link: RF-1B (Online)
Local Device Count: 42
Remote Device Count: 42

OLPAIRS: 42
Pair State: Synchronized
Link State: Online

SRDF Mode: Synchronous

Symmetrix ID: 000296802151
  RDFG 10: Remote SymmID 000296802152

Symmetrix ID: 000296802152
  RDFG 10: Remote SymmID 000296802151
```

!!! warning "Common errors"
    **`RDFG 10 not found`** — Verify the RDFG number exists with `symrdf list` and confirm it matches your configuration.
    **`RDF Link: RF-1A (Offline)`** — Check physical RDF cable connections and run `symrdf -g 10 check` to diagnose link failures.
    **`Pair State: Out-of-Sync`** — Resume replication with `symrdf -g 10 resume` after verifying no data corruption occurred.
---

## Health Check Summary Table

![Health Check Summary Table](../../../../assets/storage-dell-srdf-s-hc-health-check-summary-table.svg)

![Health Check Summary Table](../../../../assets/storage-dell-srdf-s-hc-health-check-summary-table.svg)

| Check | Command | Healthy Result | Alert Threshold |
|---|---|---|---|
| Pair state | `symrdf -g <rdfg> query` | All Synchronized | Any non-Synchronized |
| Invalid tracks | `symrdf -g <rdfg> query -detail` | 0 tracks | > 0 tracks |
| RDF director | `symcfg list -dir all -rdf` | Online | Any Offline/Failed |
| Link utilization | `symstat -rdf` | < 80% sustained | > 80% for > 5 min |
| Remote connectivity | `symcfg list -rdfg <n> -detail` | Link Online | Link Offline/Partitioned |

---

## Known Issues and Field Notes

![Known Issues and Field Notes](../../../../assets/storage-dell-srdf-s-hc-known-issues-and-field-notes.svg)

![Known Issues and Field Notes](../../../../assets/storage-dell-srdf-s-hc-known-issues-and-field-notes.svg)

- **Intermittent "Transmit Idle" during off-peak hours**: Normal behaviour when there are no writes to replicate. Does not indicate a problem. Confirm by checking that track count remains 0.
- **Director shows Online but link shows Partitioned**: Usually a transient WAN interruption. Wait 2 minutes and re-query. If it persists, escalate to network team to check the dark fibre or IP WAN path.
- **Health check script timeouts on large arrays**: If `symcfg list -rdfg all` takes > 60 seconds, break queries into per-group calls and parallelize across RDFG groups using a shell loop.
- **Mismatched device counts between R1 and R2**: Investigate immediately — indicates a pairing configuration error. Use `symrdf -g <rdfg> list -v` on both arrays to compare device lists.

---

## Validation

![Validation](../../../../assets/storage-dell-srdf-s-hc-validation.svg)

![Validation](../../../../assets/storage-dell-srdf-s-hc-validation.svg)

Validation confirms that SRDF/S replication is protecting data as designed, that pair states are correct, and that a failover would succeed if required. Validation runs are performed after configuration changes, after DR tests, after link maintenance, and on a scheduled basis (typically monthly). Validation differs from health checks in that it actively verifies end-to-end data integrity and failover readiness rather than just checking operational status.

### Pre-Validation Inventory

![Pre-Validation Inventory](../../../../assets/storage-dell-srdf-s-hc-pre-validation-inventory.svg)

Before running validation, capture a baseline state snapshot:

```bash
# Save current pair state for all RDFG groups
symcfg list -rdfg all > /tmp/rdfg_inventory_$(date +%Y%m%d).txt

# Capture device-level state for each group
symrdf -g 10 query -detail >> /tmp/rdfg_inventory_$(date +%Y%m%d).txt
symrdf -g 11 query -detail >> /tmp/rdfg_inventory_$(date +%Y%m%d).txt

# Confirm RDF director status
symcfg list -dir all -rdf >> /tmp/rdfg_inventory_$(date +%Y%m%d).txt

# Record SRDF group configuration
symcfg list -rdfg 10 -detail >> /tmp/rdfg_inventory_$(date +%Y%m%d).txt
```


```text title="Expected output"
Symmetrix ID: 000296701234
RDFG #10: RDF1
  Symmetrix ID: 000296701234
  Remote Symmetrix ID: 000296705678
  RDFG Number: 10
  RDFG Type: Synchronous
  Number of Pairs: 48
  Number of Devices: 48

RDFG #11: RDF2
  Symmetrix ID: 000296701234
  Remote Symmetrix ID: 000296709012
  RDFG Number: 11
  RDFG Type: Asynchronous
  Number of Pairs: 32
  Number of Devices: 32

RDF Director Status:
  Director 4e: Online, RDF Link: Optimal
  Director 4f: Online, RDF Link: Optimal
  Director 5e: Online, RDF Link: Optimal
  Director 5f: Online, RDF Link: Optimal

RDFG 10 Configuration:
  Symmetrix ID: 000296701234
  Remote Symmetrix ID: 000296705678
  RDFG Number: 10
  RDFG Type: Synchronous
  Number of Pairs: 48
  Number of Devices: 48
  Pair State: Synchronized
```

!!! warning "Common errors"
    **`SYMCFG-00001: Symmetrix ID not found or not responding`** — Verify the Symmetrix array is online and accessible by running `symcfg discover` and confirm the array ID matches your environment.
    **`SYMRDF-00015: RDFG group 10 not found`** — Confirm the RDFG group number exists on this array by running `symcfg list -rdfg all` to list all configured groups.
    **`Permission denied: /tmp/rdfg_inventory_*.txt`** — Ensure the user running the script has write permissions to /tmp or specify an alternate writable directory like `/var/tmp`.
### Pair State and Data Consistency Validation

![Pair State and Data Consistency Validation](../../../../assets/storage-dell-srdf-s-hc-pair-state-and-data-consistency-validation.svg)

```bash
# Confirm all pairs are Synchronized (0 invalid tracks)
symrdf -g 10 query -detail | grep -E "Pair State|Invalid Tracks"

# Verify SRDF/S mode (not accidentally switched to /A)
symcfg list -rdfg 10 -detail | grep "SRDF Mode"

# Check for any devices in non-protected states
symrdf -g 10 query | grep -iv "synchronized\|transmit idle"

# Validate device count matches expected configuration
symrdf -g 10 list -v | grep -c "R1"

# Cross-check R2 array shows matching device count
symrdf -sid 0002 -g 10 list -v | grep -c "R2"
```


```text title="Expected output"
Pair State                                    Synchronized
Invalid Tracks                                0
Pair State                                    Synchronized
Invalid Tracks                                0
SRDF Mode                                     Synchronous
(no output — all devices in expected states)
47
47
```

!!! warning "Common errors"
    **`symrdf: Command not found`** — Ensure the Symmetrix CLI tools are installed and the `$PATH` includes the Solutions Enabler bin directory (typically `/opt/emc/SYMCLI/bin`).
    **`SRDF group 10 not found`** — Verify the RDF group number with `symrdf list` and confirm the group exists on both R1 and R2 arrays.
    **`Device count mismatch between R1 and R2`** — Run `symrdf -g 10 query -detail` to identify which devices are out of sync, then resynchronize using `symrdf -g 10 -i set -state synchronized`.
### Simulated Failover Validation (Non-Disruptive)

![Simulated Failover Validation (Non-Disruptive)](../../../../assets/storage-dell-srdf-s-hc-simulated-failover-validation-non-disruptive.svg)

A non-disruptive test verifies that the failover command succeeds without actually transferring production I/O. Use `symrdf -testmode` where available, or perform a suspend/resume cycle to confirm link responsiveness:

```bash
# Suspend all pairs (simulates loss of sync link — non-destructive)
symrdf -g 10 -type S suspend -noprompt

# Confirm Suspended state
symrdf -g 10 query

# Resume and verify re-synchronization completes
symrdf -g 10 -type S resume -noprompt

# Wait for Synchronized and confirm 0 tracks
symrdf -g 10 query -detail | grep "Invalid Tracks"
```


```text title="Expected output"
Suspend all pairs (simulates loss of sync link — non-destructive)
Suspending RDF pair(s)...
RDF pair(s) successfully suspended.

Confirm Suspended state
Group Number: 10
   Pair#  LocalDev   RemoteDev  Status      RDF Mode  Tracks
   0      000EF     000EF      Suspended   Synchronous  0
   1      000F0     000F0      Suspended   Synchronous  0
   2      000F1     000F1      Suspended   Synchronous  0

Resume and verify re-synchronization completes
Resuming RDF pair(s)...
RDF pair(s) successfully resumed.

Wait for Synchronized and confirm 0 tracks
   Invalid Tracks: 0
   Invalid Tracks: 0
   Invalid Tracks: 0
```

!!! warning "Common errors"
    **`SYMAPI_C_PROC_FAILURE (29) — Symmetrix device not responding`** — Verify the Symmetrix array is online and accessible via `symcfg list -v`, and confirm network connectivity to the array.
    **`RDF pair(s) could not be suspended — Pair(s) in Invalid state`** — Check pair status with `symrdf -g 10 query` and resolve any failed pairs before attempting suspend operations.
    **`symrdf: Command authorization failed`** — Ensure your user account has appropriate SYMAPI permissions; contact your storage administrator to grant RDF management privileges.
For a full DR test failover, follow the DR test runbook and use the SRM test failover workflow to isolate impact to the test bubble network.

### Post-Change Validation

![Post-Change Validation](../../../../assets/storage-dell-srdf-s-hc-post-change-validation.svg)

After any SRDF configuration change (adding devices, changing RDFG membership, link maintenance):

```bash
# Confirm new devices appear in group query
symrdf -g 10 list -v

# Confirm all devices reach Synchronized within SLA window
symrdf -g 10 query -detail

# Check no unexpected devices are in Suspended or Split state
symrdf -g 10 query | grep -iv "synchronized\|syncInProg"

# Confirm OLPAIRS configuration is intact
symrdf -g 10 query -detail | grep OLPAIRS
```


```text title="Expected output"
Group ID: 10
Device Name           Index  Symmetrix ID       R1 Cap   R2 Cap   State
DEV001               0000   000123456789ABCD   100 GB   100 GB   Synchronized
DEV002               0001   000123456789ABCD   100 GB   100 GB   Synchronized
DEV003               0002   000123456789ABCD   100 GB   100 GB   Synchronized
DEV004               0003   000123456789ABCD   100 GB   100 GB   Synchronized
DEV005               0004   000123456789ABCD   100 GB   100 GB   Synchronized

Group ID: 10, Symmetrix ID: 000123456789ABCD
Device Name           Index  R1 State          R2 State          RDF Mode   Consistency
DEV001               0000   Synchronized      Synchronized      Synchronous   Yes
DEV002               0001   Synchronized      Synchronized      Synchronous   Yes
DEV003               0002   Synchronized      Synchronized      Synchronous   Yes
DEV004               0003   Synchronized      Synchronized      Synchronous   Yes
DEV005               0004   Synchronized      Synchronized      Synchronous   Yes

(no output — all devices in expected state)

OLPAIRS Configuration: Enabled
OLPAIRS Mode: Active
OLPAIRS Consistency: Maintained
```

!!! warning "Common errors"
    **`symrdf: Command not found`** — Verify SymCLI is installed and the Symmetrix CLI bin directory is in your $PATH.
    **`Group ID 10 not found`** — Confirm the RDF group number exists with `symrdf list` and verify you have permissions to access the Symmetrix array.
    **`SYMAPI_CONNECT_ERROR: Cannot connect to the Symmetrix`** — Ensure the Symmetrix array is reachable and the SYMAPI_SERVER environment variable is correctly configured.
### Validation Checklist Table

![Validation Checklist Table](../../../../assets/storage-dell-srdf-s-hc-validation-checklist-table.svg)

| Validation Item | Command | Pass Criteria |
|---|---|---|
| All pairs Synchronized | `symrdf -g <rdfg> query` | State = Synchronized |
| Zero invalid tracks | `symrdf -g <rdfg> query -detail` | Invalid Tracks = 0 |
| SRDF mode is /S | `symcfg list -rdfg <n> -detail` | Mode = Synchronous |
| RDF directors Online | `symcfg list -dir all -rdf` | All directors Online |
| Device count matches design | `symrdf -g <rdfg> list -v` | Count matches CMDB |
| Remote array reachable | `symcfg list -rdfg <n> -detail` | Link Online |
| Resync completes within SLA | Monitor `SyncInProg` duration | < agreed RTO window |

### Known Issues and Field Notes (Validation)

![Known Issues and Field Notes (Validation)](../../../../assets/storage-dell-srdf-s-hc-known-issues-and-field-notes-validation.svg)

- **Validation script shows false positives during scheduled snapshots**: TimeFinder/SnapVX operations on R1 devices can briefly increase track counts. Schedule validation runs outside snapshot windows.
- **Device count mismatch between arrays**: If R1 and R2 show different device counts, the RDFG was likely modified on one array without the corresponding change on the other. Open a Dell support case immediately — do not attempt manual corrections.
- **SRDF mode shows "Adaptive Copy" instead of "Synchronous"**: This indicates the array temporarily switched to adaptive copy mode due to link congestion. Review link utilization history and correct mode with `symrdf -g <rdfg> -type S set mode synchronous`.
- **Post-DR-test validation shows Suspended pairs**: SRM test failover with array-based replication uses a test bubble snapshot, not a real failover. If pairs appear Suspended after cleanup, run `symrdf -g <rdfg> -type S resume -noprompt` and verify they return to Synchronized.

---

## Verify

- `symrdf query` shows all devices in `Synchronized` state (not `Suspended` or `SyncInProg`)
- `symstat -type rdf -i 5 -c 3` shows 0 KB invalid tracks under normal load
- No RDFG-related critical alerts in Unisphere
- Link utilisation is within expected baseline — no sustained spikes above 80%

---

## See also

- [Srdf S — Procedures](../procedures/)
- [Srdf S — CLI Reference](../cli-reference/)
- [Srdf S — Common Issues](../../troubleshooting/common-issues/)
