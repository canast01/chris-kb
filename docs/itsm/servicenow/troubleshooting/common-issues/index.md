---
tags:
  - servicenow
  - troubleshooting
search:
  boost: 1.5
---
# ServiceNow Common Issues

```javascript
// To find long-running transactions, run in Background Scripts:
var gr = new GlideRecord('sys_running_transaction');
gr.query();
while (gr.next()) {
    gs.print(gr.getValue('name') + ' | ' + gr.getValue('duration') + ' | ' + gr.getValue('thread'));
}
```

```bash
# Linux — check if MID service is running
systemctl status mid-server
journalctl -u mid-server -n 50

# Check wrapper.log for auth or connectivity errors
tail -100 /opt/servicenow/mid/agent/logs/wrapper.log | grep -i "error\|warn\|401\|connect"

# Verify connectivity to instance
curl -sk https://<instance>.service-now.com/api/now/table/sys_user?sysparm_limit=1 -o /dev/null -w "%{http_code}\n"
```
```powershell
# Windows — check service
Get-Service -Name "snc_mid" | Select-Object Status, StartType
Start-Service -Name "snc_mid"

# View recent log lines
Get-Content "C:\ServiceNow\MID Server\agent\logs\wrapper.log" -Tail 50 | Select-String "ERROR|WARN|401"
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "Login and Access\n— review ACL conditions in sys_security_acl" {shape: rectangle}
R2: "Login and Access\n— add required role to user or group" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Workflow and ITSM\n— manually reassign stuck approval" {shape: rectangle}
R4: "Workflow and ITSM\n— check SLA timezone and schedule config" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "Integration\n— assign rest_api_explorer or specific role" {shape: rectangle}
R6: "Integration\n— check ECC queue for error state messages" {shape: rectangle}
D4: "D4" {shape: rectangle}
R7: "Integration\n— restart MID server service" {shape: rectangle}
R8: "Workflow and ITSM\n— check scheduled job log in sys_job" {shape: rectangle}
B5: "B5" {shape: rectangle}
R9: "Integration\n— check transform map field mappings" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}
B4: "B4" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
D4 -> R7
D4 -> R8
B5 -> R9
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Servicenow — Diagnostics](../diagnostics/)
- [Servicenow — Escalation](../escalation/)
- [Servicenow — Health Checks](../../operations/health-checks/)
