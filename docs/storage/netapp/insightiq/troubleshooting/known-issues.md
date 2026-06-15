---
tags:
  - troubleshooting
  - insightiq
  - netapp
  - known-issues
---
# NetApp InsightIQ — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known InsightIQ bugs, error codes, and workarounds covering data collection, API connectivity, and reporting.

*Applies to: NetApp InsightIQ 4.x (formerly Isilon InsightIQ)*
</div>

```text
┌────────────────────────────────────── Storage Netapp Insightiq ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                           Netapp: Storage Netapp Insightiq platform                           │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Storage Netapp Insightiq management console                    │   │
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
│    Physical: Storage Netapp Insightiq infrastructure · management network · monitoring                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Netapp             = Storage Netapp Insightiq platform overview and core concepts                  │
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

- InsightIQ errors appear in the web UI under `Administration → Data Collections`.
- Check the InsightIQ appliance system log: `tail -f /var/log/insightiq/insightiq.log`.

## Data Collection

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Cluster data collection showing `No data` | InsightIQ 4.x | InsightIQ cannot reach PowerScale platform API on 8080 | Verify TCP 8080 from InsightIQ to PowerScale SmartConnect IP | N/A |
| `Authentication failed` for managed cluster | InsightIQ 4.x | PowerScale API credentials changed or user locked out | Update cluster credentials in InsightIQ → Clusters → Edit | N/A |
| Performance graphs empty after OneFS upgrade | InsightIQ 4.x | OneFS upgrade changed platform API version; InsightIQ not updated | Upgrade InsightIQ to version compatible with new OneFS release | N/A |

## Reporting

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Report generation times out for long date ranges | InsightIQ 4.x | Database query timeout for large time ranges | Reduce report window to ≤30 days; archive older data to free DB space | N/A |
| Scheduled email report not delivered | InsightIQ 4.x | SMTP relay not configured or port 25 blocked from InsightIQ | Configure SMTP relay in InsightIQ → Administration → Email Settings | N/A |

## See also

- [NetApp InsightIQ — Common Issues](common-issues.md)
- [Dell PowerScale — Known Issues](../../../dell/powerscale/troubleshooting/known-issues/)
- [NetApp ONTAP — Known Issues](../../ontap/troubleshooting/known-issues/)
