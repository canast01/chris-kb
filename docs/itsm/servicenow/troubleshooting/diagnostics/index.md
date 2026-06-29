---
tags:
  - servicenow
  - troubleshooting
search:
  boost: 1.5
---
# ServiceNow — Diagnostics

<div class="kb-summary">
ServiceNow diagnostic tools: check instance health and thread state via stats.do, inspect live DB queries in the DB Activity Monitor, run the System Diagnostics self-test suite, tail MID Server agent logs, enable per-session debug tracing, and collect instance and log information for ServiceNow HI support tickets.

*Applies to: ServiceNow Washington / Xanadu*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "stats.do — check thread count and queue depth\nthread_monitor.do — look for blocked threads" {shape: rectangle}
D: "DB Activity Monitor for live queries\nSlow Queries log for historical > 10 sec" {shape: rectangle}
E: "ECC Queue in UI for error state messages\nMID server: tail agent0.log.0" {shape: rectangle}
F: "System Logs > All — filter by source and time\nSession Debug for per-session BR trace" {shape: rectangle}
G: "System Diagnostics for self-test suite\nCheck failed scheduler jobs: sysauto table" {shape: rectangle}
H: "Background Script diagnostic snapshot\nSystem Diagnostics > Diagnostics self-test" {shape: rectangle}
I: "I" {shape: rectangle}
J: "Identify blocking transaction and table\nDisable offending Business Rule if causing lock" {shape: rectangle}
K: "Scale check: contact ServiceNow support for node\ncapacity\nIdentify runaway scheduled job or report" {shape: rectangle}
L: "Identify slow query table and condition\nRequest index via HI portal for cloud instances" {shape: rectangle}
M: "Check MID server connectivity to instance\nVerify MID server credentials: test connection in UI" {shape: rectangle}
N: "Session Debug: enable SQL and BR trace\nReproduce issue and check session debug log" {shape: rectangle}
O: "Sysauto table: filter state=error\nWorkflow Contexts for stuck workflows" {shape: rectangle}
P: "Run Background Script snapshot\nCapture stats.do output and attach to ticket" {shape: rectangle}
Q: "Collect stats.do screenshot + thread_monitor + log\nexcerpt\nOpen ServiceNow HI support ticket" {shape: rectangle}
R: "Provide: instance name, version, affected node\nRepro steps, log excerpts, stats.do screenshot" {shape: rectangle}
A: "ServiceNow Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
I -> J
I -> K
D -> L
E -> M
F -> N
G -> O
H -> P
J -> Q
K -> Q
L -> Q
M -> Q
N -> Q
O -> Q
P -> Q
Q -> R
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_instance_health_via_sta: "Step 1 — Check instance health via stats.do" {shape: rectangle}
step_2_inspect_db_activity_monitor_f: "Step 2 — Inspect DB Activity Monitor for slow queries" {shape: rectangle}
step_3_run_system_diagnostics_selfte: "Step 3 — Run System Diagnostics self-test" {shape: rectangle}
step_4_review_application_and_mid_se: "Step 4 — Review application and MID Server logs" {shape: rectangle}
step_5_enable_session_debug_for_targ: "Step 5 — Enable Session Debug for targeted\ninvestigation" {shape: rectangle}
step_6_run_background_script_diagnos: "Step 6 — Run Background Script diagnostic snapshot" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_instance_health_via_sta: investigate
symptom -> step_2_inspect_db_activity_monitor_f: investigate
symptom -> step_3_run_system_diagnostics_selfte: investigate
symptom -> step_4_review_application_and_mid_se: investigate
symptom -> step_5_enable_session_debug_for_targ: investigate
symptom -> step_6_run_background_script_diagnos: investigate
step_1_check_instance_health_via_sta -> resolution
step_2_inspect_db_activity_monitor_f -> resolution
step_3_run_system_diagnostics_selfte -> resolution
step_4_review_application_and_mid_se -> resolution
step_5_enable_session_debug_for_targ -> resolution
step_6_run_background_script_diagnos -> resolution
```

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "Diagnostics \u2014 Thresholds",
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
        "metric": "Heap used",
        "zone": "Safe",
        "val": 85
      },
      {
        "metric": "Heap used",
        "zone": "Alert",
        "val": 15
      },
      {
        "metric": "DB pool usage",
        "zone": "Safe",
        "val": 90
      },
      {
        "metric": "DB pool usage",
        "zone": "Alert",
        "val": 10
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

- **Access:** ServiceNow admin role; MID Server host SSH access (for integration issues)
- **Gather first:** the specific symptom (slow page, script error, integration failure, scheduled job failing), the affected table or module name, and the time window when the issue occurred
- **Scope:** confirm whether the issue affects one user, one instance node, one integration, or all users

---

## Step 1 — Check instance health via stats.do

The Stats page is the first place to check during any performance issue. It surfaces real-time system health.

```text
Access: https://<instance>.service-now.com/stats.do
```

Key metrics to check:

| Metric | Location in stats.do | Problem Threshold |
|---|---|---|
| Heap used | System Information → Memory | > 85% of max heap |
| Active threads | System Information → Threads | Near max (typically 200+) |
| Request queue depth | System Information → Requests | > 50 queued requests |
| DB pool usage | Database → Connection Pool | > 90% of pool connections |
| Semaphore wait | System Information → Semaphores | Any semaphore with large wait count |

```bash
# Retrieve instance metrics via REST API
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/now/table/sys_properties?sysparm_query=nameLIKEglide.buildtag&sysparm_fields=name,value" \
  -H "Accept: application/json" | python3 -m json.tool

