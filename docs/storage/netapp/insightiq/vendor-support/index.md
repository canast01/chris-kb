---
tags:
  - netapp
---
# InsightIQ Vendor Support


<div class="kb-summary">
InsightIQ vendor support: opening NetApp support cases, collecting `isi_gather_info` and InsightIQ diagnostic bundles, and escalation contact procedure.

*Applies to: InsightIQ*
</div>

```text
┌───────────────────────────────────── InsightIQ — Vendor Support ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Support Model — Dell Technologies GSS                             │   │
│   │           InsightIQ covered by PowerScale ProSupport or ProSupport Plus entitlement           │   │
│   │           Open case at support.dell.com — provide InsightIQ version + collection log          │   │
│   │                 Sev-1: collection fully stopped on all clusters; 24x7 response                │   │
│   │             Sev-2: collection degraded or UI inaccessible; business-hours response            │   │
│   │             Interop matrix: confirm InsightIQ version vs PowerScale OneFS version             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  InsightIQ VM on-prem · support bundle collected locally · uploaded to Dell case portal               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ProSupport = Dell hardware support tier; required for InsightIQ support eligibility                  │
│  GSS = Global Support Services; Dell tier-1 technical support                                         │
│  Collection log = /var/log/isilon/insightiq/collection.log; attach to support case                    │
│  InsightIQ version = Check in UI > Help > About; needed for case opening                              │
│  OneFS version = PowerScale OS version; must be in InsightIQ interop matrix                           │
│  Interop matrix = Dell compatibility table confirming supported OneFS/InsightIQ combos                │
│  Severity 1 = All collection stopped; 24x7 phone; include iiq_status output                           │
│  Severity 2 = Degraded collection; business-hours response                                            │
│  Support bundle = Log archive from InsightIQ; iiq_backup output + collection log                      │
│  KB = Dell Knowledge Base at kb.dell.com; search for InsightIQ symptoms                               │
│  EOL = InsightIQ End of Life; check Dell lifecycle page; plan migration to CloudIQ                    │
│  TAM = Technical Account Manager; proactive guidance for large PowerScale deployments                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
InsightIQ support is provided by NetApp via the NetApp Support Portal (mysupport.netapp.com). When raising an SR, collect logs from the InsightIQ appliance at `/var/log/insightiq/` and the PostgreSQL connection status. Include details of the OneFS clusters being monitored and any recent changes (upgrades, network changes, credential rotations).

**Information to collect before opening an SR**

- InsightIQ version
- OneFS version(s) for all monitored clusters
- Number of clusters monitored
- Error messages from `/var/log/insightiq/` logs
- Screenshot or description of the issue (connection failure, missing data, UI error)
- Appliance disk usage and resource utilisation

| Resource | Details |
|---|---|
| NetApp Support Portal | mysupport.netapp.com |
| Log location | `/var/log/insightiq/` |
| NetApp IMT | mysupport.netapp.com/matrix |
| InsightIQ Documentation | docs.netapp.com |
