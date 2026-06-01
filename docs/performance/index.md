# Performance


<div class="kb-summary">
References for capacity planning, performance management, and reliability engineering.
</div>

```text
┌─────────────────────── Performance — Capacity, Baselining, Reliability & SLOs ────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Performance management: baseline current state → monitor trends → plan capacity →       │   │
│   │        optimise resource usage → test failure modes → measure availability against SLOs       │   │
│   │     SLOs translate business expectations into measurable infra targets with error budgets     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Capacity & Baseline     │  │         Optimisation        │  │      SLO & Reliability      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │     Performance baseline    │  │        Right-size VMs       │  │        SLO definition       │   │
│   │     Capacity forecasting    │  │     Reclaim idle storage    │  │         Error budget        │   │
│   │        Trend analysis       │  │         Network QoS         │  │         MTTR / MTBF         │   │
│   │      Alerting on growth     │  │       Storage tiering       │  │      Availability calc      │   │
│   │      Resource headroom      │  │       Failure testing       │  │        SLA reporting        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SLO          = Service Level Objective; target for availability/latency/error rate                 │
│    SLA          = Service Level Agreement; contractual commitment, usually above SLOs                 │
│    SLI          = Service Level Indicator; the metric measured (e.g. request success rate)            │
│    Error budget  = Allowable downtime before SLO is breached; consumed by incidents                   │
│    MTTR         = Mean Time To Recover; average incident duration; lower is better                    │
│    MTBF         = Mean Time Between Failures; average uptime between incidents                        │
│    Baseline     = Normal performance values for a system; deviations trigger investigation            │
│    Right-sizing = Match VM/instance resources to actual usage; remove over-provisioning               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="capacity-forecasting/"><strong>Capacity Forecasting</strong><span>Projecting compute, storage, and network capacity requirements from trend data.</span></a>
<a class="kb-card" href="failure-testing/"><strong>Failure Testing</strong><span>Chaos engineering and fault injection procedures for validating HA and DR configurations.</span></a>
<a class="kb-card" href="performance-baselining/"><strong>Performance Baselining</strong><span>Establishing performance baselines for compute, storage, and network before changes.</span></a>
<a class="kb-card" href="reliability-engineering/"><strong>Reliability Engineering</strong><span>MTTR/MTBF tracking, failure mode analysis, and reliability improvement planning.</span></a>
<a class="kb-card" href="resource-optimization/"><strong>Resource Optimization</strong><span>Right-sizing VMs, reclaiming unused storage, and reducing idle resource consumption.</span></a>
<a class="kb-card" href="service-availability/"><strong>Service Availability</strong><span>Availability measurement, downtime tracking, and reporting against SLA targets.</span></a>
<a class="kb-card" href="service-level-objectives/"><strong>Service Level Objectives</strong><span>Defining, measuring, and reporting SLOs for infrastructure services.</span></a>
</div>
