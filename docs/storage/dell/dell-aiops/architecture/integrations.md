---
tags:
  - architecture
  - dell
---
# Dell AIOps — Integrations

<div class="kb-summary">
Dell AIOps is embedded in CloudIQ — integrations are shared. Supported Dell array types, notification channels, and the APEX Console API are the key integration surfaces.

*Applies to: Dell AIOps*
</div>

```text
┌─────────────────────────────── Dell AIOps — Architecture Integrations ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Infrastructure Inputs             │              Notification Outputs              │   │
│   │             PowerStore REST API              │               ServiceNow webhook               │   │
│   │               PowerScale PAPI                │                 PagerDuty REST                 │   │
│   │              PowerFlex REST API              │              Slack/Teams webhook               │   │
│   │             CloudIQ bridge feed              │                   Email SMTP                   │   │
│   │            VxRail REST / VCF API             │              Grafana data source               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  AIOps polls infrastructure APIs · outbound notifications over TCP 443/25 to targets                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PAPI = PowerScale Platform API; REST interface for isilon/PowerScale management                      │
│  REST API = PowerStore/PowerFlex management API; AIOps polls every 5 minutes                          │
│  CloudIQ bridge = Component ingesting CloudIQ health data into AIOps for correlation                  │
│  VCF API = VMware Cloud Foundation API for vSphere and SDDC component metrics                         │
│  Webhook = HTTP POST from AIOps when alert fires; payload in JSON                                     │
│  Grafana data source = AIOps REST API proxied as Grafana data source for custom panels                │
│  SMTP = Email notification from AIOps SMTP client on alert                                            │
│  PagerDuty = On-call routing platform receiving AIOps alerts via Events API v2                        │
│  Slack webhook = Incoming webhook URL for posting alert summaries to a Slack channel                  │
│  Poll interval = Frequency AIOps adapter queries infrastructure API; default 5 minutes                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Integration with ServiceNow CMDB

- AIOps anomaly alerts can auto-create ServiceNow incidents linked to the affected CI
- Requires SCG → CloudIQ → ServiceNow connector configured with the correct CMDB table mapping (`cmdb_ci_storage_server`)
- Map CloudIQ array names to ServiceNow CI names to ensure correct CI assignment on incident creation

---

## See also

- [Dell Aiops — How It Works](how-it-works/)
- [Dell Aiops — Design Standards](design-standards/)
