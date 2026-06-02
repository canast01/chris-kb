# Azure Monitoring

<div class="kb-summary">
Azure Monitoring articles, operational checks, troubleshooting notes, and references.
</div>

```text
┌────────────────────────────────────── Azure Monitoring Overview ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                    Azure Monitor — Metrics, Logs, Alerts, and Observability                   │   │
│   │  Azure Monitor: platform for all metrics, logs, alerts, and dashboards across Azure services  │   │
│   │ Log Analytics: workspace stores logs; KQL query language; used for dashboards and alert rules │   │
│   │     Alerts: metric, log, and activity log alert rules; action groups for notification and     │   │
│   │  Diagnostic settings: route resource logs and metrics to Log Analytics, Storage, or Event Hub │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Metrics and logs feed alert rules · Alerts trigger action groups · Dashboards provide visibility   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Azure Monitor        │  │        Log Analytics        │  │            Alerts           │   │
│   │   Metrics: platform native  │  │    Workspace: per region    │  │   Metric alert: threshold   │   │
│   │   Activity log: ctrl-plane  │  │    KQL: query + transform   │  │     Log alert: KQL query    │   │
│   │     Diagnostic settings     │  │      Retention: 30-730d     │  │     Activity alert: ops     │   │
│   │    Service Health: events   │  │    Workbooks: dashboards    │  │   Action group: email/web   │   │
│   │   Dashboards: pin metrics   │  │     Saved queries: reuse    │  │   Alert rule: severity 0-4  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Azure Monitor collects metrics/logs · Log Analytics stores and queries · Alerts notify and automate│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Azure Monitor   │  Log Analytics   │       Alerts      │   Activity Log   │  Service Health  │   │
│   │   Metrics: CPU   │    KQL: query    │   Metric: CPU>80  │   Who changed?   │  Planned maint   │   │
│   │  Diag settings   │  Workspace: RG   │   Log: KQL rule   │  Activity alert  │  Incidents: svc  │   │
│   │  Dashboard: pin  │  Retention: 90d  │   Action: email   │    Export: LA    │  Health alerts   │   │
│   │    Workbooks     │   Saved query    │    Severity 0-4   │    ARM events    │  Subscr events   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure Monitor backend · Log Analytics workspace storage · Action Group notification services         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Azure Monitor     = Platform service aggregating all metrics, logs, alerts, and traces from Azure    │
│  Log Analytics workspace= Storage and query engine for Azure Monitor logs; uses KQL; one or more per  │
│  KQL               = Kusto Query Language; used in Log Analytics, Application Insights, and Data      │
│  Diagnostic settings= Resource-level config routing logs/metrics to Log Analytics, Storage, or Event  │
│  Activity Log      = Subscription-level control-plane audit log; who did what, when; 90 days retention│
│  Metric alert      = Fires when a metric (CPU, memory, latency) crosses a threshold for N minutes     │
│  Log alert         = Fires when a KQL query returns rows; evaluated on a schedule (5 min – 1 day)     │
│  Activity alert    = Fires on specific control-plane events (e.g. VM deleted, RBAC assigned)          │
│  Action group      = Reusable set of notification actions (email, SMS, webhook, Logic App, ITSM)      │
│  Alert severity    = Sev 0 (Critical) to Sev 4 (Verbose); used to route and prioritise alerts         │
│  Service Health    = Azure-side health events and planned maintenance for your subscriptions/services │
│  Workbook          = Azure Monitor interactive report combining metrics, logs, and parameters in one  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="activity-log/">
  <strong>Activity Log</strong>
  <span>Subscription-level audit log of control-plane operations, who changed what and when.</span>
</a>

<a class="kb-card" href="alerts/">
  <strong>Alerts</strong>
  <span>Metric, log, and activity log alert rules with action groups for notification and automation.</span>
</a>

<a class="kb-card" href="azure-monitor/">
  <strong>Azure Monitor</strong>
  <span>Unified monitoring platform for metrics, logs, alerts, diagnostics, and dashboards.</span>
</a>

<a class="kb-card" href="dashboards/">
  <strong>Dashboards</strong>
  <span>Pinned metric charts, log query results, and resource tiles for operational visibility.</span>
</a>

<a class="kb-card" href="diagnostic-settings/">
  <strong>Diagnostic Settings</strong>
  <span>Route resource logs and metrics to Log Analytics, Storage, or Event Hub for retention and analysis.</span>
</a>

<a class="kb-card" href="log-analytics/">
  <strong>Log Analytics</strong>
  <span>KQL-based log query workspace for ingesting, querying, and alerting on log data.</span>
</a>

<a class="kb-card" href="metrics/">
  <strong>Metrics</strong>
  <span>Near-real-time numeric time-series data for Azure resources; used for alerting and auto-scale.</span>
</a>

<a class="kb-card" href="service-health/">
  <strong>Service Health</strong>
  <span>Azure platform health events, planned maintenance, and service advisories affecting your resources.</span>
</a>

<a class="kb-card" href="workbooks/">
  <strong>Workbooks</strong>
  <span>Interactive report templates combining metrics, logs, and parameters for operational reporting.</span>
</a>
</div>
