# ServiceNow — Common Issues


<div class="kb-summary">
Quick-reference troubleshooting guide for frequently encountered ServiceNow operational problems. Each issue includes symptoms, root causes, diagnostic steps, and resolution procedures.
</div>

---

## Issue Index

| # | Issue | Severity | Typical Cause |
|---|---|---|---|
| 1 | [Slow instance performance](#1-slow-instance-performance) | P2–P3 | High query load, runaway script |
| 2 | [MID Server disconnected](#2-mid-server-disconnected) | P2 | Network, service crash, auth failure |
| 3 | [LDAP sync failures](#3-ldap-sync-failures) | P2–P3 | Connectivity, expired credentials |
| 4 | [Workflow / Flow stalled](#4-workflow-flow-stalled) | P2–P3 | Unhandled error, condition loop |
| 5 | [Import set failures](#5-import-set-failures) | P3 | Transform map error, data validation |
| 6 | [Email notification failures](#6-email-notification-failures) | P2–P3 | SMTP config, template error, flood control |
| 7 | [Scheduled job failures](#7-scheduled-job-failures) | P2–P3 | Script error, resource contention |

---

## 1. Slow Instance Performance

### Symptoms

- Pages taking > 5 seconds to load
- `stats.do` showing high memory usage or blocked threads
- Users reporting timeouts on form saves or list views
- REST API calls returning slowly or timing out

### Common Root Causes

| Cause | Indicator |
|---|---|
| Runaway Business Rule or Script | Thread Monitor shows same script blocking repeatedly |
| Large unindexed query | DB activity monitor shows full table scans |
| Spike in active sessions (e.g., import job) | Session count 3x above baseline |
| Heap exhaustion → GC pressure | Heap usage > 85% on `stats.do` |
| Slow external REST call (outbound, synchronous) | Threads blocked waiting on HTTP response |

### Diagnostic Steps

1. Navigate to `https://<instance>.service-now.com/stats.do`
2. Check **Heap** — if > 85%, open a P2 incident and contact ServiceNow support
3. Open **Thread Monitor** (`thread_monitor.do`) — identify threads in WAIT/BLOCKED state
4. Navigate to **System Diagnostics > DB Activity Monitor** — identify slow queries (> 5s)
5. Check **System Logs > All** with filter `level=error` for recent stack traces

### Resolution

```javascript
// To find long-running transactions, run in Background Scripts:
var gr = new GlideRecord('sys_running_transaction');
gr.query();
while (gr.next()) {
    gs.print(gr.getValue('name') + ' | ' + gr.getValue('duration') + ' | ' + gr.getValue('thread'));
}
```
┌────────────────────────────────────── ServiceNow Common Issues ───────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │                Login / Access                │                                                    │
│   │       SSO redirect loop → clear cookie       │                                                    │
│   │        Account locked → admin unlock         │                                                    │
│   │       No role → check group membership       │                                                    │
│   │        MFA failure → reset TOTP seed         │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │                 Performance                 │   │
│                                                     │         Slow list → add table index         │   │
│                                                     │         Form loads slow → GlideAjax         │   │
│                                                     │       High memory → review sched jobs       │   │
│                                                     │        Timeout → semaphore leak check       │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │                 Integration                  │                                                    │
│   │        REST fails → check ECC errors         │                                                    │
│   │        MID offline → restart service         │                                                    │
│   │         LDAP sync fail → bind creds          │                                                    │
│   │         Email not sent → SMTP config         │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │               Workflow / ITSM               │   │
│                                                     │       Stuck approval → manual reassign      │   │
│                                                     │       SLA not running → check timezone      │   │
│                                                     │          Notif not sent → event log         │   │
│                                                     │       Cat item error → variable check       │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS · MID server · SMTP relay · LDAP/AD servers · IdP                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SSO redirect loop= SAML response rejected; clear browser cookies and retry                           │
│  GlideAjax  = client-server script framework; slow calls block form rendering                         │
│  Semaphore  = thread lock; leaked semaphore holds thread pool causing timeouts                        │
│  ECC queue  = integration message queue; error state shows failed REST/SOAP calls                     │
│  MID server = on-prem agent; must be running and connected to instance                                │
│  Bind creds = LDAP service account credentials; rotation requires UI update                           │
│  Event log  = sys_event table; notification triggers logged here for debug                            │
│  Cat item   = service catalog item; variable errors prevent form submission                           │
│  SLA timezone= SLA schedule uses instance timezone; mismatch causes wrong calc                        │
│  TOTP seed  = secret key for authenticator app; reset via admin user record                           │
│  Table index= DB index on column; missing index on filter field causes slow lists                     │
│  Sched jobs = background scheduled tasks; excessive jobs starve user threads                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

## 2. MID Server Disconnected

### Symptoms

- MID Server status shows **Down** or **Unvalidated** in **MID Server > MID Servers**
- Discovery jobs failing with "No MID Server available" error
- ECC Queue input records accumulating with no processing

### Common Root Causes

| Cause | Indicator |
|---|---|
| MID Server service stopped | Service not running on the host |
| Credential change not propagated | 401 Unauthorized in MID Server log |
| JVM out of memory | OOM error in `agent0.log.0` |
| Network change blocking HTTPS | Connection timeout to instance URL |
| MID Server version mismatch after upgrade | Validation failure in MID Server record |

### Diagnostic Steps

```powershell
# Windows — check service
Get-Service -Name "ServiceNow MID Server_*"
Get-Content "C:\ServiceNow\MID Server\agent\logs\agent0.log.0" -Tail 50
```

### Resolution

1. **If service is down:** `sudo systemctl start mid-server` (Linux) or `Start-Service` (Windows)
2. **If 401/credential errors:** Reset the MID Server password in ServiceNow (**MID Server > MID Servers** > select record > **Reset Password**), then update `config.xml` on the host:
   ```xml
   <parameter name="mid.instance.password" value="new-password"/>
   ```
3. **If JVM OOM:** Increase heap in MID Server wrapper config (`wrapper.java.maxmemory=4096`)
4. **After restart:** Allow 2–5 minutes for the MID Server to reconnect and validate
5. **If persistent:** Purge old ECC Queue Output records, then re-validate the MID Server from the instance UI

---

## 3. LDAP Sync Failures

### Symptoms

- New users not appearing in ServiceNow after AD onboarding
- **System LDAP > LDAP Listener Log** shows errors
- Scheduled LDAP import job in Error state

### Common Root Causes

| Cause | Indicator |
|---|---|
| Service account password expired | `LDAP: Invalid credentials` in listener log |
| LDAP server certificate expired | `SSL handshake failure` |
| Base DN changed | `No such object` error |
| LDAP server unreachable | Connection timeout |
| Schema mismatch | Attribute mapping error in transform |

### Diagnostic Steps

1. Navigate to **System LDAP > LDAP Listener Log** — review most recent entries
2. Navigate to **System LDAP > LDAP Servers** — click **Test Connection** on each configured server
3. Check the scheduled job: **System Scheduler > Scheduled Jobs** — filter for `LDAP Import`
4. Review **System Logs > All** filtered to the import job execution time

### Resolution

- **Password expired:** Update credentials in **System LDAP > LDAP Server** and rotate the service account password in AD
- **Certificate expired:** Import the new CA certificate: **System Definition > Certificates > Import**
- **Base DN changed:** Update the **Base DN** field in **System LDAP > LDAP OU Definitions**
- **Connectivity:** Verify firewall rules allow TCP/636 (LDAPS) from ServiceNow IP ranges to the LDAP server. ServiceNow publishes outbound IP ranges in the HI portal

After fixing the root cause, trigger a manual import: **System LDAP > LDAP Servers** > **Import Now**.

---

## 4. Workflow / Flow Stalled

### Symptoms

- Change requests, incidents, or requests stuck in a state indefinitely
- No assignment notification sent
- Approval notifications not firing

### Common Root Causes

| Cause | Indicator |
|---|---|
| Unhandled exception in a script activity | Workflow context shows Error state |
| Approval group has no members | Approval waiting indefinitely |
| Wait for condition never satisfied | Context stuck in Wait state |
| Missing role on approver | Approver cannot see approval request |
| Flow Designer trigger not firing | No flow execution history |

### Diagnostic Steps

**Legacy Workflow:**

1. Open the record (incident, change, etc.)
2. Related links: **Workflow Context** (if available) or navigate to **Workflow > Workflow Contexts**
3. Filter by `workflow_version STARTSWITH <workflow-name>`
4. Inspect context state; click **Activities** tab to see where execution stopped
5. Check **System Logs** for JavaScript errors matching the workflow execution time

**Flow Designer:**

1. Navigate to **Process Automation > Flow Designer**
2. Click **Executions** tab
3. Filter by trigger table and record `sys_id`
4. Expand the failed execution to see the exact step and error

### Resolution

- **Script error:** Fix the script in the workflow/flow activity; restart the context from the failed step (right-click activity > **Restart from here**)
- **Empty approval group:** Add members to the approval group or update the approval routing logic
- **Stuck context:** Navigate to the context record, set **State = Cancelled**, then re-trigger the workflow from the record: **Workflow > Restart Workflow**
- **Flow error:** Click the failed execution > **Retry** after fixing the underlying issue

---

## 5. Import Set Failures

### Symptoms

- Import Set shows **Error** or **Ignored** records
- CMDB CIs not created or updated after import
- Transform Map log shows coalesce field mismatch

### Common Root Causes

| Cause | Indicator |
|---|---|
| Coalesce field value missing in source data | `Coalesce field is empty` in transform log |
| Field length exceeded | Database error in transform log |
| Required field missing | Record not inserted; error logged |
| Transform script exception | JavaScript error in transform log |
| Duplicate coalesce match | Multiple target records found |

### Diagnostic Steps

1. Navigate to **System Import Sets > Import Sets**
2. Open the failing import set
3. Click **Transform Log** — review Error entries
4. Check the **Transform Map** for the staging table: **System Import Sets > Transform Maps**
5. Test with a single record: use **Test Transform** button on the Transform Map

### Resolution

- **Coalesce mismatch:** Ensure source data always includes the coalesce field value (e.g., `name`, `ip_address`); adjust the Transform Map coalesce setting if the field changed
- **Field length:** Truncate the source value in the transform script: `answer = source.u_long_field.substring(0, 255);`
- **Script error:** Debug via **Test Transform** with a sample record; fix the field map script
- **Cleanup:** Import set staging data accumulates — run the **Import Set Cleanup** scheduled job or purge manually: **System Import Sets > Import Sets** > bulk delete processed records older than 30 days

---

## 6. Email Notification Failures

### Symptoms

- Users not receiving expected notifications
- Incident assignment emails not sending
- **System Mailboxes > Sent** shows no outbound messages

### Common Root Causes

| Cause | Indicator |
|---|---|
| SMTP relay unreachable | **System Mailboxes > Outgoing** shows error |
| Email flood control triggered | Notification suppressed in system log |
| Notification condition not met | Notification rule filter incorrect |
| User email address blank/invalid | Email not generated for recipient |
| Email script template error | JavaScript error in notification log |
| Instance-level email disabled | `glide.email.smtp.active = false` |

### Diagnostic Steps

1. Navigate to **System Mailboxes > Outgoing** — check for SMTP connection errors
2. Navigate to **System Log > Emails** — search for the specific notification
3. Check `glide.email.smtp.active` in **System Properties > Email**:
   ```
   https://<instance>.service-now.com/nav_to.do?uri=sys_properties_list.do?sysparm_query=name=glide.email.smtp.active
   ```
4. Open the relevant Notification rule (**System Notification > Email > Notifications**) and click **Preview** to test against a specific record

### Resolution

- **SMTP down:** Verify SMTP relay connectivity; update **System Mailboxes > Outgoing** settings
- **Email disabled on sub-production:** This is correct — do not enable production-equivalent email on Dev/UAT. Use a test mailbox address instead
- **Flood control:** Review `glide.email.max_emails_per_event` property; temporarily increase if legitimate volume is being suppressed
- **Notification condition:** Use **Preview Notification** to verify the condition evaluates true for the target record; fix the filter if needed
- **Recipient missing email:** Fix user record; emails will send on next notification event

---

## 7. Scheduled Job Failures

### Symptoms

- Scheduled job in **Error** state in **System Scheduler > Scheduled Jobs**
- Background processes not completing (LDAP, import, cleanup, report)
- System log shows JavaScript error at expected job execution time

### Common Root Causes

| Cause | Indicator |
|---|---|
| Script exception | JavaScript stack trace in system log |
| Transaction timeout (> 30s) | `Transaction cancelled: max transaction time exceeded` |
| Database constraint violation | SQL error in log |
| External dependency unavailable | REST/SOAP call fails inside job |
| Concurrent job collision | Lock contention in log |

### Diagnostic Steps

1. Navigate to **System Scheduler > Scheduled Jobs** — open the failed job
2. Click **Log Messages** related link to view execution log
3. Navigate to **System Logs > All** and filter to the job's last run timestamp
4. Check if the error is transient (network hiccup) or persistent (script bug)

### Resolution

- **Script exception:** Review the script in the job definition. Use Background Scripts to test in isolation:
  ```javascript
  // Test a specific scheduled job function
  var job = new GlideRecord('sysauto_script');
  job.get('name', 'My Failing Job');
  gs.print('Script: ' + job.getValue('script'));
  // Then run the script manually
  ```
- **Transaction timeout:** Break the job into smaller batches using `GlideRecord.setLimit()` or process via chunks with an offset
- **External dependency:** Add try/catch around the external call; log the failure and allow the job to complete gracefully
- **After fixing:** Manually trigger the job (**Execute Now** button) to confirm the fix before the next scheduled run
