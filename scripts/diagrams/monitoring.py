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

# ── Aria Operations remaining pages ──────────────────────────────────────────

W2 = 103

# ── CloudIQ diagrams ──────────────────────────────────────────────────────────

# ── Dell AIOps diagrams ───────────────────────────────────────────────────────

@kb_diagram('monitoring-dell-aiops', 'docs/storage/dell/dell-aiops/index.md', 'Dell AIOps — AI-driven infrastructure observability')
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


@kb_diagram('monitoring-dell-aiops-arch-how', 'docs/storage/dell/dell-aiops/architecture/how-it-works/index.md', 'Dell AIOps how it works')
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


@kb_diagram('monitoring-dell-aiops-arch-design', 'docs/storage/dell/dell-aiops/architecture/design-standards/index.md', 'Dell AIOps design standards')
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


@kb_diagram('monitoring-dell-aiops-arch-int', 'docs/storage/dell/dell-aiops/architecture/integrations/index.md', 'Dell AIOps integrations')
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


@kb_diagram('monitoring-dell-aiops-alerts', 'docs/storage/dell/dell-aiops/alerts/index.md', 'Dell AIOps alerts')
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


@kb_diagram('monitoring-dell-aiops-cli', 'docs/storage/dell/dell-aiops/cli-reference/index.md', 'Dell AIOps CLI and API reference')
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


@kb_diagram('monitoring-dell-aiops-design', 'docs/storage/dell/dell-aiops/design-standards/index.md', 'Dell AIOps design standards top-level')
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


@kb_diagram('monitoring-dell-aiops-insights', 'docs/storage/dell/dell-aiops/insights/index.md', 'Dell AIOps insights')
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


@kb_diagram('monitoring-dell-aiops-integration', 'docs/storage/dell/dell-aiops/integration/index.md', 'Dell AIOps integration guide')
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


@kb_diagram('monitoring-dell-aiops-lifecycle', 'docs/storage/dell/dell-aiops/lifecycle/index.md', 'Dell AIOps lifecycle')
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


@kb_diagram('monitoring-dell-aiops-ops', 'docs/storage/dell/dell-aiops/operations/index.md', 'Dell AIOps operations')
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


@kb_diagram('monitoring-dell-aiops-recommendations', 'docs/storage/dell/dell-aiops/recommendations/index.md', 'Dell AIOps recommendations')
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


@kb_diagram('monitoring-dell-aiops-reporting', 'docs/storage/dell/dell-aiops/reporting/index.md', 'Dell AIOps reporting')
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


@kb_diagram('monitoring-dell-aiops-scripts', 'docs/storage/dell/dell-aiops/scripts/index.md', 'Dell AIOps scripts reference')
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


@kb_diagram('monitoring-dell-aiops-security', 'docs/storage/dell/dell-aiops/security/index.md', 'Dell AIOps security')
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


@kb_diagram('monitoring-dell-aiops-troubleshooting', 'docs/storage/dell/dell-aiops/troubleshooting/index.md', 'Dell AIOps troubleshooting')
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


@kb_diagram('monitoring-dell-aiops-vendor', 'docs/storage/dell/dell-aiops/vendor-support/index.md', 'Dell AIOps vendor support')
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

@kb_diagram('monitoring-insightiq', 'docs/storage/netapp/insightiq/index.md', 'InsightIQ — PowerScale performance reporting')
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


@kb_diagram('monitoring-insightiq-arch-how', 'docs/storage/netapp/insightiq/architecture/how-it-works/index.md', 'InsightIQ how it works')
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


@kb_diagram('monitoring-insightiq-arch-design', 'docs/storage/netapp/insightiq/architecture/design-standards/index.md', 'InsightIQ design standards')
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


@kb_diagram('monitoring-insightiq-arch-int', 'docs/storage/netapp/insightiq/architecture/integrations/index.md', 'InsightIQ integrations')
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


@kb_diagram('monitoring-insightiq-capacity', 'docs/storage/netapp/insightiq/capacity/index.md', 'InsightIQ capacity management')
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


@kb_diagram('monitoring-insightiq-cli', 'docs/storage/netapp/insightiq/cli-reference/index.md', 'InsightIQ CLI reference')
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


@kb_diagram('monitoring-insightiq-design', 'docs/storage/netapp/insightiq/design-standards/index.md', 'InsightIQ design standards top-level')
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


