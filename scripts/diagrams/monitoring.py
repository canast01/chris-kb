"""
Monitoring (Aria Operations, CloudIQ, Dell AIOps, InsightIQ, Nexus Dashboard, Pure1) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

# ── Shared layout constants ───────────────────────────────────────────────────
W2 = 103
IV_L, IV_R = 3, 99
B1_L, B1_R = 3, 33
B2_L, B2_R = 36, 66
B3_L, B3_R = 69, 99
M1, M2, M3 = 18, 51, 84
PD1, PD2, PD3, PD4 = 22, 41, 61, 80

# ═══════════════════════════════════════════════════════════════════════════════
# MONITORING ROOT / SHARED PAGES
# ═══════════════════════════════════════════════════════════════════════════════

@kb_diagram(
    'monitoring-root',
    'docs/monitoring/index.md',
    'Monitoring overview — all products and shared services',
)
def monitoring_root():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Monitoring — Platform Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Monitoring Platform — Observability for Virtualisation, Storage, Network, and Compute')))
    lines.append(R(bMid(IV_L, IV_R, 'Products: Aria Operations · CloudIQ · Dell AIOps · InsightIQ · Nexus Dashboard · Pure1')))
    lines.append(R(bMid(IV_L, IV_R, 'Capabilities: metrics collection · alert routing · capacity forecasting · anomaly detection')))
    lines.append(R(bMid(IV_L, IV_R, 'Shared services: syslog · log retention · metrics baseline · event correlation · health')))
    lines.append(R(bMid(IV_L, IV_R, 'Targets: vSphere · NSX · PowerStore · PowerScale · ACI fabric · FlashArray · FlashBlade')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Each monitoring tool serves a distinct domain — together they form a unified observability layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VMware Domain'),
        bMid(B2_L, B2_R, 'Dell Domain'),
        bMid(B3_L, B3_R, 'Network/Storage'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Aria Operations'),
        bMid(B2_L, B2_R, 'CloudIQ (SaaS)'),
        bMid(B3_L, B3_R, 'Nexus Dashboard'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter/NSX targets'),
        bMid(B2_L, B2_R, 'Dell AIOps (SaaS)'),
        bMid(B3_L, B3_R, 'Pure1 (SaaS)'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity forecasting'),
        bMid(B2_L, B2_R, 'PowerStore/PowerMax'),
        bMid(B3_L, B3_R, 'FlashArray/Blade'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Anomaly detection'),
        bMid(B2_L, B2_R, 'InsightIQ (VM app)'),
        bMid(B3_L, B3_R, 'ACI fabric health'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Compliance packs'),
        bMid(B2_L, B2_R, 'PowerScale perf'),
        bMid(B3_L, B3_R, 'Flow analytics'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('On-prem: Aria Ops cluster on vSphere · InsightIQ VM on PowerScale · Nexus Dashboard cluster'))
    lines.append(txt_row('SaaS: CloudIQ · Dell AIOps · Pure1 — phone-home telemetry, no local server required'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Aria Operations  = On-prem analytics for vSphere, NSX, storage; collector + analytics nodes'))
    lines.append(txt_row('CloudIQ          = Dell SaaS platform; health scores and capacity forecasts for Dell arrays'))
    lines.append(txt_row('Dell AIOps       = AI-driven insight layer; anomaly correlation and root-cause suggestions'))
    lines.append(txt_row('InsightIQ        = VM appliance for PowerScale/Isilon performance analytics'))
    lines.append(txt_row('Nexus Dashboard  = Cisco fabric visibility; NDI app for ACI/NX-OS health and assurance'))
    lines.append(txt_row('Pure1            = Pure Storage SaaS; health, capacity, and performance for FlashArray/Blade'))
    lines.append(txt_row('Syslog           = RFC-5424 event stream; aggregated to a central syslog server (e.g. rsyslog)'))
    lines.append(txt_row('Metrics baseline = Documented normal operating ranges; used to tune alert thresholds'))
    lines.append(txt_row('Event correlation= Linking related alerts to a single root cause to reduce alert noise'))
    lines.append(txt_row('Alert management = Policy-driven routing of alerts to teams, tickets, and paging systems'))
    lines.append(txt_row('Log retention    = Policy governing how long logs are stored on-prem or in cloud storage'))
    lines.append(txt_row('Health score     = Composite 0-100 score aggregating component health indicators'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-alert-management',
    'docs/monitoring/alert-management/index.md',
    'Alert management — routing, suppression, escalation policies',
)
def monitoring_alert_management():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Monitoring — Alert Management'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Alert Management — Routing, Suppression, Escalation, and Notification Policies')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert sources: Aria Operations · CloudIQ · Dell AIOps · Nexus Dashboard NDI · Pure1')))
    lines.append(R(bMid(IV_L, IV_R, 'Routing targets: email · SMTP relay · PagerDuty · ServiceNow ITSM · Slack webhooks')))
    lines.append(R(bMid(IV_L, IV_R, 'Suppression rules: maintenance windows · severity thresholds · dedup intervals')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation tiers: L1 auto-ticket → L2 paging → L3 vendor engage → P1 bridge')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Alert policies govern who is notified, how quickly, and what actions auto-trigger'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert Sources'),
        bMid(B2_L, B2_R, 'Routing Rules'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Aria Ops alerts'),
        bMid(B2_L, B2_R, 'Severity filter'),
        bMid(B3_L, B3_R, 'L1: auto-ticket'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CloudIQ health alerts'),
        bMid(B2_L, B2_R, 'Object-type filter'),
        bMid(B3_L, B3_R, 'L2: on-call page'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NDI anomaly alerts'),
        bMid(B2_L, B2_R, 'Maintenance window'),
        bMid(B3_L, B3_R, 'L3: vendor TAM'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pure1 capacity alerts'),
        bMid(B2_L, B2_R, 'Dedup interval 5 min'),
        bMid(B3_L, B3_R, 'P1: war room bridge'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AIOps predicted fail'),
        bMid(B2_L, B2_R, 'Correlated grouping'),
        bMid(B3_L, B3_R, 'SLA: 15-min response'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('SMTP relay: on-prem MTA (Postfix/Exchange) · PagerDuty: SaaS · ServiceNow: on-prem or SaaS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Severity          = Critical/Warning/Info classification applied to each alert'))
    lines.append(txt_row('Suppression rule  = Policy silencing alerts during maintenance or known-issue windows'))
    lines.append(txt_row('Deduplication     = Preventing repeat notifications for the same active alert condition'))
    lines.append(txt_row('Escalation policy = Tiered response path: L1 auto-ticket → L2 page → L3 vendor → P1 bridge'))
    lines.append(txt_row('Maintenance window= Scheduled suppression period applied to specific objects or groups'))
    lines.append(txt_row('PagerDuty         = SaaS on-call paging platform; ingests alerts via API or email integration'))
    lines.append(txt_row('ServiceNow ITSM   = Incident and change management platform; receives alert-driven tickets'))
    lines.append(txt_row('SMTP relay        = Internal mail transfer agent routing notification emails'))
    lines.append(txt_row('Correlated group  = Multiple alerts from different sources mapped to a single incident'))
    lines.append(txt_row('SLA               = Service Level Agreement; defines maximum acceptable response time'))
    lines.append(txt_row('P1 bridge         = Priority-1 war-room call convened when critical systems are impacted'))
    lines.append(txt_row('Alert fatigue     = Operator desensitisation caused by excessive or low-quality alerts'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-dashboard-standards',
    'docs/monitoring/dashboard-standards/index.md',
    'Dashboard standards — naming, layout, and visualisation conventions',
)
def monitoring_dashboard_standards():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Monitoring — Dashboard Standards'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Dashboard Standards — Naming, Layout, Widget, and Data Source Conventions')))
    lines.append(R(bMid(IV_L, IV_R, 'Naming: <PRODUCT>-<DOMAIN>-<SCOPE> e.g. ARIA-VSPHERE-CLUSTER-PERF')))
    lines.append(R(bMid(IV_L, IV_R, 'Layout: header summary row · detail grid · trend charts · capacity strip')))
    lines.append(R(bMid(IV_L, IV_R, 'Widgets: scoreboard (current state) · time-series (trend) · heatmap (distribution)')))
    lines.append(R(bMid(IV_L, IV_R, 'Colour: green <70% · amber 70-85% · red >85% for capacity and CPU/mem utilisation')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Consistent dashboards reduce MTTR by ensuring operators know exactly where to look'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Naming Standard'),
        bMid(B2_L, B2_R, 'Widget Types'),
        bMid(B3_L, B3_R, 'Governance'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Product prefix'),
        bMid(B2_L, B2_R, 'Scoreboard: KPIs'),
        bMid(B3_L, B3_R, 'Owner per dashboard'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Domain segment'),
        bMid(B2_L, B2_R, 'Time-series: trend'),
        bMid(B3_L, B3_R, 'Review cycle: Q1'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Scope segment'),
        bMid(B2_L, B2_R, 'Heatmap: distrib'),
        bMid(B3_L, B3_R, 'Version in title'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'No spaces/special'),
        bMid(B2_L, B2_R, 'List: top-N items'),
        bMid(B3_L, B3_R, 'Archived not deleted'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Version suffix'),
        bMid(B2_L, B2_R, 'Alert widget: count'),
        bMid(B3_L, B3_R, 'RBAC: read-only pub'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Dashboards reside in Aria Operations UI · Nexus Dashboard NDI · Pure1 portal · CloudIQ SaaS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Scoreboard widget = Single-value tile showing current state with colour threshold band'))
    lines.append(txt_row('Time-series widget= Line/area chart plotting metric values over a configurable time window'))
    lines.append(txt_row('Heatmap widget    = Grid colouring cells by metric value; useful for per-VM or per-host views'))
    lines.append(txt_row('KPI               = Key Performance Indicator; top-level metric surfaced in the header row'))
    lines.append(txt_row('Capacity strip    = Bottom row of a dashboard showing remaining headroom per resource type'))
    lines.append(txt_row('RBAC              = Role-Based Access Control; governs who can edit vs. view a dashboard'))
    lines.append(txt_row('Threshold band    = Numeric ranges mapped to green/amber/red colour codings'))
    lines.append(txt_row('Dashboard owner   = Team member accountable for accuracy and maintenance of the dashboard'))
    lines.append(txt_row('Archived          = Dashboard removed from active view but retained for audit/history'))
    lines.append(txt_row('MTTR              = Mean Time To Resolve; reduced when dashboards are consistent and clear'))
    lines.append(txt_row('Top-N list        = Widget ranking objects by metric value; identifies worst offenders quickly'))
    lines.append(txt_row('Version suffix    = e.g. v2; indicates updated dashboard replacing a prior published version'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-event-correlation',
    'docs/monitoring/event-correlation/index.md',
    'Event correlation — linking alerts to root causes across domains',
)
def monitoring_event_correlation():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Monitoring — Event Correlation'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Event Correlation — Linking Multi-Domain Alerts to a Single Root Cause')))
    lines.append(R(bMid(IV_L, IV_R, 'Sources: Aria Ops · CloudIQ · NDI · Pure1 · syslog · SNMP traps · vCenter events')))
    lines.append(R(bMid(IV_L, IV_R, 'Correlation engine: time-window grouping · object-relationship traversal')))
    lines.append(R(bMid(IV_L, IV_R, 'Output: single correlated incident in ServiceNow · suppressed child alerts')))
    lines.append(R(bMid(IV_L, IV_R, 'Tools: Aria Ops correlation rules · AIOps root-cause suggestions · NDI change analysis')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Correlation reduces noise by grouping 10–100 alerts into a single actionable incident'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert Ingestion'),
        bMid(B2_L, B2_R, 'Correlation Logic'),
        bMid(B3_L, B3_R, 'Incident Output'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Aria Ops OOTB rules'),
        bMid(B2_L, B2_R, 'Time-window: 5 min'),
        bMid(B3_L, B3_R, 'ServiceNow P2 ticket'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CloudIQ SNMP/API'),
        bMid(B2_L, B2_R, 'Object relationship'),
        bMid(B3_L, B3_R, 'Parent alert visible'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NDI anomaly events'),
        bMid(B2_L, B2_R, 'Topology traversal'),
        bMid(B3_L, B3_R, 'Children suppressed'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Syslog messages'),
        bMid(B2_L, B2_R, 'AIOps ML grouping'),
        bMid(B3_L, B3_R, 'RCA note attached'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter tasks/events'),
        bMid(B2_L, B2_R, 'Change-correlation'),
        bMid(B3_L, B3_R, 'Operator notified'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Correlation runs in Aria Ops analytics node · AIOps SaaS ML pipeline · NDI Insights app'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Root cause        = Underlying fault that triggered one or more downstream alert conditions'))
    lines.append(txt_row('Time-window       = Period during which alerts are grouped for correlation (default 5 min)'))
    lines.append(txt_row('Object relationship= Topology link (e.g. VM→host→cluster) used to trace cause to effect'))
    lines.append(txt_row('Topology traversal= Walking the inventory graph from child to ancestor to find root object'))
    lines.append(txt_row('Correlated incident= Single ITSM ticket representing a group of related alerts'))
    lines.append(txt_row('Child alert        = Alert subordinate to a parent; suppressed when parent is active'))
    lines.append(txt_row('Change-correlation = Linking an alert to a recent change record as probable cause'))
    lines.append(txt_row('OOTB rules         = Out-of-the-box correlation rules shipped with Aria Operations'))
    lines.append(txt_row('ML grouping        = AIOps machine-learning model clustering alerts by causal similarity'))
    lines.append(txt_row('RCA note           = Root Cause Analysis note attached to the incident by the platform'))
    lines.append(txt_row('SNMP trap          = UDP event message sent by infrastructure to a monitoring collector'))
    lines.append(txt_row('Suppression        = Silencing child alerts once a parent incident is open'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-health-monitoring',
    'docs/monitoring/health-monitoring/index.md',
    'Health monitoring — platform-wide health checks and scoring',
)
def monitoring_health_monitoring():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Monitoring — Health Monitoring'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Health Monitoring — Composite Health Scores and Component-Level Checks')))
    lines.append(R(bMid(IV_L, IV_R, 'Domains: vSphere (Aria) · Dell storage (CloudIQ) · Fabric (NDI) · Pure storage (Pure1)')))
    lines.append(R(bMid(IV_L, IV_R, 'Check types: availability · performance · capacity · configuration · security posture')))
    lines.append(R(bMid(IV_L, IV_R, 'Health score: 0-100 composite; weighted by criticality; drives alert priority')))
    lines.append(R(bMid(IV_L, IV_R, 'Cadence: real-time streaming (NDI/Pure1) · 5-min polling (Aria) · hourly (CloudIQ)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  A degraded health score is a leading indicator — act before a component fails fully'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Check Categories'),
        bMid(B2_L, B2_R, 'Scoring Method'),
        bMid(B3_L, B3_R, 'Response Actions'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Availability check'),
        bMid(B2_L, B2_R, '0-100 composite'),
        bMid(B3_L, B3_R, 'Alert auto-trigger'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Performance check'),
        bMid(B2_L, B2_R, 'Weighted by role'),
        bMid(B3_L, B3_R, 'Ticket auto-create'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity check'),
        bMid(B2_L, B2_R, 'Trend adjustment'),
        bMid(B3_L, B3_R, 'Runbook link attach'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Config compliance'),
        bMid(B2_L, B2_R, 'Anomaly penalty'),
        bMid(B3_L, B3_R, 'Escalation fire'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Security posture'),
        bMid(B2_L, B2_R, 'Historical baseline',),
        bMid(B3_L, B3_R, 'Dashboard update'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Health checks run in: Aria Analytics node · CloudIQ SaaS · NDI Insights app · Pure1 SaaS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Health score      = 0-100 composite aggregating availability, performance, and capacity metrics'))
    lines.append(txt_row('Availability check= Ping/API test confirming a component is reachable and responding'))
    lines.append(txt_row('Performance check = Metric comparison against baseline thresholds (e.g. CPU/latency/IOPS)'))
    lines.append(txt_row('Capacity check    = Remaining headroom evaluation; flags when approaching configured limits'))
    lines.append(txt_row('Config compliance = Verifying running config matches approved baseline or compliance pack'))
    lines.append(txt_row('Security posture  = Check for open ports, default credentials, missing patches'))
    lines.append(txt_row('Anomaly penalty   = Score deduction applied when ML model detects unusual behaviour'))
    lines.append(txt_row('Trend adjustment  = Score modifier based on trajectory; degrading trend lowers score faster'))
    lines.append(txt_row('Runbook link      = URL to remediation steps automatically attached to a health alert'))
    lines.append(txt_row('Weighted scoring  = Higher-criticality checks contribute proportionally more to overall score'))
    lines.append(txt_row('Leading indicator = Metric that degrades before an outage; enables proactive response'))
    lines.append(txt_row('Historical baseline= Learned normal behaviour used to calibrate anomaly detection'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-log-retention',
    'docs/monitoring/log-retention/index.md',
    'Log retention — policies for on-prem and cloud log storage',
)
def monitoring_log_retention():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Monitoring — Log Retention'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Log Retention — Policies, Storage Tiers, and Compliance Requirements')))
    lines.append(R(bMid(IV_L, IV_R, 'Log types: syslog · vCenter events · API audit · security audit · performance data')))
    lines.append(R(bMid(IV_L, IV_R, 'Tiers: hot (NFS/local, 30 days) · warm (object store, 90 days) · cold (archive, 1 yr)')))
    lines.append(R(bMid(IV_L, IV_R, 'Compliance: SOC2/ISO27001 require 12-month minimum for security audit logs')))
    lines.append(R(bMid(IV_L, IV_R, 'Tools: Aria Log Insight · rsyslog · Splunk forward · S3-compatible archive')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Retention tiers balance query speed vs. storage cost — hot for ops, cold for compliance'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Hot Tier (30 days)'),
        bMid(B2_L, B2_R, 'Warm Tier (90 days)'),
        bMid(B3_L, B3_R, 'Cold Tier (1 year+)'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NFS or local SSD'),
        bMid(B2_L, B2_R, 'Object store (S3)'),
        bMid(B3_L, B3_R, 'Glacier/deep archive'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Full-text search'),
        bMid(B2_L, B2_R, 'Compressed gzip'),
        bMid(B3_L, B3_R, 'Encrypted at rest'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Sub-second query'),
        bMid(B2_L, B2_R, 'Index retained 30d'),
        bMid(B3_L, B3_R, 'Restore: 4-hr SLA'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Log Insight bucket'),
        bMid(B2_L, B2_R, 'Policy-auto-move'),
        bMid(B3_L, B3_R, 'Legal hold flag'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Syslog stream live'),
        bMid(B2_L, B2_R, 'Security audit logs'),
        bMid(B3_L, B3_R, 'Compliance audit'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Aria Log Insight VM on vSphere · NFS datastore for hot tier · MinIO/S3 for warm/cold tiers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Hot tier          = Fast-access storage for recent logs; supports real-time search'))
    lines.append(txt_row('Warm tier         = Compressed object storage; slower but cost-efficient for 30-90 day range'))
    lines.append(txt_row('Cold tier         = Deep archive; minimal cost; long restore times; used for compliance'))
    lines.append(txt_row('Retention policy  = Rule defining how long a log type is kept and when it transitions tiers'))
    lines.append(txt_row('Log Insight       = VMware Aria Log Insight; on-prem log aggregation and search platform'))
    lines.append(txt_row('rsyslog           = Linux syslog daemon; ingests and forwards RFC-5424 syslog messages'))
    lines.append(txt_row('Legal hold        = Flag preventing log deletion regardless of retention policy expiry'))
    lines.append(txt_row('SOC2              = Service Organization Control 2; audit framework requiring log retention'))
    lines.append(txt_row('ISO 27001         = Information security management standard with log evidence requirements'))
    lines.append(txt_row('Gzip compression  = Lossless compression reducing warm-tier storage by 60-80%'))
    lines.append(txt_row('Object store      = S3-compatible storage backend for warm/cold log archiving'))
    lines.append(txt_row('Auto-move policy  = Lifecycle rule automatically migrating logs between tiers on schedule'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-metrics-baseline',
    'docs/monitoring/metrics-baseline/index.md',
    'Metrics baseline — defining normal operating ranges for threshold tuning',
)
def monitoring_metrics_baseline():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Monitoring — Metrics Baseline'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Metrics Baseline — Documenting Normal Ranges to Drive Accurate Alert Thresholds')))
    lines.append(R(bMid(IV_L, IV_R, 'Key metrics: CPU util · memory util · storage IOPS/latency · network throughput')))
    lines.append(R(bMid(IV_L, IV_R, 'Baseline period: 4-week rolling window captures daily and weekly patterns')))
    lines.append(R(bMid(IV_L, IV_R, 'Methods: percentile banding (p50/p95/p99) · seasonal adjustment · learned anomaly')))
    lines.append(R(bMid(IV_L, IV_R, 'Output: documented threshold table per object type used in all monitoring tools')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  A stale baseline creates false positives or misses real anomalies — review quarterly'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Compute Metrics'),
        bMid(B2_L, B2_R, 'Storage Metrics'),
        bMid(B3_L, B3_R, 'Network Metrics'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CPU util: warn 80%'),
        bMid(B2_L, B2_R, 'IOPS: warn 70% max'),
        bMid(B3_L, B3_R, 'Throughput: 70%'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Mem util: warn 85%'),
        bMid(B2_L, B2_R, 'Latency: warn 2ms'),
        bMid(B3_L, B3_R, 'Error rate: <0.01%'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CPU ready: warn 5%'),
        bMid(B2_L, B2_R, 'Cap: warn 75% full'),
        bMid(B3_L, B3_R, 'Drops: warn >10/s'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Co-stop: warn 3%'),
        bMid(B2_L, B2_R, 'Queue depth: warn'),
        bMid(B3_L, B3_R, 'RTT: warn >5ms'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Swap: crit >0 MB/s'),
        bMid(B2_L, B2_R, 'Rebuild time: 4hr'),
        bMid(B3_L, B3_R, 'CRC errors: 0'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Baseline data sourced from: Aria Operations · CloudIQ · Pure1 · NDI — reviewed quarterly'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Baseline          = Statistical representation of normal operating behaviour over a time window'))
    lines.append(txt_row('p50               = 50th percentile (median); typical operating value'))
    lines.append(txt_row('p95               = 95th percentile; near-peak value; used for warn threshold'))
    lines.append(txt_row('p99               = 99th percentile; extreme peak; used for critical threshold'))
    lines.append(txt_row('CPU ready         = Time a VM waits for a physical CPU; >5% indicates contention'))
    lines.append(txt_row('Co-stop           = SMP VM waiting for all vCPUs; >3% indicates over-provisioned vCPUs'))
    lines.append(txt_row('Memory balloon    = VMware reclamation driver; active ballooning indicates memory pressure'))
    lines.append(txt_row('Seasonal adjust   = Accounting for day-of-week or time-of-day patterns in thresholds'))
    lines.append(txt_row('Queue depth       = Number of outstanding I/O requests; elevated = storage saturation'))
    lines.append(txt_row('Learned anomaly   = ML-derived deviation from historical pattern rather than static threshold'))
    lines.append(txt_row('Threshold table   = Reference document listing warn/crit values per metric per object type'))
    lines.append(txt_row('False positive    = Alert firing when conditions are actually normal; caused by stale baseline'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-syslog',
    'docs/monitoring/syslog/index.md',
    'Syslog — centralised syslog collection and forwarding architecture',
)
def monitoring_syslog():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Monitoring — Syslog'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Syslog — Centralised Log Collection: RFC 5424 over UDP/514 and TLS/6514')))
    lines.append(R(bMid(IV_L, IV_R, 'Sources: ESXi hosts · vCenter · NSX managers · storage arrays · network switches')))
    lines.append(R(bMid(IV_L, IV_R, 'Collectors: rsyslog/syslog-ng on-prem · Aria Log Insight · Splunk forwarder')))
    lines.append(R(bMid(IV_L, IV_R, 'Parsing: structured data fields: facility · severity · hostname · msgid · SD')))
    lines.append(R(bMid(IV_L, IV_R, 'ESXi config: esxcli system syslog config set --loghost=<IP>:514 --protocol=udp')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  TLS transport (port 6514) is required for syslog crossing security zone boundaries'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Sources'),
        bMid(B2_L, B2_R, 'Collectors'),
        bMid(B3_L, B3_R, 'Consumers'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ESXi: UDP 514'),
        bMid(B2_L, B2_R, 'rsyslog HA pair'),
        bMid(B3_L, B3_R, 'Aria Log Insight'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter: UDP 514'),
        bMid(B2_L, B2_R, 'syslog-ng relay'),
        bMid(B3_L, B3_R, 'Splunk indexer'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX: TLS 6514'),
        bMid(B2_L, B2_R, 'Log Insight agent'),
        bMid(B3_L, B3_R, 'SIEM correlation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Storage: SNMP+syslog'),
        bMid(B2_L, B2_R, 'Queue: 10k msg/s'),
        bMid(B3_L, B3_R, 'Alert rules engine'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Switches: UDP 514'),
        bMid(B2_L, B2_R, 'TLS cert rotation'),
        bMid(B3_L, B3_R, 'Retention policy'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('rsyslog VMs: 2x on dedicated VLAN · Log Insight cluster on vSphere · NFS for log storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RFC 5424          = IETF standard defining syslog message format with structured data'))
    lines.append(txt_row('Facility          = Log category code (e.g. kern=0, user=1, mail=2, daemon=3)'))
    lines.append(txt_row('Severity          = Log level: 0=Emergency · 1=Alert · 2=Crit · 3=Err · 4=Warn · 5=Notice'))
    lines.append(txt_row('rsyslog           = High-performance Linux syslog daemon; supports TCP/UDP/TLS/RELP'))
    lines.append(txt_row('syslog-ng         = Enterprise syslog daemon with advanced filtering and routing'))
    lines.append(txt_row('Log Insight       = VMware Aria Log Insight; structured log search and alerting'))
    lines.append(txt_row('TLS 6514          = Encrypted syslog transport; required for cross-zone log forwarding'))
    lines.append(txt_row('RELP              = Reliable Event Logging Protocol; guaranteed delivery over TCP'))
    lines.append(txt_row('SD (structured)   = RFC 5424 key=value pairs in the structured-data section of syslog'))
    lines.append(txt_row('esxcli syslog     = ESXi command to configure remote syslog destination and protocol'))
    lines.append(txt_row('SIEM              = Security Information and Event Management; consumes syslog for threat detection'))
    lines.append(txt_row('Queue depth       = In-memory message buffer in collector; overflow causes message loss'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ═══════════════════════════════════════════════════════════════════════════════
# ARIA OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

@kb_diagram(
    'monitoring-aria-ops',
    'docs/monitoring/aria-operations/index.md',
    'Aria Operations overview — VMware Aria Ops (vROps) platform summary',
)
def monitoring_aria_ops():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Platform Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Operations (vROps) — Analytics-Driven Infrastructure Monitoring')))
    lines.append(R(bMid(IV_L, IV_R, 'Architecture: Master node + Replica node + Collector nodes (data nodes optional)')))
    lines.append(R(bMid(IV_L, IV_R, 'Data sources: vCenter · NSX · vSAN · Storage adapters (Unity, PowerStore, ONTAP)')))
    lines.append(R(bMid(IV_L, IV_R, 'Key features: capacity forecasting · anomaly detection · compliance · workload opt')))
    lines.append(R(bMid(IV_L, IV_R, 'Access: HTTPS/443 · REST API · vracli · vami_config · vRSLCM lifecycle')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Aria Ops is the primary on-prem analytics tool for all vSphere, NSX, and vSAN workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Integrations'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Master node'),
        bMid(B2_L, B2_R, 'Alert management'),
        bMid(B3_L, B3_R, 'vCenter adapter'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Replica node'),
        bMid(B2_L, B2_R, 'Capacity planning'),
        bMid(B3_L, B3_R, 'NSX adapter'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collector node(s)'),
        bMid(B2_L, B2_R, 'Dashboards'),
        bMid(B3_L, B3_R, 'Storage adapters'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Data node (opt)'),
        bMid(B2_L, B2_R, 'Compliance packs'),
        bMid(B3_L, B3_R, 'ServiceNow plugin'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'REST API :443'),
        bMid(B2_L, B2_R, 'Workload optimise'),
        bMid(B3_L, B3_R, 'Log Insight plugin'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Aria Ops cluster: 3+ VMs on vSphere · Minimum 4 vCPU/16 GB per node · vPostgres embedded DB'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master node       = Primary analytics node; hosts UI, REST API, and orchestration services'))
    lines.append(txt_row('Replica node      = Hot standby for master; promotes automatically on master failure'))
    lines.append(txt_row('Collector node    = Remote data collector; deployed near data sources to reduce WAN load'))
    lines.append(txt_row('Data node         = Additional analytics/storage node; added for large-scale environments'))
    lines.append(txt_row('Adapter           = Plugin connecting Aria Ops to a data source (vCenter, NSX, storage, etc.)'))
    lines.append(txt_row('Compliance pack   = Pre-built policy set (e.g. CIS, DISA STIG) for configuration compliance'))
    lines.append(txt_row('Capacity forecast = ML projection of when a resource reaches its configured threshold'))
    lines.append(txt_row('Workload optimize = Aria Ops recommendation to rebalance VMs across hosts for efficiency'))
    lines.append(txt_row('vracli            = Command-line interface for Aria Ops cluster administration'))
    lines.append(txt_row('vami_config       = VAMI-based configuration CLI for network and services on Aria Ops appliance'))
    lines.append(txt_row('vRSLCM            = vRealize Suite Lifecycle Manager; deploys and upgrades Aria Ops'))
    lines.append(txt_row('REST API          = HTTPS API on port 443; used for alert queries, object inventory, reports'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-aria-ops-arch',
    'docs/monitoring/aria-operations/architecture/index.md',
    'Aria Operations architecture — cluster topology and data flow',
)
def monitoring_aria_ops_arch():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations Cluster Architecture — Nodes, Data Flow, and HA Design')))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster: Master (primary) + Replica (HA) + Collector(s) + optional Data node(s)')))
    lines.append(R(bMid(IV_L, IV_R, 'Data flow: adapters collect → collector node buffers → master analytics engine')))
    lines.append(R(bMid(IV_L, IV_R, 'Storage: embedded Cassandra (time-series) + vPostgres (relational metadata)')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: nodes communicate on TCP 443/10443 · collectors use outbound TCP 443')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Collector nodes are placed in each site or vPod to keep data collection local'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Master Node'),
        bMid(B2_L, B2_R, 'Collector Node'),
        bMid(B3_L, B3_R, 'Data Node'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Analytics engine'),
        bMid(B2_L, B2_R, 'Remote adapter'),
        bMid(B3_L, B3_R, 'Cassandra shard'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'UI + REST API'),
        bMid(B2_L, B2_R, 'Buffer 5-min data'),
        bMid(B3_L, B3_R, 'Scales capacity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vPostgres DB'),
        bMid(B2_L, B2_R, 'TCP 443 upstream'),
        bMid(B3_L, B3_R, '>5000 objects'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cassandra primary'),
        bMid(B2_L, B2_R, 'No UI component'),
        bMid(B3_L, B3_R, 'Added via UI wizard'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HA: replica ready'),
        bMid(B2_L, B2_R, 'Per-site deploy'),
        bMid(B3_L, B3_R, 'Rebalances auto'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('All nodes are VMs on vSphere · Master: 4 vCPU/16 GB min · Data node: 8 vCPU/32 GB'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cassandra         = Apache distributed time-series DB used by Aria Ops for metric storage'))
    lines.append(txt_row('vPostgres         = PostgreSQL fork embedded in Aria Ops; stores inventory and configuration'))
    lines.append(txt_row('Adapter instance  = Running adapter configuration connecting to a specific data source'))
    lines.append(txt_row('Buffer            = Collector-side temporary storage holding metrics before master upload'))
    lines.append(txt_row('TCP 443/10443     = Intra-cluster communication ports between nodes'))
    lines.append(txt_row('Analytics engine  = Master-node service computing baselines, anomalies, and recommendations'))
    lines.append(txt_row('Replica node      = Mirrors master state; takes over UI and analytics on master failure'))
    lines.append(txt_row('HA failover       = Automatic promotion of replica to master when master heartbeat is lost'))
    lines.append(txt_row('vPod              = VMware Pod; a discrete compute/network unit with its own collector'))
    lines.append(txt_row('Object count      = Total monitored resources; drives node-sizing requirements'))
    lines.append(txt_row('Rebalance         = Redistribution of Cassandra data across data nodes after scale-out'))
    lines.append(txt_row('TCP outbound      = Collector-to-master direction; only outbound TCP 443 required from collector'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-aria-ops-arch-how-it-works',
    'docs/monitoring/aria-operations/architecture/how-it-works/index.md',
    'Aria Operations — how data collection and analytics work',
)
def monitoring_aria_ops_arch_how_it_works():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Aria Operations — How It Works'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations Data Pipeline — Collection · Storage · Analysis · Output')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 1: Adapter polls vCenter/NSX/storage every 5 minutes via API')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 2: Collector buffers metrics locally then ships to master analytics engine')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 3: Analytics computes baselines, forecasts, anomaly scores, compliance')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 4: Alerts triggered → dashboard updated → recommendations published')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  The 5-minute poll cycle is the default; adapters support custom collection intervals'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collection'),
        bMid(B2_L, B2_R, 'Analytics'),
        bMid(B3_L, B3_R, 'Outputs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Adapter API poll'),
        bMid(B2_L, B2_R, 'Dynamic threshold'),
        bMid(B3_L, B3_R, 'Alerts in UI'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '5-min interval'),
        bMid(B2_L, B2_R, 'Capacity forecast'),
        bMid(B3_L, B3_R, 'REST API alerts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Object discovery'),
        bMid(B2_L, B2_R, 'Anomaly detect'),
        bMid(B3_L, B3_R, 'Dashboards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Metric tagging'),
        bMid(B2_L, B2_R, 'Compliance check'),
        bMid(B3_L, B3_R, 'Reports PDF/CSV'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collector buffer'),
        bMid(B2_L, B2_R, 'Workload reclaim',),
        bMid(B3_L, B3_R, 'ServiceNow ticket'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Data sources on same network segment as collector nodes — all on-prem vSphere environment'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Poll interval     = Frequency at which an adapter queries a data source (default 5 min)'))
    lines.append(txt_row('Dynamic threshold = Adaptive warn/crit level computed from rolling baseline statistics'))
    lines.append(txt_row('Object discovery  = Automatic inventory scan finding new VMs, hosts, and datastores'))
    lines.append(txt_row('Metric tagging    = Associating metadata labels to metrics for filtering and grouping'))
    lines.append(txt_row('Capacity forecast = Time-series projection predicting when a resource will be exhausted'))
    lines.append(txt_row('Anomaly score     = 0-100 deviation score; high values indicate abnormal behaviour'))
    lines.append(txt_row('Workload reclaim  = Recommendation to right-size over-provisioned VMs'))
    lines.append(txt_row('Compliance check  = Test of object config against a compliance pack policy rule'))
    lines.append(txt_row('REST API alert    = JSON alert object served at /api/alerts for external consumption'))
    lines.append(txt_row('Report            = Scheduled PDF or CSV output of dashboard or capacity data'))
    lines.append(txt_row('OOTB adapter      = Out-of-the-box adapter shipping with Aria Ops (vCenter, NSX, vSAN)'))
    lines.append(txt_row('MP (Management Pack)= Community or vendor adapter extending Aria Ops to new data sources'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-aria-ops-arch-design',
    'docs/monitoring/aria-operations/architecture/design-standards/index.md',
    'Aria Operations architecture design standards',
)
def monitoring_aria_ops_arch_design():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Architecture Design Standards'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations Design Standards — Sizing, HA, Network, and Naming Conventions')))
    lines.append(R(bMid(IV_L, IV_R, 'Sizing: Master 4vCPU/16GB · Replica 4vCPU/16GB · Collector 2vCPU/8GB per 3000 obj')))
    lines.append(R(bMid(IV_L, IV_R, 'HA: always deploy Replica node; target RPO<5 min, RTO<10 min on master failure')))
    lines.append(R(bMid(IV_L, IV_R, 'Naming: vrops-master-01, vrops-replica-01, vrops-col-<site>-01')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: dedicate monitoring VLAN; allow TCP 443 collector→master; TLS enforced')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Design decisions must be documented in the platform design record before deployment'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Sizing Rules'),
        bMid(B2_L, B2_R, 'HA Design'),
        bMid(B3_L, B3_R, 'Network Design'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Master: 4vCPU/16G'),
        bMid(B2_L, B2_R, 'Replica: mandatory'),
        bMid(B3_L, B3_R, 'VLAN: monitoring'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collector: 2vCPU'),
        bMid(B2_L, B2_R, 'RPO: <5 min'),
        bMid(B3_L, B3_R, 'TCP 443 col→mstr'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '3000 obj/collector'),
        bMid(B2_L, B2_R, 'RTO: <10 min'),
        bMid(B3_L, B3_R, 'TLS 1.2 minimum'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Data node @5000+'),
        bMid(B2_L, B2_R, 'Auto-failover on'),
        bMid(B3_L, B3_R, 'DNS round-robin'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk: SSD/NVMe'),
        bMid(B2_L, B2_R, 'vSphere DRS anti'),
        bMid(B3_L, B3_R, 'Firewall rule doc'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Master and Replica on separate ESXi hosts (DRS anti-affinity rule) · SSD datastore required'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Anti-affinity rule= DRS rule keeping Master and Replica VMs on separate physical hosts'))
    lines.append(txt_row('RPO               = Recovery Point Objective; maximum data loss acceptable (5 min for Aria Ops)'))
    lines.append(txt_row('RTO               = Recovery Time Objective; maximum time to restore service (10 min target)'))
    lines.append(txt_row('Monitoring VLAN   = Dedicated network segment for monitoring traffic; isolates collection'))
    lines.append(txt_row('SSD datastore     = Solid-state backed storage; required for Cassandra write performance'))
    lines.append(txt_row('TLS 1.2           = Minimum transport security version; TLS 1.3 preferred'))
    lines.append(txt_row('DNS round-robin   = Multiple A records for load distribution across collector endpoints'))
    lines.append(txt_row('Platform design record= Document capturing all design decisions for audit and review'))
    lines.append(txt_row('Auto-failover     = Automatic promotion of replica without operator intervention'))
    lines.append(txt_row('DRS               = Distributed Resource Scheduler; manages VM placement on vSphere'))
    lines.append(txt_row('Firewall rule doc = Documented ACL entries for all monitoring-plane TCP/UDP flows'))
    lines.append(txt_row('NVMe              = Non-Volatile Memory Express; fastest storage interface for DB workloads'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-aria-ops-arch-integrations',
    'docs/monitoring/aria-operations/architecture/integrations/index.md',
    'Aria Operations architecture integrations — adapters and plugins',
)
def monitoring_aria_ops_arch_integrations():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Architecture Integrations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations Integrations — Adapters, Plugins, and Outbound Connectors')))
    lines.append(R(bMid(IV_L, IV_R, 'OOTB adapters: vCenter · NSX · vSAN · Horizon · Tanzu · Site Recovery')))
    lines.append(R(bMid(IV_L, IV_R, 'Storage MPs: Dell Unity · Dell PowerStore · NetApp ONTAP · Pure Storage')))
    lines.append(R(bMid(IV_L, IV_R, 'Outbound: ServiceNow (ITSM) · REST notification · email · SNMP trap · Log Insight')))
    lines.append(R(bMid(IV_L, IV_R, 'Auth: vCenter SSO · local admin · LDAP/AD · certificate-based service accounts')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Each adapter requires a dedicated service account with read-only or specific API roles'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Inbound Adapters'),
        bMid(B2_L, B2_R, 'Storage MPs'),
        bMid(B3_L, B3_R, 'Outbound Plugins'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter adapter'),
        bMid(B2_L, B2_R, 'Dell Unity MP'),
        bMid(B3_L, B3_R, 'ServiceNow plugin'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX-T adapter'),
        bMid(B2_L, B2_R, 'Dell PowerStore MP'),
        bMid(B3_L, B3_R, 'REST notify'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN adapter'),
        bMid(B2_L, B2_R, 'NetApp ONTAP MP'),
        bMid(B3_L, B3_R, 'Email SMTP'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Horizon adapter'),
        bMid(B2_L, B2_R, 'Pure Storage MP'),
        bMid(B3_L, B3_R, 'SNMP trap send'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Tanzu adapter'),
        bMid(B2_L, B2_R, 'PowerMax/VMAX MP'),
        bMid(B3_L, B3_R, 'Log Insight fwd'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Adapters run on Aria Ops nodes · MPs installed via VMware Marketplace or vendor portal'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Management Pack   = Vendor-supplied adapter bundle extending Aria Ops to a new data source'))
    lines.append(txt_row('OOTB adapter      = Out-of-the-box adapter bundled with Aria Operations installation'))
    lines.append(txt_row('Service account   = Dedicated read-only account used by adapter to authenticate to source'))
    lines.append(txt_row('Outbound plugin   = Connector sending alert/event data from Aria Ops to ITSM or notify'))
    lines.append(txt_row('REST notification = HTTP POST to a webhook URL when an Aria Ops alert fires'))
    lines.append(txt_row('vCenter SSO       = Single Sign-On; Aria Ops uses vCenter SSO for user authentication'))
    lines.append(txt_row('LDAP/AD           = Directory authentication for Aria Ops local users'))
    lines.append(txt_row('ServiceNow plugin = Aria Ops plugin creating incidents or changes in ServiceNow on alert'))
    lines.append(txt_row('Log Insight fwd   = Plugin forwarding Aria Ops events to Aria Log Insight for correlation'))
    lines.append(txt_row('SNMP trap         = SNMPv2/v3 trap generated by Aria Ops and sent to an NMS'))
    lines.append(txt_row('VMware Marketplace= Online portal for downloading Management Packs for Aria products'))
    lines.append(txt_row('Certificate auth  = TLS client certificate used instead of username/password for adapters'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-aria-ops-ops',
    'docs/monitoring/aria-operations/operations/index.md',
    'Aria Operations daily operations — health checks and maintenance tasks',
)
def monitoring_aria_ops_ops():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations Day-2 Operations — Health, Maintenance, and Housekeeping Tasks')))
    lines.append(R(bMid(IV_L, IV_R, 'Daily checks: cluster health · adapter status · alert queue depth · disk usage')))
    lines.append(R(bMid(IV_L, IV_R, 'Weekly tasks: review capacity forecasts · compliance report · stale alert cleanup')))
    lines.append(R(bMid(IV_L, IV_R, 'Monthly: log rotation · user audit · MP version check · certificate expiry review')))
    lines.append(R(bMid(IV_L, IV_R, 'Emergency: vracli restart service · cluster rejoin · support bundle collection')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Log the support bundle path before engaging VMware TAM: /data/support_bundle/'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Checks'),
        bMid(B2_L, B2_R, 'Weekly Tasks'),
        bMid(B3_L, B3_R, 'Monthly Tasks'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cluster health OK'),
        bMid(B2_L, B2_R, 'Capacity forecast'),
        bMid(B3_L, B3_R, 'Log rotation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Adapter status OK'),
        bMid(B2_L, B2_R, 'Compliance report'),
        bMid(B3_L, B3_R, 'User audit'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert queue <500'),
        bMid(B2_L, B2_R, 'Stale alert purge'),
        bMid(B3_L, B3_R, 'MP version check'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk <80% full'),
        bMid(B2_L, B2_R, 'Dashboard review'),
        bMid(B3_L, B3_R, 'Cert expiry scan'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collector reachable'),
        bMid(B2_L, B2_R, 'Group membership'),
        bMid(B3_L, B3_R, 'Backup verify'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Operations tasks performed via Aria Ops UI (HTTPS/443) or vracli SSH on master node'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vracli            = Aria Ops CLI: vracli cluster status · vracli services restart'))
    lines.append(txt_row('Cluster health    = UI indicator aggregating node status, service health, and Cassandra ring'))
    lines.append(txt_row('Adapter status    = Green/Yellow/Red collector connectivity state in Administration > Adapters'))
    lines.append(txt_row('Alert queue       = Count of active unacknowledged alerts; >500 requires triage'))
    lines.append(txt_row('Support bundle    = Compressed diagnostic archive: vracli support-bundle collect'))
    lines.append(txt_row('Log rotation      = Automated log file cycling to prevent disk exhaustion'))
    lines.append(txt_row('Stale alert purge = Cancelling alerts whose monitored object no longer exists'))
    lines.append(txt_row('Certificate expiry= TLS cert used by adapter or UI; must be renewed before expiry'))
    lines.append(txt_row('Compliance report = Scheduled export of policy violation counts per compliance pack'))
    lines.append(txt_row('MP version check  = Verifying Management Packs match vendor release notes'))
    lines.append(txt_row('User audit        = Review of local and AD-synced users for inactive or excessive roles'))
    lines.append(txt_row('Cassandra ring    = Distributed DB health; vracli cassandra status shows ring state'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-aria-ops-alerts',
    'docs/monitoring/aria-operations/alerts/index.md',
    'Aria Operations alerts — symptom-based alert definitions and policies',
)
def monitoring_aria_ops_alerts():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Alerts'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations Alert Framework — Symptoms, Recommendations, and Outbound Actions')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert anatomy: Alert Definition → Symptom(s) → Recommendation → Action')))
    lines.append(R(bMid(IV_L, IV_R, 'Symptoms: metric threshold · property change · event (fault/task) · message event')))
    lines.append(R(bMid(IV_L, IV_R, 'Impact: Health · Risk · Efficiency — each drives different response priority')))
    lines.append(R(bMid(IV_L, IV_R, 'Outbound: email · REST · ServiceNow · SNMP trap · Log Insight notification')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Impact type drives dashboard placement: Health=Ops board · Risk=Capacity board'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Symptom Types'),
        bMid(B2_L, B2_R, 'Impact Types'),
        bMid(B3_L, B3_R, 'Outbound Actions'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Metric threshold'),
        bMid(B2_L, B2_R, 'Health impact'),
        bMid(B3_L, B3_R, 'Email SMTP'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Property change'),
        bMid(B2_L, B2_R, 'Risk impact'),
        bMid(B3_L, B3_R, 'REST webhook'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Event (fault)'),
        bMid(B2_L, B2_R, 'Efficiency impact'),
        bMid(B3_L, B3_R, 'ServiceNow ticket'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Message event'),
        bMid(B2_L, B2_R, 'Criticality 1-5'),
        bMid(B3_L, B3_R, 'SNMP trap'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'KPI symptom'),
        bMid(B2_L, B2_R, 'Wait cycle conf',),
        bMid(B3_L, B3_R, 'Log Insight notify'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Alert engine runs on Aria Ops master node · outbound connectors configured in Administration'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Alert definition  = Named policy grouping one or more symptoms with a recommendation'))
    lines.append(txt_row('Symptom           = Specific condition triggering an alert (metric, property, event, message)'))
    lines.append(txt_row('Recommendation    = Suggested remediation step linked to an alert definition'))
    lines.append(txt_row('Health impact     = Alert affecting current operational state (e.g. CPU critical)'))
    lines.append(txt_row('Risk impact       = Alert indicating future degradation (e.g. disk will fill in 7 days)'))
    lines.append(txt_row('Efficiency impact = Alert flagging resource waste (e.g. oversized idle VMs)'))
    lines.append(txt_row('Criticality       = 1-5 scale; 1=Critical, 5=Info; drives UI badge colour'))
    lines.append(txt_row('Wait cycle        = Number of collection cycles a symptom must persist before alert fires'))
    lines.append(txt_row('KPI symptom       = Symptom based on a KPI metric defined in a dashboard super metric'))
    lines.append(txt_row('Super metric      = Custom metric formula combining multiple raw metrics'))
    lines.append(txt_row('Cancel alert      = Manual or automated resolution of an active alert'))
    lines.append(txt_row('Outbound action   = Configured connector sending alert payload to external system'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-aria-ops-capacity',
    'docs/monitoring/aria-operations/capacity/index.md',
    'Aria Operations capacity — forecasting and right-sizing',
)
def monitoring_aria_ops_capacity():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Capacity'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations Capacity Management — Forecasting, Right-Sizing, and What-If')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity models: Demand model (usage trend) · Allocation model (provisioned CPU/mem)')))
    lines.append(R(bMid(IV_L, IV_R, 'Forecast horizon: 30 / 60 / 90 days configurable per object type')))
    lines.append(R(bMid(IV_L, IV_R, 'Right-sizing: oversized VMs flagged; reclaim CPU/mem/disk recommendations')))
    lines.append(R(bMid(IV_L, IV_R, 'What-if: add N VMs and see projected impact on cluster headroom')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Run what-if analysis before any major workload migration to validate headroom'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity Models'),
        bMid(B2_L, B2_R, 'Forecasting'),
        bMid(B3_L, B3_R, 'Right-Sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Demand model'),
        bMid(B2_L, B2_R, '30-day horizon'),
        bMid(B3_L, B3_R, 'Oversized VMs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Allocation model'),
        bMid(B2_L, B2_R, '60-day horizon'),
        bMid(B3_L, B3_R, 'Undersized VMs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Custom buffers'),
        bMid(B2_L, B2_R, '90-day horizon'),
        bMid(B3_L, B3_R, 'Reclaim CPU/mem'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Policy overrides'),
        bMid(B2_L, B2_R, 'What-if: add VMs'),
        bMid(B3_L, B3_R, 'Reclaim disk'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Per-cluster scope'),
        bMid(B2_L, B2_R, 'Trend visualise'),
        bMid(B3_L, B3_R, 'Batch action'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Capacity analytics on Aria Ops master · data feeds: vCenter/vSAN/storage adapters'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Demand model      = Capacity model tracking actual usage trend over time'))
    lines.append(txt_row('Allocation model  = Capacity model tracking provisioned (allocated) CPU and memory'))
    lines.append(txt_row('Buffer            = Reserved headroom percentage excluded from usable capacity calc'))
    lines.append(txt_row('Forecast horizon  = Number of days projected; longer = less accurate but more strategic'))
    lines.append(txt_row('What-if analysis  = Simulation adding/removing workloads to predict capacity impact'))
    lines.append(txt_row('Right-sizing      = Recommendation to adjust vCPU/vMem to match actual usage patterns'))
    lines.append(txt_row('Reclaim           = Action recovering idle CPU, memory, or disk from oversized VMs'))
    lines.append(txt_row('Oversized VM      = VM provisioned significantly above its measured peak utilisation'))
    lines.append(txt_row('Undersized VM     = VM hitting its provisioned limits; causes performance degradation'))
    lines.append(txt_row('Batch action      = Applying right-size recommendations to multiple VMs simultaneously'))
    lines.append(txt_row('Policy override   = Cluster-specific capacity policy overriding global default settings'))
    lines.append(txt_row('Headroom          = Remaining available capacity before the configured utilisation limit'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-aria-ops-cli',
    'docs/monitoring/aria-operations/cli-reference/index.md',
    'Aria Operations CLI reference — vracli and vami_config commands',
)
def monitoring_aria_ops_cli():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Aria Operations — CLI Reference'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations CLI — vracli and vami_config Command Reference')))
    lines.append(R(bMid(IV_L, IV_R, 'vracli: cluster management · service control · support bundle · user management')))
    lines.append(R(bMid(IV_L, IV_R, 'vami_config: network settings · NTP · DNS · proxy · password on VAMI interface')))
    lines.append(R(bMid(IV_L, IV_R, 'REST API: curl -s -k -u admin:<pw> https://<vrops>/api/alerts | python3 -m json.tool')))
    lines.append(R(bMid(IV_L, IV_R, 'SSH access: root@<vrops-master> — key-based or password per security policy')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Always run vracli cluster status before and after any service restart'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vracli Commands'),
        bMid(B2_L, B2_R, 'vami_config Cmds'),
        bMid(B3_L, B3_R, 'REST API Calls'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'cluster status'),
        bMid(B2_L, B2_R, 'network get'),
        bMid(B3_L, B3_R, 'GET /api/alerts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'cluster restart'),
        bMid(B2_L, B2_R, 'ntp get/set'),
        bMid(B3_L, B3_R, 'GET /api/resources'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'services list'),
        bMid(B2_L, B2_R, 'dns get/set'),
        bMid(B3_L, B3_R, 'POST /api/auth'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'support-bundle'),
        bMid(B2_L, B2_R, 'proxy set'),
        bMid(B3_L, B3_R, 'DELETE /api/alerts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'cassandra status'),
        bMid(B2_L, B2_R, 'passwd set'),
        bMid(B3_L, B3_R, 'GET /api/reports'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('CLI runs on Aria Ops nodes via SSH · vami_config runs as root on VAMI management console'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vracli            = Primary Aria Ops CLI; available via SSH on master and replica nodes'))
    lines.append(txt_row('vami_config       = VAMI appliance management CLI for network, DNS, NTP, and proxy settings'))
    lines.append(txt_row('cluster status    = Reports node connectivity, service state, and Cassandra ring health'))
    lines.append(txt_row('support-bundle    = Collects logs, configs, and diagnostics into a .tar.gz for GSS/TAM'))
    lines.append(txt_row('cassandra status  = Checks Cassandra ring membership, token distribution, and replication'))
    lines.append(txt_row('VAMI              = Virtual Appliance Management Infrastructure; web UI on port 5480'))
    lines.append(txt_row('REST API          = HTTPS API on port 443; requires token or Basic auth'))
    lines.append(txt_row('Bearer token      = JWT returned by POST /api/auth; used in Authorization header'))
    lines.append(txt_row('GSS               = Global Support Services; VMware/Broadcom first-line support'))
    lines.append(txt_row('TAM               = Technical Account Manager; assigned VMware support engineer'))
    lines.append(txt_row('services list     = Lists all Aria Ops services and their running/stopped state'))
    lines.append(txt_row('proxy set         = Configures HTTP proxy for Aria Ops outbound internet connectivity'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'monitoring-aria-ops-dashboards',
    'docs/monitoring/aria-operations/dashboards/index.md',
    'Aria Operations dashboards — built-in and custom dashboard design',
)
def monitoring_aria_ops_dashboards():
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Dashboards'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations Dashboards — Built-in, Custom, and Shared Dashboard Management')))
    lines.append(R(bMid(IV_L, IV_R, 'Built-in: Executive Overview · Capacity Overview · vSphere Health · NSX Health')))
    lines.append(R(bMid(IV_L, IV_R, 'Widget types: scoreboard · time-series · heatmap · topology · alert list · object list')))
    lines.append(R(bMid(IV_L, IV_R, 'Interaction: drill-down from widget to object · filter by tag · time-range picker')))
    lines.append(R(bMid(IV_L, IV_R, 'Sharing: publish to group · export JSON · import · embed in external portal')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Import community dashboards from VMware {code} exchange to accelerate deployment'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Built-in Dashboards'),
        bMid(B2_L, B2_R, 'Custom Widgets'),
        bMid(B3_L, B3_R, 'Sharing & Export'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Executive Overview'),
        bMid(B2_L, B2_R, 'Scoreboard'),
        bMid(B3_L, B3_R, 'Publish to group'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity Overview'),
        bMid(B2_L, B2_R, 'Time-series chart'),
        bMid(B3_L, B3_R, 'Export JSON'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere Health'),
        bMid(B2_L, B2_R, 'Heatmap widget'),
        bMid(B3_L, B3_R, 'Import JSON'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX Health'),
        bMid(B2_L, B2_R, 'Topology map'),
        bMid(B3_L, B3_R, 'Embed iframe'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert Overview'),
        bMid(B2_L, B2_R, 'Alert list widget',),
        bMid(B3_L, B3_R, 'Clone/customise'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Dashboards stored in Aria Ops vPostgres DB · UI served on HTTPS/443 from master node'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Built-in dashboard = Pre-configured dashboard shipped with Aria Operations'))
    lines.append(txt_row('Scoreboard widget  = Tile displaying current metric value with colour-coded threshold'))
    lines.append(txt_row('Time-series widget = Line chart of metric over configurable time window'))
    lines.append(txt_row('Heatmap widget     = Grid with colour-coded cells per object; fast outlier detection'))
    lines.append(txt_row('Topology widget    = Visual map of object relationships (VM → host → cluster)'))
    lines.append(txt_row('Alert list widget  = Live count and list of active alerts for filtered object set'))
    lines.append(txt_row('Drill-down         = Clicking widget navigates to the individual object detail page'))
    lines.append(txt_row('Tag filter         = Filtering dashboard widgets by vSphere tag or Aria Ops group tag'))
    lines.append(txt_row('Export JSON        = Serialising dashboard definition for sharing or backup'))
    lines.append(txt_row('VMware {code}      = VMware community code exchange hosting dashboard JSON templates'))
    lines.append(txt_row('Super metric       = Custom calculated metric combining multiple raw metrics in a formula'))
    lines.append(txt_row('Clone dashboard    = Copying an existing dashboard as starting point for customisation'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines
