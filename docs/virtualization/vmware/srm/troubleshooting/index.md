# Site Recovery Manager — Troubleshooting

```text
┌──────────────────────────────────────── SRM — Troubleshooting ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Site pair connectivity failures; replication lag and RPO breaches; PG config errors      │   │
│   │      Recovery plan execution failures; array API connectivity issues; HBCR agent failures     │   │
│   │       Diagnostics: SRM log files, VR appliance log, array API test, RPO dashboard review      │   │
│   │      Recovery plan test identifies misconfigurations before a real failover event occurs      │   │
│   │    Escalation: collect SRM bundles from both sites; engage array vendor; contact TAM for P1   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define triage path · diagnostics isolate replication or plan layer                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │        Site pair conn       │  │        SRM log files        │  │        SRM bndl both        │   │
│   │        Replic lag/RPO       │  │       VR appliance log      │  │         GSS P1 case         │   │
│   │        PG config err        │  │        Array API test       │  │        Both site logs       │   │
│   │      Recovery plan fail     │  │      Recovery plan test     │  │       Array vendor esc      │   │
│   │        Array API err        │  │        RPO dashboard        │  │         TAM contact         │   │
│   │       HBCR agent fail       │  │        Support bundle       │  │          P1 process         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics use logs and RPO dashboard                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │  Site pair fail  │  SRM log files   │/var/log/vmware/srm│    SRM bundle    │  Re-pair sites   │   │
│   │    Replic lag    │  RPO dashboard   │    VR app /logs   │   GSS P1 case    │   Resync data    │   │
│   │  PG config err   │  Recovery test   │    /var/log/hms   │   Array vendor   │  Fix PG config   │   │
│   │  Recovery fail   │  Array API test  │    /var/log/vr    │   TAM contact    │   Plan dry run   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers (both sites) · vSAN/SAN · WAN/DCI link · Array storage · AD domain                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Site pair          = Trusted link between SRM servers; failure blocks all SRM operations cross-site  │
│  RPO breach         = Replication lag exceeds configured RPO threshold; alerts in SRM dashboard       │
│  Protection group   = VM set in SRM; config error prevents inclusion in recovery plans                │
│  Recovery plan      = Ordered failover runbook; execution failures logged with step-level detail      │
│  HBCR agent         = Host-Based Changed Block Replication agent; failure stops vSphere Replication   │
│  Array-based replication = Array LUN replication via SRA; API errors block SRM inventory sync         │
│  SRM support bundle = Log package from SRM appliance; collected from both sites for GSS cases         │
│  VR appliance log   = vSphere Replication appliance logs; diagnose HBCR and replication failures      │
│  TAM escalation     = Technical Account Manager escalation for P1 DR incidents                        │
│  Test failover      = Non-disruptive test; use to validate plan config before real event              │
│  Reprotect          = Post-failover step; reverses replication; required before failback              │
│  Recovery time      = Actual elapsed time of recovery plan execution; compare against RTO target      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently seen problems and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to VMware support.</span>
</a>

</div>
