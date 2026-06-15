---
tags:
  - troubleshooting
  - pure1
  - pure-storage
  - known-issues
---
# Pure1 — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Pure1 issues covering array connectivity, portal access, and data display problems. Pure1 is a SaaS platform — most issues are phone-home connectivity from arrays.

*Applies to: Pure1 cloud portal*
</div>

```text
┌───────────────────────────────────────── Storage Pure Pure1 ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               Pure: Storage Pure Pure1 platform                               │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                       Management: Storage Pure Pure1 management console                       │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Storage Pure Pure1 infrastructure · management network · monitoring                      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Pure               = Storage Pure Pure1 platform overview and core concepts                        │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Pure1 issues are either phone-home connectivity (array side) or portal access (browser side).
- Array connectivity: verify outbound TCP 443 from array management IP to `pure1.purestorage.com`.
- Portal issues: log in at `pure1.purestorage.com`; contact Pure Storage support if portal is unavailable.

## Array Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Array shows `Offline` in Pure1 | All | TCP 443 blocked from array management IP to pure1.purestorage.com | Open firewall; test: `curl -sk https://pure1.purestorage.com` from array management network | N/A |
| Array connected but data stale >24 hours | All | Intermittent network drops interrupting telemetry upload | Check network stability from array management IP; review firewall session table for timeouts | N/A |
| `puremessage test` returns `Connection failed` | Purity 6.x | Proxy required but not configured | Configure HTTP proxy on array: `purearray setattr --proxy http://<proxy>:<port>` | N/A |

## Portal Access

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Cannot log in to Pure1 portal | N/A | SSO federation issue or Pure1 outage | Try direct login at `pure1.purestorage.com`; check `status.purestorage.com` for outage | N/A |
| Array visible in Pure1 but showing no performance data | All | Array model not yet configured for full telemetry | Contact Pure support — some older models have limited telemetry | N/A |

## See also

- [Pure1 — Common Issues](common-issues.md)
- [Pure Storage FlashArray — Known Issues](../../flasharray/troubleshooting/known-issues/)
- [Pure Storage FlashBlade — Known Issues](../../flashblade/troubleshooting/known-issues/)
