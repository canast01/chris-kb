```javascript
// To find long-running transactions, run in Background Scripts:
var gr = new GlideRecord('sys_running_transaction');
gr.query();
while (gr.next()) {
    gs.print(gr.getValue('name') + ' | ' + gr.getValue('duration') + ' | ' + gr.getValue('thread'));
}
```

```text
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
