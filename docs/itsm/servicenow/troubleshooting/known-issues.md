---
tags:
  - troubleshooting
  - servicenow
  - itsm
  - known-issues
---
# ServiceNow — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known ServiceNow bugs, error codes, and workarounds covering MID Server, integrations, and instance performance.

*Applies to: ServiceNow Washington DC / Xanadu releases*
</div>

```text
┌───────────────────────────────────────────── ServiceNow ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               ITSM/ITOM platform — MID Server, instance, REST/SOAP integrations               │   │
│   │                    Protocols: HTTPS · MID Server outbound to instance (443)                   │   │
│   │                   Management: instance UI (System Diagnostics, System Logs)                   │   │
│   │               MID Server discovery -> Instance DB -> Business rules -> Workflow               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Instance          │  │       ServiceNow cloud      │  │      Multi-tenant SaaS      │   │
│   │         Integration         │  │          MID Server         │  │    On-prem, outbound only   │   │
│   │             Data            │  │             CMDB            │  │     Config item database    │   │
│   │           Workflow          │  │        Flow Designer        │  │    Business logic engine    │   │
│   │             Auth            │  │      SSO/LDAP/MID creds     │  │    Per-integration scope    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │     Instance     │ SaaS application │       HTTPS       │    SSO/local     │   Multi-tenant   │   │
│   │    MID Server    │  On-prem agent   │     HTTPS out     │   Service acct   │No inbound needed │   │
│   │       CMDB       │   Config data    │      Internal     │    ACL-scoped    │Discovery fills it│   │
│   │     REST API     │Integration endpt │       HTTPS       │   OAuth/Basic    │web_service_admin │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: ServiceNow SaaS instance (cloud) - on-prem MID Server host(s)                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  MID Server     = on-prem agent for outbound-only ServiceNow integration                              │
│  CMDB           = Configuration Mgmt Database; tracks config items                                    │
│  Discovery      = MID Server feature scanning networks for the CMDB                                   │
│  sys_log        = ServiceNow internal application log table                                           │
│  Business rule  = server-side script on insert/update/delete                                          │
│  ACL            = Access Control List; row/field-level security rule                                  │
│  Update Set     = packaged customization moved between instances                                      │
│  Flow Designer  = no-code workflow automation tool                                                    │
│  Inbound Action = email-triggered automation rule                                                     │
│  Scoped app     = isolated namespace for custom development                                           │
│  web_service_admin = role required for most REST integrations                                         │
│  Clone          = full copy of one instance to another                                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- ServiceNow errors appear in `System Log → All` in the instance UI.
- MID Server logs: `<mid-server-install>\logs\agent0.log.0`.
- Most MID Server issues are outbound connectivity (TCP 443 to instance URL).

## MID Server

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| MID Server `Down` in ServiceNow | Any | MID Server service stopped or TCP 443 blocked | Restart MID Server: `service mid-server restart`; verify TCP 443 to `<instance>.service-now.com` | N/A |
| `MID Server validation failed` | Any | MID Server version incompatible with instance version | Upgrade MID Server to version matching instance release | N/A |
| Discovery not finding targets | Any | MID Server cannot reach targets on required ports (22/5985/161) | Verify MID Server network access to target IPs on required ports | N/A |

## Integrations

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `REST API integration returning 403` | Any | Integration service account lacks API access role | Assign `web_service_admin` or specific API role to integration user | N/A |
| Inbound email action not triggering | Any | Email inbound action rule condition not matching | Check inbound action rule condition in `System Policy → Inbound Actions` | N/A |

## Performance

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Slow list views with many records | Any | Missing index on filtered column | Add ServiceNow index via `sys_db_object`; contact ServiceNow support for large deployments | N/A |
| Background jobs backlogged | Any | Too many concurrent scheduled jobs | Stagger job schedules; increase worker thread pool in instance settings | N/A |

## See also

- [ServiceNow — Common Issues](common-issues/)
- [Ansible — Known Issues](../../../automation/ansible/troubleshooting/known-issues.md)
