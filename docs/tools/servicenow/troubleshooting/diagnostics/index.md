# ServiceNow — Diagnostic Tools

Reference guide for ServiceNow's built-in diagnostic tools, log file locations, and support information gathering procedures. Use these before engaging ServiceNow support to accelerate resolution.

---

## Diagnostic Tools Overview

| Tool | URL / Path | Purpose |
|---|---|---|
| Stats page | `/stats.do` | Real-time memory, thread, session metrics |
| Thread Monitor | `/thread_monitor.do` | Active Java threads with stack traces |
| DB Activity Monitor | **System Diagnostics > DB Activity Monitor** | Live query analysis |
| System Diagnostics | **System Diagnostics > Diagnostics** | Self-test suite |
| Slow Query Analyzer | **System Diagnostics > Slow Queries** | Historical slow query log |
| Log File Browser | **System Logs > All** | Application event log |
| Node Log Browser | **System Diagnostics > Log File Browser** | Per-node application logs |
| Session Debug | **System Diagnostics > Session Debug** | Per-session tracing |
| Upgrade Monitor | **System Diagnostics > Upgrade Monitor** | Upgrade and patch status |
| MID Server Log Viewer | **MID Server > Logs** | Remote MID Server log access |

---

## Stats Page (`/stats.do`)

The Stats page is the first place to check during any performance issue. It surfaces real-time system health without requiring admin access to the underlying infrastructure.

Access: `https://<instance>.service-now.com/stats.do`

### Key Sections

**System Information:**

```
Instance Build:         Yokohama Patch 5
Node ID:                app-node-02
Instance started:       2026-05-01 03:14:22 UTC
JVM version:            17.0.11
```

**Memory:**

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| Total JVM memory | Varies | — | — |
| Used heap | < 70% | 70–85% | > 85% |
| Free heap | > 30% | 15–30% | < 15% |
| GC overhead | < 5% | 5–15% | > 15% |

**Threads:**

```
Worker threads (busy/total):   12 / 40     <- aim for < 80%
Scheduler threads (running):    3
DB connections (active/max):   18 / 50
```

**Cache Hit Rates:**

| Cache | Healthy Hit Rate |
|---|---|
| Query result cache | > 70% |
| GlideRecord cache | > 80% |
| ACL cache | > 90% |

---

## Thread Monitor (`/thread_monitor.do`)

Shows every active Java thread with current state and stack trace. Use to identify blocked or runaway threads.

Access: `https://<instance>.service-now.com/thread_monitor.do`

### Reading Thread State

| Thread State | Meaning | Action |
|---|---|---|
| RUNNABLE | Executing code | Normal |
| WAITING | Waiting on a lock or condition | Investigate if > 5 minutes |
| BLOCKED | Blocked on a monitor lock | Immediate investigation |
| TIMED_WAITING | Sleeping — waiting for signal | Usually normal (scheduled work) |

### Identifying Problematic Threads

Look for threads showing the same script or Business Rule name repeatedly across multiple calls. This indicates a lock contention or infinite loop.

Example stack trace pattern indicating a Business Rule loop:

```
"GlideWorker-42" BLOCKED
  at com.glide.db.DBSynchronizer.lock(DBSynchronizer.java:...)
  at com.glide.db.DBSynchronizer.acquire(...)
  at com.glide.script.ScriptLoader.loadScript(...)
  ...invoked from: BR_AutoAssignIncidents on incident
```

**Action:** Disable the offending Business Rule and investigate the script logic.

---

## DB Activity Monitor

Shows live database query activity. Access via **System Diagnostics > DB Activity Monitor**.

### Key Columns

| Column | Meaning |
|---|---|
| Duration (ms) | Query execution time |
| Table | Target table |
| SQL | Query text (may be truncated) |
| User | ServiceNow user who triggered the query |
| Business Rule | Script that initiated the query |

### Slow Query Threshold

ServiceNow logs queries exceeding 10 seconds to the Slow Query log. Access via **System Diagnostics > Slow Queries**.

For persistent slow queries:

1. Identify the table and query condition
2. Check if an index exists: **System Definition > Tables & Columns** → select table → **Indexes** tab
3. Add a composite index if one is missing (requires ServiceNow support for cloud instances — raise an HI request)

---

## System Diagnostics Module

Navigate to: **System Diagnostics > Diagnostics**

Runs a self-test suite covering:

- Database connectivity
- Scheduler health
- Email configuration
- MID Server connectivity
- File system access
- Session manager

Results are categorized as **Pass**, **Warning**, or **Fail**. Screenshot and attach to any support ticket.

---

## Log File Locations

### Application Logs (accessed via UI)

ServiceNow cloud instances do not expose raw file system access. Logs are accessed through the UI.