@kb_diagram('monitoring-insightiq-integration', 'docs/storage/netapp/insightiq/integration/index.md', 'InsightIQ integration guide')
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


@kb_diagram('monitoring-insightiq-lifecycle', 'docs/storage/netapp/insightiq/lifecycle/index.md', 'InsightIQ lifecycle management')
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


@kb_diagram('monitoring-insightiq-ops', 'docs/storage/netapp/insightiq/operations/index.md', 'InsightIQ operations')
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


@kb_diagram('monitoring-insightiq-performance', 'docs/storage/netapp/insightiq/performance/index.md', 'InsightIQ performance analysis')
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


@kb_diagram('monitoring-insightiq-reports', 'docs/storage/netapp/insightiq/reports/index.md', 'InsightIQ reports')
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


@kb_diagram('monitoring-insightiq-scripts', 'docs/storage/netapp/insightiq/scripts/index.md', 'InsightIQ scripts reference')
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


@kb_diagram('monitoring-insightiq-security', 'docs/storage/netapp/insightiq/security/index.md', 'InsightIQ security')
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


@kb_diagram('monitoring-insightiq-troubleshooting', 'docs/storage/netapp/insightiq/troubleshooting/index.md', 'InsightIQ troubleshooting')
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


@kb_diagram('monitoring-insightiq-vendor', 'docs/storage/netapp/insightiq/vendor-support/index.md', 'InsightIQ vendor support')
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


@kb_diagram('monitoring-insightiq-workloads', 'docs/storage/netapp/insightiq/workloads/index.md', 'InsightIQ workload analysis')
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

# ── Pure1 diagrams ────────────────────────────────────────────────────────────

@kb_diagram('monitoring-pure1', 'docs/storage/pure/pure1/index.md', 'Pure1 — Pure Storage cloud management and analytics')
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


@kb_diagram('monitoring-pure1-arch-how', 'docs/storage/pure/pure1/architecture/how-it-works/index.md', 'Pure1 how it works')
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


@kb_diagram('monitoring-pure1-arch-design', 'docs/storage/pure/pure1/architecture/design-standards/index.md', 'Pure1 design standards')
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


@kb_diagram('monitoring-pure1-arch-int', 'docs/storage/pure/pure1/architecture/integrations/index.md', 'Pure1 integrations')
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


@kb_diagram('monitoring-pure1-alerts', 'docs/storage/pure/pure1/alerts/index.md', 'Pure1 alerts')
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


@kb_diagram('monitoring-pure1-capacity', 'docs/storage/pure/pure1/capacity/index.md', 'Pure1 capacity management')
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


@kb_diagram('monitoring-pure1-cli', 'docs/storage/pure/pure1/cli-reference/index.md', 'Pure1 CLI and API reference')
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


@kb_diagram('monitoring-pure1-design', 'docs/storage/pure/pure1/design-standards/index.md', 'Pure1 design standards')
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


@kb_diagram('monitoring-pure1-health', 'docs/storage/pure/pure1/health/index.md', 'Pure1 health monitoring')
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


@kb_diagram('monitoring-pure1-integration', 'docs/storage/pure/pure1/integration/index.md', 'Pure1 integration guide')
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


@kb_diagram('monitoring-pure1-lifecycle', 'docs/storage/pure/pure1/lifecycle/index.md', 'Pure1 lifecycle management')
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


@kb_diagram('monitoring-pure1-ops', 'docs/storage/pure/pure1/operations/index.md', 'Pure1 operations')
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


@kb_diagram('monitoring-pure1-performance', 'docs/storage/pure/pure1/performance/index.md', 'Pure1 performance analysis')
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


@kb_diagram('monitoring-pure1-scripts', 'docs/storage/pure/pure1/scripts/index.md', 'Pure1 scripts reference')
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


@kb_diagram('monitoring-pure1-security', 'docs/storage/pure/pure1/security/index.md', 'Pure1 security')
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


@kb_diagram('monitoring-pure1-support', 'docs/storage/pure/pure1/support/index.md', 'Pure1 support integration')
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


@kb_diagram('monitoring-pure1-troubleshooting', 'docs/storage/pure/pure1/troubleshooting/index.md', 'Pure1 troubleshooting')
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


@kb_diagram('monitoring-pure1-vendor', 'docs/storage/pure/pure1/vendor-support/index.md', 'Pure1 vendor support')
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
