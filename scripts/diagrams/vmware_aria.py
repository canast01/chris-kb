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
