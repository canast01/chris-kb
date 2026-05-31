# Aria Operations for Logs

<div class="kb-summary">
Technical and operational reference for VMware Aria Operations for Logs. Covers log ingestion, querying, alerting, dashboards, and integration for VMware infrastructure log management and analysis.
</div>

```text
┌─────────────────────────────────── Aria Operations for Logs Stack ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           VMware Aria Operations for Logs — Centralised Log Management and Analysis           │   │
│   │          Log ingestion: syslog (UDP/TCP 514), CFAPI agents on VMs, Fluentd forwarding         │   │
│   │     Content packs: pre-built dashboards and queries for vSphere, NSX, ESXi, Linux, Windows    │   │
│   │     Interactive analytics: live-tail, field extraction, regex filters, time-window search     │   │
│   │        Alerts: query-based triggers; webhooks to PagerDuty, Slack, ServiceNow, or email       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Ingestion receives logs · analytics queries them · alerts and dashboards surface insights          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │     Master+worker nodes     │  │   Log search: query+filter  │  │    RBAC: AD + local users   │   │
│   │     syslog: UDP/TCP 514     │  │    Content pack: install    │  │    TLS: syslog encrypted    │   │
│   │     CFAPI agent: per-VM     │  │    Alert: query + webhook   │  │      SSO: vCenter login     │   │
│   │      Forwarder: to SIEM     │  │    Dashboard: build+share   │  │    Retention: policy set    │   │
│   │    Disk: retention sizing   │  │    Agent group: bulk mgmt   │  │     Audit: admin actions    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture ingests logs · Operations search and alert · Security controls access and retention   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │Logs not arriving │System diagnostics│  Ingest rate: OK? │   GSS + bundle   │ li-admin status  │   │
│   │Disk full: purging│ Disk usage check │  Disk: >70% used? │  TAM escalation  │ li-admin cluster │   │
│   │ Alert not firing │Alert query debug │  Alert: enabled?  │ Collect app logs │ li-admin alerts  │   │
│   │Content pack error│ content-pack.log │ Packs: installed? │P1: log loss event│  li-admin packs  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Aria Logs VMs (master+worker) · large /storage/core disk · syslog network paths · Aria Suite LCM     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CFAPI agent   = Log agent installed on VMs; forwards structured logs via CFAPI protocol on port 9543 │
│  Content pack  = Pre-built bundle of log queries, dashboards, and alerts for a specific product       │
│  Field extract = Named regex capture group applied to log messages to create queryable fields         │
│  Agent group   = Logical grouping of CFAPI agents sharing the same configuration and filters          │
│  Webhook       = HTTP callback for alerts; sends payload to Slack, PagerDuty, or custom URL           │
│  Forwarder     = Sends matching log events to a remote syslog target or SIEM for correlation          │
│  Interactive analytics= Live log search with regex, field filters, and time window; no pre-indexing   │
│  Retention     = Policy setting number of days logs are kept before purging; constrained by disk      │
│  Master node   = Primary Aria Logs node; holds index and coordinates worker nodes in cluster          │
│  Worker node   = Additional Aria Logs node adding ingestion capacity and search throughput            │
│  syslog        = UDP/TCP port 514 protocol; most infrastructure devices send logs via syslog          │
│  li-admin      = Aria Logs admin CLI; cluster status, disk usage, configuration management            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
