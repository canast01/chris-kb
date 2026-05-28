"""
Virtualization operations: health checks and runbooks.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import kb_diagram, make_helpers, bTop, bMid, bBot, sections, arrow, connector, merge, title_border, row

W2 = 103
IV_L, IV_R = 3, 99
B1_L, B1_R = 3, 50
B2_L, B2_R = 53, 99
M1, M2 = 26, 76
TB1_L, TB1_R = 3, 33
TB2_L, TB2_R = 36, 66
TB3_L, TB3_R = 69, 99
TM1, TM2, TM3 = 18, 51, 84
PD1, PD2, PD3, PD4 = 22, 41, 61, 80


@kb_diagram(
    'virtualization-operations-health-checks',
    'docs/virtualization/operations/health-checks/index.md',
    'Virtualization health checks — daily, capacity, and change-window checks',
)
def virt_health_checks():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Virtualization Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('  Structured checks across daily operations, capacity planning, and change management'))
    lines.append(txt_row())
    lines.append(R(arrow([TM1, TM2, TM3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(TB1_L, TB1_R), bTop(TB2_L, TB2_R), bTop(TB3_L, TB3_R))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Daily (~15 min)'), bMid(TB2_L, TB2_R, 'Capacity (weekly)'), bMid(TB3_L, TB3_R, 'Pre / Post Change'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, '─────────────────'), bMid(TB2_L, TB2_R, '─────────────────'), bMid(TB3_L, TB3_R, '─────────────────'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'vCenter alarms'), bMid(TB2_L, TB2_R, 'CPU < 70% target'), bMid(TB3_L, TB3_R, 'Alarms cleared'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Host connectivity'), bMid(TB2_L, TB2_R, 'RAM balloon = 0'), bMid(TB3_L, TB3_R, 'vSAN healthy'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'vSAN health'), bMid(TB2_L, TB2_R, 'Storage < 80%'), bMid(TB3_L, TB3_R, 'Snapshots clear'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Datastore space'), bMid(TB2_L, TB2_R, 'Growth trend OK'), bMid(TB3_L, TB3_R, 'Backups confirmed'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'VM state check'), bMid(TB2_L, TB2_R, 'Forecast 90 days'), bMid(TB3_L, TB3_R, 'HA/DRS active'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Backup status'), bMid(TB2_L, TB2_R, 'Licence headroom'), bMid(TB3_L, TB3_R, 'App owner sign-off'))))
    lines.append(R(merge(bBot(TB1_L, TB1_R), bBot(TB2_L, TB2_R), bBot(TB3_L, TB3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  HA         = High Availability; restarts VMs on surviving hosts when a host fails'))
    lines.append(txt_row('  DRS        = Distributed Resource Scheduler; balances VM load across cluster hosts'))
    lines.append(txt_row('  vSAN       = VMware hyper-converged storage; health = no resync, no degraded objects'))
    lines.append(txt_row('  Balloon    = VMware memory reclaim driver; non-zero = host under memory pressure'))
    lines.append(txt_row('  Swap       = VM disk-based memory swap; non-zero = critical memory shortage on host'))
    lines.append(txt_row('  Datastore  = Storage volume presented to ESXi; monitor used % and provisioning ratio'))
    lines.append(txt_row('  VAMI       = vCenter Appliance Management Interface; port 5480; cert and patch mgmt'))
    lines.append(txt_row('  Alarm      = vCenter triggered alert; P1=red critical, P2=yellow warning, P3=info'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-health-checks-alert-review',
    'docs/virtualization/operations/health-checks/alert-review/index.md',
    'Alert health check — sources, triage priority, and response actions',
)
def virt_alert_review():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Alert Health Check — Review Flow'))
    lines.append(txt_row())
    lines.append(txt_row('  Review all active alerts every morning; triage by priority; assign or suppress'))
    lines.append(txt_row())
    lines.append(R(arrow([TM1, TM2, TM3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(TB1_L, TB1_R), bTop(TB2_L, TB2_R), bTop(TB3_L, TB3_R))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Alert Sources'), bMid(TB2_L, TB2_R, 'Priority Triage'), bMid(TB3_L, TB3_R, 'Response Actions'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, '─────────────────'), bMid(TB2_L, TB2_R, '─────────────────'), bMid(TB3_L, TB3_R, '─────────────────'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'vCenter alarms'), bMid(TB2_L, TB2_R, 'P1 = red critical'), bMid(TB3_L, TB3_R, 'P1 → immediate'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Aria Operations'), bMid(TB2_L, TB2_R, 'P2 = yellow warn'), bMid(TB3_L, TB3_R, 'P2 → assign owner'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Pure1 / iDRAC'), bMid(TB2_L, TB2_R, 'P3 = blue info'), bMid(TB3_L, TB3_R, 'P3 → log + weekly'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Monitoring tools'), bMid(TB2_L, TB2_R, ''), bMid(TB3_L, TB3_R, 'False pos → tune'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Manual reports'), bMid(TB2_L, TB2_R, ''), bMid(TB3_L, TB3_R, 'Repeat → RCA req'))))
    lines.append(R(merge(bBot(TB1_L, TB1_R), bBot(TB2_L, TB2_R), bBot(TB3_L, TB3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  P1           = Critical; immediate action; escalate if not resolved within 30 min'))
    lines.append(txt_row('  P2           = Warning; assign an owner; resolve within business hours'))
    lines.append(txt_row('  P3           = Informational; log and review weekly; no immediate action required'))
    lines.append(txt_row('  False positive = Alert fires incorrectly; tune threshold or suppress after RCA'))
    lines.append(txt_row('  Repeat alert  = Same alert fires repeatedly; trigger RCA to find root cause'))
    lines.append(txt_row('  Aria Ops      = VMware Aria Operations; collects metrics and fires perf alerts'))
    lines.append(txt_row('  Pure1         = Pure Storage cloud portal; array health, capacity, and alerts'))
    lines.append(txt_row('  iDRAC         = Dell integrated remote access; hardware alerts: temp, disk, PSU'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-health-checks-daily-health-check',
    'docs/virtualization/operations/health-checks/daily-health-check/index.md',
    'Daily health check — morning sequence covering all critical components',
)
def virt_daily_health_check():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Daily Health Check — Morning Sequence'))
    lines.append(txt_row())
    lines.append(txt_row('  Run every morning; target completion under 15 minutes; document failures in the change log'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['Step', 'Component', 'Pass Condition', 'On FAIL', 'Tool'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['──────────────', '──────────────', '───────────────', '──────────────', '──────────────'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['1  vCenter', 'No red alarms', 'All green/clear', 'Investigate 1st', 'vSphere Client'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['2  Host status', 'All connected', 'No disconnects', 'Restart vpxa', 'vSphere Client'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['3  Cluster HA', 'HA enabled', 'Admission OK', 'Check HA logs', 'esxcli / UI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['4  vSAN health', 'Green status', 'No resync', 'vSAN Health UI', 'vSAN Health UI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['5  Datastores', '< 80% used', 'No overprov.', 'Free up space', 'Storage view'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['6  VM state', 'All powered on', 'No stuck tasks', 'Force-end task', 'vSphere Client'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['7  Backup jobs', 'All succeeded', 'No failed jobs', '→ backup runbook', 'Backup console'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['8  Snapshots', 'None stale', '< 24h or 10 GB', 'Consolidate VMs', 'Snapshot mgr'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  vpxa       = VMware vCenter Agent on each ESXi host; restart restores host connection'))
    lines.append(txt_row('  hostd      = ESXi host management daemon; restart if vpxa restart fails'))
    lines.append(txt_row('  HA admission = Policy ensuring enough cluster capacity to restart all protected VMs'))
    lines.append(txt_row('  Resync     = vSAN rebuilding data to meet the storage policy; do not patch during'))
    lines.append(txt_row('  Consolidate = Merging stale snapshots into the VM base disk; run via vSphere Client'))
    lines.append(txt_row('  Stuck task  = vCenter task in running state > 30 min; cancel via task manager panel'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-health-checks-capacity-review',
    'docs/virtualization/operations/health-checks/capacity-review/index.md',
    'Capacity review — CPU, RAM, storage, vSAN, and licensing thresholds',
)
def virt_capacity_review():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Capacity Review — Weekly Resource Check'))
    lines.append(txt_row())
    lines.append(txt_row('  Run weekly and after any significant workload addition; forecast 90 days ahead'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['Resource', 'Green', 'Amber — action', 'Red — escalate', 'Frequency'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['──────────────', '──────────────', '───────────────', '──────────────', '──────────────'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['CPU cluster', '< 70% avg', '70-85% → plan', '85%+ → P1 now', 'Daily + weekly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['RAM balloon', '0 balloon', 'Any → investig.', '> 0 swap → P1', 'Daily'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['Datastore', '< 75% used', '75-85% → free', '85%+ → expand', 'Daily'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['vSAN capacity', '< 70% used', '70-80% → plan', '80%+ → P1 now', 'Weekly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['Licensing', 'All covered', 'Expiry < 60 d', 'Expiry < 30 d', 'Monthly'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Balloon    = Memory reclaim driver inflates inside the VM; signals host memory pressure'))
    lines.append(txt_row('  Swap       = Host swaps VM memory to disk; severe performance impact; treat as P1'))
    lines.append(txt_row('  Headroom   = Spare capacity after HA failover reservation is accounted for'))
    lines.append(txt_row('  Thin prov. = Allocating more virtual disk than physical; monitor actual used, not alloc'))
    lines.append(txt_row('  Forecast   = Project current growth rate 90 days; order hardware before hitting amber'))
    lines.append(txt_row('  vSAN slack = vSAN requires ~25% free space for rebuild operations; do not fill beyond 70%'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-health-checks-management-access-check',
    'docs/virtualization/operations/health-checks/management-access-check/index.md',
    'Management access check — DNS, HTTPS, and login validation for all endpoints',
)
def virt_mgmt_access_check():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Management Access Check'))
    lines.append(txt_row())
    lines.append(txt_row('  Run weekly; confirm DNS, HTTPS, and login for every management endpoint'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check Sequence (per endpoint)'), bMid(B2_L, B2_R, 'Endpoints to Verify'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '──────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '1. DNS resolves FQDN?'), bMid(B2_L, B2_R, 'vCenter FQDN (HTTPS)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '   FAIL → check DNS / HOSTS'), bMid(B2_L, B2_R, '  └─ SSO login test'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2. HTTPS port 443 reachable?'), bMid(B2_L, B2_R, '  └─ VAMI port 5480'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '   FAIL → check firewall rule'), bMid(B2_L, B2_R, 'NSX Manager FQDN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3. Login succeeds?'), bMid(B2_L, B2_R, 'Backup console FQDN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '   FAIL → check SSO / AD bind'), bMid(B2_L, B2_R, 'Monitoring dashboard'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4. Session timeout acceptable?'), bMid(B2_L, B2_R, 'Storage array FQDN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '   FAIL → check session policy'), bMid(B2_L, B2_R, 'vSAN Witness host'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  FQDN    = Fully Qualified Domain Name; must resolve in DNS; e.g. vcenter.corp.local'))
    lines.append(txt_row('  SSO     = vCenter Single Sign-On; authentication service; default domain: vsphere.local'))
    lines.append(txt_row('  VAMI    = vCenter Appliance Management Interface; port 5480; cert and patch management'))
    lines.append(txt_row('  AD bind = LDAP/LDAPS connection from SSO to Active Directory; check if login fails'))
    lines.append(txt_row('  Timeout = Session idle timeout; check if users report being logged out too quickly'))
    lines.append(txt_row('  NSX Mgr = NSX Manager UI; HTTPS on port 443; login via admin or LDAP-integrated account'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-health-checks-pre-change-check',
    'docs/virtualization/operations/health-checks/pre-change-check/index.md',
    'Pre-change checks — baseline validation before any maintenance or upgrade',
)
def virt_pre_change_check():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Pre-Change Checks — Before Maintenance'))
    lines.append(txt_row())
    lines.append(txt_row('  Verify platform is healthy before any host maintenance, upgrade, or config change'))
    lines.append(txt_row())
    lines.append(R(arrow([TM1, TM2, TM3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(TB1_L, TB1_R), bTop(TB2_L, TB2_R), bTop(TB3_L, TB3_R))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'vCenter Health'), bMid(TB2_L, TB2_R, 'vSAN + Storage'), bMid(TB3_L, TB3_R, 'Snapshots + Backup'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, '─────────────────'), bMid(TB2_L, TB2_R, '─────────────────'), bMid(TB3_L, TB3_R, '─────────────────'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'All hosts connected'), bMid(TB2_L, TB2_R, 'vSAN health green'), bMid(TB3_L, TB3_R, 'No stale snapshots'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'No active alarms'), bMid(TB2_L, TB2_R, 'No resync in prog.'), bMid(TB3_L, TB3_R, 'Snaps < 24h/10 GB'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'HA/DRS enabled'), bMid(TB2_L, TB2_R, 'All paths active'), bMid(TB3_L, TB3_R, 'Backup ran < 24h'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Admission ctrl OK'), bMid(TB2_L, TB2_R, 'Datastore < 80%'), bMid(TB3_L, TB3_R, 'Change rec. approv.'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Tasks/events clear'), bMid(TB2_L, TB2_R, 'No stale extents'), bMid(TB3_L, TB3_R, 'MW window confirm.'))))
    lines.append(R(merge(bBot(TB1_L, TB1_R), bBot(TB2_L, TB2_R), bBot(TB3_L, TB3_R))))
    lines.append(txt_row())
    lines.append(R(arrow([M1])))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'All PASS → proceed with change    ·    Any FAIL → hold until resolved')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Admission ctrl = HA policy reserving cluster capacity to restart all protected VMs'))
    lines.append(txt_row('  Resync         = vSAN rebuilding data after a failure; change causes resync cascade'))
    lines.append(txt_row('  Stale extent   = vSAN object component with no active mirror; signals degraded health'))
    lines.append(txt_row('  Active paths   = Storage paths from ESXi to array; all should be active/optimised'))
    lines.append(txt_row('  MW window      = Maintenance window; agreed time with app owner and change manager'))
    lines.append(txt_row('  Change rec.    = ITSM change record; must be approved before any maintenance begins'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-health-checks-post-change-validation',
    'docs/virtualization/operations/health-checks/post-change-validation/index.md',
    'Post-change validation — immediate and extended checks after any maintenance',
)
def virt_post_change_validation():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Post-Change Validation'))
    lines.append(txt_row())
    lines.append(txt_row('  Run after any change — maintenance, upgrade, patch, or config modification'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Immediate — within 5 min'), bMid(B2_L, B2_R, 'Extended — within 1 hour'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '──────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Hosts connected to vCenter'), bMid(B2_L, B2_R, 'Monitoring alerts clear'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cluster HA / DRS active'), bMid(B2_L, B2_R, 'App owner confirms OK'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No VMs in unexpected state'), bMid(B2_L, B2_R, 'Backup job succeeds'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Datastore paths accessible'), bMid(B2_L, B2_R, 'Snapshot count stable'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No new critical alarms'), bMid(B2_L, B2_R, 'Performance metrics normal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vSAN health green'), bMid(B2_L, B2_R, 'Change record closed'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Unexpected state = VM powered off, suspended, or orphaned unexpectedly after change'))
    lines.append(txt_row('  Datastore paths  = Storage I/O paths from ESXi; check via esxcli storage core path list'))
    lines.append(txt_row('  Snapshot stable  = No new snapshots created by backup; no stale snapshots accumulating'))
    lines.append(txt_row('  App owner        = Business stakeholder; must confirm application is healthy post-change'))
    lines.append(txt_row('  Change record    = Close only after all checks pass and app owner sign-off is documented'))
    lines.append(txt_row('  Monitoring alert = Any new alert fired after change = likely caused by the change; triage'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks',
    'docs/virtualization/operations/runbooks/index.md',
    'Virtualization runbooks — incident, planned work, and reference index',
)
def virt_runbooks_index():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Virtualization Runbooks'))
    lines.append(txt_row())
    lines.append(txt_row('  Practical runbooks for incidents, maintenance, lifecycle work, and RCA follow-up'))
    lines.append(txt_row())
    lines.append(R(arrow([TM1, TM2, TM3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(TB1_L, TB1_R), bTop(TB2_L, TB2_R), bTop(TB3_L, TB3_R))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Incident Response'), bMid(TB2_L, TB2_R, 'Planned Work'), bMid(TB3_L, TB3_R, 'Reference'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, '─────────────────'), bMid(TB2_L, TB2_R, '─────────────────'), bMid(TB3_L, TB3_R, '─────────────────'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Backup failure'), bMid(TB2_L, TB2_R, 'Host evacuation'), bMid(TB3_L, TB3_R, 'Health check index'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'vCenter outage'), bMid(TB2_L, TB2_R, 'Snapshot cleanup'), bMid(TB3_L, TB3_R, 'Troubleshooting'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Host disconnected'), bMid(TB2_L, TB2_R, 'VM lifecycle'), bMid(TB3_L, TB3_R, 'Inventory'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Evidence collect'), bMid(TB2_L, TB2_R, 'Cert renewal'), bMid(TB3_L, TB3_R, 'Quick reference'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'RCA template'), bMid(TB2_L, TB2_R, 'Maintenance window'), bMid(TB3_L, TB3_R, 'Decision trees'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Incident response'), bMid(TB2_L, TB2_R, 'Network validation'), bMid(TB3_L, TB3_R, 'Cheat sheets'))))
    lines.append(R(merge(bBot(TB1_L, TB1_R), bBot(TB2_L, TB2_R), bBot(TB3_L, TB3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Runbook          = Step-by-step procedure for a known task or incident type'))
    lines.append(txt_row('  Evidence collect = Gather logs and screenshots before any remediation begins'))
    lines.append(txt_row('  RCA              = Root Cause Analysis; post-incident document explaining why failure occurred'))
    lines.append(txt_row('  Host evacuation  = vMotion all VMs off a host before patching or hardware work'))
    lines.append(txt_row('  VM lifecycle     = Standard steps for deploy, rename, reconfigure, and decommission'))
    lines.append(txt_row('  Incident         = Unplanned disruption; follow incident response runbook immediately'))
    lines.append(txt_row('  Planned work     = Scheduled change; requires approved change record before starting'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-backup-failure',
    'docs/virtualization/operations/runbooks/backup-failure/index.md',
    'VMware backup failure runbook — diagnose, fix, and verify backup jobs',
)
def virt_runbook_backup_failure():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'VMware Backup Failure Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  Identify failed VMs, diagnose the error, remediate, and verify before closing'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identify + Diagnose'), bMid(B2_L, B2_R, 'Fix + Verify'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '──────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check console for failed jobs'), bMid(B2_L, B2_R, 'Check VM snapshot state'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Note VM, job, error, time'), bMid(B2_L, B2_R, 'Right-click VM → Snapshots'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Common errors:'), bMid(B2_L, B2_R, 'Consolidate stale snapshots'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '· Snapshot creation failed'), bMid(B2_L, B2_R, 'Free datastore space if full'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '· Snapshot consolidation warn'), bMid(B2_L, B2_R, 'Fix proxy / network path'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '· Datastore out of space'), bMid(B2_L, B2_R, 'Retry failed job manually'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '· Network / proxy failure'), bMid(B2_L, B2_R, 'Verify job succeeded'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '· vCenter API error'), bMid(B2_L, B2_R, 'Document in change record'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Snapshot      = Point-in-time copy of VM disk state; backup creates and removes per job'))
    lines.append(txt_row('  Consolidation = Merging leftover snapshot files into base disk; run if stale snap exists'))
    lines.append(txt_row('  Proxy         = Backup proxy server that performs data movement; check connectivity'))
    lines.append(txt_row('  CBT           = Changed Block Tracking; VMware API tracking changed disk blocks for backup'))
    lines.append(txt_row('  quiesce       = VSS snapshot with application-consistent state; fails if VMware tools old'))
    lines.append(txt_row('  Orphaned snap = Snapshot in datastore but not in vCenter; causes silent disk growth'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-certificate-renewal-planning',
    'docs/virtualization/operations/runbooks/certificate-renewal-planning/index.md',
    'VMware certificate renewal runbook — planning and execution steps',
)
def virt_runbook_cert_renewal():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'VMware Certificate Renewal Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  Plan certificate renewals early; capture pre/post evidence; test all integrations'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Planning'), bMid(B2_L, B2_R, 'Execution'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '──────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identify expiring certificate'), bMid(B2_L, B2_R, 'Schedule maintenance window'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm type: SSL / STS / SU'), bMid(B2_L, B2_R, 'Notify stakeholders'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'List all affected products'), bMid(B2_L, B2_R, 'Run cert renewal procedure'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Note integrations at risk'), bMid(B2_L, B2_R, 'Post-change: login test'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capture: subject, SAN, expiry'), bMid(B2_L, B2_R, 'Verify all integrations OK'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Screenshot as pre-evidence'), bMid(B2_L, B2_R, 'Capture post-change evidence'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm vCenter backup exists'), bMid(B2_L, B2_R, 'Close change record'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Machine SSL = vCenter/ESXi HTTPS cert; presented to browsers and API clients'))
    lines.append(txt_row('  STS cert    = Security Token Service cert; used for SAML token signing in SSO'))
    lines.append(txt_row('  SU cert     = Solution User cert; used by vCenter services to authenticate to SSO'))
    lines.append(txt_row('  SAN         = Subject Alternative Name; list of FQDNs the cert is valid for'))
    lines.append(txt_row('  VMCA        = VMware Certificate Authority; built-in CA; issues certs to ESXi hosts'))
    lines.append(txt_row('  Expiry buffer = Renew at 60 days remaining; 30 days = urgent; 0 days = service outage'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-evidence-collection',
    'docs/virtualization/operations/runbooks/evidence-collection/index.md',
    'Evidence collection runbook — gather logs and screenshots before escalation',
)
def virt_runbook_evidence():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Virtualization Evidence Collection Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  Collect evidence before vendor escalation, RCA work, or major incident review'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-Checks'), bMid(B2_L, B2_R, 'Collect'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '──────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm issue scope'), bMid(B2_L, B2_R, 'Screenshot active alarms'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm affected objects'), bMid(B2_L, B2_R, 'Export tasks and events'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm timestamps + timezone'), bMid(B2_L, B2_R, 'Note object names + IDs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm recent changes'), bMid(B2_L, B2_R, 'Collect ESXi / VCSA logs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confirm ticket / case number'), bMid(B2_L, B2_R, 'Capture version strings'))))
    lines.append(R(merge(bMid(B1_L, B1_R, ''), bMid(B2_L, B2_R, 'Export support bundle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, ''), bMid(B2_L, B2_R, 'Attach all to ticket'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Support bundle  = vm-support.sh output; full ESXi/VCSA log archive for vendor support'))
    lines.append(txt_row('  Tasks + events  = vCenter audit trail; export via Monitor → Tasks for the time window'))
    lines.append(txt_row('  Affected object = VM, host, datastore, or network affected by the incident'))
    lines.append(txt_row('  Case number     = Vendor support ticket ID; always reference in evidence bundle name'))
    lines.append(txt_row('  Timezone        = Always record timestamps in UTC to avoid ambiguity across regions'))
    lines.append(txt_row('  RCA             = Root Cause Analysis; requires accurate timeline and evidence log'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-host-evacuation',
    'docs/virtualization/operations/runbooks/host-evacuation/index.md',
    'ESXi host evacuation runbook — safely drain a host before maintenance',
)
def virt_runbook_host_evacuation():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'ESXi Host Evacuation Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  Drain all VMs from a host before patching, hardware work, or decommission'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['Phase', 'Action', 'Verify', 'On FAIL', 'Tool'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['──────────────', '──────────────', '───────────────', '──────────────', '──────────────'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['1  Pre-check', 'Confirm cluster OK', 'HA/DRS enabled', 'Fix before start', 'vSphere Client'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['2  Maintenance', 'Enter maint. mode', 'DRS vMotions VMs', 'vMotion manually', 'vSphere Client'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['3  Verify drain', 'No VMs on host', '0 VM count', 'Force migrate', 'vSphere Client'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['4  Work', 'Perform task', 'Task completed', 'Rollback plan', 'Per procedure'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['5  Exit maint.', 'Exit maint. mode', 'Host reconnects', 'Check hostd/vpxa', 'vSphere Client'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['6  Post-check', 'Validate health', 'DRS rebalances', 'Review alarms', 'vSphere Client'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Maintenance mode = ESXi state that blocks new VM placement and triggers DRS evacuation'))
    lines.append(txt_row('  vMotion          = Live migration of a running VM between ESXi hosts; zero downtime'))
    lines.append(txt_row('  DRS              = Distributed Resource Scheduler; automates vMotion during evacuation'))
    lines.append(txt_row('  hostd            = ESXi host management daemon; restart if host fails to reconnect'))
    lines.append(txt_row('  vpxa             = vCenter agent on ESXi; restart to fix disconnected host state'))
    lines.append(txt_row('  HA admission     = Cluster must have spare capacity to accept evacuated VMs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-incident-response',
    'docs/virtualization/operations/runbooks/incident-response/index.md',
    'Incident response runbook — detect, assess, contain, resolve, close',
)
def virt_runbook_incident_response():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Incident Response Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  Use for any active VMware platform issue; follow phases in order'))
    lines.append(txt_row())
    lines.append(R(arrow([TM1, TM2, TM3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(TB1_L, TB1_R), bTop(TB2_L, TB2_R), bTop(TB3_L, TB3_R))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Detect + Assess'), bMid(TB2_L, TB2_R, 'Contain + Fix'), bMid(TB3_L, TB3_R, 'Resolve + Close'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, '─────────────────'), bMid(TB2_L, TB2_R, '─────────────────'), bMid(TB3_L, TB3_R, '─────────────────'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Alert or user report'), bMid(TB2_L, TB2_R, 'Isolate scope'), bMid(TB3_L, TB3_R, 'Verify fix holds'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Confirm issue is real'), bMid(TB2_L, TB2_R, 'Prevent spread'), bMid(TB3_L, TB3_R, 'Monitor 30 min'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Open incident ticket'), bMid(TB2_L, TB2_R, 'Apply fix / workaround'), bMid(TB3_L, TB3_R, 'Notify stakeholders'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Define scope: VM/host'), bMid(TB2_L, TB2_R, 'Collect evidence'), bMid(TB3_L, TB3_R, 'Close ticket'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Set severity P1/P2/P3'), bMid(TB2_L, TB2_R, 'Escalate if P1'), bMid(TB3_L, TB3_R, 'Schedule RCA'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Notify stakeholders'), bMid(TB2_L, TB2_R, 'Update ticket live'), bMid(TB3_L, TB3_R, 'Post-mortem doc'))))
    lines.append(R(merge(bBot(TB1_L, TB1_R), bBot(TB2_L, TB2_R), bBot(TB3_L, TB3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  P1 = Critical; full platform or business service down; immediate escalation required'))
    lines.append(txt_row('  P2 = Major; significant degradation; resolve within business hours'))
    lines.append(txt_row('  P3 = Minor; limited impact; resolve within next maintenance window'))
    lines.append(txt_row('  Contain   = Stop the issue spreading before applying a fix; e.g. isolate a host'))
    lines.append(txt_row('  Workaround = Temporary fix to restore service; permanent fix follows in RCA action'))
    lines.append(txt_row('  Post-mortem = Written RCA document; timeline, root cause, and preventive actions'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-maintenance-window',
    'docs/virtualization/operations/runbooks/maintenance-window/index.md',
    'Maintenance window runbook — pre, execute, post, and close phases',
)
def virt_runbook_maintenance_window():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Maintenance Window Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  Use for all planned VMware work; follow pre/execute/post phases in order'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['Phase', 'Key Actions', 'Gate Criteria', 'On FAIL', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['──────────────', '──────────────', '───────────────', '──────────────', '──────────────'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['1  Pre-checks', 'Health + backups', 'All green', 'Do not proceed', 'Infra engineer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['2  Notify', 'Stakeholders out', 'Comms confirmed', 'Delay window', 'Change manager'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['3  Execute', 'Perform change', 'Per procedure', 'Rollback plan', 'Infra engineer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['4  Post-check', 'Validate health', 'All checks pass', '→ incident proc.', 'Infra engineer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['5  App check', 'Owner confirms', 'Sign-off received', 'Escalate to P2', 'App owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['6  Close', 'Update CR + docs', 'CR closed', 'Note exceptions', 'Change manager'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CR          = Change Record; ITSM ticket approved before work begins; closed after'))
    lines.append(txt_row('  Rollback    = Pre-planned steps to undo the change if it fails; must be documented'))
    lines.append(txt_row('  Comms       = Stakeholder notification; send before window opens and after it closes'))
    lines.append(txt_row('  App owner   = Business owner of the application; provides sign-off after maintenance'))
    lines.append(txt_row('  Gate        = Go/no-go check at each phase; any failure stops the window'))
    lines.append(txt_row('  Exceptions  = Deviations from the plan; always document in the change record'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-network-validation',
    'docs/virtualization/operations/runbooks/network-validation/index.md',
    'Network validation runbook — check VM, port group, uplink, and VLAN after changes',
)
def virt_runbook_network_validation():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Virtualization Network Validation Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  Use after network changes, VLAN changes, host work, NSX changes, or VM connectivity issues'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check Sequence'), bMid(B2_L, B2_R, 'Common Fixes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '──────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '1. VM network assignment'), bMid(B2_L, B2_R, 'Reassign port group'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2. Port group VLAN config'), bMid(B2_L, B2_R, 'Fix VLAN ID mismatch'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3. Host uplink status'), bMid(B2_L, B2_R, 'Check NIC / cable'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4. VLAN / overlay config'), bMid(B2_L, B2_R, 'Fix switch VLAN trunk'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '5. NSX segment (if overlay)'), bMid(B2_L, B2_R, 'Re-deploy NSX config'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '6. Ping from VM'), bMid(B2_L, B2_R, 'Check firewall rule'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '7. DNS resolution in VM'), bMid(B2_L, B2_R, 'Check DNS server IP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '8. App connectivity test'), bMid(B2_L, B2_R, 'App owner confirms'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Port group    = Named network on a vSwitch or dvSwitch; VMs connect to port groups'))
    lines.append(txt_row('  dvSwitch      = Distributed virtual switch; managed centrally from vCenter'))
    lines.append(txt_row('  VLAN trunk    = Physical switch port allowing multiple VLANs; must match port group'))
    lines.append(txt_row('  NSX segment   = Overlay network (GENEVE); not tied to physical VLANs'))
    lines.append(txt_row('  Uplink        = Physical NIC on ESXi connected to physical switch; check link state'))
    lines.append(txt_row('  Teaming       = NIC bonding policy on vSwitch; active/standby or load balance'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-rca-template',
    'docs/virtualization/operations/runbooks/rca-template/index.md',
    'RCA template — structure for post-incident root cause analysis documents',
)
def virt_runbook_rca_template():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RCA Template — Root Cause Analysis'))
    lines.append(txt_row())
    lines.append(txt_row('  Complete after every P1/P2 incident; attach to change record and share with team'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Document Sections'), bMid(B2_L, B2_R, 'Action Items'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '──────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Summary: what happened'), bMid(B2_L, B2_R, 'Immediate: already done'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Impact: systems + users'), bMid(B2_L, B2_R, 'Short-term: within 7 days'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Timeline: ordered events'), bMid(B2_L, B2_R, 'Long-term: prevent recurrence'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Root cause: why it failed'), bMid(B2_L, B2_R, 'Owner assigned per item'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Contributing factors'), bMid(B2_L, B2_R, 'Due dates set'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'What went well'), bMid(B2_L, B2_R, 'Tracked in ITSM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Lessons learned'), bMid(B2_L, B2_R, 'Reviewed at team meeting'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Root cause      = The single underlying reason the incident occurred; not a symptom'))
    lines.append(txt_row('  Contributing    = Factors that made the failure worse or harder to detect'))
    lines.append(txt_row('  Timeline        = Chronological event log from first detection to resolution'))
    lines.append(txt_row('  5 Whys          = Ask "why" five times to drill from symptom to root cause'))
    lines.append(txt_row('  Action item     = Specific task with owner and due date to prevent recurrence'))
    lines.append(txt_row('  Blameless RCA   = Focus on system/process failures, not individual mistakes'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-snapshot-cleanup',
    'docs/virtualization/operations/runbooks/snapshot-cleanup/index.md',
    'Snapshot cleanup runbook — identify, consolidate, and remove stale snapshots',
)
def virt_runbook_snapshot_cleanup():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'vSAN Snapshot Cleanup Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  Identify degraded vSAN objects; check disks and hosts; restore or rebuild'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['Step', 'Action', 'Check', 'On FAIL', 'Tool'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['──────────────', '──────────────', '───────────────', '──────────────', '──────────────'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['1  vSAN health', 'Open Skyline', 'No red checks', 'Note failures', 'vCenter UI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['2  Objects', 'Virtual Objects', 'Degraded list', 'Note VM names', 'vCenter UI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['3  Disk check', 'Physical Disk', 'No failed disks', 'Replace disk', 'iDRAC / UI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['4  Host check', 'Host status', 'All connected', 'Rejoin cluster', 'vCenter UI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['5  Rebuild', 'Policy repair', 'Objects rebuild', 'Escalate VMware', 'vCenter UI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                            ['6  Verify', 'Skyline green', 'No degraded obj', 'Re-run steps', 'vCenter UI'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Skyline Health = vSAN built-in health checks UI; vCenter → Cluster → vSAN → Skyline'))
    lines.append(txt_row('  Degraded obj   = vSAN object with fewer mirrors than the storage policy requires'))
    lines.append(txt_row('  Non-compliant  = vSAN object exists but does not meet current storage policy'))
    lines.append(txt_row('  Absent         = vSAN object has no accessible components; VM may be impacted'))
    lines.append(txt_row('  Policy repair  = vSAN automatically rebuilds objects after a host or disk returns'))
    lines.append(txt_row('  FTT            = Failures To Tolerate; storage policy setting; FTT=1 needs 3 hosts min'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-storage-path-validation',
    'docs/virtualization/operations/runbooks/storage-path-validation/index.md',
    'Storage path validation runbook — check datastores, adapters, paths, and multipathing',
)
def virt_runbook_storage_path():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Storage Path Validation Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  Use after SAN changes, storage maintenance, host work, or datastore alerts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check Sequence'), bMid(B2_L, B2_R, 'Common Fixes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '──────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '1. Datastore visibility'), bMid(B2_L, B2_R, 'Rescan HBA adapters'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2. Host storage adapters'), bMid(B2_L, B2_R, 'Check HBA driver/FW'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3. Path count and state'), bMid(B2_L, B2_R, 'Fix zoning on SAN switch'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4. Multipathing policy'), bMid(B2_L, B2_R, 'Set RR per array guide'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '5. Array masking / zoning'), bMid(B2_L, B2_R, 'Add host to zone set'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '6. Datastore I/O test'), bMid(B2_L, B2_R, 'Run iometer / dd test'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '7. App I/O validation'), bMid(B2_L, B2_R, 'App owner confirms'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  HBA      = Host Bus Adapter; FC or iSCSI NIC on ESXi connecting to SAN fabric'))
    lines.append(txt_row('  Zoning   = SAN switch config allowing specific HBAs to see specific storage ports'))
    lines.append(txt_row('  Masking  = Array-side config allowing specific initiators to access specific LUNs'))
    lines.append(txt_row('  RR       = Round Robin multipathing policy; distributes I/O across all active paths'))
    lines.append(txt_row('  Dead path = Path in dead/error state; verify SAN port, cable, and zone config'))
    lines.append(txt_row('  Rescan   = ESXi re-discovers storage; run after SAN changes to pick up new LUNs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-vcenter-outage',
    'docs/virtualization/operations/runbooks/vcenter-outage/index.md',
    'vCenter outage runbook — diagnose and restore VCSA availability',
)
def virt_runbook_vcenter_outage():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'vCenter Outage Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  ESXi hosts continue running VMs independently; vCenter is management plane only'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Diagnose'), bMid(B2_L, B2_R, 'Restore'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '──────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Ping vCenter FQDN + IP'), bMid(B2_L, B2_R, 'Power on VCSA VM via iDRAC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access VAMI port 5480'), bMid(B2_L, B2_R, 'Start services via VAMI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review service health'), bMid(B2_L, B2_R, 'service-control --start --all'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check disk partitions'), bMid(B2_L, B2_R, 'Free disk if /storage full'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check DNS forward/reverse'), bMid(B2_L, B2_R, 'Fix DNS record / hosts file'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check VCSA VM power state'), bMid(B2_L, B2_R, 'Restore from file backup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check iDRAC / IPMI logs'), bMid(B2_L, B2_R, 'Escalate to VMware GSS'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  VCSA         = vCenter Server Appliance; Linux-based VM running all vCenter services'))
    lines.append(txt_row('  VAMI         = Appliance Management Interface; port 5480; accessible when vCenter UI is not'))
    lines.append(txt_row('  service-control = VCSA CLI tool; start/stop/status all vCenter services'))
    lines.append(txt_row('  Management plane = vCenter; losing it does NOT stop running VMs — hosts operate standalone'))
    lines.append(txt_row('  File backup  = vCenter native backup; SFTP destination; restore via VCSA installer'))
    lines.append(txt_row('  GSS          = VMware Global Support Services; escalate P1 outages with SR number'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization-operations-runbooks-vm-lifecycle',
    'docs/virtualization/operations/runbooks/vm-lifecycle/index.md',
    'VM lifecycle runbook — build, change, review, and decommission procedures',
)
def virt_runbook_vm_lifecycle():
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'VM Lifecycle Runbook'))
    lines.append(txt_row())
    lines.append(txt_row('  Standard steps for VM deploy, reconfigure, ownership review, and decommission'))
    lines.append(txt_row())
    lines.append(R(arrow([TM1, TM2, TM3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(TB1_L, TB1_R), bTop(TB2_L, TB2_R), bTop(TB3_L, TB3_R))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Build'), bMid(TB2_L, TB2_R, 'Operate + Review'), bMid(TB3_L, TB3_R, 'Decommission'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, '─────────────────'), bMid(TB2_L, TB2_R, '─────────────────'), bMid(TB3_L, TB3_R, '─────────────────'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Validate request'), bMid(TB2_L, TB2_R, 'Confirm owner'), bMid(TB3_L, TB3_R, 'Owner approval'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Confirm sizing'), bMid(TB2_L, TB2_R, 'Review sizing'), bMid(TB3_L, TB3_R, 'Final backup'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Deploy from template'), bMid(TB2_L, TB2_R, 'Check backup'), bMid(TB3_L, TB3_R, 'Power off VM'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Apply naming standard'), bMid(TB2_L, TB2_R, 'Check monitoring'), bMid(TB3_L, TB3_R, 'Delete from vCenter'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Assign backup policy'), bMid(TB2_L, TB2_R, 'Patch compliance'), bMid(TB3_L, TB3_R, 'Remove from backup'))))
    lines.append(R(merge(bMid(TB1_L, TB1_R, 'Add to monitoring'), bMid(TB2_L, TB2_R, 'Annual review'), bMid(TB3_L, TB3_R, 'Update CMDB'))))
    lines.append(R(merge(bBot(TB1_L, TB1_R), bBot(TB2_L, TB2_R), bBot(TB3_L, TB3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Template     = Golden image VM used as the base for new deployments; keep patched'))
    lines.append(txt_row('  Naming std   = Consistent VM name format; e.g. SITE-ROLE-NN; critical for CMDB'))
    lines.append(txt_row('  Backup policy = Defines schedule, retention, and target for the VM backup job'))
    lines.append(txt_row('  CMDB         = Configuration Management Database; tracks all VMs and their owners'))
    lines.append(txt_row('  Annual review = Yearly check that VM is still needed and owner is still valid'))
    lines.append(txt_row('  Decommission  = Remove VM, backup exclusions, monitoring, DNS, and CMDB in that order'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
