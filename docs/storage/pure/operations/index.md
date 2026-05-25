# Pure Operations

```text
┌───────────────────────────────────── Pure Storage Operations Hub ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Pure Storage Operations — Pure1, Alerts, and Support Case Management             │   │
│   │    Pure1 cloud portal: central management for all FlashArray and FlashBlade arrays globally   │   │
│   │Alerts: hardware, software, and capacity events; severity levels Info, Warning, Error, Critical│   │
│   │    Support cases: opened via Pure1 or phone; include log bundle, serial number, and impact    │   │
│   │   Proactive support: Pure1 AI detects anomalies and opens cases automatically before failure  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Pure1 feeds alerts and support workflows — day-to-day ops span portal, CLI, and case management    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Pure1 Portal        │  │            Alerts           │  │        Support Cases        │   │
│   │    Array fleet dashboard    │  │  Severity: Info → Critical  │  │   Open via Pure1 or phone   │   │
│   │  Capacity + perf analytics  │  │  Hardware alerts: drive, CT │  │   Collect: log bundle + SN  │   │
│   │  AI-driven health insights  │  │  SW alerts: Purity version  │  │    Severity: P1-P4 tiers    │   │
│   │    Upgrade scheduler: NDU   │  │    Capacity alerts: >80%    │  │    Remote assist session    │   │
│   │   Proactive case auto-open  │  │   Repl alerts: lag + state  │  │   TAM for strategic issues  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Pure1 provides fleet visibility · Alerts drive action                                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Pure1 Features  │   Alert Types    │   Case Workflow   │    Escalation    │   CLI Commands   │   │
│   │ Fleet dashboard  │  Drive failure   │ Collect log bundle│  TAM engagement  │  purearray list  │   │
│   │Capacity forecast │    CT warning    │  Describe impact  │  Remote assist   │  purealert list  │   │
│   │  Perf analytics  │  Purity upgrade  │ Submit via portal │ Exec escalation  │  purearray get   │   │
│   │ Upgrade schedule │  Capacity >80%   │ P1: 24/7 response │  VP escalation   │ purelog download │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FlashArray / FlashBlade arrays · customer data centre · Pure1 cloud (SaaS portal) · Internet uplink  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Pure1         = Cloud management portal for all Pure arrays; telemetry, AI health, and upgrade       │
│  Alert severity= Info (FYI) · Warning (monitor) · Error (investigate) · Critical (act immediately)    │
│  Log bundle    = puresupport bundle command output; full diagnostic archive for support case          │
│  Proactive case= Pure1 AI opens a support case automatically when anomaly detected before failure     │
│  P1 case       = Severity 1; production down or data loss; 24/7 response SLA, engineer on phone       │
│  P2 case       = Severity 2; degraded performance or risk; business-hours response with engineer      │
│  Remote assist = Pure engineer connects via secure tunnel to live array for real-time troubleshooting │
│  TAM           = Technical Account Manager; Pure named escalation contact for strategic accounts      │
│  NDU scheduler = Non-Disruptive Upgrade scheduler in Pure1; picks maintenance window for Purity update│
│  purealert     = CLI command to list, acknowledge, and filter alerts on FlashArray or FlashBlade      │
│  Capacity alert= Fires when array used capacity exceeds configured threshold (default 80%)            │
│  SN            = Serial number; required in every Pure support case for array identification          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Use this section for practical notes, checks, commands, troubleshooting, design references, and change validation.

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="alerts/">
  <strong>Alerts</strong>
  <span>Notes, checks, runbooks, commands, troubleshooting, and operational references for Alerts.</span>
</a>

<a class="kb-card" href="pure1/">
  <strong>Pure1</strong>
  <span>Notes, checks, runbooks, commands, troubleshooting, and operational references for Pure1.</span>
</a>

<a class="kb-card" href="support-cases/">
  <strong>Support Cases</strong>
  <span>Notes, checks, runbooks, commands, troubleshooting, and operational references for Support Cases.</span>
</a>

</div>