| Log | Navigation Path | Content |
|---|---|---|
| Application log | **System Logs > All** | All app events, errors, warnings |
| Script log | **System Logs > Script Log Statements** | `gs.log()` / `gs.error()` output |
| Email log | **System Logs > Emails** | Outbound email delivery log |
| Transaction log | **System Diagnostics > Transactions** | Per-request timing data |
| Import Set log | **System Import Sets > Transform Log** | Transform execution details |
| Workflow log | **Workflow > Workflow Contexts** | Workflow execution history |
| ECC Queue log | **MID Server > ECC Queue** | MID-instance message bus |

### MID Server Logs (on-premises)

MID Server logs are stored on the host running the MID Server agent.

**Linux:**

```
/opt/servicenow/mid/agent/logs/
├── agent0.log.0          # Current log (active)
├── agent0.log.1          # Previous rotation
├── agent0.log.2
└── agent.err.0           # Error output stream
```

**Windows:**

```
C:\ServiceNow\MID Server\agent\logs\
├── agent0.log.0
├── agent0.log.1
└── agent.err.0
```

**Common log search commands:**

```bash
# Find all ERROR lines in the last 500 lines
tail -500 /opt/servicenow/mid/agent/logs/agent0.log.0 | grep -i "error\|exception\|failed"

# Watch live log
tail -f /opt/servicenow/mid/agent/logs/agent0.log.0

# Find authentication failures
grep -i "401\|unauthorized\|invalid credentials" /opt/servicenow/mid/agent/logs/agent0.log.0

# Find connectivity issues
grep -i "connection refused\|timeout\|unreachable" /opt/servicenow/mid/agent/logs/agent0.log.0
```

### Increasing MID Server Log Verbosity

Edit `/opt/servicenow/mid/agent/config.xml`:

```xml
<!-- Change INFO to DEBUG for verbose output -->
<parameter name="loglevel" value="DEBUG"/>
```

Restart the MID Server service after changing. Remember to set back to `INFO` after debugging — DEBUG logs are verbose and fill disk quickly.

---

## Session Debug

Enable detailed debug output for a specific session without affecting all users.

Navigate to: **System Diagnostics > Session Debug**

Available debug options:

| Option | What It Captures |
|---|---|
| Business Rules | BR evaluation per request |
| ACLs | Access control evaluation trace |
| SQL | All database queries for the session |
| GlideRecord | Record read/write operations |
| Scripting | Script execution trace |

**To enable for your own session:**

```
https://<instance>.service-now.com/session_debug.do
```

Check the desired debug flags, then reproduce the issue. Debug output appears inline on pages or in **System Diagnostics > Session Debug Log**.

**Caution:** SQL debug generates very large output. Only enable for targeted investigation and disable immediately after.

---

## Support Information Gathering

When raising a ServiceNow support ticket, gather the following before submitting:

### Instance Information

```bash
# Retrieve via API
curl -s -u "$SN_USER:$SN_PASS" \
  "$SN_INSTANCE/api/now/table/sys_properties?sysparm_query=nameLIKEglide.buildtag&sysparm_fields=name,value" \
  -H "Accept: application/json" | jq '.result[] | {name, value}'
```

- Instance name and URL
- Current version and patch level (visible on `stats.do`)
- Affected node ID(s) (visible on `stats.do` under System Information)

### Reproducing the Issue

- Exact steps to reproduce
- User account used (provide a test account if possible)
- Time of occurrence (UTC)
- Expected vs. actual behavior

### Log Excerpts

From **System Logs > All** — filter to the time window of the issue, export as CSV or copy the relevant error messages.

### Diagnostic Screenshots

- `stats.do` output at time of issue (or closest available)
- Thread Monitor (`thread_monitor.do`) if performance-related
- System Diagnostics results if available

### HI Portal Ticket Template

```
Subject: [Instance: mycompany] <Short description of issue>

Instance: mycompany.service-now.com
Version: Yokohama Patch 5
Affected node: app-node-02 (if known)
Time of issue: 2026-05-08 09:15 UTC
Impact: P2 — Department level degradation

DESCRIPTION:
<What is happening, what the expected behavior is>

STEPS TO REPRODUCE:
1.
2.
3.

LOGS:
[Paste relevant log excerpts]

DIAGNOSTICS:
[Attach stats.do screenshot]
[Attach thread_monitor.do screenshot if relevant]

BUSINESS IMPACT:
<Number of users affected, business processes impacted>
```

---

## Diagnostic Script — Instance Snapshot

Run this Background Script to capture a diagnostic snapshot:

```javascript
// Navigate to: System Definition > Scripts - Background
// Run this to capture key instance metrics

var output = [];

// Instance version
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

// MID Server status
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
