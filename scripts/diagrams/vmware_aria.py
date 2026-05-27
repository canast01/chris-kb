"""
VMware Aria Suite diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

@kb_diagram(
    'aria-automation',
    'docs/virtualization/vmware/aria-automation/index.md',
    'Aria Automation Stack — blueprints, CAS, ABX, service catalogue, approval policies',
)
def aria_automation_stack():
    """Aria Automation (vRealize Automation) Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Automation Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Automation — Infrastructure Automation and Service Catalogue')))
    lines.append(R(bMid(IV_L, IV_R, 'Blueprints (templates): IaC definitions for VMs, networks, storage, and cloud resources')))
    lines.append(R(bMid(IV_L, IV_R, 'Service Catalogue: self-service portal for end-users to request approved deployments')))
    lines.append(R(bMid(IV_L, IV_R, 'CAS: Cloud Assembly; where blueprints are designed and cloud accounts connected')))
    lines.append(R(bMid(IV_L, IV_R, 'ABX: Action-Based eXtensibility; serverless functions triggered on deployment events')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Blueprints define desired state · Service Catalogue delivers self-service · ABX extends automation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CAS: cloud accounts'),
        bMid(B2_L, B2_R, 'Blueprint: design+version'),
        bMid(B3_L, B3_R, 'RBAC: org + project roles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ABX: serverless actions'),
        bMid(B2_L, B2_R, 'Deployment: manage+delete'),
        bMid(B3_L, B3_R, 'Approval policies: gated'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service Broker: catalogue'),
        bMid(B2_L, B2_R, 'Cloud account: sync'),
        bMid(B3_L, B3_R, 'Secrets: integrated vault'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pipelines: CI/CD IaC'),
        bMid(B2_L, B2_R, 'Content source: Git/vRO'),
        bMid(B3_L, B3_R, 'Content trust: signed'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Terraform: IaC provider'),
        bMid(B2_L, B2_R, 'Approval: request+grant'),
        bMid(B3_L, B3_R, 'Audit: deployment log'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the platform · Operations manage deployments'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Deployment fails', 'vra-support bundle', 'Services: running?', 'GSS + bundle', 'vra-cli login'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Approval not firin', 'cloud-account sync', 'Cloud acct: sync OK', 'TAM escalation', 'vra-cli get deploy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Blueprint error', 'ABX action logs', 'ABX: runtime OK?', 'Collect service lo', 'vra-cli get bluepr'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Catalogue empty', 'content-source syn', 'Catalogue: publish?', 'P1: automation dow', 'vra-cli get reques'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Aria Automation VMs on vSphere cluster · vPostgres DB · NSX network segments · Aria Suite LCM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Blueprint     = YAML IaC template defining VMs, networks, storage, and cloud resources'))
    lines.append(txt_row('CAS           = Cloud Assembly; blueprint designer and cloud account manager in Aria Automation'))
    lines.append(txt_row('ABX           = Action-Based eXtensibility; serverless functions (Python/JS/PS) on deploy events'))
    lines.append(txt_row('Service Broker= Catalogue front-end; users request approved items from published content sources'))
    lines.append(txt_row('Deployment    = Running instance of a blueprint; tracks provisioned resources and lifecycle'))
    lines.append(txt_row('Cloud Account = vSphere, AWS, Azure, or GCP connection supplying infrastructure endpoints'))
    lines.append(txt_row('Project       = RBAC boundary; groups users and cloud zones; controls blueprint deployment targets'))
    lines.append(txt_row('Content Source= Git repo or vRO connection feeding blueprint content into Service Catalogue'))
    lines.append(txt_row('Approval Policy= Workflow gate before deployment; requires named approver or group sign-off'))
    lines.append(txt_row('vRO           = vRealize Orchestrator; workflow engine integrated with Aria Automation'))
    lines.append(txt_row('Pipeline      = CI/CD pipeline in Aria Automation Pipelines; integrates Git, test, and deploy'))
    lines.append(txt_row('Terraform provider= Aria Automation Terraform service; manages Terraform state and runs plans'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-operations',
    'docs/virtualization/vmware/aria-operations/index.md',
    'Aria Operations Stack — analytics cluster, adapters, management packs, rightsizing',
)
def aria_operations_stack():
    """Aria Operations (vRealize Operations) Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations (vROps) Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Operations — Performance, Capacity, and Compliance Management')))
    lines.append(R(bMid(IV_L, IV_R, 'Analytics cluster: master + replica + data nodes collect and correlate all metrics')))
    lines.append(R(bMid(IV_L, IV_R, 'Adapters: vSphere, vSAN, NSX, AWS, Azure, storage — each adds metric collection')))
    lines.append(R(bMid(IV_L, IV_R, 'Policies: alert thresholds, capacity model, workload placement, compliance benchmark')))
    lines.append(R(bMid(IV_L, IV_R, 'Rightsizing: reclaim wasted CPU/RAM; workload heatmaps; capacity forecasting')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Adapters collect metrics · analytics engine correlates · policies alert and guide optimisation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Analytics: master+data'),
        bMid(B2_L, B2_R, 'Alert: configure+action'),
        bMid(B3_L, B3_R, 'RBAC: user + role mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Adapters: vSphere/NSX/S3'),
        bMid(B2_L, B2_R, 'Rightsizing: reclaim'),
        bMid(B3_L, B3_R, 'SSO: AD/vCenter login'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Management packs: extend'),
        bMid(B2_L, B2_R, 'Capacity: forecast+what-if'),
        bMid(B3_L, B3_R, 'Compliance: benchmark'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Policies: alert + capacity'),
        bMid(B2_L, B2_R, 'Dashboard: build+share'),
        bMid(B3_L, B3_R, 'TLS: cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Remote collector: scale'),
        bMid(B2_L, B2_R, 'Report: schedule+export'),
        bMid(B3_L, B3_R, 'Audit log: user actions'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture scales collection · Operations optimise the environment · Security controls access'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Adapter not coll.', 'vrops-support bund', 'Analytics: online?', 'GSS + bundle', 'vrops-cli cluster'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert storm: noise', 'adapter-log review', 'Adapter: green?', 'TAM escalation', 'vrops-cli alerts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Disk filling up', 'vsan/disk usage', 'Disk: >70%?', 'Collect app logs', 'vrops-cli capacity'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['No capacity data', 'Analytics node log', 'Data age: <15 min?', 'P1: analytics fail', 'vrops-cli objects'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Aria Operations VMs (master/replica/data/RC) · vSphere cluster · shared datastore'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Analytics node= Aria Operations cluster member that stores and processes collected metric data'))
    lines.append(txt_row('Adapter       = Plugin collecting metrics from a source (vSphere, NSX, vSAN, AWS, storage)'))
    lines.append(txt_row('Management Pack= Bundle of adapters, dashboards, alerts, and policies for a specific product'))
    lines.append(txt_row('Policy        = Configuration for alert thresholds, capacity model, and compliance benchmark'))
    lines.append(txt_row('Rightsizing   = Recommendations to reclaim oversized vCPU/vRAM allocations from idle VMs'))
    lines.append(txt_row('Remote Collector= Aria Operations node deployed close to data source; forwards to analytics cluster'))
    lines.append(txt_row('Compliance    = Benchmark checks (CIS, DISA STIG, PCI-DSS) against collected configuration data'))
    lines.append(txt_row('Heatmap       = Visual grid showing resource utilisation across VMs, hosts, or clusters'))
    lines.append(txt_row('What-if       = Capacity scenario modelling; simulates adding VMs or hosts to forecast headroom'))
    lines.append(txt_row('Alert         = Symptom-driven notification when metric breaches threshold defined in policy'))
    lines.append(txt_row('Workload      = Aria Operations concept; resource utilisation relative to demand and capacity'))
    lines.append(txt_row('Report        = Scheduled or on-demand export of capacity, alerts, or compliance data as PDF/CSV'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── VMware product diagrams — batch 2 of 2 ────────────────────────────────────

@kb_diagram(
    'aria-logs',
    'docs/virtualization/vmware/aria-operations-for-logs/index.md',
    'Aria Operations for Logs Stack — log ingestion, content packs, alerts, webhooks',
)
def aria_logs_stack():
    """Aria Operations for Logs Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations for Logs Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Operations for Logs — Centralised Log Management and Analysis')))
    lines.append(R(bMid(IV_L, IV_R, 'Log ingestion: syslog (UDP/TCP 514), CFAPI agents on VMs, Fluentd forwarding')))
    lines.append(R(bMid(IV_L, IV_R, 'Content packs: pre-built dashboards and queries for vSphere, NSX, ESXi, Linux, Windows')))
    lines.append(R(bMid(IV_L, IV_R, 'Interactive analytics: live-tail, field extraction, regex filters, time-window search')))
    lines.append(R(bMid(IV_L, IV_R, 'Alerts: query-based triggers; webhooks to PagerDuty, Slack, ServiceNow, or email')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Ingestion receives logs · analytics queries them · alerts and dashboards surface insights'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Master+worker nodes'),
        bMid(B2_L, B2_R, 'Log search: query+filter'),
        bMid(B3_L, B3_R, 'RBAC: AD + local users'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'syslog: UDP/TCP 514'),
        bMid(B2_L, B2_R, 'Content pack: install'),
        bMid(B3_L, B3_R, 'TLS: syslog encrypted'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CFAPI agent: per-VM'),
        bMid(B2_L, B2_R, 'Alert: query + webhook'),
        bMid(B3_L, B3_R, 'SSO: vCenter login'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Forwarder: to SIEM'),
        bMid(B2_L, B2_R, 'Dashboard: build+share'),
        bMid(B3_L, B3_R, 'Retention: policy set'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk: retention sizing'),
        bMid(B2_L, B2_R, 'Agent group: bulk mgmt'),
        bMid(B3_L, B3_R, 'Audit: admin actions'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture ingests logs · Operations search and alert · Security controls access and retention'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Logs not arriving', 'System diagnostics', 'Ingest rate: OK?', 'GSS + bundle', 'li-admin status'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Disk full: purging', 'Disk usage check', 'Disk: >70% used?', 'TAM escalation', 'li-admin cluster'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert not firing', 'Alert query debug', 'Alert: enabled?', 'Collect app logs', 'li-admin alerts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Content pack error', 'content-pack.log', 'Packs: installed?', 'P1: log loss event', 'li-admin packs'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Aria Logs VMs (master+worker) · large /storage/core disk · syslog network paths · Aria Suite LCM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CFAPI agent   = Log agent installed on VMs; forwards structured logs via CFAPI protocol on port 9543'))
    lines.append(txt_row('Content pack  = Pre-built bundle of log queries, dashboards, and alerts for a specific product'))
    lines.append(txt_row('Field extract = Named regex capture group applied to log messages to create queryable fields'))
    lines.append(txt_row('Agent group   = Logical grouping of CFAPI agents sharing the same configuration and filters'))
    lines.append(txt_row('Webhook       = HTTP callback for alerts; sends payload to Slack, PagerDuty, or custom URL'))
    lines.append(txt_row('Forwarder     = Sends matching log events to a remote syslog target or SIEM for correlation'))
    lines.append(txt_row('Interactive analytics= Live log search with regex, field filters, and time window; no pre-indexing'))
    lines.append(txt_row('Retention     = Policy setting number of days logs are kept before purging; constrained by disk'))
    lines.append(txt_row('Master node   = Primary Aria Logs node; holds index and coordinates worker nodes in cluster'))
    lines.append(txt_row('Worker node   = Additional Aria Logs node adding ingestion capacity and search throughput'))
    lines.append(txt_row('syslog        = UDP/TCP port 514 protocol; most infrastructure devices send logs via syslog'))
    lines.append(txt_row('li-admin      = Aria Logs admin CLI; cluster status, disk usage, configuration management'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-networks',
    'docs/virtualization/vmware/aria-operations-for-networks/index.md',
    'Aria Operations for Networks Stack — path analysis, IPFIX flows, physical topology',
)
def aria_networks_stack():
    """Aria Operations for Networks Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations for Networks Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Operations for Networks — Network Visibility and Troubleshooting')))
    lines.append(R(bMid(IV_L, IV_R, 'Path analysis: end-to-end network path between source and destination VMs or IPs')))
    lines.append(R(bMid(IV_L, IV_R, 'Flow analytics: IPFIX/NetFlow collection; application traffic maps; top talkers')))
    lines.append(R(bMid(IV_L, IV_R, 'Physical topology: autodiscovered switch/router map integrated with NSX overlay view')))
    lines.append(R(bMid(IV_L, IV_R, 'Security: network exposure analysis; identifies unintended external reachability')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Collectors gather flows · path analysis traces packets · topology maps the full network'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Platform + collectors'),
        bMid(B2_L, B2_R, 'Path analysis: src→dst'),
        bMid(B3_L, B3_R, 'Exposure: internet reach'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX: overlay + DFW data'),
        bMid(B2_L, B2_R, 'Flow: top talker + app'),
        bMid(B3_L, B3_R, 'Security groups: view'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IPFIX/NetFlow: from hosts'),
        bMid(B2_L, B2_R, 'Physical topology: map'),
        bMid(B3_L, B3_R, 'Alert: exposure + drift'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Physical: SNMP discover'),
        bMid(B2_L, B2_R, 'Alert: path change'),
        bMid(B3_L, B3_R, 'RBAC: user + role'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter: VM + NIC data'),
        bMid(B2_L, B2_R, 'Network intent: plan'),
        bMid(B3_L, B3_R, 'Compliance: check rules'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture collects network data · Operations trace paths and flows · Security surfaces exposure'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['No flow data', 'Collector logs', 'Collector: online?', 'GSS + bundle', 'vrni-cli cluster'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Path shows blocked', 'path analysis log', 'Data source: sync?', 'TAM escalation', 'vrni-cli sources'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Topology missing', 'SNMP poll debug', 'Phys topo: OK?', 'Collect app logs', 'vrni-cli flows'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NSX not integrated', 'NSX credential che', 'NSX data: current?', 'P1: net blind spot', 'vrni-cli alerts'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Aria Networks VMs (platform+collectors) · SNMP access to switches · IPFIX from ESXi hosts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Path analysis = Traces every hop from source to destination; shows NSX DFW rules that allow/block'))
    lines.append(txt_row('IPFIX         = IP Flow Information Export; flow telemetry from ESXi/NSX to collectors'))
    lines.append(txt_row('Collector     = Aria Networks remote node that receives IPFIX/NetFlow and forwards to platform'))
    lines.append(txt_row('Physical topology= Auto-discovered map of switches, routers, and links via SNMP and LLDP/CDP'))
    lines.append(txt_row('Flow          = Recorded network conversation: src/dst IP, port, protocol, byte count, duration'))
    lines.append(txt_row('Network intent= Policy that describes desired connectivity; Aria Networks validates compliance'))
    lines.append(txt_row('Exposure      = VM or service reachable from internet/untrusted network; flagged as security risk'))
    lines.append(txt_row('Application   = Auto-discovered group of VMs that communicate; basis for microsegmentation planning'))
    lines.append(txt_row('Top talker    = VM or IP generating the highest volume of network flows in a time window'))
    lines.append(txt_row('NSX integration= Aria Networks pulls DFW rule, segment, and group data directly from NSX Manager'))
    lines.append(txt_row('SNMP          = Simple Network Management Protocol; used to poll physical switch for topology data'))
    lines.append(txt_row('Data source   = vCenter, NSX, or physical device added to Aria Networks for data collection'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-lcm',
    'docs/virtualization/vmware/aria-suite-lifecycle/index.md',
    'Aria Suite Lifecycle Manager — deploy/upgrade Aria products, cert manager, Locker',
)
def aria_lcm_stack():
    """Aria Suite Lifecycle Manager Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Suite Lifecycle Manager Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Suite Lifecycle Manager (Aria SuiteLC) — Aria Product LCM')))
    lines.append(R(bMid(IV_L, IV_R, 'Deploys and upgrades: Aria Operations, Logs, Networks, Automation, and Workspace ONE')))
    lines.append(R(bMid(IV_L, IV_R, 'Environment: logical grouping of Aria products sharing vSphere infra and certificates')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate manager: Aria SuiteLC manages TLS certs for all Aria products centrally')))
    lines.append(R(bMid(IV_L, IV_R, 'Locker: secure credential store for passwords, certificates, and licence keys')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Aria SuiteLC deploys products · manages their certs and passwords · executes upgrades'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Global env: infra acct'),
        bMid(B2_L, B2_R, 'Deploy: product wizard'),
        bMid(B3_L, B3_R, 'Locker: creds + certs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Product env: Aria suite'),
        bMid(B2_L, B2_R, 'Upgrade: binary + apply'),
        bMid(B3_L, B3_R, 'Cert replace: all prods'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Binary mapping: depot'),
        bMid(B2_L, B2_R, 'Cert: rotate on demand'),
        bMid(B3_L, B3_R, 'RBAC: admin + viewer'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere: infra account'),
        bMid(B2_L, B2_R, 'Health: env health check'),
        bMid(B3_L, B3_R, 'Password: scheduled rot'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Upgrade checker: pre-val'),
        bMid(B2_L, B2_R, 'Scale: node add/remove'),
        bMid(B3_L, B3_R, 'Audit: change log'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines environments · Operations deploy and upgrade'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upgrade precheck f', 'lcm-support bundle', 'Env health: green?', 'GSS + bundle', 'lcm-cli status'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert rotation fail', 'certificate.log', 'Certs: valid +30d?', 'TAM escalation', 'lcm-cli certs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Product deploy stu', 'product-install.lo', 'Binary: available?', 'Collect install lo', 'lcm-cli products'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Locker credential ', 'locker-service.log', 'Locker: reachable?', 'P1: LCM failure', 'lcm-cli locker'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Aria SuiteLC VM on vSphere · vSphere infrastructure account · NFS/VMFS datastore · port 443'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Global environment= Aria SuiteLC top-level container; links to vSphere infra account and NTP/DNS'))
    lines.append(txt_row('Product environment= Named grouping of Aria products sharing an infra account and cert authority'))
    lines.append(txt_row('Infrastructure account= vCenter service account used by Aria SuiteLC to deploy product VMs'))
    lines.append(txt_row('Locker        = Secure vault inside Aria SuiteLC; stores passwords, certs, and licence keys'))
    lines.append(txt_row('Binary mapping = Links downloaded product installer to a product version for deployment/upgrade'))
    lines.append(txt_row('Upgrade checker= Pre-upgrade compatibility validation; checks versions and health before proceeding'))
    lines.append(txt_row('Certificate manager= Aria SuiteLC module that generates, replaces, and renews TLS certs for products'))
    lines.append(txt_row('Content management= Feature to import/export Aria product config (blueprints, dashboards) via LCM'))
    lines.append(txt_row('Password rotation= Scheduled or manual rotation of product service account passwords via Locker'))
    lines.append(txt_row('Scale out     = Adding nodes to a product (e.g. vROps data node) managed through Aria SuiteLC'))
    lines.append(txt_row('Health check  = Aria SuiteLC environment health scan; validates products, certs, and credentials'))
    lines.append(txt_row('Depot         = VMware Customer Connect binary source; Aria SuiteLC downloads product binaries'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-automation-architecture',
    'docs/virtualization/vmware/aria-automation/architecture/index.md',
    'Aria Automation Architecture — Prelude cluster, CAS, ABX, service broker, extensibility',
)
def aria_automation_architecture():
    """Aria Automation Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Automation — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Automation = Automation appliance + Service Broker + Assembler + Extensibility (ABX +')))
    lines.append(R(bMid(IV_L, IV_R, 'Service Broker provides self-service catalog with entitlements and approval policies')))
    lines.append(R(bMid(IV_L, IV_R, 'Assembler manages blueprints, cloud accounts, and cloud zones for multi-cloud provisioning')))
    lines.append(R(bMid(IV_L, IV_R, 'ABX actions and embedded Orchestrator extend automation with custom functions and workflows')))
    lines.append(R(bMid(IV_L, IV_R, 'Connects to cloud accounts: vCenter, AWS, Azure, GCP; cloud proxy for on-premises connectivity')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines platform components · integrations connect cloud accounts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Automation appliance'),
        bMid(B2_L, B2_R, 'vCenter cloud acct'),
        bMid(B3_L, B3_R, 'Org/project RBAC'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service Broker: catalog'),
        bMid(B2_L, B2_R, 'GitHub/GitLab: IaC'),
        bMid(B3_L, B3_R, 'Blueprint versioning'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Assembler: blueprints'),
        bMid(B2_L, B2_R, 'ServiceNow ITSM'),
        bMid(B3_L, B3_R, 'Naming standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ABX: extensibility'),
        bMid(B2_L, B2_R, 'AD/LDAP auth'),
        bMid(B3_L, B3_R, 'ABX action limits'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Orchestrator: embed'),
        bMid(B2_L, B2_R, 'Terraform plugin'),
        bMid(B3_L, B3_R, 'Approval policies'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cloud accounts'),
        bMid(B2_L, B2_R, 'Slack/Teams notify'),
        bMid(B3_L, B3_R, 'Cloud zones'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers platform components · integrations connect cloud and ITSM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Service Broker', 'vCenter acct', 'Org/proj RBAC', 'Single-node', 'Blueprint std'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Assembler', 'GitHub IaC', 'Blueprint ver', 'HA cluster', 'Naming conv'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ABX actions', 'ServiceNow', 'Approval policy', 'Cloud proxy', 'ABX limits'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Orchestrator', 'Terraform', 'Cloud zones', 'Multi-cloud', 'Secret policy'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (Automation appliance) · RAM DIMMs · Network NICs · vCenter/cloud provider targets'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Service Broker = Aria Automation self-service catalog; manages entitlements and approval workflows'))
    lines.append(txt_row('Assembler     = Aria Automation design surface; creates blueprints and manages cloud accounts/zones'))
    lines.append(txt_row('ABX (Action Based Extensibility) = FaaS runtime for Python/Node/PowerShell custom actions'))
    lines.append(txt_row('Orchestrator  = vRO embedded in Aria Automation; runs complex multi-step workflows'))
    lines.append(txt_row('Blueprint     = IaC template in Aria YAML; defines cloud-agnostic infrastructure topology'))
    lines.append(txt_row('Cloud account = Aria connection to a cloud endpoint: vCenter, AWS, Azure, or GCP'))
    lines.append(txt_row('Cloud zone    = Subset of a cloud account resources (clusters, regions) available for provisioning'))
    lines.append(txt_row('Catalog item  = Published blueprint or Orchestrator workflow available in Service Broker'))
    lines.append(txt_row('Entitlement   = Policy granting a project/user access to specific catalog items in Service Broker'))
    lines.append(txt_row('Approval policy = Workflow requiring approver sign-off before catalog item request is fulfilled'))
    lines.append(txt_row('Cloud proxy   = Lightweight VM deployed on-premises; routes Aria SaaS traffic to vCenter'))
    lines.append(txt_row('Organization/Project = Org is top-level tenant; Project scopes users, cloud zones, and policies'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-automation-operations',
    'docs/virtualization/vmware/aria-automation/operations/index.md',
    'Aria Automation Operations — blueprint publishing, upgrade, cert management, API',
)
def aria_automation_operations():
    """Aria Automation Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Automation — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Blueprint lifecycle management; request monitoring for failed deployments; catalog item health')))
    lines.append(R(bMid(IV_L, IV_R, 'Subscription and event broker management; pipeline status monitoring; ABX function execution')))
    lines.append(R(bMid(IV_L, IV_R, 'Daily: review failed requests, check cloud account connectivity, verify ABX timeout thresholds')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: Automation upgrade with pre-upgrade snapshot; embedded vRO and plugin updates')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: vRA REST API, ABX Python/Node, Terraform integration, vRO workflows')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch request failures · lifecycle keeps Automation current · automation scales delivery'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Request monitoring'),
        bMid(B2_L, B2_R, 'Automation upgrade'),
        bMid(B3_L, B3_R, 'vRA REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Failed deploys'),
        bMid(B2_L, B2_R, 'Pre-upg snapshot'),
        bMid(B3_L, B3_R, 'ABX: Python/Node'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Catalog health'),
        bMid(B2_L, B2_R, 'Embedded vRO'),
        bMid(B3_L, B3_R, 'Terraform intg'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Sub. events'),
        bMid(B2_L, B2_R, 'ABX FaaS update'),
        bMid(B3_L, B3_R, 'vRO workflows'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pipeline status'),
        bMid(B2_L, B2_R, 'Plugin updates'),
        bMid(B3_L, B3_R, 'PowerShell ABX'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ABX timeout chk'),
        bMid(B2_L, B2_R, 'API compat chk'),
        bMid(B3_L, B3_R, 'API Explorer'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor request health · lifecycle upgrades safely with snapshot'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vRA REST API', 'Requests: ok', 'Blueprint ver', 'Pre-upg snap', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ABX function', 'Catalog: items', 'Deploy test', 'Automation upg', 'Policy backup'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Terraform CLI', 'Cloud accts ok', 'ABX test', 'API compat', 'Blueprint bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API Explorer', 'Pipelines: ok', 'Entitlement', 'Post-upg val', 'Restore redep'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (Automation appliance) · RAM DIMMs · Network NICs · Cloud provider connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Blueprint     = IaC template; versioned in Aria Automation; deploy, update, and destroy lifecycle'))
    lines.append(txt_row('Request       = User-initiated catalog item deployment; tracked in Service Broker with status and'))
    lines.append(txt_row('Catalog item  = Published blueprint or workflow in Service Broker; versioned and'))
    lines.append(txt_row('ABX action    = FaaS function (Python/Node/PowerShell) triggered by events or directly from blueprint'))
    lines.append(txt_row('Subscription  = Event broker rule mapping a lifecycle event to an ABX action or Orchestrator workflow'))
    lines.append(txt_row('Event broker  = Aria Automation event bus; publishes compute/network/storage events to subscriptions'))
    lines.append(txt_row('Cloud account = Aria connection to vCenter/AWS/Azure/GCP; health check ensures connectivity'))
    lines.append(txt_row('Approval policy = Required sign-off before request fulfillment; configurable per catalog item'))
    lines.append(txt_row('Orchestrator workflow = vRO workflow embedded in Aria Automation; runs complex multi-step tasks'))
    lines.append(txt_row('vRA REST API  = Primary Aria Automation programmatic interface; used for requests, blueprints,'))
    lines.append(txt_row('Terraform provider = Aria Automation Terraform provider for IaC-driven provisioning workflows'))
    lines.append(txt_row('Entitlement   = Service Broker policy granting project members access to specific catalog items'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-automation-security',
    'docs/virtualization/vmware/aria-automation/security/index.md',
    'Aria Automation Security — vIDM SSO, RBAC org/project, TLS, audit events',
)
def aria_automation_security():
    """Aria Automation Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Automation — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Workspace ONE/vIDM for SSO; org/project RBAC for catalog and blueprint access control')))
    lines.append(R(bMid(IV_L, IV_R, 'API token management with TTL; approval policies for deployment governance and compliance')))
    lines.append(R(bMid(IV_L, IV_R, 'Secret references for credential storage; Password Locker replaces plaintext in blueprints')))
    lines.append(R(bMid(IV_L, IV_R, 'TLS enforced on all endpoints; cloud account credentials stored encrypted; HTTPS API only')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit log captures all request, catalog, and ABX events for compliance review')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates Aria access · RBAC scopes catalog and blueprints · secrets protect credentials'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'WS1/vIDM SSO'),
        bMid(B2_L, B2_R, 'Org/proj roles'),
        bMid(B3_L, B3_R, 'TLS all endpoints'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD/LDAP intg'),
        bMid(B2_L, B2_R, 'Custom roles'),
        bMid(B3_L, B3_R, 'Secrets at rest'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API token auth'),
        bMid(B2_L, B2_R, 'Resource-level'),
        bMid(B3_L, B3_R, 'Password Locker'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'OAuth 2.0'),
        bMid(B2_L, B2_R, 'Approval policy'),
        bMid(B3_L, B3_R, 'Cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Project member'),
        bMid(B2_L, B2_R, 'Catalog entitle'),
        bMid(B3_L, B3_R, 'HTTPS API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Break-glass admin'),
        bMid(B2_L, B2_R, 'Cloud zone acc'),
        bMid(B3_L, B3_R, 'Secret refs'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who uses Aria · RBAC limits catalog and blueprint scope'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vIDM/WS1 SSO', 'Org admin', 'TLS enforced', 'API token TTL', 'Request audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD/LDAP', 'Project roles', 'Secrets encr', 'Min permissions', 'Catalog events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API tokens', 'Custom roles', 'Password Locker', 'Cert rotation', 'ABX log audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['OAuth 2.0', 'Approval policy', 'HTTPS only', 'Secret refs', 'Org event log'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (Automation appliance) · RAM DIMMs · Network NICs · Identity provider infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM (Identity Manager) = VMware Identity Manager; provides SSO for Aria Automation via SAML/OAuth'))
    lines.append(txt_row('Workspace ONE = Broadcom unified endpoint and identity platform; SSO source for Aria Automation'))
    lines.append(txt_row('Organization  = Top-level Aria Automation tenant; all projects and users belong to an organization'))
    lines.append(txt_row('Project       = Aria Automation grouping; scopes cloud zones, members, and catalog entitlements'))
    lines.append(txt_row('RBAC          = Role-based access control; org/project roles control blueprint and catalog access'))
    lines.append(txt_row('API token     = Bearer token for Aria REST API; has configurable TTL; scoped to user role'))
    lines.append(txt_row('Approval policy = Deployment governance requiring approver action before request proceeds'))
    lines.append(txt_row('Entitlement   = Service Broker policy controlling which projects can consume which catalog items'))
    lines.append(txt_row('Password Locker = Aria Automation encrypted credential store; replaces plaintext blueprint passwords'))
    lines.append(txt_row('Secret reference = Blueprint reference to Password Locker entry; keeps credentials out of IaC code'))
    lines.append(txt_row('Cloud account credentials = Encrypted vCenter/cloud API keys stored in Aria Automation'))
    lines.append(txt_row('OAuth 2.0     = Token-based authorization protocol; used for Aria API and third-party integrations'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-automation-troubleshooting',
    'docs/virtualization/vmware/aria-automation/troubleshooting/index.md',
    'Aria Automation Troubleshooting — deployment failures, vRO errors, ABX, support bundle',
)
def aria_automation_troubleshooting():
    """Aria Automation Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Automation — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Blueprint deploy failures; ABX action errors; cloud account connectivity issues')))
    lines.append(R(bMid(IV_L, IV_R, 'Catalog item errors; pipeline failures; API debug for root cause analysis')))
    lines.append(R(bMid(IV_L, IV_R, 'Event broker subscription troubleshooting; lease expiry and approval stuck scenarios')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: vRA API debug, ABX function logs, vRO log files, request detail view')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: vRA log bundle export; GSS case; TAM for P1; support compatibility matrix')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Blueprint fail'),
        bMid(B2_L, B2_R, 'vRA API debug'),
        bMid(B3_L, B3_R, 'vRA log bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ABX action err'),
        bMid(B2_L, B2_R, 'ABX function log'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cloud acct conn'),
        bMid(B2_L, B2_R, 'vRO log files'),
        bMid(B3_L, B3_R, 'ABX debug mode'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Catalog item err'),
        bMid(B2_L, B2_R, 'Request details'),
        bMid(B3_L, B3_R, 'API trace'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Lease expiry'),
        bMid(B2_L, B2_R, 'Event broker log'),
        bMid(B3_L, B3_R, 'Support matrix'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Approval stuck'),
        bMid(B2_L, B2_R, 'ABX FaaS console'),
        bMid(B3_L, B3_R, 'Log export'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use API and logs · escalation bundles evidence for GSS'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Blueprint fail', 'vRA API debug', '/var/log/vra', 'vRA log bundle', 'Re-deploy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ABX error', 'ABX func logs', '/var/log/abx', 'GSS P1 case', 'Fix + retry'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cloud acct err', 'vRO logs', '/var/log/vro', 'TAM escalate', 'Re-auth acct'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Approval stuck', 'Event broker', '/var/log/event', 'Support matrix', 'Clear + retry'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (Automation appliance) · RAM DIMMs · Network NICs · Cloud provider APIs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Blueprint deployment = End-to-end request from Service Broker through Assembler to cloud provider'))
    lines.append(txt_row('ABX action    = FaaS function failure; check ABX console logs and timeout configuration'))
    lines.append(txt_row('Cloud account = vCenter/AWS/Azure connection; re-validate credentials and proxy connectivity'))
    lines.append(txt_row('Catalog item  = Service Broker published item; errors traced via request detail and event log'))
    lines.append(txt_row('Approval policy = Stuck approval due to missing approver; check policy config and user assignment'))
    lines.append(txt_row('Event broker  = Aria Automation event bus; subscription failures visible in event broker log'))
    lines.append(txt_row('Subscription  = Event-to-action mapping; failed subscriptions appear in event broker error log'))
    lines.append(txt_row('Lease expiry  = Deployment TTL reached; check reclaim notification config and project lease policy'))
    lines.append(txt_row('vRO (Orchestrator) = Embedded workflow engine; logs at /var/log/vro for workflow execution debug'))
    lines.append(txt_row('API debug     = Aria REST API with ?debug=true parameter; returns detailed provisioning trace'))
    lines.append(txt_row('Request lifecycle = Created → Pending Approval → In Progress → Successful/Failed states'))
    lines.append(txt_row('Pipeline stage = Aria Automation Pipelines stage failure; review stage log for task error detail'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-operations-architecture',
    'docs/virtualization/vmware/aria-operations/architecture/index.md',
    'Aria Operations Architecture — analytics cluster, remote collectors, adapters, capacity',
)
def aria_operations_architecture():
    """Aria Operations Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations (formerly vROps) — analytics cluster: primary + replica + data nodes per site')))
    lines.append(R(bMid(IV_L, IV_R, 'Remote collectors deployed per site collect metrics without exposing firewall paths to the')))
    lines.append(R(bMid(IV_L, IV_R, 'Adapter instances per integration: vSphere, NSX-T, storage, ServiceNow, SIEM, email/SNMP')))
    lines.append(R(bMid(IV_L, IV_R, 'Dashboards and alerts surface health, risk, efficiency badges across vSphere, NSX, storage,')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity management and optimization actions right-size VMs and forecast resource exhaustion')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines the cluster internals · integrations connect adapters'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Analytics cluster'),
        bMid(B2_L, B2_R, 'vSphere adapter'),
        bMid(B3_L, B3_R, 'Cluster L/XL sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Remote collectors'),
        bMid(B2_L, B2_R, 'NSX-T adapter'),
        bMid(B3_L, B3_R, 'Remote coll/site'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Adapter instances'),
        bMid(B2_L, B2_R, 'Storage adapters'),
        bMid(B3_L, B3_R, 'Adapter config std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collector groups'),
        bMid(B2_L, B2_R, 'ServiceNow ITSM'),
        bMid(B3_L, B3_R, 'Data retain 6 mo'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboards+alerts'),
        bMid(B2_L, B2_R, 'SIEM/Kafka'),
        bMid(B3_L, B3_R, 'Alert policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity mgmt'),
        bMid(B2_L, B2_R, 'Email/SNMP alert'),
        bMid(B3_L, B3_R, 'Custom dash std'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers cluster nodes · integrations connect adapters and ITSM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Analytics cluster', 'vSphere adapter', 'Cluster sizing', 'Single node', 'Alert policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Remote collectors', 'NSX-T adapter', 'Remote coll', 'Small cluster', 'Dashboard std'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Adapter instances', 'Storage adapters', 'Data retention', 'HA cluster', 'Naming conv'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Collector groups', 'ServiceNow intg', 'Custom policies', 'Multi-cloud', 'RBAC std'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (cluster nodes + remote collectors) · RAM DIMMs · Network NICs · vCenter/cloud targets'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Analytics cluster  = Primary + replica + data nodes forming the Aria Ops processing engine'))
    lines.append(txt_row('Primary node       = Cluster leader; hosts the UI, API, and coordinates analytics workload'))
    lines.append(txt_row('Replica node       = Standby for primary; takes over if primary fails; participates in analytics'))
    lines.append(txt_row('Data node          = Additional analytics capacity node; scales metric ingestion and retention'))
    lines.append(txt_row('Remote collector   = Lightweight VM per site; collects adapter data and forwards to cluster'))
    lines.append(txt_row('Adapter instance   = Configured connection to a monitored product: vSphere, NSX, storage, cloud'))
    lines.append(txt_row('Collector group    = Named group of remote collectors assigned to adapter instances for load sharing'))
    lines.append(txt_row('Dashboard          = Customizable view of metrics, badges, and alerts for a resource group'))
    lines.append(txt_row('Alert definition   = Rule triggering notification when a metric crosses a threshold or symptom fires'))
    lines.append(txt_row('Capacity analytics = Forecasting engine projecting resource exhaustion based on trend analysis'))
    lines.append(txt_row('Optimization action = Recommended change (right-size, power off, migrate) to improve efficiency'))
    lines.append(txt_row('Badge              = Health/risk/efficiency score (0-100) summarising object state at a glance'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-operations-operations',
    'docs/virtualization/vmware/aria-operations/operations/index.md',
    'Aria Operations Operations — alert management, right-sizing, lifecycle, REST API',
)
def aria_operations_operations():
    """Aria Operations Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Alert management and noise reduction: tune thresholds, suppress flapping, cancel false')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity optimization: review right-sizing recommendations; act on workload placement advice')))
    lines.append(R(bMid(IV_L, IV_R, 'Report scheduling: cost management integration; automated PDF/CSV delivery to stakeholders')))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster node health monitoring: verify all nodes stable; check adapter collection intervals')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: upgrade wizard sequences node upgrades; pre-upgrade health check mandatory')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops review alerts and capacity · lifecycle keeps cluster current'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert management'),
        bMid(B2_L, B2_R, 'Upgrade planner'),
        bMid(B3_L, B3_R, 'REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity overview'),
        bMid(B2_L, B2_R, 'Pre-upg health'),
        bMid(B3_L, B3_R, 'PowerCLI vROps'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Optim. actions'),
        bMid(B2_L, B2_R, 'Node upg order'),
        bMid(B3_L, B3_R, 'Alert API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Workload place'),
        bMid(B2_L, B2_R, 'Adapter compat'),
        bMid(B3_L, B3_R, 'Capacity API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Badge status'),
        bMid(B2_L, B2_R, 'CMDB sync'),
        bMid(B3_L, B3_R, 'Dashboard API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Report schedule'),
        bMid(B2_L, B2_R, 'Cert renew'),
        bMid(B3_L, B3_R, 'Report API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch alert noise · lifecycle upgrades nodes in sequence · automation reduces manual toil'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['REST API calls', 'Cluster: green', 'Alert triage', 'Upgrade wizard', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PowerCLI vROps', 'Nodes: healthy', 'Capacity rpt', 'Pre-chk health', 'Support.zip'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert API', 'Adapters: ok', 'Add remote coll', 'Node upg order', 'Restore config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Capacity API', 'Collectors: up', 'Dashboard add', 'Post-upg val', 'Metric data bk'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (primary/replica/data/collector) · RAM DIMMs · Network NICs · vCenter/cloud connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Analytics cluster  = Primary + replica + data nodes; all must be healthy for full functionality'))
    lines.append(txt_row('Remote collector   = Lightweight VM per site forwarding adapter metrics to the analytics cluster'))
    lines.append(txt_row('Adapter instance   = Configured integration to a monitored product; collection interval configurable'))
    lines.append(txt_row('Alert definition   = Symptom-based rule firing notifications on threshold breach or anomaly'))
    lines.append(txt_row('Capacity engine    = Forecasting subsystem projecting time-to-exhaustion for CPU, RAM, storage'))
    lines.append(txt_row('Optimization action = Right-size, power-off, or migrate recommendation generated by analytics'))
    lines.append(txt_row('Workload placement = DRS-aligned recommendation for optimal VM-to-host assignment'))
    lines.append(txt_row('Badge score        = 0-100 health/risk/efficiency score assigned to every monitored object'))
    lines.append(txt_row('Right-sizing       = Reducing oversized vCPU/RAM allocations based on observed peak utilisation'))
    lines.append(txt_row('Cost driver        = Resource consumer identified as a top contributor to capacity or cost usage'))
    lines.append(txt_row('Upgrade planner    = Built-in wizard validating compatibility and sequencing node upgrade steps'))
    lines.append(txt_row('support.zip bundle = Diagnostic package collected from Aria Ops for GSS case submission'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-operations-security',
    'docs/virtualization/vmware/aria-operations/security/index.md',
    'Aria Operations Security — vIDM SSO, RBAC roles, TLS, API tokens, audit log',
)
def aria_operations_security():
    """Aria Operations Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vIDM/Active Directory integration for SSO; RBAC roles (admin/user/viewer) for object-level')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate management: cluster and adapter TLS certificates rotated on schedule')))
    lines.append(R(bMid(IV_L, IV_R, 'API token authentication: scoped bearer tokens for REST API integrations and automation')))
    lines.append(R(bMid(IV_L, IV_R, 'All REST API communication over TLS; encrypted passwords stored in credential vault')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit event log captures all admin actions; syslog forwarding to SIEM over TLS')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates access · RBAC scopes permissions · encryption and audit enforce compliance'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vIDM/AD auth'),
        bMid(B2_L, B2_R, 'Admin: full access'),
        bMid(B3_L, B3_R, 'REST over TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP/AD groups'),
        bMid(B2_L, B2_R, 'User: dashboards'),
        bMid(B3_L, B3_R, 'Cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Local admin'),
        bMid(B2_L, B2_R, 'Viewer: read-only'),
        bMid(B3_L, B3_R, 'Encrypted passwords'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert-based auth'),
        bMid(B2_L, B2_R, 'Object-level acc'),
        bMid(B3_L, B3_R, 'Syslog over TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API token'),
        bMid(B2_L, B2_R, 'Custom roles'),
        bMid(B3_L, B3_R, 'Data encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Audit log'),
        bMid(B2_L, B2_R, 'Content share'),
        bMid(B3_L, B3_R, 'FIPS mode'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who logs in · access control limits scope · encryption and audit enforce compliance'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vIDM/AD SSO', 'Admin role', 'TLS enforced', 'Cert rotation', 'Event audit log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LDAP groups', 'User role', 'Pwd encrypted', 'API token TTL', 'Adapter log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API tokens', 'Viewer role', 'Syslog TLS', 'RBAC review', 'Alert log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert-based', 'Object access', 'FIPS mode', 'Min-perm API', 'Config changes'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (cluster) · RAM DIMMs · Network NICs · Identity provider (AD/LDAP) · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM               = VMware Identity Manager; provides SSO and group-based role assignment to Aria'))
    lines.append(txt_row('Active Directory    = LDAP-compatible directory; groups mapped to Aria Ops roles for user access'))
    lines.append(txt_row('RBAC               = Role-Based Access Control; admin/user/viewer roles scoped to object groups'))
    lines.append(txt_row('Admin role         = Full access: manage adapters, alerts, dashboards, users, and system config'))
    lines.append(txt_row('User role          = Dashboard and alert access; can create content but not manage system config'))
    lines.append(txt_row('Viewer role        = Read-only access to dashboards and alerts; cannot create or modify content'))
    lines.append(txt_row('Object-level access = Permissions scoped to specific resource groups or monitored object sets'))
    lines.append(txt_row('API token          = Bearer token for REST API auth; scoped to user role; configurable TTL'))
    lines.append(txt_row('TLS                = Transport Layer Security; all API and UI communication encrypted in transit'))
    lines.append(txt_row('FIPS mode          = Federal Information Processing Standard 140-2 compliant cryptography mode'))
    lines.append(txt_row('Certificate management = Rotate cluster TLS and adapter certs via admin UI or REST API'))
    lines.append(txt_row('Audit event log    = Immutable record of all admin actions: login, config change, user management'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-operations-troubleshooting',
    'docs/virtualization/vmware/aria-operations/troubleshooting/index.md',
    'Aria Operations Troubleshooting — adapter failures, alert noise, missing data, support.zip',
)
def aria_operations_troubleshooting():
    """Aria Operations Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Adapter collection failures: verify credentials, firewall paths, and adapter version')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert noise and false positives: tune symptom thresholds; check adapter collection gaps')))
    lines.append(R(bMid(IV_L, IV_R, 'Missing metric data: confirm remote collector reachability; check collector group assignment')))
    lines.append(R(bMid(IV_L, IV_R, 'Dashboard errors: verify data source adapter health; check widget metric mappings')))
    lines.append(R(bMid(IV_L, IV_R, 'support.zip bundle collects all cluster logs; attach to GSS case for escalation')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics isolate adapter or cluster root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Adapter coll fail'),
        bMid(B2_L, B2_R, 'Cluster diagnostics'),
        bMid(B3_L, B3_R, 'Support.zip'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert noise'),
        bMid(B2_L, B2_R, 'Adapter log'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Missing data'),
        bMid(B2_L, B2_R, 'Support.zip'),
        bMid(B3_L, B3_R, 'Skyline health'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboard error'),
        bMid(B2_L, B2_R, 'REST API debug'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Remote coll down'),
        bMid(B2_L, B2_R, 'Log Insight intg'),
        bMid(B3_L, B3_R, 'Log bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity wrong'),
        bMid(B2_L, B2_R, 'Metric explorer'),
        bMid(B3_L, B3_R, 'Version compat'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues triage adapter and cluster faults · diagnostics use logs and metric explorer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Adapter fail', 'Adapter log', '/var/log/vrops', 'support.zip', 'Re-auth adapter'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert noise', 'Metric explorer', 'Cluster diag', 'GSS P1 case', 'Tune alert'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Missing data', 'REST API debug', '/var/log/casa', 'TAM escalate', 'Re-collect'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Collector down', 'Support.zip', '/var/log/coll', 'Skyline health', 'Restart coll'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (cluster nodes + collectors) · RAM DIMMs · Network NICs · vCenter/cloud connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Adapter collection = Periodic metric pull by an adapter instance; fails on auth or network errors'))
    lines.append(txt_row('Remote collector   = Site-local VM forwarding metrics; offline if unreachable or out of resources'))
    lines.append(txt_row('Alert noise        = Excessive or false-positive alerts caused by overly sensitive symptom thresholds'))
    lines.append(txt_row('Metric gap         = Missing data points in a metric time series; caused by collection or node'))
    lines.append(txt_row('Support.zip bundle = Full diagnostic archive from Aria Ops cluster; submitted to GSS for analysis'))
    lines.append(txt_row('Cluster diagnostics = Built-in health tool validating node connectivity, services, and disk usage'))
    lines.append(txt_row('Metric explorer    = UI tool for querying raw metric time series to identify gaps or anomalies'))
    lines.append(txt_row('Capacity calculation = Engine consuming metric history to project resource exhaustion dates'))
    lines.append(txt_row('Skyline Health     = VMware proactive support tool that validates cluster health against best'))
    lines.append(txt_row('REST API           = Aria Ops API for querying metrics, alerts, recommendations programmatically'))
    lines.append(txt_row('Log Insight intg   = Aria Logs integration forwarding Aria Ops cluster logs for structured search'))
    lines.append(txt_row('False positive alert = Alert firing when no real problem exists; tuned via symptom threshold change'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-logs-architecture',
    'docs/virtualization/vmware/aria-operations-for-logs/architecture/index.md',
    'Aria Logs Architecture — master/worker HA cluster, vRLI agents, VLQL, content packs',
)
def aria_logs_architecture():
    """Aria Logs Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Logs — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations for Logs (formerly vRealize Log Insight) — master node + worker nodes HA')))
    lines.append(R(bMid(IV_L, IV_R, 'vRLI agents on Windows/Linux hosts; syslog TCP/UDP ingestion from network devices and ESXi')))
    lines.append(R(bMid(IV_L, IV_R, 'VLQL structured queries for interactive analytics; alert pipelines to vROps/email/webhook')))
    lines.append(R(bMid(IV_L, IV_R, 'Content packs provide structured field extraction and dashboards for known log sources')))
    lines.append(R(bMid(IV_L, IV_R, 'Log forwarder exports filtered streams to SIEM; retention enforced by disk policy per node')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines cluster mechanics · integrations connect log sources'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Master + workers HA'),
        bMid(B2_L, B2_R, 'vROps integration'),
        bMid(B3_L, B3_R, '3-node HA cluster'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vRLI agents'),
        bMid(B2_L, B2_R, 'NSX syslog'),
        bMid(B3_L, B3_R, 'Log retention pol'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Syslog TCP/UDP'),
        bMid(B2_L, B2_R, 'ESXi syslog'),
        bMid(B3_L, B3_R, 'Agent deployment'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VLQL queries'),
        bMid(B2_L, B2_R, 'Windows agent'),
        bMid(B3_L, B3_R, 'Alert thresholds'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert pipelines'),
        bMid(B2_L, B2_R, 'Syslog sources'),
        bMid(B3_L, B3_R, 'Content pack org'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Content packs'),
        bMid(B2_L, B2_R, 'SIEM forwarding'),
        bMid(B3_L, B3_R, 'Disk sizing'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers cluster and ingestion · integrations connect sources'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Master+workers', 'vROps intg', '3-node cluster', 'Single node', 'Retention pol'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vRLI agents', 'NSX syslog', 'Log retention', 'HA cluster', 'Alert thresh'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Syslog TCP/UDP', 'ESXi syslog', 'Agent deploy', 'Forwarder', 'Disk sizing'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VLQL queries', 'SIEM forward', 'Alert config', 'Multi-site', 'Content packs'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (master + workers) · RAM DIMMs · Network NICs · High-capacity storage (log disk)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master node        = Aria Logs cluster leader; hosts UI, API, and coordinates ingestion across'))
    lines.append(txt_row('Worker node        = Additional cluster member; shares ingestion load and stores log partitions'))
    lines.append(txt_row('vRLI agent         = Lightweight agent on Windows/Linux; forwards structured log events to cluster'))
    lines.append(txt_row('Syslog ingestion   = UDP/TCP syslog receiver on port 514/6514; accepts RFC3164/5424 formatted logs'))
    lines.append(txt_row('VLQL               = vRLI Query Language; structured query syntax for filtering and aggregating logs'))
    lines.append(txt_row('Content pack       = Pre-built dashboards and field extractors for a specific log source (NSX,'))
    lines.append(txt_row('Alert pipeline     = Rule triggering notifications or forwarding to vROps/email/webhook on log match'))
    lines.append(txt_row('Log forwarder      = Cluster feature streaming filtered log events to an external SIEM destination'))
    lines.append(txt_row('Structured parsing = Field extraction from raw log text using content pack or custom regex rules'))
    lines.append(txt_row('Log retention      = Disk-based policy deleting oldest log partitions when capacity threshold reached'))
    lines.append(txt_row('HA cluster         = Master + 2+ worker nodes with integrated load balancer virtual IP for ingestion'))
    lines.append(txt_row('Interactive analytics = UI-based VLQL query workspace for ad-hoc log investigation and charting'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-logs-operations',
    'docs/virtualization/vmware/aria-operations-for-logs/operations/index.md',
    'Aria Logs Operations — alert management, disk retention, content packs, upgrade',
)
def aria_logs_operations():
    """Aria Logs Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Logs — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Alert management and dashboard queries; agent health monitoring across all forwarding hosts')))
    lines.append(R(bMid(IV_L, IV_R, 'Disk usage and retention enforcement: monitor partition fill rate; expand disks proactively')))
    lines.append(R(bMid(IV_L, IV_R, 'Content pack management: import, update, and validate packs for new log source onboarding')))
    lines.append(R(bMid(IV_L, IV_R, 'Forwarder configuration for SIEM integration: filter, tag, and stream log events externally')))
    lines.append(R(bMid(IV_L, IV_R, 'vRLI upgrade sequence: backup config, upgrade nodes in order, validate post-upgrade health')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops review alerts and agents · lifecycle upgrades nodes safely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert review'),
        bMid(B2_L, B2_R, 'vRLI upgrades'),
        bMid(B3_L, B3_R, 'vRLI REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboard query'),
        bMid(B2_L, B2_R, 'Pre-chk backup'),
        bMid(B3_L, B3_R, 'Content pk import'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Agent health'),
        bMid(B2_L, B2_R, 'Node upg order'),
        bMid(B3_L, B3_R, 'Agent config API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk usage'),
        bMid(B2_L, B2_R, 'Agent upgrade'),
        bMid(B3_L, B3_R, 'Alert API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Source health'),
        bMid(B2_L, B2_R, 'Content pk update'),
        bMid(B3_L, B3_R, 'Query API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Content pk status'),
        bMid(B2_L, B2_R, 'Cert renew'),
        bMid(B3_L, B3_R, 'VLQL scripted'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor agents and disk · lifecycle upgrades safely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['REST API calls', 'Cluster: green', 'Alert tune', 'Upgrade node', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VLQL queries', 'Agents: sending', 'Add log source', 'Agent update', 'Content bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert API', 'Disk: <80%', 'Forwarder cfg', 'Content pk upg', 'Restore config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Content pk API', 'Sources: active', 'Retention chk', 'Post-upg val', 'Log archive'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (master + workers) · RAM DIMMs · Network NICs · High-capacity log storage · Syslog network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Content pack       = Pre-built field extractors and dashboards; imported via UI or REST API'))
    lines.append(txt_row('vRLI agent         = Host-based log forwarder; reports sending state visible in admin sources page'))
    lines.append(txt_row('Alert pipeline     = Log-match rule triggering email, webhook, or vROps notification on condition'))
    lines.append(txt_row('VLQL query         = vRLI Query Language statement for filtering, grouping, and charting log events'))
    lines.append(txt_row('Log forwarder      = Cluster feature streaming matched events to SIEM via syslog or REST endpoint'))
    lines.append(txt_row('Disk retention     = Automatic deletion of oldest log partitions when disk reaches configured'))
    lines.append(txt_row('HA cluster upgrade = Sequenced upgrade: master node last; workers upgraded first to preserve'))
    lines.append(txt_row('Source health      = Admin UI view showing per-source event rate and last-received timestamp'))
    lines.append(txt_row('REST API           = vRLI API for querying events, managing alerts, sources, and content packs'))
    lines.append(txt_row('Interactive analytics = VLQL query workspace for ad-hoc investigation with chart and table views'))
    lines.append(txt_row('Log ingestion rate = Events-per-second metric; baseline for disk capacity planning and alerting'))
    lines.append(txt_row('Content pack version = Versioned pack release; update to get new dashboards and field extractors'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-logs-security',
    'docs/virtualization/vmware/aria-operations-for-logs/security/index.md',
    'Aria Logs Security — AD/LDAP SSO, RBAC, TLS agent/syslog, FIPS, audit trail',
)
def aria_logs_security():
    """Aria Logs Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Logs — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Active Directory/LDAP for SSO; role-based access for dashboards and alerts per user group')))
    lines.append(R(bMid(IV_L, IV_R, 'TLS for agent connections and syslog TCP/TLS; REST API served over HTTPS only')))
    lines.append(R(bMid(IV_L, IV_R, 'FIPS 140-2 mode available; encrypted passwords at rest in credential store')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit trail captures all admin actions: login events, config changes, source additions')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate rotation for agent TLS, cluster UI cert, and syslog TLS endpoints')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates access · role-based access scopes dashboards'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD/LDAP auth'),
        bMid(B2_L, B2_R, 'Admin: full'),
        bMid(B3_L, B3_R, 'Agent TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP integration'),
        bMid(B2_L, B2_R, 'User: dashboards'),
        bMid(B3_L, B3_R, 'Syslog TCP/TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Local admin'),
        bMid(B2_L, B2_R, 'Dashboard roles'),
        bMid(B3_L, B3_R, 'REST over HTTPS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Role-based'),
        bMid(B2_L, B2_R, 'Source access'),
        bMid(B3_L, B3_R, 'Cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API token'),
        bMid(B2_L, B2_R, 'Alert mgmt'),
        bMid(B3_L, B3_R, 'FIPS mode'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SAML support'),
        bMid(B2_L, B2_R, 'Content pk admin'),
        bMid(B3_L, B3_R, 'Pwd encrypted'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who logs in · access control scopes dashboards · encryption secures all log paths'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD/LDAP SSO', 'Admin role', 'Agent TLS', 'Cert rotation', 'Admin events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API tokens', 'User role', 'Syslog TLS', 'FIPS mode', 'Query log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SAML support', 'Dashboard role', 'HTTPS REST', 'Pwd policy', 'Alert audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Local admin', 'Source access', 'Cert mgmt', 'Min-perm API', 'Config changes'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (cluster) · RAM DIMMs · Network NICs · AD/LDAP server · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AD/LDAP            = Active Directory/LDAP; group membership mapped to Aria Logs roles'))
    lines.append(txt_row('SAML               = Security Assertion Markup Language; federated SSO for Aria Logs UI login'))
    lines.append(txt_row('Role-based access   = Admin/user/viewer roles; scoped to dashboard sets and log source access'))
    lines.append(txt_row('Admin role         = Full Aria Logs access: manage sources, alerts, content packs, and users'))
    lines.append(txt_row('User role          = Dashboard view and query access; cannot manage sources or system config'))
    lines.append(txt_row('TLS agent connection = Encrypted channel between vRLI agent and cluster ingestion endpoint'))
    lines.append(txt_row('Syslog over TLS    = RFC5425 TLS-wrapped syslog on port 6514; encrypts log transit from sources'))
    lines.append(txt_row('FIPS 140-2         = Federal cryptographic standard; enabled at cluster level for compliance'))
    lines.append(txt_row('Certificate management = Rotate UI, agent, and syslog TLS certificates via admin settings'))
    lines.append(txt_row('API token          = Bearer token for REST API calls; scoped to authenticated user role'))
    lines.append(txt_row('Audit trail        = Immutable log of admin actions: logins, config changes, source management'))
    lines.append(txt_row('Encrypted credentials = Passwords and secrets stored encrypted in cluster credential vault'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-logs-troubleshooting',
    'docs/virtualization/vmware/aria-operations-for-logs/troubleshooting/index.md',
    'Aria Logs Troubleshooting — agents silent, disk full, alert not firing, vRLI bundle',
)
def aria_logs_troubleshooting():
    """Aria Logs Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Logs — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Agents not sending logs: check agent connectivity, firewall rules, and agent configuration')))
    lines.append(R(bMid(IV_L, IV_R, 'Missing log sources: verify syslog UDP/TCP port reachability and source IP configuration')))
    lines.append(R(bMid(IV_L, IV_R, 'Disk full blocking ingestion: expand disk or reduce retention; clear oldest partitions')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert not firing: validate field extraction in content pack; check query match logic')))
    lines.append(R(bMid(IV_L, IV_R, 'vRLI support bundle collects cluster and agent logs; attach to GSS case for escalation')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues triage agent and source faults · diagnostics use logs and API'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Agent not sending'),
        bMid(B2_L, B2_R, 'Admin UI sources'),
        bMid(B3_L, B3_R, 'vRLI support bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Source missing'),
        bMid(B2_L, B2_R, 'Agent log files'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk full'),
        bMid(B2_L, B2_R, '/var/log/loginsight'),
        bMid(B3_L, B3_R, 'Agent config exp'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert not fire'),
        bMid(B2_L, B2_R, 'REST API debug'),
        bMid(B3_L, B3_R, 'Log sample coll'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Query empty'),
        bMid(B2_L, B2_R, 'Source status'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Forwarder err'),
        bMid(B2_L, B2_R, 'Content pk test'),
        bMid(B3_L, B3_R, 'Version matrix'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use source admin and log paths'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Agent silent', 'Agent log file', '/var/log/loginsight', 'vRLI bundle', 'Restart agent'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Disk full', 'Source status', '/var/log/li-server', 'GSS P1 case', 'Expand disk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert not fire', 'REST API dbg', '/var/log/agent', 'TAM escalate', 'Retune alert'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Query empty', 'Content pk test', '/var/log/server', 'Version matrix', 'Fix time range'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (cluster) · RAM DIMMs · Network NICs · Log storage · Syslog source hosts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vRLI agent         = Host-based log forwarder; check agent service status and firewall on port 9000'))
    lines.append(txt_row('Syslog source      = Network device or host sending UDP/TCP syslog; verify source IP is allowed'))
    lines.append(txt_row('Disk retention     = Policy deleting oldest partitions at threshold; full disk blocks all ingestion'))
    lines.append(txt_row('Alert pipeline     = Log-match rule; fails silently if field extraction is incorrect in content pack'))
    lines.append(txt_row('VLQL query         = Query returning empty if time range, field name, or syntax is incorrect'))
    lines.append(txt_row('Content pack       = Field extractor and dashboard bundle; test via UI to validate regex patterns'))
    lines.append(txt_row('Log forwarder      = SIEM stream; errors if destination unreachable or certificate mismatch'))
    lines.append(txt_row('Ingestion rate     = Events-per-second; drop to zero indicates cluster issue or source problem'))
    lines.append(txt_row('Cluster node health = Admin dashboard showing master and worker node status and disk usage'))
    lines.append(txt_row('REST API debug     = Query the vRLI API directly to bypass UI and validate field extraction'))
    lines.append(txt_row('Support bundle     = Full diagnostic archive: cluster logs, config, and event data for GSS review'))
    lines.append(txt_row('Agent configuration = JSON config file on host specifying cluster address, port, and log paths'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-networks-architecture',
    'docs/virtualization/vmware/aria-operations-for-networks/architecture/index.md',
    'Aria Networks Architecture — platform/collector VMs, IPFIX flows, path analysis, NSX',
)
def aria_networks_architecture():
    """Aria Networks Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Networks — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations for Networks (formerly vRealize Network Insight) = Platform VM + Collector VMs')))
    lines.append(R(bMid(IV_L, IV_R, 'Ingests VMware (NSX/vCenter) and physical switch data (SNMP) for full-stack network visibility')))
    lines.append(R(bMid(IV_L, IV_R, 'Provides network topology, path tracing, flow analysis, and security group auditing')))
    lines.append(R(bMid(IV_L, IV_R, 'Collector VMs deployed per site forward data to the central Platform VM for correlation')))
    lines.append(R(bMid(IV_L, IV_R, 'Data sources: NSX-T/V, vCenter, physical switches (SNMP v3), AWS/Azure VPC flow logs, IPAM')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines data collection mechanics · integrations connect all data sources'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Platform VM: central'),
        bMid(B2_L, B2_R, 'NSX-T/V source'),
        bMid(B3_L, B3_R, 'Collector per site'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collector VMs: sites'),
        bMid(B2_L, B2_R, 'vCenter source'),
        bMid(B3_L, B3_R, 'Platform sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX data source'),
        bMid(B2_L, B2_R, 'Physical switch'),
        bMid(B3_L, B3_R, 'Data src creds'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Physical SNMP'),
        bMid(B2_L, B2_R, 'AWS/Azure VPC'),
        bMid(B3_L, B3_R, 'SNMP v3 config'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Path trace engine'),
        bMid(B2_L, B2_R, 'IPAM integration'),
        bMid(B3_L, B3_R, 'Collection interval'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Flow analysis'),
        bMid(B2_L, B2_R, 'Log Insight fwd'),
        bMid(B3_L, B3_R, 'Retention policy'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers data ingestion · integrations bring in all network sources'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Platform VM', 'NSX-T source', 'Collector sizing', 'Single platform', 'SNMP v3'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Collector VMs', 'vCenter source', 'Platform size', 'Multi-site', 'Cred rotation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Path trace', 'Physical SNMP', 'Retention pol', 'AWS/Azure', 'Collection intv'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Flow analysis', 'IPAM intg', 'Cred mgmt', 'Enterprise', 'Alert thresh'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (Platform + Collector) · RAM DIMMs · Network NICs · Physical switches (SNMP) · NSX/vCenter'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Platform VM       = Central Aria Networks appliance; receives data from all Collectors; hosts the UI'))
    lines.append(txt_row('Collector VM      = Per-site VM that collects data from local data sources and forwards to Platform'))
    lines.append(txt_row('Data source       = Configured connection to NSX, vCenter, physical switch, or cloud for data'))
    lines.append(txt_row('Path tracing      = End-to-end network path visualization from source VM to destination across'))
    lines.append(txt_row('Flow analysis     = Query interface for historical and real-time network flow data from all data'))
    lines.append(txt_row('SNMP v3           = SNMPv3 protocol for physical switch collection; provides auth and encryption'))
    lines.append(txt_row('NSX-T data source = Aria Networks integration that ingests NSX topology, DFW rules, and flow data'))
    lines.append(txt_row('Physical topology = Network map that includes physical switches alongside virtual overlay components'))
    lines.append(txt_row('VPC flow logs     = AWS/Azure network flow records ingested by Aria Networks for hybrid visibility'))
    lines.append(txt_row('Network intent check = Policy verification that compares actual traffic flows against defined'))
    lines.append(txt_row('Security group audit = Review of NSX/cloud security group membership and rule coverage for compliance'))
    lines.append(txt_row('Collection interval = Frequency at which Collector VMs poll each data source; configurable per'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-networks-operations',
    'docs/virtualization/vmware/aria-operations-for-networks/operations/index.md',
    'Aria Networks Operations — flow queries, path analysis, alert management, upgrade',
)
def aria_networks_operations():
    """Aria Networks Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Networks — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Network intent checks for policy compliance; flow analysis queries for traffic patterns per')))
    lines.append(R(bMid(IV_L, IV_R, 'Path trace for troubleshooting connectivity issues between any two endpoints in the environment')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert review for topology changes; security group auditing for microsegmentation drift')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: vRNI upgrades via Platform UI; upgrade Platform first then Collector VMs at each')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: REST API for path trace, flow query, alert management, and scheduled report')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops verify network intent · lifecycle keeps platform current'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Intent checks'),
        bMid(B2_L, B2_R, 'vRNI upgrades'),
        bMid(B3_L, B3_R, 'vRNI REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert review'),
        bMid(B2_L, B2_R, 'Platform+coll upg'),
        bMid(B3_L, B3_R, 'Path trace API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Flow analysis'),
        bMid(B2_L, B2_R, 'Data src re-auth'),
        bMid(B3_L, B3_R, 'Flow query API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Sec grp audit'),
        bMid(B2_L, B2_R, 'SNMP compat'),
        bMid(B3_L, B3_R, 'Alert API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Path trace'),
        bMid(B2_L, B2_R, 'Cert renew'),
        bMid(B3_L, B3_R, 'Report API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboard review'),
        bMid(B2_L, B2_R, 'Config backup'),
        bMid(B3_L, B3_R, 'Python SDK'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch policy drift · lifecycle upgrades Platform before Collectors'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['REST API calls', 'Platform: ok', 'Intent check', 'Upgrade plat', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Flow query API', 'Collectors: up', 'Path trace', 'Coll upgrade', 'API config bk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert API', 'Data srcs: ok', 'Sec grp audit', 'Data src auth', 'Restore config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Python SDK', 'Alerts: none', 'Flow report', 'Post-upg val', 'Log archive'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · NSX/vCenter/Physical switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Network intent    = Defined policy for how traffic should flow between workloads; verified against'))
    lines.append(txt_row('Path trace        = On-demand trace of the actual network path between two endpoints in the'))
    lines.append(txt_row('Flow analysis     = Query of historical flow data to identify communication patterns and anomalies'))
    lines.append(txt_row('Security group audit = Comparison of current security group membership against expected baseline'))
    lines.append(txt_row('Data source       = Configured NSX/vCenter/switch/cloud connection; requires re-auth after cred'))
    lines.append(txt_row('Collector health  = Status of each site Collector VM; must show connected and collecting for valid'))
    lines.append(txt_row('REST API          = Aria Networks REST API; supports path trace, flow query, alert, and report'))
    lines.append(txt_row('Platform upgrade  = Upgrade Platform VM first using built-in UI wizard before upgrading any'))
    lines.append(txt_row('Collector upgrade = Per-site upgrade of Collector VMs after Platform VM upgrade is validated'))
    lines.append(txt_row('SNMP v3           = SNMPv3 credentials for physical switch collection; compat check needed at upgrade'))
    lines.append(txt_row('VPC flow logs     = Cloud provider flow logs from AWS/Azure ingested for hybrid network visibility'))
    lines.append(txt_row('Alert threshold   = Configurable metric limit that triggers an Aria Networks alert for topology'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-networks-security',
    'docs/virtualization/vmware/aria-operations-for-networks/security/index.md',
    'Aria Networks Security — vIDM SSO, RBAC, TLS, API tokens, audit log',
)
def aria_networks_security():
    """Aria Networks Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Networks — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AD/LDAP auth for user access; data source service accounts for NSX/vCenter/switch collection')))
    lines.append(R(bMid(IV_L, IV_R, 'API key management for REST API access; SNMP v3 credentials for physical switch collection')))
    lines.append(R(bMid(IV_L, IV_R, 'REST API over TLS; role-based access for data visibility; SAML support for SSO integration')))
    lines.append(R(bMid(IV_L, IV_R, 'Roles: Admin (full), Member (view), Auditor (read-only); scoped to data source visibility')))
    lines.append(R(bMid(IV_L, IV_R, 'Credential rotation policy for data source service accounts; API key TTL enforcement')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates platform access · RBAC limits data visibility'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD/LDAP auth'),
        bMid(B2_L, B2_R, 'Admin: full'),
        bMid(B3_L, B3_R, 'REST API TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Local admin'),
        bMid(B2_L, B2_R, 'Member: view'),
        bMid(B3_L, B3_R, 'Collector TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Data src svc acct'),
        bMid(B2_L, B2_R, 'Auditor: read'),
        bMid(B3_L, B3_R, 'Data at rest'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API key mgmt'),
        bMid(B2_L, B2_R, 'Data src access'),
        bMid(B3_L, B3_R, 'Cert mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SAML support'),
        bMid(B2_L, B2_R, 'Report share'),
        bMid(B3_L, B3_R, 'SNMP v3 auth'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Role-based'),
        bMid(B2_L, B2_R, 'Alert mgmt'),
        bMid(B3_L, B3_R, 'Pwd storage'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls user access · RBAC scopes data visibility · TLS and SNMP v3 protect data in transit'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD/LDAP auth', 'Admin role', 'REST TLS', 'Cred rotation', 'Event log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API keys', 'Member role', 'Collector TLS', 'SNMP v3', 'Data src log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Data src accts', 'Auditor role', 'Data encr', 'Cert rotation', 'Alert audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SAML support', 'Report share', 'Pwd storage', 'API key TTL', 'Config changes'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · AD/LDAP · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AD/LDAP           = Active Directory or LDAP integration for user authentication to Aria Networks'))
    lines.append(txt_row('API key           = Authentication token for REST API access; scoped to user role; subject to TTL'))
    lines.append(txt_row('Data source credential = Service account used by Aria Networks to connect to NSX, vCenter, or'))
    lines.append(txt_row('SNMP v3           = SNMPv3 credentials for physical switch collection; provides authentication and'))
    lines.append(txt_row('Service account   = Dedicated non-interactive account used for data source authentication and'))
    lines.append(txt_row('Admin role        = Full access role in Aria Networks; can configure data sources, users, and all'))
    lines.append(txt_row('Member role       = Standard access role; can view topology, run queries, and use path trace features'))
    lines.append(txt_row('Auditor role      = Read-only role; can view all data and reports but cannot make configuration'))
    lines.append(txt_row('TLS encryption    = Transport Layer Security enforced on all REST API and Collector-to-Platform'))
    lines.append(txt_row('Certificate management = Platform and Collector TLS cert lifecycle including rotation and CA trust'))
    lines.append(txt_row('Credential rotation = Periodic renewal of data source service account passwords and API keys per'))
    lines.append(txt_row('Role-based access = RBAC model limiting which data sources and features each user role can access'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-networks-troubleshooting',
    'docs/virtualization/vmware/aria-operations-for-networks/troubleshooting/index.md',
    'Aria Networks Troubleshooting — flow gaps, path analysis errors, collector offline',
)
def aria_networks_troubleshooting():
    """Aria Networks Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Networks — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Collector offline and not collecting data; missing flow data gaps in platform analytics')))
    lines.append(R(bMid(IV_L, IV_R, 'Path trace errors for connectivity troubleshooting; NSX data source stale after credential')))
    lines.append(R(bMid(IV_L, IV_R, 'Physical switch collection gaps due to SNMP misconfiguration or firewall blocking SNMP')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert not firing for topology changes; platform UI unresponsive or API returning errors')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: support bundle export from Platform UI; GSS case with logs and API debug output')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate data source or platform layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collector offline'),
        bMid(B2_L, B2_R, 'Support bundle'),
        bMid(B3_L, B3_R, 'Bundle export'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Flow data gap'),
        bMid(B2_L, B2_R, 'Collector logs'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Path trace err'),
        bMid(B2_L, B2_R, 'Data src status'),
        bMid(B3_L, B3_R, 'Cred reset'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX src stale'),
        bMid(B2_L, B2_R, 'API debug mode'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Phys sw gap'),
        bMid(B2_L, B2_R, 'Flow query dbg'),
        bMid(B3_L, B3_R, 'Version matrix'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert not fire'),
        bMid(B2_L, B2_R, 'SNMP test'),
        bMid(B3_L, B3_R, 'Log collect'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics isolate data source or network layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Collector down', 'Coll log file', '/var/log/coll', 'Bundle export', 'Restart coll'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Flow data gap', 'Data src status', '/var/log/platform', 'GSS P1 case', 'Re-auth src'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Path trace err', 'API debug', '/var/log/api', 'TAM escalate', 'Fix routing'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NSX src stale', 'SNMP test', '/var/log/nsx-ds', 'Cred rotation', 'Re-sync src'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · NSX/vCenter/switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Collector offline      = Collector VM not reachable or service stopped; no data flows to Platform VM'))
    lines.append(txt_row('Flow data gap         = Missing time range in flow analytics; caused by Collector outage or data'))
    lines.append(txt_row('Path trace engine     = Aria Networks component that computes end-to-end path using topology and'))
    lines.append(txt_row('NSX data source       = Configured NSX connection; becomes stale if credentials change without'))
    lines.append(txt_row('SNMP collection       = Physical switch polling via SNMP; gaps caused by cred mismatch or firewall'))
    lines.append(txt_row('Support bundle        = Diagnostic archive generated from Platform UI; contains logs and'))
    lines.append(txt_row('API debug mode        = Verbose logging mode for REST API requests; helps diagnose query and auth'))
    lines.append(txt_row('Data source re-authentication = Process of re-entering credentials for a stale NSX/vCenter data'))
    lines.append(txt_row('Platform restart      = Service or VM restart of the Platform appliance to recover from unresponsive'))
    lines.append(txt_row('Credential rotation   = Update of service account passwords requiring re-auth of all affected data'))
    lines.append(txt_row('Version compatibility  = Aria Networks to NSX/vCenter version matrix; mismatch can cause collection'))
    lines.append(txt_row('Stale topology        = Outdated network map caused by data source not syncing; resolve by'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-lcm-architecture',
    'docs/virtualization/vmware/aria-suite-lifecycle/architecture/index.md',
    'Aria LCM Architecture — LCM appliance, Locker, cert manager, product registry',
)
def aria_lcm_architecture():
    """Aria LCM Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria LCM — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Suite Lifecycle (formerly vRealize Suite LCM) = LCM appliance with embedded vIDM identity')))
    lines.append(R(bMid(IV_L, IV_R, 'Manages lifecycle of Aria products (vRA/vROps/vRLI/vRNI) grouped into named Environments')))
    lines.append(R(bMid(IV_L, IV_R, 'Password Locker stores and encrypts credentials at rest; Certificate Locker manages product')))
    lines.append(R(bMid(IV_L, IV_R, 'Install/upgrade wizard orchestrates product deployment order and pre-check validation')))
    lines.append(R(bMid(IV_L, IV_R, 'DR replication between LCM instances; My VMware integration for product binary downloads')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines LCM appliance role · integrations connect identity and deployment targets'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM appliance'),
        bMid(B2_L, B2_R, 'WS1/vIDM SSO'),
        bMid(B3_L, B3_R, 'LCM sizing 4vCPU'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Environments'),
        bMid(B2_L, B2_R, 'vCenter deploy tgt'),
        bMid(B3_L, B3_R, 'Env naming std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Password Locker'),
        bMid(B2_L, B2_R, 'My VMware DL'),
        bMid(B3_L, B3_R, 'Pwd Locker policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert Locker'),
        bMid(B2_L, B2_R, 'LDAP directory'),
        bMid(B3_L, B3_R, 'Cert Locker std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Install/upgrade'),
        bMid(B2_L, B2_R, 'NSX placement'),
        bMid(B3_L, B3_R, 'Product compat'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DR replication'),
        bMid(B2_L, B2_R, 'NTP/DNS config'),
        bMid(B3_L, B3_R, 'DR replication'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers LCM appliance and Lockers · integrations connect identity and vCenter'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM appliance', 'vIDM/WS1 SSO', 'LCM sizing', 'Single LCM', 'Env naming'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Environments', 'vCenter deploy', 'Env naming', 'DR pair', 'Pwd policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Password Locker', 'My VMware DL', 'Cert policy', 'Multi-env', 'Compat matrix'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert Locker', 'LDAP directory', 'DR replica', 'Enterprise', 'Locker std'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (LCM appliance) · RAM DIMMs · Network NICs · vCenter (deployment target) · Identity provider'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LCM appliance     = Aria Suite Lifecycle virtual appliance; central orchestrator for all Aria'))
    lines.append(txt_row('Environment       = Logical grouping in LCM containing related Aria products sharing the same vIDM'))
    lines.append(txt_row('Password Locker   = Encrypted credential store in LCM; holds passwords for all products and'))
    lines.append(txt_row('Certificate Locker = LCM certificate store; manages TLS certs for Aria products; supports CA-signed'))
    lines.append(txt_row('vIDM (Identity Manager) = Embedded identity provider in LCM; provides SSO across all managed Aria'))
    lines.append(txt_row('Product BOM       = Bill of Materials; version matrix listing compatible Aria product versions per'))
    lines.append(txt_row('Install wizard    = LCM UI workflow for deploying a new Aria product into an existing Environment'))
    lines.append(txt_row('Upgrade wizard    = LCM UI workflow for upgrading Aria products in dependency order with pre-check'))
    lines.append(txt_row('Day-2 operations  = Post-install operations in LCM: cert rotation, password rotation, content'))
    lines.append(txt_row('DR replication    = LCM appliance replication to a secondary site for disaster recovery failover'))
    lines.append(txt_row('My VMware         = Broadcom/VMware portal integration; LCM downloads product binaries directly from'))
    lines.append(txt_row('Workspace ONE     = VMware identity and access management platform; can replace embedded vIDM in LCM'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-lcm-operations',
    'docs/virtualization/vmware/aria-suite-lifecycle/operations/index.md',
    'Aria LCM Operations — product deploy/upgrade, binary sync, cert rotation, Locker',
)
def aria_lcm_operations():
    """Aria LCM Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria LCM — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Environment health dashboard for all Aria products; upgrade wizard for orchestrated upgrades')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate rotation via Certificate Locker; password rotation via Password Locker workflows')))
    lines.append(R(bMid(IV_L, IV_R, 'Content management for environments; request monitoring for all LCM background jobs')))
    lines.append(R(bMid(IV_L, IV_R, 'Upgrade wizard validates BOM compatibility and runs pre-checks before any product upgrade')))
    lines.append(R(bMid(IV_L, IV_R, 'LCM REST API for day-2 automation; vIDM integration API for identity and SSO management')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor all Aria products · lifecycle wizard orchestrates upgrades'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Env health dash'),
        bMid(B2_L, B2_R, 'Upgrade wizard'),
        bMid(B3_L, B3_R, 'LCM REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Product versions'),
        bMid(B2_L, B2_R, 'Pre-chk validate'),
        bMid(B3_L, B3_R, 'Day-2 actions'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert expiry'),
        bMid(B2_L, B2_R, 'BOM compat chk'),
        bMid(B3_L, B3_R, 'Cert API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Request status'),
        bMid(B2_L, B2_R, 'Product upg order'),
        bMid(B3_L, B3_R, 'Pwd Locker API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Locker inventory'),
        bMid(B2_L, B2_R, 'Post-upg val'),
        bMid(B3_L, B3_R, 'Content mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Download catalog'),
        bMid(B2_L, B2_R, 'Cert rotation'),
        bMid(B3_L, B3_R, 'vIDM intg API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch cert expiry and version drift · upgrade wizard enforces order'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM REST API', 'Env: healthy', 'Cert rotation', 'Upgrade wizard', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Day-2 API', 'Products: ok', 'Pwd rotation', 'Pre-chk run', 'Locker backup'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert API', 'Certs: valid', 'Add product', 'BOM compat', 'Restore LCM'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Pwd Locker API', 'Downloads ok', 'Env snapshot', 'Post-upg val', 'DR failover'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (LCM appliance) · RAM DIMMs · Network NICs · vCenter (deploy target) · Internet (My VMware)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Upgrade wizard    = LCM UI workflow that orchestrates Aria product upgrades in correct dependency'))
    lines.append(txt_row('Pre-check validation = Automated checks run before upgrade; verifies disk space, connectivity, and'))
    lines.append(txt_row('Certificate Locker = LCM component for managing TLS certificates; used for cert rotation workflows'))
    lines.append(txt_row('Password Locker   = LCM encrypted credential store; used for password rotation day-2 operations'))
    lines.append(txt_row('BOM compatibility = Verification that all Aria products in an Environment are on a supported version'))
    lines.append(txt_row('Day-2 operations  = Post-install LCM tasks: cert rotation, password rotation, environment snapshots'))
    lines.append(txt_row('Environment health = Dashboard view showing status of all Aria products in each LCM Environment'))
    lines.append(txt_row('Product version   = Currently installed Aria product version tracked by LCM in each Environment'))
    lines.append(txt_row('Request monitoring = LCM job tracker for all background operations; shows progress and error details'))
    lines.append(txt_row('DR replication    = LCM configuration backup replicated to DR site for failover capability'))
    lines.append(txt_row('Content management = LCM workflow for managing Aria Automation content packs and blueprints'))
    lines.append(txt_row('LCM REST API      = REST API for automating LCM day-2 operations: cert rotation, upgrades, locker'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-lcm-security',
    'docs/virtualization/vmware/aria-suite-lifecycle/security/index.md',
    'Aria LCM Security — vIDM SSO, RBAC, Locker vault, TLS, audit log',
)
def aria_lcm_security():
    """Aria LCM Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria LCM — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vIDM/Workspace ONE for SSO; environment-level RBAC (admin/operator/viewer) for LCM access')))
    lines.append(R(bMid(IV_L, IV_R, 'Password Locker encrypts credentials at rest; Certificate Locker manages product TLS certs')))
    lines.append(R(bMid(IV_L, IV_R, 'All API over HTTPS; audit log for all LCM operations including Locker access and upgrades')))
    lines.append(R(bMid(IV_L, IV_R, 'Break-glass local admin account; session timeout enforcement; API key with TTL policy')))
    lines.append(R(bMid(IV_L, IV_R, 'Least privilege: operator role limited to day-2 tasks; viewer role read-only for dashboards')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates LCM access · RBAC scopes environment permissions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vIDM/WS1 SSO'),
        bMid(B2_L, B2_R, 'LCM admin role'),
        bMid(B3_L, B3_R, 'LCM TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP/AD auth'),
        bMid(B2_L, B2_R, 'Operator role'),
        bMid(B3_L, B3_R, 'Locker encr at rest'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Local admin'),
        bMid(B2_L, B2_R, 'Viewer role'),
        bMid(B3_L, B3_R, 'vIDM TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM API key'),
        bMid(B2_L, B2_R, 'Env-level acc'),
        bMid(B3_L, B3_R, 'Cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Break-glass'),
        bMid(B2_L, B2_R, 'Locker read/write'),
        bMid(B3_L, B3_R, 'HTTPS only API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Session timeout'),
        bMid(B2_L, B2_R, 'Request approve'),
        bMid(B3_L, B3_R, 'Log encryption'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth gates LCM access · RBAC scopes per-environment permissions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vIDM/WS1', 'Admin role', 'TLS enforced', 'Cert rotation', 'LCM event log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LDAP/AD', 'Operator role', 'Locker encr', 'API key TTL', 'Request log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API keys', 'Viewer role', 'vIDM TLS', 'Session timeout', 'Cert changes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Break-glass', 'Env access', 'HTTPS only', 'Min permissions', 'Role audit'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (LCM appliance) · RAM DIMMs · Network NICs · Identity provider (vIDM/AD) · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM              = VMware Identity Manager embedded in LCM; provides SSO across all managed Aria'))
    lines.append(txt_row('Workspace ONE     = VMware identity platform; alternative to embedded vIDM for enterprise SSO'))
    lines.append(txt_row('LCM RBAC          = Role-based access control in LCM; scoped per Environment; admin/operator/viewer'))
    lines.append(txt_row('Admin role        = Full LCM access; can install/upgrade products, manage Lockers, and configure'))
    lines.append(txt_row('Operator role     = Day-2 access in LCM; can run cert/password rotation and monitoring; no install'))
    lines.append(txt_row('Viewer role       = Read-only LCM access; can view Environment health and Locker inventory; no write'))
    lines.append(txt_row('Password Locker encryption = AES encryption of all credentials stored in LCM Password Locker at rest'))
    lines.append(txt_row('Certificate Locker = LCM store for TLS certificates; supports rotation workflows and CA-signed cert'))
    lines.append(txt_row('API key           = Bearer token for LCM REST API access; subject to TTL and minimum privilege policy'))
    lines.append(txt_row('HTTPS enforcement = All LCM API and UI traffic requires TLS; HTTP redirected or blocked by policy'))
    lines.append(txt_row('Session timeout   = LCM UI session automatically expires after idle period; configurable per'))
    lines.append(txt_row('Audit event log   = LCM audit trail recording all user actions: logins, upgrades, Locker access,'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'aria-lcm-troubleshooting',
    'docs/virtualization/vmware/aria-suite-lifecycle/troubleshooting/index.md',
    'Aria LCM Troubleshooting — deploy failures, binary sync, cert issues, support bundle',
)
def aria_lcm_troubleshooting():
    """Aria LCM Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria LCM — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Environment install failures; upgrade stall mid-way through product deployment sequence')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate mismatch between LCM and managed products; vIDM connectivity issues for SSO')))
    lines.append(R(bMid(IV_L, IV_R, 'Disk space on LCM appliance blocking upgrades; API errors for day-2 operations')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: LCM UI request logs, /var/log/vlcm, vIDM diagnostics, REST API debug mode')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: LCM support bundle export from UI; pre-check report; TAM escalation for P1')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate LCM or product layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Env install fail'),
        bMid(B2_L, B2_R, 'LCM UI req logs'),
        bMid(B3_L, B3_R, 'LCM support bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Upgrade stall'),
        bMid(B2_L, B2_R, '/var/log/vlcm'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert mismatch'),
        bMid(B2_L, B2_R, 'vIDM diagnostics'),
        bMid(B3_L, B3_R, 'Pre-chk report'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vIDM offline'),
        bMid(B2_L, B2_R, 'REST API debug'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk space'),
        bMid(B2_L, B2_R, 'Pre-chk output'),
        bMid(B3_L, B3_R, 'Version matrix'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API errors'),
        bMid(B2_L, B2_R, 'Product logs'),
        bMid(B3_L, B3_R, 'Log export'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use LCM logs and pre-check output'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Install fail', 'LCM UI logs', '/var/log/vlcm', 'LCM bundle', 'Retry install'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upgrade stall', 'REST API debug', '/var/log/vra', 'GSS P1 case', 'Resume upg'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert mismatch', 'Pre-chk output', '/var/log/vro', 'TAM escalate', 'Re-issue cert'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vIDM offline', 'vIDM diag', '/var/log/vidm', 'Version matrix', 'Restart vIDM'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (LCM appliance) · RAM DIMMs · Network NICs · vCenter · vIDM/Workspace ONE'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Environment installation = LCM workflow deploying Aria products into a new or existing named'))
    lines.append(txt_row('Upgrade orchestration = LCM upgrade wizard that sequences product upgrades to maintain compatibility'))
    lines.append(txt_row('Certificate mismatch  = TLS cert on LCM or product does not match expected CA or SAN; causes auth'))
    lines.append(txt_row('vIDM connectivity     = LCM requires vIDM to be reachable for SSO; vIDM failure breaks all product'))
    lines.append(txt_row('Disk space threshold  = LCM appliance disk usage limit; upgrade aborts if insufficient space detected'))
    lines.append(txt_row('Pre-check validation  = Automated checks before install/upgrade; catches misconfig before deployment'))
    lines.append(txt_row('LCM support bundle    = Diagnostic archive from LCM UI; contains vlcm logs and request history for'))
    lines.append(txt_row('Day-2 operation       = Post-install LCM task such as cert rotation, password rotation, or content'))
    lines.append(txt_row('API debug             = Verbose REST API logging mode in LCM; shows detailed request and response'))
    lines.append(txt_row('BOM version mismatch  = Aria products in an Environment on incompatible versions; blocks LCM upgrade'))
    lines.append(txt_row('TAM escalation        = Escalation to Technical Account Manager for critical LCM P1 upgrade or'))
    lines.append(txt_row('Product log collection = Gathering logs from individual Aria products (vRA/vROps/vRLI) to diagnose'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Aria Automation sub-pages ─────────────────────────────────────────────────

@kb_diagram('aria-auto-arch-how', 'docs/virtualization/vmware/aria-automation/architecture/how-it-works/index.md', 'Aria Automation — how it works')
def _aria_auto_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('Cloud-agnostic self-service automation via blueprints, cloud templates, and resource orchestration.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service Portal (Consumer layer)'), bMid(L2, R2, 'Designer / Admin layer'))))
    lines.append(R(merge(bMid(L1, R1, 'Self-service catalog of deployments'), bMid(L2, R2, 'Cloud templates (YAML/drag-drop)'))))
    lines.append(R(merge(bMid(L1, R1, 'Request → approval → provisioning'), bMid(L2, R2, 'Blueprints define topology + inputs'))))
    lines.append(R(merge(bMid(L1, R1, 'Day-2 actions: resize/snapshot/delete'), bMid(L2, R2, 'Policies: cost, network, storage'))))
    lines.append(R(merge(bMid(L1, R1, 'Role: consumer sees only entitled items'), bMid(L2, R2, 'Projects isolate teams and quotas'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Approved requests flow to the orchestration engine which calls cloud account APIs.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Orchestration Engine'), bMid(L2, R2, 'Cloud Accounts / Endpoints'))))
    lines.append(R(merge(bMid(L1, R1, 'Workflow runs: Aria Orchestrator'), bMid(L2, R2, 'vSphere, AWS, Azure, GCP accounts'))))
    lines.append(R(merge(bMid(L1, R1, 'ABX extensibility actions (FaaS)'), bMid(L2, R2, 'NSX-T for network provisioning'))))
    lines.append(R(merge(bMid(L1, R1, 'Resource lifecycle state machine'), bMid(L2, R2, 'vCenter clusters and datastores'))))
    lines.append(R(merge(bMid(L1, R1, 'Event broker for async events'), bMid(L2, R2, 'Terraform provider integration'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Linux VMs (vRA appliances) · vCenter hosts · DNS · LDAP/AD · NTP · TLS certificates'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cloud template    = YAML descriptor defining resources, inputs, and conditions for a deployment'))
    lines.append(txt_row('Blueprint         = Older term for cloud template; still used in vRA 8.x UI and docs'))
    lines.append(txt_row('Project           = Tenant boundary in vRA; owns cloud accounts, members, and quotas'))
    lines.append(txt_row('Catalog item      = Versioned cloud template published to the service catalog for consumers'))
    lines.append(txt_row('ABX action        = Action-Based Extensibility; serverless function triggered by vRA events'))
    lines.append(txt_row('Aria Orchestrator = Workflow engine embedded in vRA; executes complex multi-step automations'))
    lines.append(txt_row('Day-2 action      = Post-deployment operation (resize, snapshot, decommission) on a resource'))
    lines.append(txt_row('Cloud account     = vRA connection to an infrastructure endpoint (vCenter, AWS, Azure)'))
    lines.append(txt_row('Deployment        = Running instance of a provisioned cloud template with tracked lifecycle'))
    lines.append(txt_row('Approval policy   = Governance rule requiring human sign-off before provisioning proceeds'))
    lines.append(txt_row('Terraform config  = HCL workspace managed by vRA IaaC integration for Terraform providers'))
    lines.append(txt_row('Event subscription= vRA event broker rule mapping resource event to ABX action or workflow'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-arch-int', 'docs/virtualization/vmware/aria-automation/architecture/integrations/index.md', 'Aria Automation — integrations')
def _aria_auto_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('Aria Automation integrates with identity, monitoring, ITSM, and cloud endpoints.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity & SSO Integrations'), bMid(L2, R2, 'Infrastructure Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'vIDM/Workspace ONE: SAML SSO'), bMid(L2, R2, 'vCenter: VM/network/storage prov.'))))
    lines.append(R(merge(bMid(L1, R1, 'Active Directory via LDAP/LDAPS'), bMid(L2, R2, 'NSX-T: segment + security group'))))
    lines.append(R(merge(bMid(L1, R1, 'SCIM group sync for project roles'), bMid(L2, R2, 'AWS/Azure/GCP cloud accounts'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA enforced via vIDM policies'), bMid(L2, R2, 'Terraform Cloud/Enterprise IaaC'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Operational and ITSM integrations close the loop between provisioning and governance.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ITSM / Governance'), bMid(L2, R2, 'Observability'))))
    lines.append(R(merge(bMid(L1, R1, 'ServiceNow: CMDB + request sync'), bMid(L2, R2, 'Aria Operations: cost+health data'))))
    lines.append(R(merge(bMid(L1, R1, 'Jira: ticket creation on deploy'), bMid(L2, R2, 'CloudWatch / Azure Monitor hooks'))))
    lines.append(R(merge(bMid(L1, R1, 'Salt/Puppet/Ansible config mgmt'), bMid(L2, R2, 'Aria Ops for Logs: vRA audit logs'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API: custom integrations'), bMid(L2, R2, 'Webhooks: event broker endpoints'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA appliance VMs · AD servers · NSX managers · vCenter · cloud region endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM             = VMware Identity Manager; provides SSO and MFA for vRA and Aria suite'))
    lines.append(txt_row('SCIM             = System for Cross-domain Identity Management; syncs groups from AD to vIDM'))
    lines.append(txt_row('LDAP integration = vRA reads AD groups to map project members and roles'))
    lines.append(txt_row('NSX-T segment    = Logical network created by vRA during VM provisioning via NSX API'))
    lines.append(txt_row('Cloud account    = vRA connection record holding credentials for a specific cloud endpoint'))
    lines.append(txt_row('IaaC integration = Terraform Cloud/Enterprise workspace managed from vRA catalog'))
    lines.append(txt_row('ServiceNow plugin= vRA plugin syncing deployments and change records to ServiceNow CMDB'))
    lines.append(txt_row('ABX webhook      = ABX action that POSTs JSON to external URL on resource lifecycle event'))
    lines.append(txt_row('Config mgmt      = Ansible/Salt/Puppet bootstrap run as post-deploy ABX or Orchestrator wf'))
    lines.append(txt_row('REST API         = vRA public API (swagger at /vco/api); used for all automation integrations'))
    lines.append(txt_row('Event broker     = vRA pub-sub system; publishes events to subscribed ABX or Orchestrator wf'))
    lines.append(txt_row('Cost integration = Aria Operations cost data surfaced in vRA to show estimated spend per item'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-arch-design', 'docs/virtualization/vmware/aria-automation/architecture/design-standards/index.md', 'Aria Automation — design standards')
def _aria_auto_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('Design patterns for projects, templates, naming, and governance in Aria Automation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Project & Naming Standards'), bMid(L2, R2, 'Template Design Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'One project per team/BU/env tier'), bMid(L2, R2, 'Inputs: only required params exposed'))))
    lines.append(R(merge(bMid(L1, R1, 'Naming: env-team-purpose pattern'), bMid(L2, R2, 'Constraints: machine.count limits'))))
    lines.append(R(merge(bMid(L1, R1, 'Cloud zones linked per project'), bMid(L2, R2, 'Versioning: major for breaking changes'))))
    lines.append(R(merge(bMid(L1, R1, 'Quotas: CPU/memory/storage caps'), bMid(L2, R2, 'No hardcoded IPs or credentials'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Governance standards enforce consistent tagging, approvals, and lifecycle management.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Governance Standards'), bMid(L2, R2, 'Extensibility Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'Approval policies for all prod items'), bMid(L2, R2, 'ABX actions in version control (Git)'))))
    lines.append(R(merge(bMid(L1, R1, 'Cost policies: budget alerts per proj'), bMid(L2, R2, 'Orchestrator workflows tested in dev'))))
    lines.append(R(merge(bMid(L1, R1, 'Lease policies: auto-expire VMs'), bMid(L2, R2, 'No inline scripts in cloud templates'))))
    lines.append(R(merge(bMid(L1, R1, 'Mandatory tags: env/owner/team'), bMid(L2, R2, 'ABX: separate actions per concern'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA appliance cluster · vCenter · NSX-T · AD · Git for IaC and action source control'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cloud zone        = Placement policy linking a project to a vCenter cluster or cloud region'))
    lines.append(txt_row('Quota             = Resource limit (CPU/mem/storage count) enforced per project in vRA'))
    lines.append(txt_row('Lease policy      = Expiry rule: deployments auto-deleted or sent for approval after N days'))
    lines.append(txt_row('Approval policy   = Governance workflow requiring authoriser sign-off before provisioning'))
    lines.append(txt_row('Cost policy       = Budget threshold triggering alert or block when project spend exceeds limit'))
    lines.append(txt_row('Template version  = Immutable snapshot of a cloud template; major versions break consumers'))
    lines.append(txt_row('Constraint tag    = vRA tag applied to a resource (cluster/datastore) to control placement'))
    lines.append(txt_row('Input property    = Template parameter exposed to consumer at request time (dropdown/free text)'))
    lines.append(txt_row('ABX source control= Git repo storing ABX action code; imported via vRA integration setting'))
    lines.append(txt_row('No inline scripts = Design rule: scripts belong in ABX actions, not cloudConfig/customisation'))
    lines.append(txt_row('Naming convention = Consistent env-team-role-seq pattern for VMs, networks, and deployments'))
    lines.append(txt_row('Mandatory tag     = Tag enforced by lease/approval policy; deployment blocked without it'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-ops-backup', 'docs/virtualization/vmware/aria-automation/operations/backup-restore/index.md', 'Aria Automation — backup and restore')
def _aria_auto_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Backup and Restore'))
    lines.append(txt_row())
    lines.append(txt_row('Backup covers vRA Postgres DB, Orchestrator, file-based config, and vIDM state.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'What to Back Up'), bMid(L2, R2, 'Backup Methods'))))
    lines.append(R(merge(bMid(L1, R1, 'Postgres DB (vRA service state)'), bMid(L2, R2, 'VAMI snapshot + export tool'))))
    lines.append(R(merge(bMid(L1, R1, 'Aria Orchestrator DB + workflows'), bMid(L2, R2, 'pg_dump for Postgres directly'))))
    lines.append(R(merge(bMid(L1, R1, 'vIDM: tenant config + user data'), bMid(L2, R2, 'VM snapshot before upgrades'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS certs and private keys'), bMid(L2, R2, 'Offsite: NFS/S3 backup target'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Restore process replays DB + config in order: vIDM → vRA → Orchestrator → verify.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Restore Sequence'), bMid(L2, R2, 'Restore Validation'))))
    lines.append(R(merge(bMid(L1, R1, '1. Restore vIDM from backup'), bMid(L2, R2, 'Login via SSO after vIDM restore'))))
    lines.append(R(merge(bMid(L1, R1, '2. Restore vRA Postgres DB'), bMid(L2, R2, 'Catalog items visible and requestable'))))
    lines.append(R(merge(bMid(L1, R1, '3. Restart vRA services'), bMid(L2, R2, 'Orchestrator workflows listed OK'))))
    lines.append(R(merge(bMid(L1, R1, '4. Validate cloud account sync'), bMid(L2, R2, 'Cloud accounts: data collection green'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA Linux appliances · Postgres cluster · vIDM VM · NFS/S3 backup storage · vCenter'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VAMI              = Virtual Appliance Management Interface; web UI for vRA appliance config'))
    lines.append(txt_row('Postgres DB       = PostgreSQL database holding vRA service state, deployments, and catalog'))
    lines.append(txt_row('pg_dump           = PostgreSQL native backup utility; exports DB to SQL or custom format file'))
    lines.append(txt_row('vIDM backup       = Separate process; export vIDM config + tenant DB before vRA backup'))
    lines.append(txt_row('Orchestrator DB   = Separate Postgres schema holding workflow definitions and run history'))
    lines.append(txt_row('VM snapshot       = vCenter snapshot of appliance; used as pre-upgrade rollback point'))
    lines.append(txt_row('Restore order     = vIDM first (SSO dependency), then vRA, then verify Orchestrator connection'))
    lines.append(txt_row('RPO               = Recovery Point Objective; how much data loss is acceptable (target: ≤24h)'))
    lines.append(txt_row('RTO               = Recovery Time Objective; how fast must vRA be restored (target: ≤4h)'))
    lines.append(txt_row('Cert backup       = Private key + cert chain stored in password-protected archive off-appliance'))
    lines.append(txt_row('Data collection   = vRA process syncing resource inventory from cloud accounts post-restore'))
    lines.append(txt_row('NFS backup target = Network storage mount where backup archives are written and retained'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-ops-cli', 'docs/virtualization/vmware/aria-automation/operations/cli-reference/index.md', 'Aria Automation — CLI reference')
def _aria_auto_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('vRA is operated via REST API, vracli, and VAMI; no traditional SSH-heavy CLI.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vracli (appliance CLI)'), bMid(L2, R2, 'REST API (primary interface)'))))
    lines.append(R(merge(bMid(L1, R1, 'vracli status: service health'), bMid(L2, R2, 'POST /csp/gateway/am/api/login'))))
    lines.append(R(merge(bMid(L1, R1, 'vracli certificate: cert mgmt'), bMid(L2, R2, 'GET /deployment/api/deployments'))))
    lines.append(R(merge(bMid(L1, R1, 'vracli vidm: vIDM config'), bMid(L2, R2, 'POST /blueprint/api/blueprints'))))
    lines.append(R(merge(bMid(L1, R1, 'vracli proxy: proxy settings'), bMid(L2, R2, 'GET /catalog/api/items'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Service and log commands run on the vRA appliance via SSH as root.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service Management'), bMid(L2, R2, 'Log Locations'))))
    lines.append(R(merge(bMid(L1, R1, 'systemctl status vra-cluster'), bMid(L2, R2, '/var/log/vmware/vra/'))))
    lines.append(R(merge(bMid(L1, R1, 'kubectl get pods -n prelude'), bMid(L2, R2, 'journalctl -u vra-cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'kubectl logs <pod> -n prelude'), bMid(L2, R2, '/var/log/vmware/vlcm/ (LCM)'))))
    lines.append(R(merge(bMid(L1, R1, 'vracli status --all (full check)'), bMid(L2, R2, 'kubectl logs <pod> -n prelude'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA Linux appliance VMs · internal Kubernetes (k3s/Rancher) · Postgres · vIDM VM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vracli            = Appliance CLI shipped with vRA; manages certs, vIDM config, proxy, NTP'))
    lines.append(txt_row('prelude namespace  = Kubernetes namespace where vRA microservices run inside the appliance'))
    lines.append(txt_row('kubectl           = Kubernetes CLI; used on vRA appliance to inspect pods and logs'))
    lines.append(txt_row('REST API          = Primary programmatic interface; all UI actions use the same API underneath'))
    lines.append(txt_row('Bearer token      = JWT returned by /csp/gateway/am/api/login; passed as Authorization header'))
    lines.append(txt_row('Swagger UI        = /vco/api/docs (Orchestrator) and /automation-ui/api/docs (vRA) for REST docs'))
    lines.append(txt_row('vracli status     = Reports health of each microservice; green/red output per service'))
    lines.append(txt_row('systemctl         = Linux service manager; vra-cluster is main managed service'))
    lines.append(txt_row('journalctl        = Linux log viewer; use -u vra-cluster for appliance startup logs'))
    lines.append(txt_row('VAMI              = Web-based appliance management at :5480; configure network/NTP/proxy'))
    lines.append(txt_row('ABX CLI           = No dedicated CLI; ABX actions tested via vRA UI Run or REST trigger'))
    lines.append(txt_row('Orchestrator CLI  = vco-controlcenter at :8283 for Orchestrator admin and log download'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-ops-health', 'docs/virtualization/vmware/aria-automation/operations/health-checks/index.md', 'Aria Automation — health checks')
def _aria_auto_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('Daily health checks cover service status, cloud account sync, Orchestrator, and vIDM.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service Health'), bMid(L2, R2, 'Integration Health'))))
    lines.append(R(merge(bMid(L1, R1, 'vracli status --all: all green'), bMid(L2, R2, 'Cloud accounts: data collection OK'))))
    lines.append(R(merge(bMid(L1, R1, 'kubectl get pods: all Running'), bMid(L2, R2, 'vIDM: SSO login works for test user'))))
    lines.append(R(merge(bMid(L1, R1, 'VAMI: disk/mem/CPU in limits'), bMid(L2, R2, 'Orchestrator: endpoint connections OK'))))
    lines.append(R(merge(bMid(L1, R1, 'Postgres replication lag: 0'), bMid(L2, R2, 'NSX-T account: networks enumerated'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Functional checks confirm catalog, requests, and event broker are operating correctly.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Functional Checks'), bMid(L2, R2, 'Alert Thresholds'))))
    lines.append(R(merge(bMid(L1, R1, 'Catalog: items visible to consumers'), bMid(L2, R2, 'Disk: warn >70%, crit >85%'))))
    lines.append(R(merge(bMid(L1, R1, 'Test request: deploy+delete VM'), bMid(L2, R2, 'Postgres lag: warn >30s'))))
    lines.append(R(merge(bMid(L1, R1, 'ABX test action: runs in <30s'), bMid(L2, R2, 'Data collection fail: alert'))))
    lines.append(R(merge(bMid(L1, R1, 'Event broker: subscription active'), bMid(L2, R2, 'Pod restart >3/hour: investigate'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA appliance VMs · Postgres nodes · vIDM VM · vCenter · NSX manager · NTP'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vracli status     = CLI command returning per-service health (green/red) for all vRA services'))
    lines.append(txt_row('Data collection   = vRA background job syncing cloud resource inventory from each account'))
    lines.append(txt_row('Postgres lag      = Replication delay between primary and standby Postgres nodes'))
    lines.append(txt_row('Pod restart count = kubectl restartCount; high value indicates crashing microservice'))
    lines.append(txt_row('VAMI disk check   = /storage partition usage on vRA appliance; log growth can fill disk'))
    lines.append(txt_row('ABX test action   = Simple echo/ping ABX action run to verify FaaS execution pipeline'))
    lines.append(txt_row('Event broker sub  = Active subscription count; zero subscriptions means no event hooks fire'))
    lines.append(txt_row('SSO login test    = Browser login via vIDM to confirm SAML chain is working end-to-end'))
    lines.append(txt_row('Cloud account OK  = vRA data collection status shows green for all registered endpoints'))
    lines.append(txt_row('Orchestrator conn = vRA Orchestrator endpoint reachable and authenticated from vRA service'))
    lines.append(txt_row('NSX enumeration   = vRA lists NSX segments proving NSX-T integration is functional'))
    lines.append(txt_row('Catalog visible   = Consumer role user sees expected items in self-service portal'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-ops-install', 'docs/virtualization/vmware/aria-automation/operations/install-upgrade/index.md', 'Aria Automation — install and upgrade')
def _aria_auto_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('Aria Automation is deployed and upgraded via Aria Suite LCM; manual OVA only for new installs.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Pre-Install / Pre-Upgrade'), bMid(L2, R2, 'Install / Upgrade Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'DNS: fwd+rev for vRA FQDN'), bMid(L2, R2, 'LCM: Environment → Add product'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP: appliance time synced'), bMid(L2, R2, 'Select version from LCM depot'))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter: resource pool + datastore'), bMid(L2, R2, 'LCM pre-checks must pass green'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS cert: SAN matches vRA FQDN'), bMid(L2, R2, 'Deploy OVA → power on → VAMI init'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Post-install: configure vIDM, cloud accounts, projects, and catalog before handover.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Post-Install Config'), bMid(L2, R2, 'Upgrade Validation'))))
    lines.append(R(merge(bMid(L1, R1, 'VAMI: set FQDN, NTP, proxy'), bMid(L2, R2, 'vracli status --all: all green'))))
    lines.append(R(merge(bMid(L1, R1, 'vIDM integration: SAML/LDAP'), bMid(L2, R2, 'Catalog items visible post-upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Cloud accounts: add vCenter/AWS'), bMid(L2, R2, 'Test request: deploy small VM'))))
    lines.append(R(merge(bMid(L1, R1, 'Projects and quotas: set per team'), bMid(L2, R2, 'Orchestrator: workflows intact'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA OVA (4 vCPU/25 GB RAM min) · vCenter · DNS/NTP · LCM appliance · TLS CA'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LCM depot         = Aria Suite LCM binary repository; download product OVAs for managed deploy'))
    lines.append(txt_row('Environment       = LCM grouping of related Aria products sharing vIDM and certificates'))
    lines.append(txt_row('OVA deployment    = vCenter deploy from OVA; used for initial install only (not upgrades)'))
    lines.append(txt_row('VAMI init         = First-boot configuration wizard setting hostname, NTP, password'))
    lines.append(txt_row('Pre-checks        = LCM automated validation of DNS, NTP, cert, and resource before deploy'))
    lines.append(txt_row('vIDM integration  = SAML trust configured in vRA VAMI; enables SSO for all Aria products'))
    lines.append(txt_row('Cloud account add = vRA wizard adding vCenter/AWS/Azure credentials and verifying connectivity'))
    lines.append(txt_row('Project quota     = Resource limits set per project after install; not set by default'))
    lines.append(txt_row('Upgrade sequence  = LCM handles version ordering; do not upgrade vRA before vIDM'))
    lines.append(txt_row('Rollback point    = VM snapshot taken before LCM upgrade; revert if upgrade fails'))
    lines.append(txt_row('Greenfield install = New vRA in a new LCM environment; no migration from older vRA 7.x'))
    lines.append(txt_row('SAN cert          = Subject Alternative Name; must include vRA FQDN for browser trust'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-ops-proc', 'docs/virtualization/vmware/aria-automation/operations/procedures/index.md', 'Aria Automation — operational procedures')
def _aria_auto_ops_proc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Operational Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Common vRA operational tasks: cert rotation, password rotation, account changes, cleanup.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Rotation'), bMid(L2, R2, 'Password Rotation'))))
    lines.append(R(merge(bMid(L1, R1, 'Generate new cert (SAN: vRA FQDN)'), bMid(L2, R2, 'vRA admin password: VAMI → change'))))
    lines.append(R(merge(bMid(L1, R1, 'Import via LCM cert management'), bMid(L2, R2, 'Postgres password: vracli + restart'))))
    lines.append(R(merge(bMid(L1, R1, 'LCM redeploys certs to products'), bMid(L2, R2, 'Cloud account creds: update in UI'))))
    lines.append(R(merge(bMid(L1, R1, 'Validate SSO and catalog after'), bMid(L2, R2, 'Service account: rotate + test ABX'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Account and resource management procedures keep vRA clean and correctly scoped.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cloud Account Management'), bMid(L2, R2, 'Resource Cleanup'))))
    lines.append(R(merge(bMid(L1, R1, 'Add: wizard + test connectivity'), bMid(L2, R2, 'Orphaned deployments: force delete'))))
    lines.append(R(merge(bMid(L1, R1, 'Update creds: edit + reconnect'), bMid(L2, R2, 'Stale catalog items: unpublish+delete'))))
    lines.append(R(merge(bMid(L1, R1, 'Remove: detach from projects first'), bMid(L2, R2, 'Expired leases: auto or manual del'))))
    lines.append(R(merge(bMid(L1, R1, 'Data collection: trigger manually'), bMid(L2, R2, 'ABX logs: retained 30d, purge older'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA appliances · LCM appliance · Postgres · vIDM · vCenter · CA for cert issuance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cert rotation     = Replacing expiring TLS cert on vRA via LCM certificate management UI'))
    lines.append(txt_row('LCM cert push     = LCM distributes updated cert to all products in the Environment'))
    lines.append(txt_row('VAMI password     = Root/admin password for vRA appliance changed via VAMI web UI at :5480'))
    lines.append(txt_row('Postgres creds    = DB credentials stored in vracli config; update and restart service'))
    lines.append(txt_row('Cloud account creds= AWS access key / vCenter password stored in vRA; edit without removing'))
    lines.append(txt_row('Force delete      = vRA admin can hard-delete stuck deployments via API or UI override'))
    lines.append(txt_row('Orphaned resource = Deployment record in vRA with no matching resource in cloud account'))
    lines.append(txt_row('Data collection   = vRA polls cloud accounts for resource inventory; trigger via UI or API'))
    lines.append(txt_row('Lease expiry      = Automated deletion triggered by lease policy when deployment exceeds TTL'))
    lines.append(txt_row('ABX log retention = Action run logs stored 30 days; older logs purged automatically'))
    lines.append(txt_row('Unpublish item    = Remove catalog item from consumer view without deleting the template'))
    lines.append(txt_row('Service account   = vRA uses a service account to authenticate to AD, vCenter, and NSX'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-ops-scripts', 'docs/virtualization/vmware/aria-automation/operations/scripts/index.md', 'Aria Automation — scripts reference')
def _aria_auto_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Scripts Reference'))
    lines.append(txt_row())
    lines.append(txt_row('vRA scripting uses ABX actions (Python/Node/PS), Orchestrator workflows, and REST API calls.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ABX Action Examples'), bMid(L2, R2, 'Orchestrator Script Examples'))))
    lines.append(R(merge(bMid(L1, R1, 'Python: tag VM after deploy'), bMid(L2, R2, 'vCenter: snapshot VM via API'))))
    lines.append(R(merge(bMid(L1, R1, 'Node.js: call ServiceNow REST'), bMid(L2, R2, 'AD: create computer account'))))
    lines.append(R(merge(bMid(L1, R1, 'PowerShell: run WinRM on VM'), bMid(L2, R2, 'NSX: create security group'))))
    lines.append(R(merge(bMid(L1, R1, 'Python: update CMDB record'), bMid(L2, R2, 'DNS: add A record via plugin'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('REST API scripts interact with vRA programmatically for automation and reporting.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'REST API Script Patterns'), bMid(L2, R2, 'Useful Utilities'))))
    lines.append(R(merge(bMid(L1, R1, 'GET token → GET deployments'), bMid(L2, R2, 'vracli status --all (health)'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /request catalog item'), bMid(L2, R2, 'kubectl get pods -n prelude'))))
    lines.append(R(merge(bMid(L1, R1, 'DELETE /deployment/{id} cleanup'), bMid(L2, R2, 'pg_dump for DB backup'))))
    lines.append(R(merge(bMid(L1, R1, 'PATCH /blueprint update template'), bMid(L2, R2, 'curl -k for quick API test'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA appliance · ABX FaaS runtime · Orchestrator embedded · Postgres · vIDM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ABX action        = Serverless function in Python/Node.js/PowerShell executed by vRA event'))
    lines.append(txt_row('Action input      = JSON context object passed to ABX action with resource properties'))
    lines.append(txt_row('Action output     = Key-value pairs returned by ABX to update deployment properties'))
    lines.append(txt_row('Orchestrator wf   = Visual workflow in Aria Orchestrator; called from vRA via ABX or event'))
    lines.append(txt_row('WinRM             = Windows Remote Management; used by PowerShell ABX to run scripts on VMs'))
    lines.append(txt_row('REST bearer token = JWT from /csp/gateway/am/api/login; header: Authorization: Bearer <tok>'))
    lines.append(txt_row('CMDB update       = ABX POST to ServiceNow or custom CMDB REST API after resource creation'))
    lines.append(txt_row('Deployment ID     = UUID assigned to each vRA deployment; used in API paths for operations'))
    lines.append(txt_row('vracli status     = Appliance CLI health check; useful in shell scripts for monitoring'))
    lines.append(txt_row('pg_dump           = PostgreSQL backup tool; script to dump vRA DB to NFS before upgrades'))
    lines.append(txt_row('kubectl           = Kubernetes CLI on vRA appliance; script to check pod health or restart'))
    lines.append(txt_row('Event subscription= ABX or Orchestrator wf registered to run on specific vRA resource events'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-sec-access', 'docs/virtualization/vmware/aria-automation/security/access-control/index.md', 'Aria Automation — access control')
def _aria_auto_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('vRA access is governed by project membership, catalog entitlements, and approval policies.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Roles and Permissions'), bMid(L2, R2, 'Project Access Model'))))
    lines.append(R(merge(bMid(L1, R1, 'System Admin: full vRA access'), bMid(L2, R2, 'Project member: request+manage own'))))
    lines.append(R(merge(bMid(L1, R1, 'Project Admin: manage one project'), bMid(L2, R2, 'Project Admin: manage members+quotas'))))
    lines.append(R(merge(bMid(L1, R1, 'Member: request catalog items'), bMid(L2, R2, 'Entitlement: catalog item → project'))))
    lines.append(R(merge(bMid(L1, R1, 'Viewer: read-only deployments'), bMid(L2, R2, 'No cross-project visibility by default'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Entitlements and policies control which users can request and who must approve.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Catalog Entitlements'), bMid(L2, R2, 'Approval Policies'))))
    lines.append(R(merge(bMid(L1, R1, 'Entitle item → user/group/project'), bMid(L2, R2, 'Policy: approver group + level'))))
    lines.append(R(merge(bMid(L1, R1, 'Source: published catalog items only'), bMid(L2, R2, 'Mandatory for prod-tier catalog items'))))
    lines.append(R(merge(bMid(L1, R1, 'Sharing: item accessible across orgs'), bMid(L2, R2, 'Auto-approve: dev/test environments'))))
    lines.append(R(merge(bMid(L1, R1, 'Revoke: remove entitlement record'), bMid(L2, R2, 'Audit: approval decisions logged'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA appliance · vIDM (user/group source) · AD/LDAP · Postgres (policy store)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('System Admin      = Global vRA admin role; full access to all projects and configurations'))
    lines.append(txt_row('Project Admin     = Role scoped to one project; manages members, quotas, and entitlements'))
    lines.append(txt_row('Project member    = Can request catalog items and manage own deployments within project'))
    lines.append(txt_row('Viewer role       = Read-only access to deployment status; cannot request or modify'))
    lines.append(txt_row('Entitlement       = Record linking a catalog item (or source) to a project or user/group'))
    lines.append(txt_row('Catalog source    = Blueprint/Terraform/ABX library shared as catalog item collection'))
    lines.append(txt_row('Approval policy   = Named rule requiring human authorisation before vRA provisions resources'))
    lines.append(txt_row('Approval level    = Single or multi-level; e.g. manager then finance for expensive items'))
    lines.append(txt_row('Auto-approve      = Policy setting for non-prod items; request proceeds without human input'))
    lines.append(txt_row('vIDM group        = AD group synced to vIDM; mapped to vRA project role'))
    lines.append(txt_row('Cross-project     = Sharing catalog items from one project to another via entitlement'))
    lines.append(txt_row('Audit log         = vRA records who requested, who approved, and timestamps for compliance'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-sec-auth', 'docs/virtualization/vmware/aria-automation/security/authentication/index.md', 'Aria Automation — authentication')
def _aria_auto_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('vRA authentication flows through vIDM (Workspace ONE) via SAML; local accounts are minimal.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Authentication Methods'), bMid(L2, R2, 'vIDM / SSO Flow'))))
    lines.append(R(merge(bMid(L1, R1, 'Primary: SAML via vIDM/WS1'), bMid(L2, R2, 'Browser → vRA → redirect vIDM'))))
    lines.append(R(merge(bMid(L1, R1, 'API: Bearer JWT from CSP gateway'), bMid(L2, R2, 'vIDM → LDAP/SAML IdP validate'))))
    lines.append(R(merge(bMid(L1, R1, 'Local admin: break-glass only'), bMid(L2, R2, 'vIDM returns SAML assertion'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA: enforced via vIDM policy'), bMid(L2, R2, 'vRA validates assertion, issues JWT'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('API authentication uses a short-lived JWT; service accounts use refresh tokens.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'API Auth Flow'), bMid(L2, R2, 'MFA and Policy'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /csp/gateway/am/api/login'), bMid(L2, R2, 'MFA: TOTP, push, or hardware key'))))
    lines.append(R(merge(bMid(L1, R1, 'Payload: {username, password}'), bMid(L2, R2, 'Policy: step-up for admin actions'))))
    lines.append(R(merge(bMid(L1, R1, 'Returns: access_token (JWT/1h TTL)'), bMid(L2, R2, 'Session timeout: 8h default'))))
    lines.append(R(merge(bMid(L1, R1, 'Refresh: use refresh_token to renew'), bMid(L2, R2, 'Failed logins: lockout after 5'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vIDM/WS1 appliance · vRA appliance · AD/LDAP directory · NTP (for SAML timestamps)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM              = VMware Identity Manager; SAML IdP for all Aria suite products'))
    lines.append(txt_row('SAML assertion    = XML token vIDM returns after authenticating user; vRA validates signature'))
    lines.append(txt_row('JWT               = JSON Web Token; short-lived bearer token for vRA REST API calls'))
    lines.append(txt_row('CSP gateway       = Cloud Services Platform auth gateway endpoint in vRA'))
    lines.append(txt_row('Refresh token     = Long-lived token for service accounts; exchange for new access token'))
    lines.append(txt_row('MFA               = Multi-Factor Authentication; enforced via vIDM access policy'))
    lines.append(txt_row('TOTP              = Time-based One-Time Password; one MFA method supported by vIDM'))
    lines.append(txt_row('Break-glass admin = Local vRA admin account used only when vIDM is unavailable'))
    lines.append(txt_row('Access policy     = vIDM policy defining auth method, MFA, and device requirements'))
    lines.append(txt_row('Session timeout   = Duration before vRA redirects user back to vIDM for re-authentication'))
    lines.append(txt_row('Lockout           = Account locked after N failed logins; admin must unlock via vIDM'))
    lines.append(txt_row('Token TTL         = Access token expires in 1 hour; refresh token lasts days/weeks'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-sec-enc', 'docs/virtualization/vmware/aria-automation/security/encryption/index.md', 'Aria Automation — encryption')
def _aria_auto_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('vRA encrypts data in transit (TLS 1.2+) and at rest (vRA secrets store + vCenter D@RE).'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Data in Transit'), bMid(L2, R2, 'Data at Rest'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS 1.2+ all API and UI traffic'), bMid(L2, R2, 'Secrets store: cloud acct creds enc'))))
    lines.append(R(merge(bMid(L1, R1, 'Internal microservices: mTLS'), bMid(L2, R2, 'Postgres: encrypted volume (vSAN D@RE)'))))
    lines.append(R(merge(bMid(L1, R1, 'ABX to external: TLS required'), bMid(L2, R2, 'vIDM: user data encrypted at rest'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert: CA-signed, no self-signed prod'), bMid(L2, R2, 'Backup archives: GPG or vault enc'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Credential security: cloud account passwords stored in vRA secrets, never plaintext.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Management'), bMid(L2, R2, 'Secret Storage'))))
    lines.append(R(merge(bMid(L1, R1, 'LCM manages certs for all products'), bMid(L2, R2, 'vRA secrets API stores creds enc'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert rotation via LCM cert manager'), bMid(L2, R2, 'HashiCorp Vault: external option'))))
    lines.append(R(merge(bMid(L1, R1, 'Minimum: RSA 2048 / ECDSA 256'), bMid(L2, R2, 'No plaintext creds in templates'))))
    lines.append(R(merge(bMid(L1, R1, 'Alert: cert expiry <30d warning'), bMid(L2, R2, 'ABX: use encrypted inputs, not vars'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA appliances · vSAN D@RE for storage · LCM cert store · vIDM · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TLS 1.2+          = Transport Layer Security version 1.2 or higher; enforced on all endpoints'))
    lines.append(txt_row('mTLS              = Mutual TLS; both client and server authenticate via cert in internal comms'))
    lines.append(txt_row('Secrets store     = vRA built-in encrypted KV store for cloud account credentials'))
    lines.append(txt_row('D@RE              = Data at Rest Encryption; vSAN or datastore-level encryption for vRA VMs'))
    lines.append(txt_row('HashiCorp Vault   = External secrets manager; vRA can pull creds from Vault via ABX'))
    lines.append(txt_row('LCM cert manager  = Aria Suite LCM module managing TLS cert lifecycle for all products'))
    lines.append(txt_row('RSA 2048          = Minimum acceptable key size for vRA TLS certificates'))
    lines.append(txt_row('Cert rotation     = Replacing expiring cert via LCM; pushes new cert to all Aria products'))
    lines.append(txt_row('Encrypted input   = vRA cloud template input marked as encrypted; value masked in UI and logs'))
    lines.append(txt_row('Backup encryption = GPG or Vault-wrapped archive for offline backup of vRA DB and certs'))
    lines.append(txt_row('CA-signed cert    = Certificate signed by internal or public CA; required in production'))
    lines.append(txt_row('Cert expiry alert = LCM warns 30 days before cert expiry; schedule rotation in advance'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-sec-hard', 'docs/virtualization/vmware/aria-automation/security/hardening/index.md', 'Aria Automation — hardening')
def _aria_auto_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('Harden vRA by disabling unused services, enforcing TLS, MFA, and minimal access.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Hardening'), bMid(L2, R2, 'Access Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Firewall: allow only 443 inbound'), bMid(L2, R2, 'MFA mandatory for all vRA users'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable SSH after setup (use VAMI)'), bMid(L2, R2, 'Minimum privilege: member not admin'))))
    lines.append(R(merge(bMid(L1, R1, 'Management VLAN: restrict access'), bMid(L2, R2, 'Break-glass: change after each use'))))
    lines.append(R(merge(bMid(L1, R1, 'No direct DB access from prod nets'), bMid(L2, R2, 'vIDM: enforce device compliance'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Configuration hardening removes attack surface and enforces secure defaults.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Configuration Hardening'), bMid(L2, R2, 'Audit and Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS 1.2+ only; disable TLS 1.0/1.1'), bMid(L2, R2, 'Aria Ops: vRA operations audit'))))
    lines.append(R(merge(bMid(L1, R1, 'No self-signed certs in production'), bMid(L2, R2, 'vRA activity log: 90d retention'))))
    lines.append(R(merge(bMid(L1, R1, 'Approval policies on all prod items'), bMid(L2, R2, 'SIEM: forward vRA syslog events'))))
    lines.append(R(merge(bMid(L1, R1, 'Lease policies: no unlimited VMs'), bMid(L2, R2, 'VMware STIG: apply vRA hardening'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA appliance VMs · management VLAN · firewall rules · vIDM · SIEM for log forwarding'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VAMI SSH disable  = After setup, SSH on vRA appliance is disabled; use VAMI for mgmt tasks'))
    lines.append(txt_row('Management VLAN   = Isolated network segment for vRA appliance management interfaces'))
    lines.append(txt_row('Break-glass acct  = Local admin used only in emergency; password rotated after every use'))
    lines.append(txt_row('Device compliance = vIDM policy requiring managed/enrolled device for vRA access'))
    lines.append(txt_row('TLS enforcement   = vRA config disabling TLS 1.0 and 1.1 on all endpoints'))
    lines.append(txt_row('VMware STIG       = Security Technical Implementation Guide published by VMware/DISA'))
    lines.append(txt_row('Syslog forwarding = vRA sends audit events to SIEM via rsyslog or vRealize Log Insight'))
    lines.append(txt_row('Lease policy      = Enforces time limit on deployments; prevents VM sprawl'))
    lines.append(txt_row('Approval policy   = Prevents unreviewed production deployments; mandatory for prod catalog'))
    lines.append(txt_row('Minimum privilege = Users assigned lowest role that meets their work requirements'))
    lines.append(txt_row('Activity log      = vRA built-in audit trail of all requests, approvals, and actions'))
    lines.append(txt_row('SIEM integration  = Security Information and Event Management; aggregates vRA and vIDM logs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-ts-common', 'docs/virtualization/vmware/aria-automation/troubleshooting/common-issues/index.md', 'Aria Automation — common issues')
def _aria_auto_ts_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common vRA issues: failed requests, data collection errors, SSO failures, Orchestrator faults.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Provisioning Failures'), bMid(L2, R2, 'Integration Failures'))))
    lines.append(R(merge(bMid(L1, R1, 'Network: NSX segment not created'), bMid(L2, R2, 'vIDM SSO: cert mismatch/expired'))))
    lines.append(R(merge(bMid(L1, R1, 'Storage: no datastore match policy'), bMid(L2, R2, 'Cloud acct: data collect failed'))))
    lines.append(R(merge(bMid(L1, R1, 'Quota exceeded: project limit hit'), bMid(L2, R2, 'Orchestrator: endpoint unreachable'))))
    lines.append(R(merge(bMid(L1, R1, 'Template invalid: YAML syntax err'), bMid(L2, R2, 'ABX timeout: action >5 min fails'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Check deployment events tab and pod logs for root cause before escalating.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Diagnostic Steps'), bMid(L2, R2, 'Quick Fixes'))))
    lines.append(R(merge(bMid(L1, R1, 'Deployment events tab: error detail'), bMid(L2, R2, 'YAML error: vRA template validator'))))
    lines.append(R(merge(bMid(L1, R1, 'kubectl logs <pod>: service error'), bMid(L2, R2, 'SSO: re-import vIDM cert in VAMI'))))
    lines.append(R(merge(bMid(L1, R1, 'Cloud acct: check data collect log'), bMid(L2, R2, 'Quota: increase or reassign project'))))
    lines.append(R(merge(bMid(L1, R1, 'vracli status: find failed service'), bMid(L2, R2, 'ABX: increase timeout in action'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA appliance · kubectl (k3s) · Postgres · vIDM · NSX manager · vCenter'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Deployment events = vRA timeline of provisioning steps; shows which step and why it failed'))
    lines.append(txt_row('Data collection   = vRA polling cloud endpoints; failure means stale or missing resource list'))
    lines.append(txt_row('NSX segment fail  = vRA cannot create network; check NSX account connection and permissions'))
    lines.append(txt_row('Storage policy    = Placement rule matching VM to datastore; fails if no datastore matches'))
    lines.append(txt_row('Quota exceeded    = Project hit CPU/mem/count limit; admin must raise quota or delete unused'))
    lines.append(txt_row('YAML validation   = vRA cloud template syntax check; run in template editor before publish'))
    lines.append(txt_row('ABX timeout       = Default 5-minute action limit; increase for long-running tasks'))
    lines.append(txt_row('vIDM cert mismatch= TLS cert on vIDM does not match SAN expected by vRA; update VAMI'))
    lines.append(txt_row('Orch endpoint     = Aria Orchestrator endpoint registered in vRA; must be reachable on 443'))
    lines.append(txt_row('Pod log           = kubectl logs <pod-name> -n prelude; per-microservice diagnostic output'))
    lines.append(txt_row('vracli status     = Summary health; find which service is failing before diving into pods'))
    lines.append(txt_row('Cloud acct log    = vRA data collection history; shows timestamps and errors per account'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-ts-diag', 'docs/virtualization/vmware/aria-automation/troubleshooting/diagnostics/index.md', 'Aria Automation — diagnostics')
def _aria_auto_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('Collect vRA logs and support bundle before engaging VMware support for complex issues.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Log Collection'), bMid(L2, R2, 'Support Bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'kubectl logs -n prelude --all'), bMid(L2, R2, 'LCM: Logscraper utility'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log/vmware/vra/ on appliance'), bMid(L2, R2, 'VAMI → Support → Generate bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'journalctl -u vra-cluster -n 500'), bMid(L2, R2, 'Includes k8s pod logs + config'))))
    lines.append(R(merge(bMid(L1, R1, 'ABX run history in vRA UI'), bMid(L2, R2, 'Upload to VMware SR for analysis'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('API-level diagnostics: check connectivity, auth, and response codes systematically.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'API Diagnostics'), bMid(L2, R2, 'DB Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'curl -k /csp/gateway/am/api/login'), bMid(L2, R2, 'psql -U postgres vra DB access'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /deployment/api/deployments'), bMid(L2, R2, 'Check replication: pg_stat_replication'))))
    lines.append(R(merge(bMid(L1, R1, 'Check 401/403/500 response codes'), bMid(L2, R2, 'Check bloat: pg_stat_user_tables'))))
    lines.append(R(merge(bMid(L1, R1, 'Swagger UI /vco/api/docs testing'), bMid(L2, R2, 'Vacuum: VACUUM ANALYZE public.*'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA Linux appliances · k3s Kubernetes · Postgres · vIDM · LCM logscraper'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LCM logscraper    = LCM utility collecting logs from all Aria products into one archive'))
    lines.append(txt_row('Support bundle    = vRA-generated diagnostic archive; includes pod logs, configs, DB state'))
    lines.append(txt_row('kubectl logs --all = Collect logs from all pods across the prelude namespace at once'))
    lines.append(txt_row('journalctl        = Linux log viewer for systemd; captures vra-cluster startup messages'))
    lines.append(txt_row('ABX run history   = Per-action execution log in vRA UI showing inputs, outputs, and errors'))
    lines.append(txt_row('Swagger UI        = /vco/api/docs and /automation-ui/api/docs; test APIs interactively'))
    lines.append(txt_row('401/403 response  = Unauthorised/forbidden; check token expiry or role assignment'))
    lines.append(txt_row('500 response      = Internal server error; look at pod logs for stack trace'))
    lines.append(txt_row('pg_stat_replication= Postgres view showing standby lag; high lag indicates DB issue'))
    lines.append(txt_row('VACUUM ANALYZE    = Postgres maintenance command; reclaims space and updates query stats'))
    lines.append(txt_row('psql access       = Direct Postgres client on vRA appliance; use only for diagnostics'))
    lines.append(txt_row('VMware SR         = Support Request; opened with support bundle attached for complex issues'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-auto-ts-esc', 'docs/virtualization/vmware/aria-automation/troubleshooting/escalation/index.md', 'Aria Automation — escalation')
def _aria_auto_ts_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Automation — Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('Escalate vRA issues when self-service diagnostics are exhausted and impact is unresolved.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Triggers'), bMid(L2, R2, 'Prepare Before Escalating'))))
    lines.append(R(merge(bMid(L1, R1, 'vRA service down > 30 min'), bMid(L2, R2, 'Support bundle (LCM logscraper)'))))
    lines.append(R(merge(bMid(L1, R1, 'Data loss or corruption suspected'), bMid(L2, R2, 'vRA version and patch level'))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade failure mid-process'), bMid(L2, R2, 'Timeline of events and changes'))))
    lines.append(R(merge(bMid(L1, R1, 'Security breach or data exposure'), bMid(L2, R2, 'Deployment events + pod logs'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Open VMware SR with P1 priority for service-down; provide bundle and timeline.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'VMware Support Path'), bMid(L2, R2, 'Internal Escalation'))))
    lines.append(R(merge(bMid(L1, R1, 'SR: my.vmware.com or portal'), bMid(L2, R2, 'Platform team: notify stakeholders'))))
    lines.append(R(merge(bMid(L1, R1, 'P1: live call with GSS engineer'), bMid(L2, R2, 'Change freeze if upgrade-related'))))
    lines.append(R(merge(bMid(L1, R1, 'TAM: escalate for critical accounts'), bMid(L2, R2, 'DR: consider vRA failover if HA'))))
    lines.append(R(merge(bMid(L1, R1, 'KB: search kb.vmware.com first'), bMid(L2, R2, 'Post-incident: RCA within 48h'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRA appliance cluster · LCM · Postgres · vIDM · vCenter · support upload endpoint'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SR                = Support Request; formal case opened with VMware GSS'))
    lines.append(txt_row('P1 priority       = Critical severity; service down with no workaround; live engineer call'))
    lines.append(txt_row('GSS               = Global Support Services; VMware technical support team'))
    lines.append(txt_row('TAM               = Technical Account Manager; premium support contact for critical accounts'))
    lines.append(txt_row('LCM logscraper    = Diagnostic archive tool; collect before calling support'))
    lines.append(txt_row('Support bundle    = Generated from VAMI or LCM; contains pod logs, DB state, configs'))
    lines.append(txt_row('Change freeze     = Halt all non-critical changes during active incident investigation'))
    lines.append(txt_row('RCA               = Root Cause Analysis; post-incident document describing failure and fix'))
    lines.append(txt_row('vRA HA            = High Availability mode; second vRA node can serve if primary fails'))
    lines.append(txt_row('kb.vmware.com     = VMware Knowledge Base; search before opening SR to find known fixes'))
    lines.append(txt_row('Timeline          = Chronological record of events, changes, and symptoms before the issue'))
    lines.append(txt_row('Stakeholder notif = Communicate impact and ETA to application owners and business units'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Aria Operations for Logs sub-pages ───────────────────────────────────────

@kb_diagram('aria-logs-arch-how', 'docs/virtualization/vmware/aria-operations-for-logs/architecture/how-it-works/index.md', 'Aria Ops for Logs — how it works')
def _aria_logs_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('Centralised log aggregation, indexing, and alerting for VMware and multi-cloud environments.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Ingestion Layer'), bMid(L2, R2, 'Analysis Layer'))))
    lines.append(R(merge(bMid(L1, R1, 'Syslog: UDP/TCP 514, TLS 6514'), bMid(L2, R2, 'Real-time indexing of log events'))))
    lines.append(R(merge(bMid(L1, R1, 'vSphere agent: ESXi/vCenter logs'), bMid(L2, R2, 'Interactive analytics: filter+group'))))
    lines.append(R(merge(bMid(L1, R1, 'CF/vRLI agent: app log shipping'), bMid(L2, R2, 'Field extraction: auto + custom'))))
    lines.append(R(merge(bMid(L1, R1, 'REST ingest API for custom sources'), bMid(L2, R2, 'Dashboards: saved query views'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Alerts fire on query thresholds; Aria Ops integration correlates logs with metrics.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Alerting and Forwarding'), bMid(L2, R2, 'Integration'))))
    lines.append(R(merge(bMid(L1, R1, 'Alert: query matches threshold'), bMid(L2, R2, 'Aria Operations: log launch-in-context'))))
    lines.append(R(merge(bMid(L1, R1, 'Notify: email/webhook/ServiceNow'), bMid(L2, R2, 'vCenter: VM log correlation'))))
    lines.append(R(merge(bMid(L1, R1, 'Forward: syslog to SIEM (Splunk)'), bMid(L2, R2, 'NSX: DFW rule match log events'))))
    lines.append(R(merge(bMid(L1, R1, 'Archive: export to S3/NFS for DR'), bMid(L2, R2, 'VxRail: hardware event ingestion'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Linux VM (vRLI appliance) · NIC for syslog ingestion · vCenter · ESXi hosts · NTP'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vRLI              = vRealize Log Insight; former name for Aria Operations for Logs'))
    lines.append(txt_row('Syslog            = Protocol for log transmission; UDP 514 (unreliable) or TCP/TLS 6514'))
    lines.append(txt_row('vSphere agent     = vRLI agent on ESXi and vCenter; ships structured logs directly'))
    lines.append(txt_row('Field extraction  = vRLI parses log text to create queryable structured fields'))
    lines.append(txt_row('Interactive analytics= vRLI UI for free-text search, filter, group, and timeline analysis'))
    lines.append(txt_row('Alert             = Query-based trigger; fires when event count or pattern exceeds threshold'))
    lines.append(txt_row('Content pack      = Pre-built dashboards and alerts for a specific product (e.g. NSX, vSAN)'))
    lines.append(txt_row('Launch in context = Aria Ops alert opens vRLI filtered to same host/timeframe'))
    lines.append(txt_row('SIEM forwarding   = vRLI forwards selected events to Splunk or other SIEM via syslog'))
    lines.append(txt_row('Archive           = Long-term log export to NFS or S3 for compliance retention'))
    lines.append(txt_row('Worker node       = Additional vRLI VM for horizontal scale; master distributes ingestion'))
    lines.append(txt_row('Ingestion API     = REST endpoint for pushing structured JSON logs from custom applications'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-arch-int', 'docs/virtualization/vmware/aria-operations-for-logs/architecture/integrations/index.md', 'Aria Ops for Logs — integrations')
def _aria_logs_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('vRLI integrates with VMware products, SIEM, ITSM, and cloud logging targets.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'VMware Integrations'), bMid(L2, R2, 'External Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter: event and task logs'), bMid(L2, R2, 'Splunk: syslog forward + plugin'))))
    lines.append(R(merge(bMid(L1, R1, 'ESXi: syslog direct to vRLI'), bMid(L2, R2, 'ServiceNow: alert → ticket creation'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX-T: DFW + gateway audit logs'), bMid(L2, R2, 'PagerDuty: alert webhook'))))
    lines.append(R(merge(bMid(L1, R1, 'Aria Operations: launch-in-context'), bMid(L2, R2, 'S3/NFS: archive storage target'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Content packs extend vRLI with product-specific dashboards and parsers.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Content Pack Sources'), bMid(L2, R2, 'Authentication Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'VMware Solution Exchange packs'), bMid(L2, R2, 'vIDM/AD: SSO for vRLI UI access'))))
    lines.append(R(merge(bMid(L1, R1, 'VxRail: hardware event content pack'), bMid(L2, R2, 'LDAP: group-based role assignment'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN: disk/resync/health events'), bMid(L2, R2, 'API key: automation ingest access'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom pack: import ZIP from repo'), bMid(L2, R2, 'TLS: cert-auth between vRLI nodes'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI master/worker VMs · vCenter · ESXi · NSX manager · SIEM target · NTP/DNS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Content pack      = ZIP bundle of dashboards, queries, alerts, and field extractors for a product'))
    lines.append(txt_row('Launch in context = Aria Ops opens vRLI filtered to the alerting host and time window'))
    lines.append(txt_row('SIEM forward      = vRLI sends matching events to Splunk/QRadar via syslog protocol'))
    lines.append(txt_row('ServiceNow alert  = vRLI webhook creates ServiceNow incident on alert threshold breach'))
    lines.append(txt_row('vSolution Exchange= VMware marketplace for content packs and plugins'))
    lines.append(txt_row('API key           = vRLI bearer token for REST ingest API; rotate periodically'))
    lines.append(txt_row('LDAP group        = AD security group mapped to vRLI role (User/Admin) via directory config'))
    lines.append(txt_row('Archive target    = NFS mount or S3 bucket receiving vRLI log archives for long retention'))
    lines.append(txt_row('NSX DFW logs      = Distributed Firewall rule match events ingested by vRLI for security audit'))
    lines.append(txt_row('VxRail pack       = Dell content pack for VxRail hardware events in vRLI'))
    lines.append(txt_row('vSAN pack         = VMware content pack for vSAN health, resync, and disk fault events'))
    lines.append(txt_row('Custom field      = User-defined regex extractor creating a queryable field from log text'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-arch-design', 'docs/virtualization/vmware/aria-operations-for-logs/architecture/design-standards/index.md', 'Aria Ops for Logs — design standards')
def _aria_logs_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('Standards for sizing, retention, clustering, and source onboarding in vRLI deployments.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Sizing Standards'), bMid(L2, R2, 'Retention Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'Master: 4 vCPU/16 GB/1 TB storage'), bMid(L2, R2, 'Hot retention: 90 days on-disk'))))
    lines.append(R(merge(bMid(L1, R1, 'Workers: add for >500 GB/day ingest'), bMid(L2, R2, 'Archive: 1 year NFS/S3 export'))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster: master + 2 workers minimum'), bMid(L2, R2, 'Security events: 1 year hot minimum'))))
    lines.append(R(merge(bMid(L1, R1, 'Network: 10 Gbps for high ingest'), bMid(L2, R2, 'GDPR/compliance: region-local store'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Source onboarding and alert design standards ensure consistent and actionable logging.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Source Onboarding'), bMid(L2, R2, 'Alert Design'))))
    lines.append(R(merge(bMid(L1, R1, 'Install content pack before onboard'), bMid(L2, R2, 'Alert on error patterns, not noise'))))
    lines.append(R(merge(bMid(L1, R1, 'Use TLS syslog (6514) for security'), bMid(L2, R2, 'Threshold: count-based, not always-on'))))
    lines.append(R(merge(bMid(L1, R1, 'Tag sources: env/product/location'), bMid(L2, R2, 'Route: critical → PagerDuty/SNow'))))
    lines.append(R(merge(bMid(L1, R1, 'ESXi: set syslog.global.logHost'), bMid(L2, R2, 'Suppress: known noisy events'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI VMs (master + workers) · 10GbE NIC · NFS/S3 archive · vCenter · ESXi'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Hot retention     = On-disk log storage duration; older data rolled to archive or deleted'))
    lines.append(txt_row('Archive           = Off-appliance export to NFS or S3; compressed, searchable via vRLI'))
    lines.append(txt_row('Worker node       = Additional vRLI VM; master delegates ingestion and query to workers'))
    lines.append(txt_row('Cluster           = Master + 2+ workers sharing index; required for HA and high ingest'))
    lines.append(txt_row('syslog.global.logHost= ESXi advanced config key pointing ESXi syslog to vRLI IP:port'))
    lines.append(txt_row('TLS syslog        = Encrypted log transport on port 6514; prevents log tampering in transit'))
    lines.append(txt_row('Source tag        = Custom field applied at ingest to identify source environment or product'))
    lines.append(txt_row('Content pack      = Pre-built dashboards+alerts for a product; install before onboarding'))
    lines.append(txt_row('Alert threshold   = Count or rate trigger; e.g. fire if >5 auth failures in 5 minutes'))
    lines.append(txt_row('Suppress rule     = vRLI filter excluding known noisy or low-value events from alerting'))
    lines.append(txt_row('GDPR retention    = Data residency requirement; logs stored in same region as source'))
    lines.append(txt_row('Ingest rate       = Measured in GB/day; determines sizing (master-only vs. cluster)'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-ops-backup', 'docs/virtualization/vmware/aria-operations-for-logs/operations/backup-restore/index.md', 'Aria Ops for Logs — backup and restore')
def _aria_logs_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Backup and Restore'))
    lines.append(txt_row())
    lines.append(txt_row('Backup vRLI config, dashboards, and alerts; log data is archived separately to NFS/S3.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'What to Back Up'), bMid(L2, R2, 'Backup Methods'))))
    lines.append(R(merge(bMid(L1, R1, 'Config: alerts, dashboards, packs'), bMid(L2, R2, 'vRLI UI: export config JSON'))))
    lines.append(R(merge(bMid(L1, R1, 'Field extractions and custom queries'), bMid(L2, R2, 'REST API: GET /api/v1/config/export'))))
    lines.append(R(merge(bMid(L1, R1, 'Log archive: NFS/S3 (long-term)'), bMid(L2, R2, 'VM snapshot before upgrades'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS certs and LDAP config'), bMid(L2, R2, 'LCM: logscraper for support bundle'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Restore imports config JSON then repoints sources; log data is not restorable from config.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Restore Sequence'), bMid(L2, R2, 'Restore Validation'))))
    lines.append(R(merge(bMid(L1, R1, '1. Deploy fresh vRLI OVA'), bMid(L2, R2, 'Import: all dashboards visible'))))
    lines.append(R(merge(bMid(L1, R1, '2. Import config JSON backup'), bMid(L2, R2, 'Alerts: re-enabled and firing'))))
    lines.append(R(merge(bMid(L1, R1, '3. Restore LDAP/cert config'), bMid(L2, R2, 'Sources: syslog flowing in'))))
    lines.append(R(merge(bMid(L1, R1, '4. Repoint ESXi/vCenter sources'), bMid(L2, R2, 'SSO: AD login working'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI Linux VM · NFS/S3 archive storage · vCenter · ESXi syslog config · LCM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Config export     = vRLI JSON export containing all settings (alerts/dashboards/sources/packs)'))
    lines.append(txt_row('Config import     = vRLI UI or API import of JSON; overwrites current configuration'))
    lines.append(txt_row('Log archive       = Compressed export of log data to NFS/S3; not part of config backup'))
    lines.append(txt_row('VM snapshot       = vCenter snapshot before vRLI upgrade; fast rollback if upgrade fails'))
    lines.append(txt_row('syslog.global.logHost= Must be re-set on ESXi hosts after vRLI IP changes on restore'))
    lines.append(txt_row('LDAP restore      = AD directory integration must be reconfigured manually after fresh deploy'))
    lines.append(txt_row('Content pack      = Must be reinstalled from marketplace if not in config export'))
    lines.append(txt_row('RPO               = Config RPO: ≤24h (daily export); log RPO: archive job interval'))
    lines.append(txt_row('RTO               = Target: fresh vRLI operational in <2h using config import'))
    lines.append(txt_row('Alert re-enable   = Imported alerts may be disabled; manually enable after import'))
    lines.append(txt_row('Source repoint    = Update syslog destination on devices after vRLI IP/FQDN changes'))
    lines.append(txt_row('LCM logscraper    = Diagnostic tool; not a backup tool; used for support bundles only'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-ops-cli', 'docs/virtualization/vmware/aria-operations-for-logs/operations/cli-reference/index.md', 'Aria Ops for Logs — CLI reference')
def _aria_logs_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('vRLI management uses the REST API, VAMI, and limited SSH commands on the appliance.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'REST API Commands'), bMid(L2, R2, 'VAMI Operations (:9543)'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /api/v1/cluster/nodes health'), bMid(L2, R2, 'Network: IP/hostname/DNS/NTP'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /api/v1/config/export config'), bMid(L2, R2, 'SSL: cert import and management'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /api/v1/config/import restore'), bMid(L2, R2, 'Admin password: change via VAMI'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /api/v1/events/ingest push'), bMid(L2, R2, 'Support bundle: generate here'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SSH commands for service checks and log review on the vRLI Linux appliance.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SSH Appliance Commands'), bMid(L2, R2, 'Log Locations'))))
    lines.append(R(merge(bMid(L1, R1, 'service loginsight status'), bMid(L2, R2, '/var/log/loginsight/'))))
    lines.append(R(merge(bMid(L1, R1, 'service loginsight restart'), bMid(L2, R2, '/var/log/loginsight/runtime.log'))))
    lines.append(R(merge(bMid(L1, R1, 'df -h: check disk usage'), bMid(L2, R2, '/var/log/loginsight/queries.log'))))
    lines.append(R(merge(bMid(L1, R1, 'netstat -tulpn: port check'), bMid(L2, R2, '/var/log/loginsight/alerts.log'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI Linux appliance · VAMI at :9543 · REST API at :443/9000 · NFS storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VAMI              = Virtual Appliance Management Interface at port 9543 for vRLI'))
    lines.append(txt_row('/api/v1           = vRLI REST API base path; all management operations available here'))
    lines.append(txt_row('loginsight service= Linux service managing vRLI processes; restart to clear soft faults'))
    lines.append(txt_row('Ingest API        = POST /api/v1/events/ingest; JSON body with log events + fields'))
    lines.append(txt_row('Config export API = GET /api/v1/config/export; returns full config JSON for backup'))
    lines.append(txt_row('Config import API = POST /api/v1/config/import; restores config from JSON backup'))
    lines.append(txt_row('Cluster nodes API = GET /api/v1/cluster/nodes; shows master+worker health status'))
    lines.append(txt_row('runtime.log       = Main vRLI application log; check for startup errors and exceptions'))
    lines.append(txt_row('queries.log       = Slow or failed query log; diagnose performance issues'))
    lines.append(txt_row('alerts.log        = Alert firing history; confirm alerting is working'))
    lines.append(txt_row('df -h             = Check disk usage on vRLI appliance; /storage partition critical'))
    lines.append(txt_row('API bearer token  = Auth via POST /api/v1/sessions; returns sessionId for API calls'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-ops-health', 'docs/virtualization/vmware/aria-operations-for-logs/operations/health-checks/index.md', 'Aria Ops for Logs — health checks')
def _aria_logs_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('Daily vRLI health check: disk, ingestion rate, cluster nodes, alerts, and source flow.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Health'), bMid(L2, R2, 'Ingestion Health'))))
    lines.append(R(merge(bMid(L1, R1, 'All nodes: green in Cluster section'), bMid(L2, R2, 'Events/sec: steady baseline rate'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk: hot partition <80% used'), bMid(L2, R2, 'Sources: all expected sending logs'))))
    lines.append(R(merge(bMid(L1, R1, 'CPU/RAM: under 80% average'), bMid(L2, R2, 'vSphere sources: heartbeat recent'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP: all nodes time-synced'), bMid(L2, R2, 'Drop rate: near zero if healthy'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Alert and forwarding health confirm the notification pipeline is operational.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Alert Health'), bMid(L2, R2, 'Integration Health'))))
    lines.append(R(merge(bMid(L1, R1, 'Alerts: all enabled (none disabled)'), bMid(L2, R2, 'Aria Ops connection: green'))))
    lines.append(R(merge(bMid(L1, R1, 'Test alert: fire and receive notify'), bMid(L2, R2, 'SIEM forward: test event received'))))
    lines.append(R(merge(bMid(L1, R1, 'Alert history: no unexpected gaps'), bMid(L2, R2, 'SSO: AD login test user works'))))
    lines.append(R(merge(bMid(L1, R1, 'Webhook: HTTP 200 from target'), bMid(L2, R2, 'Archive: last export job succeeded'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI master/worker VMs · disk storage · NTP · ESXi syslog config · SIEM target'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Hot partition      = /storage/var/loginsight/ disk; fills with indexed log data'))
    lines.append(txt_row('Events/sec         = Real-time ingestion rate; baseline varies by environment size'))
    lines.append(txt_row('Drop rate          = Percentage of received syslog messages discarded; should be ~0%'))
    lines.append(txt_row('Heartbeat          = vSphere agent sends periodic log; gap indicates source disconnected'))
    lines.append(txt_row('Cluster nodes      = Master + workers visible in Administration → Cluster section'))
    lines.append(txt_row('Alert test         = Manually trigger alert query to confirm notification delivery'))
    lines.append(txt_row('Webhook 200        = Successful HTTP response from notification target on alert fire'))
    lines.append(txt_row('Archive job        = Scheduled task exporting logs to NFS/S3; check last success time'))
    lines.append(txt_row('Aria Ops conn      = vRLI integration with Aria Operations; shows in Aria Ops admin page'))
    lines.append(txt_row('SSO test           = Browser login test confirming LDAP/AD authentication still working'))
    lines.append(txt_row('SIEM test event    = Send synthetic log and verify it appears in SIEM after forwarding'))
    lines.append(txt_row('NTP sync           = All vRLI nodes must be NTP-synced; time skew breaks cluster consensus'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-ops-install', 'docs/virtualization/vmware/aria-operations-for-logs/operations/install-upgrade/index.md', 'Aria Ops for Logs — install and upgrade')
def _aria_logs_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('vRLI is installed via OVA in vCenter; upgrades use PAK file uploaded to VAMI or LCM.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Pre-Install Requirements'), bMid(L2, R2, 'Install Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'DNS: FQDN fwd+rev for vRLI'), bMid(L2, R2, 'Deploy OVA in vCenter'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP: appliance time synced'), bMid(L2, R2, 'VAMI first-boot: set IP/FQDN/NTP'))))
    lines.append(R(merge(bMid(L1, R1, 'Storage: 1 TB+ for log data'), bMid(L2, R2, 'License: activate in VAMI'))))
    lines.append(R(merge(bMid(L1, R1, 'Firewall: 514/6514/443/9543 open'), bMid(L2, R2, 'vSphere integration: add vCenter'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Upgrade via PAK file in VAMI or managed by LCM; take VM snapshot before upgrading.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Process'), bMid(L2, R2, 'Post-Upgrade Validation'))))
    lines.append(R(merge(bMid(L1, R1, '1. Snapshot master (and workers)'), bMid(L2, R2, 'Cluster: all nodes green'))))
    lines.append(R(merge(bMid(L1, R1, '2. Upload PAK to VAMI or use LCM'), bMid(L2, R2, 'Ingestion: events/sec resumed'))))
    lines.append(R(merge(bMid(L1, R1, '3. Upgrade master first, then workers'), bMid(L2, R2, 'Alerts: all enabled and firing'))))
    lines.append(R(merge(bMid(L1, R1, '4. Monitor VAMI upgrade progress'), bMid(L2, R2, 'SSO and forwarding: verified OK'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI OVA/PAK · vCenter · datastore ≥1 TB · DNS/NTP · LCM (optional managed upgrade)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OVA               = Open Virtual Appliance; initial install format for vRLI'))
    lines.append(txt_row('PAK file          = vRLI upgrade package; upload to VAMI Administration → Upgrade'))
    lines.append(txt_row('VAMI              = Virtual Appliance Management Interface; configure vRLI at :9543'))
    lines.append(txt_row('LCM managed       = Aria Suite LCM can install and upgrade vRLI in managed environments'))
    lines.append(txt_row('vSphere integration= Add vCenter to vRLI; auto-deploys vSphere agent to ESXi hosts'))
    lines.append(txt_row('Syslog ports      = UDP/TCP 514 (plaintext) and TCP 6514 (TLS); must be open in firewall'))
    lines.append(txt_row('Upgrade sequence  = Master upgraded first; workers must be on same version as master'))
    lines.append(txt_row('VM snapshot       = Pre-upgrade rollback point; delete after 48h if upgrade successful'))
    lines.append(txt_row('License           = vRLI license activated in VAMI; free tier: 25 OSI included'))
    lines.append(txt_row('Post-upgrade check= Verify cluster, ingestion, alerts, and forwarding all functional'))
    lines.append(txt_row('Worker join       = Worker nodes re-join cluster automatically after upgrade'))
    lines.append(txt_row('OSI               = Operationally Significant Instance; licensed unit in vRLI'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-ops-proc', 'docs/virtualization/vmware/aria-operations-for-logs/operations/procedures/index.md', 'Aria Ops for Logs — procedures')
def _aria_logs_ops_proc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Common operational procedures: add sources, rotate certs, manage disk, adjust alerts.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Add Log Source'), bMid(L2, R2, 'Certificate Rotation'))))
    lines.append(R(merge(bMid(L1, R1, '1. Install content pack if available'), bMid(L2, R2, '1. Generate new cert with correct SAN'))))
    lines.append(R(merge(bMid(L1, R1, '2. Configure device syslog to vRLI'), bMid(L2, R2, '2. Import cert via VAMI → SSL'))))
    lines.append(R(merge(bMid(L1, R1, '3. Verify events arriving in Explore'), bMid(L2, R2, '3. Restart loginsight service'))))
    lines.append(R(merge(bMid(L1, R1, '4. Tag source: env/product fields'), bMid(L2, R2, '4. Verify sources still sending logs'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Disk and retention management prevent appliance from filling up during high-volume events.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Disk Management'), bMid(L2, R2, 'Alert Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Monitor: Admin → System Monitor'), bMid(L2, R2, 'Add: Queries → create alert'))))
    lines.append(R(merge(bMid(L1, R1, 'Archive: trigger manual export'), bMid(L2, R2, 'Test: fire test from alert editor'))))
    lines.append(R(merge(bMid(L1, R1, 'Purge: reduce retention period'), bMid(L2, R2, 'Route: map to webhook/email/SNow'))))
    lines.append(R(merge(bMid(L1, R1, 'Expand: add worker for more space'), bMid(L2, R2, 'Suppress: noise via suppression rule'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI appliance · /storage disk · NFS archive target · vCenter · syslog sources'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Content pack      = Install before onboarding; provides parsers and dashboards for source'))
    lines.append(txt_row('Explore           = vRLI real-time log viewer; used to confirm new sources are sending'))
    lines.append(txt_row('Source tag        = Custom field on ingested events identifying environment or product'))
    lines.append(txt_row('SAN cert          = Subject Alternative Name; FQDN of vRLI must be in cert SAN list'))
    lines.append(txt_row('loginsight service= Linux service restarted after cert change to apply new TLS cert'))
    lines.append(txt_row('System Monitor    = vRLI Admin section showing disk, CPU, RAM, and ingestion metrics'))
    lines.append(txt_row('Manual archive    = Trigger export of log data to NFS/S3 before disk fills'))
    lines.append(txt_row('Retention period  = Days of hot log data kept on disk; reduce to free space'))
    lines.append(txt_row('Worker node       = Add for more disk and processing; joins cluster automatically'))
    lines.append(txt_row('Alert suppression = Rule preventing noisy known-good events from firing notifications'))
    lines.append(txt_row('Webhook route     = Notification channel sending HTTP POST to external system on alert'))
    lines.append(txt_row('Alert test        = Manual trigger in alert editor; confirms notification delivery'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-ops-scripts', 'docs/virtualization/vmware/aria-operations-for-logs/operations/scripts/index.md', 'Aria Ops for Logs — scripts')
def _aria_logs_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Scripts Reference'))
    lines.append(txt_row())
    lines.append(txt_row('vRLI scripting uses REST API for config export/import, ingest, and query automation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Common REST API Scripts'), bMid(L2, R2, 'ESXi Syslog Config Script'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /api/v1/config/export → backup'), bMid(L2, R2, 'esxcli system syslog config set'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /api/v1/config/import restore'), bMid(L2, R2, '--loghost=ssl://vRLI-FQDN:6514'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /api/v1/events/ingest push'), bMid(L2, R2, 'esxcli system syslog reload'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /api/v1/cluster/nodes status'), bMid(L2, R2, 'Apply via PowerCLI foreach host'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Disk and alert scripts automate routine operations for large-scale deployments.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Appliance Maintenance Scripts'), bMid(L2, R2, 'Monitoring Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'df -h /storage: disk check'), bMid(L2, R2, 'curl GET /api/v1/cluster/nodes'))))
    lines.append(R(merge(bMid(L1, R1, 'service loginsight restart'), bMid(L2, R2, 'Parse JSON: check state==MASTER'))))
    lines.append(R(merge(bMid(L1, R1, 'find /storage -mtime +90 archive'), bMid(L2, R2, 'Alert if disk > 80% threshold'))))
    lines.append(R(merge(bMid(L1, R1, 'netstat -tulpn: verify ports open'), bMid(L2, R2, 'Cron: daily config export to NFS'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI Linux appliance · ESXi hosts · PowerCLI station · NFS for backup scripts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Config export API = GET /api/v1/config/export; JSON backup of all vRLI settings'))
    lines.append(txt_row('Config import API = POST /api/v1/config/import; restore from config JSON backup'))
    lines.append(txt_row('Ingest API        = POST /api/v1/events/ingest; body: {events:[{text,fields,timestamp}]}'))
    lines.append(txt_row('Cluster nodes API = GET /api/v1/cluster/nodes; returns state (MASTER/WORKER/etc)'))
    lines.append(txt_row('esxcli syslog     = ESXi command to configure log destination; run per-host or via PowerCLI'))
    lines.append(txt_row('PowerCLI foreach  = Connect-VIServer then Get-VMHost | foreach {Invoke-EsxCli...}'))
    lines.append(txt_row('loginsight svc    = service loginsight restart; safe restart without data loss'))
    lines.append(txt_row('Cron config backup= Daily cron calling config export API and writing JSON to NFS'))
    lines.append(txt_row('Disk alert script = Checks df -h output; emails/pages if /storage >80% used'))
    lines.append(txt_row('SSL syslog URL    = ssl://vRLI-FQDN:6514 format used in esxcli loghost config'))
    lines.append(txt_row('Sessions API      = POST /api/v1/sessions with creds; returns sessionId for auth'))
    lines.append(txt_row('Bearer header     = Authorization: Bearer <sessionId> on subsequent API calls'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-sec-access', 'docs/virtualization/vmware/aria-operations-for-logs/security/access-control/index.md', 'Aria Ops for Logs — access control')
def _aria_logs_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('vRLI access is controlled by built-in roles and AD group mappings via LDAP integration.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Built-in Roles'), bMid(L2, R2, 'LDAP Group Mapping'))))
    lines.append(R(merge(bMid(L1, R1, 'Super Admin: full configuration'), bMid(L2, R2, 'AD group → vRLI role assignment'))))
    lines.append(R(merge(bMid(L1, R1, 'User: view and query logs only'), bMid(L2, R2, 'LDAP config: Administration → Auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Dashboard User: dashboards only'), bMid(L2, R2, 'Group DN: full distinguished name'))))
    lines.append(R(merge(bMid(L1, R1, 'API: programmatic ingest access'), bMid(L2, R2, 'Test LDAP: verify bind and search'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Network access control limits which systems can push logs and access the UI.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Access Control'), bMid(L2, R2, 'API Access Control'))))
    lines.append(R(merge(bMid(L1, R1, 'Firewall: restrict UI to mgmt nets'), bMid(L2, R2, 'API key: separate from user login'))))
    lines.append(R(merge(bMid(L1, R1, 'Syslog: allow from source CIDR only'), bMid(L2, R2, 'Session token: 30 min default TTL'))))
    lines.append(R(merge(bMid(L1, R1, 'Admin VAMI (:9543): jumphost only'), bMid(L2, R2, 'Rotate API key periodically'))))
    lines.append(R(merge(bMid(L1, R1, 'No direct DB access from prod nets'), bMid(L2, R2, 'Audit: log all admin actions'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI appliance · AD/LDAP server · firewall rules · management VLAN · NTP'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Super Admin       = Full access to all vRLI configuration, sources, and users'))
    lines.append(txt_row('User role         = Can search and view logs and dashboards; cannot change config'))
    lines.append(txt_row('Dashboard User    = Restricted role; view dashboards only, no Explore or admin access'))
    lines.append(txt_row('LDAP integration  = AD connection in vRLI; maps AD groups to Super Admin or User role'))
    lines.append(txt_row('Group DN          = Distinguished Name of AD group used in LDAP group mapping'))
    lines.append(txt_row('LDAP bind user    = Read-only service account vRLI uses to query AD for group membership'))
    lines.append(txt_row('API key           = vRLI static token for ingest API; does not expire unless rotated'))
    lines.append(txt_row('Session token     = Short-lived bearer token returned by /api/v1/sessions login'))
    lines.append(txt_row('VAMI access       = Port 9543; restrict to jump hosts or management network only'))
    lines.append(txt_row('Syslog source ACL = Firewall rule limiting which source IPs can reach vRLI ports'))
    lines.append(txt_row('Audit log         = vRLI logs all login, config change, and admin actions for review'))
    lines.append(txt_row('MFA               = Not native to vRLI; enforce MFA via vIDM if SSO integrated'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-sec-auth', 'docs/virtualization/vmware/aria-operations-for-logs/security/authentication/index.md', 'Aria Ops for Logs — authentication')
def _aria_logs_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('vRLI supports local auth, LDAP/AD integration, and vIDM SSO for enterprise environments.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Authentication Methods'), bMid(L2, R2, 'LDAP/AD Configuration'))))
    lines.append(R(merge(bMid(L1, R1, 'Local: built-in admin account'), bMid(L2, R2, 'Admin → Authentication → Active Dir'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP: AD groups mapped to roles'), bMid(L2, R2, 'Bind DN: service account credentials'))))
    lines.append(R(merge(bMid(L1, R1, 'vIDM SSO: SAML if in LCM env'), bMid(L2, R2, 'Search base: DC=corp,DC=local'))))
    lines.append(R(merge(bMid(L1, R1, 'API: session token from login POST'), bMid(L2, R2, 'Group filter: memberOf attribute'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('vIDM SSO is preferred in Aria Suite deployments for centralised identity management.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vIDM SSO Flow'), bMid(L2, R2, 'Session Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Browser → vRLI → redirect vIDM'), bMid(L2, R2, 'Session TTL: 30 min default'))))
    lines.append(R(merge(bMid(L1, R1, 'vIDM validates user + MFA'), bMid(L2, R2, 'Idle timeout: re-auth required'))))
    lines.append(R(merge(bMid(L1, R1, 'SAML assertion → vRLI grants role'), bMid(L2, R2, 'Multiple sessions: allowed'))))
    lines.append(R(merge(bMid(L1, R1, 'Role derived from AD group via vIDM'), bMid(L2, R2, 'Lockout: handled by vIDM/AD'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI appliance · AD/LDAP server · vIDM (optional SSO) · NTP (SAML timestamp)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Local admin       = Default vRLI built-in account; change password immediately after install'))
    lines.append(txt_row('LDAP bind DN      = Service account used by vRLI to search AD; read-only permissions'))
    lines.append(txt_row('Search base       = AD OU or domain root where vRLI searches for users and groups'))
    lines.append(txt_row('memberOf filter   = LDAP attribute used to check which group a user belongs to'))
    lines.append(txt_row('vIDM SSO          = SAML-based SSO; configured when vRLI is part of Aria Suite LCM env'))
    lines.append(txt_row('SAML assertion    = XML token from vIDM confirming user identity and group membership'))
    lines.append(txt_row('Session token     = Short-lived bearer token for REST API; from POST /api/v1/sessions'))
    lines.append(txt_row('Session TTL       = 30-minute inactivity timeout; re-auth required after expiry'))
    lines.append(txt_row('MFA via vIDM      = Multi-Factor Authentication enforced at vIDM level for all Aria products'))
    lines.append(txt_row('Role from group   = vRLI maps AD group to Super Admin or User; no fine-grained RBAC'))
    lines.append(txt_row('Lockout policy    = AD account lockout applies; managed in AD not in vRLI'))
    lines.append(txt_row('API session       = POST /api/v1/sessions {username, password}; returns sessionId'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-sec-enc', 'docs/virtualization/vmware/aria-operations-for-logs/security/encryption/index.md', 'Aria Ops for Logs — encryption')
def _aria_logs_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('vRLI encrypts log transport (TLS 6514) and UI/API access (TLS 443); storage uses vSAN D@RE.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Data in Transit'), bMid(L2, R2, 'Data at Rest'))))
    lines.append(R(merge(bMid(L1, R1, 'UI/API: TLS 1.2+ on port 443'), bMid(L2, R2, 'Log data: vSAN D@RE or datastore enc'))))
    lines.append(R(merge(bMid(L1, R1, 'Syslog encrypted: TCP TLS 6514'), bMid(L2, R2, 'Archive: compress + GPG encrypt'))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster comms: TLS between nodes'), bMid(L2, R2, 'Config backup: encrypted archive'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP: LDAPS (636) or STARTTLS'), bMid(L2, R2, 'VAMI creds: encrypted at rest'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Certificate management uses VAMI import; LCM manages certs in managed deployments.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Management'), bMid(L2, R2, 'Cipher Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'Import CA cert + key via VAMI SSL'), bMid(L2, R2, 'TLS 1.2 minimum; 1.3 preferred'))))
    lines.append(R(merge(bMid(L1, R1, 'LCM: manages cert if in LCM env'), bMid(L2, R2, 'RSA 2048+ or ECDSA P-256+'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert expiry: alert at <30d warning'), bMid(L2, R2, 'No MD5/SHA-1; SHA-256 minimum'))))
    lines.append(R(merge(bMid(L1, R1, 'SAN: must include vRLI FQDN'), bMid(L2, R2, 'LDAPS: port 636 to AD for auth'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI appliance · vSAN (D@RE) · CA infrastructure · LDAP/AD · NFS archive'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TLS syslog 6514   = Encrypted syslog transport; devices must trust vRLI cert CA'))
    lines.append(txt_row('D@RE              = Data at Rest Encryption; vSAN or datastore encrypts vRLI VM disks'))
    lines.append(txt_row('LDAPS             = LDAP over TLS on port 636; required for secure AD authentication'))
    lines.append(txt_row('STARTTLS          = Upgrade plain LDAP to TLS; alternative to LDAPS'))
    lines.append(txt_row('VAMI SSL section  = Administration → SSL in VAMI; upload new cert and key'))
    lines.append(txt_row('SAN               = Subject Alternative Name; vRLI FQDN must be listed for browser trust'))
    lines.append(txt_row('Cert rotation     = Import new cert via VAMI → restart loginsight service'))
    lines.append(txt_row('LCM cert mgmt     = Aria Suite LCM rotates certs across all products in managed environment'))
    lines.append(txt_row('Archive encryption= GPG or password-zip for archived log exports stored on NFS'))
    lines.append(txt_row('Cluster TLS       = Worker-to-master communication encrypted; cert from same CA'))
    lines.append(txt_row('Cipher suite      = TLS_AES_256_GCM_SHA384 preferred; weak ciphers disabled'))
    lines.append(txt_row('Cert expiry alert = vRLI shows warning banner when cert expires within 30 days'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-sec-hard', 'docs/virtualization/vmware/aria-operations-for-logs/security/hardening/index.md', 'Aria Ops for Logs — hardening')
def _aria_logs_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('Harden vRLI with TLS syslog, firewall restrictions, minimal admin accounts, and audit.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Hardening'), bMid(L2, R2, 'Access Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Use TLS 6514, not UDP 514'), bMid(L2, R2, 'Minimum accounts: disable unused'))))
    lines.append(R(merge(bMid(L1, R1, 'Firewall: UI (443) mgmt-net only'), bMid(L2, R2, 'Admin password: strong + rotated'))))
    lines.append(R(merge(bMid(L1, R1, 'VAMI (9543): jump host only'), bMid(L2, R2, 'LDAP: use LDAPS (636), not plain'))))
    lines.append(R(merge(bMid(L1, R1, 'SSH: disable after initial setup'), bMid(L2, R2, 'MFA via vIDM if SSO configured'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Audit and monitoring settings ensure log integrity and compliance for vRLI itself.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Configuration Hardening'), bMid(L2, R2, 'Audit and Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable TLS 1.0/1.1 on all ports'), bMid(L2, R2, 'Syslog vRLI itself to SIEM'))))
    lines.append(R(merge(bMid(L1, R1, 'CA-signed cert; no self-signed prod'), bMid(L2, R2, 'Admin action audit in vRLI logs'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP: synced for log timestamp trust'), bMid(L2, R2, 'VMware STIG: apply vRLI guide'))))
    lines.append(R(merge(bMid(L1, R1, 'No plaintext syslog from prod hosts'), bMid(L2, R2, 'Log retention: meet compliance min'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI appliance · management VLAN · firewall · vIDM (SSO+MFA) · AD LDAPS · CA'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('UDP 514 disable   = UDP syslog provides no encryption or auth; replace with TLS 6514'))
    lines.append(txt_row('VAMI restriction  = Restrict port 9543 to jump hosts only; avoid internet exposure'))
    lines.append(txt_row('SSH disable       = SSH to vRLI appliance disabled post-setup; use VAMI for maintenance'))
    lines.append(txt_row('LDAPS             = LDAP over TLS; prevents AD credential sniffing'))
    lines.append(txt_row('Self-signed cert  = Acceptable in lab; production requires CA-signed cert'))
    lines.append(txt_row('VMware STIG       = Security hardening guide; follow applicable controls for vRLI'))
    lines.append(txt_row('Log vRLI to SIEM  = vRLI forwards its own admin audit events to Splunk/SIEM'))
    lines.append(txt_row('Timestamp trust   = NTP sync ensures log timestamps are accurate; critical for forensics'))
    lines.append(txt_row('Compliance min    = Many regulations require ≥90d hot + 1yr archive log retention'))
    lines.append(txt_row('TLS 1.0/1.1       = Deprecated protocols; disable in vRLI SSL config'))
    lines.append(txt_row('Admin audit       = vRLI logs all login, config change events in runtime.log'))
    lines.append(txt_row('MFA enforcement   = Handled by vIDM access policy if vRLI uses SSO'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-ts-common', 'docs/virtualization/vmware/aria-operations-for-logs/troubleshooting/common-issues/index.md', 'Aria Ops for Logs — common issues')
def _aria_logs_ts_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common vRLI issues: disk full, missing sources, alert failures, LDAP auth errors.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Ingestion Issues'), bMid(L2, R2, 'Authentication Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Source not sending: check firewall'), bMid(L2, R2, 'LDAP auth fail: bind account locked'))))
    lines.append(R(merge(bMid(L1, R1, 'Drop rate high: disk nearly full'), bMid(L2, R2, 'SSO fail: cert mismatch vIDM/vRLI'))))
    lines.append(R(merge(bMid(L1, R1, 'ESXi logs missing: syslog not set'), bMid(L2, R2, 'Login loop: check SAML assertion'))))
    lines.append(R(merge(bMid(L1, R1, 'High ingest lag: worker overloaded'), bMid(L2, R2, 'Local admin: password forgotten'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Check disk first; full disk stops ingestion and can corrupt the vRLI index.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Alert and Cluster Issues'), bMid(L2, R2, 'Quick Fixes'))))
    lines.append(R(merge(bMid(L1, R1, 'Alert not firing: check disabled'), bMid(L2, R2, 'Disk full: archive + purge old data'))))
    lines.append(R(merge(bMid(L1, R1, 'Webhook 500: target URL changed'), bMid(L2, R2, 'Source missing: check syslog config'))))
    lines.append(R(merge(bMid(L1, R1, 'Worker disconnected: NTP skew'), bMid(L2, R2, 'LDAP: reset bind account password'))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster split: network partition'), bMid(L2, R2, 'Alert: re-enable + test fire'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI appliance · /storage disk · ESXi syslog config · AD/LDAP · vIDM · firewall'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Drop rate         = Events discarded; spikes when disk full or ingest rate exceeds capacity'))
    lines.append(txt_row('Disk full         = /storage partition fills with log index; causes ingestion to stop'))
    lines.append(txt_row('syslog not set    = ESXi syslog.global.logHost not configured or pointing to wrong host'))
    lines.append(txt_row('Bind account lock = LDAP service account locked in AD; vRLI cannot authenticate users'))
    lines.append(txt_row('SAML loop         = Browser redirects to vIDM repeatedly; check cert SAN and clock sync'))
    lines.append(txt_row('Alert disabled    = Imported or upgraded alerts may be disabled; manually re-enable'))
    lines.append(txt_row('Webhook 500       = HTTP error from alert target; update URL or check target service'))
    lines.append(txt_row('NTP skew          = Time difference between vRLI nodes breaks cluster consensus'))
    lines.append(txt_row('Cluster split     = Network partition causing master and worker to lose contact'))
    lines.append(txt_row('Archive + purge   = Export logs to NFS then reduce retention period to free disk'))
    lines.append(txt_row('Ingest lag        = Events delayed; add worker node or reduce ingest sources'))
    lines.append(txt_row('Worker overloaded = Worker CPU/RAM at limit; scale out by adding another worker VM'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-ts-diag', 'docs/virtualization/vmware/aria-operations-for-logs/troubleshooting/diagnostics/index.md', 'Aria Ops for Logs — diagnostics')
def _aria_logs_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('Diagnose vRLI problems using system monitor, runtime logs, API checks, and support bundle.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Built-in Diagnostics'), bMid(L2, R2, 'Log File Review'))))
    lines.append(R(merge(bMid(L1, R1, 'Admin → System Monitor: disk/CPU'), bMid(L2, R2, '/var/log/loginsight/runtime.log'))))
    lines.append(R(merge(bMid(L1, R1, 'Admin → Cluster: node status'), bMid(L2, R2, '/var/log/loginsight/queries.log'))))
    lines.append(R(merge(bMid(L1, R1, 'API: GET /api/v1/cluster/nodes'), bMid(L2, R2, '/var/log/loginsight/alerts.log'))))
    lines.append(R(merge(bMid(L1, R1, 'Explore: search for ingest errors'), bMid(L2, R2, '/var/log/vmware/vra/ (if LCM)'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Generate support bundle from VAMI before contacting VMware support for complex issues.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Support Bundle'), bMid(L2, R2, 'Network Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'VAMI → Support → Download bundle'), bMid(L2, R2, 'netstat -tulpn: ports listening'))))
    lines.append(R(merge(bMid(L1, R1, 'Includes: logs + config + DB state'), bMid(L2, R2, 'tcpdump: verify syslog packets'))))
    lines.append(R(merge(bMid(L1, R1, 'LCM logscraper: multi-product diag'), bMid(L2, R2, 'nc -zv host 514: test port reach'))))
    lines.append(R(merge(bMid(L1, R1, 'Upload to VMware SR for analysis'), bMid(L2, R2, 'curl -k :443/api/v1: API reachable'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI appliance · VAMI at :9543 · LCM logscraper · AD/LDAP · firewall'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('System Monitor    = vRLI Admin section showing real-time disk/CPU/RAM/ingestion metrics'))
    lines.append(txt_row('runtime.log       = Main vRLI log; Java exceptions, startup errors, cluster events'))
    lines.append(txt_row('queries.log       = Records slow or failed queries; diagnose search performance'))
    lines.append(txt_row('alerts.log        = Alert firing log; check if alerts fired and notifications sent'))
    lines.append(txt_row('Cluster nodes API = GET /api/v1/cluster/nodes; shows node state and role'))
    lines.append(txt_row('VAMI support bundle= Downloads all vRLI logs and config in one archive'))
    lines.append(txt_row('LCM logscraper    = Multi-product diagnostic tool for Aria Suite managed environments'))
    lines.append(txt_row('tcpdump           = Capture syslog packets on vRLI NIC to confirm devices are sending'))
    lines.append(txt_row('nc -zv            = Netcat port test; confirm syslog port reachable from source host'))
    lines.append(txt_row('curl -k           = Quick API connectivity test; check vRLI REST API responds'))
    lines.append(txt_row('netstat -tulpn     = List listening ports; verify 514, 6514, 443, 9543 are open'))
    lines.append(txt_row('VMware SR         = Support Request; provide bundle + timeline + version details'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('aria-logs-ts-esc', 'docs/virtualization/vmware/aria-operations-for-logs/troubleshooting/escalation/index.md', 'Aria Ops for Logs — escalation')
def _aria_logs_ts_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Aria Operations for Logs — Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('Escalate vRLI issues when log ingestion loss or corruption impacts operations and compliance.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Triggers'), bMid(L2, R2, 'Pre-Escalation Checklist'))))
    lines.append(R(merge(bMid(L1, R1, 'Log ingestion stopped > 1 hour'), bMid(L2, R2, 'Support bundle from VAMI'))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster node down, cannot recover'), bMid(L2, R2, 'vRLI version and patch level'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk corruption / index error'), bMid(L2, R2, 'Timeline: when ingestion stopped'))))
    lines.append(R(merge(bMid(L1, R1, 'Compliance data loss suspected'), bMid(L2, R2, 'System monitor screenshot'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Open VMware SR with support bundle; engage TAM for compliance-critical data loss.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'VMware Support Path'), bMid(L2, R2, 'Internal Actions'))))
    lines.append(R(merge(bMid(L1, R1, 'SR: my.vmware.com or portal'), bMid(L2, R2, 'Notify security/compliance team'))))
    lines.append(R(merge(bMid(L1, R1, 'P2: node down; P1: full data loss'), bMid(L2, R2, 'Redirect sources to SIEM direct'))))
    lines.append(R(merge(bMid(L1, R1, 'TAM: compliance data loss P1'), bMid(L2, R2, 'Change freeze during investigation'))))
    lines.append(R(merge(bMid(L1, R1, 'KB: search before opening SR'), bMid(L2, R2, 'RCA: document and present in 48h'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vRLI appliance · /storage disk · VAMI · VMware SR portal · SIEM fallback target'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Support bundle    = VAMI-generated archive; mandatory before opening VMware SR'))
    lines.append(txt_row('P1 SR             = Critical: full log ingestion loss; compliance risk; live call'))
    lines.append(txt_row('P2 SR             = Major: single node down but cluster partial; business hours'))
    lines.append(txt_row('TAM               = Technical Account Manager; escalation path for premium accounts'))
    lines.append(txt_row('SIEM fallback     = Direct syslog to Splunk/SIEM while vRLI is being recovered'))
    lines.append(txt_row('Compliance notify = Inform security/compliance team if regulated log data lost'))
    lines.append(txt_row('Change freeze     = Halt all changes during active incident to preserve evidence'))
    lines.append(txt_row('RCA               = Root Cause Analysis; required after P1 by most compliance frameworks'))
    lines.append(txt_row('Index error       = vRLI log data index corruption; may require rebuild with data loss'))
    lines.append(txt_row('Disk corruption   = /storage filesystem error; requires vRLI restore from backup'))
    lines.append(txt_row('Cluster node down = Worker or master unavailable; check NTP + network + disk'))
    lines.append(txt_row('kb.vmware.com     = Search VMware KB before opening SR; known fixes often available'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
