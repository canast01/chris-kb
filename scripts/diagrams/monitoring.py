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


# ── Aria Operations remaining pages ──────────────────────────────────────────

W2 = 103

@kb_diagram('monitoring-aria-ops-design', 'docs/monitoring/aria-operations/design-standards/index.md', 'Aria Operations design standards')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Sizing & Topology'), bMid(B2_L, B2_R, 'Data Retention'), bMid(B3_L, B3_R, 'High Availability'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'XS: 1 node ≤1k obj'), bMid(B2_L, B2_R, 'Metrics: 6 months'), bMid(B3_L, B3_R, '2-node minimum'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'S: 1 node ≤5k obj'), bMid(B2_L, B2_R, 'Events: 6 months'), bMid(B3_L, B3_R, 'Witness optional'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'M: 2 nodes ≤20k'), bMid(B2_L, B2_R, 'Snapshots: 30 days'), bMid(B3_L, B3_R, 'vSphere HA enabled'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'L: 4 nodes ≤50k'), bMid(B2_L, B2_R, 'Purge via vROps UI'), bMid(B3_L, B3_R, 'DRS anti-affinity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'XL: 8 nodes ≤150k'), bMid(B2_L, B2_R, 'Backup: nightly'), bMid(B3_L, B3_R, 'Shared datastore'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Naming, tagging, and alert policy standards drive consistent operation across all environments'))
    lines.append(txt_row())
    lines.append(R(arrow([16, 50, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Naming Standards'), bMid(B2_L, B2_R, 'Alert Policy Design'), bMid(B3_L, B3_R, 'Adapter Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Groups: env-team'), bMid(B2_L, B2_R, 'Symptom first'), bMid(B3_L, B3_R, '1 adapter/instance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dashboards: func-obj'), bMid(B2_L, B2_R, 'Threshold reviewed Q'), bMid(B3_L, B3_R, 'Credential vault'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Reports: sched-scope'), bMid(B2_L, B2_R, 'No duplicate alerts'), bMid(B3_L, B3_R, 'PAK from VMware'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alerts: sev-component'), bMid(B2_L, B2_R, 'Notify via outbound'), bMid(B3_L, B3_R, 'Test before prod'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tags: env+owner'), bMid(B2_L, B2_R, 'Escalation defined'), bMid(B3_L, B3_R, 'Version locked'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Master node: 4 vCPU 16 GB min · Data node: 8 vCPU 32 GB · NFS/vSAN for VMDK storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Object = Monitored entity in Aria Ops (VM, host, datastore, application component)'))
    lines.append(txt_row('Super metric = Formula combining raw metrics into a single derived KPI'))
    lines.append(txt_row('Policy = Named ruleset controlling collection intervals, thresholds, and alert actions'))
    lines.append(txt_row('Group = Dynamic or static collection of objects; policies and alerts applied at group level'))
    lines.append(txt_row('PAK = Plugin/adapter package installed via Administration > Solutions'))
    lines.append(txt_row('Symptom = Condition evaluated against metric; true/false trigger for alert'))
    lines.append(txt_row('Recommendation = Action suggested when alert fires (KB link, runbook, automated action)'))
    lines.append(txt_row('Outbound plugin = Webhook or SMTP/SNMP connector for alert notification'))
    lines.append(txt_row('Anti-affinity = DRS rule keeping Aria Ops nodes on separate ESXi hosts'))
    lines.append(txt_row('Retention = Days Aria Ops stores raw metrics before rollup and eventual purge'))
    lines.append(txt_row('Witness node = Tie-breaking node used in 2-node HA cluster to avoid split-brain'))
    lines.append(txt_row('NFS datastore = Shared storage enabling vSphere HA restart of Aria Ops VMs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-aria-ops-integration', 'docs/monitoring/aria-operations/integration/index.md', 'Aria Operations integrations')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations — Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Core Platform Integrations')))
    lines.append(R(bMid(L, RR, 'vCenter: primary data source — inventory, metrics, events, tags, alarms')))
    lines.append(R(bMid(L, RR, 'NSX: network topology, logical switches, edges, DFW rules, and BGP state')))
    lines.append(R(bMid(L, RR, 'vSAN: cluster health, capacity, performance, and disk group metrics')))
    lines.append(R(bMid(L, RR, 'Aria Automation: request lifecycle, deployment state, and cost data')))
    lines.append(R(bMid(L, RR, 'Aria Logs: log-based alerts forwarded to Aria Ops as notifications')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Adapters connect Aria Ops to external systems; each adapter has its own credential and schedule'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Infrastructure Adapters'), bMid(B2_L, B2_R, 'ITSM / Notification'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dell EMC: PowerStore'), bMid(B2_L, B2_R, 'ServiceNow: CMDB sync'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pure Storage FlashArray'), bMid(B2_L, B2_R, 'SMTP: email alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NetApp ONTAP adapter'), bMid(B2_L, B2_R, 'SNMP trap outbound'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cisco UCS adapter'), bMid(B2_L, B2_R, 'Slack/Teams webhook'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'AWS/Azure cloud'), bMid(B2_L, B2_R, 'PagerDuty REST API'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Adapter processes run inside Aria Ops master node · outbound plugins use TCP 443/25/162'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Adapter = PAK-based plugin that collects data from a specific source (storage, cloud, network)'))
    lines.append(txt_row('PAK file = Plugin/adapter package distributed by VMware or partner; installed via Solutions UI'))
    lines.append(txt_row('Credential = Stored username/password or token used by adapter to authenticate to source'))
    lines.append(txt_row('Collection interval = Frequency at which adapter queries source; typically 5 minutes'))
    lines.append(txt_row('Outbound plugin = Connector for sending alert notifications (SMTP, SNMP, REST, webhook)'))
    lines.append(txt_row('CMDB sync = Pushing Aria Ops object inventory into ServiceNow CMDB via adapter'))
    lines.append(txt_row('Tag propagation = vSphere tags imported by vCenter adapter and applied to Aria Ops objects'))
    lines.append(txt_row('Cloud account = AWS/Azure subscription registered in Aria Ops for cross-cloud visibility'))
    lines.append(txt_row('REST adapter = Generic HTTP adapter for any REST API source not covered by a PAK'))
    lines.append(txt_row('Webhook = HTTP POST payload sent by outbound plugin when alert fires'))
    lines.append(txt_row('SNMP trap = UDP notification sent to network management system on alert condition'))
    lines.append(txt_row('Alert notification = Outbound message triggered when alert changes state (firing or resolved)'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-aria-ops-lifecycle', 'docs/monitoring/aria-operations/lifecycle/index.md', 'Aria Operations lifecycle management')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations — Lifecycle Management'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Install / Deploy'), bMid(B2_L, B2_R, 'Upgrade Path'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OVA deploy to vCenter'), bMid(B2_L, B2_R, 'Check interop matrix'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Size per node count'), bMid(B2_L, B2_R, 'PAK upgrade first'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'License via Aria LCM'), bMid(B2_L, B2_R, 'Snapshot before upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter adapter setup'), bMid(B2_L, B2_R, 'Upgrade via Admin UI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Initial policy config'), bMid(B2_L, B2_R, 'Data nodes first'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Add data nodes'), bMid(B2_L, B2_R, 'Master node last'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Snapshots before upgrade + rollback plan required; Aria LCM preferred for orchestrated upgrades'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup & Restore'), bMid(B2_L, B2_R, 'Decommission'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'File-based backup'), bMid(B2_L, B2_R, 'Export dashboards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NFS or SCP target'), bMid(B2_L, B2_R, 'Export alert defs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Scheduled nightly'), bMid(B2_L, B2_R, 'Remove adapters'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Retention: 7 copies'), bMid(B2_L, B2_R, 'Power off VMs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Restore via Admin UI'), bMid(B2_L, B2_R, 'Delete from vCenter'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('OVA size S: 4 vCPU/16 GB · M: 8/32 · L: 16/48 · NFS backup target requires TCP 2049'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Aria LCM = Aria Lifecycle Manager; orchestrates upgrade sequencing across Aria product stack'))
    lines.append(txt_row('OVA = Open Virtual Appliance; VM image format used to deploy Aria Ops nodes'))
    lines.append(txt_row('Interop matrix = VMware compatibility matrix; confirms supported vCenter/ESXi versions'))
    lines.append(txt_row('PAK upgrade = Updating adapter packages before upgrading the core platform'))
    lines.append(txt_row('File-based backup = Aria Ops native backup creating encrypted archive of config and data'))
    lines.append(txt_row('Data node = Worker node that stores metric data and runs analytics jobs'))
    lines.append(txt_row('Master node = Primary node hosting the UI, REST API, and cluster coordinator'))
    lines.append(txt_row('Rollback = Restoring from snapshot if upgrade fails; requires VM snapshot taken before start'))
    lines.append(txt_row('License key = Aria Ops license applied via Administration > Licensing; tied to object count'))
    lines.append(txt_row('SCP target = SSH-based file copy destination for backup archives'))
    lines.append(txt_row('Admin UI = Web-based cluster management at https://<master>:5480'))
    lines.append(txt_row('Upgrade token = Short-lived credential required for cluster join during multi-node upgrade'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-aria-ops-reports', 'docs/monitoring/aria-operations/reports/index.md', 'Aria Operations reports')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations — Reports'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Built-in Reports'), bMid(B2_L, B2_R, 'Custom Reports'), bMid(B3_L, B3_R, 'Scheduling'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Inventory summary'), bMid(B2_L, B2_R, 'Add/remove metrics'), bMid(B3_L, B3_R, 'Hourly/daily/weekly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity overview'), bMid(B2_L, B2_R, 'Filter by group/tag'), bMid(B3_L, B3_R, 'Email on complete'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VM rightsizing'), bMid(B2_L, B2_R, 'Time range select'), bMid(B3_L, B3_R, 'SMTP outbound plug'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert summary'), bMid(B2_L, B2_R, 'Export PDF/CSV'), bMid(B3_L, B3_R, 'Recipient list'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Host performance'), bMid(B2_L, B2_R, 'Clone template'), bMid(B3_L, B3_R, 'Retention: 30 days'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Reports generated on master node · PDF export uses embedded renderer · SCP delivery optional'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Report template = Reusable definition of metrics, filters, and format for a report'))
    lines.append(txt_row('Clone template = Copying a built-in report template to create a customised version'))
    lines.append(txt_row('Subject view = Scope of objects a report runs against (group, tag, or all objects)'))
    lines.append(txt_row('Metric column = Individual metric added as column in tabular report section'))
    lines.append(txt_row('PDF export = Formatted report rendered to PDF; useful for executive or compliance sharing'))
    lines.append(txt_row('CSV export = Raw metric data in comma-separated format for spreadsheet analysis'))
    lines.append(txt_row('Scheduled report = Report configured to run automatically at a defined interval'))
    lines.append(txt_row('SMTP outbound = Email delivery plugin configured in Administration > Outbound Settings'))
    lines.append(txt_row('Rightsizing report = Identifies over/under-provisioned VMs based on utilisation thresholds'))
    lines.append(txt_row('Retention = Number of past report runs kept in Aria Ops; older runs purged automatically'))
    lines.append(txt_row('Time range = Historical window for report data (last 24h, 7d, 30d, custom)'))
    lines.append(txt_row('Recipient list = Named list of email addresses for scheduled report delivery'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-aria-ops-scripts', 'docs/monitoring/aria-operations/scripts/index.md', 'Aria Operations scripts reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations — Scripts Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'REST API Automation — Python / PowerShell / Bash examples')))
    lines.append(R(bMid(L, RR, 'Token auth: POST /suite-api/api/auth/token/acquire → Bearer token')))
    lines.append(R(bMid(L, RR, 'Alert query: GET /suite-api/api/alerts?status=ACTIVE → JSON list')))
    lines.append(R(bMid(L, RR, 'Resource list: GET /suite-api/api/resources?resourceKind=VirtualMachine')))
    lines.append(R(bMid(L, RR, 'Custom metric push: POST /suite-api/api/resources/{id}/stats')))
    lines.append(R(bMid(L, RR, 'Report run: POST /suite-api/api/reports → returns reportId for status poll')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Scripts automate report generation, alert bulk-acknowledge, and custom metric injection'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Operational Scripts', 'Admin Scripts'])))
    lines.append(R(sections(L, RR, [50], ['bulk-ack-alerts.py', 'export-dashboards.py'])))
    lines.append(R(sections(L, RR, [50], ['push-custom-metrics.py', 'cleanup-orphaned-objects.py'])))
    lines.append(R(sections(L, RR, [50], ['rightsizing-report.py', 'license-usage-check.py'])))
    lines.append(R(sections(L, RR, [50], ['alert-summary-csv.py', 'adapter-status-check.py'])))
    lines.append(R(sections(L, RR, [50], ['group-membership-audit.py', 'backup-trigger.sh'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('REST API on master node TCP 443 · scripts run from any host with network access to master'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('suite-api = Aria Ops REST API path prefix; all endpoints start with /suite-api/api'))
    lines.append(txt_row('Bearer token = Short-lived auth token from /auth/token/acquire; valid ~30 minutes'))
    lines.append(txt_row('resourceKind = Object type filter (VirtualMachine, HostSystem, Datastore, etc.)'))
    lines.append(txt_row('Custom metric = Externally pushed metric stored alongside collected metrics for an object'))
    lines.append(txt_row('Bulk acknowledge = API call to mark multiple active alerts as acknowledged in one request'))
    lines.append(txt_row('Report trigger = POST to /api/reports to generate on-demand report without UI interaction'))
    lines.append(txt_row('Orphaned object = Object remaining in Aria Ops after its source (VM, host) is deleted'))
    lines.append(txt_row('Dashboard JSON = Exported dashboard definition; can be imported via API on another instance'))
    lines.append(txt_row('Adapter status = Health state of an adapter (collecting, no-data, error) queryable via API'))
    lines.append(txt_row('License usage = Object count against licensed capacity; reportable via Admin API'))
    lines.append(txt_row('Group membership = Objects belonging to a group; listable via /api/groups/{id}/members'))
    lines.append(txt_row('Retry logic = Exponential backoff pattern for handling 429/503 from Aria Ops API'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-aria-ops-security', 'docs/monitoring/aria-operations/security/index.md', 'Aria Operations security')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations — Security'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Authentication & Access'), bMid(B2_L, B2_R, 'Network Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local admin account'), bMid(B2_L, B2_R, 'HTTPS only TCP 443'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vIDM SSO optional'), bMid(B2_L, B2_R, 'Firewall: mgmt VLAN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP/AD integration'), bMid(B2_L, B2_R, 'No direct internet'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC: role → object'), bMid(B2_L, B2_R, 'Cluster TCP 443/6061'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Least-privilege roles'), bMid(B2_L, B2_R, 'TLS 1.2+ enforced'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Audit log in vROps'), bMid(B2_L, B2_R, 'Cert replace via UI'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Hardening follows VMware STIG; custom cert replaces self-signed; credential vault for adapters'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Credential Management'), bMid(B2_L, B2_R, 'Hardening'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Adapter credentials'), bMid(B2_L, B2_R, 'VMware STIG applied'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Stored encrypted'), bMid(B2_L, B2_R, 'Disable SSH post-config'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rotate on breach'), bMid(B2_L, B2_R, 'Root pw complexity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service accounts'), bMid(B2_L, B2_R, 'NTP configured'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Minimum permissions'), bMid(B2_L, B2_R, 'Syslog to SIEM'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Credentials stored encrypted in Aria Ops internal DB · audit log in /var/log/vmware/vcops'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM = VMware Identity Manager; enables SAML SSO for Aria Ops UI login'))
    lines.append(txt_row('RBAC = Role-Based Access Control; permissions defined per role and scoped to object groups'))
    lines.append(txt_row('Credential = Stored adapter username/password; encrypted at rest in Aria Ops DB'))
    lines.append(txt_row('Service account = Dedicated low-privilege vCenter user for Aria Ops adapter authentication'))
    lines.append(txt_row('Read-only role = vCenter role with Browse Datastore and Read-Only granted; sufficient for adapter'))
    lines.append(txt_row('STIG = Security Technical Implementation Guide; VMware-published hardening baseline'))
    lines.append(txt_row('Audit log = Record of user logins, role changes, and configuration modifications'))
    lines.append(txt_row('TLS 1.2 = Minimum TLS version enforced for all Aria Ops API and UI connections'))
    lines.append(txt_row('Custom cert = CA-signed certificate replacing self-signed; applied via Admin UI HTTPS settings'))
    lines.append(txt_row('Cluster port 6061 = Internal Aria Ops cluster communication port; restricted to cluster subnet'))
    lines.append(txt_row('Syslog forwarding = Shipping Aria Ops audit events to external SIEM (Splunk, Elastic)'))
    lines.append(txt_row('SSH disable = SSH access to appliance disabled post-deployment except during maintenance'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-aria-ops-troubleshooting', 'docs/monitoring/aria-operations/troubleshooting/index.md', 'Aria Operations troubleshooting')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Adapter Not Collecting'), bMid(B2_L, B2_R, 'UI / API Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check credential'), bMid(B2_L, B2_R, 'Restart web service'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify network reach'), bMid(B2_L, B2_R, 'Check master status'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review adapter log'), bMid(B2_L, B2_R, 'vracli cluster list'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Re-test in Solutions'), bMid(B2_L, B2_R, 'Clear browser cache'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check firewall rules'), bMid(B2_L, B2_R, 'Check cert validity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Reinstall PAK'), bMid(B2_L, B2_R, 'Collect support bundle'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Support bundle via vrops-support-get command; logs in /var/log/vmware/vcops on each node'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Performance Issues'), bMid(B2_L, B2_R, 'Alert / Policy Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check node CPU/mem'), bMid(B2_L, B2_R, 'Check symptom state'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review object count'), bMid(B2_L, B2_R, 'Policy inheritance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Reduce collection int'), bMid(B2_L, B2_R, 'Alert dedup check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Add data nodes'), bMid(B2_L, B2_R, 'Outbound plugin test'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Archive old data'), bMid(B2_L, B2_R, 'Notification history'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Logs: /var/log/vmware/vcops · support bundle: vrops-support-get from master node SSH'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Support bundle = Compressed archive of logs and config; used by VMware GSS for diagnosis'))
    lines.append(txt_row('vrops-support-get = CLI command on Aria Ops appliance to collect support bundle'))
    lines.append(txt_row('Solutions UI = Administration > Solutions; shows adapter status and allows credential test'))
    lines.append(txt_row('Cluster list = vracli cluster list shows node health: ONLINE/OFFLINE/INITIALIZING'))
    lines.append(txt_row('PAK reinstall = Remove and re-add adapter package; resets adapter state without data loss'))
    lines.append(txt_row('Collection interval = How often adapter polls source; reduce if master is overloaded'))
    lines.append(txt_row('Symptom state = True/False evaluation of a threshold condition for an object'))
    lines.append(txt_row('Policy inheritance = Child policy inheriting settings from parent; override at child level'))
    lines.append(txt_row('Alert dedup = Aria Ops suppressing repeat alerts for same symptom within cool-down window'))
    lines.append(txt_row('Notification history = Log of outbound alert notifications sent; in Administration > Outbound'))
    lines.append(txt_row('Object count = Number of monitored objects; growth reduces collection capacity per node'))
    lines.append(txt_row('Data node = Worker node; adding nodes scales collection capacity linearly'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-aria-ops-vendor-support', 'docs/monitoring/aria-operations/vendor-support/index.md', 'Aria Operations vendor support')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations — Vendor Support'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Support Model — Broadcom (formerly VMware) GSS')))
    lines.append(R(bMid(L, RR, 'Aria Operations support bundled with vSphere+ / VCF subscription')))
    lines.append(R(bMid(L, RR, 'Ticket via Broadcom Support Portal: support.broadcom.com')))
    lines.append(R(bMid(L, RR, 'Severity 1: 24x7 phone; S2: business hours + 2-hour callback')))
    lines.append(R(bMid(L, RR, 'GSS requires support bundle (vrops-support-get) for most cases')))
    lines.append(R(bMid(L, RR, 'Interop matrix: interopmatrix.broadcom.com — confirm vCenter/ESXi versions')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Partner adapters (Dell, Pure, NetApp) supported by respective vendor PAK maintainers'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Resources', 'Process'])))
    lines.append(R(sections(L, RR, [50], ['Broadcom KBs: kb.vmware.com', 'Open case: support.broadcom.com'])))
    lines.append(R(sections(L, RR, [50], ['Aria Ops release notes', 'Collect: vrops-support-get'])))
    lines.append(R(sections(L, RR, [50], ['VMware {code} developer forum', 'Attach bundle to case'])))
    lines.append(R(sections(L, RR, [50], ['Interop matrix (broadcom)', 'Escalate to Sev-1 if prod down'])))
    lines.append(R(sections(L, RR, [50], ['vExpert community blogs', 'TAM for proactive guidance'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Support bundle collected from master node · upload via SFTP or Broadcom case portal'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GSS = Global Support Services; Broadcom tier-1 support organisation'))
    lines.append(txt_row('Support bundle = vrops-support-get output; compressed archive of logs sent to GSS'))
    lines.append(txt_row('Severity 1 = Production down or critical feature unavailable; 24x7 response'))
    lines.append(txt_row('Severity 2 = Major functionality impaired; business-hours priority response'))
    lines.append(txt_row('Interop matrix = Official compatibility table for Aria Ops with vCenter/ESXi versions'))
    lines.append(txt_row('PAK partner = Adapter vendor (Dell, Pure Storage, NetApp) responsible for their adapter PAK'))
    lines.append(txt_row('TAM = Technical Account Manager; proactive Broadcom contact for licensed customers'))
    lines.append(txt_row('KB = Knowledge Base article; searchable at kb.vmware.com with KB<number>'))
    lines.append(txt_row('Release notes = Per-version document listing fixes, new features, and known issues'))
    lines.append(txt_row('VMware {code} = Developer community and code exchange at code.vmware.com'))
    lines.append(txt_row('vExpert = VMware community recognition program; blogs and forums by Aria Ops experts'))
    lines.append(txt_row('Escalation = Requesting case move to Severity 1 or senior engineer when impact increases'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── CloudIQ diagrams ──────────────────────────────────────────────────────────

@kb_diagram('monitoring-cloudiq', 'docs/monitoring/cloudiq/index.md', 'CloudIQ — Dell cloud-based AI/ML storage monitoring')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Dell Cloud-Based AI/ML Storage Monitoring'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'CloudIQ: SaaS monitoring platform for Dell infrastructure — PowerStore, PowerScale, PowerFlex')))
    lines.append(R(bMid(L, RR, 'AI/ML engine analyses telemetry to predict failures, score health, and recommend actions')))
    lines.append(R(bMid(L, RR, 'Data collected by secure gateway (or direct) and pushed to Dell cloud over HTTPS/443')))
    lines.append(R(bMid(L, RR, 'No on-premises agent required for most Dell storage — native telemetry forwarding')))
    lines.append(R(bMid(L, RR, 'Access via cloudiq.dell.com — browser-based; no software to install at the customer site')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Health score, anomaly detection, and capacity forecasting cover entire Dell storage estate'))
    lines.append(txt_row())
    lines.append(R(arrow([16, 50, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health & Alerts'), bMid(B2_L, B2_R, 'Capacity'), bMid(B3_L, B3_R, 'Performance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health score 0-100'), bMid(B2_L, B2_R, 'Forecast 30-90 days'), bMid(B3_L, B3_R, 'Latency/IOPS trends'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'AI anomaly detect'), bMid(B2_L, B2_R, 'Thin provision %'), bMid(B3_L, B3_R, 'Bandwidth metrics'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Email / webhook'), bMid(B2_L, B2_R, 'Tier breakdown'), bMid(B3_L, B3_R, 'Per-volume stats'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Severity levels'), bMid(B2_L, B2_R, 'Growth rate calc'), bMid(B3_L, B3_R, 'Heatmap view'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Acknowledge/snooze'), bMid(B2_L, B2_R, 'Reclamation tips'), bMid(B3_L, B3_R, 'Baseline compare'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('On-prem: Dell storage arrays · Gateway VM (if used) · Outbound TCP 443 to cloudiq.dell.com'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CloudIQ = Dell SaaS monitoring platform with AI/ML engine; browser-based at cloudiq.dell.com'))
    lines.append(txt_row('Health score = 0-100 composite score for an array; red <70, yellow 70-89, green ≥90'))
    lines.append(txt_row('Anomaly = Statistically unusual metric behaviour detected by ML model'))
    lines.append(txt_row('Secure gateway = Optional on-prem VM proxying telemetry to Dell cloud for air-gapped environments'))
    lines.append(txt_row('Telemetry = Metrics, events, and configuration data forwarded from Dell arrays to CloudIQ'))
    lines.append(txt_row('Forecast = ML-based capacity prediction showing projected full date at current growth rate'))
    lines.append(txt_row('Thin provisioning % = Ratio of allocated capacity to physical capacity; over-commit risk indicator'))
    lines.append(txt_row('Reclamation = Identifying and freeing unused or wasted allocated capacity on volumes'))
    lines.append(txt_row('Recommendation = AI-generated action to improve health score or avoid predicted issue'))
    lines.append(txt_row('IOPS = Input/Output Operations Per Second; primary storage performance metric'))
    lines.append(txt_row('Latency = Average time from request to completion; target <1ms for all-flash arrays'))
    lines.append(txt_row('Bandwidth = Data throughput in MB/s; complements IOPS for large-block workload sizing'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-arch', 'docs/monitoring/cloudiq/architecture/index.md', 'CloudIQ architecture overview')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Dell Cloud (cloudiq.dell.com) — SaaS backend')))
    lines.append(R(bMid(L, RR, 'AI/ML Engine · Time-series DB · Alert Engine · REST API · Web UI')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Telemetry flows outbound from arrays over HTTPS/443 to Dell cloud; no inbound connections'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'On-Premises Sources'), bMid(B2_L, B2_R, 'Connectivity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PowerStore native'), bMid(B2_L, B2_R, 'Direct: array → cloud'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PowerScale native'), bMid(B2_L, B2_R, 'Gateway VM optional'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PowerFlex native'), bMid(B2_L, B2_R, 'HTTPS TCP 443 only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Unity XT native'), bMid(B2_L, B2_R, 'Proxy supported'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PowerMax with DM'), bMid(B2_L, B2_R, 'SNI-based mTLS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VMAX via SRM'), bMid(B2_L, B2_R, 'No VPN required'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Dell arrays: physical hardware on-prem · Gateway VM: 2 vCPU/4 GB if needed · TCP 443 outbound'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SaaS = Software as a Service; CloudIQ hosted and operated by Dell in cloud'))
    lines.append(txt_row('Gateway VM = Optional on-prem virtual machine proxying telemetry for arrays without direct reach'))
    lines.append(txt_row('Telemetry = Metrics, logs, events, and configuration data pushed from arrays to CloudIQ'))
    lines.append(txt_row('mTLS = Mutual TLS; both client and server authenticate with certificates'))
    lines.append(txt_row('SNI = Server Name Indication; TLS extension allowing multiple hostnames on one IP'))
    lines.append(txt_row('DM = Data Mobility component for PowerMax CloudIQ registration'))
    lines.append(txt_row('Time-series DB = Database optimised for sequential metric storage and range queries'))
    lines.append(txt_row('AI/ML engine = Machine learning models trained on Dell fleet data for anomaly and failure prediction'))
    lines.append(txt_row('REST API = CloudIQ programmatic interface for custom dashboards and automation'))
    lines.append(txt_row('Native integration = Array firmware sends telemetry directly without additional software'))
    lines.append(txt_row('Proxy support = HTTP proxy configuration on gateway or array for internet access'))
    lines.append(txt_row('No inbound = CloudIQ never initiates connections to customer network; telemetry is push-only'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-arch-how', 'docs/monitoring/cloudiq/architecture/how-it-works/index.md', 'CloudIQ how it works')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Step 1: Array Registration — connect array to cloudiq.dell.com using Dell account')))
    lines.append(R(bMid(L, RR, 'Step 2: Telemetry Push — array sends metrics/events every 5 minutes over HTTPS')))
    lines.append(R(bMid(L, RR, 'Step 3: AI Processing — ML models score health, detect anomalies, forecast capacity')))
    lines.append(R(bMid(L, RR, 'Step 4: Alert Generation — violations trigger alerts; notifications via email/webhook')))
    lines.append(R(bMid(L, RR, 'Step 5: Recommendation — AI suggests corrective actions with estimated impact')))
    lines.append(R(bMid(L, RR, 'Step 6: User Action — engineer reviews, acknowledges, and implements recommendation')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Arrays on-prem · Dell cloud processing · engineer accesses via browser at cloudiq.dell.com'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Array registration = Linking a Dell storage system to a CloudIQ organisation/account'))
    lines.append(txt_row('Telemetry interval = Frequency of metric push; typically 5 minutes for most array types'))
    lines.append(txt_row('Health score = 0-100 composite score derived from multiple metric and event inputs'))
    lines.append(txt_row('Anomaly detection = ML model identifying behaviour deviating from learned baseline'))
    lines.append(txt_row('Capacity forecast = Regression model predicting when array will reach capacity threshold'))
    lines.append(txt_row('Alert = Notification generated when health score drops below threshold or anomaly detected'))
    lines.append(txt_row('Recommendation = AI-generated corrective action with priority and expected benefit'))
    lines.append(txt_row('Acknowledge = Marking alert as seen and accepted; stops re-notification'))
    lines.append(txt_row('Snooze = Temporarily silencing an alert for a defined period'))
    lines.append(txt_row('Baseline = Normal operating pattern learned by ML over initial collection window'))
    lines.append(txt_row('Organisation = CloudIQ tenant grouping arrays and users for a customer account'))
    lines.append(txt_row('Dell account = MyService360 or Dell account credential used for CloudIQ login and registration'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-arch-design', 'docs/monitoring/cloudiq/architecture/design-standards/index.md', 'CloudIQ design standards')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Registration Standards'), bMid(B2_L, B2_R, 'Alert Policy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'All arrays registered'), bMid(B2_L, B2_R, 'Email: ops-storage@'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Naming: site-model-id'), bMid(B2_L, B2_R, 'Webhook: monitoring tool'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tag by env+team'), bMid(B2_L, B2_R, 'Severity thresholds doc'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Single org per site'), bMid(B2_L, B2_R, 'Review monthly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service account only'), bMid(B2_L, B2_R, 'Escalation runbook'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('All Dell arrays must be registered · TCP 443 outbound required from storage management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Organisation = CloudIQ tenant; group all arrays from one customer/site into a single org'))
    lines.append(txt_row('Service account = Dedicated Dell account for CloudIQ integration; not a personal login'))
    lines.append(txt_row('Tag = Metadata label applied in CloudIQ to group arrays by environment, team, or location'))
    lines.append(txt_row('Naming convention = Standardised array name in CloudIQ: site-model-serial or similar'))
    lines.append(txt_row('Alert threshold = Score or metric value at which CloudIQ generates a notification'))
    lines.append(txt_row('Webhook = HTTP endpoint receiving CloudIQ alert POSTs for integration with Slack/ITSM'))
    lines.append(txt_row('Monthly review = Regular cadence to validate alert thresholds and clear stale recommendations'))
    lines.append(txt_row('Escalation runbook = Documented steps for P1 storage alert from CloudIQ to on-call engineer'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-arch-int', 'docs/monitoring/cloudiq/architecture/integrations/index.md', 'CloudIQ integrations')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Supported Arrays', 'Notification Targets'])))
    lines.append(R(sections(L, RR, [50], ['PowerStore: native integration', 'Email: SMTP to ops mailbox'])))
    lines.append(R(sections(L, RR, [50], ['PowerScale: native integration', 'Webhook: Slack/Teams/ServiceNow'])))
    lines.append(R(sections(L, RR, [50], ['PowerFlex: native integration', 'API: REST for custom tooling'])))
    lines.append(R(sections(L, RR, [50], ['Unity XT: native integration', 'MyService360: support portal link'])))
    lines.append(R(sections(L, RR, [50], ['PowerMax: via Data Mobility', 'Aria Ops: CloudIQ adapter PAK'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Arrays push telemetry to cloudiq.dell.com · CloudIQ pushes alerts to webhook targets'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Native integration = Array firmware includes CloudIQ telemetry client; no agent needed'))
    lines.append(txt_row('Data Mobility = PowerMax component handling CloudIQ registration and telemetry forwarding'))
    lines.append(txt_row('Webhook = Outbound HTTP POST from CloudIQ when alert fires; JSON payload'))
    lines.append(txt_row('REST API = CloudIQ programmatic interface for retrieving health scores and alert data'))
    lines.append(txt_row('MyService360 = Dell customer support portal; linked from CloudIQ for case creation'))
    lines.append(txt_row('Aria Ops PAK = Adapter package enabling Aria Operations to pull CloudIQ data on-prem'))
    lines.append(txt_row('SMTP notification = Email sent by CloudIQ when alert fires or score drops'))
    lines.append(txt_row('API token = Bearer token for CloudIQ REST API; generated in account settings'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-capacity', 'docs/monitoring/cloudiq/capacity/index.md', 'CloudIQ capacity management')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Capacity Management'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity Overview'), bMid(B2_L, B2_R, 'Forecasting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Total raw capacity'), bMid(B2_L, B2_R, '30/60/90 day forecast'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Used vs free'), bMid(B2_L, B2_R, 'ML growth model'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tier breakdown'), bMid(B2_L, B2_R, 'Projected full date'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Thin provision %'), bMid(B2_L, B2_R, 'Confidence band'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snapshot overhead'), bMid(B2_L, B2_R, 'Add-capacity alert'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Reclaim candidates'), bMid(B2_L, B2_R, 'Seasonal adjust'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Capacity data from array firmware · Dell cloud processes and stores trend for forecast model'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Raw capacity = Total physical storage before RAID/parity overhead'))
    lines.append(txt_row('Usable capacity = Raw minus RAID overhead; available for data'))
    lines.append(txt_row('Thin provisioning = Allocating more logical capacity than physical; deduplication + compression expand'))
    lines.append(txt_row('Forecast = ML regression on historical consumption predicting when capacity will be exhausted'))
    lines.append(txt_row('Confidence band = Upper/lower bound on forecast based on variance in historical data'))
    lines.append(txt_row('Add-capacity alert = CloudIQ alert when forecast horizon drops below threshold (e.g., 90 days)'))
    lines.append(txt_row('Reclaim candidate = Volume with zero or near-zero utilisation; flagged for decommission review'))
    lines.append(txt_row('Snapshot overhead = Capacity consumed by snapshots; tracked separately from primary data'))
    lines.append(txt_row('Tier = Storage class within an array (e.g., NVMe, SAS, SSD) each with separate capacity'))
    lines.append(txt_row('Seasonal adjustment = ML model accounting for cyclical usage spikes in forecast'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-alerts', 'docs/monitoring/cloudiq/alerts/index.md', 'CloudIQ alerts')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Alerts'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Alert Categories', 'Alert Actions'])))
    lines.append(R(sections(L, RR, [50], ['Health: score < threshold', 'Acknowledge: mark as seen'])))
    lines.append(R(sections(L, RR, [50], ['Capacity: fill date < 90d', 'Snooze: mute for N hours'])))
    lines.append(R(sections(L, RR, [50], ['Performance: latency spike', 'Dismiss: remove if false-pos'])))
    lines.append(R(sections(L, RR, [50], ['Hardware: component fault', 'Create service request'])))
    lines.append(R(sections(L, RR, [50], ['Anomaly: ML deviation', 'Link to recommendation'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Alerts generated in Dell cloud · delivered via email/webhook · viewed at cloudiq.dell.com'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Alert = CloudIQ notification for a condition requiring attention on an array'))
    lines.append(txt_row('Health alert = Fired when array health score drops below configured threshold'))
    lines.append(txt_row('Capacity alert = Fired when projected full date is within defined horizon (default 90 days)'))
    lines.append(txt_row('Performance alert = Fired when latency or IOPS deviates significantly from baseline'))
    lines.append(txt_row('Hardware alert = Firmware-detected component fault forwarded via telemetry'))
    lines.append(txt_row('Anomaly alert = ML-detected statistical deviation not matching known fault pattern'))
    lines.append(txt_row('Acknowledge = Confirms alert reviewed; suppresses repeat notification'))
    lines.append(txt_row('Snooze = Temporary suppression for a defined window; re-fires after window expires'))
    lines.append(txt_row('Dismiss = Permanent closure of alert; used for confirmed false-positives'))
    lines.append(txt_row('Service request = Dell support case created from CloudIQ alert with pre-populated diagnostics'))
    lines.append(txt_row('Recommendation = AI-generated fix linked to alert; addresses root cause'))
    lines.append(txt_row('Severity = Alert priority: Critical, Warning, Informational'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-cli', 'docs/monitoring/cloudiq/cli-reference/index.md', 'CloudIQ CLI and API reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — CLI and API Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'CloudIQ REST API — Base URL: https://cloudiq.dell.com/cloudiq/rest/v1')))
    lines.append(R(bMid(L, RR, 'Auth: Bearer token from POST /rest/v1/auth/token (client_id + client_secret)')))
    lines.append(R(bMid(L, RR, 'Systems: GET /rest/v1/storage-systems — list all registered arrays')))
    lines.append(R(bMid(L, RR, 'Health: GET /rest/v1/storage-systems/{id}/health — health score and issues')))
    lines.append(R(bMid(L, RR, 'Alerts: GET /rest/v1/alerts?filter=acknowledged eq false — active alerts')))
    lines.append(R(bMid(L, RR, 'Capacity: GET /rest/v1/storage-systems/{id}/capacity — current and forecast')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('REST API hosted at cloudiq.dell.com · API client runs from any host with internet access'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('REST API = HTTP-based programmatic interface for CloudIQ data and configuration'))
    lines.append(txt_row('Bearer token = Short-lived auth credential; obtained via client_id/client_secret exchange'))
    lines.append(txt_row('client_id = OAuth application identifier registered in CloudIQ account settings'))
    lines.append(txt_row('client_secret = OAuth secret paired with client_id; treat as password'))
    lines.append(txt_row('OData filter = Query parameter for filtering (e.g., acknowledged eq false)'))
    lines.append(txt_row('storage-systems = API resource representing a registered Dell storage array'))
    lines.append(txt_row('Health endpoint = Returns score, issue list, and component-level details for an array'))
    lines.append(txt_row('Capacity endpoint = Returns raw/usable/used capacity and forecast data'))
    lines.append(txt_row('Alerts endpoint = Returns list of alerts with severity, state, and linked recommendations'))
    lines.append(txt_row('Pagination = API uses limit/offset parameters; max 100 records per request'))
    lines.append(txt_row('Rate limiting = API enforces request limits; retry with backoff on 429 responses'))
    lines.append(txt_row('JSON response = All API responses in JSON; use jq for command-line parsing'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-design', 'docs/monitoring/cloudiq/design-standards/index.md', 'CloudIQ design standards top-level')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Onboarding Standards'), bMid(B2_L, B2_R, 'Operational Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Register all arrays'), bMid(B2_L, B2_R, 'Review weekly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Consistent naming'), bMid(B2_L, B2_R, 'Alerts to ITSM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tag env + location'), bMid(B2_L, B2_R, 'Recommendations acted'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service account only'), bMid(B2_L, B2_R, 'Capacity plan monthly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify telemetry OK'), bMid(B2_L, B2_R, 'Escalation runbook'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('All Dell arrays on TCP 443 to cloudiq.dell.com · gateway VM for restricted networks'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Telemetry verification = Confirming array shows as Connected and data age < 15 minutes'))
    lines.append(txt_row('Naming standard = site-model-id format for array display name in CloudIQ'))
    lines.append(txt_row('Tag = CloudIQ metadata label for grouping (env:prod, location:dc1, team:storage)'))
    lines.append(txt_row('Service account = Dedicated non-personal Dell account for CloudIQ org management'))
    lines.append(txt_row('ITSM integration = Webhook forwarding CloudIQ alerts to ServiceNow or similar'))
    lines.append(txt_row('Recommendation = AI action item; policy requires acting within SLA (e.g., 5 business days)'))
    lines.append(txt_row('Capacity plan = Monthly review of forecast data to plan procurement before critical threshold'))
    lines.append(txt_row('Escalation runbook = Procedure triggered by Critical severity alert in CloudIQ'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-health', 'docs/monitoring/cloudiq/health/index.md', 'CloudIQ health monitoring')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Health Monitoring'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Health Score Model: 0-100 composite per array')))
    lines.append(R(bMid(L, RR, 'Component inputs: hardware faults, performance, capacity, software events')))
    lines.append(R(bMid(L, RR, 'Score 90-100: Green — healthy · 70-89: Yellow — warning · 0-69: Red — critical')))
    lines.append(R(bMid(L, RR, 'Trend indicator: improving / steady / degrading over last 24 hours')))
    lines.append(R(bMid(L, RR, 'Issue list: individual problems contributing to score reduction with weighting')))
    lines.append(R(bMid(L, RR, 'Fleet view: all arrays ranked by health score; outliers highlighted')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Health score computed in Dell cloud from telemetry · updated approximately every 5 minutes'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Health score = Weighted composite of hardware, performance, capacity, and software inputs'))
    lines.append(txt_row('Issue = Individual contributing problem; each has a weight and recommended fix'))
    lines.append(txt_row('Trend = Direction of health score movement over trailing 24-hour window'))
    lines.append(txt_row('Fleet view = Dashboard showing all registered arrays ordered by health score'))
    lines.append(txt_row('Red array = Health score below 70; requires immediate investigation'))
    lines.append(txt_row('Yellow array = Health score 70-89; monitor closely and plan remediation'))
    lines.append(txt_row('Hardware fault = Physical component issue (drive, fan, power supply) reducing score'))
    lines.append(txt_row('Performance issue = Sustained latency or IOPS anomaly contributing to score reduction'))
    lines.append(txt_row('Software event = Firmware error or software exception recorded by array'))
    lines.append(txt_row('Weight = Relative contribution of an issue to total score reduction'))
    lines.append(txt_row('Resolved issue = Problem that cleared; score increases when issue count decreases'))
    lines.append(txt_row('Score history = 30-day time-series of health score; viewable in CloudIQ UI per array'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-integration', 'docs/monitoring/cloudiq/integration/index.md', 'CloudIQ integration guide')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Integration Guide'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ITSM Integration'), bMid(B2_L, B2_R, 'Monitoring Stack'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ServiceNow webhook'), bMid(B2_L, B2_R, 'Aria Ops adapter'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Auto-incident create'), bMid(B2_L, B2_R, 'Grafana data source'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CMDB asset link'), bMid(B2_L, B2_R, 'Splunk HTTP Event'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert → incident map'), bMid(B2_L, B2_R, 'PagerDuty webhook'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bi-directional sync'), bMid(B2_L, B2_R, 'Custom REST script'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('CloudIQ in Dell cloud · webhook receivers on-prem or in monitoring SaaS platforms'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Webhook = Outbound HTTP POST from CloudIQ when alert fires; JSON body with array details'))
    lines.append(txt_row('ServiceNow webhook = HTTP endpoint in ServiceNow receiving CloudIQ alerts as incidents'))
    lines.append(txt_row('Auto-incident = ServiceNow incident created automatically from CloudIQ alert payload'))
    lines.append(txt_row('CMDB link = Matching CloudIQ array to ServiceNow CMDB CI using serial number'))
    lines.append(txt_row('Aria Ops adapter = PAK package pulling CloudIQ health data into Aria Operations'))
    lines.append(txt_row('Grafana data source = Custom plugin or REST proxy exposing CloudIQ metrics to Grafana'))
    lines.append(txt_row('Splunk HEC = HTTP Event Collector; CloudIQ webhook forwarded for log-based correlation'))
    lines.append(txt_row('PagerDuty webhook = CloudIQ alert forwarded to PagerDuty for on-call routing'))
    lines.append(txt_row('REST script = Python/shell script polling CloudIQ API and pushing to other systems'))
    lines.append(txt_row('Bi-directional = ServiceNow incident closure reflected back to CloudIQ alert state'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-lifecycle', 'docs/monitoring/cloudiq/lifecycle/index.md', 'CloudIQ lifecycle management')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Lifecycle Management'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Onboarding'), bMid(B2_L, B2_R, 'Ongoing Maintenance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create Dell account'), bMid(B2_L, B2_R, 'Monitor telemetry age'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Register arrays'), bMid(B2_L, B2_R, 'Re-register if stale'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Configure alerts'), bMid(B2_L, B2_R, 'Update array firmware'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Add users + roles'), bMid(B2_L, B2_R, 'Rotate service account'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test webhook delivery'), bMid(B2_L, B2_R, 'Annual access review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('CloudIQ is SaaS — no on-prem component to patch · array firmware controls telemetry client'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Telemetry age = Time since last successful push from array; stale > 15 min triggers alert'))
    lines.append(txt_row('Re-registration = Removing and re-adding array to CloudIQ; resets telemetry stream'))
    lines.append(txt_row('Service account rotation = Changing Dell account password used for CloudIQ API access'))
    lines.append(txt_row('Access review = Auditing CloudIQ user list; removing departed staff and role changes'))
    lines.append(txt_row('Array firmware = On-array software; update process depends on array model (PSTCLI, ESRS)'))
    lines.append(txt_row('ESRS = EMC Secure Remote Services; gateway used by some older Dell arrays for telemetry'))
    lines.append(txt_row('CloudIQ SaaS = Hosted by Dell; no customer upgrade responsibility for the platform itself'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-ops', 'docs/monitoring/cloudiq/operations/index.md', 'CloudIQ operations')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Operations'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Daily Checks'), bMid(B2_L, B2_R, 'Weekly Tasks'), bMid(B3_L, B3_R, 'Monthly Tasks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review fleet health'), bMid(B2_L, B2_R, 'Action open alerts'), bMid(B3_L, B3_R, 'Capacity planning'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check red arrays'), bMid(B2_L, B2_R, 'Review recs'), bMid(B3_L, B3_R, 'Review thresholds'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify telemetry'), bMid(B2_L, B2_R, 'Check forecasts'), bMid(B3_L, B3_R, 'Report to mgmt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Triage new alerts'), bMid(B2_L, B2_R, 'Update ITSM'), bMid(B3_L, B3_R, 'Access review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check anomalies'), bMid(B2_L, B2_R, 'Snooze/dismiss'), bMid(B3_L, B3_R, 'Procurement plan'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Operations entirely via cloudiq.dell.com browser UI · no on-prem tooling required'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Fleet health = Overview of all registered arrays and their current health scores'))
    lines.append(txt_row('Telemetry verification = Confirming each array shows Connected and data age < 15 minutes'))
    lines.append(txt_row('Triage = Classifying new alert as actionable, false positive, or informational'))
    lines.append(txt_row('Recommendation = AI-suggested action; should be reviewed and acted on within SLA'))
    lines.append(txt_row('Forecast review = Checking projected capacity exhaustion dates for all arrays'))
    lines.append(txt_row('Snooze = Temporarily muting a known-benign alert for a defined period'))
    lines.append(txt_row('Dismiss = Closing a confirmed false-positive alert permanently'))
    lines.append(txt_row('Procurement plan = Capacity expansion request based on CloudIQ forecast horizon'))
    lines.append(txt_row('Access review = Monthly check of CloudIQ user list for stale or inappropriate access'))
    lines.append(txt_row('ITSM update = Recording CloudIQ alert actions in ServiceNow incident or problem ticket'))
    lines.append(txt_row('Threshold review = Adjusting alert trigger values based on operational experience'))
    lines.append(txt_row('Management report = Monthly summary of health trends and capacity outlook for leadership'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-recommendations', 'docs/monitoring/cloudiq/recommendations/index.md', 'CloudIQ AI recommendations')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — AI Recommendations'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'CloudIQ AI generates recommendations based on health issues and anomalies')))
    lines.append(R(bMid(L, RR, 'Categories: Performance, Capacity, Availability, Security, Best Practice')))
    lines.append(R(bMid(L, RR, 'Priority: Critical (act now), High (act soon), Medium (plan), Low (optional)')))
    lines.append(R(bMid(L, RR, 'Each recommendation: problem description, impact, suggested action, KB link')))
    lines.append(R(bMid(L, RR, 'Track status: Open → In Progress → Resolved → Dismissed')))
    lines.append(R(bMid(L, RR, 'Resolution improves health score once Dell cloud receives confirming telemetry')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Recommendations computed in Dell cloud from fleet-wide ML · no on-prem component'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Recommendation = AI action item linking a detected issue to a corrective step'))
    lines.append(txt_row('Priority = Urgency classification: Critical/High/Medium/Low'))
    lines.append(txt_row('KB link = Dell Knowledge Base article linked from recommendation for detailed steps'))
    lines.append(txt_row('Impact = Estimated health score improvement if recommendation is implemented'))
    lines.append(txt_row('In Progress = Status indicating team has started working on the recommendation'))
    lines.append(txt_row('Resolved = Recommendation marked done; CloudIQ validates via subsequent telemetry'))
    lines.append(txt_row('Dismissed = Recommendation closed without action; should include a reason comment'))
    lines.append(txt_row('Fleet-wide ML = Models trained on all registered Dell arrays globally for pattern matching'))
    lines.append(txt_row('Best practice = Recommendation to align configuration with Dell recommended settings'))
    lines.append(txt_row('Security recommendation = Flagging insecure configuration (weak auth, unencrypted replication)'))
    lines.append(txt_row('Confirming telemetry = Subsequent metric push showing issue condition no longer present'))
    lines.append(txt_row('SLA = Internal target for acting on Critical/High recommendations (e.g., within 3 business days)'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-reporting', 'docs/monitoring/cloudiq/reporting/index.md', 'CloudIQ reporting')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Reporting'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Built-in Reports'), bMid(B2_L, B2_R, 'Custom / Export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fleet health summary'), bMid(B2_L, B2_R, 'CSV capacity export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity forecast'), bMid(B2_L, B2_R, 'PDF health report'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert history'), bMid(B2_L, B2_R, 'API data pull'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Performance trends'), bMid(B2_L, B2_R, 'Schedule email'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Recommendation status'), bMid(B2_L, B2_R, 'Custom time range'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Reports generated in Dell cloud · PDF/CSV download via browser · API for automation'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Fleet health summary = Report showing all arrays with current health score and issue count'))
    lines.append(txt_row('Capacity forecast report = Per-array projected full dates for planning horizon'))
    lines.append(txt_row('Alert history = Time-series of alerts over selected period; useful for trend analysis'))
    lines.append(txt_row('Performance trend = Historical IOPS/latency/bandwidth per array over custom window'))
    lines.append(txt_row('Recommendation status = Open/resolved/dismissed counts per category and priority'))
    lines.append(txt_row('CSV export = Comma-separated raw data download; import into Excel or BI tool'))
    lines.append(txt_row('PDF report = Formatted document suitable for management review or audit'))
    lines.append(txt_row('Scheduled email = CloudIQ sending report on defined cadence to recipient list'))
    lines.append(txt_row('API data pull = REST GET calls to retrieve report data programmatically'))
    lines.append(txt_row('Custom time range = Selecting arbitrary start/end dates for historical report generation'))
    lines.append(txt_row('BI tool = Business intelligence platform (Tableau, Power BI) consuming CloudIQ CSV exports'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-scripts', 'docs/monitoring/cloudiq/scripts/index.md', 'CloudIQ scripts reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Scripts Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'CloudIQ REST API scripts — Python examples')))
    lines.append(R(bMid(L, RR, 'auth.py: obtain Bearer token via POST /rest/v1/auth/token')))
    lines.append(R(bMid(L, RR, 'get-health.py: fetch all arrays health scores; flag red arrays')))
    lines.append(R(bMid(L, RR, 'get-alerts.py: list active unacknowledged alerts; export to CSV')))
    lines.append(R(bMid(L, RR, 'capacity-forecast.py: get forecast data; alert if < 90 days to full')))
    lines.append(R(bMid(L, RR, 'recommendations.py: list open high/critical recs; post to Slack')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Scripts run from any host with internet access · Python 3.8+ with requests library'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Bearer token = Auth credential; hardcode client_id/secret or use env vars'))
    lines.append(txt_row('client_id = OAuth application ID from CloudIQ account > API access settings'))
    lines.append(txt_row('Requests library = Python HTTP library (pip install requests) for REST calls'))
    lines.append(txt_row('Flag red = Script logic to alert when health score < 70 or issue count > threshold'))
    lines.append(txt_row('CSV export = Writing API response to CSV for spreadsheet consumption'))
    lines.append(txt_row('Slack webhook = POST to Slack incoming webhook URL with formatted alert summary'))
    lines.append(txt_row('Forecast horizon = Number of days until projected capacity exhaustion'))
    lines.append(txt_row('Rate limit = CloudIQ API enforces limits; script should retry with exponential backoff'))
    lines.append(txt_row('Environment variables = Storing client_id/secret in env vars rather than hardcoding'))
    lines.append(txt_row('Cron = Scheduling script to run automatically (e.g., daily capacity check)'))
    lines.append(txt_row('OData filter = Query string for filtering API results (status eq active)'))
    lines.append(txt_row('Pagination = Handling limit/offset for large result sets in API responses'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-security', 'docs/monitoring/cloudiq/security/index.md', 'CloudIQ security')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Security'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access Control'), bMid(B2_L, B2_R, 'Data Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dell account + MFA'), bMid(B2_L, B2_R, 'TLS 1.2+ in transit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC: Admin/Viewer'), bMid(B2_L, B2_R, 'Encrypted at rest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service account only'), bMid(B2_L, B2_R, 'No config pushed to arr'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Annual access review'), bMid(B2_L, B2_R, 'Telemetry only — no data'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Audit log in CloudIQ'), bMid(B2_L, B2_R, 'Dell SOC2 compliant'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Data stored in Dell cloud datacentres · customer data isolated per tenant · SOC2 Type II'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Dell account MFA = Multi-factor authentication required for cloudiq.dell.com login'))
    lines.append(txt_row('RBAC = Role-Based Access Control; Admin (full) vs Viewer (read-only) roles'))
    lines.append(txt_row('Service account = Non-personal account for API access; password rotated per policy'))
    lines.append(txt_row('Telemetry only = CloudIQ receives metrics and events; does not access user data or files'))
    lines.append(txt_row('No config push = CloudIQ is monitoring-only; it cannot change array configuration'))
    lines.append(txt_row('TLS 1.2 = Minimum transport encryption for all CloudIQ connections'))
    lines.append(txt_row('Encrypted at rest = Telemetry data encrypted in Dell cloud storage'))
    lines.append(txt_row('SOC2 Type II = Dell security audit certification; covers data handling and access controls'))
    lines.append(txt_row('Audit log = Record of logins and configuration changes viewable in CloudIQ admin section'))
    lines.append(txt_row('Tenant isolation = Each customer organisation data separated in multi-tenant cloud'))
    lines.append(txt_row('Annual review = Yearly audit of CloudIQ users; remove stale accounts and inappropriate roles'))
    lines.append(txt_row('API token security = client_id/secret treated as password; never logged or committed to code'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-troubleshooting', 'docs/monitoring/cloudiq/troubleshooting/index.md', 'CloudIQ troubleshooting')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Array Not Reporting'), bMid(B2_L, B2_R, 'Alert/Score Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check TCP 443 outbound'), bMid(B2_L, B2_R, 'Verify telemetry age'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify DNS resolution'), bMid(B2_L, B2_R, 'Check issue list'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Re-test from array CLI'), bMid(B2_L, B2_R, 'Check threshold config'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Re-register array'), bMid(B2_L, B2_R, 'Clear false-pos dismiss'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check gateway VM'), bMid(B2_L, B2_R, 'Open Dell support case'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review array firmware'), bMid(B2_L, B2_R, 'Attach telemetry log'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('All troubleshooting via array CLI/UI and cloudiq.dell.com · Dell support via support portal'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Not reporting = Array shows Disconnected or telemetry age > 15 minutes in CloudIQ'))
    lines.append(txt_row('TCP 443 test = Telnet or curl from array management IP to cloudiq.dell.com:443'))
    lines.append(txt_row('DNS resolution = Array must resolve cloudiq.dell.com; check DNS server config on array'))
    lines.append(txt_row('Re-register = Removing array from CloudIQ and re-adding; resets telemetry stream'))
    lines.append(txt_row('Gateway VM = Check VM is powered on, has internet access, and service is running'))
    lines.append(txt_row('Telemetry age = Minutes since last data received; shown per array in CloudIQ UI'))
    lines.append(txt_row('False positive = Alert that does not represent a real issue; dismiss with reason'))
    lines.append(txt_row('Threshold = Alert trigger value; adjust if getting too many low-value notifications'))
    lines.append(txt_row('Array firmware = Older firmware may have telemetry bugs; update to supported release'))
    lines.append(txt_row('Dell support case = Open at support.dell.com with array serial and CloudIQ org name'))
    lines.append(txt_row('Telemetry log = Array-side log of CloudIQ push attempts; provided to Dell GSS'))
    lines.append(txt_row('Proxy check = If gateway VM uses proxy, verify proxy allows cloudiq.dell.com:443'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-cloudiq-vendor', 'docs/monitoring/cloudiq/vendor-support/index.md', 'CloudIQ vendor support')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'CloudIQ — Vendor Support'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Support Model — Dell Technologies GSS')))
    lines.append(R(bMid(L, RR, 'CloudIQ included with ProSupport or ProSupport Plus on eligible Dell arrays')))
    lines.append(R(bMid(L, RR, 'Open case: support.dell.com — provide array serial + CloudIQ org name')))
    lines.append(R(bMid(L, RR, 'Severity 1: production storage down + CloudIQ data gap > 1 hour')))
    lines.append(R(bMid(L, RR, 'Telemetry issues: Dell GSS can view telemetry logs from cloud backend')))
    lines.append(R(bMid(L, RR, 'Feature requests: submit via cloudiq.dell.com > Feedback link')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Dell cloud hosted · support portal at support.dell.com · 24x7 for Sev-1'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ProSupport = Dell hardware support tier; required for CloudIQ inclusion'))
    lines.append(txt_row('ProSupport Plus = Premium support tier with predictive analytics and proactive support'))
    lines.append(txt_row('GSS = Global Support Services; Dell tier-1 technical support organisation'))
    lines.append(txt_row('Array serial = Hardware identifier required for support case; found on array bezel or UI'))
    lines.append(txt_row('CloudIQ org name = Organisation display name from cloudiq.dell.com account settings'))
    lines.append(txt_row('Telemetry log = Backend log of push attempts; Dell GSS can access internally'))
    lines.append(txt_row('Data gap = Period where CloudIQ received no telemetry; shown as gap in time-series'))
    lines.append(txt_row('Severity 1 = Critical support priority; 24x7 response; production impacted'))
    lines.append(txt_row('Feature request = Submitted via UI feedback; reviewed by CloudIQ product team'))
    lines.append(txt_row('Release notes = CloudIQ changelog; SaaS platform updated by Dell without customer action'))
    lines.append(txt_row('MyService360 = Dell customer portal showing entitlements, cases, and assets'))
    lines.append(txt_row('ProSupport expiry = CloudIQ access may be affected if ProSupport lapses on array'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Dell AIOps diagrams ───────────────────────────────────────────────────────

@kb_diagram('monitoring-dell-aiops', 'docs/monitoring/dell-aiops/index.md', 'Dell AIOps — AI-driven infrastructure observability')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — AI-Driven Infrastructure Observability'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Dell AIOps: AI/ML platform ingesting metrics from Dell storage, compute, and networking')))
    lines.append(R(bMid(L, RR, 'Detects anomalies, predicts failures, and surfaces prioritised recommendations')))
    lines.append(R(bMid(L, RR, 'Deployed on-premises as VMs or containers; integrates with CloudIQ and APEX telemetry')))
    lines.append(R(bMid(L, RR, 'Dashboards, alert routing, and capacity insights from a single pane of glass')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Data flows from infrastructure → AIOps engine → dashboards, alerts, and ITSM'))
    lines.append(txt_row())
    lines.append(R(arrow([16, 50, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Data Sources'), bMid(B2_L, B2_R, 'AI Engine'), bMid(B3_L, B3_R, 'Outputs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PowerStore'), bMid(B2_L, B2_R, 'Anomaly detect'), bMid(B3_L, B3_R, 'Alert console'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PowerScale'), bMid(B2_L, B2_R, 'Failure predict'), bMid(B3_L, B3_R, 'Dashboards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PowerFlex'), bMid(B2_L, B2_R, 'Capacity forecast'), bMid(B3_L, B3_R, 'Recommendations'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'APEX platform'), bMid(B2_L, B2_R, 'Root cause'), bMid(B3_L, B3_R, 'ITSM webhook'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VxRail / VCF'), bMid(B2_L, B2_R, 'Workload insight'), bMid(B3_L, B3_R, 'API for tooling'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AIOps VMs on-prem or cloud · infrastructure arrays/servers on-prem · TCP 443 between components'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AIOps = AI for IT Operations; applying ML to operational telemetry for proactive management'))
    lines.append(txt_row('Anomaly detection = ML model identifying statistical outliers in metric streams'))
    lines.append(txt_row('Failure prediction = Model forecasting component or system failure before it occurs'))
    lines.append(txt_row('Root cause analysis = Automated correlation of events and metrics to identify failure source'))
    lines.append(txt_row('Capacity forecast = ML prediction of when capacity threshold will be reached'))
    lines.append(txt_row('Workload insight = Analysis of IO patterns, queue depth, and latency per workload'))
    lines.append(txt_row('Recommendation = AI-generated action to prevent or resolve a detected issue'))
    lines.append(txt_row('ITSM webhook = Outbound notification to ServiceNow, Jira, or PagerDuty'))
    lines.append(txt_row('Telemetry = Metrics, events, and logs forwarded from infrastructure to AIOps engine'))
    lines.append(txt_row('APEX = Dell as-a-Service platform; telemetry included in AIOps data ingestion'))
    lines.append(txt_row('VxRail = Dell hyperconverged infrastructure; AIOps monitors HCI cluster health'))
    lines.append(txt_row('Single pane = Unified UI showing health, alerts, and capacity across all Dell infrastructure'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-arch', 'docs/monitoring/dell-aiops/architecture/index.md', 'Dell AIOps architecture')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Architecture: microservices deployed as containers or VMs on-premises')))
    lines.append(R(bMid(L, RR, 'Collector tier: agents/adapters on each array/server push metrics to ingest service')))
    lines.append(R(bMid(L, RR, 'Processing tier: time-series DB + ML engine process streams in near-real-time')))
    lines.append(R(bMid(L, RR, 'Presentation tier: web UI, REST API, alert engine, and outbound notification bus')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Microservice architecture scales horizontally; each tier deployable independently'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Collector Tier'), bMid(B2_L, B2_R, 'Processing Tier'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Native API adapters'), bMid(B2_L, B2_R, 'Time-series database'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SNMP/REST polling'), bMid(B2_L, B2_R, 'ML model runtime'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CloudIQ bridge'), bMid(B2_L, B2_R, 'Event correlation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Push via HTTPS/443'), bMid(B2_L, B2_R, 'Alerting engine'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Configurable interval'), bMid(B2_L, B2_R, 'Outbound bus'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AIOps VMs: 8 vCPU/32 GB typical · SSD-backed storage for time-series DB · TCP 443 mesh'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Microservices = Independently deployable services each handling a specific function'))
    lines.append(txt_row('Collector = Agent or adapter that polls or receives metrics from infrastructure'))
    lines.append(txt_row('Ingest service = API endpoint receiving telemetry from collectors'))
    lines.append(txt_row('Time-series DB = Database optimised for sequential metric storage; InfluxDB or similar'))
    lines.append(txt_row('ML model runtime = Execution environment for trained anomaly and prediction models'))
    lines.append(txt_row('Event correlation = Grouping related events from different sources into a single alert'))
    lines.append(txt_row('Alerting engine = Rule evaluator triggering notifications when conditions are met'))
    lines.append(txt_row('Outbound bus = Message broker routing alerts to email, webhook, and API consumers'))
    lines.append(txt_row('CloudIQ bridge = Component forwarding CloudIQ telemetry into AIOps processing tier'))
    lines.append(txt_row('REST API = Programmatic access to AIOps data for custom dashboards and automation'))
    lines.append(txt_row('Horizontal scale = Adding collector or processing nodes to handle more data sources'))
    lines.append(txt_row('HTTPS/443 = All AIOps inter-component communication encrypted in transit'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-arch-how', 'docs/monitoring/dell-aiops/architecture/how-it-works/index.md', 'Dell AIOps how it works')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Step 1: Collection — adapters poll or receive telemetry from Dell infrastructure')))
    lines.append(R(bMid(L, RR, 'Step 2: Ingest — data normalised and stored in time-series database')))
    lines.append(R(bMid(L, RR, 'Step 3: ML Analysis — models run anomaly detection, forecasting, and correlation')))
    lines.append(R(bMid(L, RR, 'Step 4: Alert Generation — threshold or ML trigger creates alert with context')))
    lines.append(R(bMid(L, RR, 'Step 5: Notification — alert routed to console, email, webhook, or ITSM')))
    lines.append(R(bMid(L, RR, 'Step 6: Remediation — engineer acts on recommendation; alert closes on clear')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Data flow: infrastructure → collector → ingest API → time-series DB → ML → alert bus'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Adapter = Component connecting AIOps to a specific data source (PowerStore, PowerScale)'))
    lines.append(txt_row('Normalisation = Converting vendor-specific metrics to AIOps common schema'))
    lines.append(txt_row('Time-series = Metric stored with timestamp; enables trend and rate-of-change analysis'))
    lines.append(txt_row('Anomaly = Data point or pattern deviating from ML-learned baseline'))
    lines.append(txt_row('Forecasting = Regression model predicting future metric values (capacity exhaustion)'))
    lines.append(txt_row('Correlation = Linking related alerts from different sources into a single incident'))
    lines.append(txt_row('Threshold = Static or dynamic trigger value for alert generation'))
    lines.append(txt_row('Webhook = HTTP POST sent to external system when alert fires'))
    lines.append(txt_row('Recommendation = AI-generated action linked to alert for resolving root cause'))
    lines.append(txt_row('Alert close = Automatic resolution when triggering condition clears in subsequent poll'))
    lines.append(txt_row('Context = Alert enriched with related metrics, affected objects, and suggested fix'))
    lines.append(txt_row('Ingest API = REST endpoint receiving normalised metrics from collectors'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-arch-design', 'docs/monitoring/dell-aiops/architecture/design-standards/index.md', 'Dell AIOps design standards')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Deployment Standards'), bMid(B2_L, B2_R, 'Operational Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dedicated AIOps VMs'), bMid(B2_L, B2_R, 'All Dell infra covered'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSD for time-series DB'), bMid(B2_L, B2_R, 'Adapters per product'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HA pair minimum'), bMid(B2_L, B2_R, 'Consistent thresholds'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup nightly'), bMid(B2_L, B2_R, 'Alert to ITSM always'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS 1.2 end-to-end'), bMid(B2_L, B2_R, 'Review recommendations'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AIOps VMs on management cluster · SSD datastore · management VLAN only'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Dedicated VMs = AIOps runs on reserved VMs; not co-located with monitored workloads'))
    lines.append(txt_row('SSD datastore = Fast storage required for time-series DB write throughput'))
    lines.append(txt_row('HA pair = Two AIOps nodes for redundancy; active/passive or load-balanced'))
    lines.append(txt_row('Threshold consistency = Same alert trigger values across all environments; documented in runbook'))
    lines.append(txt_row('Adapter per product = Each Dell product type has a dedicated adapter configured'))
    lines.append(txt_row('ITSM always = Every fired alert routed to ServiceNow; no silent monitoring'))
    lines.append(txt_row('Recommendation review = Weekly process to act on or dismiss open AI recommendations'))
    lines.append(txt_row('Nightly backup = AIOps config and DB snapshot to NFS or object store'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-arch-int', 'docs/monitoring/dell-aiops/architecture/integrations/index.md', 'Dell AIOps integrations')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Infrastructure Inputs', 'Notification Outputs'])))
    lines.append(R(sections(L, RR, [50], ['PowerStore REST API', 'ServiceNow webhook'])))
    lines.append(R(sections(L, RR, [50], ['PowerScale PAPI', 'PagerDuty REST'])))
    lines.append(R(sections(L, RR, [50], ['PowerFlex REST API', 'Slack/Teams webhook'])))
    lines.append(R(sections(L, RR, [50], ['CloudIQ bridge feed', 'Email SMTP'])))
    lines.append(R(sections(L, RR, [50], ['VxRail REST / VCF API', 'Grafana data source'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AIOps polls infrastructure APIs · outbound notifications over TCP 443/25 to targets'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PAPI = PowerScale Platform API; REST interface for isilon/PowerScale management'))
    lines.append(txt_row('REST API = PowerStore/PowerFlex management API; AIOps polls every 5 minutes'))
    lines.append(txt_row('CloudIQ bridge = Component ingesting CloudIQ health data into AIOps for correlation'))
    lines.append(txt_row('VCF API = VMware Cloud Foundation API for vSphere and SDDC component metrics'))
    lines.append(txt_row('Webhook = HTTP POST from AIOps when alert fires; payload in JSON'))
    lines.append(txt_row('Grafana data source = AIOps REST API proxied as Grafana data source for custom panels'))
    lines.append(txt_row('SMTP = Email notification from AIOps SMTP client on alert'))
    lines.append(txt_row('PagerDuty = On-call routing platform receiving AIOps alerts via Events API v2'))
    lines.append(txt_row('Slack webhook = Incoming webhook URL for posting alert summaries to a Slack channel'))
    lines.append(txt_row('Poll interval = Frequency AIOps adapter queries infrastructure API; default 5 minutes'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-alerts', 'docs/monitoring/dell-aiops/alerts/index.md', 'Dell AIOps alerts')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Alerts'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Alert Types', 'Alert Lifecycle'])))
    lines.append(R(sections(L, RR, [50], ['Threshold: static metric limit', 'Open: condition met'])))
    lines.append(R(sections(L, RR, [50], ['Anomaly: ML baseline deviation', 'Acknowledged: engineer seen'])))
    lines.append(R(sections(L, RR, [50], ['Predictive: failure forecast', 'In Progress: being worked'])))
    lines.append(R(sections(L, RR, [50], ['Capacity: fill date near', 'Resolved: condition cleared'])))
    lines.append(R(sections(L, RR, [50], ['Hardware: component fault', 'Dismissed: false positive'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Alerts generated in AIOps engine · delivered via console, email, webhook, and ITSM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Threshold alert = Fires when metric exceeds static limit (e.g., utilisation > 85%)'))
    lines.append(txt_row('Anomaly alert = Fires when ML model detects unusual pattern outside learned baseline'))
    lines.append(txt_row('Predictive alert = Fires when model forecasts failure or capacity exhaustion within horizon'))
    lines.append(txt_row('Capacity alert = Fires when forecast horizon drops below threshold (e.g., 90 days)'))
    lines.append(txt_row('Hardware alert = Propagated from array firmware; component failure detected'))
    lines.append(txt_row('Acknowledge = Engineer marks alert as seen; stops re-notification'))
    lines.append(txt_row('In Progress = Status indicating active remediation in progress'))
    lines.append(txt_row('Resolved = Alert auto-closes when triggering condition no longer detected'))
    lines.append(txt_row('Dismissed = Alert closed as false-positive; reason required'))
    lines.append(txt_row('Severity = Critical / Warning / Informational; routes to different notification targets'))
    lines.append(txt_row('Alert context = Related metrics, affected objects, and recommendation attached to alert'))
    lines.append(txt_row('Noise reduction = Correlation grouping related alerts into single actionable incident'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-cli', 'docs/monitoring/dell-aiops/cli-reference/index.md', 'Dell AIOps CLI and API reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — CLI and API Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'AIOps REST API — Base URL: https://<aiops-host>/api/v1')))
    lines.append(R(bMid(L, RR, 'Auth: POST /api/v1/auth/login → Bearer token')))
    lines.append(R(bMid(L, RR, 'Alerts: GET /api/v1/alerts?status=open — list active alerts')))
    lines.append(R(bMid(L, RR, 'Systems: GET /api/v1/systems — list monitored infrastructure')))
    lines.append(R(bMid(L, RR, 'Metrics: GET /api/v1/metrics/{system_id}?metric=latency_ms&range=1h')))
    lines.append(R(bMid(L, RR, 'Recommendations: GET /api/v1/recommendations?priority=critical')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('REST API on AIOps master node TCP 443 · CLI scripts run from any mgmt host'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Bearer token = Short-lived auth credential from /auth/login; include in Authorization header'))
    lines.append(txt_row('status=open = Filter returning only unresolved alerts'))
    lines.append(txt_row('system_id = Unique identifier for a monitored infrastructure component in AIOps'))
    lines.append(txt_row('metric param = Name of the metric to retrieve (latency_ms, iops, throughput_mb)'))
    lines.append(txt_row('range param = Time window for metric data (1h, 24h, 7d)'))
    lines.append(txt_row('priority filter = Filter recommendations by Critical/High/Medium/Low'))
    lines.append(txt_row('Pagination = Use limit/offset params; default 100 records per page'))
    lines.append(txt_row('Webhook test = POST /api/v1/webhooks/{id}/test — verify webhook delivery'))
    lines.append(txt_row('Health check = GET /api/v1/health — confirm AIOps services are running'))
    lines.append(txt_row('Admin CLI = aiops-admin tool on host; used for backup, config, and service restart'))
    lines.append(txt_row('JSON response = All API responses in JSON format; parse with jq'))
    lines.append(txt_row('Rate limit = API enforces per-client limits; retry with exponential backoff on 429'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-design', 'docs/monitoring/dell-aiops/design-standards/index.md', 'Dell AIOps design standards top-level')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Platform Standards'), bMid(B2_L, B2_R, 'Alert & Notification'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'All Dell infra added'), bMid(B2_L, B2_R, 'ITSM for all alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSD time-series store'), bMid(B2_L, B2_R, 'Severity documented'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HA deployment'), bMid(B2_L, B2_R, 'No alert left > 24h'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup daily'), bMid(B2_L, B2_R, 'Weekly rec review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dedicated admin access'), bMid(B2_L, B2_R, 'Escalation defined'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AIOps on management cluster · SSD datastore · management network only'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('HA deployment = Active/passive or clustered AIOps for platform availability'))
    lines.append(txt_row('SSD time-series = Flash storage required for time-series DB write performance'))
    lines.append(txt_row('All infra added = Every Dell array/server registered in AIOps; no blind spots'))
    lines.append(txt_row('ITSM for all = ServiceNow incident created for every Critical/High AIOps alert'))
    lines.append(txt_row('Alert SLA = Policy requiring no open Critical alert older than 24 hours'))
    lines.append(txt_row('Weekly review = Dedicated calendar event to action AIOps recommendations'))
    lines.append(txt_row('Escalation = Runbook defining who to call when AIOps shows Critical storage/compute alert'))
    lines.append(txt_row('Dedicated admin = AIOps admin login separate from day-to-day operator access'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-insights', 'docs/monitoring/dell-aiops/insights/index.md', 'Dell AIOps insights')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Insights'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'AIOps Insights: AI-generated summaries of infrastructure health trends')))
    lines.append(R(bMid(L, RR, 'Categories: Efficiency, Risk, Capacity, Performance, Security')))
    lines.append(R(bMid(L, RR, 'Insight = aggregated pattern observed across multiple objects and time windows')))
    lines.append(R(bMid(L, RR, 'Includes estimated business impact and priority ranking')))
    lines.append(R(bMid(L, RR, 'Updated daily from ML analysis of all ingested telemetry')))
    lines.append(R(bMid(L, RR, 'Actionable: each insight links to recommendations and affected systems')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Insights computed in AIOps ML engine · stored in AIOps DB · displayed in UI and API'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Insight = Aggregated finding from ML analysis covering multiple systems or time windows'))
    lines.append(txt_row('Efficiency insight = Identifying over-provisioned or under-utilised resources'))
    lines.append(txt_row('Risk insight = Patterns suggesting increased failure probability across a group of systems'))
    lines.append(txt_row('Capacity insight = Fleet-wide capacity outlook; systems at risk within 90 days'))
    lines.append(txt_row('Performance insight = Workload patterns causing latency degradation across multiple arrays'))
    lines.append(txt_row('Security insight = Configuration gaps or unusual access patterns detected by ML'))
    lines.append(txt_row('Business impact = Estimated operational risk or cost of not acting on insight'))
    lines.append(txt_row('Priority ranking = Insights ordered by estimated impact and urgency'))
    lines.append(txt_row('Affected systems = List of infrastructure objects contributing to the insight'))
    lines.append(txt_row('Linked recommendations = Specific actions to address the identified pattern'))
    lines.append(txt_row('Daily refresh = Insight model runs nightly on new telemetry; UI updated each morning'))
    lines.append(txt_row('Pattern = Recurring behaviour observed across objects over time; basis for insight generation'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-integration', 'docs/monitoring/dell-aiops/integration/index.md', 'Dell AIOps integration guide')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Integration Guide'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ITSM Integration'), bMid(B2_L, B2_R, 'Observability Stack'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ServiceNow webhook'), bMid(B2_L, B2_R, 'Grafana data source'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Auto incident create'), bMid(B2_L, B2_R, 'Splunk HEC forward'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CMDB CI update'), bMid(B2_L, B2_R, 'Elastic integration'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PagerDuty routing'), bMid(B2_L, B2_R, 'Custom REST client'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Jira issue create'), bMid(B2_L, B2_R, 'Prometheus exporter'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AIOps on-prem · outbound TCP 443 to ITSM/SaaS targets · no inbound connections required'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ServiceNow webhook = AIOps POST to ServiceNow event endpoint on alert fire'))
    lines.append(txt_row('CMDB CI = Configuration Item in ServiceNow matched to AIOps monitored system'))
    lines.append(txt_row('Auto incident = ServiceNow incident created automatically from AIOps alert payload'))
    lines.append(txt_row('PagerDuty = On-call routing; AIOps sends Events API v2 payload for escalation'))
    lines.append(txt_row('Jira issue = AIOps creates Jira bug/task for recommendation tracking in dev teams'))
    lines.append(txt_row('Grafana data source = AIOps REST API configured as Grafana JSON data source'))
    lines.append(txt_row('Splunk HEC = HTTP Event Collector; AIOps forwards alerts as events for SIEM correlation'))
    lines.append(txt_row('Prometheus exporter = AIOps /metrics endpoint scraped by Prometheus'))
    lines.append(txt_row('Elastic integration = AIOps alert forwarded to Elasticsearch for log analytics'))
    lines.append(txt_row('REST client = Custom script polling AIOps API and pushing to proprietary system'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-lifecycle', 'docs/monitoring/dell-aiops/lifecycle/index.md', 'Dell AIOps lifecycle')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Lifecycle Management'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Deploy / Install'), bMid(B2_L, B2_R, 'Upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OVA or container'), bMid(B2_L, B2_R, 'Check release notes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Configure adapters'), bMid(B2_L, B2_R, 'Snapshot before'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Connect data sources'), bMid(B2_L, B2_R, 'Rolling upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Set alert policies'), bMid(B2_L, B2_R, 'Verify after'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Configure ITSM out'), bMid(B2_L, B2_R, 'Rollback if fail'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AIOps on management cluster VMs · upgrade via admin CLI or UI · snapshot enables rollback'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OVA deployment = VM image for vSphere; alternative container deployment for Kubernetes'))
    lines.append(txt_row('Adapter = Per-product data source connector configured after initial platform deployment'))
    lines.append(txt_row('Rolling upgrade = Upgrading nodes one at a time to maintain availability during upgrade'))
    lines.append(txt_row('Snapshot = VM snapshot taken before upgrade; enables fast rollback if upgrade fails'))
    lines.append(txt_row('Release notes = Per-version document; check for breaking changes before upgrade'))
    lines.append(txt_row('Verify after = Post-upgrade checks: adapters collecting, alerts firing, UI accessible'))
    lines.append(txt_row('Rollback = Revert to snapshot if upgrade causes data loss or service disruption'))
    lines.append(txt_row('Alert policy = Named ruleset defining thresholds and notification targets; survives upgrade'))
    lines.append(txt_row('Admin CLI = aiops-admin command-line tool for backup, upgrade, and service management'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-ops', 'docs/monitoring/dell-aiops/operations/index.md', 'Dell AIOps operations')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Operations'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Daily'), bMid(B2_L, B2_R, 'Weekly'), bMid(B3_L, B3_R, 'Monthly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review alert console'), bMid(B2_L, B2_R, 'Action recommendations'), bMid(B3_L, B3_R, 'Capacity review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check anomalies'), bMid(B2_L, B2_R, 'Review insights'), bMid(B3_L, B3_R, 'Threshold audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify adapters OK'), bMid(B2_L, B2_R, 'Update ITSM tickets'), bMid(B3_L, B3_R, 'Access review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Triage new alerts'), bMid(B2_L, B2_R, 'Check forecasts'), bMid(B3_L, B3_R, 'Report to mgmt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check platform health'), bMid(B2_L, B2_R, 'Dismiss false pos'), bMid(B3_L, B3_R, 'Procurement plan'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Operations via AIOps web UI and REST API · admin CLI for platform-level checks'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Alert console = AIOps UI showing all active alerts sorted by severity and age'))
    lines.append(txt_row('Adapter status = Health check confirming each data source adapter is collecting normally'))
    lines.append(txt_row('Platform health = AIOps self-monitoring; check /api/v1/health endpoint'))
    lines.append(txt_row('Triage = Classifying new alert: actionable, false positive, or informational'))
    lines.append(txt_row('Recommendation = AI action item; review weekly and track in ITSM'))
    lines.append(txt_row('Insight review = Weekly check of AI-generated fleet-wide patterns'))
    lines.append(txt_row('Forecast check = Reviewing capacity projections per system for procurement planning'))
    lines.append(txt_row('Threshold audit = Monthly validation that alert thresholds match current operational norms'))
    lines.append(txt_row('Access review = Monthly check of AIOps user list for stale or inappropriate access'))
    lines.append(txt_row('Procurement plan = Capacity expansion request based on AIOps forecast data'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-recommendations', 'docs/monitoring/dell-aiops/recommendations/index.md', 'Dell AIOps recommendations')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Recommendations'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'AIOps AI generates recommendations from anomalies, insights, and health scores')))
    lines.append(R(bMid(L, RR, 'Categories: Performance, Capacity, Availability, Security, Configuration')))
    lines.append(R(bMid(L, RR, 'Priority: Critical → High → Medium → Low based on estimated impact')))
    lines.append(R(bMid(L, RR, 'Each recommendation: problem, affected systems, steps, and expected outcome')))
    lines.append(R(bMid(L, RR, 'Status flow: Open → In Progress → Resolved / Dismissed')))
    lines.append(R(bMid(L, RR, 'Linked to ITSM: recommendation can trigger ServiceNow problem record')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Recommendations computed by AIOps ML engine · tracked in AIOps DB · exported via API'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Recommendation = AI-generated action linking a detected issue to a corrective step'))
    lines.append(txt_row('Priority = Urgency classification: Critical (act now)/High (act soon)/Medium/Low'))
    lines.append(txt_row('Affected systems = Infrastructure components contributing to the recommendation'))
    lines.append(txt_row('Expected outcome = Estimated improvement if recommendation is implemented'))
    lines.append(txt_row('In Progress = Status indicating team has started working on the recommendation'))
    lines.append(txt_row('Resolved = Recommendation closed; AIOps validates via subsequent telemetry'))
    lines.append(txt_row('Dismissed = Closed without action; requires reason comment for audit trail'))
    lines.append(txt_row('ServiceNow problem = ITSM record created from recommendation for tracking in change process'))
    lines.append(txt_row('SLA = Internal target for acting on Critical recs (e.g., within 2 business days)'))
    lines.append(txt_row('Configuration rec = Flagging settings that deviate from Dell best practice baseline'))
    lines.append(txt_row('Weekly review = Dedicated recurring meeting to action or defer open recommendations'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-reporting', 'docs/monitoring/dell-aiops/reporting/index.md', 'Dell AIOps reporting')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Reporting'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Built-in Reports'), bMid(B2_L, B2_R, 'Export / Custom'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fleet health summary'), bMid(B2_L, B2_R, 'CSV metric export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert history'), bMid(B2_L, B2_R, 'PDF report'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity forecast'), bMid(B2_L, B2_R, 'API data pull'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Recommendation status'), bMid(B2_L, B2_R, 'Scheduled email'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Performance trends'), bMid(B2_L, B2_R, 'Grafana panels'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Reports generated on AIOps master · CSV/PDF via browser · API for automation'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Fleet health report = Summary of all monitored systems with health score and issue count'))
    lines.append(txt_row('Alert history = Time-series of alert activity; useful for trend and MTTR analysis'))
    lines.append(txt_row('Capacity forecast report = Per-system projected fill dates for procurement planning'))
    lines.append(txt_row('Performance trend = Historical IOPS/latency/throughput per system over custom window'))
    lines.append(txt_row('Recommendation status = Open/resolved/dismissed counts by category and priority'))
    lines.append(txt_row('CSV export = Raw metric data download for spreadsheet or BI tool consumption'))
    lines.append(txt_row('PDF report = Formatted document suitable for management or audit review'))
    lines.append(txt_row('Scheduled email = AIOps sending report on configured cadence to recipient list'))
    lines.append(txt_row('API data pull = REST GET to retrieve report data for custom downstream tooling'))
    lines.append(txt_row('Grafana panels = AIOps metrics exposed via REST and visualised in Grafana dashboards'))
    lines.append(txt_row('MTTR = Mean Time To Resolve; calculated from alert history open/close timestamps'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-scripts', 'docs/monitoring/dell-aiops/scripts/index.md', 'Dell AIOps scripts reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Scripts Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'AIOps REST API scripts — Python examples')))
    lines.append(R(bMid(L, RR, 'get-token.py: POST /api/v1/auth/login → Bearer token for session')))
    lines.append(R(bMid(L, RR, 'get-alerts.py: GET /api/v1/alerts?status=open → CSV with severity/system')))
    lines.append(R(bMid(L, RR, 'capacity-check.py: GET /api/v1/capacity → flag systems < 90 days to full')))
    lines.append(R(bMid(L, RR, 'recommendations.py: GET /api/v1/recommendations → post Critical to Slack')))
    lines.append(R(bMid(L, RR, 'adapter-health.py: GET /api/v1/adapters → verify all collecting status')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Scripts run from management host · Python 3.8+ with requests · AIOps TCP 443'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Bearer token = Short-lived credential from /auth/login; pass in Authorization header'))
    lines.append(txt_row('status=open = Filter for unresolved alerts only'))
    lines.append(txt_row('capacity endpoint = Returns per-system current and forecast capacity data'))
    lines.append(txt_row('recommendations endpoint = Returns prioritised AI action items'))
    lines.append(txt_row('adapters endpoint = Returns health status for each configured data source adapter'))
    lines.append(txt_row('Slack webhook = Incoming webhook URL for posting summaries to a Slack channel'))
    lines.append(txt_row('Cron schedule = Automated execution (e.g., daily at 06:00 for capacity check)'))
    lines.append(txt_row('Environment vars = Store AIOps URL, username, password in env; never hardcode'))
    lines.append(txt_row('Exponential backoff = Retry logic for 429/503 responses from AIOps API'))
    lines.append(txt_row('CSV output = Writing alert/capacity data to CSV for spreadsheet import'))
    lines.append(txt_row('Collecting status = Adapter state confirming data being received; opposite of No Data'))
    lines.append(txt_row('Requests library = pip install requests; standard Python HTTP client'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-security', 'docs/monitoring/dell-aiops/security/index.md', 'Dell AIOps security')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Security'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access Control'), bMid(B2_L, B2_R, 'Network & Data Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local admin + LDAP'), bMid(B2_L, B2_R, 'TLS 1.2 all comms'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC: role per team'), bMid(B2_L, B2_R, 'Mgmt VLAN only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service accounts'), bMid(B2_L, B2_R, 'Custom cert replace'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA on admin UI'), bMid(B2_L, B2_R, 'Audit log retained'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Annual access review'), bMid(B2_L, B2_R, 'Syslog to SIEM'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AIOps VMs on management cluster · data encrypted at rest · outbound only TCP 443'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC = Role-Based Access Control; Admin/Operator/Viewer roles with different permissions'))
    lines.append(txt_row('Service account = Non-personal credential for adapter authentication to infrastructure'))
    lines.append(txt_row('MFA = Multi-factor authentication on AIOps admin UI; reduces credential theft risk'))
    lines.append(txt_row('Custom cert = CA-signed certificate replacing self-signed; applied to AIOps HTTPS'))
    lines.append(txt_row('Audit log = Record of logins, config changes, and alert actions in AIOps'))
    lines.append(txt_row('Syslog = Forwarding AIOps audit events to SIEM (Splunk, Elastic) for correlation'))
    lines.append(txt_row('Mgmt VLAN = AIOps on isolated management network; no direct access from user VLANs'))
    lines.append(txt_row('Data at rest = AIOps time-series DB and config encrypted on disk'))
    lines.append(txt_row('Annual review = Yearly audit of AIOps user list; remove departed staff accounts'))
    lines.append(txt_row('Credential rotation = Changing adapter service account passwords per security policy'))
    lines.append(txt_row('TLS 1.2 = Minimum transport encryption for all AIOps connections'))
    lines.append(txt_row('Least privilege = Adapter accounts have read-only access to infrastructure APIs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-troubleshooting', 'docs/monitoring/dell-aiops/troubleshooting/index.md', 'Dell AIOps troubleshooting')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Adapter Not Collecting'), bMid(B2_L, B2_R, 'Platform Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check credential'), bMid(B2_L, B2_R, 'Check /api/v1/health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify network reach'), bMid(B2_L, B2_R, 'Restart services'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review adapter log'), bMid(B2_L, B2_R, 'Check disk space'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Re-save adapter'), bMid(B2_L, B2_R, 'Time-series DB check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check firewall'), bMid(B2_L, B2_R, 'Collect support bundle'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Logs: /var/log/aiops/ on each node · support bundle via aiops-admin support collect'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Adapter log = Per-adapter log in /var/log/aiops/adapters/; shows collection errors'))
    lines.append(txt_row('Health endpoint = GET /api/v1/health returns status of all AIOps services'))
    lines.append(txt_row('Re-save adapter = Resaving adapter config resets its state; often fixes transient errors'))
    lines.append(txt_row('Disk space = Time-series DB fills disk over time; monitor and archive/purge old data'))
    lines.append(txt_row('Time-series DB = Check DB health with aiops-admin db status'))
    lines.append(txt_row('Support bundle = aiops-admin support collect creates compressed log archive'))
    lines.append(txt_row('Service restart = aiops-admin service restart <name> to recover failed service'))
    lines.append(txt_row('Firewall = Check management host can reach infrastructure API ports (443, 8080)'))
    lines.append(txt_row('Credential = Wrong or expired password causes No Data state; update in adapter settings'))
    lines.append(txt_row('Network reach = Test from AIOps host: curl -k https://<array>:443/api/types'))
    lines.append(txt_row('Log level = Increase to DEBUG in adapter settings for detailed collection tracing'))
    lines.append(txt_row('Dell support = Open case at support.dell.com; attach support bundle'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-dell-aiops-vendor', 'docs/monitoring/dell-aiops/vendor-support/index.md', 'Dell AIOps vendor support')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Dell AIOps — Vendor Support'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Support Model — Dell Technologies GSS')))
    lines.append(R(bMid(L, RR, 'AIOps included with ProSupport Plus on eligible Dell infrastructure')))
    lines.append(R(bMid(L, RR, 'Open case: support.dell.com — provide AIOps version + support bundle')))
    lines.append(R(bMid(L, RR, 'Sev-1: production monitoring platform down; 24x7 phone response')))
    lines.append(R(bMid(L, RR, 'Sev-2: major functionality impaired; business-hours response')))
    lines.append(R(bMid(L, RR, 'Feature requests: submit via AIOps UI > Feedback or Dell Idea portal')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AIOps on-prem · support bundle collected locally · uploaded to Dell case portal'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ProSupport Plus = Dell premium support tier; includes AIOps and proactive support features'))
    lines.append(txt_row('GSS = Global Support Services; Dell technical support organisation'))
    lines.append(txt_row('Support bundle = aiops-admin support collect output; required for most support cases'))
    lines.append(txt_row('AIOps version = Check in UI or via aiops-admin version; required for case opening'))
    lines.append(txt_row('Severity 1 = Production monitoring platform unavailable; 24x7 phone escalation'))
    lines.append(txt_row('Severity 2 = Major feature impaired (no collection, no alerts); business-hours response'))
    lines.append(txt_row('Idea portal = Dell customer feedback portal for AIOps feature requests'))
    lines.append(txt_row('Release notes = Per-version changelog; check before upgrade and when diagnosing issues'))
    lines.append(txt_row('KB = Dell Knowledge Base at kb.dell.com; search by product and symptom'))
    lines.append(txt_row('TAM = Technical Account Manager; proactive guidance for licensed customers'))
    lines.append(txt_row('Escalation = Requesting Sev-1 or senior engineer when case priority increases'))
    lines.append(txt_row('Community forum = Dell Technology Forum online community for AIOps peer support'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── InsightIQ diagrams ────────────────────────────────────────────────────────

@kb_diagram('monitoring-insightiq', 'docs/monitoring/insightiq/index.md', 'InsightIQ — PowerScale performance reporting')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — PowerScale Performance Reporting'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'InsightIQ: on-premises performance analytics appliance for Dell EMC PowerScale (Isilon)')))
    lines.append(R(bMid(L, RR, 'Collects detailed performance data: IOPS, latency, throughput, protocol, and client stats')))
    lines.append(R(bMid(L, RR, 'Stores multi-year historical data for trend analysis, capacity planning, and chargebacks')))
    lines.append(R(bMid(L, RR, 'Deployed as VM (OVA) on vSphere; connects to PowerScale cluster via PAPI')))
    lines.append(R(bMid(L, RR, 'Web UI with built-in dashboards and custom report builder; no agent on cluster')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  InsightIQ provides the long-term performance history that PowerScale built-in tools lack'))
    lines.append(txt_row())
    lines.append(R(arrow([16, 50, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Performance'), bMid(B2_L, B2_R, 'Capacity'), bMid(B3_L, B3_R, 'Workloads'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'IOPS per node'), bMid(B2_L, B2_R, 'Space trends'), bMid(B3_L, B3_R, 'Per-client IO'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Latency per proto'), bMid(B2_L, B2_R, 'Growth forecast'), bMid(B3_L, B3_R, 'Per-share stats'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Throughput MB/s'), bMid(B2_L, B2_R, 'Quota tracking'), bMid(B3_L, B3_R, 'Top talkers'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CPU / disk util'), bMid(B2_L, B2_R, 'Tier breakdown'), bMid(B3_L, B3_R, 'Protocol mix'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cache hit rate'), bMid(B2_L, B2_R, 'Dedup/compress'), bMid(B3_L, B3_R, 'Chargeback data'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('InsightIQ VM: 4 vCPU/8 GB · local datastore for metrics DB · PAPI TCP 8080 to cluster'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('InsightIQ = Dell EMC performance analytics appliance for PowerScale clusters'))
    lines.append(txt_row('PAPI = PowerScale Platform API; REST interface used by InsightIQ to collect data'))
    lines.append(txt_row('OVA = Open Virtual Appliance; VM image for InsightIQ deployment on vSphere'))
    lines.append(txt_row('IOPS = Input/Output Operations per Second; primary performance metric'))
    lines.append(txt_row('Latency = Time from client request to response; measured per protocol (NFS, SMB, S3)'))
    lines.append(txt_row('Throughput = Data transfer rate in MB/s; saturates network before IOPS typically'))
    lines.append(txt_row('Top talkers = Clients or directories with highest IO activity'))
    lines.append(txt_row('Protocol mix = Breakdown of IO by access protocol (NFS v3, NFS v4, SMB, S3, HDFS)'))
    lines.append(txt_row('Chargeback = Attributing storage consumption and IO cost to departments or projects'))
    lines.append(txt_row('Cache hit rate = Percentage of reads served from L1/L2 cache; high rate reduces latency'))
    lines.append(txt_row('Quota tracking = Monitoring directory and user quota consumption over time'))
    lines.append(txt_row('Dedup/compress = Data reduction ratio metrics tracked for capacity planning'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-arch', 'docs/monitoring/insightiq/architecture/index.md', 'InsightIQ architecture')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Architecture: single VM appliance; internal PostgreSQL stores collected metrics')))
    lines.append(R(bMid(L, RR, 'Collector: polls PowerScale PAPI every 30 seconds for performance counters')))
    lines.append(R(bMid(L, RR, 'UI: embedded web server on port 443 serves dashboards and report builder')))
    lines.append(R(bMid(L, RR, 'Data retention: configurable; default 2 years; older data rolled up or purged')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Single appliance polls PAPI; no agent on PowerScale nodes; storage grows ~10 GB/year/cluster'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Collection'), bMid(B2_L, B2_R, 'Storage'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PAPI TCP 8080'), bMid(B2_L, B2_R, 'PostgreSQL on VM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '30-sec interval'), bMid(B2_L, B2_R, '~10 GB/yr/cluster'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Protocol counters'), bMid(B2_L, B2_R, 'Rollup for old data'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Node-level stats'), bMid(B2_L, B2_R, 'Configurable retention'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Client/share stats'), bMid(B2_L, B2_R, 'Backup recommended'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('InsightIQ VM: 4 vCPU/8 GB/200 GB disk · PowerScale: PAPI user needed on cluster'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PAPI = PowerScale Platform API on TCP 8080; InsightIQ polls this for all counters'))
    lines.append(txt_row('PAPI user = Read-only cluster admin account created on PowerScale for InsightIQ'))
    lines.append(txt_row('PostgreSQL = Embedded relational DB storing time-series metrics on InsightIQ VM'))
    lines.append(txt_row('30-second interval = Default collection cadence; lower for higher resolution (more disk)'))
    lines.append(txt_row('Rollup = Aggregating 30-sec samples into 5-min then 1-hour averages for old data'))
    lines.append(txt_row('Retention = Configurable data retention period; default 2 years raw + 5 years rolled'))
    lines.append(txt_row('Protocol counters = NFS v3/v4, SMB, S3, HDFS IO stats per protocol per node'))
    lines.append(txt_row('Client stats = Per-client-IP IO breakdown; requires clientstats enabled on cluster'))
    lines.append(txt_row('Share stats = Per-NFS export or SMB share IO statistics'))
    lines.append(txt_row('Embedded web = InsightIQ UI served from nginx on TCP 443 on the appliance VM'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-arch-how', 'docs/monitoring/insightiq/architecture/how-it-works/index.md', 'InsightIQ how it works')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Step 1: Cluster Registration — add PowerScale cluster IP and PAPI credentials to InsightIQ')))
    lines.append(R(bMid(L, RR, 'Step 2: Collection — InsightIQ polls PAPI every 30 seconds for all performance counters')))
    lines.append(R(bMid(L, RR, 'Step 3: Storage — raw samples stored in PostgreSQL; older data rolled up to 5-min averages')))
    lines.append(R(bMid(L, RR, 'Step 4: Analysis — UI queries DB to render dashboards and charts on demand')))
    lines.append(R(bMid(L, RR, 'Step 5: Reporting — user builds or schedules reports; PDF/CSV export available')))
    lines.append(R(bMid(L, RR, 'Step 6: Alert — threshold breach triggers email notification to configured recipients')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('InsightIQ VM on management cluster · PAPI from VM to cluster SmartConnect IP'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cluster registration = Adding cluster access zone IP and PAPI user to InsightIQ'))
    lines.append(txt_row('SmartConnect = PowerScale DNS load-balancing for PAPI connections across nodes'))
    lines.append(txt_row('PAPI credentials = Read-only admin user on PowerScale; InsightIQ uses for all polls'))
    lines.append(txt_row('Raw sample = 30-second metric reading stored at full resolution'))
    lines.append(txt_row('Rollup = Aggregation process compressing old raw samples into hourly averages'))
    lines.append(txt_row('Dashboard = Pre-built or custom view of metrics over selected time range'))
    lines.append(txt_row('Report = Scheduled or on-demand document with metric tables and charts'))
    lines.append(txt_row('Threshold alert = Email sent when metric exceeds configured limit'))
    lines.append(txt_row('SmartConnect zone = PowerScale DNS name resolving to available node IPs'))
    lines.append(txt_row('PostgreSQL = On-appliance DB; grows at ~10 GB/year per cluster at 30-sec interval'))
    lines.append(txt_row('PDF export = Formatted report for management sharing'))
    lines.append(txt_row('CSV export = Raw data download for spreadsheet or BI analysis'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-arch-design', 'docs/monitoring/insightiq/architecture/design-standards/index.md', 'InsightIQ design standards')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Deployment Standards'), bMid(B2_L, B2_R, 'Collection Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dedicated VM per site'), bMid(B2_L, B2_R, '30-sec interval default'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '200 GB disk minimum'), bMid(B2_L, B2_R, 'All clusters added'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSD-backed datastore'), bMid(B2_L, B2_R, 'Client stats enabled'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup config nightly'), bMid(B2_L, B2_R, 'PAPI read-only user'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2-year retention min'), bMid(B2_L, B2_R, 'TLS for PAPI'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('InsightIQ VM on management cluster · SSD datastore · TCP 8080/443 to PowerScale'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Dedicated VM = InsightIQ on separate VM from monitored workloads'))
    lines.append(txt_row('SSD datastore = Flash storage for PostgreSQL write performance at 30-sec intervals'))
    lines.append(txt_row('Client stats = isi_clientstats enabled on PowerScale; required for per-client breakdown'))
    lines.append(txt_row('PAPI read-only = Minimum-privilege user; cannot modify cluster configuration'))
    lines.append(txt_row('TLS for PAPI = HTTPS connection to PAPI; verify certificate or accept self-signed'))
    lines.append(txt_row('2-year retention = Minimum raw data retention for trend analysis and compliance'))
    lines.append(txt_row('Backup config = InsightIQ appliance backup includes config and DB; NFS or SCP target'))
    lines.append(txt_row('200 GB minimum = Disk allocation for ~5 clusters at 30-sec interval over 2 years'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-arch-int', 'docs/monitoring/insightiq/architecture/integrations/index.md', 'InsightIQ integrations')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Inputs', 'Outputs'])))
    lines.append(R(sections(L, RR, [50], ['PowerScale PAPI (primary)', 'Web UI dashboards'])))
    lines.append(R(sections(L, RR, [50], ['Multiple clusters per IIQ', 'PDF/CSV report export'])))
    lines.append(R(sections(L, RR, [50], ['PAPI TCP 8080 or 8083', 'Email alert notifications'])))
    lines.append(R(sections(L, RR, [50], ['SmartConnect for DNS LB', 'API for custom tooling'])))
    lines.append(R(sections(L, RR, [50], ['Cluster admin read-only', 'Grafana via REST proxy'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('InsightIQ VM → PAPI TCP 8080 → PowerScale nodes · UI on TCP 443 from browser'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PAPI = PowerScale Platform API; primary data source for InsightIQ'))
    lines.append(txt_row('TCP 8080 = Default PAPI port; 8083 used for TLS PAPI'))
    lines.append(txt_row('SmartConnect = PowerScale DNS name for PAPI; InsightIQ connects via SmartConnect zone'))
    lines.append(txt_row('Multiple clusters = Single InsightIQ VM can monitor multiple PowerScale clusters'))
    lines.append(txt_row('Email alert = SMTP notification when threshold exceeded; recipient list in InsightIQ settings'))
    lines.append(txt_row('REST API = InsightIQ exposes limited API for programmatic data retrieval'))
    lines.append(txt_row('Grafana = Custom metrics panels built by exposing InsightIQ data via REST proxy'))
    lines.append(txt_row('CSV export = Downloading metric data for external BI or spreadsheet analysis'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-capacity', 'docs/monitoring/insightiq/capacity/index.md', 'InsightIQ capacity management')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Capacity Management'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity Metrics'), bMid(B2_L, B2_R, 'Forecasting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Total usable space'), bMid(B2_L, B2_R, 'Growth rate trend'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Used vs available'), bMid(B2_L, B2_R, 'Projected full date'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Per-tier breakdown'), bMid(B2_L, B2_R, 'Linear regression'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dedup/compress ratio'), bMid(B2_L, B2_R, 'Custom horizon'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Quota utilisation'), bMid(B2_L, B2_R, 'Export for planning'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Capacity data from PAPI · trend analysis in InsightIQ · export for spreadsheet planning'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Usable space = Total cluster capacity after RAID overhead'))
    lines.append(txt_row('Tier = Storage class within PowerScale (SSD, SAS, HDD) each with separate capacity'))
    lines.append(txt_row('Dedup ratio = Data deduplication factor; 2.0 means half the physical space used'))
    lines.append(txt_row('Compression ratio = Data compression factor; reduces physical footprint of data'))
    lines.append(txt_row('Quota = Per-directory or per-user space limit; tracked in InsightIQ for trend'))
    lines.append(txt_row('Growth rate = MB/day or GB/week consumption rate; derived from time-series'))
    lines.append(txt_row('Linear regression = Statistical method for projecting capacity exhaustion date'))
    lines.append(txt_row('Projected full date = Estimated date cluster reaches capacity at current growth rate'))
    lines.append(txt_row('Custom horizon = User-defined forecast window (30/60/90/180 days)'))
    lines.append(txt_row('CSV export = Downloading capacity data for external planning tools'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-cli', 'docs/monitoring/insightiq/cli-reference/index.md', 'InsightIQ CLI reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'InsightIQ Admin CLI — accessed via SSH or console on appliance VM')))
    lines.append(R(bMid(L, RR, 'iiq_backup — create backup of InsightIQ config and database')))
    lines.append(R(bMid(L, RR, 'iiq_restore — restore from backup archive')))
    lines.append(R(bMid(L, RR, 'iiq_start / iiq_stop / iiq_status — manage InsightIQ services')))
    lines.append(R(bMid(L, RR, 'iiq_add_cluster — register a new PowerScale cluster from CLI')))
    lines.append(R(bMid(L, RR, 'iiq_config — view or modify appliance configuration settings')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('SSH to InsightIQ VM management IP · local console via vSphere · root or iiq user'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('iiq_backup = Creates compressed archive of InsightIQ DB and config files'))
    lines.append(txt_row('iiq_restore = Restores from backup; use after re-deploy or data corruption'))
    lines.append(txt_row('iiq_status = Shows running/stopped state of InsightIQ data collection service'))
    lines.append(txt_row('iiq_add_cluster = CLI alternative to UI for adding a new PowerScale cluster'))
    lines.append(txt_row('iiq_config = View and modify InsightIQ settings (SMTP, retention, data path)'))
    lines.append(txt_row('SSH access = Required for admin CLI; restrict to management network'))
    lines.append(txt_row('Root login = Appliance root user; use only for admin CLI operations'))
    lines.append(txt_row('Web UI = Primary interface for dashboards and reports at https://<iiq-ip>'))
    lines.append(txt_row('Service restart = iiq_stop followed by iiq_start to recover stalled collection'))
    lines.append(txt_row('Log files = /var/log/isilon/insightiq/ for collection and service logs'))
    lines.append(txt_row('Config file = /etc/insightiq/config.conf; modified by iiq_config or manually'))
    lines.append(txt_row('Backup target = NFS mount or local directory configured in iiq_config'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-design', 'docs/monitoring/insightiq/design-standards/index.md', 'InsightIQ design standards top-level')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Platform Design'), bMid(B2_L, B2_R, 'Data Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'One VM per site'), bMid(B2_L, B2_R, '2-year min retention'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '200+ GB SSD disk'), bMid(B2_L, B2_R, 'Client stats ON'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'All clusters added'), bMid(B2_L, B2_R, '30-sec collection'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PAPI read-only acct'), bMid(B2_L, B2_R, 'Backup nightly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Management VLAN'), bMid(B2_L, B2_R, 'Report scheduled weekly'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('InsightIQ VM on management cluster · SSD VMDK · PAPI TCP 8080 to cluster'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('One VM per site = Each data centre site has a dedicated InsightIQ appliance'))
    lines.append(txt_row('200+ GB SSD = Disk allocation; SSD required for PostgreSQL write performance'))
    lines.append(txt_row('Client stats = isi_clientstats must be enabled on cluster for per-client breakdown'))
    lines.append(txt_row('Read-only PAPI account = InsightIQ cannot modify cluster; dedicated account per cluster'))
    lines.append(txt_row('2-year retention = Minimum to support trend analysis and capacity planning'))
    lines.append(txt_row('Nightly backup = iiq_backup scheduled; archive to NFS before 07:00'))
    lines.append(txt_row('Weekly report = Scheduled performance report emailed to storage team every Monday'))
    lines.append(txt_row('Management VLAN = InsightIQ isolated to management network; no access from users'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-integration', 'docs/monitoring/insightiq/integration/index.md', 'InsightIQ integration guide')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Integration Guide'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Email Notifications'), bMid(B2_L, B2_R, 'External Tools'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SMTP configuration'), bMid(B2_L, B2_R, 'REST API (limited)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Threshold alerts'), bMid(B2_L, B2_R, 'CSV for BI tools'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Report delivery'), bMid(B2_L, B2_R, 'Grafana REST proxy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Recipient list'), bMid(B2_L, B2_R, 'Scheduled reports'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert cadence cfg'), bMid(B2_L, B2_R, 'PDF to management'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('InsightIQ VM → SMTP relay → email · PDF/CSV download from UI · REST on TCP 443'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SMTP = Email relay configured in InsightIQ for threshold alerts and report delivery'))
    lines.append(txt_row('Threshold alert = Email when a metric (latency, utilisation) exceeds defined limit'))
    lines.append(txt_row('Report delivery = Scheduled InsightIQ report emailed as PDF to recipient list'))
    lines.append(txt_row('REST API = InsightIQ exposes limited REST for programmatic data retrieval'))
    lines.append(txt_row('CSV for BI = Metric data exported as CSV for Power BI, Tableau, or Excel'))
    lines.append(txt_row('Grafana proxy = REST proxy exposing InsightIQ metrics as Grafana data source'))
    lines.append(txt_row('Scheduled report = Weekly/monthly report generated and emailed automatically'))
    lines.append(txt_row('PDF to management = Formatted performance report for storage operations review'))
    lines.append(txt_row('Recipient list = Email addresses configured in InsightIQ notification settings'))
    lines.append(txt_row('Alert cadence = How often InsightIQ re-sends alert if threshold remains exceeded'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-lifecycle', 'docs/monitoring/insightiq/lifecycle/index.md', 'InsightIQ lifecycle management')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Lifecycle Management'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Deploy'), bMid(B2_L, B2_R, 'Upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Deploy OVA to vCenter'), bMid(B2_L, B2_R, 'Backup first'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Assign IP and DNS'), bMid(B2_L, B2_R, 'Snapshot VM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Add clusters via UI'), bMid(B2_L, B2_R, 'Apply upgrade pkg'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Configure SMTP'), bMid(B2_L, B2_R, 'Verify collection'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Set retention policy'), bMid(B2_L, B2_R, 'Rollback if fail'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('OVA on vSphere management cluster · VM snapshot before upgrade · backup to NFS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OVA deployment = Importing InsightIQ as VM; set 4 vCPU, 8 GB RAM, 200+ GB disk'))
    lines.append(txt_row('Cluster registration = Adding PowerScale cluster in InsightIQ UI with PAPI credentials'))
    lines.append(txt_row('Retention policy = Configured in InsightIQ settings; default 2 years raw data'))
    lines.append(txt_row('SMTP configuration = InsightIQ settings for email alerts and scheduled reports'))
    lines.append(txt_row('Upgrade package = Dell-provided upgrade file; applied via iiq_upgrade command'))
    lines.append(txt_row('Snapshot = VM snapshot taken before upgrade; enables rollback if data is lost'))
    lines.append(txt_row('Backup = iiq_backup run before upgrade; stored off-VM on NFS'))
    lines.append(txt_row('Verify collection = Check InsightIQ is collecting new data after upgrade'))
    lines.append(txt_row('Rollback = Revert to VM snapshot if upgrade corrupts DB or stops collection'))
    lines.append(txt_row('Decommission = iiq_backup → save archive → power off VM → remove from vCenter'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-ops', 'docs/monitoring/insightiq/operations/index.md', 'InsightIQ operations')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Operations'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Daily Checks'), bMid(B2_L, B2_R, 'Weekly Tasks'), bMid(B3_L, B3_R, 'Monthly Tasks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify collection'), bMid(B2_L, B2_R, 'Review reports'), bMid(B3_L, B3_R, 'Capacity planning'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check disk usage'), bMid(B2_L, B2_R, 'Check alerts'), bMid(B3_L, B3_R, 'Retention review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify backup ran'), bMid(B2_L, B2_R, 'Top talker review'), bMid(B3_L, B3_R, 'Trend analysis'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm clusters up'), bMid(B2_L, B2_R, 'Latency review'), bMid(B3_L, B3_R, 'Report to mgmt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check service status'), bMid(B2_L, B2_R, 'Capacity outlook'), bMid(B3_L, B3_R, 'Access review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Daily ops via InsightIQ web UI · admin CLI for service checks · NFS backup verification'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Collection verify = Confirm InsightIQ shows Connected and recent data for each cluster'))
    lines.append(txt_row('Disk usage = Monitor InsightIQ VM datastore; alert at 80% to expand before full'))
    lines.append(txt_row('Backup verification = Confirm nightly iiq_backup completed and archive exists on NFS'))
    lines.append(txt_row('Service status = iiq_status on appliance confirms data collection daemon running'))
    lines.append(txt_row('Top talker review = Weekly check of clients generating most IO; spot unexpected growth'))
    lines.append(txt_row('Latency review = Review average and p95 latency trends; flag increases to storage team'))
    lines.append(txt_row('Capacity outlook = Review InsightIQ capacity report for projected full dates'))
    lines.append(txt_row('Retention review = Monthly check that old data purging correctly per retention policy'))
    lines.append(txt_row('Trend analysis = Monthly review of 30/90-day performance trends for capacity planning'))
    lines.append(txt_row('Access review = Monthly check of InsightIQ user list; remove stale accounts'))
    lines.append(txt_row('Management report = Monthly PDF summary of performance trends for leadership review'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-performance', 'docs/monitoring/insightiq/performance/index.md', 'InsightIQ performance analysis')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Performance Analysis'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'IOPS Analysis'), bMid(B2_L, B2_R, 'Latency Analysis'), bMid(B3_L, B3_R, 'Throughput'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Per-node IOPS'), bMid(B2_L, B2_R, 'Per-protocol lat'), bMid(B3_L, B3_R, 'MB/s per node'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Per-protocol IOPS'), bMid(B2_L, B2_R, 'p50/p95/p99'), bMid(B3_L, B3_R, 'Network vs disk'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Read vs write'), bMid(B2_L, B2_R, 'Backend vs front'), bMid(B3_L, B3_R, 'Peak vs avg'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Peak vs average'), bMid(B2_L, B2_R, 'Trend baseline'), bMid(B3_L, B3_R, 'Saturation point'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Client breakdown'), bMid(B2_L, B2_R, 'Cache impact'), bMid(B3_L, B3_R, 'Protocol mix'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Metrics from PowerScale nodes · InsightIQ aggregates to cluster and node level'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('p50 latency = Median latency; 50% of operations complete faster than this value'))
    lines.append(txt_row('p95 latency = 95th percentile latency; 5% of operations are slower; good SLA metric'))
    lines.append(txt_row('p99 latency = 99th percentile; shows tail latency impacting worst-case user experience'))
    lines.append(txt_row('Frontend latency = Client-to-cluster latency including network and protocol overhead'))
    lines.append(txt_row('Backend latency = Cluster-to-disk latency; excludes network; shows storage device health'))
    lines.append(txt_row('Cache impact = Reduction in backend IOPS due to read cache (L1 RAM, L2 SSD hits)'))
    lines.append(txt_row('Saturation point = Throughput level at which latency begins degrading non-linearly'))
    lines.append(txt_row('Protocol mix = Ratio of NFS/SMB/S3/HDFS IO; different protocols have different overheads'))
    lines.append(txt_row('Trend baseline = Historical average used to identify current deviations'))
    lines.append(txt_row('Network vs disk = Comparing frontend and backend throughput to find bottleneck tier'))
    lines.append(txt_row('Read vs write = IO breakdown critical for cache effectiveness and drive wear planning'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-reports', 'docs/monitoring/insightiq/reports/index.md', 'InsightIQ reports')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Reports'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Built-in Reports'), bMid(B2_L, B2_R, 'Scheduling & Export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Performance summary'), bMid(B2_L, B2_R, 'Daily/weekly/monthly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity trend'), bMid(B2_L, B2_R, 'Email delivery'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Top clients/shares'), bMid(B2_L, B2_R, 'PDF format'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Protocol breakdown'), bMid(B2_L, B2_R, 'CSV format'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Latency distribution'), bMid(B2_L, B2_R, 'Custom time range'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Reports built in InsightIQ · PDF/CSV download · scheduled email via SMTP'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Performance summary = Cluster IOPS, latency, throughput over selected time window'))
    lines.append(txt_row('Capacity trend = Space usage over time with growth rate and projected full date'))
    lines.append(txt_row('Top clients = Ranked list of clients by IO volume; useful for chargeback'))
    lines.append(txt_row('Top shares = Ranked NFS/SMB shares by IO; identify active workloads'))
    lines.append(txt_row('Protocol breakdown = IO split by NFS v3, NFS v4, SMB, S3, HDFS'))
    lines.append(txt_row('Latency distribution = Histogram of operation latencies; shows p50/p95/p99'))
    lines.append(txt_row('Scheduled email = InsightIQ sending report to recipient list on configured cadence'))
    lines.append(txt_row('Custom time range = User-defined start and end dates for report data window'))
    lines.append(txt_row('Chargeback = Using top-client IO data to attribute storage cost to teams'))
    lines.append(txt_row('PDF = Formatted document; suitable for management review or compliance audit'))
    lines.append(txt_row('CSV = Raw metric data for import into BI tools or spreadsheets'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-scripts', 'docs/monitoring/insightiq/scripts/index.md', 'InsightIQ scripts reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Scripts Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'InsightIQ admin scripts — run on appliance or via management host')))
    lines.append(R(bMid(L, RR, 'iiq_backup.sh — wrapper triggering iiq_backup with dated archive name')))
    lines.append(R(bMid(L, RR, 'disk-check.sh — alerts if InsightIQ VM datastore > 80% full')))
    lines.append(R(bMid(L, RR, 'collection-check.sh — verifies data age < 5 minutes via API')))
    lines.append(R(bMid(L, RR, 'export-report.py — uses InsightIQ API to download scheduled report as PDF')))
    lines.append(R(bMid(L, RR, 'top-clients.py — queries InsightIQ for top-IO clients; posts to Slack')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Scripts on InsightIQ VM or management host · Python 3 + requests · SSH for admin'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('iiq_backup = Admin CLI command; wrapper script adds date suffix to archive'))
    lines.append(txt_row('Disk check = df -h /data check on appliance; alert at 80% to avoid DB fill'))
    lines.append(txt_row('Data age = Time since last collection point; stale > 5 min suggests collection issue'))
    lines.append(txt_row('InsightIQ API = Limited REST API at https://<iiq>/api; used for report downloads'))
    lines.append(txt_row('Session cookie = InsightIQ API uses session auth; POST login to get cookie'))
    lines.append(txt_row('Top clients = List of client IPs ranked by IO; requires clientstats on cluster'))
    lines.append(txt_row('Slack webhook = Posting top-client summary to storage team Slack channel'))
    lines.append(txt_row('Cron schedule = Running scripts via crontab on management host or InsightIQ VM'))
    lines.append(txt_row('SSH key auth = Prefer SSH key over password for script access to InsightIQ'))
    lines.append(txt_row('Log check = Tail /var/log/isilon/insightiq/ for collection errors'))
    lines.append(txt_row('PDF download = GET /api/v1/reports/{id}/download with session cookie'))
    lines.append(txt_row('Python requests = pip install requests; standard HTTP library for InsightIQ API'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-security', 'docs/monitoring/insightiq/security/index.md', 'InsightIQ security')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Security'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access Control'), bMid(B2_L, B2_R, 'Network Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local admin account'), bMid(B2_L, B2_R, 'HTTPS only TCP 443'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP/AD optional'), bMid(B2_L, B2_R, 'Mgmt VLAN only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC: Admin/Viewer'), bMid(B2_L, B2_R, 'SSH restricted'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Audit log local'), bMid(B2_L, B2_R, 'TLS to PAPI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Annual access audit'), bMid(B2_L, B2_R, 'Firewall inbound 443'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('InsightIQ VM on management cluster · SSH from jump host only · PAPI on TLS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Local admin = InsightIQ admin user; strong password; not shared'))
    lines.append(txt_row('LDAP integration = Optional AD/LDAP for InsightIQ UI login; centralises auth'))
    lines.append(txt_row('RBAC = Admin (full) vs Viewer (read-only) roles in InsightIQ'))
    lines.append(txt_row('PAPI user = Read-only account on PowerScale; InsightIQ credential; rotate annually'))
    lines.append(txt_row('TLS to PAPI = HTTPS connection to PAPI TCP 8083; verify or accept self-signed'))
    lines.append(txt_row('SSH restriction = Limit SSH to InsightIQ VM to jump host IP only via firewall'))
    lines.append(txt_row('Audit log = InsightIQ logs login and config changes locally'))
    lines.append(txt_row('Mgmt VLAN = InsightIQ on management network; no direct access from user VLANs'))
    lines.append(txt_row('Firewall inbound 443 = Allow only management hosts to reach InsightIQ UI'))
    lines.append(txt_row('Annual review = Yearly audit of InsightIQ users and PAPI credentials'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-troubleshooting', 'docs/monitoring/insightiq/troubleshooting/index.md', 'InsightIQ troubleshooting')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Collection Stops'), bMid(B2_L, B2_R, 'Performance Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check iiq_status'), bMid(B2_L, B2_R, 'Check VM CPU/mem'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check PAPI TCP 8080'), bMid(B2_L, B2_R, 'Check disk usage'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify PAPI user'), bMid(B2_L, B2_R, 'Check PostgreSQL'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Restart collection'), bMid(B2_L, B2_R, 'Reduce collection int'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check cluster PAPI'), bMid(B2_L, B2_R, 'Open Dell support'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Logs: /var/log/isilon/insightiq/ · iiq_status on VM · PAPI test from VM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('iiq_status = Show InsightIQ collection daemon status (running/stopped)'))
    lines.append(txt_row('PAPI TCP 8080 = Test connectivity: curl -k https://<cluster>:8080/platform/1/auth'))
    lines.append(txt_row('PAPI user test = Verify credential: curl -u <user>:<pass> https://<cluster>:8080/platform/1'))
    lines.append(txt_row('Restart collection = iiq_stop then iiq_start to recover stalled collection process'))
    lines.append(txt_row('Disk full = df -h /data; if > 95%, purge old data or expand VMDK'))
    lines.append(txt_row('PostgreSQL check = Check DB service: systemctl status postgresql'))
    lines.append(txt_row('VM CPU/mem = If InsightIQ VM is starved, add vCPU or RAM via vSphere'))
    lines.append(txt_row('Reduce interval = Increase collection interval from 30s to 5m to reduce DB write load'))
    lines.append(txt_row('PAPI on cluster = Verify cluster PAPI is enabled and accessible (isi_backend_cache_rpc_test)'))
    lines.append(txt_row('Log review = /var/log/isilon/insightiq/collection.log for error details'))
    lines.append(txt_row('Dell support = support.dell.com; attach collection log and iiq_status output'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-vendor', 'docs/monitoring/insightiq/vendor-support/index.md', 'InsightIQ vendor support')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Vendor Support'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Support Model — Dell Technologies GSS')))
    lines.append(R(bMid(L, RR, 'InsightIQ covered by PowerScale ProSupport or ProSupport Plus entitlement')))
    lines.append(R(bMid(L, RR, 'Open case at support.dell.com — provide InsightIQ version + collection log')))
    lines.append(R(bMid(L, RR, 'Sev-1: collection fully stopped on all clusters; 24x7 response')))
    lines.append(R(bMid(L, RR, 'Sev-2: collection degraded or UI inaccessible; business-hours response')))
    lines.append(R(bMid(L, RR, 'Interop matrix: confirm InsightIQ version vs PowerScale OneFS version')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('InsightIQ VM on-prem · support bundle collected locally · uploaded to Dell case portal'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ProSupport = Dell hardware support tier; required for InsightIQ support eligibility'))
    lines.append(txt_row('GSS = Global Support Services; Dell tier-1 technical support'))
    lines.append(txt_row('Collection log = /var/log/isilon/insightiq/collection.log; attach to support case'))
    lines.append(txt_row('InsightIQ version = Check in UI > Help > About; needed for case opening'))
    lines.append(txt_row('OneFS version = PowerScale OS version; must be in InsightIQ interop matrix'))
    lines.append(txt_row('Interop matrix = Dell compatibility table confirming supported OneFS/InsightIQ combos'))
    lines.append(txt_row('Severity 1 = All collection stopped; 24x7 phone; include iiq_status output'))
    lines.append(txt_row('Severity 2 = Degraded collection; business-hours response'))
    lines.append(txt_row('Support bundle = Log archive from InsightIQ; iiq_backup output + collection log'))
    lines.append(txt_row('KB = Dell Knowledge Base at kb.dell.com; search for InsightIQ symptoms'))
    lines.append(txt_row('EOL = InsightIQ End of Life; check Dell lifecycle page; plan migration to CloudIQ'))
    lines.append(txt_row('TAM = Technical Account Manager; proactive guidance for large PowerScale deployments'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-insightiq-workloads', 'docs/monitoring/insightiq/workloads/index.md', 'InsightIQ workload analysis')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'InsightIQ — Workload Analysis'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Workload Identification'), bMid(B2_L, B2_R, 'Workload Sizing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Top-IO clients'), bMid(B2_L, B2_R, 'IOPS per workload'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Top-IO shares'), bMid(B2_L, B2_R, 'Latency SLA check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Protocol by client'), bMid(B2_L, B2_R, 'Throughput required'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Time-of-day pattern'), bMid(B2_L, B2_R, 'Capacity per team'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Growth per dir'), bMid(B2_L, B2_R, 'Chargeback report'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Workload data from InsightIQ client stats · per-share and per-directory tracking'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Workload = IO pattern from a specific client, application, or directory'))
    lines.append(txt_row('Top-IO client = Client IP or hostname generating highest IOPS or throughput'))
    lines.append(txt_row('Top-IO share = NFS export or SMB share with highest IO activity'))
    lines.append(txt_row('Protocol by client = Which protocol (NFS/SMB/S3) each client uses'))
    lines.append(txt_row('Time-of-day pattern = IO activity profile over 24h; identifies batch window vs real-time'))
    lines.append(txt_row('Growth per directory = Capacity growth rate for specific directories; useful for chargeback'))
    lines.append(txt_row('Latency SLA = Target latency for a workload; InsightIQ used to verify compliance'))
    lines.append(txt_row('Chargeback = Attributing storage cost to departments using per-client/share IO data'))
    lines.append(txt_row('Capacity per team = Space consumption breakdown by team based on directory hierarchy'))
    lines.append(txt_row('Client stats = isi_clientstats on PowerScale; must be enabled for per-client data'))
    lines.append(txt_row('IOPS per workload = Average and peak IOPS for a specific application or team'))
    lines.append(txt_row('Throughput required = Peak bandwidth needed; used for network and controller sizing'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Nexus Dashboard monitoring diagrams ───────────────────────────────────────

@kb_diagram('monitoring-nexus-dashboard', 'docs/monitoring/nexus-dashboard/index.md', 'Nexus Dashboard monitoring overview')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Fabric Monitoring and Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Nexus Dashboard: Cisco management platform for ACI, DCNM/NDFC, and NX-OS fabric operations')))
    lines.append(R(bMid(L, RR, 'Hosts applications: Nexus Dashboard Insights (NDI), Fabric Controller (NDFC), Orchestrator (NDO)')))
    lines.append(R(bMid(L, RR, 'NDI: real-time telemetry, anomaly detection, flow analytics, and infrastructure health scoring')))
    lines.append(R(bMid(L, RR, 'Deployed as cluster (3 master nodes) on physical servers or VMware; connects to APIC/switches')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Nexus Dashboard centralises Cisco fabric visibility into a single platform'))
    lines.append(txt_row())
    lines.append(R(arrow([16, 50, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Insights (NDI)'), bMid(B2_L, B2_R, 'Fabric Controller'), bMid(B3_L, B3_R, 'Orchestrator'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health scores'), bMid(B2_L, B2_R, 'DCNM functions'), bMid(B3_L, B3_R, 'Multi-site ACI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Anomaly detect'), bMid(B2_L, B2_R, 'Switch inventory'), bMid(B3_L, B3_R, 'Policy stretch'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Flow analytics'), bMid(B2_L, B2_R, 'Image management'), bMid(B3_L, B3_R, 'Tenant deploy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Event analysis'), bMid(B2_L, B2_R, 'Config compliance'), bMid(B3_L, B3_R, 'Multi-fabric'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alerts/assurance'), bMid(B2_L, B2_R, 'POAP zero-touch'), bMid(B3_L, B3_R, 'BGP EVPN mgmt'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Nexus Dashboard: 3 physical/VM nodes · ACI: APIC cluster · NX-OS: switch management TCP 22/443'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Nexus Dashboard = Cisco management platform hosting fabric apps (NDI, NDFC, NDO)'))
    lines.append(txt_row('NDI = Nexus Dashboard Insights; real-time analytics and health scoring for Cisco fabrics'))
    lines.append(txt_row('NDFC = Nexus Dashboard Fabric Controller; replaces DCNM for NX-OS and SAN fabric management'))
    lines.append(txt_row('NDO = Nexus Dashboard Orchestrator; multi-site ACI policy management and tenant deployment'))
    lines.append(txt_row('APIC = Application Policy Infrastructure Controller; ACI fabric controller'))
    lines.append(txt_row('Health score = NDI composite score per fabric/site from telemetry and event analysis'))
    lines.append(txt_row('Anomaly = NDI-detected deviation from learned baseline in fabric behaviour'))
    lines.append(txt_row('Flow analytics = NDI tracking IP flows through fabric for traffic analysis'))
    lines.append(txt_row('POAP = Power-On Auto Provisioning; zero-touch NX-OS switch bootstrap'))
    lines.append(txt_row('BGP EVPN = Routing protocol for VXLAN fabric overlay managed by NDFC'))
    lines.append(txt_row('Multi-site = NDO managing policy across multiple ACI sites or NDFC fabrics'))
    lines.append(txt_row('Assurance = NDI verifying fabric state matches intended policy configuration'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-arch', 'docs/monitoring/nexus-dashboard/architecture/index.md', 'Nexus Dashboard architecture')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Cluster: 3 master nodes (physical or VMware) for HA; optional worker nodes for scale')))
    lines.append(R(bMid(L, RR, 'Management network: ND cluster internal · Data network: connects to ACI/NX-OS fabrics')))
    lines.append(R(bMid(L, RR, 'Persistent storage: internal or external (pure, block); 500 GB+ per master node')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  3-node cluster provides quorum and HA; all master nodes active for app hosting'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Nexus Dashboard Cluster'), bMid(B2_L, B2_R, 'Fabric Connectivity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3 master nodes min'), bMid(B2_L, B2_R, 'APIC: TCP 443'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Kubernetes base OS'), bMid(B2_L, B2_R, 'NX-OS: SSH TCP 22'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App containers'), bMid(B2_L, B2_R, 'NDFC: gRPC/streaming'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2 networks: mgmt/data'), bMid(B2_L, B2_R, 'NDI: streaming telem'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '500 GB+ per node'), bMid(B2_L, B2_R, 'HTTPS for web UI/API'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Physical: 3x Cisco UCS/x86 nodes · VM: 3x VMware VMs (16 vCPU/64 GB each) · SSD storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master node = Primary Nexus Dashboard node hosting apps and control plane'))
    lines.append(txt_row('Worker node = Additional node adding capacity for app scale; optional'))
    lines.append(txt_row('Kubernetes = Container orchestration layer running ND apps as pods'))
    lines.append(txt_row('Management network = ND cluster internal communication and admin access'))
    lines.append(txt_row('Data network = Connectivity from ND to managed fabrics (APIC, switches)'))
    lines.append(txt_row('gRPC = Protocol for streaming telemetry from NX-OS switches to NDI'))
    lines.append(txt_row('Streaming telemetry = Real-time metric push from switches to NDI; MDT protocol'))
    lines.append(txt_row('App containers = NDI, NDFC, NDO each run as containerised apps on ND'))
    lines.append(txt_row('Quorum = 3-node cluster requires 2 nodes for majority decision'))
    lines.append(txt_row('Persistent storage = ND stores DB data on node local disk or external block'))
    lines.append(txt_row('MDT = Model-Driven Telemetry; real-time sensor push from NX-OS to NDI'))
    lines.append(txt_row('SSD = Flash storage required for streaming telemetry DB write performance'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-arch-how', 'docs/monitoring/nexus-dashboard/architecture/how-it-works/index.md', 'Nexus Dashboard how it works')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Step 1: Onboarding — add APIC or NX-OS fabric to Nexus Dashboard with credentials')))
    lines.append(R(bMid(L, RR, 'Step 2: Telemetry — switches stream metrics via MDT/gRPC to NDI continuously')))
    lines.append(R(bMid(L, RR, 'Step 3: Analysis — NDI ML models score health, detect anomalies, and analyse flows')))
    lines.append(R(bMid(L, RR, 'Step 4: Alert — health score drops or anomaly detected triggers event in NDI')))
    lines.append(R(bMid(L, RR, 'Step 5: Notification — email or webhook sent; ServiceNow integration creates incident')))
    lines.append(R(bMid(L, RR, 'Step 6: Remediation — engineer reviews event; NDI shows affected objects and fix')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Switches stream telemetry to ND data network IP · APIC queried via REST · ND cluster processes'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Onboarding = Adding fabric to ND; requires APIC IP/credentials or switch SSH access'))
    lines.append(txt_row('MDT = Model-Driven Telemetry; NX-OS sensor push to NDI for real-time data'))
    lines.append(txt_row('gRPC = Transport for MDT streaming; port 9339 from switch to ND data IP'))
    lines.append(txt_row('Health score = NDI composite score per site/fabric/object from telemetry analysis'))
    lines.append(txt_row('Anomaly = NDI ML deviation from learned baseline in fabric metrics'))
    lines.append(txt_row('Flow analysis = NDI tracking actual IP flows for EPG connectivity verification'))
    lines.append(txt_row('Event = NDI alert for health drop, anomaly, or assurance violation'))
    lines.append(txt_row('Assurance = NDI verifying actual fabric state matches ACI policy intent'))
    lines.append(txt_row('Notification = Email or webhook from ND when event fires'))
    lines.append(txt_row('ServiceNow = NDI integration creating ITSM incidents from fabric events'))
    lines.append(txt_row('Affected objects = NDI identifying specific switch, interface, or EPG causing health drop'))
    lines.append(txt_row('Fabric site = Single ACI fabric or DCNM/NDFC managed NX-OS domain added to ND'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-arch-design', 'docs/monitoring/nexus-dashboard/architecture/design-standards/index.md', 'Nexus Dashboard design standards')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cluster Standards'), bMid(B2_L, B2_R, 'Operational Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3 physical nodes min'), bMid(B2_L, B2_R, 'All fabrics onboarded'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSD 500 GB+ per node'), bMid(B2_L, B2_R, 'MDT on all switches'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Separate mgmt+data net'), bMid(B2_L, B2_R, 'Alerts to ITSM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup config nightly'), bMid(B2_L, B2_R, 'Weekly health review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NTP and DNS config'), bMid(B2_L, B2_R, 'Dedicated read-only acct'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('3 physical x86 or VM nodes · SSD storage · dual-homed to mgmt and data networks'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Physical nodes minimum = Bare metal preferred for production; 3 for quorum'))
    lines.append(txt_row('SSD 500 GB = Flash required for streaming telemetry time-series write performance'))
    lines.append(txt_row('Separate networks = ND requires dedicated management and data network interfaces'))
    lines.append(txt_row('MDT on all switches = Model-Driven Telemetry enabled on every monitored switch'))
    lines.append(txt_row('All fabrics onboarded = Every ACI and NX-OS fabric registered in ND'))
    lines.append(txt_row('ITSM alert = Every NDI event/anomaly routed to ServiceNow via webhook'))
    lines.append(txt_row('Read-only account = Dedicated APIC user with Observer role for NDI'))
    lines.append(txt_row('NTP consistency = ND and all switches must use same NTP source for telemetry alignment'))
    lines.append(txt_row('Weekly health review = Scheduled review of NDI health scores and open anomalies'))
    lines.append(txt_row('Backup = ND config backup nightly; stored externally on NFS or SCP target'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-arch-int', 'docs/monitoring/nexus-dashboard/architecture/integrations/index.md', 'Nexus Dashboard integrations')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Fabric Inputs', 'Notification Outputs'])))
    lines.append(R(sections(L, RR, [50], ['ACI: APIC REST API', 'Email SMTP'])))
    lines.append(R(sections(L, RR, [50], ['NX-OS: MDT gRPC/SSH', 'ServiceNow webhook'])))
    lines.append(R(sections(L, RR, [50], ['Cisco Intersight (HX)', 'PagerDuty webhook'])))
    lines.append(R(sections(L, RR, [50], ['Crosswork Network Ctrl', 'Webex Teams webhook'])))
    lines.append(R(sections(L, RR, [50], ['Third-party RESTCONF', 'Syslog to SIEM'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ND data network → fabrics · ND management → ITSM/email · gRPC TCP 9339 for MDT'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('APIC REST API = NDI polls APIC at TCP 443 for ACI fabric inventory and events'))
    lines.append(txt_row('MDT gRPC = NX-OS switches stream telemetry to ND data IP TCP 9339'))
    lines.append(txt_row('SSH = NDFC uses SSH TCP 22 to NX-OS switches for config and inventory'))
    lines.append(txt_row('Intersight = Cisco cloud management; HyperFlex cluster data fed to ND'))
    lines.append(txt_row('Crosswork = Cisco network controller; can forward telemetry to ND'))
    lines.append(txt_row('RESTCONF = Standard REST API on NX-OS; used for config and state queries'))
    lines.append(txt_row('ServiceNow = NDI events forwarded as incidents via REST webhook'))
    lines.append(txt_row('PagerDuty = On-call routing for critical NDI fabric events'))
    lines.append(txt_row('Webex Teams = Cisco collaboration; NDI events posted to space via webhook'))
    lines.append(txt_row('Syslog = NDI events forwarded to SIEM for security correlation'))
    lines.append(txt_row('TCP 9339 = gRPC port for MDT streaming from NX-OS to ND'))
    lines.append(txt_row('SMTP = Email notification for NDI events; configured in ND admin settings'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-alerts', 'docs/monitoring/nexus-dashboard/alerts/index.md', 'Nexus Dashboard alerts')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Alerts'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['NDI Alert Categories', 'Alert Actions'])))
    lines.append(R(sections(L, RR, [50], ['Anomaly: ML deviation', 'Acknowledge: seen'])))
    lines.append(R(sections(L, RR, [50], ['Compliance: policy mismatch', 'Assign: to engineer'])))
    lines.append(R(sections(L, RR, [50], ['Health: score degraded', 'Suppress: known issue'])))
    lines.append(R(sections(L, RR, [50], ['Bug: known Cisco SW defect', 'Create ITSM ticket'])))
    lines.append(R(sections(L, RR, [50], ['Delta: config changed', 'Export for audit'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('NDI generates alerts from telemetry · delivered via ND console, email, webhook'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Anomaly = NDI ML deviation from baseline; may indicate failure or misconfiguration'))
    lines.append(txt_row('Compliance = ACI EPG/contract or NX-OS configuration deviating from verified state'))
    lines.append(txt_row('Health alert = NDI site/fabric health score dropping below threshold'))
    lines.append(txt_row('Bug = NDI matching observed symptoms to Cisco known defect database'))
    lines.append(txt_row('Delta = Change event; NDI showing what configuration changed and when'))
    lines.append(txt_row('Acknowledge = Engineer marks alert as seen; stops re-notification'))
    lines.append(txt_row('Suppress = Muting known benign alert for a defined period'))
    lines.append(txt_row('ITSM ticket = ServiceNow incident created from NDI alert via webhook'))
    lines.append(txt_row('Severity = Critical/Major/Minor/Warning; routes to different teams'))
    lines.append(txt_row('Affected epoch = NDI time window during which anomaly was detected'))
    lines.append(txt_row('Impact = NDI assessment of scope (how many objects affected)'))
    lines.append(txt_row('Root cause = NDI correlation linking symptom to underlying network event'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-cli', 'docs/monitoring/nexus-dashboard/cli-reference/index.md', 'Nexus Dashboard CLI reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Nexus Dashboard admin CLI — SSH to any master node, admin user')))
    lines.append(R(bMid(L, RR, 'acs health — show cluster node health and app status')))
    lines.append(R(bMid(L, RR, 'acs backup create — create cluster config backup')))
    lines.append(R(bMid(L, RR, 'acs logs download — download app logs bundle for troubleshooting')))
    lines.append(R(bMid(L, RR, 'acs restart — restart cluster services (use with caution)')))
    lines.append(R(bMid(L, RR, 'kubectl (on ND) — inspect Kubernetes pods hosting ND apps')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('SSH to ND management IP · admin user · commands affect entire cluster'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('acs = Admin CLI Suite; Nexus Dashboard command-line interface'))
    lines.append(txt_row('acs health = Returns node status: ACTIVE/STANDBY/FAILURE for each master'))
    lines.append(txt_row('acs backup create = Creates config snapshot; stored locally or exported to SCP/NFS'))
    lines.append(txt_row('acs logs download = Collects app and system logs bundle for Dell/Cisco support'))
    lines.append(txt_row('acs restart = Restarts all ND services; use only during maintenance window'))
    lines.append(txt_row('kubectl = Kubernetes CLI available on ND for pod inspection'))
    lines.append(txt_row('Pod = Container instance running an ND app (NDI, NDFC, NDO, or ND service)'))
    lines.append(txt_row('acs upgrade = Initiates cluster upgrade from uploaded image'))
    lines.append(txt_row('acs cluster status = Shows cluster quorum state and node roles'))
    lines.append(txt_row('acs app status = Lists installed apps and their running/stopped state'))
    lines.append(txt_row('NDI REST API = https://<nd-ip>/sedgeapi/v1; auth via /api/v1/auth/token'))
    lines.append(txt_row('APIC Read-Only = Minimum privilege for NDI APIC credentials: Observer role'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-design', 'docs/monitoring/nexus-dashboard/design-standards/index.md', 'Nexus Dashboard design standards top-level')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Platform Standards'), bMid(B2_L, B2_R, 'Monitoring Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3 physical nodes'), bMid(B2_L, B2_R, 'All fabrics onboarded'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSD 500+ GB/node'), bMid(B2_L, B2_R, 'MDT on all switches'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dedicated mgmt/data'), bMid(B2_L, B2_R, 'ITSM integration'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ND backup daily'), bMid(B2_L, B2_R, 'Weekly anomaly review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC: role per team'), bMid(B2_L, B2_R, 'Compliance schedule'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('3 physical nodes minimum · SSD storage · dual-network (mgmt + data)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Physical nodes = Bare-metal ND for production; 3 nodes for quorum'))
    lines.append(txt_row('SSD 500 GB = Flash per node for streaming telemetry time-series write'))
    lines.append(txt_row('Dedicated networks = ND requires separate management and data network interfaces'))
    lines.append(txt_row('MDT on all switches = Model-Driven Telemetry enabled on all fabric switches'))
    lines.append(txt_row('ITSM integration = ServiceNow webhook configured in ND for all NDI events'))
    lines.append(txt_row('Compliance schedule = NDI running assurance checks on defined cadence'))
    lines.append(txt_row('RBAC = Role-Based Access Control; Admin/Operator/Viewer per team'))
    lines.append(txt_row('Weekly review = Calendar event for NDI anomaly and health score review'))
    lines.append(txt_row('Backup daily = acs backup create scheduled and archived off-node'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-fabric-health', 'docs/monitoring/nexus-dashboard/fabric-health/index.md', 'Nexus Dashboard fabric health')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Fabric Health'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'NDI Fabric Health Score: 0-100 composite per site from telemetry and event analysis')))
    lines.append(R(bMid(L, RR, 'Input categories: endpoints, nodes, interfaces, tunnels, services, resources')))
    lines.append(R(bMid(L, RR, 'Score 91-100: Healthy · 81-90: Warning · 0-80: Critical')))
    lines.append(R(bMid(L, RR, 'Trend: improving/steady/degrading over last collection epoch')))
    lines.append(R(bMid(L, RR, 'Anomaly drill-down: click score to see contributing issues ranked by impact')))
    lines.append(R(bMid(L, RR, 'Historical view: 30-day score trend per site and per fabric component')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Health computed in NDI from MDT/APIC data · updated every 15 minutes · stored in ND DB'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Site = Single ACI or DCNM/NDFC fabric registered in ND; health score per site'))
    lines.append(txt_row('Epoch = NDI analysis time window (15-minute snapshot); health computed per epoch'))
    lines.append(txt_row('Endpoint = VM, bare-metal, or container connected to fabric leaf switch'))
    lines.append(txt_row('Node = Spine or leaf switch; node health input covers CPU, memory, and error counters'))
    lines.append(txt_row('Interface = Physical or logical port; errors and drops contribute to interface health'))
    lines.append(txt_row('Tunnel = VXLAN or GRE overlay; tunnel health reflects underlay reachability'))
    lines.append(txt_row('Resources = ACI fabric resources: EPG, BD, contract counts approaching capacity'))
    lines.append(txt_row('Services = Layer-4 to -7 services: load balancers, firewalls inserted in fabric'))
    lines.append(txt_row('Anomaly impact = NDI score for each anomaly showing how much it reduces site health'))
    lines.append(txt_row('Critical score = Below 81; immediate investigation required; page on-call network team'))
    lines.append(txt_row('Healthy score = 91-100; normal operation; review weekly for trend changes'))
    lines.append(txt_row('Drill-down = NDI UI allows clicking from site score to node to interface level'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-integration', 'docs/monitoring/nexus-dashboard/integration/index.md', 'Nexus Dashboard integration guide')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Integration Guide'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ITSM Integration'), bMid(B2_L, B2_R, 'Observability Stack'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ServiceNow webhook'), bMid(B2_L, B2_R, 'Syslog to SIEM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Auto incident create'), bMid(B2_L, B2_R, 'Splunk HEC forward'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PagerDuty events'), bMid(B2_L, B2_R, 'Prometheus exporter'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Webex Teams notify'), bMid(B2_L, B2_R, 'Custom REST client'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Email SMTP alerts'), bMid(B2_L, B2_R, 'Grafana data source'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ND on-prem · outbound TCP 443 to ITSM SaaS · syslog UDP 514 or TCP 514 to SIEM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ServiceNow webhook = NDI POST to ServiceNow Event endpoint on alert fire'))
    lines.append(txt_row('Auto incident = ServiceNow incident auto-created from NDI alert payload'))
    lines.append(txt_row('PagerDuty = NDI sends Events API v2 payload; on-call routing by severity'))
    lines.append(txt_row('Webex Teams = Cisco collaboration; NDI posts event summary to room via webhook'))
    lines.append(txt_row('Syslog = NDI events forwarded as syslog to SIEM for security correlation'))
    lines.append(txt_row('Splunk HEC = HTTP Event Collector; NDI events for log analytics'))
    lines.append(txt_row('Prometheus = NDI /metrics endpoint scraped by Prometheus'))
    lines.append(txt_row('Grafana = ND REST API proxied as Grafana data source for custom panels'))
    lines.append(txt_row('REST client = Script polling NDI API and pushing to proprietary monitoring'))
    lines.append(txt_row('SMTP = Email notification for NDI events; configured in ND admin settings'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-integrations', 'docs/monitoring/nexus-dashboard/integrations/index.md', 'Nexus Dashboard integrations list')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Fabric Sources', 'Management Targets'])))
    lines.append(R(sections(L, RR, [50], ['ACI multi-site APIC', 'Cisco TAC Smart Call Home'])))
    lines.append(R(sections(L, RR, [50], ['NX-OS DCNM/NDFC', 'ServiceNow CMDB + events'])))
    lines.append(R(sections(L, RR, [50], ['HyperFlex Intersight', 'PagerDuty on-call routing'])))
    lines.append(R(sections(L, RR, [50], ['SD-WAN vManage', 'Splunk / Elastic SIEM'])))
    lines.append(R(sections(L, RR, [50], ['Kubernetes (ND Apps)', 'Webex Teams / Slack'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ND data network to fabrics · ND management to cloud SaaS targets · TCP 443 outbound'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Multi-site APIC = Multiple ACI fabrics each with their own APIC registered in ND'))
    lines.append(txt_row('Smart Call Home = Cisco TAC automatic support case from ND critical events'))
    lines.append(txt_row('CMDB = ServiceNow Configuration Management DB; ND updates CIs from fabric inventory'))
    lines.append(txt_row('HyperFlex = Cisco HCI; managed via Intersight; ND can pull cluster health'))
    lines.append(txt_row('SD-WAN vManage = Cisco SD-WAN controller; ND integration for WAN edge visibility'))
    lines.append(txt_row('ND Apps = NDI, NDFC, NDO run as Kubernetes apps inside ND cluster'))
    lines.append(txt_row('Webex Teams = Cisco collaboration; NDI posts events to room via webhook'))
    lines.append(txt_row('Splunk / Elastic = SIEM platforms receiving ND syslog or HEC event streams'))
    lines.append(txt_row('PagerDuty = On-call routing; ND sends events via Events API v2'))
    lines.append(txt_row('Cisco TAC = Technical Assistance Centre; Smart Call Home auto-opens cases'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-lifecycle', 'docs/monitoring/nexus-dashboard/lifecycle/index.md', 'Nexus Dashboard lifecycle')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Lifecycle Management'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Deploy'), bMid(B2_L, B2_R, 'Upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bootstrap 3 nodes'), bMid(B2_L, B2_R, 'Check release notes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Assign mgmt + data IPs'), bMid(B2_L, B2_R, 'Backup config first'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Form cluster via UI'), bMid(B2_L, B2_R, 'acs upgrade apply'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Install apps (NDI etc)'), bMid(B2_L, B2_R, 'Rolling node upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Onboard fabrics'), bMid(B2_L, B2_R, 'Verify apps post'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Configure ITSM out'), bMid(B2_L, B2_R, 'Rollback if fail'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('3 physical or VM nodes · Cisco ISO install · upgrade via acs CLI or ND UI'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Bootstrap = Initial ND node setup: assign hostname, IPs, NTP, DNS via console'))
    lines.append(txt_row('Cluster form = Joining 3 nodes into quorum cluster via ND web UI'))
    lines.append(txt_row('App install = Installing NDI, NDFC, NDO as apps from ND admin > Apps'))
    lines.append(txt_row('Fabric onboard = Adding APIC or NX-OS fabric to ND with credentials'))
    lines.append(txt_row('acs upgrade = CLI command to apply upgrade image to cluster'))
    lines.append(txt_row('Rolling upgrade = Upgrading nodes sequentially to maintain quorum'))
    lines.append(txt_row('Backup = acs backup create before upgrade; stored externally'))
    lines.append(txt_row('Rollback = Restoring from backup if upgrade causes data loss'))
    lines.append(txt_row('Release notes = Cisco release notes; check for breaking changes before upgrade'))
    lines.append(txt_row('Verify apps = Post-upgrade check: NDI collecting, NDFC managing, NDO syncing'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-ops', 'docs/monitoring/nexus-dashboard/operations/index.md', 'Nexus Dashboard operations')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Operations'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Daily'), bMid(B2_L, B2_R, 'Weekly'), bMid(B3_L, B3_R, 'Monthly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review NDI health'), bMid(B2_L, B2_R, 'Anomaly review'), bMid(B3_L, B3_R, 'Compliance audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check anomalies'), bMid(B2_L, B2_R, 'Act on ITSM items'), bMid(B3_L, B3_R, 'Threshold review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify cluster OK'), bMid(B2_L, B2_R, 'Review flow data'), bMid(B3_L, B3_R, 'Access review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check backup ran'), bMid(B2_L, B2_R, 'Dismiss false pos'), bMid(B3_L, B3_R, 'Report to mgmt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Triage new events'), bMid(B2_L, B2_R, 'Capacity outlook'), bMid(B3_L, B3_R, 'Upgrade planning'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Operations via ND web UI and acs CLI · ND management IP via browser'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('NDI health = Site health score overview; check daily for score drops'))
    lines.append(txt_row('Cluster check = acs health to confirm all 3 nodes ACTIVE'))
    lines.append(txt_row('Backup verification = acs backup list to confirm daily backup completed'))
    lines.append(txt_row('Anomaly review = Weekly triage of open NDI anomalies; dismiss or create tickets'))
    lines.append(txt_row('Flow review = Weekly check of NDI flow analytics for unexpected traffic patterns'))
    lines.append(txt_row('Compliance audit = Monthly NDI assurance run verifying fabric matches policy'))
    lines.append(txt_row('Access review = Monthly audit of ND user list; remove stale accounts'))
    lines.append(txt_row('Upgrade planning = Monthly check of ND/NDI release cadence for patch scheduling'))
    lines.append(txt_row('False positive = Anomaly that does not represent a real issue; dismiss with reason'))
    lines.append(txt_row('Capacity outlook = ND storage and compute resource trending; plan expansion'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-scripts', 'docs/monitoring/nexus-dashboard/scripts/index.md', 'Nexus Dashboard scripts reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Scripts Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'NDI REST API scripts — Python examples')))
    lines.append(R(bMid(L, RR, 'get-token.py: POST /sedgeapi/v1/auth/token → Bearer token')))
    lines.append(R(bMid(L, RR, 'get-anomalies.py: GET /sedgeapi/v1/ndi/anomalies?status=ACTIVE')))
    lines.append(R(bMid(L, RR, 'site-health.py: GET /sedgeapi/v1/ndi/sites/{id}/health — score per site')))
    lines.append(R(bMid(L, RR, 'acs-health-check.sh: SSH to ND master → acs health → parse output')))
    lines.append(R(bMid(L, RR, 'nd-backup.sh: SSH to ND → acs backup create → verify archive exists')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Scripts from management host · Python 3 + requests + paramiko · ND TCP 443/22'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('sedgeapi = NDI REST API path prefix; all NDI endpoints start with /sedgeapi/v1'))
    lines.append(txt_row('Bearer token = Auth credential from /auth/token; pass in Authorization header'))
    lines.append(txt_row('anomalies endpoint = NDI list of active anomalies with severity and affected objects'))
    lines.append(txt_row('site health endpoint = NDI health score for a specific fabric site'))
    lines.append(txt_row('acs health = CLI command on ND master showing cluster node status'))
    lines.append(txt_row('paramiko = Python SSH library for running acs commands remotely'))
    lines.append(txt_row('acs backup create = Creates ND config snapshot; verify with acs backup list'))
    lines.append(txt_row('Status filter = ?status=ACTIVE to return only unresolved anomalies'))
    lines.append(txt_row('Site ID = UUID of fabric site; retrieve from /sedgeapi/v1/ndi/sites'))
    lines.append(txt_row('Pagination = NDI API uses offset/limit; default 25 records per page'))
    lines.append(txt_row('Cron = Schedule scripts via crontab for daily health and backup checks'))
    lines.append(txt_row('JSON response = NDI API returns JSON; parse with json module or jq'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-security', 'docs/monitoring/nexus-dashboard/security/index.md', 'Nexus Dashboard security')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Security'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access Control'), bMid(B2_L, B2_R, 'Network Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local + LDAP/TACACS'), bMid(B2_L, B2_R, 'HTTPS only TCP 443'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC: role per team'), bMid(B2_L, B2_R, 'Mgmt VLAN only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'APIC read-only user'), bMid(B2_L, B2_R, 'TLS inter-node'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA integration'), bMid(B2_L, B2_R, 'gRPC auth MDT'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Annual access review'), bMid(B2_L, B2_R, 'Audit log in ND'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ND cluster on management network · APIC observer account · gRPC on data network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TACACS+ = AAA protocol for ND admin authentication; integrates with Cisco ISE'))
    lines.append(txt_row('LDAP = Directory authentication for ND UI login via AD/OpenLDAP'))
    lines.append(txt_row('RBAC = Admin/Operator/Viewer roles; scoped to site or global'))
    lines.append(txt_row('APIC Observer = Minimum-privilege read-only role for NDI APIC integration'))
    lines.append(txt_row('MFA = Multi-factor auth via SAML/SSO; ND supports external IdP'))
    lines.append(txt_row('TLS inter-node = All ND cluster internal traffic encrypted'))
    lines.append(txt_row('gRPC auth = MDT streaming uses TLS with certificate authentication'))
    lines.append(txt_row('Audit log = ND records logins, config changes, and user actions'))
    lines.append(txt_row('Mgmt VLAN = ND admin UI on management network; data network for fabric only'))
    lines.append(txt_row('Annual review = Yearly audit of ND accounts and APIC service account'))
    lines.append(txt_row('Custom cert = Replace ND self-signed with CA cert in ND admin > Certificate'))
    lines.append(txt_row('SSH restriction = Limit SSH to ND master nodes to jump-host IPs only'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-troubleshooting', 'docs/monitoring/nexus-dashboard/troubleshooting/index.md', 'Nexus Dashboard troubleshooting')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fabric Not Collecting'), bMid(B2_L, B2_R, 'Cluster Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check APIC credential'), bMid(B2_L, B2_R, 'acs health check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify TCP 443 reach'), bMid(B2_L, B2_R, 'acs cluster status'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check MDT gRPC 9339'), bMid(B2_L, B2_R, 'Check disk space'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Re-onboard fabric'), bMid(B2_L, B2_R, 'acs logs download'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check NDI app status'), bMid(B2_L, B2_R, 'Cisco TAC case'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ND admin CLI via SSH · acs health · acs logs download · gRPC from switch to ND data IP'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('acs health = Shows ACTIVE/STANDBY/FAILURE state of each ND master node'))
    lines.append(txt_row('acs cluster status = Quorum state and leader node identification'))
    lines.append(txt_row('acs logs download = Creates log bundle for all apps; attach to Cisco TAC case'))
    lines.append(txt_row('APIC credential = NDI uses Observer role; re-enter if expired'))
    lines.append(txt_row('TCP 443 reach = curl -k https://<apic>/api/class/fvTenant.json from ND data IP'))
    lines.append(txt_row('MDT gRPC 9339 = telnet <nd-data-ip> 9339 from switch to test streaming path'))
    lines.append(txt_row('Re-onboard = Remove and re-add fabric in ND; resets collection state'))
    lines.append(txt_row('NDI app status = acs app status; NDI should show RUNNING'))
    lines.append(txt_row('Disk space = df -h on ND master; 80% triggers cleanup of old telemetry'))
    lines.append(txt_row('kubectl logs = kubectl logs <pod> -n ndinsights for NDI container logs'))
    lines.append(txt_row('Cisco TAC = Open case at cisco.com/support; attach acs logs bundle'))
    lines.append(txt_row('Epoch gap = NDI shows missing epochs when telemetry interrupted'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-vendor', 'docs/monitoring/nexus-dashboard/vendor-support/index.md', 'Nexus Dashboard vendor support')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Vendor Support'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Support Model — Cisco TAC')))
    lines.append(R(bMid(L, RR, 'Nexus Dashboard covered by Cisco DNA Advantage or ACI Premier license')))
    lines.append(R(bMid(L, RR, 'Open TAC case: cisco.com/support or call 1-800-553-2447')))
    lines.append(R(bMid(L, RR, 'Sev-1: production fabric unreachable or ND cluster down; 24x7 response')))
    lines.append(R(bMid(L, RR, 'Collect: acs logs download → attach to TAC case')))
    lines.append(R(bMid(L, RR, 'Smart Call Home: auto-opens TAC case on critical events if configured')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ND on-prem · logs bundle collected locally · uploaded to TAC case portal'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cisco TAC = Technical Assistance Centre; 24x7 for Sev-1 production issues'))
    lines.append(txt_row('DNA Advantage = Cisco licensing tier required for Nexus Dashboard'))
    lines.append(txt_row('ACI Premier = ACI licensing tier including NDI and NDO'))
    lines.append(txt_row('acs logs download = Log bundle command; required attachment for ND support cases'))
    lines.append(txt_row('Smart Call Home = ND feature auto-opening Cisco TAC case on critical cluster events'))
    lines.append(txt_row('Severity 1 = Fabric unreachable or ND cluster failed; 24x7 phone response'))
    lines.append(txt_row('Severity 2 = NDI not collecting or major feature down; 4-hour response'))
    lines.append(txt_row('Contract check = Cisco TAC requires valid SMARTNET or DNA/ACI contract'))
    lines.append(txt_row('Bug search = Cisco Bug Search Tool (bst.cisco.com); search by ND version + symptom'))
    lines.append(txt_row('Release notes = Per-version Cisco ND release notes; check before upgrade'))
    lines.append(txt_row('Interop matrix = Cisco compatibility matrix for ND vs NX-OS/ACI versions'))
    lines.append(txt_row('TAM = Technical Account Manager; proactive Cisco contact for enterprise customers'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-nexus-visibility', 'docs/monitoring/nexus-dashboard/visibility/index.md', 'Nexus Dashboard visibility')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Nexus Dashboard — Visibility'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'NDI Visibility: comprehensive view of fabric state — topology, endpoints, flows')))
    lines.append(R(bMid(L, RR, 'Topology view: interactive map of spine/leaf/border-leaf interconnects')))
    lines.append(R(bMid(L, RR, 'Endpoint tracking: VM/container moves, dual-home detection, stale entries')))
    lines.append(R(bMid(L, RR, 'Flow analytics: per-flow visibility with source/dest/protocol/bytes')))
    lines.append(R(bMid(L, RR, 'Audit trail: who changed what and when across ACI and NX-OS fabrics')))
    lines.append(R(bMid(L, RR, 'Multi-site: unified view across multiple ACI domains in single UI')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Visibility data from APIC REST + MDT streaming · stored in NDI DB · rendered in ND UI'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Topology view = Interactive fabric map showing switch interconnects and health'))
    lines.append(txt_row('Endpoint = VM, container, or bare-metal IP/MAC connected to fabric leaf'))
    lines.append(txt_row('Dual-home = Endpoint connected to two leaf switches for redundancy'))
    lines.append(txt_row('Stale endpoint = Endpoint record remaining after VM is deleted; detected by NDI'))
    lines.append(txt_row('Flow analytics = NDI tracking actual traffic flows through fabric for visibility'))
    lines.append(txt_row('Audit trail = NDI logging all APIC configuration changes with user and timestamp'))
    lines.append(txt_row('Multi-site view = Single ND UI showing health and state for all registered ACI sites'))
    lines.append(txt_row('EPG = Endpoint Group; ACI policy construct; endpoints grouped by EPG'))
    lines.append(txt_row('Contract = ACI inter-EPG connectivity policy; NDI verifies enforcement'))
    lines.append(txt_row('BD = Bridge Domain; ACI Layer-2 forwarding domain containing EPGs'))
    lines.append(txt_row('Border leaf = Leaf switch connecting ACI fabric to external L3 networks'))
    lines.append(txt_row('Delta analysis = NDI showing configuration changes between two epochs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Pure1 diagrams ────────────────────────────────────────────────────────────

@kb_diagram('monitoring-pure1', 'docs/monitoring/pure1/index.md', 'Pure1 — Pure Storage cloud management and analytics')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Pure Storage Cloud Management and Analytics'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Pure1: SaaS management and AI/ML analytics platform for Pure Storage FlashArray and FlashBlade')))
    lines.append(R(bMid(L, RR, 'Phonehome: arrays connect outbound to pure1.purestorage.com; no inbound required')))
    lines.append(R(bMid(L, RR, 'AI-driven workload intelligence, capacity forecasting, and proactive support automation')))
    lines.append(R(bMid(L, RR, 'Access at pure1.purestorage.com; browser-based; no on-prem software to install')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Pure1 provides global visibility across all arrays; Evergreen subscription includes Pure1'))
    lines.append(txt_row())
    lines.append(R(arrow([16, 50, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health & Alerts'), bMid(B2_L, B2_R, 'Analytics'), bMid(B3_L, B3_R, 'Support'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health score'), bMid(B2_L, B2_R, 'Workload ID'), bMid(B3_L, B3_R, 'Auto case open'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Proactive alerts'), bMid(B2_L, B2_R, 'AI forecast'), bMid(B3_L, B3_R, 'Remote assist'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Email/webhook'), bMid(B2_L, B2_R, 'Capacity plan'), bMid(B3_L, B3_R, 'Proactive swap'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Severity levels'), bMid(B2_L, B2_R, 'Perf analysis'), bMid(B3_L, B3_R, 'Evergreen mgmt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Audit log'), bMid(B2_L, B2_R, 'Benchmark'), bMid(B3_L, B3_R, 'License track'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('FlashArrays/FlashBlades on-prem · TCP 443 outbound to pure1.purestorage.com · no gateway needed'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Pure1 = Pure Storage SaaS platform for fleet management and AI analytics'))
    lines.append(txt_row('Phonehome = Array outbound telemetry to Pure cloud; encrypted; no inbound required'))
    lines.append(txt_row('Evergreen = Pure Storage subscription model; includes Pure1 and hardware refresh rights'))
    lines.append(txt_row('Health score = Composite score per array from telemetry analysis'))
    lines.append(txt_row('Workload ID = AI identifying application workload patterns on array (VDI, Oracle, etc.)'))
    lines.append(txt_row('AI forecast = ML-based capacity exhaustion prediction per array'))
    lines.append(txt_row('Proactive alert = Pure1 detecting pre-failure condition before customer notices'))
    lines.append(txt_row('Auto case = Pure1 automatically opening support case with diagnostic data attached'))
    lines.append(txt_row('Remote assist = Pure Storage engineer connecting to array via Pure1 for support'))
    lines.append(txt_row('Proactive swap = Pure staging replacement hardware before failure occurs'))
    lines.append(txt_row('Benchmark = Pure1 comparing array performance to anonymised fleet averages'))
    lines.append(txt_row('License track = Pure1 showing Purity version and Evergreen subscription status'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-arch', 'docs/monitoring/pure1/architecture/index.md', 'Pure1 architecture overview')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Pure1 Cloud (pure1.purestorage.com) — SaaS backend operated by Pure Storage')))
    lines.append(R(bMid(L, RR, 'AI/ML engine · Time-series DB · Alert engine · Workload analyser · REST API')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Phonehome: arrays push telemetry outbound over HTTPS/443 to Pure cloud; zero inbound'))
    lines.append(txt_row())
    lines.append(R(arrow([50])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'On-Premises Arrays'), bMid(B2_L, B2_R, 'Pure1 Cloud Services'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FlashArray//X/C/E'), bMid(B2_L, B2_R, 'AI/ML analytics'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FlashBlade//S/E'), bMid(B2_L, B2_R, 'Capacity forecasting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Phonehome TCP 443'), bMid(B2_L, B2_R, 'Proactive support'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No gateway needed'), bMid(B2_L, B2_R, 'Workload ID'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Purity OS built-in'), bMid(B2_L, B2_R, 'REST API for tooling'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('FlashArrays/FlashBlades on-prem · Purity OS handles phonehome · TCP 443 outbound only'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Phonehome = Purity OS built-in feature sending telemetry to Pure cloud over HTTPS'))
    lines.append(txt_row('SaaS = Software as a Service; Pure1 hosted and operated by Pure Storage'))
    lines.append(txt_row('Purity OS = Pure Storage operating system running on FlashArray and FlashBlade'))
    lines.append(txt_row('FlashArray//X = NVMe all-flash array for block workloads'))
    lines.append(txt_row('FlashArray//C = QLC NVMe array for capacity-optimised workloads'))
    lines.append(txt_row('FlashBlade//S = Unstructured data all-flash platform for file and object'))
    lines.append(txt_row('AI/ML analytics = Pure1 ML models for anomaly detection and failure prediction'))
    lines.append(txt_row('Workload ID = Pure1 classifying workload type from IO pattern (VDI, Oracle, AI/ML)'))
    lines.append(txt_row('Proactive support = Pure1 detecting pre-failure and staging replacement before alert'))
    lines.append(txt_row('REST API = Pure1 programmatic interface for metrics and array management'))
    lines.append(txt_row('No gateway = FlashArray/FlashBlade connect directly to Pure cloud; no proxy needed'))
    lines.append(txt_row('Zero inbound = Pure cloud never initiates connections to customer network'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-arch-how', 'docs/monitoring/pure1/architecture/how-it-works/index.md', 'Pure1 how it works')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Step 1: Phonehome — Purity OS sends telemetry to pure1.purestorage.com every 30 seconds')))
    lines.append(R(bMid(L, RR, 'Step 2: Ingest — Pure cloud stores metrics in time-series DB with full resolution')))
    lines.append(R(bMid(L, RR, 'Step 3: AI Analysis — ML models score health, identify workloads, forecast capacity')))
    lines.append(R(bMid(L, RR, 'Step 4: Alert — pre-failure condition or threshold breach triggers notification')))
    lines.append(R(bMid(L, RR, 'Step 5: Auto case — Pure1 opens TAC case with diagnostics before customer is aware')))
    lines.append(R(bMid(L, RR, 'Step 6: Resolution — Pure stages hardware, engineer resolves; customer notified')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Arrays push to Pure cloud every 30 sec · Pure TAC resolves proactively · no customer action'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Phonehome interval = 30 seconds; full metric telemetry at high resolution'))
    lines.append(txt_row('Pre-failure detection = Pure1 ML identifying component degradation before failure'))
    lines.append(txt_row('Auto case = Pure1 opening TAC support case automatically with diagnostic bundle'))
    lines.append(txt_row('Proactive swap = Pure staging replacement drive/module before customer impact'))
    lines.append(txt_row('Workload ID = Pure1 classifying IO pattern (random/sequential, read/write ratio)'))
    lines.append(txt_row('Capacity forecast = ML predicting array full date from consumption trend'))
    lines.append(txt_row('Health score = Composite array health from hardware, performance, and software inputs'))
    lines.append(txt_row('Threshold breach = Alert when metric crosses defined limit (utilisation, latency)'))
    lines.append(txt_row('TAC = Pure Storage Technical Assistance Centre; resolves proactive cases'))
    lines.append(txt_row('Diagnostic bundle = Phonehome data attached to auto-opened TAC case'))
    lines.append(txt_row('No customer action = Proactive support model aims for zero-touch resolution'))
    lines.append(txt_row('Evergreen = Subscription includes proactive support and hardware refresh rights'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-arch-design', 'docs/monitoring/pure1/architecture/design-standards/index.md', 'Pure1 design standards')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Registration Standards'), bMid(B2_L, B2_R, 'Operational Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'All arrays registered'), bMid(B2_L, B2_R, 'Email alerts active'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Phonehome verified'), bMid(B2_L, B2_R, 'Review weekly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TCP 443 unblocked'), bMid(B2_L, B2_R, 'Auto-case enabled'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service account'), bMid(B2_L, B2_R, 'Capacity plan monthly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tag by env+location'), bMid(B2_L, B2_R, 'Alert to ITSM'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('All arrays require TCP 443 outbound to pure1.purestorage.com · Pure handles the rest'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Phonehome verified = Array shows Connected in Pure1; data age < 2 minutes'))
    lines.append(txt_row('TCP 443 unblocked = Firewall allows outbound from array management IP to Pure cloud'))
    lines.append(txt_row('Service account = Dedicated Pure1 org user for API access; not personal login'))
    lines.append(txt_row('Tag = Pure1 metadata for grouping arrays by environment, location, and team'))
    lines.append(txt_row('Email alerts = Pure1 sending proactive alerts to ops-storage email list'))
    lines.append(txt_row('Auto-case = Pure1 automatically opening TAC case; must be enabled per org'))
    lines.append(txt_row('Weekly review = Review Pure1 fleet health and capacity outlooks every Monday'))
    lines.append(txt_row('Alert to ITSM = Pure1 webhook configured to forward proactive alerts to ServiceNow'))
    lines.append(txt_row('Capacity monthly = Monthly review of Pure1 forecasts; inform procurement planning'))
    lines.append(txt_row('Purity current = All arrays on current Purity release; Pure1 flags older versions'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-arch-int', 'docs/monitoring/pure1/architecture/integrations/index.md', 'Pure1 integrations')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Array Sources', 'Notification Targets'])))
    lines.append(R(sections(L, RR, [50], ['FlashArray//X (native phonehome)', 'Email: ops-storage@'])))
    lines.append(R(sections(L, RR, [50], ['FlashArray//C (native phonehome)', 'Webhook: ServiceNow/Slack'])))
    lines.append(R(sections(L, RR, [50], ['FlashBlade//S (native phonehome)', 'Pure1 REST API'])))
    lines.append(R(sections(L, RR, [50], ['FlashBlade//E (native phonehome)', 'Aria Ops Pure adapter'])))
    lines.append(R(sections(L, RR, [50], ['Pure Cloud Block Store', 'SIEM via syslog proxy'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Purity phonehome built-in · TCP 443 outbound from array · Pure cloud forwards alerts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Native phonehome = Purity OS built-in; no additional agent or gateway needed'))
    lines.append(txt_row('Pure Cloud Block Store = FlashArray in AWS/Azure; also connected to Pure1'))
    lines.append(txt_row('REST API = Pure1 API for fleet-wide metric retrieval and management'))
    lines.append(txt_row('Webhook = Pure1 outbound POST to webhook URL on proactive alert'))
    lines.append(txt_row('ServiceNow = Pure1 alert forwarded as incident via webhook'))
    lines.append(txt_row('Slack = Pure1 alert posted to storage team channel via webhook'))
    lines.append(txt_row('Aria Ops adapter = PAK file pulling Pure1/FlashArray metrics into VMware Aria Operations'))
    lines.append(txt_row('SIEM proxy = Script forwarding Pure1 API alerts to syslog for SIEM ingestion'))
    lines.append(txt_row('Pure1 API token = OAuth token for REST API; generated in Pure1 account settings'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-alerts', 'docs/monitoring/pure1/alerts/index.md', 'Pure1 alerts')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Alerts'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(sections(L, RR, [50], ['Alert Categories', 'Alert Actions'])))
    lines.append(R(sections(L, RR, [50], ['Pre-failure: component degraded', 'Acknowledge: mark seen'])))
    lines.append(R(sections(L, RR, [50], ['Capacity: fill < 90 days', 'Open TAC case'])))
    lines.append(R(sections(L, RR, [50], ['Performance: latency anomaly', 'Webhook to ITSM'])))
    lines.append(R(sections(L, RR, [50], ['Software: Purity event', 'Dismiss false positive'])))
    lines.append(R(sections(L, RR, [50], ['Connectivity: phonehome gap', 'Email to ops team'])))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Alerts generated in Pure cloud · delivered via Pure1 UI, email, webhook · TAC auto-case'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Pre-failure alert = Pure1 ML detecting component degradation before failure'))
    lines.append(txt_row('Capacity alert = Projected full date within 90 days at current growth rate'))
    lines.append(txt_row('Performance alert = Latency or IOPS anomaly detected by Pure1 ML'))
    lines.append(txt_row('Software alert = Purity OS event (firmware error, NVMe error, data reduction issue)'))
    lines.append(txt_row('Connectivity alert = Array phonehome not received for > 5 minutes'))
    lines.append(txt_row('TAC auto-case = Pure1 opening case with diagnostic bundle; assigned to engineer'))
    lines.append(txt_row('Acknowledge = Marks alert as seen; suppresses re-notification'))
    lines.append(txt_row('Dismiss = Close confirmed false-positive with comment'))
    lines.append(txt_row('Severity = Critical / Warning / Info; Critical triggers auto-case'))
    lines.append(txt_row('Proactive = Alert fires before customer notices impact; target of Pure1 model'))
    lines.append(txt_row('Webhook = HTTP POST from Pure1 to configured URL when alert fires'))
    lines.append(txt_row('Phonehome gap = Connectivity loss; array cannot reach pure1.purestorage.com'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-capacity', 'docs/monitoring/pure1/capacity/index.md', 'Pure1 capacity management')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Capacity Management'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity Overview'), bMid(B2_L, B2_R, 'Forecasting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Total raw capacity'), bMid(B2_L, B2_R, '30/60/90 day horizon'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Effective used %'), bMid(B2_L, B2_R, 'ML growth model'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Data reduction 1:X'), bMid(B2_L, B2_R, 'Projected full date'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Unique vs reduced'), bMid(B2_L, B2_R, 'Seasonal adjust'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snapshot space'), bMid(B2_L, B2_R, 'Capacity alert 90d'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Capacity metrics from Purity OS via phonehome · Pure1 processes and forecasts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Effective capacity = Usable capacity after RAID; starting point for data placement'))
    lines.append(txt_row('Data reduction = Combined dedup + compression ratio (e.g., 3.5:1)'))
    lines.append(txt_row('Unique data = Data before dedup; actual bytes written by hosts'))
    lines.append(txt_row('Reduced data = Physical footprint after dedup and compression'))
    lines.append(txt_row('Snapshot space = Physical space used by snapshots; tracked separately'))
    lines.append(txt_row('Projected full date = ML forecast of when effective capacity will be exhausted'))
    lines.append(txt_row('30/60/90 day = Default forecast horizons; Pure1 alerts at < 90 days'))
    lines.append(txt_row('Seasonal adjust = ML accounting for periodic usage spikes in forecast'))
    lines.append(txt_row('Capacity alert = Pure1 alert + TAC case when horizon < 90 days'))
    lines.append(txt_row('Evergreen refresh = Capacity expansion via Pure subscription hardware refresh'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-cli', 'docs/monitoring/pure1/cli-reference/index.md', 'Pure1 CLI and API reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — CLI and API Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Pure1 REST API — Base URL: https://api.pure1.purestorage.com/api/1.latest')))
    lines.append(R(bMid(L, RR, 'Auth: POST /oauth2/1.0/token (client_id + private_key JWT) → Bearer token')))
    lines.append(R(bMid(L, RR, 'Arrays: GET /arrays — list all registered arrays with model, version, health')))
    lines.append(R(bMid(L, RR, 'Metrics: GET /metrics?names=array_total_capacity&resource_names=<array>')))
    lines.append(R(bMid(L, RR, 'Alerts: GET /alerts?filter=state=\'open\' — active alerts across fleet')))
    lines.append(R(bMid(L, RR, 'Fleet health: GET /arrays?fields=name,model,os,version,health')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Pure1 API at api.pure1.purestorage.com · client runs from any internet-connected host'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Pure1 REST API = Programmatic access to fleet-wide metrics and alert data'))
    lines.append(txt_row('JWT auth = JSON Web Token signed with RSA private key for API authentication'))
    lines.append(txt_row('client_id = Application ID registered in Pure1 > API Registration'))
    lines.append(txt_row('Bearer token = Short-lived (10 min) OAuth2 token; refresh before expiry'))
    lines.append(txt_row('arrays endpoint = Returns all arrays with model, Purity version, and health score'))
    lines.append(txt_row('metrics endpoint = Time-series metric retrieval; supports multiple arrays and metrics'))
    lines.append(txt_row('alerts endpoint = Returns active alerts; filter by state, severity, or array'))
    lines.append(txt_row('resource_names = Array name filter for metric queries'))
    lines.append(txt_row('fields param = Projection; return only needed fields to reduce payload size'))
    lines.append(txt_row('Pagination = Pure1 API uses continuation_token for large result sets'))
    lines.append(txt_row('Rate limit = API enforces per-client limits; exponential backoff on 429'))
    lines.append(txt_row('py-pure-client = Pure-provided Python library wrapping Pure1 API'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-design', 'docs/monitoring/pure1/design-standards/index.md', 'Pure1 design standards')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Registration Standards'), bMid(B2_L, B2_R, 'Alert Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'All arrays in Pure1'), bMid(B2_L, B2_R, 'Email ops-storage@'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Phonehome verified'), bMid(B2_L, B2_R, 'ITSM webhook set'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TCP 443 open outbound'), bMid(B2_L, B2_R, 'Auto-case enabled'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tag env + location'), bMid(B2_L, B2_R, 'Review weekly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service account API'), bMid(B2_L, B2_R, 'Capacity plan monthly'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('All FlashArrays and FlashBlades on TCP 443 to pure1.purestorage.com'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Phonehome verified = Array shows Connected; data age < 2 min in Pure1 UI'))
    lines.append(txt_row('ITSM webhook = Pure1 webhook configured to create ServiceNow incident on alert'))
    lines.append(txt_row('Auto-case enabled = Pure1 setting allowing automatic TAC case opening'))
    lines.append(txt_row('Tag = Pure1 org labels by env (prod/dev), location (dc1/dc2), and team'))
    lines.append(txt_row('Service account = Non-personal Pure1 account for API registration'))
    lines.append(txt_row('Weekly review = Review Pure1 fleet health and open proactive alerts every Monday'))
    lines.append(txt_row('Capacity monthly = Monthly export of Pure1 forecast data for procurement planning'))
    lines.append(txt_row('Purity current = All arrays on supported Purity release; Pure1 flags end-of-life'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-health', 'docs/monitoring/pure1/health/index.md', 'Pure1 health monitoring')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Health Monitoring'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Pure1 Health: continuous monitoring of array hardware, software, and performance')))
    lines.append(R(bMid(L, RR, 'Component inputs: drives, controllers, power supplies, fans, network, Purity events')))
    lines.append(R(bMid(L, RR, 'Health score: OK / Degraded / Unhealthy per array based on component state')))
    lines.append(R(bMid(L, RR, 'Fleet view: all arrays ranked by health; filter by tag, model, or location')))
    lines.append(R(bMid(L, RR, 'Drill-down: click array to see component-level detail and active alerts')))
    lines.append(R(bMid(L, RR, '30-day history: health trend; identify recurring degraded periods')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Health from Purity OS via phonehome · Pure cloud ML processes · UI updated every 2 min'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Health score = OK (all green) / Degraded (non-critical fault) / Unhealthy (critical)'))
    lines.append(txt_row('Fleet view = Pure1 UI showing all arrays ordered by health state'))
    lines.append(txt_row('Drill-down = Clicking array opens component view: drives, controllers, shelves'))
    lines.append(txt_row('Unhealthy = Critical component failure; TAC case auto-opened if enabled'))
    lines.append(txt_row('Degraded = Non-critical fault (e.g., single drive pre-failure); warning state'))
    lines.append(txt_row('OK = All components healthy; no active alerts'))
    lines.append(txt_row('30-day history = Pure1 stores health state over time; shows trend per array'))
    lines.append(txt_row('Component = Physical part: drive, DIMM, NIC, controller, power supply, fan'))
    lines.append(txt_row('Purity event = Software-level error logged by array OS; contributes to health'))
    lines.append(txt_row('Pre-failure = Pure1 ML detecting imminent component failure before it occurs'))
    lines.append(txt_row('Phonehome = Array sending hardware sensor data to Pure cloud every 30 seconds'))
    lines.append(txt_row('Proactive swap = Pure staging replacement and dispatching before customer impact'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-integration', 'docs/monitoring/pure1/integration/index.md', 'Pure1 integration guide')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Integration Guide'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ITSM Integration'), bMid(B2_L, B2_R, 'Monitoring Stack'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ServiceNow webhook'), bMid(B2_L, B2_R, 'Aria Ops PAK'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Auto-incident'), bMid(B2_L, B2_R, 'Grafana panels'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PagerDuty events'), bMid(B2_L, B2_R, 'Splunk HEC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Slack webhook'), bMid(B2_L, B2_R, 'Custom REST script'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Email alerts'), bMid(B2_L, B2_R, 'py-pure-client'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Pure1 in cloud · webhooks outbound to ITSM SaaS · REST API for on-prem consumers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ServiceNow webhook = Pure1 POST to ServiceNow event endpoint on proactive alert'))
    lines.append(txt_row('Auto-incident = ServiceNow incident created from Pure1 alert payload'))
    lines.append(txt_row('PagerDuty = On-call routing; Pure1 webhook delivers to PagerDuty Events API v2'))
    lines.append(txt_row('Slack webhook = Pure1 proactive alert posted to storage channel'))
    lines.append(txt_row('Aria Ops PAK = VMware adapter pulling FlashArray/FlashBlade metrics into Aria Ops'))
    lines.append(txt_row('Grafana panels = Pure1 REST API proxied as Grafana data source'))
    lines.append(txt_row('Splunk HEC = Pure1 alerts forwarded as events to Splunk for SIEM correlation'))
    lines.append(txt_row('py-pure-client = Pure-provided Python library for Pure1 and Purity REST APIs'))
    lines.append(txt_row('Custom REST script = Polling Pure1 API and pushing to proprietary dashboard/tooling'))
    lines.append(txt_row('Email = Pure1 SMTP notification for proactive alerts; configure in org settings'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-lifecycle', 'docs/monitoring/pure1/lifecycle/index.md', 'Pure1 lifecycle management')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Lifecycle Management'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Onboarding'), bMid(B2_L, B2_R, 'Ongoing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Activate Pure1 org'), bMid(B2_L, B2_R, 'Monitor phonehome'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Add arrays via SN'), bMid(B2_L, B2_R, 'Keep Purity current'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Enable phonehome'), bMid(B2_L, B2_R, 'Renew Evergreen sub'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Configure alerts'), bMid(B2_L, B2_R, 'Rotate API tokens'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Set up webhooks'), bMid(B2_L, B2_R, 'Annual access review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Pure1 is SaaS — no on-prem component to maintain · Purity upgrades handled by ops team'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Pure1 org = Customer organisation in Pure1; all arrays grouped under one org'))
    lines.append(txt_row('Activate = Creating Pure1 org via Pure portal using Evergreen contract'))
    lines.append(txt_row('Add arrays via SN = Arrays register to Pure1 using serial number + phonehome'))
    lines.append(txt_row('Enable phonehome = purearray setattr --phonehome enabled on FlashArray'))
    lines.append(txt_row('Purity current = Keep array OS on supported release; Pure1 tracks versions'))
    lines.append(txt_row('Evergreen subscription = Annual renewal; includes Pure1, support, and hardware refresh'))
    lines.append(txt_row('Rotate API tokens = Pure1 API tokens have no expiry; rotate annually per policy'))
    lines.append(txt_row('Access review = Yearly audit of Pure1 org users; remove departed staff'))
    lines.append(txt_row('Monitor phonehome = Daily check that all arrays show Connected in Pure1'))
    lines.append(txt_row('SaaS = Pure1 platform updated by Pure Storage; no customer upgrade action'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-ops', 'docs/monitoring/pure1/operations/index.md', 'Pure1 operations')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Operations'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Daily'), bMid(B2_L, B2_R, 'Weekly'), bMid(B3_L, B3_R, 'Monthly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check fleet health'), bMid(B2_L, B2_R, 'Review open alerts'), bMid(B3_L, B3_R, 'Capacity planning'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Phonehome status'), bMid(B2_L, B2_R, 'Review forecasts'), bMid(B3_L, B3_R, 'Purity versions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Active alerts'), bMid(B2_L, B2_R, 'Update ITSM'), bMid(B3_L, B3_R, 'Access review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TAC case status'), bMid(B2_L, B2_R, 'Performance check'), bMid(B3_L, B3_R, 'Report to mgmt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Degraded arrays'), bMid(B2_L, B2_R, 'Dismiss false pos'), bMid(B3_L, B3_R, 'Evergreen plan'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Operations entirely via pure1.purestorage.com browser UI · REST API for automation'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Fleet health = Overview showing all arrays with OK/Degraded/Unhealthy status'))
    lines.append(txt_row('Phonehome status = Confirming Connected for all arrays; data age < 2 minutes'))
    lines.append(txt_row('Active alerts = Open proactive alerts requiring acknowledgement or ITSM action'))
    lines.append(txt_row('TAC case status = Checking open Pure Storage support cases in Pure1'))
    lines.append(txt_row('Degraded array = Array with non-critical fault; plan remediation within SLA'))
    lines.append(txt_row('Forecast review = Weekly check of capacity projections; flag < 90 day arrays'))
    lines.append(txt_row('Performance check = Weekly review of latency/IOPS trends for workload health'))
    lines.append(txt_row('Purity versions = Monthly audit; arrays running EOS Purity should be scheduled for upgrade'))
    lines.append(txt_row('Evergreen plan = Monthly review of subscription expiry dates for renewal planning'))
    lines.append(txt_row('Access review = Monthly audit of Pure1 user list; remove stale accounts'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-performance', 'docs/monitoring/pure1/performance/index.md', 'Pure1 performance analysis')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Performance Analysis'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Performance Metrics'), bMid(B2_L, B2_R, 'Workload Intelligence'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'IOPS read/write'), bMid(B2_L, B2_R, 'Workload ID (AI)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Latency p50/p99'), bMid(B2_L, B2_R, 'IO size profile'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bandwidth MB/s'), bMid(B2_L, B2_R, 'Read/write ratio'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Queue depth'), bMid(B2_L, B2_R, 'Fleet benchmark'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Per-volume stats'), bMid(B2_L, B2_R, 'Custom time range'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Metrics from Purity OS via phonehome · Pure1 aggregates and visualises'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('IOPS = Input/Output Operations per Second; primary performance metric'))
    lines.append(txt_row('p50 latency = Median latency; 50% of operations faster than this value'))
    lines.append(txt_row('p99 latency = 99th percentile; 1% of operations slower; shows tail latency'))
    lines.append(txt_row('Bandwidth = Throughput in MB/s; saturates at network limit before IOPS typically'))
    lines.append(txt_row('Queue depth = Outstanding IO requests; high queue depth may indicate saturation'))
    lines.append(txt_row('Per-volume = Pure1 showing IOPS/latency per volume for workload isolation'))
    lines.append(txt_row('Workload ID = Pure1 AI classifying application type from IO signature'))
    lines.append(txt_row('IO size = Average IO request size in KB; small random vs large sequential'))
    lines.append(txt_row('Read/write ratio = Proportion of reads vs writes; impacts cache effectiveness'))
    lines.append(txt_row('Fleet benchmark = Pure1 comparing array performance to anonymised peer group'))
    lines.append(txt_row('Custom range = Pure1 UI allows selecting arbitrary time window for analysis'))
    lines.append(txt_row('Anomaly = Pure1 ML detecting performance deviation from established baseline'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-scripts', 'docs/monitoring/pure1/scripts/index.md', 'Pure1 scripts reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Scripts Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Pure1 REST API scripts using py-pure-client library')))
    lines.append(R(bMid(L, RR, 'get-fleet.py: list all arrays with health, version, and capacity')))
    lines.append(R(bMid(L, RR, 'get-alerts.py: active alerts across fleet; flag Critical to Slack')))
    lines.append(R(bMid(L, RR, 'capacity-check.py: arrays with < 90 days to full; email to team')))
    lines.append(R(bMid(L, RR, 'phonehome-check.py: arrays not Connected; alert if data age > 5 min')))
    lines.append(R(bMid(L, RR, 'perf-report.py: pull IOPS/latency for all arrays; CSV export')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Scripts run from any internet-connected host · Python 3 + py-pure-client'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('py-pure-client = pip install py-pure-client; Pure-provided Python library'))
    lines.append(txt_row('JWT auth = RSA-signed JWT for Pure1 API; use Pure1Client from py-pure-client'))
    lines.append(txt_row('client_id = Pure1 API registration ID from org settings'))
    lines.append(txt_row('private_key = RSA private key path; corresponding public key registered in Pure1'))
    lines.append(txt_row('Fleet list = client.get_arrays() returns all arrays with health and metadata'))
    lines.append(txt_row('Alert list = client.get_alerts(filter="state=\'open\'") for active alerts'))
    lines.append(txt_row('Metrics = client.get_metrics(names=[...], resource_names=[...]) for time-series'))
    lines.append(txt_row('Phonehome status = array.status field; Connected or Disconnected'))
    lines.append(txt_row('Data age = time since last phonehome; compute from array.last_updated'))
    lines.append(txt_row('CSV export = pandas DataFrame from metric response; df.to_csv()'))
    lines.append(txt_row('Cron = Schedule daily via crontab for capacity and phonehome checks'))
    lines.append(txt_row('Slack webhook = POST alert summary to Slack channel incoming webhook URL'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-security', 'docs/monitoring/pure1/security/index.md', 'Pure1 security')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Security'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access Control'), bMid(B2_L, B2_R, 'Data Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSO / local account'), bMid(B2_L, B2_R, 'TLS 1.2 phonehome'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA on Pure1 login'), bMid(B2_L, B2_R, 'Encrypted at rest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC: Admin/Viewer'), bMid(B2_L, B2_R, 'Telemetry only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'API RSA key auth'), bMid(B2_L, B2_R, 'No data access'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Annual access review'), bMid(B2_L, B2_R, 'SOC2 Type II'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Data in Pure cloud datacentres · tenant isolation · SOC2 Type II · no customer data'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SSO = Single Sign-On; Pure1 supports SAML 2.0 for corporate IdP integration'))
    lines.append(txt_row('MFA = Multi-factor authentication for Pure1 UI login'))
    lines.append(txt_row('RBAC = Admin (full) vs Viewer (read-only) per Pure1 org'))
    lines.append(txt_row('RSA key auth = Pure1 API uses RSA-signed JWT; no shared secret'))
    lines.append(txt_row('TLS 1.2 = Phonehome and API connections encrypted in transit'))
    lines.append(txt_row('Telemetry only = Pure1 receives metrics and events; no customer data or files'))
    lines.append(txt_row('No data access = Pure Storage cannot access stored customer data via Pure1'))
    lines.append(txt_row('Encrypted at rest = Telemetry data encrypted in Pure cloud storage'))
    lines.append(txt_row('SOC2 Type II = Pure Storage annual security audit; covers data handling'))
    lines.append(txt_row('Tenant isolation = Each customer org data separated in multi-tenant cloud'))
    lines.append(txt_row('Annual review = Yearly audit of Pure1 users; remove stale accounts and roles'))
    lines.append(txt_row('API key rotation = RSA key pair rotated annually per security policy'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-support', 'docs/monitoring/pure1/support/index.md', 'Pure1 support integration')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Support Integration'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Pure1 Support: proactive TAC case creation and remote diagnostics')))
    lines.append(R(bMid(L, RR, 'Auto-case: Pure1 ML opens TAC case before customer notices failure')))
    lines.append(R(bMid(L, RR, 'Case includes: diagnostic bundle, array serial, failure signature, priority')))
    lines.append(R(bMid(L, RR, 'Remote assist: Pure engineer connects to array via encrypted Pure1 tunnel')))
    lines.append(R(bMid(L, RR, 'Proactive swap: replacement hardware staged before failure occurs')))
    lines.append(R(bMid(L, RR, 'View cases: pure1.purestorage.com > Support > Cases')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Cases opened in Pure cloud · engineer accesses array via Pure1 secure tunnel'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Auto-case = Pure1 opening TAC case automatically on pre-failure detection'))
    lines.append(txt_row('Diagnostic bundle = Phonehome data + Purity log snapshot attached to case'))
    lines.append(txt_row('Remote assist = Pure engineer SSH-ing to array through Pure1 encrypted tunnel'))
    lines.append(txt_row('Proactive swap = Pure dispatching replacement drive/module before failure'))
    lines.append(txt_row('Case priority = Sev-1 for pre-failure; Sev-2 for degraded; Sev-3 for advisory'))
    lines.append(txt_row('Encrypted tunnel = Pure1 remote access over customer-approved secure channel'))
    lines.append(txt_row('Customer approval = Remote access requires explicit opt-in per session'))
    lines.append(txt_row('TAC = Pure Storage Technical Assistance Centre; 24x7 for Sev-1'))
    lines.append(txt_row('Case view = All open and historical cases visible in Pure1 Support portal'))
    lines.append(txt_row('Manual case = Open at support.purestorage.com if auto-case not triggered'))
    lines.append(txt_row('Evergreen = All-inclusive support model; no per-incident charges'))
    lines.append(txt_row('Phonehome = Required for auto-case and remote assist; must be enabled and connected'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-troubleshooting', 'docs/monitoring/pure1/troubleshooting/index.md', 'Pure1 troubleshooting')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Phonehome Issues'), bMid(B2_L, B2_R, 'Alert / Data Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check TCP 443 outbound'), bMid(B2_L, B2_R, 'Verify array status'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify DNS resolution'), bMid(B2_L, B2_R, 'Check data age'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'purearray setattr show'), bMid(B2_L, B2_R, 'Check alert config'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Re-enable phonehome'), bMid(B2_L, B2_R, 'Test webhook delivery'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check proxy settings'), bMid(B2_L, B2_R, 'Open TAC case'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Troubleshoot from array CLI (purearray) and pure1.purestorage.com UI'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Disconnected = Array shows Disconnected in Pure1; phonehome not received > 5 min'))
    lines.append(txt_row('TCP 443 test = From array: curl -s https://pure1.purestorage.com >/dev/null; check rc'))
    lines.append(txt_row('DNS resolution = Array must resolve pure1.purestorage.com; check array DNS settings'))
    lines.append(txt_row('purearray setattr show = View phonehome enabled/disabled state on FlashArray'))
    lines.append(txt_row('Re-enable phonehome = purearray setattr --phonehome true on FlashArray CLI'))
    lines.append(txt_row('Proxy settings = purearray setattr --proxy http://proxy:port if array uses proxy'))
    lines.append(txt_row('Data age = Time since last phonehome; check in Pure1 > array detail'))
    lines.append(txt_row('Alert config = Verify email and webhook targets in Pure1 > Admin > Notifications'))
    lines.append(txt_row('Webhook test = Pure1 UI has a test button; verify delivery to endpoint'))
    lines.append(txt_row('TAC case = support.purestorage.com; include array serial and phonehome status'))
    lines.append(txt_row('FlashBlade phonehome = pureauthapp setattr --phonehome true on FlashBlade CLI'))
    lines.append(txt_row('Firewall rule = Allow outbound TCP 443 from array mgmt IP to pure1.purestorage.com'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('monitoring-pure1-vendor', 'docs/monitoring/pure1/vendor-support/index.md', 'Pure1 vendor support')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — Vendor Support'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Support Model — Pure Storage Evergreen All-Inclusive')))
    lines.append(R(bMid(L, RR, 'Pure1 included with every FlashArray and FlashBlade Evergreen subscription')))
    lines.append(R(bMid(L, RR, 'Auto-cases opened by Pure1 before customer impact; no action required')))
    lines.append(R(bMid(L, RR, 'Manual case: support.purestorage.com — 24x7 for Sev-1 production issues')))
    lines.append(R(bMid(L, RR, 'Pure1 API support: developer.purestorage.com for API documentation')))
    lines.append(R(bMid(L, RR, 'Community: community.purestorage.com — forums, code, and best practices')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Pure cloud hosted · support portal at support.purestorage.com · 24x7 for Sev-1'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Evergreen = All-inclusive subscription: support, upgrades, and hardware refresh'))
    lines.append(txt_row('All-inclusive = No per-incident charges; unlimited cases with Evergreen'))
    lines.append(txt_row('Auto-case = Pure1 ML opening case proactively; target is zero-touch resolution'))
    lines.append(txt_row('Severity 1 = Production array down or data unavailable; 24x7 phone response'))
    lines.append(txt_row('Severity 2 = Performance degraded or component failed; 4-hour response'))
    lines.append(txt_row('Severity 3 = Non-critical advisory; best-effort response'))
    lines.append(txt_row('developer.purestorage.com = API documentation and py-pure-client reference'))
    lines.append(txt_row('Community = Pure Storage user community; code exchange and troubleshooting tips'))
    lines.append(txt_row('Pure1 feedback = Feedback link in Pure1 UI for feature requests'))
    lines.append(txt_row('TAM = Technical Account Manager; proactive guidance for large Pure fleets'))
    lines.append(txt_row('Remote assist = Pure engineer accessing array via Pure1 secure tunnel for support'))
    lines.append(txt_row('Evergreen expiry = Subscription renewal required; Pure1 access may lapse if expired'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
