---
tags:
  - servicenow
  - troubleshooting
search:
  boost: 1.5
---
# ServiceNow Common Issues
![ServiceNow Common Issues](../../../../assets/itsm-servicenow-troubleshooting-common-issues-index.svg)


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

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> B1{Record not\nvisible?}
    S --> B2{Workflow activity\nstuck?}
    S --> B3{REST API\nreturning 403?}
    S --> B4{Scheduled job\nnot running?}
    S --> B5{Import set\ntransform error?}
    B1 -->|Yes| D1{ACL or role\nissue?}
    D1 -->|ACL| R1[Login and Access\n— review ACL conditions in sys_security_acl]
    D1 -->|Role| R2[Login and Access\n— add required role to user or group]
    B2 -->|Yes| D2{Approval stuck\nor activity timed out?}
    D2 -->|Approval| R3[Workflow and ITSM\n— manually reassign stuck approval]
    D2 -->|Timeout| R4[Workflow and ITSM\n— check SLA timezone and schedule config]
    B3 -->|Yes| D3{Correct role\nassigned to API user?}
    D3 -->|No| R5[Integration\n— assign rest_api_explorer or specific role]
    D3 -->|Yes| R6[Integration\n— check ECC queue for error state messages]
    B4 -->|Yes| D4{MID server\nonline?}
    D4 -->|No| R7[Integration\n— restart MID server service]
    D4 -->|Yes| R8[Workflow and ITSM\n— check scheduled job log in sys_job]
    B5 -->|Yes| R9[Integration\n— check transform map field mappings]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8,R9 section
    class B1,B2,B3,B4,B5,D1,D2,D3,D4 decision
    class S start
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
