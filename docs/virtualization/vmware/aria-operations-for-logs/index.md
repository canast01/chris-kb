# Aria Operations for Logs

<div class="kb-summary">
Technical and operational reference for VMware Aria Operations for Logs. Covers log ingestion, querying, alerting, dashboards, and integration for VMware infrastructure log management and analysis.
</div>

```
┌─────────────────────────────────────────────────────────────┐
│         Aria Operations for Logs — Data Flow                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Log Sources                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ ESXi     │  │ vCenter  │  │ NSX-T    │  │ Linux/   │     │
│  │ syslog   │  │ syslog   │  │ syslog   │  │ Win VMs  │     │
│  │ UDP 514  │  │ UDP 514  │  │ UDP 514  │  │ LI Agent │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       └─────────────┴─────────────┴──────────────┘          │
│                           │ cfapi TLS :9543 / UDP :514      │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Aria Ops for Logs Cluster (1 Master + 2 Workers)    │   │
│  │  Cassandra index  ·  Content Packs  ·  Alert Engine  │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           │                                 │
│              ┌────────────┼────────────┐                    │
│              ▼            ▼            ▼                    │
│           Query UI      Alerts      vROps (bi-dir)          │
└─────────────────────────────────────────────────────────────┘
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