# Check MID server status via API
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/now/table/ecc_agent?sysparm_fields=name,status,version&sysparm_query=status!=Up" \
  -H "Accept: application/json" | python3 -m json.tool
# Expected: empty results (all MID servers Up)
```


```text title="Expected output"
{
  "result": [
    {
      "name": "glide.buildtag",
      "value": "jakarta-12-20231215"
    }
  ]
}
{
  "result": [
    {
      "name": "mid-server-prod-01",
      "status": "Down",
      "version": "5.0.4"
    },
    {
      "name": "mid-server-dr-02",
      "status": "Restricted",
      "version": "5.0.3"
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: dev12345.service-now.com`** — Verify `$SN_INSTANCE` is set correctly and the instance hostname is accessible from your network.
    **`{"error":{"message":"Invalid table API (ecc_agent)","status":"failure"},"status":"failure"}`** — Confirm your ServiceNow user has Table API access and the table name is correct (check instance version compatibility).
    **`jq: parse error: Invalid JSON at line 1`** — Ensure the API response is valid JSON by removing `-m json.tool` temporarily and checking the raw response for authentication or permission errors.
---

## Step 2 — Inspect DB Activity Monitor for slow queries

```text
Navigate to: System Diagnostics > DB Activity Monitor
```

Key columns:

| Column | Meaning |
|---|---|
| Duration (ms) | Query execution time |
| Table | Target table |
| SQL | Query text (may be truncated) |
| User | ServiceNow user who triggered the query |
| Business Rule | Script that initiated the query |

```text
Slow query log: System Diagnostics > Slow Queries
```

ServiceNow logs queries exceeding 10 seconds. For persistent slow queries:

1. Identify the table and query condition from the Slow Queries log
2. Check if an index exists: System Definition > Tables & Columns → select table → Indexes tab
3. Add a composite index if missing (requires HI request for cloud instances)
4. For immediate relief: identify the Business Rule or report causing the query and disable it

---

## Step 3 — Run System Diagnostics self-test

```text
Navigate to: System Diagnostics > Diagnostics
```

The self-test suite checks:

- Database connectivity
- Scheduler health
- Email configuration
- MID Server connectivity
- File system access
- Session manager

Results appear as Pass, Warning, or Fail. Screenshot and attach to any support ticket.

---

## Step 4 — Review application and MID Server logs

### Application logs (in-UI access only for SaaS instances)

| Log | Navigation Path | Content |
|---|---|---|
| Application log | System Logs > All | All app events, errors, warnings |
| Script log | System Logs > Script Log Statements | `gs.log()` / `gs.error()` output |
| Email log | System Logs > Emails | Outbound email delivery log |
| Transaction log | System Diagnostics > Transactions | Per-request timing data |
| ECC Queue log | MID Server > ECC Queue | MID-instance message bus errors |
| Workflow log | Workflow > Workflow Contexts | Workflow execution history |

### MID Server logs (on-premises host)

```bash
# Linux MID Server: tail for errors
tail -500 /opt/servicenow/mid/agent/logs/agent0.log.0 | grep -i "error\|exception\|failed"

# Watch live log
tail -f /opt/servicenow/mid/agent/logs/agent0.log.0

# Auth failures (wrong credentials)
grep -i "401\|unauthorized\|invalid credentials" /opt/servicenow/mid/agent/logs/agent0.log.0

# Connectivity issues (unreachable instance)
grep -i "connection refused\|timeout\|unreachable" /opt/servicenow/mid/agent/logs/agent0.log.0
```


```text title="Expected output"
2024-01-15 14:32:18,445 ERROR [MIDServer] Connection timeout after 30000ms to instance.service-now.com
2024-01-15 14:32:45,123 ERROR [Executor-8] Exception in probe execution: java.net.SocketTimeoutException
2024-01-15 14:33:02,567 ERROR [HTTPClient] 401 Unauthorized - Invalid credentials for user mid_integration_user
2024-01-15 14:33:18,891 WARN [MIDServer] Retrying connection attempt 3 of 5
2024-01-15 14:34:01,234 ERROR [ProbeScheduler] Failed to execute discovery probe: Connection refused (Connection refused)
2024-01-15 14:34:15,456 ERROR [MIDServer] javax.net.ssl.SSLHandshakeException: CERTIFICATE_VERIFY_FAILED

tail: file /opt/servicenow/mid/agent/logs/agent0.log.0 updated

2024-01-15 14:35:22,789 INFO [MIDServer] Probe execution completed
2024-01-15 14:35:23,012 ERROR [HTTPClient] 401 Unauthorized - Check instance URL and credentials
2024-01-15 14:35:45,234 ERROR [MIDServer] Connection refused connecting to 192.168.1.50:443
2024-01-15 14:36:01,567 ERROR [Executor-12] Timeout waiting for response from instance.service-now.com after 60000ms
```

!!! warning "Common errors"
    **`tail: cannot open '/opt/servicenow/mid/agent/logs/agent0.log.0' for reading: No such file or directory`** — Verify the MID Server installation path and check that the agent is running with `ps aux | grep mid`.
    **`grep: (standard input): Permission denied`** — Run the command with `sudo` or ensure your user has read permissions on the log file with `sudo chmod 644 /opt/servicenow/mid/agent/logs/agent0.log.0`.
    **`tail: inaccessible regular file '/opt/servicenow/mid/agent/logs/agent0.log.0': Permission denied`** — Execute with `sudo tail -f` or add your user to the servicenow group with `sudo usermod -a -G servicenow $USER`.
Log file locations:

- **Linux:** `/opt/servicenow/mid/agent/logs/agent0.log.0` (current), `.log.1` (previous), `agent.err.0` (errors)
- **Windows:** `C:\ServiceNow\MID Server\agent\logs\agent0.log.0`

To increase verbosity, edit `config.xml` — set `loglevel` to `DEBUG` and restart the MID Server service. Reset to `INFO` after debugging.

---

## Step 5 — Enable Session Debug for targeted investigation

Session Debug captures granular diagnostic data for a specific session without impacting other users.

```text
Enable: https://<instance>.service-now.com/session_debug.do
```

Available debug flags:

| Flag | What It Captures |
|---|---|
| Business Rules | BR evaluation per request |
| ACLs | Access control evaluation trace |
| SQL | All database queries for the session |
| GlideRecord | Record read/write operations |
| Scripting | Script execution trace |

After enabling, reproduce the issue. Debug output appears in **System Diagnostics > Session Debug Log**.

**Caution:** SQL debug generates very large output. Enable only for targeted investigation and disable immediately after.

---

## Step 6 — Run Background Script diagnostic snapshot

Navigate to: **System Definition > Scripts - Background**

```javascript
// Run this to capture a key instance diagnostic snapshot
var output = [];

// Instance version and node
output.push('=== Instance Info ===');
output.push('Version: ' + gs.getProperty('glide.buildtag'));
output.push('Node: ' + gs.getNodeName());

// Active sessions
var sessions = new GlideAggregate('sys_user_session');
sessions.addQuery('active', 'true');
sessions.addAggregate('COUNT');
sessions.query();
sessions.next();
output.push('Active sessions: ' + sessions.getAggregate('COUNT'));

// Failed scheduled jobs
var jobs = new GlideAggregate('sysauto');
jobs.addQuery('state', 'error');
jobs.addAggregate('COUNT');
jobs.query();
jobs.next();
output.push('Failed scheduled jobs: ' + jobs.getAggregate('COUNT'));

// MID Servers not Up
var mids = new GlideRecord('ecc_agent');
mids.addQuery('status', '!=', 'Up');
mids.query();
output.push('MID Servers not Up: ' + mids.getRowCount());

// ECC queue errors
var ecc = new GlideAggregate('ecc_queue');
ecc.addQuery('state', 'error');
ecc.addAggregate('COUNT');
ecc.query();
ecc.next();
output.push('ECC Queue errors: ' + ecc.getAggregate('COUNT'));

gs.print(output.join('\n'));
```

---

## Step 7 — Collect support information for HI ticket

```text
ServiceNow support portal: https://hi.service-now.com
```

HI ticket template:

```yaml
Subject: [Instance: mycompany] <Short description>

Instance: mycompany.service-now.com
Version: Xanadu Patch 3
Affected node: (from stats.do System Information)
Time of issue: 2026-06-15 09:15 UTC
Impact: P2 — Department-level degradation

DESCRIPTION:
<What is happening vs expected behavior>

STEPS TO REPRODUCE:
1.
2.

LOGS:
[Paste relevant log excerpts from System Logs > All]

DIAGNOSTICS:
[Attach stats.do screenshot]
[Attach thread_monitor.do screenshot if performance-related]

BUSINESS IMPACT:
<Number of users affected, critical process affected>
```

---

## Log locations

| Source | Path / Tool | What to look for |
|---|---|---|
| Application log | System Logs > All | Script errors, workflow failures |
| Transaction log | System Diagnostics > Transactions | Slow requests (>5 sec) |
| Slow queries | System Diagnostics > Slow Queries | Queries > 10 seconds |
| MID Server | `/opt/servicenow/mid/agent/logs/agent0.log.0` | Auth failures, timeouts |
| ECC Queue | MID Server > ECC Queue | Error state messages |
| Scheduler jobs | `sysauto` table, filter `state=error` | Failed scheduled jobs |

---

## See also

- [ServiceNow — Common Issues](../common-issues/)
- [ServiceNow — Escalation](../escalation/)

## Verify resolution

- `stats.do` shows heap below 85%, thread count normal, queue depth at 0
- DB Activity Monitor shows no queries exceeding 10 seconds
- `GET /api/now/table/ecc_agent?sysparm_query=status!=Up` returns empty results
- The affected Business Rule, workflow, or integration executes successfully on retest
- System Logs > All shows no new Error-level events for the affected source since the fix
