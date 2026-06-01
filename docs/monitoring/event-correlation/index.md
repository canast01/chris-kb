# Event Correlation


<div class="kb-summary">
Event Correlation reference covering Correlation Workflow, Building a Correlation Timeline, Common Correlation Patterns, SIEM Correlation Rules (Examples), Dependency Map (template) and 1 more sections.
</div>

```powershell
┌─────────────────────────────────── Monitoring — Event Correlation ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Event Correlation — Linking Multi-Domain Alerts to a Single Root Cause            │   │
│   │        Sources: Aria Ops · CloudIQ · NDI · Pure1 · syslog · SNMP traps · vCenter events       │   │
│   │            Correlation engine: time-window grouping · object-relationship traversal           │   │
│   │           Output: single correlated incident in ServiceNow · suppressed child alerts          │   │
│   │     Tools: Aria Ops correlation rules · AIOps root-cause suggestions · NDI change analysis    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Correlation reduces noise by grouping 10–100 alerts into a single actionable incident              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Alert Ingestion       │  │      Correlation Logic      │  │       Incident Output       │   │
│   │     Aria Ops OOTB rules     │  │      Time-window: 5 min     │  │     ServiceNow P2 ticket    │   │
│   │       CloudIQ SNMP/API      │  │     Object relationship     │  │     Parent alert visible    │   │
│   │      NDI anomaly events     │  │      Topology traversal     │  │     Children suppressed     │   │
│   │       Syslog messages       │  │      AIOps ML grouping      │  │      RCA note attached      │   │
│   │     vCenter tasks/events    │  │      Change-correlation     │  │      Operator notified      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Correlation runs in Aria Ops analytics node · AIOps SaaS ML pipeline · NDI Insights app              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Root cause        = Underlying fault that triggered one or more downstream alert conditions          │
│  Time-window       = Period during which alerts are grouped for correlation (default 5 min)           │
│  Object relationship= Topology link (e.g. VM→host→cluster) used to trace cause to effect              │
│  Topology traversal= Walking the inventory graph from child to ancestor to find root object           │
│  Correlated incident= Single ITSM ticket representing a group of related alerts                       │
│  Child alert        = Alert subordinate to a parent; suppressed when parent is active                 │
│  Change-correlation = Linking an alert to a recent change record as probable cause                    │
│  OOTB rules         = Out-of-the-box correlation rules shipped with Aria Operations                   │
│  ML grouping        = AIOps machine-learning model clustering alerts by causal similarity             │
│  RCA note           = Root Cause Analysis note attached to the incident by the platform               │
│  SNMP trap          = UDP event message sent by infrastructure to a monitoring collector              │
│  Suppression        = Silencing child alerts once a parent incident is open                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Common Correlation Patterns

| Symptom Cluster | Probable Root Cause |
|---|---|
| Multiple hosts: I/O errors + application timeouts | Storage array or fabric fault |
| Multiple hosts: network unreachable at same time | Upstream switch / router failure |
| VM slowness + storage latency on one array | Array controller issue or disk rebuild |
| Authentication failures across multiple services | AD / LDAP / DNS failure |
| Backup failures + high host CPU | Resource contention during backup window |
| One host: multiple service alerts simultaneously | Host hardware (memory/disk) or kernel panic |

## SIEM Correlation Rules (Examples)

**Graylog / Splunk — correlated alert logic:**
```bash
# Multiple auth failures from same source within 5 minutes
index=security sourcetype=auth action=failure
| stats count by src_ip, user
| where count > 10
| eval alert="Possible brute force"

# Storage latency spike + host I/O error within 2-minute window
index=infra (sourcetype=ontap OR sourcetype=os_ioerr)
| transaction maxspan=2m host
| where eventcount > 1
```

## Dependency Map (template)

Document for each critical service:

```text
Service: ERP Application
  → App server: app01, app02
      → Database: db01 (Oracle)
          → Storage: ONTAP SVM prod-svm, volume erp-data
              → SAN fabric: MDS-A, MDS-B, Zone: erp_zone
      → Load balancer: F5-prod VIP 10.10.10.100
  → Auth: AD domain controllers dc01, dc02
  → DNS: 10.10.10.53
```

## Cross-Platform Log Locations

| System | Log location |
|---|---|
| Linux OS | `/var/log/messages`, `/var/log/syslog`, `journalctl` |
| Windows | Event Viewer: System, Application, Security |
| ONTAP | EMS: `event log show -severity error` |
| VMware | `/var/log/vmkernel.log`, vCenter Events |
| Cisco NX-OS | `show logging last 100` |
| Brocade FOS | `errShow` |
