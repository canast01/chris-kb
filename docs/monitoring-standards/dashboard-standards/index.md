# Monitoring Dashboard Standards


<div class="kb-summary">
Monitoring Dashboard Standards reference covering Grafana — Dashboard as Code, Validation Checklist, Dashboard Review Cadence.
</div>

```text
┌────────────────────────────────── Monitoring — Dashboard Standards ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Dashboard Standards — Naming, Layout, Widget, and Data Source Conventions           │   │
│   │               Naming: <PRODUCT>-<DOMAIN>-<SCOPE> e.g. ARIA-VSPHERE-CLUSTER-PERF               │   │
│   │            Layout: header summary row · detail grid · trend charts · capacity strip           │   │
│   │       Widgets: scoreboard (current state) · time-series (trend) · heatmap (distribution)      │   │
│   │       Colour: green <70% · amber 70-85% · red >85% for capacity and CPU/mem utilisation       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Consistent dashboards reduce MTTR by ensuring operators know exactly where to look                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Naming Standard       │  │         Widget Types        │  │          Governance         │   │
│   │        Product prefix       │  │       Scoreboard: KPIs      │  │     Owner per dashboard     │   │
│   │        Domain segment       │  │      Time-series: trend     │  │       Review cycle: Q1      │   │
│   │        Scope segment        │  │       Heatmap: distrib      │  │       Version in title      │   │
│   │      No spaces/special      │  │      List: top-N items      │  │     Archived not deleted    │   │
│   │        Version suffix       │  │     Alert widget: count     │  │     RBAC: read-only pub     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Dashboards reside in Aria Operations UI · Nexus Dashboard NDI · Pure1 portal · CloudIQ SaaS          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Scoreboard widget = Single-value tile showing current state with colour threshold band               │
│  Time-series widget= Line/area chart plotting metric values over a configurable time window           │
│  Heatmap widget    = Grid colouring cells by metric value; useful for per-VM or per-host views        │
│  KPI               = Key Performance Indicator; top-level metric surfaced in the header row           │
│  Capacity strip    = Bottom row of a dashboard showing remaining headroom per resource type           │
│  RBAC              = Role-Based Access Control; governs who can edit vs. view a dashboard             │
│  Threshold band    = Numeric ranges mapped to green/amber/red colour codings                          │
│  Dashboard owner   = Team member accountable for accuracy and maintenance of the dashboard            │
│  Archived          = Dashboard removed from active view but retained for audit/history                │
│  MTTR              = Mean Time To Resolve; reduced when dashboards are consistent and clear           │
│  Top-N list        = Widget ranking objects by metric value; identifies worst offenders quickly       │
│  Version suffix    = e.g. v2; indicates updated dashboard replacing a prior published version         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Validation Checklist

- [ ] All required dashboards loading in monitoring tool
- [ ] Metrics updating at configured refresh interval
- [ ] Alert panel reflects current open alerts (not stale)
- [ ] Time-zone consistent across all panels (UTC preferred for ops dashboards)
- [ ] No broken panel queries (missing datasource or deleted metric)
- [ ] Access permissions: read for all ops, edit only for monitoring team
- [ ] Dashboard JSON committed to Git / versioned

## Dashboard Review Cadence

| Trigger | Action |
|---|---|
| Quarterly | Audit for stale panels and unused dashboards |
| After major infra change | Update panels affected by the change |
| New service onboarded | Add service to infrastructure overview within 5 days |
| Alert threshold change | Update the corresponding dashboard annotation |
