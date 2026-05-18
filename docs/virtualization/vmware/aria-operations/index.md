# Aria Operations

<div class="kb-summary">
Technical and operational reference for VMware Aria Operations. Covers performance monitoring, capacity management, compliance, alerting, dashboards, and troubleshooting across vSphere, vSAN, NSX, and Aria-managed infrastructure.
</div>

```
Aria Operations — Data Collection and Analytics Flow
┌──────────────────────────────────────────────────┐
│  Monitored Sources                               │
│  ESXi hosts · vCenter · NSX-T · vSAN             │
│  storage arrays · cloud accounts                 │
└──────────┬───────────────────────────────────────┘
           │ adapters pull metrics, events, props
           ▼
┌──────────────────────────────────────────────────┐
│  Remote Collectors / Cloud Proxies               │
│  (optional — extend reach to remote sites/DMZs)  │
└──────────┬───────────────────────────────────────┘
           │ forward to analytics cluster
           ▼
┌──────────────────────────────────────────────────┐
│  Aria Operations Analytics Cluster               │
│  ┌────────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  Primary   │  │ Replica  │  │  Data nodes  │  │
│  │  (UI/API)  │  │ (standby)│  │  (scale-out) │  │
│  └────────────┘  └──────────┘  └──────────────┘  │
│       │                                          │
│  Cassandra (time-series) · GemFire (cache)       │
└──────────┬───────────────────────────────────────┘
           │ analytics, alerts, capacity
           ▼
┌──────────────────────────────────────────────────┐
│  Consumers                                       │
│  ┌──────────────┐  ┌────────────┐  ┌──────────┐  │
│  │  Dashboards  │  │  Email /   │  │  ITSM /  │  │
│  │  (browser)   │  │  Webhook   │  │  SN tick │  │
│  └──────────────┘  └────────────┘  └──────────┘  │
└──────────────────────────────────────────────────┘
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
