"""
SAN (Brocade FabricOS, SANnav; Cisco MDS, DCNM, Nexus Dashboard) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)


@kb_diagram(
    'brocade-sannav',
    'docs/san/brocade/sannav/index.md',
    'Brocade SANnav — fabric discovery, monitoring, inventory, alerts, and reporting for FC',
)
def brocade_sannav():
    """Brocade SANnav management platform — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade SANnav — Management Platform'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SANnav: web-based SAN management for Brocade FC switches — discovery, monitoring, reporting')))
    lines.append(R(bMid(IV_L, IV_R, 'Deployed as a Linux VM; connects to all Brocade switches via SSH and REST API')))
    lines.append(R(bMid(IV_L, IV_R, 'Fabric discovery: topology mapping, zone config pull, port inventory, SFP health')))
    lines.append(R(bMid(IV_L, IV_R, 'Replaces legacy DCFM; supports up to 150 switches and 15,000 ports per instance')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Fabric discovery → health monitoring → inventory and reporting layers'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Discovery'), bMid(B2_L, B2_R, 'Monitoring'), bMid(B3_L, B3_R, 'Reporting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Switch discovery'), bMid(B2_L, B2_R, 'Port health'), bMid(B3_L, B3_R, 'Switch inventory'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Topology mapping'), bMid(B2_L, B2_R, 'Error counters'), bMid(B3_L, B3_R, 'Port inventory'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Zone config pull'), bMid(B2_L, B2_R, 'SFP Tx/Rx power'), bMid(B3_L, B3_R, 'Firmware matrix'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Credential mgmt'), bMid(B2_L, B2_R, 'Threshold alerts'), bMid(B3_L, B3_R, 'SAN reports'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SNMP integration'), bMid(B2_L, B2_R, 'Performance data'), bMid(B3_L, B3_R, 'Audit trail'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  REST API and LDAP integration allow external monitoring and centralised auth'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Function', 'Protocol', 'Output', 'Integration'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Discovery', 'Topology/zones', 'SSH/REST', 'Fabric map', 'SNMP traps'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Monitoring', 'Port/SFP health', 'Polling', 'Alerts', 'Syslog/email'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Reporting', 'Inventory/audit', 'REST API', 'PDF/CSV', 'LDAP auth'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SANnav Linux VM · Brocade FC switches (G630/G720/G730) · FC SFP transceivers'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SANnav        = Brocade SAN management platform (replaces legacy DCFM/Network Advisor)'))
    lines.append(txt_row('  Fabric        = Set of Brocade FC switches connected via ISLs sharing a single namespace'))
    lines.append(txt_row('  Zone config   = Active zone configuration defining which HBAs can communicate with which targets'))
    lines.append(txt_row('  SFP           = Small Form-factor Pluggable transceiver; optical FC link on each switch port'))
    lines.append(txt_row('  Tx/Rx power   = SFP optical transmit/receive power; out-of-range indicates failing optic'))
    lines.append(txt_row('  Port health   = FC port state: online/offline/error; error counters: CRC, Loss of Signal'))
    lines.append(txt_row('  SNMP trap     = SANnav sends fault events to NMS via SNMP; configured per severity level'))
    lines.append(txt_row('  DCFM          = Data Center Fabric Manager; legacy predecessor to SANnav'))
    lines.append(txt_row('  REST API      = SANnav REST API; used for automation and ITSM integration'))
    lines.append(txt_row('  Topology map  = SANnav graphical view of switch interconnections and ISL links'))
    lines.append(txt_row('  ISL           = Inter-Switch Link; FC trunk connecting two Brocade switches in a fabric'))
    lines.append(txt_row('  LDAP auth     = SANnav supports AD/LDAP for centralised user authentication'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-sannav-operations',
    'docs/san/brocade/sannav/operations/index.md',
    'SANnav Operations — health checks, fabric discovery, zone management, firmware, backup',
)
def brocade_sannav_operations():
    """SANnav Operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SANnav — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Day-to-day SANnav operational tasks: health checks, fabric management, lifecycle')))
    lines.append(R(bMid(IV_L, IV_R, 'Health checks: fabric status dashboard, port error counters, SFP Tx/Rx, switch CPU/mem')))
    lines.append(R(bMid(IV_L, IV_R, 'Zone management: zone wizard, alias creation, zone set activation — changes logged')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: SANnav version upgrade, FabricOS firmware job scheduling, backup/restore')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Daily health → fabric management tasks → scheduled maintenance and lifecycle ops'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health Checks'), bMid(B2_L, B2_R, 'Fabric Mgmt'), bMid(B3_L, B3_R, 'Lifecycle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dashboard review'), bMid(B2_L, B2_R, 'Zone wizard'), bMid(B3_L, B3_R, 'SANnav upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port error check'), bMid(B2_L, B2_R, 'Alias management'), bMid(B3_L, B3_R, 'FabricOS jobs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SFP power check'), bMid(B2_L, B2_R, 'Zone activation'), bMid(B3_L, B3_R, 'Config backup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Switch CPU/mem'), bMid(B2_L, B2_R, 'Port admin'), bMid(B3_L, B3_R, 'Restore test'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert review'), bMid(B2_L, B2_R, 'ISL monitoring'), bMid(B3_L, B3_R, 'Performance rpt'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  All zone changes require change ticket; activation logged in SANnav audit trail'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Task', 'Frequency', 'SANnav path', 'Output', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Fabric health', 'Daily', 'Dashboard', 'Status summary', 'Check alerts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Port errors', 'Daily', 'Inventory > Ports', 'Error counters', 'Clear after fix'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Config backup', 'Weekly', 'Admin > Backup', 'Backup file', 'Off-site copy'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SANnav VM · Brocade FC switches · ISL cables · FC SFP optics'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Zone wizard   = SANnav GUI tool for creating zones, aliases, and zone sets step-by-step'))
    lines.append(txt_row('  Alias         = Named group of port WWNs; used in zone definitions for readability'))
    lines.append(txt_row('  Zone set      = Named collection of zones; one zone set active per fabric at a time'))
    lines.append(txt_row('  Activation    = cfgenable equivalent; pushes the active zone set to all fabric switches'))
    lines.append(txt_row('  Port admin    = Enable/disable individual FC ports via SANnav without CLI access'))
    lines.append(txt_row('  ISL           = Inter-Switch Link; trunk between switches; monitored for utilisation'))
    lines.append(txt_row('  FabricOS job  = SANnav firmware upgrade task targeting one or more switches'))
    lines.append(txt_row('  Config backup = SANnav application backup (not switch backup); includes DB and settings'))
    lines.append(txt_row('  SFP power     = Optical Tx/Rx dBm values; SANnav alerts on out-of-range readings'))
    lines.append(txt_row('  Error counter = CRC, Loss of Signal, Loss of Sync counts per port; nonzero = investigate'))
    lines.append(txt_row('  Audit trail   = SANnav log of all config changes including who, what, and when'))
    lines.append(txt_row('  Performance   = SANnav bandwidth utilisation graphs per port and ISL over time'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-sannav-operations-issues',
    'docs/san/brocade/sannav/operations/common-issues/index.md',
    'SANnav Common Issues — discovery failures, login errors, stale inventory, alert storms',
)
def brocade_sannav_operations_issues():
    """SANnav Common Issues — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SANnav — Common Issues'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common SANnav operational issues with diagnosis and resolution paths')))
    lines.append(R(bMid(IV_L, IV_R, 'Discovery failures: unreachable switch, wrong credentials, SNMP not enabled on switch')))
    lines.append(R(bMid(IV_L, IV_R, 'Login issues: LDAP misconfiguration, session timeout, certificate expired on SANnav')))
    lines.append(R(bMid(IV_L, IV_R, 'Stale inventory: switch not re-polled after config change; trigger manual re-discovery')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Discovery issues → login/auth issues → inventory staleness → alert volume issues'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Discovery'), bMid(B2_L, B2_R, 'Auth / Login'), bMid(B3_L, B3_R, 'Inventory'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Switch unreachable'), bMid(B2_L, B2_R, 'LDAP config error'), bMid(B3_L, B3_R, 'Stale topology'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Wrong SSH creds'), bMid(B2_L, B2_R, 'Session timeout'), bMid(B3_L, B3_R, 'Missing ports'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SNMP disabled'), bMid(B2_L, B2_R, 'Cert expired'), bMid(B3_L, B3_R, 'Old zone data'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FW incompatible'), bMid(B2_L, B2_R, 'Password locked'), bMid(B3_L, B3_R, 'Counter gap'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TCP 22 blocked'), bMid(B2_L, B2_R, 'SSO fail'), bMid(B3_L, B3_R, 'Alert storm'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Escalate to SANnav logs at /var/log/sannav/ and Brocade TAC if issue persists'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Issue', 'Symptom', 'Root cause', 'Resolution', 'Prevention'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Discovery fail', 'Switch offline', 'SSH blocked', 'Check TCP 22', 'Firewall rule'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Stale data', 'Old zones shown', 'Poll interval', 'Manual rediscover', 'Shorten poll'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Alert storm', 'Hundreds alerts', 'Threshold low', 'Tune thresholds', 'Baseline first'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: network path SANnav → switch management port; SNMP UDP 161 must be open'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Discovery fail = SANnav cannot reach or authenticate to a switch; shows as offline in UI'))
    lines.append(txt_row('  SNMP v3       = SANnav uses SNMPv3 for trap reception; must be enabled on each switch'))
    lines.append(txt_row('  Stale topo    = SANnav topology not updated after a switch change; trigger re-discovery'))
    lines.append(txt_row('  Manual rediscover = SANnav UI action to force immediate poll of a switch or fabric'))
    lines.append(txt_row('  Alert storm   = Flood of threshold alerts; caused by misconfigured thresholds or port flap'))
    lines.append(txt_row('  Threshold tune = Adjust alert trigger values to match expected baseline traffic levels'))
    lines.append(txt_row('  Cert expired  = SANnav HTTPS cert; renew via admin console; causes browser login failure'))
    lines.append(txt_row('  LDAP config   = SANnav LDAP settings; test with known user before saving changes'))
    lines.append(txt_row('  SSH creds     = Per-switch admin username/password stored in SANnav credential store'))
    lines.append(txt_row('  Poll interval = Frequency SANnav polls switches for counters and state; default 5 minutes'))
    lines.append(txt_row('  FW compat     = SANnav has minimum FabricOS version requirements per switch model'))
    lines.append(txt_row('  Log location  = /var/log/sannav/ on SANnav VM; review sannav.log and discovery.log'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-sannav-security',
    'docs/san/brocade/sannav/security/index.md',
    'SANnav Security — LDAP auth, RBAC roles, TLS, audit logging, network access control',
)
def brocade_sannav_security():
    """SANnav Security — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SANnav — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SANnav security: LDAP/AD authentication, RBAC, TLS enforcement, and audit logging')))
    lines.append(R(bMid(IV_L, IV_R, 'Authentication: LDAP/AD integration with AD group-to-role mapping; local admin fallback')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC: Network Administrator / Network Operator / Read-only roles; fabric-level scoping')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: all login events, zone changes, and admin operations logged with user and timestamp')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Authentication gate → role-based scope → encrypted channel → immutable audit trail'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Authentication'), bMid(B2_L, B2_R, 'Access Control'), bMid(B3_L, B3_R, 'Encryption/Audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP/AD SSO'), bMid(B2_L, B2_R, 'Network Admin'), bMid(B3_L, B3_R, 'HTTPS TLS 1.2+'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'AD group mapping'), bMid(B2_L, B2_R, 'Network Operator'), bMid(B3_L, B3_R, 'API TLS enforced'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local admin acct'), bMid(B2_L, B2_R, 'Read-only'), bMid(B3_L, B3_R, 'Login audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Session timeout'), bMid(B2_L, B2_R, 'Fabric scope'), bMid(B3_L, B3_R, 'Config change log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Password policy'), bMid(B2_L, B2_R, 'Least privilege'), bMid(B3_L, B3_R, 'Syslog export'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SANnav access restricted to jump host network; direct internet access not permitted'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Control', 'Standard', 'RBAC role', 'Enforcement', 'Review'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Auth method', 'LDAP primary', 'All roles', 'SANnav settings', 'Quarterly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Zone changes', 'Admin only', 'Net Admin', 'Role enforcement', 'Per change'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Audit log', 'All actions', 'N/A', 'Syslog/SANnav', 'Monthly'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SANnav on management VLAN; jump host required for browser access'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  LDAP/AD       = SANnav authenticates against Active Directory via LDAP or LDAPS'))
    lines.append(txt_row('  AD group map  = AD security group mapped to SANnav role; changes in AD take effect on login'))
    lines.append(txt_row('  Network Admin = SANnav role with full fabric management including zone changes'))
    lines.append(txt_row('  Net Operator  = SANnav role allowing port admin and monitoring; no zone set changes'))
    lines.append(txt_row('  Read-only     = SANnav viewer role; dashboard and reports only, no configuration access'))
    lines.append(txt_row('  Fabric scope  = Limit role to specific fabrics; useful for multi-customer environments'))
    lines.append(txt_row('  Session timeout = Idle session terminated; default 30 minutes; configurable'))
    lines.append(txt_row('  TLS 1.2+      = Minimum TLS version for SANnav HTTPS and REST API; TLS 1.0/1.1 disabled'))
    lines.append(txt_row('  Audit log     = SANnav internal log of all user actions; exportable to syslog'))
    lines.append(txt_row('  Syslog export = SANnav sends audit events to external syslog/SIEM for retention'))
    lines.append(txt_row('  Local admin   = Built-in local account; break-glass only; stored in vault'))
    lines.append(txt_row('  Password pol. = Complexity and rotation requirements applied to local SANnav accounts'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-sannav-security-access',
    'docs/san/brocade/sannav/security/access-control/index.md',
    'SANnav Access Control — role-based permissions, fabric-scoped roles, service accounts',
)
def brocade_sannav_security_access():
    """SANnav Access Control — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SANnav — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SANnav RBAC: three roles mapped from AD groups; optionally scoped per fabric')))
    lines.append(R(bMid(IV_L, IV_R, 'Network Administrator: full access including zone management and switch firmware')))
    lines.append(R(bMid(IV_L, IV_R, 'Network Operator: port admin, monitoring, and reporting; no zone set activation')))
    lines.append(R(bMid(IV_L, IV_R, 'Read-only: dashboard and inventory view only; no configuration changes permitted')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Role assignment via AD group → fabric scope applied → API token for automation accounts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Network Admin'), bMid(B2_L, B2_R, 'Network Operator'), bMid(B3_L, B3_R, 'Read-Only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Zone management'), bMid(B2_L, B2_R, 'Port enable/dis'), bMid(B3_L, B3_R, 'View dashboard'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FW upgrade jobs'), bMid(B2_L, B2_R, 'Alert management'), bMid(B3_L, B3_R, 'View inventory'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'User management'), bMid(B2_L, B2_R, 'Report export'), bMid(B3_L, B3_R, 'View reports'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SANnav config'), bMid(B2_L, B2_R, 'Health checks'), bMid(B3_L, B3_R, 'View alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fabric add/del'), bMid(B2_L, B2_R, 'Performance mon'), bMid(B3_L, B3_R, 'No changes'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Service accounts use API tokens (no password); scoped to minimum required role'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Role', 'AD group', 'Fabric scope', 'API token', 'Review freq'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Net Admin', 'SAN-Admins', 'All fabrics', 'Yes (auto)', 'Quarterly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Net Operator', 'SAN-Ops', 'Per fabric', 'Yes (RO API)', 'Quarterly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Read-only', 'SAN-Viewers', 'All fabrics', 'View only', 'Annual'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SANnav on management network; access from jump host only'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RBAC          = Role-Based Access Control; SANnav maps AD groups to built-in roles'))
    lines.append(txt_row('  Fabric scope  = Restrict a role to specific fabrics; admin sees only assigned fabrics'))
    lines.append(txt_row('  API token     = SANnav-generated token for REST API access; no password exchange'))
    lines.append(txt_row('  Zone activate = cfgenable equivalent; Network Admin role required to push changes'))
    lines.append(txt_row('  AD group      = Active Directory security group mapped to SANnav role in LDAP settings'))
    lines.append(txt_row('  Service acct  = Non-human account for ITSM/monitoring integration; least-privilege'))
    lines.append(txt_row('  Port admin    = Enable or disable individual FC ports; Operator role minimum'))
    lines.append(txt_row('  FW upgrade    = Firmware upgrade job scheduling on switches; Admin role required'))
    lines.append(txt_row('  User mgmt     = Create/delete/modify SANnav user accounts; Admin only'))
    lines.append(txt_row('  Performance   = Per-port and per-ISL bandwidth graphs; Operator and above'))
    lines.append(txt_row('  Quarterly rev = Access list reviewed against joiners/movers/leavers each quarter'))
    lines.append(txt_row('  Break-glass   = Local admin account; password in vault; used if LDAP unavailable'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-sannav-troubleshooting',
    'docs/san/brocade/sannav/troubleshooting/index.md',
    'SANnav Troubleshooting — discovery failures, data gaps, login issues, alert storms',
)
def brocade_sannav_troubleshooting():
    """SANnav Troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SANnav — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SANnav troubleshooting: connectivity, data quality, authentication, and service health')))
    lines.append(R(bMid(IV_L, IV_R, 'UI/access: login failure, session expiry, certificate error, LDAP not reachable')))
    lines.append(R(bMid(IV_L, IV_R, 'Discovery: switch unreachable, SNMP timeout, wrong credentials, FabricOS incompatible')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: collect /var/log/sannav/ log bundle; open Broadcom support case')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  UI/access issues → discovery problems → data quality → SANnav service → escalation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'UI / Access'), bMid(B2_L, B2_R, 'Discovery'), bMid(B3_L, B3_R, 'Escalation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Login failure'), bMid(B2_L, B2_R, 'Switch offline'), bMid(B3_L, B3_R, 'Collect logs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Session expired'), bMid(B2_L, B2_R, 'SNMP timeout'), bMid(B3_L, B3_R, 'DB backup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cert error'), bMid(B2_L, B2_R, 'Auth mismatch'), bMid(B3_L, B3_R, 'Broadcom TAC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP timeout'), bMid(B2_L, B2_R, 'FW too old'), bMid(B3_L, B3_R, 'Syslog review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Blank dashboard'), bMid(B2_L, B2_R, 'Data gaps'), bMid(B3_L, B3_R, 'Service restart'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Restart SANnav services via systemctl before opening a support case'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'First check', 'Log to review', 'Fix', 'Escalation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Login fails', 'LDAP reachable?', 'sannav.log', 'LDAP restart', 'Broadcom TAC'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Switch offline', 'Ping switch mgmt', 'discovery.log', 'Re-add switch', 'TAC + creds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Data gap', 'Poll interval OK?', 'polling.log', 'Manual refresh', 'TAC if persist'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: management network path · SANnav VM CPU/RAM health · switch SSH reachability'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  sannav.log    = Main SANnav application log; in /var/log/sannav/ on the SANnav VM'))
    lines.append(txt_row('  discovery.log = Discovery engine log; shows switch reachability and poll failures'))
    lines.append(txt_row('  polling.log   = Counter collection log; shows which polls succeeded or timed out'))
    lines.append(txt_row('  Service restart = systemctl restart sannav; clears transient service issues'))
    lines.append(txt_row('  DB backup     = Take SANnav DB backup before any upgrade or troubleshooting attempt'))
    lines.append(txt_row('  Log bundle    = Admin > Support > Download Logs; zip of all SANnav logs for TAC'))
    lines.append(txt_row('  Cert error    = HTTPS cert expired or self-signed; renew via Admin > Certificates'))
    lines.append(txt_row('  LDAP timeout  = SANnav cannot reach LDAP server; check network path and LDAP URL'))
    lines.append(txt_row('  Data gap      = Performance counter missing for a time period; usually poll failure'))
    lines.append(txt_row('  FW too old    = Switch FabricOS below minimum SANnav supported version'))
    lines.append(txt_row('  Broadcom TAC  = Technical Assistance Centre for Brocade/SANnav support cases'))
    lines.append(txt_row('  Blank dash    = Dashboard shows no data; check SANnav services and DB health first'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-operations',
    'docs/san/brocade/fabric-os/operations/index.md',
    'FabricOS Operations — health checks, zone management, port admin, firmware, diagnostics',
)
def brocade_fabric_os_operations():
    """FabricOS Operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'FabricOS — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Day-to-day FabricOS operational tasks via CLI and SANnav — health, zones, maintenance')))
    lines.append(R(bMid(IV_L, IV_R, 'Health: switchshow, fabricshow, portshow, errshow, sfpshow — run daily or on alert')))
    lines.append(R(bMid(IV_L, IV_R, 'Zone management: zonecreate, aliadd, zoneadd, cfgenable — change-controlled')))
    lines.append(R(bMid(IV_L, IV_R, 'Maintenance: firmwaredownload, configupload, configbackup, supportshow for TAC')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Daily health checks → change-controlled zone ops → scheduled maintenance tasks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health Commands'), bMid(B2_L, B2_R, 'Zone Commands'), bMid(B3_L, B3_R, 'Maintenance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'switchshow'), bMid(B2_L, B2_R, 'zonecreate'), bMid(B3_L, B3_R, 'firmwaredownload'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'fabricshow'), bMid(B2_L, B2_R, 'aliadd'), bMid(B3_L, B3_R, 'configupload'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'portshow'), bMid(B2_L, B2_R, 'zoneadd'), bMid(B3_L, B3_R, 'configbackup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'errshow'), bMid(B2_L, B2_R, 'cfgsave'), bMid(B3_L, B3_R, 'supportshow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'sfpshow'), bMid(B2_L, B2_R, 'cfgenable'), bMid(B3_L, B3_R, 'portdisable'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'portperfshow'), bMid(B2_L, B2_R, 'zoneshow'), bMid(B3_L, B3_R, 'portlogdump'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  All zone changes require change ticket; cfgenable pushes config to all fabric switches'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Command', 'Purpose', 'Output key field', 'Frequency', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['switchshow', 'Switch health', 'State: Online', 'Daily', 'All ports green'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['errshow', 'Error counters', 'CRC, LOS, LOSync', 'Daily', 'Zero = clean'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['cfgenable', 'Zone activation', 'Config name', 'Per change', 'Change ticket'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Brocade G630/G720/G730 switches · FC SFP optics · ISL cables'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  switchshow     = Summary of all FC ports; state, speed, WWN, connected device'))
    lines.append(txt_row('  fabricshow     = List of all switches in the fabric; WWN, domain ID, IP address'))
    lines.append(txt_row('  portshow       = Detailed status of a single port including error counters'))
    lines.append(txt_row('  errshow        = Error counter summary for all ports; CRC/LOS/LOSync per port'))
    lines.append(txt_row('  sfpshow        = SFP transceiver diagnostics; Tx/Rx dBm, temperature, voltage'))
    lines.append(txt_row('  portperfshow   = Real-time port throughput in MB/s; run during I/O for baseline'))
    lines.append(txt_row('  zonecreate     = Create a new zone by name: zonecreate "zone_name", "alias1;alias2"'))
    lines.append(txt_row('  aliadd         = Add WWN members to an alias: aliadd "alias_name", "50:01:..."'))
    lines.append(txt_row('  cfgenable      = Activates the named zone configuration across all fabric switches'))
    lines.append(txt_row('  firmwaredownload = Downloads and installs FabricOS from a TFTP/FTP/SCP server'))
    lines.append(txt_row('  configupload   = Upload running config to a remote server for backup'))
    lines.append(txt_row('  supportshow    = Full diagnostic dump for TAC; combines 50+ show commands'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-operations-issues',
    'docs/san/brocade/fabric-os/operations/common-issues/index.md',
    'FabricOS Common Issues — port flapping, zone conflicts, ISL degradation, login storms',
)
def brocade_fabric_os_operations_issues():
    """FabricOS Common Issues — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'FabricOS — Common Issues'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Most common FabricOS issues with root causes and resolution steps')))
    lines.append(R(bMid(IV_L, IV_R, 'Port issues: flapping (bad SFP/cable), offline (config/speed mismatch), BB credit zero')))
    lines.append(R(bMid(IV_L, IV_R, 'Zone issues: zone conflict (cfgmerge fail), alias not found, zoning mismatch between switches')))
    lines.append(R(bMid(IV_L, IV_R, 'Fabric issues: segmented fabric (principal switch conflict), ISL degraded, E_Port down')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Port-level issues → zone issues → fabric-wide issues → login storms → escalation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port Issues'), bMid(B2_L, B2_R, 'Zone Issues'), bMid(B3_L, B3_R, 'Fabric Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port flapping'), bMid(B2_L, B2_R, 'Zone conflict'), bMid(B3_L, B3_R, 'Segmented fabric'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port offline'), bMid(B2_L, B2_R, 'Alias not found'), bMid(B3_L, B3_R, 'ISL degraded'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'BB credit = 0'), bMid(B2_L, B2_R, 'Zoning mismatch'), bMid(B3_L, B3_R, 'E_Port down'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CRC errors'), bMid(B2_L, B2_R, 'cfgmerge fail'), bMid(B3_L, B3_R, 'FLOGI storm'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bad SFP/cable'), bMid(B2_L, B2_R, 'Zone not active'), bMid(B3_L, B3_R, 'RSCN loop'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  supportshow output is the primary diagnostic artifact for TAC escalation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Issue', 'Check', 'Command', 'Fix', 'Escalation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Port flap', 'SFP Tx/Rx dBm', 'sfpshow', 'Replace SFP', 'TAC if persist'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Segmented', 'Domain IDs same', 'fabricshow', 'Reset domain ID', 'TAC merge'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['FLOGI storm', 'HBA log events', 'portlogdump', 'portdisable HBA', 'TAC + OS team'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SFP optics · OM4 LC fibre cables · ISL trunk cables · HBA drivers'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Port flapping = Port cycling online/offline rapidly; bad SFP, cable, or HBA driver'))
    lines.append(txt_row('  BB credit     = Buffer-to-buffer credit; zero means port stalled waiting to send frames'))
    lines.append(txt_row('  CRC error     = Cyclic Redundancy Check failure; bad cable, SFP, or dirty connector'))
    lines.append(txt_row('  Zone conflict = cfgmerge failure when two fabrics with incompatible zones are merged'))
    lines.append(txt_row('  cfgmerge      = Automatic zone config merge when ISL established; fails on name conflict'))
    lines.append(txt_row('  Zoning mismatch = Zone config differs between switches; clear and reactivate'))
    lines.append(txt_row('  Segmented fabric = ISL in E_Port Isolated state; domain ID or principal switch conflict'))
    lines.append(txt_row('  E_Port        = Expansion Port; ISL port type; isolated state = fabric segment'))
    lines.append(txt_row('  FLOGI storm   = HBA flooding fabric with Fabric Login requests; disable port to stop'))
    lines.append(txt_row('  RSCN          = Registered State Change Notification; excessive RSCNs disrupt I/O'))
    lines.append(txt_row('  ISL degraded  = ISL link showing errors or reduced bandwidth; check SFPs and cables'))
    lines.append(txt_row('  portlogdump   = Per-port event log dump; captures FLOGI, PLOGI, and error events'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-security',
    'docs/san/brocade/fabric-os/security/index.md',
    'FabricOS Security — LDAP auth, SSH keys, FC-SP, DCC policy, SCC policy, audit logging',
)
def brocade_fabric_os_security():
    """FabricOS Security — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'FabricOS — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FabricOS security: authentication, fabric access control, and audit logging')))
    lines.append(R(bMid(IV_L, IV_R, 'Auth: LDAP/RADIUS integration for admin/operator/user roles; SSH key auth recommended')))
    lines.append(R(bMid(IV_L, IV_R, 'Fabric security: FC-SP between ISL switches; DCC policy controls device login per port')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: secauditlog for all config changes; syslog to SIEM; Secure Fabric mode option')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Admin auth → switch CLI access control → fabric device auth → audit logging'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Authentication'), bMid(B2_L, B2_R, 'Access Control'), bMid(B3_L, B3_R, 'Audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP/RADIUS'), bMid(B2_L, B2_R, 'FC-SP ISL auth'), bMid(B3_L, B3_R, 'secauditlog'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSH key auth'), bMid(B2_L, B2_R, 'DCC policy'), bMid(B3_L, B3_R, 'Syslog export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local accounts'), bMid(B2_L, B2_R, 'SCC policy'), bMid(B3_L, B3_R, 'Login events'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Role: admin'), bMid(B2_L, B2_R, 'Zone enforcement'), bMid(B3_L, B3_R, 'Config changes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Role: operator'), bMid(B2_L, B2_R, 'Secure Fabric'), bMid(B3_L, B3_R, 'Port events'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  DCC + SCC policies prevent unauthorised device fabric login without explicit permit'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Control', 'Standard', 'FOS command', 'Verification', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Auth method', 'LDAP primary', 'aaaconfig', 'aaaconfig --show', 'RADIUS fallback'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['DCC policy', 'Enabled prod', 'dccpolicyshow', 'dccpolicyadd', 'Per-port binding'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Audit log', 'Syslog + local', 'syslogdipadd', 'secauditlogshow', 'SIEM retention'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: out-of-band management via SSH from jump host; HTTPS for SANnav'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  FC-SP         = Fibre Channel Security Protocol; mutual auth between ISL-connected switches'))
    lines.append(txt_row('  DCC policy    = Device Connection Control; binds specific WWNs to specific ports'))
    lines.append(txt_row('  SCC policy    = Switch Connection Control; restricts which switches can join via ISL'))
    lines.append(txt_row('  secauditlog   = FabricOS security audit log; records all security-relevant CLI events'))
    lines.append(txt_row('  aaaconfig     = FabricOS command for configuring LDAP/RADIUS authentication order'))
    lines.append(txt_row('  RADIUS        = Alternative to LDAP; supports accounting for auth logging per session'))
    lines.append(txt_row('  SSH key auth  = Public key authentication for admin SSH; no password over the wire'))
    lines.append(txt_row('  Secure Fabric = Optional FabricOS mode requiring DCC and SCC policies to be active'))
    lines.append(txt_row('  Admin role    = Full switch access: zoning, port admin, firmware, user management'))
    lines.append(txt_row('  Operator role = Limited to monitoring; no zone or config changes'))
    lines.append(txt_row('  Syslog        = FabricOS event log forwarded to SIEM; syslogdipadd sets destination IP'))
    lines.append(txt_row('  LDAP          = Centralised directory auth; maps LDAP groups to FabricOS admin/operator'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-troubleshooting',
    'docs/san/brocade/fabric-os/troubleshooting/index.md',
    'FabricOS Troubleshooting — port errors, fabric segmentation, ISL issues, log analysis',
)
def brocade_fabric_os_troubleshooting():
    """FabricOS Troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'FabricOS — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FabricOS troubleshooting workflow: port → fabric → ISL → trunk → escalation')))
    lines.append(R(bMid(IV_L, IV_R, 'Port-level: portshow, portlogdump, portperfshow, porterrshow for individual port issues')))
    lines.append(R(bMid(IV_L, IV_R, 'Fabric-level: fabricshow, nsshow, topologyshow for namespace and topology issues')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: supportshow output + RASlog bundle sent to Broadcom/Dell TAC')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Port-level → fabric-level → ISL/trunk → RASlog analysis → TAC escalation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port Level'), bMid(B2_L, B2_R, 'Fabric Level'), bMid(B3_L, B3_R, 'Escalation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'portshow'), bMid(B2_L, B2_R, 'fabricshow'), bMid(B3_L, B3_R, 'supportshow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'portlogdump'), bMid(B2_L, B2_R, 'nsshow'), bMid(B3_L, B3_R, 'RASlog bundle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'portperfshow'), bMid(B2_L, B2_R, 'topologyshow'), bMid(B3_L, B3_R, 'Dell/Broadcom TAC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'porterrshow'), bMid(B2_L, B2_R, 'iodshow'), bMid(B3_L, B3_R, 'configupload'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'sfpshow'), bMid(B2_L, B2_R, 'trunkshow'), bMid(B3_L, B3_R, 'Firmware check'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Always run supportshow before any disruptive action; output needed for TAC case'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'First command', 'Key output', 'Resolution', 'Escalation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Port offline', 'portshow N', 'State, no_sync', 'Check SFP/cable', 'TAC if persist'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Segmented', 'fabricshow', 'Domain IDs', 'Domain conflict', 'TAC merge'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Slow I/O', 'portperfshow', 'MB/s per port', 'BB credit / ISL', 'TAC + storage'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SFP Tx/Rx dBm · LC cable continuity · ISL physical path · HBA driver'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  portshow N    = Detailed state for port N; shows login state, connected WWN, errors'))
    lines.append(txt_row('  portlogdump   = FIFO event log for a port; captures FLOGI/PLOGI events and errors'))
    lines.append(txt_row('  portperfshow  = Real-time port throughput; run during I/O to see bytes/sec'))
    lines.append(txt_row('  porterrshow   = Error counters for all ports: CRC, LOS, LOSync, Bad EOF'))
    lines.append(txt_row('  fabricshow    = All switches in the fabric; shows domain IDs and principal switch'))
    lines.append(txt_row('  nsshow        = Name Server entries (FLOGI database); lists all logged-in devices'))
    lines.append(txt_row('  topologyshow  = ISL topology map including inter-switch distances and port connections'))
    lines.append(txt_row('  trunkshow     = ISL trunk member ports and bandwidth utilisation per trunk group'))
    lines.append(txt_row('  iodshow       = In-Order Delivery state; relevant when frames arrive out of order'))
    lines.append(txt_row('  RASlog        = FabricOS Reliability, Availability, Serviceability log; TAC key artifact'))
    lines.append(txt_row('  supportshow   = Combined diagnostic output of 50+ show commands; attach to TAC case'))
    lines.append(txt_row('  configupload  = Back up switch config before any change or TAC-guided recovery'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-dcnm',
    'docs/san/cisco/cisco-dcnm/index.md',
    'Cisco DCNM — centralised management for Nexus (LAN) and MDS (SAN) NX-OS fabrics',
)
def cisco_dcnm():
    """Cisco DCNM management platform — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco DCNM — Data Center Network Manager'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'DCNM: centralised management for Cisco NX-OS — Nexus (LAN) and MDS (SAN) fabrics')))
    lines.append(R(bMid(IV_L, IV_R, 'Deployed as OVA (ESXi) or ISO (bare metal); modes: LAN, SAN, or Unified')))
    lines.append(R(bMid(IV_L, IV_R, 'SAN mode manages MDS 9000 VSANs, zones, ISLs, and SAN Analytics performance')))
    lines.append(R(bMid(IV_L, IV_R, 'Provides fabric discovery, template-based provisioning, compliance, and reporting')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Fabric discovery → zone management → performance monitoring → compliance reporting'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fabric Management'), bMid(B2_L, B2_R, 'SAN Analytics'), bMid(B3_L, B3_R, 'Compliance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Switch discovery'), bMid(B2_L, B2_R, 'Flow telemetry'), bMid(B3_L, B3_R, 'Config check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Topology map'), bMid(B2_L, B2_R, 'Port metrics'), bMid(B3_L, B3_R, 'Policy audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VSAN/zone mgmt'), bMid(B2_L, B2_R, 'IOPS/latency'), bMid(B3_L, B3_R, 'Change tracking'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ISL management'), bMid(B2_L, B2_R, 'Top-N reports'), bMid(B3_L, B3_R, 'Diff baseline'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Template deploy'), bMid(B2_L, B2_R, 'Alert thresholds'), bMid(B3_L, B3_R, 'Audit log'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  DCNM communicates with switches via SSH (config) and SNMP/Telemetry (monitoring)'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Function', 'Protocol', 'Output', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Discovery', 'Topo/inventory', 'SSH/SNMP', 'Switch list', 'Credentials'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Zone mgmt', 'VSAN/zone CRUD', 'SSH CLI', 'Zone config', 'Active zone'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Analytics', 'Flow telemetry', 'Telemetry', 'IOPS/latency', 'Licence req.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Compliance', 'Policy check', 'Config diff', 'Report/alert', 'Baseline snap'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: DCNM OVA (8 vCPU/32 GB RAM) · OOB management VLAN · Cisco MDS 9000 switches'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  DCNM          = Data Center Network Manager; Cisco centralised fabric management platform'))
    lines.append(txt_row('  NX-OS         = Cisco data centre OS running on Nexus and MDS switch platforms'))
    lines.append(txt_row('  VSAN          = Virtual SAN; logical partition of the FC fabric; each VSAN is isolated'))
    lines.append(txt_row('  Zone          = FC zone: set of port WWNs allowed to communicate within a VSAN'))
    lines.append(txt_row('  Active zone   = Zone configuration currently enforced on the fabric; push activates it'))
    lines.append(txt_row('  ISL           = Inter-Switch Link; FC trunk connecting two MDS switches in the fabric'))
    lines.append(txt_row('  SAN Analytics = DCNM module capturing frame-level telemetry; requires Analytics licence'))
    lines.append(txt_row('  Telemetry     = Streaming push from switch to DCNM collector; lower latency than polling'))
    lines.append(txt_row('  OVA           = Open Virtual Appliance; VMware VM image format used for DCNM deployment'))
    lines.append(txt_row('  Compliance    = DCNM feature comparing running config vs golden baseline; flags drifts'))
    lines.append(txt_row('  Template      = DCNM config template applied to switch interfaces, VSANs, or policies'))
    lines.append(txt_row('  SNMP          = Simple Network Management Protocol; used for fault and performance polling'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-dcnm-operations',
    'docs/san/cisco/cisco-dcnm/operations/index.md',
    'DCNM Operations — fabric discovery, VSAN/zone management, analytics, backup/restore',
)
def cisco_dcnm_operations():
    """Cisco DCNM Operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco DCNM — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'DCNM day-2 operations: discovery management, zone changes, analytics, and backup')))
    lines.append(R(bMid(IV_L, IV_R, 'Discovery: add switch via IP, provide SSH credentials, DCNM polls SNMP + SSH')))
    lines.append(R(bMid(IV_L, IV_R, 'Zone workflow: create device aliases → build zones → add to zone set → activate')))
    lines.append(R(bMid(IV_L, IV_R, 'Analytics: IOPS/latency dashboards, top-N flows, threshold-based alerts')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Discovery → inventory → zone management → performance analytics → backup'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Discovery Ops'), bMid(B2_L, B2_R, 'Zone Ops'), bMid(B3_L, B3_R, 'Analytics Ops'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Add switch by IP'), bMid(B2_L, B2_R, 'Create device alias'), bMid(B3_L, B3_R, 'Enable telemetry'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Set credentials'), bMid(B2_L, B2_R, 'Build zone members'), bMid(B3_L, B3_R, 'View IOPS/latency'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rediscover fabric'), bMid(B2_L, B2_R, 'Add zone to set'), bMid(B3_L, B3_R, 'Top-N flows'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Template push'), bMid(B2_L, B2_R, 'Activate zone set'), bMid(B3_L, B3_R, 'Alert thresholds'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Inventory export'), bMid(B2_L, B2_R, 'Verify no_change'), bMid(B3_L, B3_R, 'Report export'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Backup: DCNM > Administration > Backup and Restore; schedule daily; test restore'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Task', 'DCNM path', 'Key field', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Add switch', 'Discovery>Disc.', 'Seed IP', 'Reachable', 'SSH creds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Zone create', 'SAN>Zoning', 'VSAN select', 'Active zone', 'Alias first'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Analytics', 'SAN>Analytics', 'Flow filter', 'IOPS graph', 'Lic. active'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Backup', 'Admin>Backup', 'Schedule', 'File size', 'Off-box copy'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: DCNM management VM · OOB switch mgmt ports · SAN Analytics telemetry path'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Device alias    = Named alias for a port WWN in DCNM; use instead of raw WWNs in zones'))
    lines.append(txt_row('  Zone set        = Named collection of zones; only one zone set can be active per VSAN'))
    lines.append(txt_row('  Activate        = Push zone set to all switches in VSAN; disrupts traffic if done wrong'))
    lines.append(txt_row('  Rediscover      = Force DCNM to re-poll switch topology; clears stale inventory'))
    lines.append(txt_row('  Template push   = DCNM applies a config template to one or more switches via SSH'))
    lines.append(txt_row('  IOPS            = Input/Output Operations Per Second; primary SAN throughput metric'))
    lines.append(txt_row('  Top-N flows     = Analytics view of highest-throughput initiator/target pairs'))
    lines.append(txt_row('  Threshold alert = DCNM alarm triggered when IOPS/latency exceeds configured limit'))
    lines.append(txt_row('  Backup          = DCNM config export: database + switch discovered state snapshot'))
    lines.append(txt_row('  Seed IP         = First switch IP given to DCNM; discovery fans out from this seed'))
    lines.append(txt_row('  Credentials     = Switch SSH username/password stored in DCNM for config operations'))
    lines.append(txt_row('  Verify          = Post-zone-change check: show zoneset active vsan X on each switch'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-dcnm-security',
    'docs/san/cisco/cisco-dcnm/security/index.md',
    'DCNM Security — RBAC, AAA (RADIUS/TACACS+), certificates, compliance, audit',
)
def cisco_dcnm_security():
    """Cisco DCNM Security — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco DCNM — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'DCNM security: RBAC roles, AAA via RADIUS/TACACS+, TLS certs, and switch compliance')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC roles: network-admin (full), network-operator (read), network-stby (standby)')))
    lines.append(R(bMid(IV_L, IV_R, 'AAA: RADIUS or TACACS+ server; local user fallback if server unreachable')))
    lines.append(R(bMid(IV_L, IV_R, 'Compliance: compare running switch config against golden baseline; report drifts')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  AAA auth → RBAC role assignment → feature access control → audit logging'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access Control'), bMid(B2_L, B2_R, 'Certificates'), bMid(B3_L, B3_R, 'Compliance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC role assign'), bMid(B2_L, B2_R, 'Self-signed CA'), bMid(B3_L, B3_R, 'Baseline snap'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RADIUS/TACACS+'), bMid(B2_L, B2_R, 'CA-signed cert'), bMid(B3_L, B3_R, 'Config compare'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local fallback'), bMid(B2_L, B2_R, 'Cert renewal'), bMid(B3_L, B3_R, 'Drift report'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSH key mgmt'), bMid(B2_L, B2_R, 'HTTPS enforce'), bMid(B3_L, B3_R, 'Policy alert'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Audit log'), bMid(B2_L, B2_R, 'Cipher restrict'), bMid(B3_L, B3_R, 'Remediate'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  HTTPS only; disable HTTP; use CA-signed cert for browser trust and API clients'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Control', 'Mechanism', 'Config path', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Auth', 'RADIUS/TACACS+', 'Admin>AAA', 'Login works', 'Local fallback'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['AuthZ', 'RBAC role', 'Admin>Roles', 'Feature test', 'Per group'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['TLS', 'CA-signed cert', 'Admin>Certs', 'Browser lock', 'Annual renew'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Compliance', 'Baseline diff', 'SAN>Complianc', 'Drift count', 'Alert email'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: RADIUS/TACACS+ server reachable via OOB management · cert private key secured'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RBAC           = Role-Based Access Control; controls which DCNM features each user can access'))
    lines.append(txt_row('  network-admin  = Full read-write access to all DCNM functions and switch configuration'))
    lines.append(txt_row('  network-operator = Read-only access; cannot push zone changes or config templates'))
    lines.append(txt_row('  RADIUS         = Remote Authentication Dial-In User Service; UDP-based AAA protocol'))
    lines.append(txt_row('  TACACS+        = Terminal Access Controller Access-Control System Plus; TCP-based AAA'))
    lines.append(txt_row('  Local fallback = DCNM uses local user DB if AAA server is unreachable; keep enabled'))
    lines.append(txt_row('  TLS cert       = HTTPS certificate for DCNM web UI; CA-signed prevents browser warnings'))
    lines.append(txt_row('  Compliance     = DCNM policy engine comparing switch running config to golden snapshot'))
    lines.append(txt_row('  Baseline snap  = Saved golden-state config used as compliance reference point'))
    lines.append(txt_row('  Drift          = Any difference between running config and baseline; flagged in report'))
    lines.append(txt_row('  Audit log      = DCNM record of all user actions with timestamp, user, and change detail'))
    lines.append(txt_row('  SSH key mgmt   = DCNM stores switch SSH credentials; rotate on schedule, audit access'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-dcnm-troubleshooting',
    'docs/san/cisco/cisco-dcnm/troubleshooting/index.md',
    'DCNM Troubleshooting — discovery failures, analytics gaps, zone push errors, DB recovery',
)
def cisco_dcnm_troubleshooting():
    """Cisco DCNM Troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco DCNM — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'DCNM troubleshooting: discovery failures, analytics data gaps, zone errors, DB recovery')))
    lines.append(R(bMid(IV_L, IV_R, 'Discovery fails: verify SSH creds, SNMP community, management reachability')))
    lines.append(R(bMid(IV_L, IV_R, 'Analytics gaps: confirm SAN Analytics licence, telemetry collector running')))
    lines.append(R(bMid(IV_L, IV_R, 'Zone push fails: check VSAN state, active zone conflict; test with POAP off')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Symptom → collect DCNM logs → isolate layer → resolve and verify → document'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Discovery Issues'), bMid(B2_L, B2_R, 'Analytics Issues'), bMid(B3_L, B3_R, 'Zone Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Switch unreachable'), bMid(B2_L, B2_R, 'No data shown'), bMid(B3_L, B3_R, 'Push rejected'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Auth failure'), bMid(B2_L, B2_R, 'Licence missing'), bMid(B3_L, B3_R, 'VSAN mismatch'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SNMP timeout'), bMid(B2_L, B2_R, 'Collector down'), bMid(B3_L, B3_R, 'Active conflict'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Stale inventory'), bMid(B2_L, B2_R, 'Telemetry gap'), bMid(B3_L, B3_R, 'Alias dup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB corruption'), bMid(B2_L, B2_R, 'Flow filter err'), bMid(B3_L, B3_R, 'Zone set lock'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Logs: /var/log/dcnm/ on DCNM appliance; enable debug level for discovery and zoning'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'First check', 'Key command', 'Resolution', 'Escalation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Disc. fails', 'Ping mgmt IP', 'ssh admin@SW', 'Fix creds', 'TAC + logs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['No analytics', 'Lic. page', 'show lic.', 'Add SAN Anlt.', 'Cisco Lic.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Zone fails', 'VSAN state', 'show vsan X', 'Resolve VSAN', 'TAC if locked'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['DB corrupt', 'DCNM status', 'appmgr status', 'Restore backup', 'TAC + snap'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: verify OOB reachability switch mgmt port → DCNM VM NIC · check SAN Analytics NIC'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  appmgr        = DCNM appliance service manager; use to check/restart DCNM services'))
    lines.append(txt_row('  Discovery fail = DCNM cannot SSH or SNMP poll a switch; check creds, reachability, ACLs'))
    lines.append(txt_row('  Stale inventory = Switch shows in DCNM but data is outdated; trigger manual rediscover'))
    lines.append(txt_row('  SAN Analytics  = DCNM performance module; requires separate licence and telemetry collector'))
    lines.append(txt_row('  Telemetry gap  = No flow data in DCNM analytics; check gRPC telemetry on switch'))
    lines.append(txt_row('  Active conflict = Zone push rejected because active zone set has different member count'))
    lines.append(txt_row('  Zone set lock  = DCNM or switch holds zone change lock; clear with no zone commit abort'))
    lines.append(txt_row('  DB corruption  = DCNM PostgreSQL DB integrity failure; restore from scheduled backup'))
    lines.append(txt_row('  POAP           = Power-On Auto-Provisioning; disable during zone troubleshooting'))
    lines.append(txt_row('  gRPC telemetry = Switch streaming protocol pushing port counters/flow stats to DCNM'))
    lines.append(txt_row('  Alias dup      = Duplicate device alias for different WWNs causes zone push rejection'))
    lines.append(txt_row('  Licence page   = DCNM > Administration > Licensing; shows installed and missing features'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-mds-operations',
    'docs/san/cisco/mds/operations/index.md',
    'Cisco MDS Operations — VSAN management, zoning, ISL/port-channel, firmware, show commands',
)
def cisco_mds_operations():
    """Cisco MDS 9000 Operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco MDS 9000 — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'MDS 9000 day-2 operations: VSAN management, zoning, ISL, port channels, ISSU')))
    lines.append(R(bMid(IV_L, IV_R, 'VSAN: create VSAN, assign ports, verify VSAN membership; VSAN 1 default — avoid')))
    lines.append(R(bMid(IV_L, IV_R, 'Zoning: device aliases → zones → zone sets → activate per VSAN')))
    lines.append(R(bMid(IV_L, IV_R, 'ISSU: In-Service Software Upgrade; minimises disruption on dual-supervisor MDS')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  VSAN create → port assign → zone build → zone activate → health verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VSAN / ISL Ops'), bMid(B2_L, B2_R, 'Zoning Ops'), bMid(B3_L, B3_R, 'Health Checks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create VSAN'), bMid(B2_L, B2_R, 'Create alias'), bMid(B3_L, B3_R, 'show interface'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Assign VSAN port'), bMid(B2_L, B2_R, 'Create zone'), bMid(B3_L, B3_R, 'show vsan'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Trunk ISL ports'), bMid(B2_L, B2_R, 'Add to zone set'), bMid(B3_L, B3_R, 'show zoneset'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port channel ISL'), bMid(B2_L, B2_R, 'Activate zone'), bMid(B3_L, B3_R, 'show flogi db'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ISSU firmware'), bMid(B2_L, B2_R, 'Verify members'), bMid(B3_L, B3_R, 'show port-ch.'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Always backup config before zone changes: copy running-config startup-config'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Task', 'NX-OS command', 'Key output', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Create VSAN', 'vsan database', 'vsan N', 'show vsan N', 'Name it'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Zone create', 'zone name Z vN', 'member pwwn', 'show zone', 'Alias better'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Activate', 'zoneset activate', 'Changes#', 'show zoneset act', 'No disruption'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ISSU', 'install all', 'Superv check', 'show version', 'Dual-sup req.'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: MDS 9000 line cards · FC SFP transceivers (SW/LW/CWDM) · ISL fibre paths'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  VSAN          = Virtual SAN; logical fabric partition on MDS; isolates devices and zones'))
    lines.append(txt_row('  Device alias  = Named alias for a port WWN; recommended over raw WWN in zone membership'))
    lines.append(txt_row('  Zone set      = Container for zones in a VSAN; activate to enforce; only one active'))
    lines.append(txt_row('  Activate      = Deploy zone set to all switches in VSAN; non-disruptive if correctly done'))
    lines.append(txt_row('  FLOGI         = Fabric Login; device procedure to join FC fabric and receive FC address'))
    lines.append(txt_row('  FCNS          = FC Name Server; VSAN-scoped directory of all logged-in devices'))
    lines.append(txt_row('  ISSU          = In-Service Software Upgrade; upgrades NX-OS without disrupting traffic'))
    lines.append(txt_row('  Trunk ISL     = ISL configured to carry multiple VSANs; uses E_port/TE_port mode'))
    lines.append(txt_row('  Port channel  = Bundle of ISL ports for higher bandwidth and link redundancy'))
    lines.append(txt_row('  show flogi db = Displays all devices that have logged into the fabric on this switch'))
    lines.append(txt_row('  show zoneset  = Shows active zone set for a VSAN; use active keyword for enforced config'))
    lines.append(txt_row('  copy run start = Saves running configuration to startup; always run after changes'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-mds-security',
    'docs/san/cisco/mds/security/index.md',
    'Cisco MDS Security — fabric binding, port security, FC-SP-2, RBAC, AAA, audit',
)
def cisco_mds_security():
    """Cisco MDS 9000 Security — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco MDS 9000 — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'MDS security: fabric binding, port security, FC-SP-2 auth, RBAC, AAA, audit log')))
    lines.append(R(bMid(IV_L, IV_R, 'Fabric binding: restrict which switch WWNs may join fabric; prevents rogue switches')))
    lines.append(R(bMid(IV_L, IV_R, 'Port security: restrict which device WWNs may login to each FC port')))
    lines.append(R(bMid(IV_L, IV_R, 'FC-SP-2: DHCHAP mutual authentication between switches; prevents fabric spoofing')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  AAA login → RBAC role → feature group access → audit logging → compliance check'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fabric Security'), bMid(B2_L, B2_R, 'Access Control'), bMid(B3_L, B3_R, 'Audit / Acct'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fabric binding'), bMid(B2_L, B2_R, 'RBAC roles'), bMid(B3_L, B3_R, 'Accounting log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port security'), bMid(B2_L, B2_R, 'RADIUS/TACACS+'), bMid(B3_L, B3_R, 'AAA acct start'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FC-SP-2 DHCHAP'), bMid(B2_L, B2_R, 'SSH key auth'), bMid(B3_L, B3_R, 'Syslog export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VSAN isolation'), bMid(B2_L, B2_R, 'Local fallback'), bMid(B3_L, B3_R, 'SNMP traps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Zoning enforce'), bMid(B2_L, B2_R, 'Password policy'), bMid(B3_L, B3_R, 'Audit review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Enable accounting for all exec and config sessions; export to centralised syslog'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Control', 'Mechanism', 'NX-OS command', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Fabric bind', 'Switch WWN', 'fabric-binding', 'show f-bind', 'Per VSAN'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Port sec.', 'Device WWN', 'port-security', 'show port-sec', 'Activate DB'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['FC-SP-2', 'DHCHAP secret', 'fcsp enable', 'show fcsp', 'Both switches'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['AAA auth', 'RADIUS/TACACS+', 'aaa group sv.', 'Test login', 'Local backup'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: RADIUS/TACACS+ server on OOB management · SSH keys on jump host · syslog server'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Fabric binding  = Allowlist of switch WWNs permitted to join fabric via E_port; VSAN-scoped'))
    lines.append(txt_row('  Port security   = Allowlist of device pWWNs permitted to login on a specific FC port'))
    lines.append(txt_row('  FC-SP-2         = Fibre Channel Security Protocol v2; DHCHAP mutual auth between FC switches'))
    lines.append(txt_row('  DHCHAP          = DH-CHAP: Diffie-Hellman Challenge Handshake Auth Protocol; no password TX'))
    lines.append(txt_row('  VSAN isolation  = Traffic in one VSAN cannot cross into another; intrinsic security boundary'))
    lines.append(txt_row('  RBAC roles      = network-admin (full), network-operator (read), custom feature groups'))
    lines.append(txt_row('  AAA             = Authentication, Authorisation, Accounting; Cisco switches support both'))
    lines.append(txt_row('  Accounting log  = NX-OS audit log; records all exec commands and config changes with user'))
    lines.append(txt_row('  SSH key auth    = Public-key authentication for switch management; disable password auth'))
    lines.append(txt_row('  Syslog export   = Forward accounting and system logs to centralised syslog for SIEM'))
    lines.append(txt_row('  SNMP trap       = Fault notification; restrict SNMP community to read-only on OOB only'))
    lines.append(txt_row('  Password policy = Enforce min length, complexity, rotation on all local accounts'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-mds-troubleshooting',
    'docs/san/cisco/mds/troubleshooting/index.md',
    'Cisco MDS Troubleshooting — port offline, VSAN isolation, login failures, ISL issues',
)
def cisco_mds_troubleshooting():
    """Cisco MDS 9000 Troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco MDS 9000 — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'MDS troubleshooting: port offline, VSAN isolated, login failures, ISL flap')))
    lines.append(R(bMid(IV_L, IV_R, 'Port offline: check SFP Rx/Tx power, cable continuity, HBA driver, VSAN assign')))
    lines.append(R(bMid(IV_L, IV_R, 'VSAN isolated: domain ID conflict or ISL allowed-VSAN mismatch; check trunk')))
    lines.append(R(bMid(IV_L, IV_R, 'Login failure: device not in FLOGI DB; verify zone membership and VSAN port')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Symptom → show command → physical check → config verify → resolve → document'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port Issues'), bMid(B2_L, B2_R, 'VSAN / Zone'), bMid(B3_L, B3_R, 'ISL Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port offline'), bMid(B2_L, B2_R, 'VSAN isolated'), bMid(B3_L, B3_R, 'ISL down'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SFP degraded'), bMid(B2_L, B2_R, 'Domain conflict'), bMid(B3_L, B3_R, 'Trunk mismatch'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FLOGI fail'), bMid(B2_L, B2_R, 'Zone lockout'), bMid(B3_L, B3_R, 'Allowed VSAN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HBA mismatch'), bMid(B2_L, B2_R, 'Alias missing'), bMid(B3_L, B3_R, 'Port channel'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Speed mismatch'), bMid(B2_L, B2_R, 'Wrong active ZS'), bMid(B3_L, B3_R, 'ISL overload'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Always run show tech-support fc before TAC escalation; save output off-switch'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'First command', 'Key output', 'Resolution', 'Escalation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Port offline', 'show int fc X/Y', 'State, reasons', 'SFP/cable fix', 'TAC if persist'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['VSAN isolated', 'show vsan X', 'State=isolated', 'Fix domain ID', 'TAC merge help'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['FLOGI miss', 'show flogi db', 'WWN present?', 'Fix zone/VSAN', 'TAC + sniff'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ISL down', 'show int fc X/Y', 'Trunk state', 'Fix trunk mode', 'TAC if link'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SFP Tx/Rx dBm · LC cable · patch panel continuity · HBA driver and firmware'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  show int fc X/Y  = Interface state, SFP power, error counters; first command for port issues'))
    lines.append(txt_row('  show flogi db    = FC fabric login table; confirms which devices have joined the fabric'))
    lines.append(txt_row('  show vsan X      = VSAN membership and state (active/isolated); isolated = domain conflict'))
    lines.append(txt_row('  show zoneset act = Active zone set contents per VSAN; verify initiator/target pairs'))
    lines.append(txt_row('  VSAN isolated    = MDS quarantines VSAN when domain ID conflict detected on ISL'))
    lines.append(txt_row('  Domain ID        = Unique numeric ID per switch per VSAN; conflict causes isolation'))
    lines.append(txt_row('  Trunk mismatch   = ISL port trunk mode or allowed-VSAN list differs between both ends'))
    lines.append(txt_row('  FLOGI            = Fabric Login; device registers WWN with Name Server when joining VSAN'))
    lines.append(txt_row('  SFP degraded     = Optical Rx below −14 dBm or Tx out-of-spec; replace transceiver'))
    lines.append(txt_row('  HBA mismatch     = HBA driver/firmware version incompatible with FC speed or features'))
    lines.append(txt_row('  show tech-support fc = Full diagnostic bundle for FC; attach to TAC case before escalate'))
    lines.append(txt_row('  Zone lockout     = Device can FLOGI but not see storage; zone missing or wrong VSAN'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-nexus-dashboard',
    'docs/san/cisco/nexus-dashboard/index.md',
    'Cisco Nexus Dashboard — multi-domain management platform hosting NDFC, NDI, and NDO',
)
def cisco_nexus_dashboard():
    """Cisco Nexus Dashboard — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Multi-Domain Management Platform'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Nexus Dashboard: multi-domain management platform hosting Insights, NDFC, and Orchestrator')))
    lines.append(R(bMid(IV_L, IV_R, 'Replaces DCNM; 3-node or 5-node cluster; form factors: virtual, physical, or cloud')))
    lines.append(R(bMid(IV_L, IV_R, 'NDFC (Nexus Dashboard Fabric Controller) replaces DCNM for LAN and SAN management')))
    lines.append(R(bMid(IV_L, IV_R, 'NDI: assurance and troubleshooting; NDO: multi-site policy push for ACI/NX-OS')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Cluster deployment → app install → site onboarding → fabric management and assurance'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Hosted Apps'), bMid(B2_L, B2_R, 'Cluster'), bMid(B3_L, B3_R, 'Connectivity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NDFC (fabric)'), bMid(B2_L, B2_R, '3-node HA min'), bMid(B3_L, B3_R, 'OOB mgmt VLAN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NDI (insights)'), bMid(B2_L, B2_R, '5-node for scale'), bMid(B3_L, B3_R, 'Data VLAN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NDO (orchestr.)'), bMid(B2_L, B2_R, 'Master/Worker'), bMid(B3_L, B3_R, 'Ext. svc IPs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'AppStore install'), bMid(B2_L, B2_R, 'Standby node'), bMid(B3_L, B3_R, 'In-band option'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App lifecycle'), bMid(B2_L, B2_R, 'Quorum (2 of 3)'), bMid(B3_L, B3_R, 'Fabric data NW'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Virtual node: 16 vCPU / 64 GB RAM / 550 GB disk; physical: Cisco UCS C220 or ND appliance'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['App', 'Function', 'Replaces', 'Key feature', 'Licence'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NDFC', 'Fabric mgmt', 'DCNM', 'Zone/VSAN', 'Essentials'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NDI', 'Assurance', 'None (new)', 'Flow analysis', 'Premier'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NDO', 'Multi-site', 'MSO/mso', 'Policy sync', 'Advanced'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ND cluster', 'App platform', 'DCNM VM', 'HA + scale', 'Bundled'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ND virtual nodes on vSphere/KVM · OOB management switch · Data fabric switches'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Nexus Dashboard = Cisco platform hosting fabric management and assurance apps as pods'))
    lines.append(txt_row('  NDFC          = Nexus Dashboard Fabric Controller; replaces standalone DCNM'))
    lines.append(txt_row('  NDI           = Nexus Dashboard Insights; flow-level assurance, anomaly detection'))
    lines.append(txt_row('  NDO           = Nexus Dashboard Orchestrator; multi-site ACI/NX-OS policy management'))
    lines.append(txt_row('  Master node   = Runs Kubernetes control plane and ND system services; always 3 masters'))
    lines.append(txt_row('  Worker node   = Optional; adds compute for app pods; increases app hosting capacity'))
    lines.append(txt_row('  Standby node  = Hot spare; automatically promotes if a master fails'))
    lines.append(txt_row('  Quorum        = ND requires 2 of 3 master nodes healthy for full read-write operation'))
    lines.append(txt_row('  OOB network   = Management network for ND admin access and switch credential SSH'))
    lines.append(txt_row('  Data network  = Fabric-facing network; ND apps use this to poll switch telemetry'))
    lines.append(txt_row('  Ext. svc IP   = External service IPs pool; allocated for app ingress endpoints'))
    lines.append(txt_row('  AppStore      = ND built-in app catalogue; install and upgrade apps from Cisco hosted repo'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-nexus-dashboard-arch-standards',
    'docs/san/cisco/nexus-dashboard/architecture/design-standards/index.md',
    'Nexus Dashboard Architecture Design Standards — sizing, HA, networking, app placement',
)
def cisco_nexus_dashboard_arch_standards():
    """Cisco Nexus Dashboard Architecture Design Standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Architecture Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ND design standards: node sizing, HA topology, network requirements, app placement rules')))
    lines.append(R(bMid(IV_L, IV_R, 'Always deploy 3 master nodes minimum; never 1-node or 2-node in production')))
    lines.append(R(bMid(IV_L, IV_R, 'OOB and Data networks must be separate VLANs; MTU 9000 required on Data VLAN')))
    lines.append(R(bMid(IV_L, IV_R, 'NDI and NDFC can co-exist on same cluster; NDO should be on a dedicated cluster')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Size cluster → configure networks → deploy nodes → install apps → validate'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Node Sizing'), bMid(B2_L, B2_R, 'Network Design'), bMid(B3_L, B3_R, 'App Placement'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Virt: 16vCPU'), bMid(B2_L, B2_R, 'OOB mgmt VLAN'), bMid(B3_L, B3_R, 'NDFC + NDI OK'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Virt: 64 GB RAM'), bMid(B2_L, B2_R, 'Data VLAN sep.'), bMid(B3_L, B3_R, 'NDO separate'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Virt: 550 GB disk'), bMid(B2_L, B2_R, 'MTU 9000 data'), bMid(B3_L, B3_R, 'Per Cisco guide'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Phys: UCS C220'), bMid(B2_L, B2_R, 'Ext svc IP /27'), bMid(B3_L, B3_R, 'App compat list'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3 masters + W'), bMid(B2_L, B2_R, 'DNS + NTP req.'), bMid(B3_L, B3_R, 'Worker for scale'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Always check Cisco ND hardware and software compatibility guide before deployment'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Requirement', 'Spec', 'Why', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['HA nodes', '3 masters min', 'Quorum', 'ND cluster UI', 'Add workers'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['OOB VLAN', 'L3 routed', 'Admin access', 'Ping ND IP', 'Dedicated'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Data VLAN', 'Jumbo MTU', 'Telemetry', 'Ping fabric', 'MTU 9000'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['App compat', 'Cisco matrix', 'Co-exist', 'App health', 'NDO separate'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: vSphere cluster (DRS, HA) · dedicated data NIC for each ND node · OOB switch'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Master node    = ND node running Kubernetes control plane; always deploy exactly 3'))
    lines.append(txt_row('  Worker node    = Additional ND compute node for app pods; scale-out option'))
    lines.append(txt_row('  Standby node   = Spare master; auto-joins if a master fails; recommended in production'))
    lines.append(txt_row('  OOB network    = Out-of-band admin network; used for ND UI, SSH, and switch SSH access'))
    lines.append(txt_row('  Data network   = In-band fabric-facing NIC; ND apps poll switches and receive telemetry'))
    lines.append(txt_row('  MTU 9000       = Jumbo frames required on Data VLAN for ND telemetry and flow export'))
    lines.append(txt_row('  Ext. svc IP    = Pool of IPs for Kubernetes LoadBalancer services (ND apps endpoints)'))
    lines.append(txt_row('  App compat     = Cisco publishes which app versions run together on same ND release'))
    lines.append(txt_row('  NDO separation = NDO multi-site orchestration works best isolated from NDFC/NDI cluster'))
    lines.append(txt_row('  DNS required   = ND nodes must resolve DNS; add ND hostnames to DNS before deploy'))
    lines.append(txt_row('  NTP required   = All ND nodes and managed switches must be NTP-synchronised'))
    lines.append(txt_row('  Cisco HCL      = Hardware Compatibility List; verify server model and NIC before deploy'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-nexus-dashboard-operations',
    'docs/san/cisco/nexus-dashboard/operations/index.md',
    'Nexus Dashboard Operations — app lifecycle, cluster health, site management, backups',
)
def cisco_nexus_dashboard_operations():
    """Cisco Nexus Dashboard Operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ND operations: app lifecycle management, cluster health, site onboarding, backups')))
    lines.append(R(bMid(IV_L, IV_R, 'App lifecycle: install from AppStore or upload image; upgrade, enable, disable, delete')))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster health: monitor node status, pod health, resource utilisation in Admin UI')))
    lines.append(R(bMid(IV_L, IV_R, 'Site onboarding: add ACI APIC or NX-OS switch credentials to ND for app use')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  App install → site add → policy configure → health monitor → backup → upgrade'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App Ops'), bMid(B2_L, B2_R, 'Cluster Ops'), bMid(B3_L, B3_R, 'Site Ops'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Install app'), bMid(B2_L, B2_R, 'Node health'), bMid(B3_L, B3_R, 'Add ACI site'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Upgrade app'), bMid(B2_L, B2_R, 'Pod status'), bMid(B3_L, B3_R, 'Add NX-OS site'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Enable/disable'), bMid(B2_L, B2_R, 'Resource usage'), bMid(B3_L, B3_R, 'Site creds'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Delete app'), bMid(B2_L, B2_R, 'Event log'), bMid(B3_L, B3_R, 'Fabric verify'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup cluster'), bMid(B2_L, B2_R, 'Cert renew'), bMid(B3_L, B3_R, 'Site health'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Backup: Admin > System Settings > System Backup; schedule daily; copy off-cluster'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Task', 'ND UI path', 'Key field', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Install app', 'Services>Apps', 'AppStore/img', 'App running', 'Compat check'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Add site', 'Admin>Sites', 'APIC/SNMP IP', 'Site healthy', 'Creds stored'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Node health', 'Admin>Nodes', 'Status', 'All healthy', 'Pod details'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Backup', 'Admin>Backup', 'Schedule', 'File saved', 'Off-cluster'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ND VM datastores · OOB switch mgmt ports · fabric switches in Data VLAN'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  AppStore       = ND built-in catalogue; downloads and installs app images from Cisco CDN'))
    lines.append(txt_row('  App lifecycle  = Install → enable → configure → upgrade → disable → delete workflow'))
    lines.append(txt_row('  Node health    = ND Admin UI node view; shows CPU/RAM/disk per node and pod counts'))
    lines.append(txt_row('  Pod status     = Kubernetes pod state for each app service; Running = healthy'))
    lines.append(txt_row('  Site           = ND term for a managed fabric (ACI cluster or NX-OS fabric)'))
    lines.append(txt_row('  ACI site       = APIC cluster onboarded to ND; NDI and NDO use it for assurance'))
    lines.append(txt_row('  NX-OS site     = NDFC-managed Nexus/MDS fabric registered as ND site'))
    lines.append(txt_row('  Backup         = ND config snapshot including cluster config and app state'))
    lines.append(txt_row('  Cert renew     = ND TLS certs expire; renew before expiry via Admin > Security'))
    lines.append(txt_row('  Event log      = ND system event log; shows node join/leave, app state changes'))
    lines.append(txt_row('  Resource usage = ND node CPU/RAM/disk utilisation; add workers if consistently >70%'))
    lines.append(txt_row('  Compat check   = Verify app version is listed as compatible with installed ND version'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-nexus-dashboard-ops-procedures',
    'docs/san/cisco/nexus-dashboard/operations/procedures/index.md',
    'Nexus Dashboard Ops Procedures — cluster upgrade, node replacement, backup/restore',
)
def cisco_nexus_dashboard_ops_procedures():
    """Cisco Nexus Dashboard Ops Procedures — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Operational Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ND operational procedures: cluster upgrade, node replacement, backup and restore')))
    lines.append(R(bMid(IV_L, IV_R, 'Upgrade: backup first → upload image → trigger upgrade → validate each node')))
    lines.append(R(bMid(IV_L, IV_R, 'Node replace: cordon node → drain pods → decommission → rejoin with same IP')))
    lines.append(R(bMid(IV_L, IV_R, 'Restore: deploy fresh cluster → import backup → validate site and app config')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Pre-check → backup → execute → verify cluster health → verify apps → document'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cluster Upgrade'), bMid(B2_L, B2_R, 'Node Replace'), bMid(B3_L, B3_R, 'Backup/Restore'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Check compat'), bMid(B2_L, B2_R, 'Cordon node'), bMid(B3_L, B3_R, 'Backup cluster'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Take backup'), bMid(B2_L, B2_R, 'Drain pods'), bMid(B3_L, B3_R, 'Copy off-cluster'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Upload image'), bMid(B2_L, B2_R, 'Decommission'), bMid(B3_L, B3_R, 'Deploy new ND'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Trigger upgrade'), bMid(B2_L, B2_R, 'Replace hardware'), bMid(B3_L, B3_R, 'Import backup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Validate health'), bMid(B2_L, B2_R, 'Rejoin cluster'), bMid(B3_L, B3_R, 'Verify apps'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  ND upgrade is rolling (one node at a time); cluster remains available during upgrade'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Procedure', 'Step', 'Command/UI', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Upgrade', 'Pre-check', 'Admin>Upgrade', 'Compat ok', 'Backup first'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Node replace', 'Cordon', 'Admin>Nodes', 'Pods drained', 'Same IP reuse'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Backup', 'Schedule', 'Admin>Backup', 'File size', 'Off-cluster'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Restore', 'Fresh deploy', 'Import backup', 'Apps healthy', 'Sites re-add'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ND VM snapshots before upgrade · replacement hardware in rack · OOB cables'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Rolling upgrade   = ND upgrades one node at a time; other nodes serve traffic'))
    lines.append(txt_row('  Cordon            = Mark node unschedulable so no new pods land on it before replacement'))
    lines.append(txt_row('  Drain             = Move all running pods off a node before maintenance'))
    lines.append(txt_row('  Decommission      = Remove node from ND cluster database; do before physical replacement'))
    lines.append(txt_row('  Rejoin            = New or replaced node boots and joins cluster using same IP and certs'))
    lines.append(txt_row('  Backup import     = ND restore: import cluster config + app state from backup file'))
    lines.append(txt_row('  Compat check      = Confirm ND release supports all installed app versions before upgrade'))
    lines.append(txt_row('  Off-cluster copy  = Transfer backup file to external storage before proceeding'))
    lines.append(txt_row('  Pre-upgrade check = ND built-in upgrade readiness validator; run before uploading image'))
    lines.append(txt_row('  Cluster health    = All nodes Healthy, all pods Running; check after every procedure'))
    lines.append(txt_row('  VM snapshot       = Take vSphere snapshot of ND VMs before upgrade; rollback option'))
    lines.append(txt_row('  Sites re-add      = After restore, verify all site credentials still work in Admin>Sites'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-nexus-dashboard-security',
    'docs/san/cisco/nexus-dashboard/security/index.md',
    'Nexus Dashboard Security — RBAC, AAA (RADIUS/TACACS+/SAML), certificates, audit',
)
def cisco_nexus_dashboard_security():
    """Cisco Nexus Dashboard Security — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ND security: RBAC roles, AAA via RADIUS/TACACS+/SAML, TLS certs, network segments')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC: site-admin, tenant-admin, operator, viewer; roles scoped per site/tenant')))
    lines.append(R(bMid(IV_L, IV_R, 'AAA: RADIUS, TACACS+, or SAML (SSO); local admin fallback always enabled')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: OOB restricted to admin; Data VLAN to fabric only; no cross-VLAN access')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  AAA login → RBAC role → site/tenant scope → resource access → audit log'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access Control'), bMid(B2_L, B2_R, 'Certificates'), bMid(B3_L, B3_R, 'Audit / Acct'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC roles'), bMid(B2_L, B2_R, 'ND UI TLS cert'), bMid(B3_L, B3_R, 'User actions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RADIUS auth'), bMid(B2_L, B2_R, 'App TLS certs'), bMid(B3_L, B3_R, 'Login events'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TACACS+ auth'), bMid(B2_L, B2_R, 'CA-signed req.'), bMid(B3_L, B3_R, 'Config changes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML/SSO'), bMid(B2_L, B2_R, 'Cert renewal'), bMid(B3_L, B3_R, 'Syslog export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local fallback'), bMid(B2_L, B2_R, 'Cipher restrict'), bMid(B3_L, B3_R, 'Audit review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Restrict ND OOB access to jump host / VPN only; never expose ND UI to public internet'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Control', 'Mechanism', 'ND UI path', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Auth', 'RADIUS/SAML', 'Admin>AAA', 'Login test', 'Local backup'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['AuthZ', 'RBAC role', 'Admin>Roles', 'Feature test', 'Per site'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['TLS', 'CA-signed cert', 'Admin>Security', 'Browser lock', 'Annual renew'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Audit', 'Event log', 'Admin>Events', 'Log complete', 'Export SIEM'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: RADIUS/TACACS+/IdP on OOB management · cert private key in secrets vault'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RBAC           = Role-Based Access Control; roles in ND are scoped to site and tenant'))
    lines.append(txt_row('  site-admin     = Full access to a specific site; cannot modify ND cluster config'))
    lines.append(txt_row('  tenant-admin   = Full access within a tenant (ACI); cannot access other tenants'))
    lines.append(txt_row('  SAML           = Security Assertion Markup Language; used for SSO with corporate IdP'))
    lines.append(txt_row('  IdP            = Identity Provider (e.g. Okta, AD FS); issues SAML assertions to ND'))
    lines.append(txt_row('  Local fallback = ND admin account active even if AAA server unreachable; keep enabled'))
    lines.append(txt_row('  TLS cert       = ND HTTPS certificate; use CA-signed for browser trust and API clients'))
    lines.append(txt_row('  Cipher restrict = Disable TLS 1.0/1.1 and weak ciphers on ND; enforce TLS 1.2+'))
    lines.append(txt_row('  OOB restrict   = Limit management network access to bastion hosts or VPN gateway only'))
    lines.append(txt_row('  Data VLAN      = Fabric-facing VLAN for telemetry; restrict to switch management subnets'))
    lines.append(txt_row('  Audit log      = ND logs every user action (login, config change) with user and timestamp'))
    lines.append(txt_row('  Syslog export  = Forward ND audit and system logs to centralised SIEM for retention'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-nexus-dashboard-troubleshooting',
    'docs/san/cisco/nexus-dashboard/troubleshooting/index.md',
    'Nexus Dashboard Troubleshooting — app failures, cluster quorum, site onboarding issues',
)
def cisco_nexus_dashboard_troubleshooting():
    """Cisco Nexus Dashboard Troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ND troubleshooting: app failures, cluster quorum loss, site onboarding errors')))
    lines.append(R(bMid(IV_L, IV_R, 'App not starting: check node resources (CPU/RAM), pod logs, app compatibility')))
    lines.append(R(bMid(IV_L, IV_R, 'Quorum loss: 2+ masters down → read-only mode; restore third node quickly')))
    lines.append(R(bMid(IV_L, IV_R, 'Site fail: verify Data VLAN reachability, APIC/switch credentials, firewall rules')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Symptom → Admin UI events → kubectl pod logs → network test → resolve → verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App Issues'), bMid(B2_L, B2_R, 'Cluster Issues'), bMid(B3_L, B3_R, 'Site Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App not starting'), bMid(B2_L, B2_R, 'Node unhealthy'), bMid(B3_L, B3_R, 'Onboard fail'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App crash loop'), bMid(B2_L, B2_R, 'Quorum loss'), bMid(B3_L, B3_R, 'Cred rejected'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Resource exhaust'), bMid(B2_L, B2_R, 'Node isolated'), bMid(B3_L, B3_R, 'Data NW fail'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App UI down'), bMid(B2_L, B2_R, 'Storage full'), bMid(B3_L, B3_R, 'Firewall block'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App compat err'), bMid(B2_L, B2_R, 'Cert expired'), bMid(B3_L, B3_R, 'Site stale data'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Use ND Admin > Events and kubectl logs for app pods; SSH to node for cluster-level diag'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'First check', 'Key command', 'Resolution', 'Escalation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['App down', 'Node resources', 'kubectl logs', 'Add worker', 'TAC + logs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Quorum loss', 'Node status', 'ND Admin UI', 'Restore node', 'TAC urgent'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Site fails', 'Ping Data IP', 'curl APIC IP', 'Fix network', 'TAC + pcap'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Cert expired', 'Admin>Sec.', 'Cert dates', 'Renew cert', 'TAC if locked'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ND VM compute (vCPU/RAM) · Data NIC connectivity · OOB switch port state'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  kubectl logs    = View pod container log; run from ND master node SSH session'))
    lines.append(txt_row('  App crash loop  = Pod repeatedly starts then fails; check logs for OOM or config error'))
    lines.append(txt_row('  Quorum loss     = Fewer than 2 master nodes reachable; ND enters read-only protection'))
    lines.append(txt_row('  Node isolated   = Master node cannot reach peers; network partition or NIC failure'))
    lines.append(txt_row('  Storage full    = ND etcd or PVC storage full; app pods fail; expand or clean up data'))
    lines.append(txt_row('  Cert expired    = ND TLS cert past expiry; browser blocks access; renew immediately'))
    lines.append(txt_row('  Site onboard fail = ND cannot reach APIC or switch via Data VLAN; check MTU, routing'))
    lines.append(txt_row('  Cred rejected   = Site credentials (APIC admin/password) wrong or account locked'))
    lines.append(txt_row('  Resource exhaust = App pods OOMKilled due to insufficient RAM on cluster; add worker'))
    lines.append(txt_row('  App compat err  = Installed app version incompatible with ND release; upgrade ND first'))
    lines.append(txt_row('  Data NW fail    = ND Data VLAN cannot reach fabric; check VLAN tagging, routing, MTU'))
    lines.append(txt_row('  Stale site data = ND shows outdated fabric topology; re-trigger site discovery'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

# ─── Batch 1: Brocade Fabric OS (1-10) ───────────────────────────────────────

@kb_diagram(
    'brocade-fabric-os',
    'docs/san/brocade/fabric-os/index.md',
    'Brocade Fabric OS — switch OS overview, fabric services, zoning, management interfaces',
)
def brocade_fabric_os():
    """Brocade Fabric OS overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade Fabric OS — Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Fabric OS (FOS): Brocade switch OS for FC SAN — zoning, routing, management')))
    lines.append(R(bMid(IV_L, IV_R, 'Runs on all Brocade FC switches (G630, G720, G730, X7 director platforms)')))
    lines.append(R(bMid(IV_L, IV_R, 'Core services: FCNS (name server), FCSM, zone management, ISL trunking')))
    lines.append(R(bMid(IV_L, IV_R, 'Management interfaces: CLI (SSH), REST API (FOS 8.2+), SANnav GUI integration')))
    lines.append(R(bMid(IV_L, IV_R, 'Fabric-wide config distribution: zone DB, fabric parameters, principal switch election')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Core OS services -> fabric-level functions -> management and integration layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FC Services'), bMid(B2_L, B2_R, 'Fabric Layer'), bMid(B3_L, B3_R, 'Management'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FCNS name server'), bMid(B2_L, B2_R, 'Zone DB sync'), bMid(B3_L, B3_R, 'CLI via SSH'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port login (FLOGI)'), bMid(B2_L, B2_R, 'ISL trunking'), bMid(B3_L, B3_R, 'REST API'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FC routing (FSPF)'), bMid(B2_L, B2_R, 'Principal switch'), bMid(B3_L, B3_R, 'SANnav GUI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FCSM security'), bMid(B2_L, B2_R, 'Fabric params'), bMid(B3_L, B3_R, 'SNMP/syslog'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RAS/diagnostics'), bMid(B2_L, B2_R, 'Domain ID mgmt'), bMid(B3_L, B3_R, 'LDAP auth'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Zone changes replicated across fabric; principal switch coordinates domain IDs'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Component', 'Role', 'Protocol', 'Version', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['FCNS', 'Name server', 'FC-GS', 'FOS 6+', 'Per-fabric DB'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['FSPF', 'FC routing', 'FC-SW', 'FOS 6+', 'Least-cost path'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['REST API', 'Mgmt interface', 'HTTPS', 'FOS 8.2+', 'JSON/XML'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Brocade G630/G720/G730 switches · X7-8/X7-4 directors · FC SFP optics · ISL cables'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Fabric OS      = Brocade proprietary OS running on all Brocade FC switch hardware'))
    lines.append(txt_row('  FCNS           = Fibre Channel Name Server; maps WWN to N_Port ID within the fabric'))
    lines.append(txt_row('  FSPF           = Fabric Shortest Path First; FC link-state routing protocol'))
    lines.append(txt_row('  FLOGI          = Fabric Login; HBA registers with fabric and obtains FC address (FCID)'))
    lines.append(txt_row('  FCSM           = FC Security Manager; enforces DH-CHAP switch authentication'))
    lines.append(txt_row('  Zone DB        = Fabric-wide zone configuration replicated to all switches in fabric'))
    lines.append(txt_row('  ISL trunk      = Multiple ISLs bundled for bandwidth aggregation between switches'))
    lines.append(txt_row('  Principal switch = Elected switch managing domain ID assignments for the fabric'))
    lines.append(txt_row('  Domain ID      = Unique numeric identifier for each switch in the fabric (1-239)'))
    lines.append(txt_row('  REST API       = FOS 8.2+ HTTP management interface; JSON/XML payloads over HTTPS'))
    lines.append(txt_row('  MAPS           = Monitoring and Alerting Policy Suite; FOS threshold alert engine'))
    lines.append(txt_row('  portcfg        = FOS CLI command to configure port speed, mode, and behaviour'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-arch',
    'docs/san/brocade/fabric-os/architecture/index.md',
    'Brocade FOS Architecture — OS layers, fabric services, hardware abstraction, data plane',
)
def brocade_fabric_os_arch():
    """Brocade FOS Architecture — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade Fabric OS — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FOS architecture: layered OS on embedded Linux with FC ASIC hardware abstraction')))
    lines.append(R(bMid(IV_L, IV_R, 'Data plane: FC frames switched in ASIC at line rate; no CPU involvement per frame')))
    lines.append(R(bMid(IV_L, IV_R, 'Control plane: FSPF routing, FCNS updates, zone DB distribution across fabric')))
    lines.append(R(bMid(IV_L, IV_R, 'Management plane: CLI daemon, REST server, SNMP agent, syslog forwarder')))
    lines.append(R(bMid(IV_L, IV_R, 'HA on directors: CP blade active/standby; failover <10 s non-disruptive')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Hardware (ASIC) -> FOS kernel/drivers -> fabric services -> management interfaces'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HW / ASIC'), bMid(B2_L, B2_R, 'Fabric Services'), bMid(B3_L, B3_R, 'Management'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FC frame switch'), bMid(B2_L, B2_R, 'FCNS/FSPF'), bMid(B3_L, B3_R, 'CLI (SSH)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SFP PHY layer'), bMid(B2_L, B2_R, 'Zone DB dist'), bMid(B3_L, B3_R, 'REST API'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port buffers'), bMid(B2_L, B2_R, 'Domain ID mgmt'), bMid(B3_L, B3_R, 'SNMP agent'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CP blade (HA)'), bMid(B2_L, B2_R, 'FCSM security'), bMid(B3_L, B3_R, 'Syslog fwd'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RAS sensors'), bMid(B2_L, B2_R, 'MAPS alerting'), bMid(B3_L, B3_R, 'SANnav link'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  CP blade failover is non-disruptive; FC frame forwarding continues during switchover'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Component', 'Function', 'Plane', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['HW', 'FC ASIC', 'Frame switching', 'Data', 'Line-rate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Kernel', 'FOS Linux', 'Driver/OS', 'Control', 'Embedded'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Services', 'FCNS/FSPF', 'Fabric ctrl', 'Control', 'Distributed'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: FC ASIC chips · CP/line blades on X7 directors · SFP optics · RAS sensors'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  FC ASIC        = Custom silicon switching FC frames at line rate with no CPU overhead'))
    lines.append(txt_row('  CP blade       = Control Processor blade on X7 directors; runs FOS management plane'))
    lines.append(txt_row('  Data plane     = FC frame forwarding in hardware; unaffected by control plane events'))
    lines.append(txt_row('  Control plane  = FSPF routing, FCNS updates, zone DB sync; CPU-managed services'))
    lines.append(txt_row('  FSPF           = Fabric Shortest Path First; computes optimal ISL paths'))
    lines.append(txt_row('  RAS sensors    = Reliability/Availability/Serviceability sensors for temp, fan, PSU'))
    lines.append(txt_row('  HA failover    = CP blade switchover; non-disruptive to data-plane traffic'))
    lines.append(txt_row('  Buffer credits = Per-port FC flow control mechanism; prevents frame loss on congested links'))
    lines.append(txt_row('  MAPS           = Monitoring and Alerting Policy Suite; threshold-based alerting engine'))
    lines.append(txt_row('  SFP PHY        = Physical layer transceiver; digital diagnostics accessible via FOS CLI'))
    lines.append(txt_row('  FOS Linux      = Embedded Linux kernel underpinning FabricOS user-space services'))
    lines.append(txt_row('  Zone DB dist   = Zone configuration replicated from principal switch to all fabric switches'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-arch-how',
    'docs/san/brocade/fabric-os/architecture/how-it-works/index.md',
    'FOS How It Works — fabric init, FLOGI, zone enforcement, frame routing, ISL trunking',
)
def brocade_fabric_os_arch_how():
    """Brocade FOS How It Works — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade Fabric OS — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FOS operational flow: fabric init, device login, zone enforcement, frame routing')))
    lines.append(R(bMid(IV_L, IV_R, 'Fabric init: switches exchange E_Port BRCDs, elect principal switch, assign domain IDs')))
    lines.append(R(bMid(IV_L, IV_R, 'Device login: HBA sends FLOGI, fabric assigns FCID, FCNS records WWN-to-FCID mapping')))
    lines.append(R(bMid(IV_L, IV_R, 'Zone enforcement: each frame checked against active zone set at ingress port ASIC')))
    lines.append(R(bMid(IV_L, IV_R, 'Frame routing: FSPF computes least-cost path; ISL trunk distributes load across links')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Fabric init -> device login (FLOGI/PLOGI) -> zone check -> FSPF routing -> delivery'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fabric Init'), bMid(B2_L, B2_R, 'Device Login'), bMid(B3_L, B3_R, 'Frame Routing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'E_Port detect'), bMid(B2_L, B2_R, 'FLOGI from HBA'), bMid(B3_L, B3_R, 'FSPF lookup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Principal elect'), bMid(B2_L, B2_R, 'FCID assigned'), bMid(B3_L, B3_R, 'ISL selection'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Domain ID assign'), bMid(B2_L, B2_R, 'FCNS register'), bMid(B3_L, B3_R, 'Zone check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Zone DB push'), bMid(B2_L, B2_R, 'PLOGI/PRLI'), bMid(B3_L, B3_R, 'Credit flow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fabric stable'), bMid(B2_L, B2_R, 'I/O begins'), bMid(B3_L, B3_R, 'Error detect'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Zone enforcement happens in ASIC at ingress; denied frames dropped before routing'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Phase', 'Event', 'Initiator', 'Result', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Init', 'BRCD exchange', 'Switches', 'Fabric formed', 'ISL up'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Login', 'FLOGI', 'HBA', 'FCID assigned', 'FCNS updated'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Routing', 'FSPF calc', 'FOS', 'Path selected', 'ISL trunk'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: HBA in server -> FC cable -> switch port -> ISL -> storage target port'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  FLOGI          = Fabric Login; first FC login HBA performs to join the fabric'))
    lines.append(txt_row('  FCID           = Fabric Controller ID; 24-bit address assigned to device by fabric'))
    lines.append(txt_row('  PLOGI          = Port Login; HBA-to-target login establishing parameters for I/O'))
    lines.append(txt_row('  PRLI           = Process Login; FCP/NVMe service parameters negotiated after PLOGI'))
    lines.append(txt_row('  E_Port         = Expansion port; ISL port connecting two FC switches'))
    lines.append(txt_row('  Principal switch = Switch elected to manage domain IDs; owns zone DB distribution'))
    lines.append(txt_row('  Domain ID      = Unique 8-bit number per switch in a fabric (1-239 valid range)'))
    lines.append(txt_row('  FSPF           = Fabric Shortest Path First; link-state protocol for optimal routing'))
    lines.append(txt_row('  ISL trunk      = Multiple ISL links aggregated; FSPF load-balances frames across them'))
    lines.append(txt_row('  Zone check     = ASIC validates source/destination WWN pair against active zone set'))
    lines.append(txt_row('  Buffer credit  = Per-link flow control token; receiver grants credit to allow transmission'))
    lines.append(txt_row('  BRCD exchange  = Brocade-specific capability exchange over E_Port during fabric init'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-arch-int',
    'docs/san/brocade/fabric-os/architecture/integrations/index.md',
    'FOS Integrations — SANnav, REST API, SNMP, syslog, LDAP, Ansible, vCenter plugin',
)
def brocade_fabric_os_arch_int():
    """Brocade FOS Integrations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade Fabric OS — Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FOS integrates with management tools, monitoring platforms, and automation frameworks')))
    lines.append(R(bMid(IV_L, IV_R, 'SANnav: primary GUI management via SSH + REST API; fabric discovery and monitoring')))
    lines.append(R(bMid(IV_L, IV_R, 'SNMP v3: NMS integration for trap forwarding; Brocade MIBs cover port/fabric OIDs')))
    lines.append(R(bMid(IV_L, IV_R, 'LDAP/AD: centralised authentication; role mapping via group membership')))
    lines.append(R(bMid(IV_L, IV_R, 'REST API: JSON-based programmatic management for Ansible and CI/CD pipelines')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Management tools -> monitoring/alerting -> identity -> automation integrations'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Management'), bMid(B2_L, B2_R, 'Monitoring'), bMid(B3_L, B3_R, 'Automation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SANnav GUI'), bMid(B2_L, B2_R, 'SNMP v3 traps'), bMid(B3_L, B3_R, 'REST API'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSH CLI'), bMid(B2_L, B2_R, 'Syslog (SIEM)'), bMid(B3_L, B3_R, 'Ansible modules'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP/AD auth'), bMid(B2_L, B2_R, 'MAPS alerts'), bMid(B3_L, B3_R, 'Python scripts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter plugin'), bMid(B2_L, B2_R, 'Email alerts'), bMid(B3_L, B3_R, 'CI/CD pipeline'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NTP sync'), bMid(B2_L, B2_R, 'Dashboard'), bMid(B3_L, B3_R, 'Terraform'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  All integrations use out-of-band Ethernet management; FC data plane unaffected'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Integration', 'Protocol', 'Auth', 'Use case', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SANnav', 'SSH+REST', 'Password/key', 'Full mgmt', 'Primary tool'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SNMP v3', 'UDP 162', 'AuthPriv', 'NMS traps', 'Brocade MIBs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['REST API', 'HTTPS 443', 'Session token', 'Automation', 'FOS 8.2+'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: mgmt Ethernet port on each switch · OOB management network · NTP server'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SANnav         = Brocade SAN management GUI; primary operational tool for FOS switches'))
    lines.append(txt_row('  REST API       = HTTPS-based FOS management API; returns JSON; requires FOS 8.2+'))
    lines.append(txt_row('  SNMP v3        = SNMPv3 with authentication (SHA) and encryption (AES) for secure traps'))
    lines.append(txt_row('  Brocade MIBs   = SNMP MIB files defining Brocade-specific OIDs for port/fabric telemetry'))
    lines.append(txt_row('  LDAP/AD        = Switch authenticates admin users against Active Directory'))
    lines.append(txt_row('  MAPS           = Monitoring and Alerting Policy Suite; configures thresholds and actions'))
    lines.append(txt_row('  Syslog         = Switch event log forwarded to SIEM (Splunk, QRadar) for correlation'))
    lines.append(txt_row('  Ansible module = brocade_fibrechannel Ansible collection for zone/port automation'))
    lines.append(txt_row('  vCenter plugin = Shows FC path visibility from VM HBA through fabric to storage'))
    lines.append(txt_row('  Session token  = REST API Bearer token returned on login; used in subsequent API calls'))
    lines.append(txt_row('  NTP sync       = Switch clock synchronised to NTP for accurate log timestamps'))
    lines.append(txt_row('  OOB mgmt       = Out-of-band management via dedicated Ethernet port; separate from FC'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-arch-design',
    'docs/san/brocade/fabric-os/architecture/design-standards/index.md',
    'FOS Design Standards — fabric topology, domain IDs, ISL design, zone naming, HA',
)
def brocade_fabric_os_arch_design():
    """Brocade FOS Design Standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade Fabric OS — Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FOS design standards for production SAN: topology, naming, ISL sizing, HA, security')))
    lines.append(R(bMid(IV_L, IV_R, 'Topology: dual-fabric A/B design; no single-fabric dependency for storage access')))
    lines.append(R(bMid(IV_L, IV_R, 'Domain IDs: statically assigned; Fabric A starts at 1, Fabric B starts at 100')))
    lines.append(R(bMid(IV_L, IV_R, 'ISL sizing: minimum 2 ISLs per switch pair; trunk for bandwidth and redundancy')))
    lines.append(R(bMid(IV_L, IV_R, 'Zone naming: host_alias_storage_alias format; no generic zone names in production')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Topology standards -> naming conventions -> ISL design -> HA and redundancy rules'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Topology'), bMid(B2_L, B2_R, 'Naming / IDs'), bMid(B3_L, B3_R, 'HA / ISL'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dual fabric A/B'), bMid(B2_L, B2_R, 'Static domain IDs'), bMid(B3_L, B3_R, 'Min 2 ISLs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Core-edge design'), bMid(B2_L, B2_R, 'Zone naming std'), bMid(B3_L, B3_R, 'ISL trunking'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No single fabric'), bMid(B2_L, B2_R, 'Alias per HBA'), bMid(B3_L, B3_R, 'Director core'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Separate VSANs'), bMid(B2_L, B2_R, 'Config naming'), bMid(B3_L, B3_R, 'Redundant PSU'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Buffer planning'), bMid(B2_L, B2_R, 'FW rev tracking'), bMid(B3_L, B3_R, 'OOB mgmt path'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Core switches (directors) connect to all edge switches; no edge-to-edge ISLs'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Standard', 'Rule', 'Rationale', 'Tool', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Dual fabric', 'A+B always', 'HA for hosts', 'Multi-pathing', 'MPIO required'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Domain ID', 'Static assign', 'Predictability', 'portcfg', 'A=1-99, B=100+'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ISL trunk', 'Min 2 per pair', 'Redundancy', 'SANnav/CLI', 'Same speed ISLs'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: dual directors at core · edge switches per row · redundant ISL paths'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Dual fabric    = Two independent FC fabrics (A and B); each host has one HBA in each'))
    lines.append(txt_row('  Core-edge      = Directors at core; fixed-port switches at edge; no edge-to-edge ISLs'))
    lines.append(txt_row('  Domain ID      = Statically assigned switch identifier; dynamic assignment risks reconfiguring'))
    lines.append(txt_row('  ISL trunk      = Bundled ISLs between same switch pair for bandwidth and redundancy'))
    lines.append(txt_row('  Zone naming    = Standard: srvname_hba0_arrayname_sp0; enables instant identification'))
    lines.append(txt_row('  Alias          = WWN alias per HBA port; one alias per physical port, not per LUN'))
    lines.append(txt_row('  Buffer credit  = Must be planned for long-distance ISLs; insufficient credits cause congestion'))
    lines.append(txt_row('  MPIO           = Multi-path I/O on host; uses both fabric A and B paths for redundancy'))
    lines.append(txt_row('  OOB mgmt       = Out-of-band Ethernet management must be redundant and always accessible'))
    lines.append(txt_row('  PSU redundancy = Each switch/director must have redundant power supplies from separate PDUs'))
    lines.append(txt_row('  FW tracking    = Firmware version matrix maintained; all switches in fabric same minor version'))
    lines.append(txt_row('  Config naming  = Zone config names include date/ticket reference for auditability'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-ops-procedures',
    'docs/san/brocade/fabric-os/operations/procedures/index.md',
    'FOS Operations Procedures — zone changes, port management, firmware upgrade, backup',
)
def brocade_fabric_os_ops_procedures():
    """Brocade FOS Operations Procedures — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade Fabric OS — Operations Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Standard FOS operational procedures for day-to-day SAN administration')))
    lines.append(R(bMid(IV_L, IV_R, 'Zone change: create alias -> create zone -> add to zone set -> cfgenable')))
    lines.append(R(bMid(IV_L, IV_R, 'Port management: portdisable/portenable; portcfgpersistentdisable for permanent off')))
    lines.append(R(bMid(IV_L, IV_R, 'Firmware upgrade: firmwaredownload -s; verify with firmwareshow after reboot')))
    lines.append(R(bMid(IV_L, IV_R, 'Config backup: configupload to save switch config to SCP/FTP server')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Pre-checks -> change procedure -> post-checks -> documentation and rollback plan'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Zone Mgmt'), bMid(B2_L, B2_R, 'Port Mgmt'), bMid(B3_L, B3_R, 'Lifecycle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'alicreate'), bMid(B2_L, B2_R, 'portdisable'), bMid(B3_L, B3_R, 'firmwaredownload'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'zonecreate'), bMid(B2_L, B2_R, 'portenable'), bMid(B3_L, B3_R, 'configupload'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'cfgadd'), bMid(B2_L, B2_R, 'portcfgspeed'), bMid(B3_L, B3_R, 'configdownload'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'cfgenable'), bMid(B2_L, B2_R, 'portcfgmode'), bMid(B3_L, B3_R, 'supportshow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'cfgsave'), bMid(B2_L, B2_R, 'portshow'), bMid(B3_L, B3_R, 'firmwareshow'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Always cfgsave after cfgenable; changes without cfgsave lost on switch reboot'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Procedure', 'CLI command', 'Impact', 'Rollback', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Zone add', 'cfgenable', 'Fabric-wide', 'cfgenable old', 'CAB required'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Port disable', 'portdisable', 'Port only', 'portenable', 'Log first'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['FW upgrade', 'firmwaredownload', 'Switch reboot', 'Prior version', 'NDU for HA'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SSH to switch mgmt IP · SCP server for config/firmware files'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  alicreate      = FOS CLI command to create a WWN alias for a host or storage port'))
    lines.append(txt_row('  zonecreate     = Creates a new zone with specified member aliases or WWNs'))
    lines.append(txt_row('  cfgadd         = Adds a zone to an existing zone configuration'))
    lines.append(txt_row('  cfgenable      = Activates the named zone configuration across the entire fabric'))
    lines.append(txt_row('  cfgsave        = Saves the zone database to non-volatile memory on all switches'))
    lines.append(txt_row('  portdisable    = Administratively disables an FC port (state: No_Light or D_Port)'))
    lines.append(txt_row('  portcfgspeed   = Sets port speed (auto, 8G, 16G, 32G, 64G)'))
    lines.append(txt_row('  firmwaredownload = Downloads FOS image from SCP/FTP and reboots switch to activate'))
    lines.append(txt_row('  configupload   = Uploads running switch config to SCP/FTP for backup'))
    lines.append(txt_row('  configdownload = Restores switch config from previously uploaded backup file'))
    lines.append(txt_row('  supportshow    = Collects full diagnostic data bundle for TAC support'))
    lines.append(txt_row('  NDU            = Non-Disruptive Upgrade; HA chassis upgrades one blade at a time'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-ops-backup',
    'docs/san/brocade/fabric-os/operations/backup-restore/index.md',
    'FOS Backup and Restore — configupload, configdownload, zone DB backup, disaster recovery',
)
def brocade_fabric_os_ops_backup():
    """Brocade FOS Backup and Restore — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade Fabric OS — Backup and Restore'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FOS backup and restore: switch config, zone DB, and full switch replacement recovery')))
    lines.append(R(bMid(IV_L, IV_R, 'configupload: saves switch config (not zone DB) to SCP/FTP; schedule weekly')))
    lines.append(R(bMid(IV_L, IV_R, 'Zone DB backup: cfgsave persists to flash; also export zone DB via SANnav')))
    lines.append(R(bMid(IV_L, IV_R, 'Switch replacement: configdownload restores config; re-cable and verify fabric')))
    lines.append(R(bMid(IV_L, IV_R, 'Director blade: hot-swap with NDU; config on CP blade survives blade failure')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Schedule backup -> verify backup file -> test restore -> store off-site copy securely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Config Backup'), bMid(B2_L, B2_R, 'Zone DB'), bMid(B3_L, B3_R, 'Recovery'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'configupload'), bMid(B2_L, B2_R, 'cfgsave'), bMid(B3_L, B3_R, 'configdownload'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCP/FTP target'), bMid(B2_L, B2_R, 'SANnav export'), bMid(B3_L, B3_R, 'Switch replace'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Weekly schedule'), bMid(B2_L, B2_R, 'Before changes'), bMid(B3_L, B3_R, 'Re-cable fabric'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Version tagged'), bMid(B2_L, B2_R, 'Zone DB export'), bMid(B3_L, B3_R, 'Verify zones'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Off-site copy'), bMid(B2_L, B2_R, 'Audit history'), bMid(B3_L, B3_R, 'Test restore'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Test restore quarterly; zone DB and config backup are independent procedures'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Backup type', 'Command', 'Frequency', 'Target', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Switch config', 'configupload', 'Weekly', 'SCP server', 'All settings'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Zone DB', 'cfgsave+export', 'Pre-change', 'SANnav/file', 'Fabric-wide'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Full restore', 'configdownload', 'On failure', 'New switch', 'Re-cable needed'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCP/FTP backup server · offline config archive · replacement switch spare'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  configupload   = FOS CLI: uploads switch config to SCP/FTP; includes port/security settings'))
    lines.append(txt_row('  configdownload = FOS CLI: restores switch config from remote file; triggers partial reboot'))
    lines.append(txt_row('  cfgsave        = Persists zone DB to non-volatile flash; must run after every zone change'))
    lines.append(txt_row('  Zone DB export = SANnav can export zone config as text file; keep with config backup'))
    lines.append(txt_row('  Switch replace = Install new switch, configdownload, re-cable ISLs and host/storage ports'))
    lines.append(txt_row('  NDU            = Non-Disruptive Upgrade; director blades hot-swapped with no fabric impact'))
    lines.append(txt_row('  Spare switch   = Pre-configured standby switch for rapid replacement; test restore regularly'))
    lines.append(txt_row('  SCP server     = Secure Copy Protocol server; preferred over FTP for encrypted transfer'))
    lines.append(txt_row('  Off-site copy  = Backup files replicated to secondary site or object storage for DR'))
    lines.append(txt_row('  Audit history  = SANnav logs all zone config changes; export as evidence for compliance'))
    lines.append(txt_row('  Version tag    = Include FOS version and date in backup filename for traceability'))
    lines.append(txt_row('  Test restore   = Quarterly restore test on lab/spare switch to validate backup integrity'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-ops-health',
    'docs/san/brocade/fabric-os/operations/health-checks/index.md',
    'FOS Health Checks — switchshow, porterrshow, SFP diagnostics, MAPS alerts, fabric health',
)
def brocade_fabric_os_ops_health():
    """Brocade FOS Health Checks — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade Fabric OS — Health Checks'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Daily FOS health checks: switch state, port errors, SFP optics, MAPS alerts')))
    lines.append(R(bMid(IV_L, IV_R, 'switchshow: verify all ports Online; check switch health state (Healthy)')))
    lines.append(R(bMid(IV_L, IV_R, 'porterrshow: review CRC, LOS, LOSync counters; nonzero values require investigation')))
    lines.append(R(bMid(IV_L, IV_R, 'sfpshow: review Tx/Rx power dBm; compare against SFP vendor thresholds')))
    lines.append(R(bMid(IV_L, IV_R, 'MAPS dashboard: check active alert policy; review mapsDb for rule violations')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Switch state -> port errors -> SFP optics -> MAPS alerts -> fabric topology review'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Switch Health'), bMid(B2_L, B2_R, 'Port Health'), bMid(B3_L, B3_R, 'SFP / Optics'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'switchshow'), bMid(B2_L, B2_R, 'porterrshow'), bMid(B3_L, B3_R, 'sfpshow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'switchstatusshow'), bMid(B2_L, B2_R, 'portstatsclear'), bMid(B3_L, B3_R, 'Tx power dBm'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MAPS dashboard'), bMid(B2_L, B2_R, 'CRC counter'), bMid(B3_L, B3_R, 'Rx power dBm'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fan/PSU status'), bMid(B2_L, B2_R, 'Loss of Signal'), bMid(B3_L, B3_R, 'Temperature'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'fabricshow'), bMid(B2_L, B2_R, 'Loss of Sync'), bMid(B3_L, B3_R, 'Vendor limits'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Clear error counters only after investigating and resolving the underlying cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Check', 'Command', 'Frequency', 'Threshold', 'Action'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Switch state', 'switchshow', 'Daily', 'All Online', 'Investigate faults'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Port errors', 'porterrshow', 'Daily', 'Zero CRC', 'Replace cable/SFP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SFP power', 'sfpshow', 'Weekly', 'Vendor range', 'Replace SFP'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: FC switches · SFP transceivers · ISL cables · console/mgmt access'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  switchshow     = Lists all ports with state (Online/Offline/Faulty) and connected device WWN'))
    lines.append(txt_row('  porterrshow    = Displays error counters per port: CRC, LOS, LOSync, ITW, Enc_in'))
    lines.append(txt_row('  portstatsclear = Resets error counters to zero; use only after resolving the issue'))
    lines.append(txt_row('  sfpshow        = Displays SFP diagnostics: Tx/Rx power, temperature, voltage'))
    lines.append(txt_row('  switchstatusshow = Summary health status of switch: Healthy, Marginal, or Down'))
    lines.append(txt_row('  fabricshow     = Lists all switches in fabric with domain IDs and WWNs'))
    lines.append(txt_row('  MAPS dashboard = SANnav MAPS view showing active policy and current rule violations'))
    lines.append(txt_row('  CRC error      = Cyclic Redundancy Check error; indicates corrupt FC frame; cable/SFP issue'))
    lines.append(txt_row('  Loss of Signal = LOS: no optical signal detected; SFP or cable failure'))
    lines.append(txt_row('  Loss of Sync   = LOSync: signal present but frame sync lost; speed mismatch or noise'))
    lines.append(txt_row('  Tx/Rx power    = SFP optical power in dBm; each SFP type has defined acceptable range'))
    lines.append(txt_row('  MAPS alert     = Automated rule-based alert when metric breaches configured threshold'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-ops-install',
    'docs/san/brocade/fabric-os/operations/install-upgrade/index.md',
    'FOS Install and Upgrade — firmwaredownload, NDU for directors, pre/post checks, rollback',
)
def brocade_fabric_os_ops_install():
    """Brocade FOS Install and Upgrade — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade Fabric OS — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FOS firmware upgrade: firmwaredownload command; NDU for HA directors')))
    lines.append(R(bMid(IV_L, IV_R, 'Pre-checks: switchshow all Online, no MAPS critical alerts, config backed up')))
    lines.append(R(bMid(IV_L, IV_R, 'Download: firmwaredownload -s <scp-server> <path>; switch reboots automatically')))
    lines.append(R(bMid(IV_L, IV_R, 'Director NDU: upgrades standby CP first, then failover; no fabric disruption')))
    lines.append(R(bMid(IV_L, IV_R, 'Post-checks: firmwareshow, switchshow, porterrshow; verify no new errors')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Pre-checks -> firmware stage -> upgrade trigger -> reboot -> post-verify -> sign-off'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-Checks'), bMid(B2_L, B2_R, 'Upgrade'), bMid(B3_L, B3_R, 'Post-Checks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'switchshow OK'), bMid(B2_L, B2_R, 'firmwaredownload'), bMid(B3_L, B3_R, 'firmwareshow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No MAPS alerts'), bMid(B2_L, B2_R, 'Stage firmware'), bMid(B3_L, B3_R, 'switchshow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Config backed up'), bMid(B2_L, B2_R, 'CP failover NDU'), bMid(B3_L, B3_R, 'porterrshow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Change ticket'), bMid(B2_L, B2_R, 'Auto-reboot'), bMid(B3_L, B3_R, 'fabricshow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Peer fabric OK'), bMid(B2_L, B2_R, 'Rollback option'), bMid(B3_L, B3_R, 'MAPS check'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Always upgrade one fabric at a time; never both A and B fabrics simultaneously'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Step', 'Action', 'Command', 'Expected', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Pre', 'Health check', 'switchshow', 'All Online', 'Per switch'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Upgrade', 'Download FW', 'firmwaredownload', 'Rebooting', 'NDU director'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Post', 'Verify version', 'firmwareshow', 'New version', 'Check errors'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCP server with FOS image · switch mgmt Ethernet · console for recovery'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  firmwaredownload = Downloads FOS image and reboots switch to activate new version'))
    lines.append(txt_row('  NDU            = Non-Disruptive Upgrade; director upgrades without disrupting FC traffic'))
    lines.append(txt_row('  firmwareshow   = Displays current and committed FOS version on each blade'))
    lines.append(txt_row('  Stage firmware = Download to flash before activating; allows verification before commit'))
    lines.append(txt_row('  CP failover    = Standby CP takes over; data plane continues; new standby then upgrades'))
    lines.append(txt_row('  Rollback       = firmwaredownload to prior version if new version has critical defects'))
    lines.append(txt_row('  Pre-checks     = Confirm fabric is healthy before maintenance; document baseline state'))
    lines.append(txt_row('  Change ticket  = All firmware upgrades require approved change management ticket'))
    lines.append(txt_row('  Peer fabric    = Verify peer fabric (B while upgrading A) is fully healthy first'))
    lines.append(txt_row('  Post-verify    = Check firmwareshow, switchshow, porterrshow, MAPS after upgrade'))
    lines.append(txt_row('  SCP image      = FOS firmware .zip downloaded from Broadcom support portal'))
    lines.append(txt_row('  One fabric     = Upgrade one fabric completely before touching the peer fabric'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade-fabric-os-ops-scripts',
    'docs/san/brocade/fabric-os/operations/scripts/index.md',
    'FOS Scripts — automation scripts for zone management, health checks, bulk port operations',
)
def brocade_fabric_os_ops_scripts():
    """Brocade FOS Scripts — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Brocade Fabric OS — Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FOS automation: Python/Ansible scripts using REST API and SSH for bulk operations')))
    lines.append(R(bMid(IV_L, IV_R, 'Zone automation: Ansible brocade_fibrechannel modules for alias/zone/cfgenable')))
    lines.append(R(bMid(IV_L, IV_R, 'Health scripts: SSH-based porterrshow/sfpshow collection across all switches')))
    lines.append(R(bMid(IV_L, IV_R, 'REST API scripts: Python requests; authenticate, query port stats, parse JSON')))
    lines.append(R(bMid(IV_L, IV_R, 'Bulk port ops: loop portdisable/portenable via paramiko SSH for mass changes')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  REST API / SSH access -> script logic -> output parsing -> action or reporting'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Zone Scripts'), bMid(B2_L, B2_R, 'Health Scripts'), bMid(B3_L, B3_R, 'REST Scripts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Ansible playbook'), bMid(B2_L, B2_R, 'SSH paramiko'), bMid(B3_L, B3_R, 'Python requests'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'alicreate batch'), bMid(B2_L, B2_R, 'porterrshow'), bMid(B3_L, B3_R, 'Token auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'zonecreate batch'), bMid(B2_L, B2_R, 'sfpshow collect'), bMid(B3_L, B3_R, 'Port stats GET'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'cfgenable auto'), bMid(B2_L, B2_R, 'Report generate'), bMid(B3_L, B3_R, 'JSON parse'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Idempotent runs'), bMid(B2_L, B2_R, 'Alert on errors'), bMid(B3_L, B3_R, 'Alert trigger'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  All scripts run from jump host; never from fabric switches directly'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Script type', 'Tool', 'Auth', 'Output', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Zone mgmt', 'Ansible', 'SSH key', 'Zone change', 'Idempotent'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Health check', 'Python+SSH', 'Password/key', 'CSV report', 'All switches'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['REST query', 'Python', 'Bearer token', 'JSON/CSV', 'FOS 8.2+'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: jump host -> mgmt network -> switch mgmt Ethernet ports'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Ansible module = brocade_fibrechannel collection; idempotent zone/alias/cfgenable tasks'))
    lines.append(txt_row('  paramiko       = Python SSH library; executes FOS CLI commands programmatically'))
    lines.append(txt_row('  Bearer token   = REST API authentication token; obtained via POST /rest/v1/login'))
    lines.append(txt_row('  Idempotent     = Script produces same result whether run once or multiple times'))
    lines.append(txt_row('  Jump host      = Dedicated management host with access to switch mgmt network'))
    lines.append(txt_row('  porterrshow    = FOS CLI command parsed by health scripts to detect port errors'))
    lines.append(txt_row('  sfpshow        = FOS CLI command reporting SFP optical power values per port'))
    lines.append(txt_row('  REST GET       = Read-only REST API call; fetches port stats, switch info, zone config'))
    lines.append(txt_row('  CSV report     = Health script output format; imported into Excel or monitoring tool'))
    lines.append(txt_row('  cfgenable auto = Ansible task to activate zone set after alias and zone creation'))
    lines.append(txt_row('  Batch alias    = Create multiple aliases from CSV input file in single script run'))
    lines.append(txt_row('  Alert trigger  = Script sends email or webhook when health metric exceeds threshold'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-fabric-os-ops-cli', 'docs/san/brocade/fabric-os/operations/cli-reference/index.md', 'Brocade Fabric OS CLI Reference')
def _brocade_fabric_os_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade Fabric OS — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('Fabric OS CLI commands: fabric management, port control, zoning, diagnostics, firmware.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric & Switch Commands'), bMid(L2, R2, 'Port & ISL Commands'))))
    lines.append(R(merge(bMid(L1, R1, 'switchshow: port + fabric state'), bMid(L2, R2, 'portshow <slot/port>'))))
    lines.append(R(merge(bMid(L1, R1, 'fabricshow: fabric topology'), bMid(L2, R2, 'portenable/portdisable'))))
    lines.append(R(merge(bMid(L1, R1, 'nsshow: name server logins'), bMid(L2, R2, 'islshow: ISL utilisation'))))
    lines.append(R(merge(bMid(L1, R1, 'switchstatusshow: overall health'), bMid(L2, R2, 'portcfgspeed: set port speed'))))
    lines.append(R(merge(bMid(L1, R1, 'chassisshow: blade inventory'), bMid(L2, R2, 'portloginshow: login list'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('switchshow is the first command for any Fabric OS health check; nsshow shows device logins.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Zoning & Security Commands'), bMid(L2, R2, 'Firmware & Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'cfgshow: display zone config'), bMid(L2, R2, 'firmwareshow: version check'))))
    lines.append(R(merge(bMid(L1, R1, 'zonecreate/zonedelete'), bMid(L2, R2, 'firmwaredownload: upgrade FOS'))))
    lines.append(R(merge(bMid(L1, R1, 'cfgsave + cfgenable <cfg>'), bMid(L2, R2, 'porttest: run loopback test'))))
    lines.append(R(merge(bMid(L1, R1, 'secpolicyadd/secpolicydel'), bMid(L2, R2, 'diagstatus: diagnostic state'))))
    lines.append(R(merge(bMid(L1, R1, 'authutil: FCAP / DH-CHAP'), bMid(L2, R2, 'supportshow: full tech bundle'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade FC switch chassis · blades · SFP transceivers · FC host bus adapters'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('switchshow      = primary CLI for port status, fabric domain ID, and zoning state'))
    lines.append(txt_row('nsshow          = Name Server show; lists all devices logged into fabric on local switch'))
    lines.append(txt_row('fabricshow      = displays fabric principal switch, all domain IDs, and topology'))
    lines.append(txt_row('cfgshow         = zone config show; lists all zones, aliases, and active config'))
    lines.append(txt_row('cfgsave         = saves zone database changes to flash; required before cfgenable'))
    lines.append(txt_row('cfgenable       = activates named zone configuration across the fabric'))
    lines.append(txt_row('islshow         = Inter-Switch Link show; displays ISL bandwidth utilisation per port'))
    lines.append(txt_row('firmwaredownload= downloads and installs new Fabric OS version via non-disruptive HA'))
    lines.append(txt_row('supportshow     = generates full diagnostic bundle; upload to Broadcom TAC'))
    lines.append(txt_row('porttest        = runs loopback diagnostic on a port; requires port offline'))
    lines.append(txt_row('DH-CHAP         = Diffie-Hellman Challenge Handshake Auth Protocol; FC switch auth'))
    lines.append(txt_row('FCAP            = Fibre Channel Authentication Protocol; cert-based switch auth'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-fabric-os-sec-access', 'docs/san/brocade/fabric-os/security/access-control/index.md', 'Brocade Fabric OS Access Control')
def _brocade_fabric_os_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade Fabric OS — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('Access control: RBAC roles, login accounts, TACACS+/RADIUS, SCC/DCC zoning policies.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'User Accounts & RBAC'), bMid(L2, R2, 'Remote Auth (TACACS+/RADIUS)'))))
    lines.append(R(merge(bMid(L1, R1, 'Built-in roles: admin/user/ops'), bMid(L2, R2, 'TACACS+ server primary/back'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom roles via roleConfig'), bMid(L2, R2, 'RADIUS: fallback to local'))))
    lines.append(R(merge(bMid(L1, R1, 'userconfig: create/modify user'), bMid(L2, R2, 'aaaconfig: set auth order'))))
    lines.append(R(merge(bMid(L1, R1, 'Account lockout: 3 attempts'), bMid(L2, R2, 'acp filter: ACL on switch'))))
    lines.append(R(merge(bMid(L1, R1, 'Virtual Fabric RBAC per chassis'), bMid(L2, R2, 'Audit log for all CLI cmds'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Local RBAC and remote TACACS+/RADIUS enforce who can run CLI commands on the switch.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SCC / DCC Policies'), bMid(L2, R2, 'Management Access Control'))))
    lines.append(R(merge(bMid(L1, R1, 'SCC: switch connection control'), bMid(L2, R2, 'SSH only: no Telnet/FTP'))))
    lines.append(R(merge(bMid(L1, R1, 'DCC: device connection control'), bMid(L2, R2, 'HTTPS for Web GUI / API'))))
    lines.append(R(merge(bMid(L1, R1, 'SCC: limit which switches join'), bMid(L2, R2, 'IP filter: src IP whitelist'))))
    lines.append(R(merge(bMid(L1, R1, 'DCC: bind ports to WWN list'), bMid(L2, R2, 'Out-of-band mgmt: eth port'))))
    lines.append(R(merge(bMid(L1, R1, 'secpolicyadd to build policy'), bMid(L2, R2, 'SNMPv3 only: disable v1/v2'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade switch chassis · management Ethernet port · TACACS+ / RADIUS server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC           = Role-Based Access Control; Fabric OS roles control CLI permissions'))
    lines.append(txt_row('roleConfig     = CLI command to create/modify custom RBAC role definitions'))
    lines.append(txt_row('userconfig     = Fabric OS CLI to create, modify, or delete local user accounts'))
    lines.append(txt_row('TACACS+        = Terminal Access Controller Access Control System; centralized CLI auth'))
    lines.append(txt_row('aaaconfig      = CLI to set authentication order (local, TACACS+, RADIUS)'))
    lines.append(txt_row('SCC            = Switch Connection Control policy; restricts which switches join fabric'))
    lines.append(txt_row('DCC            = Device Connection Control policy; binds host WWNs to specific ports'))
    lines.append(txt_row('secpolicyadd   = CLI to add members to SCC/DCC security policies'))
    lines.append(txt_row('Virtual Fabric = logical switch partitioning on Brocade directors; per-VF RBAC'))
    lines.append(txt_row('acp            = Access Control Policy; IP-level ACL for switch management access'))
    lines.append(txt_row('SNMPv3         = SNMP version 3; provides authentication and encryption for SNMP'))
    lines.append(txt_row('WWN            = World Wide Name; 64-bit FC identifier for HBAs and switch ports'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-fabric-os-sec-auth', 'docs/san/brocade/fabric-os/security/authentication/index.md', 'Brocade Fabric OS Authentication')
def _brocade_fabric_os_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade Fabric OS — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('Authentication: DH-CHAP for switch-to-switch, FCAP, TACACS+, and local login methods.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Switch-to-Switch Auth (DH-CHAP)'), bMid(L2, R2, 'User Login Authentication'))))
    lines.append(R(merge(bMid(L1, R1, 'DH-CHAP: HMAC-SHA256 exchange'), bMid(L2, R2, 'SSH key-based admin login'))))
    lines.append(R(merge(bMid(L1, R1, 'FCAP: cert-based ISL auth'), bMid(L2, R2, 'TACACS+: privilege level map'))))
    lines.append(R(merge(bMid(L1, R1, 'authutil --set -a dhchap'), bMid(L2, R2, 'RADIUS: challenge-response'))))
    lines.append(R(merge(bMid(L1, R1, 'Group shared secret per fabric'), bMid(L2, R2, 'Local: password + lockout'))))
    lines.append(R(merge(bMid(L1, R1, 'ISL formed only if auth passes'), bMid(L2, R2, 'passwdcfg: complexity rules'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('DH-CHAP authenticates switches before ISL formation; user auth via TACACS+ or local.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'PKI / Certificate Auth'), bMid(L2, R2, 'Audit & Session Control'))))
    lines.append(R(merge(bMid(L1, R1, 'FCAP: X.509 cert exchange'), bMid(L2, R2, 'audit log: all CLI commands'))))
    lines.append(R(merge(bMid(L1, R1, 'certutil: manage local certs'), bMid(L2, R2, 'Security event ID tracking'))))
    lines.append(R(merge(bMid(L1, R1, 'HTTPS cert bind to web GUI'), bMid(L2, R2, 'Session timeout: 30 min idle'))))
    lines.append(R(merge(bMid(L1, R1, 'CA-signed vs self-signed cert'), bMid(L2, R2, 'Concurrent sessions limited'))))
    lines.append(R(merge(bMid(L1, R1, 'Revocation: CRL check on auth'), bMid(L2, R2, 'syslog auth events to SIEM'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade FC switch · management Ethernet · TACACS+ server · PKI CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('DH-CHAP        = Diffie-Hellman CHAP; cryptographic switch-to-switch auth on ISL'))
    lines.append(txt_row('FCAP           = Fibre Channel Authentication Protocol; X.509 cert-based ISL auth'))
    lines.append(txt_row('authutil       = CLI to configure and test switch authentication (DH-CHAP/FCAP)'))
    lines.append(txt_row('ISL            = Inter-Switch Link; E_Port connection between two FC switches'))
    lines.append(txt_row('TACACS+        = centralised CLI auth server; maps privilege levels to Fabric OS roles'))
    lines.append(txt_row('passwdcfg      = password configuration CLI; sets complexity, expiry, lockout policy'))
    lines.append(txt_row('certutil       = Fabric OS CLI to import, export, and manage X.509 certificates'))
    lines.append(txt_row('HTTPS cert     = TLS certificate bound to management GUI; must be CA-signed in prod'))
    lines.append(txt_row('CRL            = Certificate Revocation List; checked during FCAP auth to block revoked'))
    lines.append(txt_row('Audit log      = tamper-evident log of all CLI sessions and commands with user/timestamp'))
    lines.append(txt_row('SSH key        = RSA/ECDSA key pair for passwordless admin SSH; stored in authorized_keys'))
    lines.append(txt_row('Session timeout= idle session termination; Fabric OS default 30 minutes inactivity'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-fabric-os-sec-enc', 'docs/san/brocade/fabric-os/security/encryption/index.md', 'Brocade Fabric OS Encryption')
def _brocade_fabric_os_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade Fabric OS — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('Fabric OS encryption: FC-SP for fabric security, management TLS, optional data-at-rest.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Management Plane Encryption'), bMid(L2, R2, 'Fabric Security (FC-SP)'))))
    lines.append(R(merge(bMid(L1, R1, 'SSH: encrypted CLI sessions'), bMid(L2, R2, 'FC-SP: ISL encryption option'))))
    lines.append(R(merge(bMid(L1, R1, 'HTTPS: TLS 1.2/1.3 for GUI'), bMid(L2, R2, 'DH-CHAP: auth + key exchange'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMPv3: AES-128 privacy'), bMid(L2, R2, 'Shared secret rotated per fabric'))))
    lines.append(R(merge(bMid(L1, R1, 'syslog: TLS encrypted forwarding'), bMid(L2, R2, 'FCAP: cert-based key exchange'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable Telnet/FTP/HTTP'), bMid(L2, R2, 'Per-port auth enforcement'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Management traffic encrypted via SSH/HTTPS; fabric traffic secured via FC-SP DH-CHAP.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Data-at-Rest (Hardware Enc)'), bMid(L2, R2, 'Key Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Brocade Encryption Switch (ES)'), bMid(L2, R2, 'KMIP: NetApp/Thales KMAX'))))
    lines.append(R(merge(bMid(L1, R1, 'FS8-18 blade encryption engine'), bMid(L2, R2, 'Master key in hardware HSM'))))
    lines.append(R(merge(bMid(L1, R1, 'LUN-level AES-256-XTS'), bMid(L2, R2, 'Key zeroisation on decom'))))
    lines.append(R(merge(bMid(L1, R1, 'Transparent to host and array'), bMid(L2, R2, 'Dual control: 2 admins required'))))
    lines.append(R(merge(bMid(L1, R1, 'Re-keying without data loss'), bMid(L2, R2, 'Audit: key usage events logged'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade FC switch / FS8-18 blade · HSM appliance · FC cables · storage array'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FC-SP           = Fibre Channel Security Protocol; optional ISL authentication/encryption'))
    lines.append(txt_row('DH-CHAP         = Diffie-Hellman CHAP; generates shared session key for FC-SP'))
    lines.append(txt_row('FS8-18          = Brocade encryption blade for DCX directors; LUN-level AES-256'))
    lines.append(txt_row('KMIP            = Key Management Interoperability Protocol; connects to external KMS'))
    lines.append(txt_row('AES-256-XTS     = AES in XEX-based Tweaked-codebook mode XTS; disk encryption standard'))
    lines.append(txt_row('SNMPv3 privacy  = AES-128 encryption for SNMP PDU payload; auth + privacy mode'))
    lines.append(txt_row('HSM             = Hardware Security Module; tamper-proof storage for encryption keys'))
    lines.append(txt_row('Key zeroisation = secure key erasure on decommission; NIST SP800-88 procedure'))
    lines.append(txt_row('Re-keying       = rotating encryption keys for stored data without decrypting first'))
    lines.append(txt_row('SSH             = Secure Shell; replaces Telnet for encrypted CLI management access'))
    lines.append(txt_row('TLS 1.2/1.3     = Transport Layer Security; HTTPS management GUI encryption'))
    lines.append(txt_row('Dual control    = key operations require two independent admin approvals'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-fabric-os-sec-hard', 'docs/san/brocade/fabric-os/security/hardening/index.md', 'Brocade Fabric OS Hardening')
def _brocade_fabric_os_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade Fabric OS — Security Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('Hardening: disable legacy protocols, enforce RBAC, enable security policies, patch FOS.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Protocol & Service Hardening'), bMid(L2, R2, 'Account & Auth Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable Telnet: sshutil disable'), bMid(L2, R2, 'TACACS+ for all admin auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable FTP: no sftp fallback'), bMid(L2, R2, 'Remove default admin password'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable HTTP: HTTPS only'), bMid(L2, R2, 'Lockout after 3 failed attempts'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMPv3 only: disable v1/v2c'), bMid(L2, R2, 'Complexity: 10 char + mixed'))))
    lines.append(R(merge(bMid(L1, R1, 'Restrict management IP range'), bMid(L2, R2, 'Expiry: 90-day password policy'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Disable all legacy protocols; enforce TACACS+; limit management access to known IPs.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric Security Policies'), bMid(L2, R2, 'Firmware & Patch Management'))))
    lines.append(R(merge(bMid(L1, R1, 'SCC: restrict switch ISL joins'), bMid(L2, R2, 'FOS patch cycle: quarterly'))))
    lines.append(R(merge(bMid(L1, R1, 'DCC: bind devices to ports'), bMid(L2, R2, 'Check PSIRTs before upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'DH-CHAP on all ISL ports'), bMid(L2, R2, 'Test upgrade in non-prod first'))))
    lines.append(R(merge(bMid(L1, R1, 'Zoning: deny-by-default'), bMid(L2, R2, 'HA firmware: no-disrupt path'))))
    lines.append(R(merge(bMid(L1, R1, 'MAPS: alert on anomalies'), bMid(L2, R2, 'Rollback plan if upgrade fails'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade FC switch · dedicated mgmt Ethernet · serial console for recovery'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('sshutil         = Fabric OS CLI to enable/disable SSH and Telnet services'))
    lines.append(txt_row('SCC             = Switch Connection Control; restricts which FC switches can form ISLs'))
    lines.append(txt_row('DCC             = Device Connection Control; binds HBA WWNs to specific switch ports'))
    lines.append(txt_row('DH-CHAP         = Diffie-Hellman CHAP; authenticates switches before ISL formation'))
    lines.append(txt_row('MAPS            = Monitoring and Alerting Policy Suite; threshold-based anomaly detection'))
    lines.append(txt_row('PSIRT           = Product Security Incident Response Team advisory; vendor security bulletin'))
    lines.append(txt_row('HA firmware     = non-disruptive FOS upgrade; active CP reboots while standby takes over'))
    lines.append(txt_row('SNMPv3          = SNMP v3; authentication (MD5/SHA) + privacy (AES) mode required'))
    lines.append(txt_row('Deny-by-default = zone policy: traffic allowed only if explicitly zoned together'))
    lines.append(txt_row('TACACS+         = centralised CLI auth; all switch admin commands audited centrally'))
    lines.append(txt_row('Lockout policy  = account locked after N failed logins; unlocked by admin or timeout'))
    lines.append(txt_row('IP whitelist    = management source IP restriction; configured via acp filter command'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-fabric-os-trouble-common', 'docs/san/brocade/fabric-os/troubleshooting/common-issues/index.md', 'Brocade Fabric OS Common Issues')
def _brocade_fabric_os_trouble_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade Fabric OS — Troubleshooting Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common Fabric OS issues: ISL bounce, zone merge fail, port offline, MAPS alerts, login err.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ISL & Fabric Issues'), bMid(L2, R2, 'Port & Login Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'ISL bounce: check SFP/cable'), bMid(L2, R2, 'Port offline: portenable check'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone merge conflict: cfgshow'), bMid(L2, R2, 'nsshow: device not logged in'))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric split: check E_Port state'), bMid(L2, R2, 'CRC errors: replace SFP/cable'))))
    lines.append(R(merge(bMid(L1, R1, 'DH-CHAP fail: secret mismatch'), bMid(L2, R2, 'Speed mismatch: portcfgspeed'))))
    lines.append(R(merge(bMid(L1, R1, 'Domain conflict: isolate switch'), bMid(L2, R2, 'F_Port G_Port state error'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('ISL and zone issues affect whole fabric; port and login issues affect specific devices.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Performance & MAPS Issues'), bMid(L2, R2, 'Firmware & Recovery'))))
    lines.append(R(merge(bMid(L1, R1, 'MAPS: threshold exceeded alert'), bMid(L2, R2, 'firmwareshow: mismatch VER'))))
    lines.append(R(merge(bMid(L1, R1, 'Credit starvation: BB credits'), bMid(L2, R2, 'HA reboot: trigger failover'))))
    lines.append(R(merge(bMid(L1, R1, 'Utilisation: portperfshow'), bMid(L2, R2, 'supportshow for TAC bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'FCIP tunnel congestion drop'), bMid(L2, R2, 'Factory reset: switchdisable'))))
    lines.append(R(merge(bMid(L1, R1, 'Queue depth: host HBA adjust'), bMid(L2, R2, 'Serial console: recovery boot'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade FC switch · SFP transceivers · FC cables · management Ethernet · serial console'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ISL             = Inter-Switch Link; E_Port connection between FC switches'))
    lines.append(txt_row('Zone merge      = zone database conflict between two fabrics joining; requires resolve'))
    lines.append(txt_row('CRC error       = Cyclic Redundancy Check error on FC frame; indicates bad SFP/cable'))
    lines.append(txt_row('BB credits      = Buffer-to-Buffer credits; flow control for FC frames between switches'))
    lines.append(txt_row('Credit starvation= receiver has no BB credits; sender must pause; causes latency'))
    lines.append(txt_row('MAPS            = Monitoring and Alerting Policy Suite; rule-based threshold alerting'))
    lines.append(txt_row('portperfshow    = CLI to display per-port throughput and error counters'))
    lines.append(txt_row('nsshow          = Name Server show; lists all devices logged into the local switch'))
    lines.append(txt_row('DH-CHAP fail    = ISL authentication failure; both switches must share same secret'))
    lines.append(txt_row('Domain conflict = two switches with same domain ID; isolate and renumber one'))
    lines.append(txt_row('supportshow     = generates full diagnostic tech-support bundle for TAC upload'))
    lines.append(txt_row('HA reboot       = High Availability failover; active CP reboots to standby CP'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-fabric-os-trouble-diag', 'docs/san/brocade/fabric-os/troubleshooting/diagnostics/index.md', 'Brocade Fabric OS Diagnostics')
def _brocade_fabric_os_trouble_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade Fabric OS — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('Diagnostics: error logs, portshow, MAPS rules, raslog, supportshow, and port tests.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Log & Event Diagnostics'), bMid(L2, R2, 'Port & Hardware Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'errshow: fabric error log'), bMid(L2, R2, 'portshow: port state + stats'))))
    lines.append(R(merge(bMid(L1, R1, 'raslog: RAS event log detail'), bMid(L2, R2, 'portstatsshow: counters delta'))))
    lines.append(R(merge(bMid(L1, R1, 'errdump: dump to syslog'), bMid(L2, R2, 'porttest: loopback diagnostic'))))
    lines.append(R(merge(bMid(L1, R1, 'MAPS: mapsconfig + mapspolicy'), bMid(L2, R2, 'sensorshow: temp + fan + PSU'))))
    lines.append(R(merge(bMid(L1, R1, 'syslogdipadd: send to syslog'), bMid(L2, R2, 'diagstatus: blade diagnostics'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('errshow and raslog are the primary event sources; portshow for per-port analysis.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric-Level Diagnostics'), bMid(L2, R2, 'Collection for TAC Escalation'))))
    lines.append(R(merge(bMid(L1, R1, 'nsshow + fabricshow'), bMid(L2, R2, 'supportshow: full bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'cfgshow: zone config snapshot'), bMid(L2, R2, 'supportsave: save to USB/SCP'))))
    lines.append(R(merge(bMid(L1, R1, 'islshow: ISL utilisation data'), bMid(L2, R2, 'portdump: binary port trace'))))
    lines.append(R(merge(bMid(L1, R1, 'switchstatusshow: overall'), bMid(L2, R2, 'mgmtshow: management NIC'))))
    lines.append(R(merge(bMid(L1, R1, 'licenseshow: FOS license check'), bMid(L2, R2, 'pcap: port frame capture'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade FC switch · serial console · USB drive for supportsave · syslog server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('errshow         = displays fabric error log; most recent errors first with severity'))
    lines.append(txt_row('raslog          = RAS (Reliability/Availability/Serviceability) detailed event log'))
    lines.append(txt_row('portshow        = per-port status: state, speed, SFP type, credits, error counters'))
    lines.append(txt_row('portstatsshow   = per-port frame counter snapshot; use twice for delta'))
    lines.append(txt_row('porttest        = in-service loopback; port must be disabled first'))
    lines.append(txt_row('sensorshow      = hardware sensor readings: temperature, fan RPM, PSU voltage'))
    lines.append(txt_row('diagstatus      = blade/chassis diagnostic test results and pass/fail status'))
    lines.append(txt_row('supportshow     = full diagnostic bundle; run on both switches in HA pair'))
    lines.append(txt_row('supportsave     = saves supportshow output to SCP/FTP/USB for offline analysis'))
    lines.append(txt_row('MAPS            = Monitoring and Alerting Policy Suite; tracks thresholds over time'))
    lines.append(txt_row('pcap            = port frame capture; captures FC frames for protocol analysis'))
    lines.append(txt_row('syslogdipadd    = adds a syslog server IP; Fabric OS sends events to SIEM'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-fabric-os-trouble-esc', 'docs/san/brocade/fabric-os/troubleshooting/escalation/index.md', 'Brocade Fabric OS Escalation')
def _brocade_fabric_os_trouble_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade Fabric OS — Troubleshooting Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('Escalation path: internal SAN team → Broadcom TAC with supportshow bundle and timeline.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Internal Escalation'), bMid(L2, R2, 'Broadcom TAC Escalation'))))
    lines.append(R(merge(bMid(L1, R1, 'SAN L1 → SAN L2: logs+timeline'), bMid(L2, R2, 'Open case: support.broadcom'))))
    lines.append(R(merge(bMid(L1, R1, 'SAN L2 → L3: supportsave bundle'), bMid(L2, R2, 'Serial/contract number req.'))))
    lines.append(R(merge(bMid(L1, R1, 'L3 → TAC: full diag data'), bMid(L2, R2, 'Sev-1: fabric down in prod'))))
    lines.append(R(merge(bMid(L1, R1, 'Incident manager for Sev-1'), bMid(L2, R2, 'Remote: TAC SSH to switch'))))
    lines.append(R(merge(bMid(L1, R1, 'Change freeze during incident'), bMid(L2, R2, 'Escalation to engineering'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Collect supportsave from all affected switches before engaging Broadcom TAC.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Data Package'), bMid(L2, R2, 'Escalation Criteria'))))
    lines.append(R(merge(bMid(L1, R1, 'supportsave from each switch'), bMid(L2, R2, 'Sev-1: fabric/storage down'))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric topology: fabricshow'), bMid(L2, R2, 'Sev-2: degraded production'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone config: cfgshow output'), bMid(L2, R2, 'Sev-3: non-critical issue'))))
    lines.append(R(merge(bMid(L1, R1, 'Error timeline from errshow'), bMid(L2, R2, 'Sev-4: general question'))))
    lines.append(R(merge(bMid(L1, R1, 'Recent changes before failure'), bMid(L2, R2, 'Post-incident: RCA request'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade FC switch · management Ethernet · serial console · Broadcom TAC upload portal'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('supportsave     = saves full diagnostic bundle to SCP/FTP/USB; required for TAC'))
    lines.append(txt_row('errshow         = error log snapshot; provides timeline of events before failure'))
    lines.append(txt_row('fabricshow      = fabric topology; shows all domain IDs and switch names'))
    lines.append(txt_row('cfgshow         = zone config snapshot; shows active and saved zone databases'))
    lines.append(txt_row('Sev-1           = production down; fabric or storage completely inaccessible'))
    lines.append(txt_row('RCA             = Root Cause Analysis; post-incident document requested from TAC'))
    lines.append(txt_row('Broadcom TAC    = Technical Assistance Center; opened at support.broadcom.com'))
    lines.append(txt_row('Incident manager= internal role; coordinates bridge call and vendor TAC engagement'))
    lines.append(txt_row('Serial number   = switch chassis serial; required to open Broadcom support case'))
    lines.append(txt_row('Change freeze   = no config changes during active Sev-1 incident investigation'))
    lines.append(txt_row('Remote access   = TAC engineer SSH into switch via customer-granted access'))
    lines.append(txt_row('Post-incident   = RCA + preventive actions + monitoring improvements after resolution'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-arch', 'docs/san/brocade/sannav/architecture/index.md', 'Brocade SANnav Architecture')
def _brocade_sannav_arch():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2, L3, R3 = 3, 33, 36, 66, 69, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav: centralised SAN management platform for Brocade FC fabrics, zoning, and analytics.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'How It Works'), bMid(L2, R2, 'Integrations'), bMid(L3, R3, 'Design Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'SANnav OVA: VM appliance'), bMid(L2, R2, 'DCNM / NDFC import'), bMid(L3, R3, 'HA: primary + standby'))))
    lines.append(R(merge(bMid(L1, R1, 'Discovers via SNMP/REST API'), bMid(L2, R2, 'syslog forward to SIEM'), bMid(L3, R3, 'Separate mgmt VLAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone management GUI + API'), bMid(L2, R2, 'TACACS+ for auth'), bMid(L3, R3, 'Role-based access'))))
    lines.append(R(merge(bMid(L1, R1, 'MAPS alert aggregation'), bMid(L2, R2, 'REST API for automation'), bMid(L3, R3, 'Backup to NFS/SCP'))))
    lines.append(R(merge(bMid(L1, R1, 'Firmware management'), bMid(L2, R2, 'Email/SNMP alerting'), bMid(L3, R3, 'TLS 1.2/1.3 only'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('SANnav aggregates all Brocade fabric management into one GUI and REST API endpoint.'))
    lines.append(txt_row())
    lines.append(R(arrow([18, 51, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Managed Resources'), bMid(L2, R2, 'Data Layer'), bMid(L3, R3, 'Management Layer'))))
    lines.append(R(merge(bMid(L1, R1, 'Brocade FC switches'), bMid(L2, R2, 'PostgreSQL DB: config'), bMid(L3, R3, 'Web GUI: HTTPS'))))
    lines.append(R(merge(bMid(L1, R1, 'Brocade Directors'), bMid(L2, R2, 'Elasticsearch: analytics'), bMid(L3, R3, 'REST API: token auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Virtual Fabrics (VF)'), bMid(L2, R2, 'Time-series perf data'), bMid(L3, R3, 'CLI: sannav-admin'))))
    lines.append(R(merge(bMid(L1, R1, 'FC zone databases'), bMid(L2, R2, 'Configuration backup'), bMid(L3, R3, 'LDAP/TACACS+ auth'))))
    lines.append(R(merge(bMid(L1, R1, 'SFP inventory per port'), bMid(L2, R2, 'Audit trail events'), bMid(L3, R3, 'SNMP trap receiver'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Linux VM (OVA) on vSphere · management Ethernet · Brocade FC switch management ports'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav          = Broadcom SAN Navigator; management platform for Brocade FC fabrics'))
    lines.append(txt_row('OVA             = Open Virtual Appliance; pre-built VM image for vSphere deployment'))
    lines.append(txt_row('MAPS            = Monitoring and Alerting Policy Suite; threshold alerts from switches'))
    lines.append(txt_row('Virtual Fabric  = logical switch partitioning on Brocade directors; managed per-VF'))
    lines.append(txt_row('REST API        = SANnav northbound API; JSON over HTTPS for automation integration'))
    lines.append(txt_row('Elasticsearch   = search and analytics engine; stores SANnav performance time-series'))
    lines.append(txt_row('PostgreSQL      = relational database storing SANnav configuration and inventory'))
    lines.append(txt_row('SFP             = Small Form-factor Pluggable transceiver; FC port optical module'))
    lines.append(txt_row('Zone database   = set of zones and aliases defining which devices can communicate'))
    lines.append(txt_row('TACACS+         = Terminal Access Controller Auth; centralised SANnav user auth'))
    lines.append(txt_row('HA pair         = SANnav primary + standby; standby takes over if primary fails'))
    lines.append(txt_row('Audit trail     = log of all user actions in SANnav; retained for compliance'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-arch-how', 'docs/san/brocade/sannav/architecture/how-it-works/index.md', 'Brocade SANnav How It Works')
def _brocade_sannav_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav discovers switches via SNMP/REST, aggregates MAPS events, manages zones centrally.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Discovery & Polling'), bMid(L2, R2, 'Zone Management Workflow'))))
    lines.append(R(merge(bMid(L1, R1, 'Add switch IP → SNMP v3 poll'), bMid(L2, R2, 'GUI: browse fabric topology'))))
    lines.append(R(merge(bMid(L1, R1, 'FOS REST API credential auth'), bMid(L2, R2, 'Zone wizard: alias + zone'))))
    lines.append(R(merge(bMid(L1, R1, 'Topology built: domain + ports'), bMid(L2, R2, 'Push zone config to fabric'))))
    lines.append(R(merge(bMid(L1, R1, 'Inventory: SFP/HBA/port data'), bMid(L2, R2, 'cfgsave + cfgenable remote'))))
    lines.append(R(merge(bMid(L1, R1, 'MAPS alerts: event forwarding'), bMid(L2, R2, 'Zone diff: compare changes'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SANnav polls switches for state; zone changes are staged and pushed via FOS API.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Performance Monitoring'), bMid(L2, R2, 'Firmware Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Port utilisation: 5-min poll'), bMid(L2, R2, 'Upload FOS image to SANnav'))))
    lines.append(R(merge(bMid(L1, R1, 'Dashboards: top talkers'), bMid(L2, R2, 'Stage firmware per switch'))))
    lines.append(R(merge(bMid(L1, R1, 'Historical: 90-day retention'), bMid(L2, R2, 'Schedule: maintenance window'))))
    lines.append(R(merge(bMid(L1, R1, 'Alerts: email/SNMP on breach'), bMid(L2, R2, 'HA upgrade: non-disruptive'))))
    lines.append(R(merge(bMid(L1, R1, 'Bottleneck detection report'), bMid(L2, R2, 'Post-upgrade version verify'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav VM · management network · Brocade FC switches · NTP for time sync'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SNMPv3          = polling protocol; SANnav uses for switch discovery and alerting'))
    lines.append(txt_row('FOS REST API    = Fabric OS northbound API; SANnav uses for zone/config management'))
    lines.append(txt_row('MAPS alert      = switch-side threshold event forwarded to SANnav as notification'))
    lines.append(txt_row('Zone wizard     = SANnav GUI workflow for creating aliases and zones step-by-step'))
    lines.append(txt_row('cfgsave/cfgenable= zone config save and activation; SANnav triggers on switches'))
    lines.append(txt_row('Zone diff       = SANnav shows before/after zone changes before committing'))
    lines.append(txt_row('Top talkers     = ports/flows with highest utilisation; identified in performance view'))
    lines.append(txt_row('HA upgrade      = firmware loaded to standby CP first; switch-over then upgrade active'))
    lines.append(txt_row('5-min poll      = default SANnav performance data collection interval per port'))
    lines.append(txt_row('Stage firmware  = upload FOS image to switch flash without activating; activate later'))
    lines.append(txt_row('Bottleneck report= SANnav identifies congested ISLs and credit-starved ports'))
    lines.append(txt_row('90-day retention= default performance data history in SANnav Elasticsearch store'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-arch-int', 'docs/san/brocade/sannav/architecture/integrations/index.md', 'Brocade SANnav Integrations')
def _brocade_sannav_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav integrates with SIEM, TACACS+, SNMP NMS, REST automation, and NTP/SMTP.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity & Auth Integrations'), bMid(L2, R2, 'Monitoring Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'TACACS+: admin user auth'), bMid(L2, R2, 'SNMP trap to NMS (HPE/IBM)'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP: group-based role map'), bMid(L2, R2, 'syslog to SIEM (Splunk/QRadar)'))))
    lines.append(R(merge(bMid(L1, R1, 'RADIUS: fallback auth option'), bMid(L2, R2, 'Email: SMTP alert forwarding'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO: SAML 2.0 support'), bMid(L2, R2, 'Webhook: REST event push'))))
    lines.append(R(merge(bMid(L1, R1, 'Local accounts: fallback only'), bMid(L2, R2, 'Grafana: API data source'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Auth integrations centralise login; monitoring integrations feed SIEM and NMS.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Automation Integrations'), bMid(L2, R2, 'Infrastructure Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API: token + HTTPS'), bMid(L2, R2, 'NTP: time sync for events'))))
    lines.append(R(merge(bMid(L1, R1, 'Ansible: SANnav collection'), bMid(L2, R2, 'DNS: switch hostname resolve'))))
    lines.append(R(merge(bMid(L1, R1, 'Terraform: SANnav provider'), bMid(L2, R2, 'NFS: backup destination'))))
    lines.append(R(merge(bMid(L1, R1, 'ServiceNow: CMDB CI sync'), bMid(L2, R2, 'SCP: supportsave upload'))))
    lines.append(R(merge(bMid(L1, R1, 'Python requests library'), bMid(L2, R2, 'vSphere: OVA VM hosting'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav VM on vSphere · management Ethernet · TACACS+/LDAP server · NFS backup share'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TACACS+         = Terminal Access Controller; centralised admin auth for SANnav GUI'))
    lines.append(txt_row('LDAP            = Lightweight Directory Access Protocol; AD group-to-role mapping'))
    lines.append(txt_row('SAML 2.0        = Security Assertion Markup Language; SSO federation for SANnav'))
    lines.append(txt_row('REST API        = SANnav northbound API; JSON/HTTPS; token-based authentication'))
    lines.append(txt_row('SNMP trap       = SANnav forwards MAPS/fabric events to NMS via SNMP v2c/v3'))
    lines.append(txt_row('Webhook         = HTTP POST to external system on SANnav event trigger'))
    lines.append(txt_row('Ansible collection= Broadcom-published Ansible modules for SANnav automation'))
    lines.append(txt_row('ServiceNow CMDB = CI records for fabric switches auto-synced from SANnav inventory'))
    lines.append(txt_row('NFS backup      = SANnav config/database backup to NFS share; scheduled daily'))
    lines.append(txt_row('NTP             = Network Time Protocol; critical for correlated event timestamps'))
    lines.append(txt_row('OVA             = Open Virtual Appliance; SANnav delivered as vSphere OVA template'))
    lines.append(txt_row('SCP             = Secure Copy; used for supportsave upload and firmware transfers'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-arch-design', 'docs/san/brocade/sannav/architecture/design-standards/index.md', 'Brocade SANnav Design Standards')
def _brocade_sannav_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('Design principles: HA deployment, dedicated management VLAN, RBAC, TLS, backups.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Deployment Standards'), bMid(L2, R2, 'Security Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'HA pair: primary + standby VM'), bMid(L2, R2, 'TLS 1.2+ for all web traffic'))))
    lines.append(R(merge(bMid(L1, R1, 'Separate management VLAN'), bMid(L2, R2, 'TACACS+ mandatory; no local'))))
    lines.append(R(merge(bMid(L1, R1, '4 vCPU / 16 GB RAM minimum'), bMid(L2, R2, 'RBAC: read-only for operators'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP for all timestamps'), bMid(L2, R2, 'SNMPv3 only; disable v1/v2c'))))
    lines.append(R(merge(bMid(L1, R1, 'Dedicated mgmt DNS entries'), bMid(L2, R2, 'IP whitelist for API access'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('HA ensures continuity; dedicated VLAN isolates management traffic from data plane.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Operational Standards'), bMid(L2, R2, 'Scalability Guidelines'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup: daily NFS; 30-day ret.'), bMid(L2, R2, 'Max 1,000 switches per node'))))
    lines.append(R(merge(bMid(L1, R1, 'Alert review: daily MAPS check'), bMid(L2, R2, 'Max 100,000 ports per node'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone changes: change ticket'), bMid(L2, R2, 'Separate instances per fabric'))))
    lines.append(R(merge(bMid(L1, R1, 'Firmware mgmt via SANnav only'), bMid(L2, R2, 'Scale-out: additional VM'))))
    lines.append(R(merge(bMid(L1, R1, 'Quarterly SANnav upgrade'), bMid(L2, R2, 'Storage: 2 TB for 90-day perf'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere host · shared datastore (2 TB+) · management Ethernet switch · NFS backup'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('HA pair         = SANnav primary+standby VMs; standby syncs config and takes over'))
    lines.append(txt_row('Management VLAN = isolated VLAN for switch OOB and SANnav traffic; no user VLAN'))
    lines.append(txt_row('RBAC            = Role-Based Access Control; admin/operator/read-only roles in SANnav'))
    lines.append(txt_row('NTP             = Network Time Protocol; all events timestamped; required for SIEM'))
    lines.append(txt_row('SNMPv3          = SNMP version 3; auth + privacy mode; disable v1/v2c in SANnav'))
    lines.append(txt_row('IP whitelist     = restrict REST API and management access to known source IPs'))
    lines.append(txt_row('TLS 1.2+        = minimum TLS version for SANnav HTTPS management GUI'))
    lines.append(txt_row('NFS backup      = daily SANnav configuration and database backup to NFS share'))
    lines.append(txt_row('MAPS check      = daily review of Monitoring and Alerting Policy Suite events'))
    lines.append(txt_row('Change ticket   = ITSM requirement; all zone changes need approved change record'))
    lines.append(txt_row('90-day perf     = SANnav default performance data retention; requires ~2 TB storage'))
    lines.append(txt_row('Scale-out       = deploy additional SANnav instances when port count exceeds limit'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-ops-procedures', 'docs/san/brocade/sannav/operations/procedures/index.md', 'Brocade SANnav Operations Procedures')
def _brocade_sannav_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Operations Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Day-to-day SANnav procedures: zone changes, switch adds, firmware, health monitoring.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Zone Change Procedure'), bMid(L2, R2, 'Switch Add / Remove'))))
    lines.append(R(merge(bMid(L1, R1, '1. Create alias for HBA WWN'), bMid(L2, R2, '1. Add switch IP in SANnav'))))
    lines.append(R(merge(bMid(L1, R1, '2. Add alias to target zone'), bMid(L2, R2, '2. Set SNMP v3 credentials'))))
    lines.append(R(merge(bMid(L1, R1, '3. Add zone to active config'), bMid(L2, R2, '3. Discover: verify ports'))))
    lines.append(R(merge(bMid(L1, R1, '4. Review diff before push'), bMid(L2, R2, '4. Configure MAPS policy'))))
    lines.append(R(merge(bMid(L1, R1, '5. cfgsave + cfgenable'), bMid(L2, R2, '5. Verify firmware level'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Zone changes require change ticket; always review diff before activating config.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Firmware Management'), bMid(L2, R2, 'Health Monitoring Routine'))))
    lines.append(R(merge(bMid(L1, R1, '1. Upload FOS to SANnav repo'), bMid(L2, R2, 'Daily: MAPS alert review'))))
    lines.append(R(merge(bMid(L1, R1, '2. Validate against switch ver'), bMid(L2, R2, 'Weekly: port error report'))))
    lines.append(R(merge(bMid(L1, R1, '3. Schedule upgrade window'), bMid(L2, R2, 'Monthly: utilisation trend'))))
    lines.append(R(merge(bMid(L1, R1, '4. HA upgrade: standby first'), bMid(L2, R2, 'Quarterly: zone audit'))))
    lines.append(R(merge(bMid(L1, R1, '5. Verify version post-upgrade'), bMid(L2, R2, 'Annual: SANnav upgrade'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav VM · management network · Brocade FC switch chassis · SFP transceivers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Alias           = named WWN or alias group; used as zone member instead of raw WWN'))
    lines.append(txt_row('Zone diff       = SANnav shows before/after view of zone changes before activating'))
    lines.append(txt_row('cfgsave/cfgenable= save and activate zone config; SANnav executes these on switches'))
    lines.append(txt_row('MAPS            = Monitoring and Alerting Policy Suite; daily alert review priority'))
    lines.append(txt_row('HA upgrade      = firmware activated on standby CP first; switchover then active'))
    lines.append(txt_row('FOS repo        = SANnav local repository for staging Fabric OS firmware images'))
    lines.append(txt_row('Port error report= weekly SANnav report on CRC/loss-of-sync per port'))
    lines.append(txt_row('Zone audit      = quarterly review of all zones for unused aliases and orphaned WWNs'))
    lines.append(txt_row('Change ticket   = ITSM-required approval before any zone or fabric configuration change'))
    lines.append(txt_row('WWN             = World Wide Name; 64-bit identifier for HBAs and switch ports'))
    lines.append(txt_row('Utilisation trend= monthly SANnav capacity report; identifies approaching saturation'))
    lines.append(txt_row('SNMP v3         = SNMPv3 credentials required for SANnav to discover and poll switches'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-ops-backup', 'docs/san/brocade/sannav/operations/backup-restore/index.md', 'Brocade SANnav Backup Restore')
def _brocade_sannav_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Backup and Restore'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav backup covers config DB, performance data, zone snapshots, and switch firmware.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SANnav Backup'), bMid(L2, R2, 'Switch Zone Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'Daily: NFS destination backup'), bMid(L2, R2, 'configupload per switch'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup includes: DB + config'), bMid(L2, R2, 'Zoning snapshot before change'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: GUI → Admin → Backup'), bMid(L2, R2, 'Store in NFS or version ctrl'))))
    lines.append(R(merge(bMid(L1, R1, 'Retention: 30 days recommended'), bMid(L2, R2, 'cfgshow: verify active config'))))
    lines.append(R(merge(bMid(L1, R1, 'Test restore quarterly'), bMid(L2, R2, 'supportsave before firmware'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SANnav config backup and zone backups are independent; both required for full recovery.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SANnav Restore Procedure'), bMid(L2, R2, 'Switch Config Restore'))))
    lines.append(R(merge(bMid(L1, R1, '1. Deploy fresh SANnav OVA'), bMid(L2, R2, 'configdownload to switch'))))
    lines.append(R(merge(bMid(L1, R1, '2. Restore DB from NFS backup'), bMid(L2, R2, 'Zone restore: cfgsave first'))))
    lines.append(R(merge(bMid(L1, R1, '3. Verify switch discovery'), bMid(L2, R2, 'cfgenable to activate zones'))))
    lines.append(R(merge(bMid(L1, R1, '4. Re-validate TACACS+ auth'), bMid(L2, R2, 'Verify: nsshow + fabricshow'))))
    lines.append(R(merge(bMid(L1, R1, '5. Test alert forwarding'), bMid(L2, R2, 'Test: host I/O after restore'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav VM · NFS backup server · Brocade FC switch chassis · vSphere host'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('NFS backup      = SANnav configuration and database exported to NFS mount point'))
    lines.append(txt_row('configupload    = Fabric OS CLI; uploads switch config (zones + system) to FTP/SCP'))
    lines.append(txt_row('configdownload  = Fabric OS CLI; restores switch config from FTP/SCP file'))
    lines.append(txt_row('cfgsave         = saves zone database changes to switch NVRAM flash'))
    lines.append(txt_row('cfgenable       = activates named zone configuration across the fabric'))
    lines.append(txt_row('supportsave     = full diagnostic capture; run before any firmware or major change'))
    lines.append(txt_row('Zone snapshot   = cfgshow output captured before zone change as rollback reference'))
    lines.append(txt_row('SANnav OVA      = fresh SANnav VM deployed from Broadcom-provided OVA template'))
    lines.append(txt_row('nsshow          = name server show; verifies devices re-login after restore'))
    lines.append(txt_row('fabricshow      = topology show; verifies fabric re-forms after config restore'))
    lines.append(txt_row('Retention policy= keep 30 days of SANnav backups; prune older to manage storage'))
    lines.append(txt_row('Restore test    = quarterly test of full restore to validate backup integrity'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-ops-health', 'docs/san/brocade/sannav/operations/health-checks/index.md', 'Brocade SANnav Health Checks')
def _brocade_sannav_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav health checks: MAPS dashboards, port error trends, switch status, ISL load.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SANnav Dashboard Health'), bMid(L2, R2, 'Switch-Level Health'))))
    lines.append(R(merge(bMid(L1, R1, 'MAPS: active alerts by severity'), bMid(L2, R2, 'switchstatusshow: all green'))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric topology: no split'), bMid(L2, R2, 'sensorshow: temp < threshold'))))
    lines.append(R(merge(bMid(L1, R1, 'Port inventory: no offline ports'), bMid(L2, R2, 'Fan + PSU: healthy state'))))
    lines.append(R(merge(bMid(L1, R1, 'Firmware currency: < 2 versions'), bMid(L2, R2, 'CP status: active + standby'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone config: saved == active'), bMid(L2, R2, 'Port errors < 10/day limit'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('MAPS and SANnav dashboards are primary health indicators; review daily.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ISL & Fabric Health'), bMid(L2, R2, 'SANnav Platform Health'))))
    lines.append(R(merge(bMid(L1, R1, 'islshow: utilisation < 70%'), bMid(L2, R2, 'SANnav service: all running'))))
    lines.append(R(merge(bMid(L1, R1, 'ISL BB credits: no starvation'), bMid(L2, R2, 'DB size: within capacity'))))
    lines.append(R(merge(bMid(L1, R1, 'fabricshow: single fabric'), bMid(L2, R2, 'HA sync: primary = standby'))))
    lines.append(R(merge(bMid(L1, R1, 'Bottleneck: no congested ISLs'), bMid(L2, R2, 'Backup: last job success'))))
    lines.append(R(merge(bMid(L1, R1, 'D_Port: link quality > -3 dBm'), bMid(L2, R2, 'Alerts: SMTP + SNMP active'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade FC switch chassis · SFP optical levels · ISL cables · SANnav VM resources'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('MAPS            = Monitoring and Alerting Policy Suite; tracks thresholds per port'))
    lines.append(txt_row('switchstatusshow= overall switch health status; green = all healthy'))
    lines.append(txt_row('sensorshow      = temp/fan/PSU readings; alert if temperature exceeds threshold'))
    lines.append(txt_row('BB credits      = Buffer-to-Buffer credits; starvation causes ISL congestion'))
    lines.append(txt_row('islshow         = ISL utilisation; > 70% sustained indicates need for more ISLs'))
    lines.append(txt_row('D_Port          = diagnostic port; optical signal quality measurement (dBm)'))
    lines.append(txt_row('fabricshow      = single fabric confirmation; split fabric = major incident'))
    lines.append(txt_row('CP status       = Control Processor; HA pair should have active + standby running'))
    lines.append(txt_row('Bottleneck      = SANnav congestion detection; ISL fully utilized under load'))
    lines.append(txt_row('HA sync         = primary and standby SANnav databases must be in sync'))
    lines.append(txt_row('Zone config     = saved config should match active config; divergence = risk'))
    lines.append(txt_row('dBm             = decibels relative to 1 milliwatt; SFP optical power measurement'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-ops-install', 'docs/san/brocade/sannav/operations/install-upgrade/index.md', 'Brocade SANnav Install Upgrade')
def _brocade_sannav_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav deployment: OVA to vSphere, initial config, discover switches, upgrade path.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fresh Install Steps'), bMid(L2, R2, 'Initial Configuration'))))
    lines.append(R(merge(bMid(L1, R1, '1. Download SANnav OVA from BCM'), bMid(L2, R2, '1. Set hostname + IP address'))))
    lines.append(R(merge(bMid(L1, R1, '2. Deploy OVA in vSphere'), bMid(L2, R2, '2. Configure NTP servers'))))
    lines.append(R(merge(bMid(L1, R1, '3. Power on + accept EULA'), bMid(L2, R2, '3. Set admin password'))))
    lines.append(R(merge(bMid(L1, R1, '4. Assign: 4 vCPU / 16 GB RAM'), bMid(L2, R2, '4. Configure TACACS+/LDAP'))))
    lines.append(R(merge(bMid(L1, R1, '5. 2 TB datastore for perf data'), bMid(L2, R2, '5. Discover fabric switches'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('OVA deployment is quick; NTP and TACACS+ must be configured before adding switches.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Procedure'), bMid(L2, R2, 'Post-Upgrade Validation'))))
    lines.append(R(merge(bMid(L1, R1, '1. Backup SANnav DB to NFS'), bMid(L2, R2, '1. Verify all switches present'))))
    lines.append(R(merge(bMid(L1, R1, '2. Download new SANnav OVA'), bMid(L2, R2, '2. Check MAPS alerts forwarding'))))
    lines.append(R(merge(bMid(L1, R1, '3. Deploy standby; restore DB'), bMid(L2, R2, '3. Re-test TACACS+ auth'))))
    lines.append(R(merge(bMid(L1, R1, '4. Validate standby operation'), bMid(L2, R2, '4. Verify NFS backup schedule'))))
    lines.append(R(merge(bMid(L1, R1, '5. Swing DNS; decom old'), bMid(L2, R2, '5. Confirm zone management ok'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere host · shared 2 TB datastore · management network · NFS backup share'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OVA             = Open Virtual Appliance; SANnav package for vSphere deployment'))
    lines.append(txt_row('BCM             = Broadcom; download SANnav OVA from support.broadcom.com'))
    lines.append(txt_row('EULA            = End User License Agreement; accepted on first SANnav boot'))
    lines.append(txt_row('vCPU            = virtual CPU; SANnav minimum is 4 vCPU for production use'))
    lines.append(txt_row('Datastore       = vSphere storage; SANnav needs ~2 TB for 90-day perf history'))
    lines.append(txt_row('NFS backup      = SANnav DB backup destination; required before any upgrade'))
    lines.append(txt_row('Swing DNS       = update DNS A record to point to new SANnav VM after validation'))
    lines.append(txt_row('TACACS+         = centralised auth; must be re-tested after every SANnav upgrade'))
    lines.append(txt_row('MAPS forwarding = MAPS alerts from switches must flow to new SANnav after upgrade'))
    lines.append(txt_row('NTP servers     = time sync; must be configured before adding switches to SANnav'))
    lines.append(txt_row('Zone management = ability to push zone changes from SANnav GUI after upgrade'))
    lines.append(txt_row('Standby upgrade = deploy new SANnav version as standby; validate before DNS swing'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-ops-scripts', 'docs/san/brocade/sannav/operations/scripts/index.md', 'Brocade SANnav Operations Scripts')
def _brocade_sannav_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Operations Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav scripting: REST API automation, zone management, reporting, Ansible playbooks.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'REST API Scripting'), bMid(L2, R2, 'Zone Automation Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Auth: POST /api/v1/login token'), bMid(L2, R2, 'Python: create alias + zone'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /api/v1/fabric/switch list'), bMid(L2, R2, 'Ansible: broadcom.sannav'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /api/v1/port/performance'), bMid(L2, R2, 'Validate: cfgshow post-push'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /api/v1/zone to create'), bMid(L2, R2, 'Batch zone from CSV input'))))
    lines.append(R(merge(bMid(L1, R1, 'DELETE /api/v1/zone cleanup'), bMid(L2, R2, 'WWN lookup: nsshow parse'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('REST API enables full zone lifecycle automation; Ansible collection wraps API calls.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Reporting Scripts'), bMid(L2, R2, 'Maintenance Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Port utilisation: weekly CSV'), bMid(L2, R2, 'supportsave: all switches'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone audit: unused aliases'), bMid(L2, R2, 'Backup trigger: pre-change'))))
    lines.append(R(merge(bMid(L1, R1, 'SFP inventory: power levels'), bMid(L2, R2, 'Firmware check: ver compare'))))
    lines.append(R(merge(bMid(L1, R1, 'MAPS: alert summary email'), bMid(L2, R2, 'Stale zone cleanup script'))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric topology: PDF report'), bMid(L2, R2, 'Port error daily report'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav VM · REST API port 443 · Brocade FC switches · automation host (Linux/Windows)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('REST API        = SANnav northbound API; JSON over HTTPS port 443'))
    lines.append(txt_row('Token auth      = JWT token issued on login; passed as Bearer in all API requests'))
    lines.append(txt_row('broadcom.sannav = Ansible Galaxy collection for SANnav automation modules'))
    lines.append(txt_row('Zone alias      = named grouping of WWNs used as zone member; managed via API'))
    lines.append(txt_row('cfgshow         = zone config verification; run post-push to confirm zone state'))
    lines.append(txt_row('nsshow          = name server parse; maps WWPN to device names and ports'))
    lines.append(txt_row('supportsave     = automated collection of diagnostic bundle from all switches'))
    lines.append(txt_row('SFP inventory   = REST API retrieves transceiver power levels for predictive alerts'))
    lines.append(txt_row('Stale zone      = zone with an alias that has no active device login; safe to remove'))
    lines.append(txt_row('MAPS summary    = automated email report of MAPS violations above threshold'))
    lines.append(txt_row('WWN             = World Wide Name; 64-bit HBA/port identifier for zone membership'))
    lines.append(txt_row('CSV input       = bulk zone creation from spreadsheet; scripted via REST API batch'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-ops-cli', 'docs/san/brocade/sannav/operations/cli-reference/index.md', 'Brocade SANnav CLI Reference')
def _brocade_sannav_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav management CLI: sannav-admin for system tasks; FOS CLI for fabric operations.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SANnav Admin CLI (VM-side)'), bMid(L2, R2, 'FOS CLI (Switch-side)'))))
    lines.append(R(merge(bMid(L1, R1, 'sannav-admin status: services'), bMid(L2, R2, 'switchshow: port + state'))))
    lines.append(R(merge(bMid(L1, R1, 'sannav-admin backup now'), bMid(L2, R2, 'cfgshow: zone database'))))
    lines.append(R(merge(bMid(L1, R1, 'sannav-admin restart: service'), bMid(L2, R2, 'nsshow: device logins'))))
    lines.append(R(merge(bMid(L1, R1, 'sannav-admin logs: tail -f'), bMid(L2, R2, 'errshow: error log'))))
    lines.append(R(merge(bMid(L1, R1, 'sannav-admin upgrade: initiate'), bMid(L2, R2, 'supportshow: TAC bundle'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('sannav-admin controls the VM appliance; FOS CLI controls individual fabric switches.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'REST API Quick Reference'), bMid(L2, R2, 'Common Troubleshooting CLI'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /api/v1/login → token'), bMid(L2, R2, 'curl /api/v1/health check'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /api/v1/fabric → list'), bMid(L2, R2, 'sannav-admin db-status'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /api/v1/switch/{id}/port'), bMid(L2, R2, 'netstat -tlnp port 443'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /api/v1/zoning/zone'), bMid(L2, R2, 'journalctl -u sannav'))))
    lines.append(R(merge(bMid(L1, R1, 'DELETE /api/v1/zoning/alias'), bMid(L2, R2, 'df -h: check disk space'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav Linux VM · SSH access · REST API port 443 · Brocade FC switch management'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('sannav-admin    = SANnav VM system CLI; manages services, backups, logs, upgrades'))
    lines.append(txt_row('status          = sannav-admin subcommand; shows all SANnav service health'))
    lines.append(txt_row('switchshow      = FOS CLI; primary per-switch port status and fabric state view'))
    lines.append(txt_row('cfgshow         = FOS CLI; displays all zones, aliases, and active zone config'))
    lines.append(txt_row('nsshow          = FOS CLI; Name Server; lists device logins on this switch'))
    lines.append(txt_row('errshow         = FOS CLI; fabric error log with timestamps'))
    lines.append(txt_row('supportshow     = FOS CLI; generates complete diagnostic bundle for TAC'))
    lines.append(txt_row('POST /login     = REST API login; returns JWT token valid for session duration'))
    lines.append(txt_row('journalctl      = systemd log viewer; shows SANnav service stdout/stderr'))
    lines.append(txt_row('db-status       = sannav-admin check; shows PostgreSQL and Elasticsearch health'))
    lines.append(txt_row('REST token      = JWT Bearer token; required header on all subsequent API calls'))
    lines.append(txt_row('curl            = command-line HTTP client; used to test SANnav REST API endpoints'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-sec-auth', 'docs/san/brocade/sannav/security/authentication/index.md', 'Brocade SANnav Authentication')
def _brocade_sannav_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav auth: TACACS+/LDAP for GUI, REST API tokens, MFA via SSO, local fallback.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'GUI Authentication'), bMid(L2, R2, 'API Authentication'))))
    lines.append(R(merge(bMid(L1, R1, 'TACACS+: primary auth method'), bMid(L2, R2, 'POST /api/v1/login → JWT'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP: AD group-to-role map'), bMid(L2, R2, 'Token expiry: configurable'))))
    lines.append(R(merge(bMid(L1, R1, 'SAML 2.0 SSO: IdP-initiated'), bMid(L2, R2, 'HTTPS: TLS 1.2/1.3 required'))))
    lines.append(R(merge(bMid(L1, R1, 'Local: last-resort fallback'), bMid(L2, R2, 'API key: long-lived service'))))
    lines.append(R(merge(bMid(L1, R1, 'Session timeout: 30 min idle'), bMid(L2, R2, 'Rate limiting: brute-force'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('TACACS+/LDAP for human login; JWT tokens for automation; local only as break-glass.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Audit & Session Control'), bMid(L2, R2, 'Switch Auth (via SANnav)'))))
    lines.append(R(merge(bMid(L1, R1, 'All logins logged: user+time'), bMid(L2, R2, 'FOS auth: per-switch creds'))))
    lines.append(R(merge(bMid(L1, R1, 'Failed logins: alert threshold'), bMid(L2, R2, 'SNMPv3: auth + privacy mode'))))
    lines.append(R(merge(bMid(L1, R1, 'Concurrent sessions: limited'), bMid(L2, R2, 'SANnav proxies zone changes'))))
    lines.append(R(merge(bMid(L1, R1, 'Action audit: all GUI changes'), bMid(L2, R2, 'Switch TACACS+ separate cfg'))))
    lines.append(R(merge(bMid(L1, R1, 'Export audit to SIEM/syslog'), bMid(L2, R2, 'Credential vault: HashiCorp'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav VM · TACACS+ server · LDAP/AD · IdP for SAML · Brocade FC switch management'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TACACS+         = Terminal Access Controller; centralized CLI + GUI auth for SANnav'))
    lines.append(txt_row('LDAP            = Lightweight Directory Access Protocol; AD group to SANnav role map'))
    lines.append(txt_row('SAML 2.0        = Security Assertion Markup Language; IdP-initiated SSO for SANnav'))
    lines.append(txt_row('JWT             = JSON Web Token; bearer token returned on REST API login'))
    lines.append(txt_row('API key         = long-lived service account token for non-interactive automation'))
    lines.append(txt_row('Session timeout = idle session expired after 30 minutes by default; configurable'))
    lines.append(txt_row('Rate limiting   = SANnav blocks repeated failed login attempts to prevent brute-force'))
    lines.append(txt_row('Action audit    = every GUI/API change logged with user, timestamp, and action'))
    lines.append(txt_row('SIEM export     = SANnav audit log sent to Splunk/QRadar via syslog/webhook'))
    lines.append(txt_row('SNMPv3          = SNMP v3 auth+privacy used for switch polling from SANnav'))
    lines.append(txt_row('HashiCorp Vault = credential vault; stores SANnav switch passwords for automation'))
    lines.append(txt_row('Break-glass     = local admin account used only when TACACS+ is unreachable'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-sec-enc', 'docs/san/brocade/sannav/security/encryption/index.md', 'Brocade SANnav Encryption')
def _brocade_sannav_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav encryption: TLS 1.2/1.3 for all management traffic; DB and log encryption at rest.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Management Traffic Encryption'), bMid(L2, R2, 'Data at Rest Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'HTTPS: TLS 1.2/1.3 for GUI'), bMid(L2, R2, 'PostgreSQL: encrypted volumes'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API: HTTPS port 443'), bMid(L2, R2, 'OS-level: dm-crypt/LUKS'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMPv3: AES-128 privacy mode'), bMid(L2, R2, 'Log files: filesystem enc'))))
    lines.append(R(merge(bMid(L1, R1, 'syslog: TLS-encrypted forward'), bMid(L2, R2, 'Backup: encrypted NFS files'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable HTTP: redirect to HTTPS'), bMid(L2, R2, 'Audit trail: append-only'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('TLS secures all management channels; disk encryption protects data if VM is extracted.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Management'), bMid(L2, R2, 'Protocol Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Replace default self-signed cert'), bMid(L2, R2, 'Disable TLS 1.0/1.1 + SSL'))))
    lines.append(R(merge(bMid(L1, R1, 'CA-signed cert for prod GUI'), bMid(L2, R2, 'Cipher: AES-GCM preferred'))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate renewal reminder'), bMid(L2, R2, 'HSTS header: enforce HTTPS'))))
    lines.append(R(merge(bMid(L1, R1, 'PKCS#12 import via admin CLI'), bMid(L2, R2, 'Disable weak SNMP strings'))))
    lines.append(R(merge(bMid(L1, R1, 'Annual rotation before expiry'), bMid(L2, R2, 'SSH: key-based admin only'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav Linux VM · vSphere encrypted datastore · PKI CA for cert issuance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TLS 1.3         = Transport Layer Security 1.3; forward secrecy; preferred version'))
    lines.append(txt_row('REST API HTTPS   = all SANnav API calls over port 443; token in Authorization header'))
    lines.append(txt_row('SNMPv3 privacy   = AES-128 encryption of SNMP PDU payload; auth + privacy mode'))
    lines.append(txt_row('dm-crypt/LUKS   = Linux kernel disk encryption; used for SANnav VM data volumes'))
    lines.append(txt_row('PostgreSQL enc   = database files on encrypted volume; prevents offline data access'))
    lines.append(txt_row('Audit trail      = append-only event log; tampering detectable via log integrity check'))
    lines.append(txt_row('PKCS#12         = certificate format; bundles cert + private key for import'))
    lines.append(txt_row('HSTS            = HTTP Strict Transport Security; forces HTTPS for all future requests'))
    lines.append(txt_row('AES-GCM         = AES Galois/Counter Mode; authenticated encryption cipher suite'))
    lines.append(txt_row('Self-signed cert = default SANnav cert; replace with CA-signed cert in production'))
    lines.append(txt_row('CA-signed cert   = TLS certificate issued by internal or public CA; trusted by browsers'))
    lines.append(txt_row('syslog TLS       = encrypted syslog; audit and event logs forwarded securely to SIEM'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-sec-hard', 'docs/san/brocade/sannav/security/hardening/index.md', 'Brocade SANnav Hardening')
def _brocade_sannav_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Security Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav hardening: disable defaults, TACACS+ enforce, TLS, RBAC, patch management.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Platform Hardening'), bMid(L2, R2, 'Access Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Replace default admin password'), bMid(L2, R2, 'TACACS+: no local admin use'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable HTTP; HTTPS only'), bMid(L2, R2, 'RBAC: read-only for ops'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable unused OS services'), bMid(L2, R2, 'API: IP whitelist source IPs'))))
    lines.append(R(merge(bMid(L1, R1, 'OS firewall: port 443 only'), bMid(L2, R2, 'Session timeout: 30 min'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS 1.2+ only; disable older'), bMid(L2, R2, 'MFA via SAML SSO'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Change defaults on day 1; restrict API access; enforce TACACS+ before production use.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Monitoring & Alerting'), bMid(L2, R2, 'Patch & Update Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit log: all actions logged'), bMid(L2, R2, 'Quarterly SANnav upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Failed logins: alert to SIEM'), bMid(L2, R2, 'Check BCM PSIRTs monthly'))))
    lines.append(R(merge(bMid(L1, R1, 'Config changes: diff + alert'), bMid(L2, R2, 'OS patches: monthly cycle'))))
    lines.append(R(merge(bMid(L1, R1, 'API token expiry: 8h default'), bMid(L2, R2, 'Backup before any upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert expiry monitor: 60d warn'), bMid(L2, R2, 'Test in staging first'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav Linux VM · vSphere host · management-only VLAN · TACACS+ server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TLS 1.2+        = minimum required; disable TLS 1.0/1.1 and SSL 3.0'))
    lines.append(txt_row('RBAC            = Role-Based Access Control; operator = read-only; admin = full'))
    lines.append(txt_row('IP whitelist    = restrict SANnav REST API to known source IP ranges'))
    lines.append(txt_row('SAML SSO        = SANnav integrates with IdP; MFA enforced at IdP level'))
    lines.append(txt_row('Session timeout = idle GUI/API session terminated after 30 minutes'))
    lines.append(txt_row('API token expiry= JWT expires after configurable period; 8 hours default'))
    lines.append(txt_row('PSIRT           = Product Security Incident Response; Broadcom security advisories'))
    lines.append(txt_row('Audit log       = all GUI clicks and API calls logged with user and timestamp'))
    lines.append(txt_row('Config diff     = SANnav detects out-of-band zone changes and alerts'))
    lines.append(txt_row('Cert expiry     = TLS certificate monitored; 60-day warning before expiry'))
    lines.append(txt_row('OS patches      = SANnav VM runs Linux; apply OS patches on monthly cycle'))
    lines.append(txt_row('Staging test    = validate SANnav upgrade in non-prod before production rollout'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-trouble-common', 'docs/san/brocade/sannav/troubleshooting/common-issues/index.md', 'Brocade SANnav Common Issues')
def _brocade_sannav_trouble_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Troubleshooting Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common SANnav issues: switch unreachable, zone push fail, auth error, stale data, UI slow.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Switch Connectivity Issues'), bMid(L2, R2, 'Zone Management Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Switch unreachable: ping test'), bMid(L2, R2, 'Zone push fail: FOS auth'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMP poll fail: check creds'), bMid(L2, R2, 'Conflict: out-of-band change'))))
    lines.append(R(merge(bMid(L1, R1, 'Wrong mgmt IP: re-add switch'), bMid(L2, R2, 'Stale zone: re-discover'))))
    lines.append(R(merge(bMid(L1, R1, 'Discovery timeout: increase'), bMid(L2, R2, 'Zone diff: confirm before push'))))
    lines.append(R(merge(bMid(L1, R1, 'FOS version unsupported'), bMid(L2, R2, 'Config lock: cfgdisable first'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Switch connectivity must be verified first; zone failures often trace to FOS auth.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Auth & Login Issues'), bMid(L2, R2, 'Performance & UI Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'TACACS+ timeout: check server'), bMid(L2, R2, 'UI slow: browser cache clear'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP bind fail: verify creds'), bMid(L2, R2, 'Elasticsearch overload: disk'))))
    lines.append(R(merge(bMid(L1, R1, 'Token expired: re-login'), bMid(L2, R2, 'DB size: run prune old data'))))
    lines.append(R(merge(bMid(L1, R1, 'Local fallback: TACACS+ down'), bMid(L2, R2, 'Sannav service: restart'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit log: check failed logins'), bMid(L2, R2, 'Log: journalctl -u sannav'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav VM · management network · TACACS+ server · Brocade FC switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SNMP poll       = SANnav polls switches every 5 minutes; fail = switch shows red'))
    lines.append(txt_row('FOS auth        = SANnav stores per-switch FOS login credentials for zone push'))
    lines.append(txt_row('Out-of-band change= zone change made directly on switch bypassing SANnav'))
    lines.append(txt_row('Config lock     = FOS zone config locked if another session is editing'))
    lines.append(txt_row('Re-discover     = SANnav re-polls switch to refresh stale topology and zone data'))
    lines.append(txt_row('TACACS+ timeout = SANnav login fails if TACACS+ server unreachable; uses local'))
    lines.append(txt_row('LDAP bind       = service account bind to AD; check password expiry'))
    lines.append(txt_row('JWT token       = expires after configured period; re-login to get new token'))
    lines.append(txt_row('Elasticsearch   = performance data store; disk full causes SANnav UI slowness'))
    lines.append(txt_row('Prune old data  = sannav-admin command to remove old perf data and free disk'))
    lines.append(txt_row('journalctl      = Linux systemd log; check for SANnav service errors and restarts'))
    lines.append(txt_row('Config diff     = SANnav compares its zone db to switch; shows out-of-band changes'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-trouble-diag', 'docs/san/brocade/sannav/troubleshooting/diagnostics/index.md', 'Brocade SANnav Diagnostics')
def _brocade_sannav_trouble_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav diagnostics: service logs, DB status, API health, performance data, MAPS review.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SANnav Service Diagnostics'), bMid(L2, R2, 'Database Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'journalctl -u sannav: logs'), bMid(L2, R2, 'sannav-admin db-status'))))
    lines.append(R(merge(bMid(L1, R1, 'sannav-admin status: services'), bMid(L2, R2, 'PostgreSQL: pg_activity'))))
    lines.append(R(merge(bMid(L1, R1, 'curl /api/v1/health: response'), bMid(L2, R2, 'Elasticsearch: cluster health'))))
    lines.append(R(merge(bMid(L1, R1, 'netstat: port 443 listening'), bMid(L2, R2, 'df -h: disk space check'))))
    lines.append(R(merge(bMid(L1, R1, 'top: CPU/RAM on SANnav VM'), bMid(L2, R2, 'du -sh: data dir sizes'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('journalctl and sannav-admin are first-line diagnostics; DB status if data issues.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Switch-Level Diagnostics'), bMid(L2, R2, 'Escalation Data Collection'))))
    lines.append(R(merge(bMid(L1, R1, 'switchshow: verify port state'), bMid(L2, R2, 'Export SANnav logs: GUI'))))
    lines.append(R(merge(bMid(L1, R1, 'errshow: switch error log'), bMid(L2, R2, 'supportsave: each switch'))))
    lines.append(R(merge(bMid(L1, R1, 'fabricshow: fabric topology'), bMid(L2, R2, 'Audit log export: CSV'))))
    lines.append(R(merge(bMid(L1, R1, 'nsshow: device login state'), bMid(L2, R2, 'API debug: verbose logging'))))
    lines.append(R(merge(bMid(L1, R1, 'MAPS: dashboard alerts'), bMid(L2, R2, 'Screenshot: UI issue record'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav VM · vSphere monitoring · Brocade FC switch management ports · NFS backup'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('journalctl      = systemd log viewer; shows SANnav service start/stop and errors'))
    lines.append(txt_row('sannav-admin    = SANnav VM CLI; status/db-status/restart subcommands'))
    lines.append(txt_row('pg_activity     = PostgreSQL active query monitor; identifies slow queries'))
    lines.append(txt_row('Elasticsearch   = analytics DB; cluster health yellow/red = data issues'))
    lines.append(txt_row('/api/v1/health  = SANnav REST health endpoint; returns service status JSON'))
    lines.append(txt_row('df -h           = disk free check; Elasticsearch fills disk causing UI failures'))
    lines.append(txt_row('top             = Linux process monitor; check SANnav CPU/RAM consumption'))
    lines.append(txt_row('switchshow      = FOS CLI first check; verify switch not reporting errors'))
    lines.append(txt_row('errshow         = FOS error log; correlate switch events with SANnav issues'))
    lines.append(txt_row('MAPS dashboard  = SANnav aggregated view of all MAPS alerts across fabric'))
    lines.append(txt_row('supportsave     = FOS diagnostic bundle; required when escalating to Broadcom TAC'))
    lines.append(txt_row('Audit log CSV   = exported SANnav user action log; shared during security review'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('brocade-sannav-trouble-esc', 'docs/san/brocade/sannav/troubleshooting/escalation/index.md', 'Brocade SANnav Escalation')
def _brocade_sannav_trouble_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Brocade SANnav — Troubleshooting Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('SANnav escalation: internal L2/L3 → Broadcom TAC with log bundle, case, and access.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Internal Escalation Path'), bMid(L2, R2, 'Broadcom TAC Escalation'))))
    lines.append(R(merge(bMid(L1, R1, 'L1 → L2: basic checks done'), bMid(L2, R2, 'Open case: support.broadcom'))))
    lines.append(R(merge(bMid(L1, R1, 'L2 → L3: log bundle + timeline'), bMid(L2, R2, 'Provide: SANnav + FOS vers'))))
    lines.append(R(merge(bMid(L1, R1, 'L3 → TAC: full data package'), bMid(L2, R2, 'Sev-1: SANnav unreachable'))))
    lines.append(R(merge(bMid(L1, R1, 'Incident bridge for Sev-1'), bMid(L2, R2, 'Remote: TAC SSH to SANnav'))))
    lines.append(R(merge(bMid(L1, R1, 'No changes during incident'), bMid(L2, R2, 'RCA expected after close'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Collect SANnav logs and switch supportsave before contacting Broadcom TAC.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Data Package'), bMid(L2, R2, 'Severity Classification'))))
    lines.append(R(merge(bMid(L1, R1, 'SANnav logs: journalctl dump'), bMid(L2, R2, 'Sev-1: SANnav down; fabric'))))
    lines.append(R(merge(bMid(L1, R1, 'DB status: sannav-admin out'), bMid(L2, R2, 'Sev-2: zone push failing'))))
    lines.append(R(merge(bMid(L1, R1, 'FOS version per switch'), bMid(L2, R2, 'Sev-3: monitoring partial'))))
    lines.append(R(merge(bMid(L1, R1, 'supportsave from all switches'), bMid(L2, R2, 'Sev-4: question/enhancement'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit log export: CSV'), bMid(L2, R2, 'CSAT survey after closure'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SANnav VM · management Ethernet · serial console access · Broadcom upload endpoint'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('journalctl dump = full SANnav service log export; share compressed to TAC'))
    lines.append(txt_row('sannav-admin    = SANnav VM CLI; db-status and status output needed for TAC'))
    lines.append(txt_row('supportsave     = FOS diagnostic bundle; one per switch in the affected fabric'))
    lines.append(txt_row('Audit log CSV   = SANnav action log export; shows what changed before incident'))
    lines.append(txt_row('Sev-1           = SANnav completely down; fabric management unavailable'))
    lines.append(txt_row('Sev-2           = SANnav partially working; zone changes or discovery failing'))
    lines.append(txt_row('TAC remote      = Broadcom engineer SSHs into SANnav VM with customer permission'))
    lines.append(txt_row('RCA             = Root Cause Analysis document; Broadcom provides after Sev-1 close'))
    lines.append(txt_row('CSAT            = Customer Satisfaction survey; sent by Broadcom after case closure'))
    lines.append(txt_row('FOS version     = Fabric OS version; compatibility matrix needed for SANnav match'))
    lines.append(txt_row('Incident bridge = conference call with all responders during active Sev-1 event'))
    lines.append(txt_row('No changes      = freeze all fabric and SANnav changes during active incident'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-arch', 'docs/san/cisco/cisco-dcnm/architecture/index.md', 'Cisco DCNM Architecture')
def _cisco_dcnm_arch():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2, L3, R3 = 3, 33, 36, 66, 69, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM (Data Center Network Manager): centralised SAN + LAN management for Cisco MDS/Nexus.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'How It Works'), bMid(L2, R2, 'Integrations'), bMid(L3, R3, 'Design Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'OVA/ISO VM appliance'), bMid(L2, R2, 'Cisco ISE: AAA policy'), bMid(L3, R3, 'HA: primary + standby'))))
    lines.append(R(merge(bMid(L1, R1, 'Discovers via SNMP/NETCONF'), bMid(L2, R2, 'SIEM: syslog + SNMP'), bMid(L3, R3, 'Mgmt VLAN isolation'))))
    lines.append(R(merge(bMid(L1, R1, 'SAN zoning + LAN config'), bMid(L2, R2, 'ServiceNow CMDB sync'), bMid(L3, R3, 'RBAC: read/write/admin'))))
    lines.append(R(merge(bMid(L1, R1, 'Topology: VSAN map view'), bMid(L2, R2, 'REST API northbound'), bMid(L3, R3, 'TLS 1.2/1.3 HTTPS'))))
    lines.append(R(merge(bMid(L1, R1, 'Firmware lifecycle mgmt'), bMid(L2, R2, 'Email/SNMP alerting'), bMid(L3, R3, '2 TB storage perf'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('DCNM unifies SAN and LAN fabric management into one platform for Cisco data centers.'))
    lines.append(txt_row())
    lines.append(R(arrow([18, 51, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Managed Resources'), bMid(L2, R2, 'Data Layer'), bMid(L3, R3, 'Management Layer'))))
    lines.append(R(merge(bMid(L1, R1, 'Cisco MDS 9000 FC switches'), bMid(L2, R2, 'PostgreSQL: config DB'), bMid(L3, R3, 'Web GUI: HTTPS'))))
    lines.append(R(merge(bMid(L1, R1, 'Nexus switches (LAN)'), bMid(L2, R2, 'Elastic: perf analytics'), bMid(L3, R3, 'REST/RESTCONF API'))))
    lines.append(R(merge(bMid(L1, R1, 'VSAN zone databases'), bMid(L2, R2, 'Time-series counters'), bMid(L3, R3, 'DCNM CLI admin'))))
    lines.append(R(merge(bMid(L1, R1, 'SFP + HBA inventory'), bMid(L2, R2, 'Config backup store'), bMid(L3, R3, 'TACACS+/RADIUS auth'))))
    lines.append(R(merge(bMid(L1, R1, 'FC zone alias mapping'), bMid(L2, R2, 'Audit event trail'), bMid(L3, R3, 'SNMP trap receiver'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Linux VM on vSphere · management Ethernet · Cisco MDS switch management ports'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM            = Data Center Network Manager; Cisco SAN+LAN management platform'))
    lines.append(txt_row('VSAN            = Virtual SAN; logical FC fabric partition on MDS switches'))
    lines.append(txt_row('OVA             = Open Virtual Appliance; DCNM package for vSphere deployment'))
    lines.append(txt_row('SNMP            = Simple Network Management Protocol; used for device discovery/polling'))
    lines.append(txt_row('NETCONF         = Network Configuration Protocol; XML-based switch configuration'))
    lines.append(txt_row('REST API        = DCNM northbound API; JSON/HTTPS for automation integration'))
    lines.append(txt_row('TACACS+         = centralised CLI and GUI auth; maps roles to DCNM permissions'))
    lines.append(txt_row('ISE             = Cisco Identity Services Engine; AAA policy and RADIUS/TACACS+'))
    lines.append(txt_row('PostgreSQL      = relational DB for DCNM configuration and inventory data'))
    lines.append(txt_row('Elasticsearch   = DCNM analytics DB; stores performance time-series data'))
    lines.append(txt_row('RBAC            = Role-Based Access Control; network-admin/operator/read-only'))
    lines.append(txt_row('SFP inventory   = transceiver data from switch; optical power + type + serial'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-arch-how', 'docs/san/cisco/cisco-dcnm/architecture/how-it-works/index.md', 'Cisco DCNM How It Works')
def _cisco_dcnm_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM discovers via SNMP, manages VSAN zones, pushes NX-OS configs, monitors performance.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Discovery & Polling'), bMid(L2, R2, 'VSAN Zone Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Add switch IP → SNMP v3 poll'), bMid(L2, R2, 'GUI: browse VSAN topology'))))
    lines.append(R(merge(bMid(L1, R1, 'SSH/NETCONF credential auth'), bMid(L2, R2, 'Zone wizard: alias + zone'))))
    lines.append(R(merge(bMid(L1, R1, 'Topology built: domain + ports'), bMid(L2, R2, 'Push zone config to VSAN'))))
    lines.append(R(merge(bMid(L1, R1, 'SFP/HBA inventory per port'), bMid(L2, R2, 'zoneset activate on switch'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMP alerts: event forwarding'), bMid(L2, R2, 'Zone diff: before push view'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('DCNM polls switches for state; zone changes staged and pushed via SSH/NETCONF.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Performance Monitoring'), bMid(L2, R2, 'Firmware Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Port utilisation: 5-min poll'), bMid(L2, R2, 'Upload NX-OS image to DCNM'))))
    lines.append(R(merge(bMid(L1, R1, 'VSAN traffic dashboards'), bMid(L2, R2, 'Install via ISSU per switch'))))
    lines.append(R(merge(bMid(L1, R1, 'Historical: 90-day retention'), bMid(L2, R2, 'Schedule: maintenance window'))))
    lines.append(R(merge(bMid(L1, R1, 'Alerts: email/SNMP threshold'), bMid(L2, R2, 'Verify version post-upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Top ISL bottleneck report'), bMid(L2, R2, 'Rollback: prior image kept'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · management network · Cisco MDS/Nexus switches · NTP for time sync'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VSAN            = Virtual SAN; logical FC fabric on MDS; zones exist per VSAN'))
    lines.append(txt_row('SNMPv3          = polling protocol; DCNM uses for MDS discovery and event alerts'))
    lines.append(txt_row('NETCONF         = XML-based config protocol; DCNM uses for switch configuration push'))
    lines.append(txt_row('Zone wizard     = DCNM GUI workflow for creating FC zones and aliases step-by-step'))
    lines.append(txt_row('zoneset activate= NX-OS command; activates zone set in VSAN; DCNM triggers remotely'))
    lines.append(txt_row('Zone diff       = DCNM shows before/after view of zone changes before pushing'))
    lines.append(txt_row('ISSU            = In-Service Software Upgrade; NX-OS upgrade without traffic disruption'))
    lines.append(txt_row('NX-OS           = Cisco operating system for MDS and Nexus switches'))
    lines.append(txt_row('5-min poll      = default DCNM performance collection interval per port'))
    lines.append(txt_row('90-day retention= default performance history in DCNM Elasticsearch store'))
    lines.append(txt_row('Top bottleneck  = DCNM identifies overutilised ISLs and credit-starved ports'))
    lines.append(txt_row('ISSU rollback   = prior NX-OS image kept on bootflash; used if upgrade fails'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-arch-int', 'docs/san/cisco/cisco-dcnm/architecture/integrations/index.md', 'Cisco DCNM Integrations')
def _cisco_dcnm_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM integrates with Cisco ISE, SIEM, REST automation, CMDB, and NTP/SMTP.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity & Auth Integrations'), bMid(L2, R2, 'Monitoring Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'Cisco ISE: TACACS+/RADIUS'), bMid(L2, R2, 'SNMP trap to NMS (CW/Solarwinds)'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP: AD group-to-role map'), bMid(L2, R2, 'Syslog: SIEM Splunk/QRadar'))))
    lines.append(R(merge(bMid(L1, R1, 'RADIUS: fallback auth method'), bMid(L2, R2, 'Email: SMTP alerting'))))
    lines.append(R(merge(bMid(L1, R1, 'Local accounts: emergency only'), bMid(L2, R2, 'REST webhook: event push'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO: SAML 2.0 via IdP'), bMid(L2, R2, 'Grafana: REST data source'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('ISE provides centralised TACACS+; SIEM integrations forward all events for correlation.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Automation Integrations'), bMid(L2, R2, 'Infrastructure Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API: token + HTTPS'), bMid(L2, R2, 'NTP: time sync for all events'))))
    lines.append(R(merge(bMid(L1, R1, 'Ansible: cisco.dcnm collection'), bMid(L2, R2, 'DNS: switch name resolution'))))
    lines.append(R(merge(bMid(L1, R1, 'Terraform: DCNM provider'), bMid(L2, R2, 'NFS: config backup target'))))
    lines.append(R(merge(bMid(L1, R1, 'ServiceNow: CMDB CI update'), bMid(L2, R2, 'SCP: config archive transfer'))))
    lines.append(R(merge(bMid(L1, R1, 'Python requests library'), bMid(L2, R2, 'vSphere: OVA VM platform'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · management Ethernet · Cisco ISE appliance · NFS backup share'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cisco ISE       = Identity Services Engine; TACACS+ + RADIUS for Cisco devices'))
    lines.append(txt_row('TACACS+         = Terminal Access Controller; centralised CLI + GUI auth for DCNM'))
    lines.append(txt_row('LDAP            = Lightweight Directory Access Protocol; AD group to DCNM role map'))
    lines.append(txt_row('SAML 2.0        = Security Assertion Markup Language; SSO federation for DCNM GUI'))
    lines.append(txt_row('REST API        = DCNM northbound API; JSON/HTTPS with token authentication'))
    lines.append(txt_row('cisco.dcnm      = Ansible Galaxy collection; modules for DCNM automation'))
    lines.append(txt_row('Terraform       = HashiCorp IaC; DCNM provider for zone and VLAN provisioning'))
    lines.append(txt_row('ServiceNow CMDB = CI records for MDS switches auto-synced from DCNM inventory'))
    lines.append(txt_row('SNMP trap       = DCNM forwards MDS health events to NMS (CiscoWorks/SolarWinds)'))
    lines.append(txt_row('Syslog          = DCNM forwards audit and health events to SIEM for correlation'))
    lines.append(txt_row('NFS backup      = DCNM config/DB backup to NFS; scheduled nightly'))
    lines.append(txt_row('NTP             = Network Time Protocol; required for correlated event timestamps'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-arch-design', 'docs/san/cisco/cisco-dcnm/architecture/design-standards/index.md', 'Cisco DCNM Design Standards')
def _cisco_dcnm_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM design: HA deployment, management VLAN, RBAC, TLS, backup, and scale limits.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Deployment Standards'), bMid(L2, R2, 'Security Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'HA pair: primary + standby'), bMid(L2, R2, 'TLS 1.2+ for all HTTPS'))))
    lines.append(R(merge(bMid(L1, R1, 'Dedicated management VLAN'), bMid(L2, R2, 'TACACS+ via ISE mandatory'))))
    lines.append(R(merge(bMid(L1, R1, '8 vCPU / 32 GB RAM (large)'), bMid(L2, R2, 'RBAC: operator = read-only'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP for all timestamps'), bMid(L2, R2, 'SNMPv3 only; disable v1/v2c'))))
    lines.append(R(merge(bMid(L1, R1, 'Dedicated DNS entries mgmt'), bMid(L2, R2, 'IP whitelist API access'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('HA and dedicated management VLAN are baseline; ISE + TLS are security minimums.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Operational Standards'), bMid(L2, R2, 'Scalability Guidelines'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup: nightly NFS; 30-day'), bMid(L2, R2, 'Max 2,000 switches / node'))))
    lines.append(R(merge(bMid(L1, R1, 'Alert review: daily SNMP check'), bMid(L2, R2, 'Max 200,000 ports / node'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone changes: change ticket'), bMid(L2, R2, 'Separate SAN vs LAN domain'))))
    lines.append(R(merge(bMid(L1, R1, 'Firmware via DCNM only'), bMid(L2, R2, 'Scale-out: multi-cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'Quarterly DCNM upgrade'), bMid(L2, R2, '2 TB storage perf history'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere host · 2 TB datastore · management Ethernet · NFS backup share'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('HA pair         = DCNM primary + standby VMs; database replication between them'))
    lines.append(txt_row('Management VLAN = isolated VLAN for OOB switch management and DCNM traffic'))
    lines.append(txt_row('ISE             = Cisco Identity Services Engine; provides TACACS+ for DCNM'))
    lines.append(txt_row('TLS 1.2+        = minimum TLS version for DCNM HTTPS GUI and REST API'))
    lines.append(txt_row('RBAC            = Role-Based Access Control; network-admin/operator/read-only'))
    lines.append(txt_row('SNMPv3          = SNMP version 3; auth + privacy mode; disable v1/v2c in DCNM'))
    lines.append(txt_row('IP whitelist    = restrict REST API source IPs to automation host subnet'))
    lines.append(txt_row('NFS backup      = nightly DCNM config and database export to NFS mount'))
    lines.append(txt_row('2,000 switches  = Cisco-recommended maximum MDS/Nexus per DCNM instance'))
    lines.append(txt_row('SAN vs LAN      = DCNM manages both; separate logical domains per best practice'))
    lines.append(txt_row('Multi-cluster   = multiple DCNM instances federated; each manages a subset'))
    lines.append(txt_row('Change ticket   = ITSM requirement; all zone and config changes pre-approved'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-ops-procedures', 'docs/san/cisco/cisco-dcnm/operations/procedures/index.md', 'Cisco DCNM Operations Procedures')
def _cisco_dcnm_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Operations Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM day-2 procedures: zone changes, switch adds, firmware upgrades, health monitoring.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Zone Change Procedure'), bMid(L2, R2, 'Switch Add / Remove'))))
    lines.append(R(merge(bMid(L1, R1, '1. Create device alias (WWN)'), bMid(L2, R2, '1. Add switch IP in DCNM'))))
    lines.append(R(merge(bMid(L1, R1, '2. Create zone with aliases'), bMid(L2, R2, '2. Set SNMPv3 credentials'))))
    lines.append(R(merge(bMid(L1, R1, '3. Add zone to zone set'), bMid(L2, R2, '3. Discover: verify VSAN'))))
    lines.append(R(merge(bMid(L1, R1, '4. Review zone diff in DCNM'), bMid(L2, R2, '4. Set SNMP threshold rules'))))
    lines.append(R(merge(bMid(L1, R1, '5. Activate zone set in VSAN'), bMid(L2, R2, '5. Verify NX-OS version'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Zone set activation requires change ticket; always review diff before activation.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Firmware Management'), bMid(L2, R2, 'Health Monitoring Routine'))))
    lines.append(R(merge(bMid(L1, R1, '1. Upload NX-OS to DCNM repo'), bMid(L2, R2, 'Daily: SNMP alert review'))))
    lines.append(R(merge(bMid(L1, R1, '2. Validate compatibility'), bMid(L2, R2, 'Weekly: port error report'))))
    lines.append(R(merge(bMid(L1, R1, '3. ISSU upgrade via DCNM'), bMid(L2, R2, 'Monthly: ISL utilisation'))))
    lines.append(R(merge(bMid(L1, R1, '4. Verify via show version'), bMid(L2, R2, 'Quarterly: zone set audit'))))
    lines.append(R(merge(bMid(L1, R1, '5. Post-upgrade traffic test'), bMid(L2, R2, 'Annual: DCNM upgrade'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · management network · Cisco MDS switch chassis · SFP transceivers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Device alias    = named mapping for WWN in VSAN; used as zone member instead of raw WWN'))
    lines.append(txt_row('Zone set        = collection of zones applied to a VSAN; only one active at a time'))
    lines.append(txt_row('Zone diff       = DCNM shows before/after comparison before activating zone set'))
    lines.append(txt_row('zoneset activate= NX-OS command; activates zone set in VSAN; DCNM triggers remotely'))
    lines.append(txt_row('ISSU            = In-Service Software Upgrade; NX-OS upgrade without traffic disruption'))
    lines.append(txt_row('SNMPv3          = SNMP v3 credentials required for DCNM switch discovery and polling'))
    lines.append(txt_row('VSAN            = Virtual SAN; logical FC fabric partition; zones are per-VSAN'))
    lines.append(txt_row('Port error report= weekly DCNM report on CRC/discard/loss-of-sync per port'))
    lines.append(txt_row('Zone set audit  = quarterly review of all zones for stale aliases and orphaned WWNs'))
    lines.append(txt_row('Change ticket   = ITSM approval required before zone activation or firmware upgrade'))
    lines.append(txt_row('ISL utilisation = monthly DCNM ISL throughput trend; > 70% = add more ISLs'))
    lines.append(txt_row('NX-OS repo      = DCNM internal firmware storage; images staged before upgrade'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-ops-backup', 'docs/san/cisco/cisco-dcnm/operations/backup-restore/index.md', 'Cisco DCNM Backup Restore')
def _cisco_dcnm_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Backup and Restore'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM backup covers the config DB, zone snapshots, NX-OS configs, and topology data.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DCNM Platform Backup'), bMid(L2, R2, 'Switch Config Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'Nightly: NFS destination'), bMid(L2, R2, 'copy run startup on MDS'))))
    lines.append(R(merge(bMid(L1, R1, 'Includes: DB + topology data'), bMid(L2, R2, 'DCNM: archive config per sw'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: DCNM Admin → Backup'), bMid(L2, R2, 'Pre-change zone snapshot'))))
    lines.append(R(merge(bMid(L1, R1, 'Retention: 30 days min'), bMid(L2, R2, 'Export zone set: text file'))))
    lines.append(R(merge(bMid(L1, R1, 'Test restore quarterly'), bMid(L2, R2, 'SCP to central backup store'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('DCNM DB backup and switch zone snapshots are both required for full recovery.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DCNM Restore Procedure'), bMid(L2, R2, 'Switch Config Restore'))))
    lines.append(R(merge(bMid(L1, R1, '1. Deploy fresh DCNM OVA'), bMid(L2, R2, 'copy tftp: startup-config'))))
    lines.append(R(merge(bMid(L1, R1, '2. Restore DB from NFS backup'), bMid(L2, R2, 'Restore zone: import file'))))
    lines.append(R(merge(bMid(L1, R1, '3. Verify switch discovery'), bMid(L2, R2, 'zoneset activate in VSAN'))))
    lines.append(R(merge(bMid(L1, R1, '4. Re-validate ISE auth'), bMid(L2, R2, 'Verify: show zoneset active'))))
    lines.append(R(merge(bMid(L1, R1, '5. Test alert forwarding'), bMid(L2, R2, 'Test: host I/O after restore'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · NFS backup server · Cisco MDS switch chassis · vSphere host'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('NFS backup      = DCNM configuration and DB exported to NFS mount point'))
    lines.append(txt_row('copy run startup= NX-OS command; saves running config to startup-config (NVRAM)'))
    lines.append(txt_row('DCNM archive    = per-switch config archive stored in DCNM; viewable in GUI'))
    lines.append(txt_row('Zone snapshot   = show zoneset active output saved before any zone change'))
    lines.append(txt_row('Zone set export = zone set saved to text file for offline backup and audit'))
    lines.append(txt_row('SCP             = Secure Copy; transfer config archives to central backup server'))
    lines.append(txt_row('DCNM OVA        = fresh DCNM VM from Cisco-provided OVA; base for restore'))
    lines.append(txt_row('copy tftp       = NX-OS; copies startup-config from TFTP server for restore'))
    lines.append(txt_row('zoneset activate= NX-OS command; applies restored zone set to VSAN'))
    lines.append(txt_row('show zoneset    = verifies zone set is active and matches expected configuration'))
    lines.append(txt_row('Retention 30d   = keep 30 days of DCNM backups; prune older ones to save storage'))
    lines.append(txt_row('Restore test    = quarterly test of full DCNM restore to validate backup integrity'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-ops-health', 'docs/san/cisco/cisco-dcnm/operations/health-checks/index.md', 'Cisco DCNM Health Checks')
def _cisco_dcnm_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM health checks: dashboard alerts, switch status, ISL load, zone consistency.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DCNM Dashboard Health'), bMid(L2, R2, 'Switch-Level Health'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMP alerts: active by severity'), bMid(L2, R2, 'show system health: all OK'))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric topology: no split VSAN'), bMid(L2, R2, 'show environment: temp/PSU'))))
    lines.append(R(merge(bMid(L1, R1, 'Port inventory: no offline'), bMid(L2, R2, 'show interface: no errors'))))
    lines.append(R(merge(bMid(L1, R1, 'NX-OS currency: < 2 versions'), bMid(L2, R2, 'show version: verify build'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone set: saved == active'), bMid(L2, R2, 'show flogi database: logins'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('DCNM dashboard and MDS show commands are first-line health checks; run daily.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ISL & VSAN Health'), bMid(L2, R2, 'DCNM Platform Health'))))
    lines.append(R(merge(bMid(L1, R1, 'show interface trunk: ISL util'), bMid(L2, R2, 'DCNM services: all running'))))
    lines.append(R(merge(bMid(L1, R1, 'ISL > 70% util: add more'), bMid(L2, R2, 'DB: disk usage < 80%'))))
    lines.append(R(merge(bMid(L1, R1, 'show vsan: all active'), bMid(L2, R2, 'HA sync: primary = standby'))))
    lines.append(R(merge(bMid(L1, R1, 'Credit starvation: pause check'), bMid(L2, R2, 'Backup: last job success'))))
    lines.append(R(merge(bMid(L1, R1, 'Port error rate < 10/day'), bMid(L2, R2, 'Cert expiry > 60 days left'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Cisco MDS switch chassis · SFP transceivers · ISL FC cables · DCNM VM resources'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('show system health= MDS NX-OS command; reports module and fabric health status'))
    lines.append(txt_row('show environment = MDS NX-OS; shows temperature, fan, and PSU sensor readings'))
    lines.append(txt_row('show flogi database= FC login database; verifies all HBAs are logged into fabric'))
    lines.append(txt_row('show vsan        = VSAN state; confirms all VSANs are active and not suspended'))
    lines.append(txt_row('show interface trunk= ISL trunk status and utilisation counters'))
    lines.append(txt_row('Credit starvation= FC flow control issue; BB credits exhausted; causes pause'))
    lines.append(txt_row('Zone set saved   = saved zone database should match active; divergence = risk'))
    lines.append(txt_row('DCNM HA sync    = primary and standby DCNM databases must be synchronised'))
    lines.append(txt_row('Cert expiry      = TLS certificate monitored; alert 60 days before expiry'))
    lines.append(txt_row('NX-OS currency   = keep MDS within 2 major versions of latest supported release'))
    lines.append(txt_row('Backup status    = nightly DCNM backup job result; alert on failure'))
    lines.append(txt_row('VSAN split       = VSAN partition causing isolation; major incident requiring fix'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-ops-install', 'docs/san/cisco/cisco-dcnm/operations/install-upgrade/index.md', 'Cisco DCNM Install Upgrade')
def _cisco_dcnm_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM deployment: OVA/ISO to vSphere, initial config, switch discovery, upgrade path.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fresh Install Steps'), bMid(L2, R2, 'Initial Configuration'))))
    lines.append(R(merge(bMid(L1, R1, '1. Download DCNM OVA from CCO'), bMid(L2, R2, '1. Set hostname + IP + DNS'))))
    lines.append(R(merge(bMid(L1, R1, '2. Deploy OVA in vSphere'), bMid(L2, R2, '2. Configure NTP servers'))))
    lines.append(R(merge(bMid(L1, R1, '3. Boot + initial config wizard'), bMid(L2, R2, '3. Set admin credentials'))))
    lines.append(R(merge(bMid(L1, R1, '4. 8 vCPU / 32 GB RAM (large)'), bMid(L2, R2, '4. Configure ISE TACACS+'))))
    lines.append(R(merge(bMid(L1, R1, '5. 2 TB datastore for perf'), bMid(L2, R2, '5. Discover MDS switches'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('OVA deployment is automated; ISE and NTP must be configured before adding switches.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Procedure'), bMid(L2, R2, 'Post-Upgrade Validation'))))
    lines.append(R(merge(bMid(L1, R1, '1. Backup DCNM DB to NFS'), bMid(L2, R2, '1. Verify all switches shown'))))
    lines.append(R(merge(bMid(L1, R1, '2. Download new DCNM OVA'), bMid(L2, R2, '2. Check SNMP alert forward'))))
    lines.append(R(merge(bMid(L1, R1, '3. Deploy standby; restore DB'), bMid(L2, R2, '3. Re-test ISE TACACS+ auth'))))
    lines.append(R(merge(bMid(L1, R1, '4. Validate standby function'), bMid(L2, R2, '4. Verify NFS backup schedule'))))
    lines.append(R(merge(bMid(L1, R1, '5. Swing DNS; decom old VM'), bMid(L2, R2, '5. Confirm zone push works'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere host · 2 TB datastore · management network · NFS backup share'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CCO             = Cisco Connection Online; software download portal (software.cisco.com)'))
    lines.append(txt_row('OVA             = Open Virtual Appliance; DCNM packaged as vSphere-ready VM template'))
    lines.append(txt_row('Config wizard   = DCNM first-boot setup; sets IP, NTP, credentials interactively'))
    lines.append(txt_row('ISE             = Cisco Identity Services Engine; provides TACACS+ for DCNM auth'))
    lines.append(txt_row('NFS backup      = nightly DCNM DB backup; required before any upgrade'))
    lines.append(txt_row('Swing DNS       = update DNS A record to new DCNM VM IP after validation'))
    lines.append(txt_row('Standby upgrade = deploy new DCNM version as standby first; validate then swing'))
    lines.append(txt_row('SNMP forwarding = DCNM forwards switch alerts to NMS; test after every upgrade'))
    lines.append(txt_row('Zone push test  = verify DCNM can activate zone set on MDS switch after upgrade'))
    lines.append(txt_row('vCPU / RAM      = DCNM large mode: 8 vCPU / 32 GB; medium: 4 vCPU / 16 GB'))
    lines.append(txt_row('2 TB datastore  = DCNM storage for 90-day performance data; Elasticsearch store'))
    lines.append(txt_row('NTP             = Network Time Protocol; timestamps required for event correlation'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-ops-scripts', 'docs/san/cisco/cisco-dcnm/operations/scripts/index.md', 'Cisco DCNM Operations Scripts')
def _cisco_dcnm_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Operations Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM scripting: REST API, Ansible cisco.dcnm, zone automation, reporting scripts.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'REST API Scripting'), bMid(L2, R2, 'Zone Automation'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /rest/logon → token'), bMid(L2, R2, 'Ansible: cisco.dcnm.dcnm_zone'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /rest/san/fabric list'), bMid(L2, R2, 'Python: create alias + zone'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /rest/san/zone/{fabric}'), bMid(L2, R2, 'Batch zone from CSV input'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /rest/san/zone create'), bMid(L2, R2, 'Validate: show zone active'))))
    lines.append(R(merge(bMid(L1, R1, 'DELETE /rest/san/zone cleanup'), bMid(L2, R2, 'WWN lookup: show flogi parse'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('cisco.dcnm Ansible collection wraps REST API; Python scripts for batch operations.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Reporting Scripts'), bMid(L2, R2, 'Maintenance Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Port utilisation: weekly CSV'), bMid(L2, R2, 'Config archive: all switches'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone audit: stale aliases'), bMid(L2, R2, 'Backup trigger: pre-change'))))
    lines.append(R(merge(bMid(L1, R1, 'SFP inventory: power levels'), bMid(L2, R2, 'NX-OS check: ver compare'))))
    lines.append(R(merge(bMid(L1, R1, 'Alert summary: email weekly'), bMid(L2, R2, 'Stale zone cleanup script'))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric topology: inventory'), bMid(L2, R2, 'Port error daily report'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · REST API port 443 · Cisco MDS switches · automation host'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('REST API        = DCNM northbound API; JSON/HTTPS; token returned on /rest/logon'))
    lines.append(txt_row('cisco.dcnm      = Ansible Galaxy collection; dcnm_zone, dcnm_vsan modules'))
    lines.append(txt_row('dcnm_zone       = Ansible module; create, delete, and activate DCNM zones'))
    lines.append(txt_row('show zone active= NX-OS command; verifies zone set is active in VSAN'))
    lines.append(txt_row('show flogi database= NX-OS; maps WWPNs to fabric login; used for alias lookup'))
    lines.append(txt_row('CSV input       = bulk zone creation from spreadsheet; Python REST API batch'))
    lines.append(txt_row('Stale alias     = alias with WWN that has no active fabric login; safe to prune'))
    lines.append(txt_row('Config archive  = DCNM-stored switch config; scripted retrieval for CMDB'))
    lines.append(txt_row('SFP inventory   = REST API retrieves transceiver power levels for all ports'))
    lines.append(txt_row('Alert summary   = weekly email report of DCNM SNMP threshold violations'))
    lines.append(txt_row('NX-OS check     = script compares running NX-OS version against approved baseline'))
    lines.append(txt_row('Token           = JWT Bearer token; required Authorization header on all API calls'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-ops-cli', 'docs/san/cisco/cisco-dcnm/operations/cli-reference/index.md', 'Cisco DCNM CLI Reference')
def _cisco_dcnm_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM management CLI and key NX-OS MDS commands for fabric operations and troubleshooting.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DCNM Admin CLI'), bMid(L2, R2, 'NX-OS MDS SAN Commands'))))
    lines.append(R(merge(bMid(L1, R1, 'appmgr status: service check'), bMid(L2, R2, 'show flogi database'))))
    lines.append(R(merge(bMid(L1, R1, 'appmgr backup: trigger backup'), bMid(L2, R2, 'show zoneset active'))))
    lines.append(R(merge(bMid(L1, R1, 'appmgr stop/start dcnm'), bMid(L2, R2, 'show vsan: VSAN state'))))
    lines.append(R(merge(bMid(L1, R1, 'dcnm_root passwd change'), bMid(L2, R2, 'show interface fc: errors'))))
    lines.append(R(merge(bMid(L1, R1, 'tail -f /var/log/dcnm/...'), bMid(L2, R2, 'show port-channel: ISL'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('appmgr manages DCNM services; NX-OS MDS CLI verifies switch-level fabric state.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'REST API Quick Reference'), bMid(L2, R2, 'Common Troubleshooting CLI'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /rest/logon → token'), bMid(L2, R2, 'curl /rest/health'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /rest/san/fabric'), bMid(L2, R2, 'appmgr status all'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /rest/san/zone/{fabric}'), bMid(L2, R2, 'netstat -tlnp 443'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /rest/san/zone/deploy'), bMid(L2, R2, 'df -h: disk usage'))))
    lines.append(R(merge(bMid(L1, R1, 'DELETE /rest/san/zone/{id}'), bMid(L2, R2, 'show tech-support: TAC'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM Linux VM · SSH access · REST API port 443 · Cisco MDS management Ethernet'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('appmgr          = DCNM VM management CLI; controls service lifecycle and backups'))
    lines.append(txt_row('show flogi database= NX-OS; shows all FC logins; confirms HBA access to fabric'))
    lines.append(txt_row('show zoneset active= NX-OS; shows active zone set members in each VSAN'))
    lines.append(txt_row('show vsan        = NX-OS; VSAN state; all should be active'))
    lines.append(txt_row('show interface fc= NX-OS; per-port FC counters: errors, throughput, credits'))
    lines.append(txt_row('show port-channel= NX-OS; ISL port-channel (PortChannel) status and members'))
    lines.append(txt_row('/rest/logon      = DCNM REST auth endpoint; POST credentials; returns JWT token'))
    lines.append(txt_row('/rest/san/fabric = DCNM REST; lists all managed SAN fabrics'))
    lines.append(txt_row('/rest/san/zone/deploy= DCNM REST; triggers zone set activation in VSAN'))
    lines.append(txt_row('show tech-support= NX-OS MDS full diagnostic bundle; send to Cisco TAC'))
    lines.append(txt_row('df -h            = Linux disk free; check DCNM disk for Elasticsearch fill'))
    lines.append(txt_row('netstat -tlnp    = verify DCNM port 443 is listening; basic health check'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-ops-common', 'docs/san/cisco/cisco-dcnm/operations/common-issues/index.md', 'Cisco DCNM Common Issues')
def _cisco_dcnm_ops_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Common Operational Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common DCNM issues: switch unreachable, zone push fail, auth error, stale data, UI slow.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Switch Connectivity Issues'), bMid(L2, R2, 'Zone Management Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Switch unreachable: ping test'), bMid(L2, R2, 'Zone push fail: NX-OS creds'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMP v3 poll timeout: creds'), bMid(L2, R2, 'Conflict: out-of-band change'))))
    lines.append(R(merge(bMid(L1, R1, 'Discovery timeout: re-add sw'), bMid(L2, R2, 'Zone diff stale: re-discover'))))
    lines.append(R(merge(bMid(L1, R1, 'NX-OS version unsupported'), bMid(L2, R2, 'Zone lock: active edit session'))))
    lines.append(R(merge(bMid(L1, R1, 'IP change on switch: update'), bMid(L2, R2, 'VSAN mismatch: verify both'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Switch connectivity verified first; zone failures trace to NX-OS credentials or VSAN.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Auth & Login Issues'), bMid(L2, R2, 'Performance & DB Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'ISE TACACS+ timeout check'), bMid(L2, R2, 'UI slow: clear browser cache'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP bind fail: service acct'), bMid(L2, R2, 'Elasticsearch disk full'))))
    lines.append(R(merge(bMid(L1, R1, 'Token expired: re-login'), bMid(L2, R2, 'Run DB prune via appmgr'))))
    lines.append(R(merge(bMid(L1, R1, 'Local fallback: ISE unreachable'), bMid(L2, R2, 'appmgr restart: DCNM'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit log: check failed logins'), bMid(L2, R2, 'journalctl for service err'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · management network · Cisco ISE · Cisco MDS switch management ports'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SNMPv3 poll     = DCNM polls switches every 5 minutes; timeout = switch shows red'))
    lines.append(txt_row('NX-OS creds     = DCNM stores per-switch SSH credentials for zone push'))
    lines.append(txt_row('Out-of-band     = zone change made directly on MDS bypassing DCNM; causes conflict'))
    lines.append(txt_row('Zone lock       = NX-OS zone lock when another session is editing; resolve first'))
    lines.append(txt_row('Re-discover     = DCNM re-polls switch to refresh stale topology and zone data'))
    lines.append(txt_row('VSAN mismatch   = zone pushed to wrong VSAN; verify VSAN ID on both ends'))
    lines.append(txt_row('ISE TACACS+     = Cisco ISE provides DCNM TACACS+ auth; timeout = login failure'))
    lines.append(txt_row('LDAP bind       = DCNM AD integration service account; check password expiry'))
    lines.append(txt_row('Elasticsearch   = DCNM performance data store; disk full causes UI performance issues'))
    lines.append(txt_row('appmgr          = DCNM VM CLI; restart/status/prune subcommands'))
    lines.append(txt_row('journalctl      = Linux systemd log; shows DCNM service restart and error events'))
    lines.append(txt_row('Zone stale      = DCNM zone database out of sync with switch; re-discover to fix'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-sec-access', 'docs/san/cisco/cisco-dcnm/security/access-control/index.md', 'Cisco DCNM Access Control')
def _cisco_dcnm_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM access control: RBAC roles, ISE TACACS+, LDAP group mapping, API token scoping.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'User Accounts & RBAC'), bMid(L2, R2, 'Remote Auth (ISE/TACACS+)'))))
    lines.append(R(merge(bMid(L1, R1, 'Built-in: network-admin/oper'), bMid(L2, R2, 'Cisco ISE TACACS+ server'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom roles via role config'), bMid(L2, R2, 'Role map: privilege level'))))
    lines.append(R(merge(bMid(L1, R1, 'Local accounts: emergency only'), bMid(L2, R2, 'RADIUS: fallback option'))))
    lines.append(R(merge(bMid(L1, R1, 'Account lockout: 5 attempts'), bMid(L2, R2, 'Auth order: TACACS+ first'))))
    lines.append(R(merge(bMid(L1, R1, 'Per-fabric access restriction'), bMid(L2, R2, 'Audit: all actions logged'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('RBAC and ISE TACACS+ enforce least privilege; local accounts reserved for break-glass.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'API Access Control'), bMid(L2, R2, 'Management Access Control'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API: token scoped role'), bMid(L2, R2, 'HTTPS only: port 443'))))
    lines.append(R(merge(bMid(L1, R1, 'API key: service account'), bMid(L2, R2, 'IP whitelist: src restrict'))))
    lines.append(R(merge(bMid(L1, R1, 'Token expiry: configurable'), bMid(L2, R2, 'Session timeout: 30 min'))))
    lines.append(R(merge(bMid(L1, R1, 'Rate limiting: brute-force'), bMid(L2, R2, 'Out-of-band: mgmt VLAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Scope: read vs read-write'), bMid(L2, R2, 'MFA: SAML SSO enforced'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · Cisco ISE appliance · LDAP/AD server · management VLAN'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC            = Role-Based Access Control; network-admin/operator/read-only in DCNM'))
    lines.append(txt_row('ISE             = Cisco Identity Services Engine; TACACS+ and RADIUS provider'))
    lines.append(txt_row('TACACS+         = Terminal Access Controller; centralised CLI+GUI auth with audit'))
    lines.append(txt_row('Privilege level = TACACS+ maps to DCNM role (15=admin, 5=operator, 1=read-only)'))
    lines.append(txt_row('Auth order      = DCNM tries TACACS+ first, then RADIUS, then local fallback'))
    lines.append(txt_row('Per-fabric RBAC = restrict operators to specific SAN fabrics; not all'))
    lines.append(txt_row('API token       = JWT; inherits role permissions of the user who logged in'))
    lines.append(txt_row('Service account = dedicated API user; separate from human admin accounts'))
    lines.append(txt_row('IP whitelist    = source IP restriction for DCNM management and REST API access'))
    lines.append(txt_row('Session timeout = idle GUI/API session terminated after 30 minutes'))
    lines.append(txt_row('SAML SSO        = DCNM integrates with IdP; MFA enforced at identity provider'))
    lines.append(txt_row('Audit log       = all DCNM GUI and API actions logged with user and timestamp'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-sec-auth', 'docs/san/cisco/cisco-dcnm/security/authentication/index.md', 'Cisco DCNM Authentication')
def _cisco_dcnm_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM auth: ISE TACACS+ for GUI, REST JWT, SAML SSO, local accounts as break-glass.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'GUI Authentication'), bMid(L2, R2, 'API Authentication'))))
    lines.append(R(merge(bMid(L1, R1, 'ISE TACACS+: primary method'), bMid(L2, R2, 'POST /rest/logon → JWT'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP: AD group-to-role map'), bMid(L2, R2, 'Token expiry: 8h default'))))
    lines.append(R(merge(bMid(L1, R1, 'SAML 2.0 SSO: IdP-federated'), bMid(L2, R2, 'HTTPS: TLS 1.2/1.3 only'))))
    lines.append(R(merge(bMid(L1, R1, 'Local: break-glass only'), bMid(L2, R2, 'Service acct: API key'))))
    lines.append(R(merge(bMid(L1, R1, 'Lockout: 5 failed attempts'), bMid(L2, R2, 'Rate limit: brute-force'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('ISE TACACS+ for human GUI login; JWT for automation; SAML SSO integrates MFA.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Session & Audit Control'), bMid(L2, R2, 'Switch Auth (DCNM-side)'))))
    lines.append(R(merge(bMid(L1, R1, 'All logins: user + timestamp'), bMid(L2, R2, 'SSH creds stored per switch'))))
    lines.append(R(merge(bMid(L1, R1, 'Failed logins: alert to SIEM'), bMid(L2, R2, 'NX-OS TACACS+ separate'))))
    lines.append(R(merge(bMid(L1, R1, 'Concurrent sessions: limited'), bMid(L2, R2, 'Credential vault: HashiCorp'))))
    lines.append(R(merge(bMid(L1, R1, 'Action audit: all changes'), bMid(L2, R2, 'SNMPv3: auth + privacy'))))
    lines.append(R(merge(bMid(L1, R1, 'Export audit: syslog / CSV'), bMid(L2, R2, 'Rotation: quarterly creds'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · Cisco ISE · LDAP/AD · IdP for SAML · Cisco MDS switch management'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ISE TACACS+     = Cisco ISE provides TACACS+ protocol; maps to DCNM role'))
    lines.append(txt_row('LDAP            = AD group-to-DCNM role mapping via LDAP bind'))
    lines.append(txt_row('SAML 2.0        = SSO federation; MFA enforced at identity provider level'))
    lines.append(txt_row('JWT             = JSON Web Token; bearer token returned on /rest/logon'))
    lines.append(txt_row('Service account = dedicated API user; separate credentials for automation'))
    lines.append(txt_row('Lockout         = DCNM locks account after 5 failed logins; unlock via admin'))
    lines.append(txt_row('Rate limiting   = blocks repeated failed attempts to prevent brute-force'))
    lines.append(txt_row('Session timeout = idle GUI/API session terminated after configurable period'))
    lines.append(txt_row('Action audit    = all DCNM GUI clicks and API calls logged with user/timestamp'))
    lines.append(txt_row('NX-OS TACACS+   = MDS switch CLI authentication via ISE; separate from DCNM'))
    lines.append(txt_row('HashiCorp Vault = credential vault; stores DCNM switch passwords for automation'))
    lines.append(txt_row('SNMPv3 auth     = SNMP v3 authentication (SHA); privacy (AES) for polling'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-sec-enc', 'docs/san/cisco/cisco-dcnm/security/encryption/index.md', 'Cisco DCNM Encryption')
def _cisco_dcnm_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM encryption: TLS 1.2/1.3 management, SNMPv3 privacy, OS disk encryption at rest.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Management Traffic Encryption'), bMid(L2, R2, 'Data at Rest Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'HTTPS: TLS 1.2/1.3 GUI/API'), bMid(L2, R2, 'OS-level: LUKS/dm-crypt'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API: HTTPS port 443'), bMid(L2, R2, 'PostgreSQL on enc volume'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMPv3: AES-128 privacy mode'), bMid(L2, R2, 'Elasticsearch on enc vol'))))
    lines.append(R(merge(bMid(L1, R1, 'syslog: TLS encrypted forward'), bMid(L2, R2, 'Backup: encrypted at NFS'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable HTTP; HTTPS redirect'), bMid(L2, R2, 'Audit trail: append-only'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('TLS on all management channels; LUKS disk encryption protects data at rest.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Management'), bMid(L2, R2, 'Protocol Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Replace self-signed cert day 1'), bMid(L2, R2, 'Disable TLS 1.0/1.1 SSL'))))
    lines.append(R(merge(bMid(L1, R1, 'CA-signed cert: production'), bMid(L2, R2, 'Cipher: AES-GCM preferred'))))
    lines.append(R(merge(bMid(L1, R1, 'PKCS#12 import via admin CLI'), bMid(L2, R2, 'HSTS: enforce HTTPS'))))
    lines.append(R(merge(bMid(L1, R1, 'Monitor expiry: 60-day warn'), bMid(L2, R2, 'Disable v1/v2c SNMP'))))
    lines.append(R(merge(bMid(L1, R1, 'Annual renewal: update cert'), bMid(L2, R2, 'SSH key-based: admin only'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM Linux VM · vSphere encrypted datastore · PKI CA for certificate issuance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TLS 1.3         = Transport Layer Security 1.3; forward secrecy; preferred version'))
    lines.append(txt_row('SNMPv3 privacy  = AES-128 encryption of SNMP PDU payload; auth + privacy mode'))
    lines.append(txt_row('LUKS            = Linux Unified Key Setup; full-disk encryption for DCNM VM volumes'))
    lines.append(txt_row('dm-crypt        = Linux kernel disk encryption subsystem; LUKS uses dm-crypt'))
    lines.append(txt_row('PostgreSQL enc  = DCNM config DB on encrypted volume; offline access blocked'))
    lines.append(txt_row('Elasticsearch enc= performance DB on encrypted volume; data protected at rest'))
    lines.append(txt_row('Audit trail     = append-only log; integrity verifiable; used for forensics'))
    lines.append(txt_row('PKCS#12         = certificate container format; bundles cert + private key'))
    lines.append(txt_row('HSTS            = HTTP Strict Transport Security; browser forces HTTPS always'))
    lines.append(txt_row('AES-GCM         = AES Galois Counter Mode; authenticated encryption cipher suite'))
    lines.append(txt_row('CA-signed cert  = TLS cert from internal or public CA; replace self-signed in prod'))
    lines.append(txt_row('syslog TLS      = encrypted syslog forwarding; audit events protected in transit'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-sec-hard', 'docs/san/cisco/cisco-dcnm/security/hardening/index.md', 'Cisco DCNM Hardening')
def _cisco_dcnm_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Security Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM hardening: disable defaults, enforce ISE TACACS+, TLS, RBAC, patch management.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Platform Hardening'), bMid(L2, R2, 'Access Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Change default admin password'), bMid(L2, R2, 'ISE TACACS+: no local use'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable HTTP; HTTPS only'), bMid(L2, R2, 'RBAC: operator read-only'))))
    lines.append(R(merge(bMid(L1, R1, 'Firewall: port 443 only'), bMid(L2, R2, 'API IP whitelist: restrict'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS 1.2+ only; disable older'), bMid(L2, R2, 'Session timeout: 30 min'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable unused OS services'), bMid(L2, R2, 'MFA via SAML SSO'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Change defaults day 1; restrict API; enforce ISE TACACS+ before production use.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Monitoring & Alert Hardening'), bMid(L2, R2, 'Patch Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit log: all actions logged'), bMid(L2, R2, 'Quarterly DCNM upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Failed logins: SIEM alert'), bMid(L2, R2, 'Cisco PSIRT: check monthly'))))
    lines.append(R(merge(bMid(L1, R1, 'Config change: diff + alert'), bMid(L2, R2, 'OS patches: monthly cycle'))))
    lines.append(R(merge(bMid(L1, R1, 'API token expiry: 8h'), bMid(L2, R2, 'Backup before upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert expiry: 60-day warning'), bMid(L2, R2, 'Test in staging first'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM Linux VM · vSphere host · management-only VLAN · Cisco ISE appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TLS 1.2+        = minimum required; disable TLS 1.0/1.1 and SSL 3.0'))
    lines.append(txt_row('ISE TACACS+     = Cisco ISE centralised CLI auth; all admin actions audited'))
    lines.append(txt_row('RBAC            = Role-Based Access Control; operator = read-only; admin = full'))
    lines.append(txt_row('IP whitelist    = restrict DCNM REST API to known source IP ranges'))
    lines.append(txt_row('SAML SSO        = DCNM integrates with IdP; MFA enforced at identity provider'))
    lines.append(txt_row('Session timeout = idle GUI/API session terminated after 30 minutes'))
    lines.append(txt_row('API token expiry= JWT expires after configurable period; 8h default'))
    lines.append(txt_row('Cisco PSIRT     = Product Security Incident Response; Cisco security advisories'))
    lines.append(txt_row('Audit log       = all DCNM GUI and API calls logged with user and timestamp'))
    lines.append(txt_row('Config diff     = DCNM detects out-of-band zone changes and sends alert'))
    lines.append(txt_row('Cert expiry     = TLS certificate monitored; 60-day warning before expiry'))
    lines.append(txt_row('Staging test    = validate DCNM upgrade in non-prod before production rollout'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-trouble-common', 'docs/san/cisco/cisco-dcnm/troubleshooting/common-issues/index.md', 'Cisco DCNM Troubleshooting Common')
def _cisco_dcnm_trouble_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Troubleshooting Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM common issues: switch loss, zone push failure, login error, DB full, ISL alerts.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric & Switch Issues'), bMid(L2, R2, 'Zone Push Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Switch lost from DCNM: ping'), bMid(L2, R2, 'Push fail: SSH cred expired'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMP poll fail: v3 check'), bMid(L2, R2, 'Zone lock: no edit session'))))
    lines.append(R(merge(bMid(L1, R1, 'VSAN isolated: check ISL'), bMid(L2, R2, 'VSAN mismatch: verify both'))))
    lines.append(R(merge(bMid(L1, R1, 'ISL bounce: check SFP/cable'), bMid(L2, R2, 'Conflict: out-of-band change'))))
    lines.append(R(merge(bMid(L1, R1, 'Domain conflict: isolate sw'), bMid(L2, R2, 'show zoneset: verify active'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SNMP and SSH credentials are the most common failure points for DCNM operations.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Auth & Platform Issues'), bMid(L2, R2, 'Performance Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'ISE TACACS+ fail: check svc'), bMid(L2, R2, 'UI slow: Elasticsearch disk'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP bind fail: acct expiry'), bMid(L2, R2, 'appmgr restart: service'))))
    lines.append(R(merge(bMid(L1, R1, 'Token expired: re-logon'), bMid(L2, R2, 'df -h: disk full check'))))
    lines.append(R(merge(bMid(L1, R1, 'Local fallback: ISE down'), bMid(L2, R2, 'Prune old perf data'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit log: failed login check'), bMid(L2, R2, 'journalctl: svc errors'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · management network · Cisco ISE · Cisco MDS switch management ports'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SNMP v3         = DCNM polls switches every 5 min; credential mismatch = red switch'))
    lines.append(txt_row('SSH credentials = per-switch credentials for zone push; update on password change'))
    lines.append(txt_row('Zone lock       = NX-OS zone edit session active; DCNM cannot push until cleared'))
    lines.append(txt_row('VSAN isolated   = VSAN partition; devices in same VSAN cannot communicate'))
    lines.append(txt_row('Domain conflict = two MDS switches same FC domain ID; isolate and renumber'))
    lines.append(txt_row('Out-of-band     = zone change on switch bypassing DCNM; causes config conflict'))
    lines.append(txt_row('show zoneset    = NX-OS; verify active zone set matches expected config'))
    lines.append(txt_row('ISE TACACS+     = check ISE service health if DCNM login fails'))
    lines.append(txt_row('LDAP bind       = DCNM AD integration service account; check for expiry'))
    lines.append(txt_row('Elasticsearch   = DCNM perf DB; disk full causes UI slowness and timeouts'))
    lines.append(txt_row('appmgr          = DCNM VM CLI; restart/status/prune for service management'))
    lines.append(txt_row('journalctl      = Linux systemd log; shows DCNM service crashes and errors'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-trouble-diag', 'docs/san/cisco/cisco-dcnm/troubleshooting/diagnostics/index.md', 'Cisco DCNM Diagnostics')
def _cisco_dcnm_trouble_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM diagnostics: service logs, DB health, REST health endpoint, NX-OS show commands.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DCNM Platform Diagnostics'), bMid(L2, R2, 'Database Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'appmgr status: all services'), bMid(L2, R2, 'appmgr db-status: check'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /rest/health: API check'), bMid(L2, R2, 'PostgreSQL: pg_isready'))))
    lines.append(R(merge(bMid(L1, R1, 'journalctl -u dcnm: log'), bMid(L2, R2, 'Elasticsearch cluster health'))))
    lines.append(R(merge(bMid(L1, R1, 'netstat -tlnp 443: listen'), bMid(L2, R2, 'df -h: disk usage check'))))
    lines.append(R(merge(bMid(L1, R1, 'top: CPU/RAM on DCNM VM'), bMid(L2, R2, 'du -sh: data directory sizes'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('appmgr status and journalctl are first-line; DB and disk status if data issues.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Switch-Level Diagnostics'), bMid(L2, R2, 'TAC Escalation Data'))))
    lines.append(R(merge(bMid(L1, R1, 'show interface fc: errors'), bMid(L2, R2, 'Export DCNM logs: GUI'))))
    lines.append(R(merge(bMid(L1, R1, 'show flogi database'), bMid(L2, R2, 'show tech-support: MDS'))))
    lines.append(R(merge(bMid(L1, R1, 'show zoneset active'), bMid(L2, R2, 'Audit log export: CSV'))))
    lines.append(R(merge(bMid(L1, R1, 'show system health'), bMid(L2, R2, 'API debug: verbose mode'))))
    lines.append(R(merge(bMid(L1, R1, 'show environment: sensors'), bMid(L2, R2, 'Screenshots: UI issue'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · vSphere monitoring · Cisco MDS switch management ports · syslog server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('appmgr status   = DCNM VM CLI; shows all service health in one view'))
    lines.append(txt_row('GET /rest/health = DCNM REST health endpoint; returns service status JSON'))
    lines.append(txt_row('journalctl      = systemd log viewer; shows DCNM service errors and restarts'))
    lines.append(txt_row('pg_isready      = PostgreSQL CLI; checks if DB accepts connections'))
    lines.append(txt_row('Elasticsearch   = DCNM analytics DB; cluster health API shows shard status'))
    lines.append(txt_row('df -h           = disk free check; Elasticsearch fills disk causing failures'))
    lines.append(txt_row('show tech-support= NX-OS MDS full diagnostic bundle; required for Cisco TAC'))
    lines.append(txt_row('show flogi database= FC login database on MDS; verifies HBA access'))
    lines.append(txt_row('show zoneset active= NX-OS active zone set verification'))
    lines.append(txt_row('show system health= MDS overall health; checks modules and fabric state'))
    lines.append(txt_row('show environment= MDS sensor data: temperature, fan, PSU readings'))
    lines.append(txt_row('Audit log CSV   = DCNM user action export; shared during security investigations'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-dcnm-trouble-esc', 'docs/san/cisco/cisco-dcnm/troubleshooting/escalation/index.md', 'Cisco DCNM Escalation')
def _cisco_dcnm_trouble_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco DCNM — Troubleshooting Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM escalation: internal L2/L3 → Cisco TAC with log bundle, case severity, remote.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Internal Escalation Path'), bMid(L2, R2, 'Cisco TAC Escalation'))))
    lines.append(R(merge(bMid(L1, R1, 'L1 → L2: basic checks + logs'), bMid(L2, R2, 'Open case: TAC portal'))))
    lines.append(R(merge(bMid(L1, R1, 'L2 → L3: logs + show-tech'), bMid(L2, R2, 'DCNM version + NX-OS ver'))))
    lines.append(R(merge(bMid(L1, R1, 'L3 → TAC: full data package'), bMid(L2, R2, 'Sev-1: fabric management'))))
    lines.append(R(merge(bMid(L1, R1, 'Incident bridge for Sev-1'), bMid(L2, R2, 'Remote: TAC SSH to DCNM'))))
    lines.append(R(merge(bMid(L1, R1, 'No config changes during inc.'), bMid(L2, R2, 'RCA expected post-close'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Collect DCNM logs and MDS show tech-support before opening a Cisco TAC case.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Data Package'), bMid(L2, R2, 'Severity Classification'))))
    lines.append(R(merge(bMid(L1, R1, 'DCNM logs: journalctl dump'), bMid(L2, R2, 'Sev-1: DCNM down; fabric'))))
    lines.append(R(merge(bMid(L1, R1, 'appmgr status + db-status'), bMid(L2, R2, 'Sev-2: zone push failing'))))
    lines.append(R(merge(bMid(L1, R1, 'show tech-support: per MDS'), bMid(L2, R2, 'Sev-3: partial monitoring'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit log CSV export'), bMid(L2, R2, 'Sev-4: general question'))))
    lines.append(R(merge(bMid(L1, R1, 'Timeline: events before issue'), bMid(L2, R2, 'CSAT after case close'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DCNM VM · management Ethernet · Cisco TAC upload portal · serial console access'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('journalctl dump = full DCNM service log; gzip and share to Cisco TAC'))
    lines.append(txt_row('appmgr status   = DCNM VM CLI; service health output for TAC review'))
    lines.append(txt_row('show tech-support= NX-OS MDS full diagnostic bundle; one per affected switch'))
    lines.append(txt_row('Audit log CSV   = DCNM action log export; shows what changed before incident'))
    lines.append(txt_row('Sev-1           = DCNM completely down; fabric management unavailable'))
    lines.append(txt_row('Sev-2           = DCNM partially working; zone changes or discovery failing'))
    lines.append(txt_row('Cisco TAC       = Technical Assistance Center; opened at tools.cisco.com'))
    lines.append(txt_row('TAC remote      = Cisco engineer SSHs into DCNM VM with customer permission'))
    lines.append(txt_row('RCA             = Root Cause Analysis; Cisco provides after Sev-1 case closure'))
    lines.append(txt_row('CSAT            = Customer Satisfaction survey; sent after TAC case closure'))
    lines.append(txt_row('Incident bridge = conference call coordinating all responders during Sev-1'))
    lines.append(txt_row('No config changes= freeze all DCNM and MDS changes during active incident'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds', 'docs/san/cisco/mds/index.md', 'Cisco MDS 9000 Overview')
def _cisco_mds_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2, L3, R3 = 3, 33, 36, 66, 69, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — Overview'))
    lines.append(txt_row())
    lines.append(txt_row('MDS 9000: Cisco enterprise FC/FCoE switch family. Modular directors and fixed switches.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Product Family'), bMid(L2, R2, 'Key Capabilities'), bMid(L3, R3, 'Management'))))
    lines.append(R(merge(bMid(L1, R1, '9706/9710/9718 directors'), bMid(L2, R2, 'FC 32/64G port speed'), bMid(L3, R3, 'DCNM: GUI + REST API'))))
    lines.append(R(merge(bMid(L1, R1, '9148T fixed 48-port switch'), bMid(L2, R2, 'VSAN: logical segmentation'), bMid(L3, R3, 'NX-OS CLI: SSH'))))
    lines.append(R(merge(bMid(L1, R1, '9132T 32-port fixed switch'), bMid(L2, R2, 'FCoE: Fibre Chan over Eth'), bMid(L3, R3, 'SNMP v3 polling'))))
    lines.append(R(merge(bMid(L1, R1, '9700 high-density director'), bMid(L2, R2, 'FICON: mainframe support'), bMid(L3, R3, 'NetConf/gRPC API'))))
    lines.append(R(merge(bMid(L1, R1, 'HA: dual supervisors'), bMid(L2, R2, 'D-Port: diagnostics'), bMid(L3, R3, 'TACACS+/RADIUS auth'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('MDS 9000 is the Cisco flagship FC switch; VSAN and zoning are core SAN functions.'))
    lines.append(txt_row())
    lines.append(R(arrow([18, 51, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Architecture'), bMid(L2, R2, 'Operations'), bMid(L3, R3, 'Security'))))
    lines.append(R(merge(bMid(L1, R1, 'VSAN design'), bMid(L2, R2, 'Zone management'), bMid(L3, R3, 'RBAC + TACACS+'))))
    lines.append(R(merge(bMid(L1, R1, 'ISL / PortChannel'), bMid(L2, R2, 'Firmware ISSU'), bMid(L3, R3, 'DH-CHAP switch auth'))))
    lines.append(R(merge(bMid(L1, R1, 'FSPF routing'), bMid(L2, R2, 'Health monitoring'), bMid(L3, R3, 'SNMPv3 only'))))
    lines.append(R(merge(bMid(L1, R1, 'FCoE gateway'), bMid(L2, R2, 'Performance analysis'), bMid(L3, R3, 'AES-256 link enc'))))
    lines.append(R(merge(bMid(L1, R1, 'FCIP for DWDM WAN'), bMid(L2, R2, 'Backup/restore'), bMid(L3, R3, 'CFS security policy'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS director chassis · line cards/blades · dual supervisors · SFP transceivers · FC cables'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VSAN            = Virtual SAN; logical FC fabric on MDS; isolates traffic by VSAN ID'))
    lines.append(txt_row('Zoning          = FC access control; defines which initiators can see which targets'))
    lines.append(txt_row('ISL             = Inter-Switch Link; E_Port connection between two FC switches'))
    lines.append(txt_row('PortChannel     = aggregated ISL bundle; increases bandwidth and provides redundancy'))
    lines.append(txt_row('FSPF            = Fabric Shortest Path First; FC routing protocol for path selection'))
    lines.append(txt_row('ISSU            = In-Service Software Upgrade; NX-OS upgrade without traffic disruption'))
    lines.append(txt_row('FCoE            = Fibre Channel over Ethernet; FC protocol encapsulated in 10/25GbE'))
    lines.append(txt_row('FICON           = Fibre Connection; IBM mainframe I/O protocol over FC fabric'))
    lines.append(txt_row('FCIP            = Fibre Channel over IP; FC frames tunnelled over IP/WAN'))
    lines.append(txt_row('DH-CHAP         = Diffie-Hellman CHAP; ISL authentication between MDS switches'))
    lines.append(txt_row('CFS             = Cisco Fabric Services; distributes config across fabric'))
    lines.append(txt_row('D-Port          = diagnostic port; tests link signal quality and latency'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-arch', 'docs/san/cisco/mds/architecture/index.md', 'Cisco MDS Architecture')
def _cisco_mds_arch():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2, L3, R3 = 3, 33, 36, 66, 69, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('MDS architecture: VSAN segmentation, ISL PortChannels, FSPF routing, zone enforcement.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'How It Works'), bMid(L2, R2, 'Integrations'), bMid(L3, R3, 'Design Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'VSAN: logical fabric partition'), bMid(L2, R2, 'DCNM: GUI management'), bMid(L3, R3, 'Dual ISL paths'))))
    lines.append(R(merge(bMid(L1, R1, 'ISL E_Port for switch-switch'), bMid(L2, R2, 'ISE: TACACS+ auth'), bMid(L3, R3, 'VSAN per workload'))))
    lines.append(R(merge(bMid(L1, R1, 'FSPF: shortest path routing'), bMid(L2, R2, 'SIEM: syslog events'), bMid(L3, R3, 'PortChannel for trunk'))))
    lines.append(R(merge(bMid(L1, R1, 'CFS: config distribution'), bMid(L2, R2, 'NetApp/HPE: FC target'), bMid(L3, R3, 'Zone set per VSAN'))))
    lines.append(R(merge(bMid(L1, R1, 'FCoE: FC over 10/25G Eth'), bMid(L2, R2, 'vSphere: VMFS FC LUN'), bMid(L3, R3, 'ISSU: non-disrupt'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('VSAN segmentation and ISL PortChannels form the MDS architecture foundation.'))
    lines.append(txt_row())
    lines.append(R(arrow([18, 51, 84])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Control Plane'), bMid(L2, R2, 'Data Plane'), bMid(L3, R3, 'Management Plane'))))
    lines.append(R(merge(bMid(L1, R1, 'FSPF: path computation'), bMid(L2, R2, 'FC frame forwarding'), bMid(L3, R3, 'DCNM REST API'))))
    lines.append(R(merge(bMid(L1, R1, 'FLOGI: HBA login'), bMid(L2, R2, 'Hardware switching'), bMid(L3, R3, 'NX-OS SSH CLI'))))
    lines.append(R(merge(bMid(L1, R1, 'Name server: device DB'), bMid(L2, R2, 'BB credit flow control'), bMid(L3, R3, 'SNMP v3 traps'))))
    lines.append(R(merge(bMid(L1, R1, 'CFS zone propagation'), bMid(L2, R2, 'QoS: VSAN priorities'), bMid(L3, R3, 'TACACS+ auth'))))
    lines.append(R(merge(bMid(L1, R1, 'PLOGI: target login'), bMid(L2, R2, 'SAN analytics port'), bMid(L3, R3, 'NetConf/gRPC'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS director chassis · supervisor modules · line card blades · SFP transceivers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VSAN            = Virtual SAN; logical partition; one zone database per VSAN'))
    lines.append(txt_row('FSPF            = Fabric Shortest Path First; link-state routing protocol for FC'))
    lines.append(txt_row('FLOGI           = Fabric Login; HBA registers with FC Name Server via FLOGI'))
    lines.append(txt_row('PLOGI           = Port Login; initiator logs into target after FLOGI'))
    lines.append(txt_row('CFS             = Cisco Fabric Services; distributes zone and config across fabric'))
    lines.append(txt_row('ISL             = Inter-Switch Link; E_Port trunk carrying multiple VSANs'))
    lines.append(txt_row('PortChannel     = bundled ISLs; provides bandwidth aggregation and redundancy'))
    lines.append(txt_row('BB credits      = Buffer-to-Buffer credits; flow control mechanism per FC port'))
    lines.append(txt_row('ISSU            = In-Service Software Upgrade; no traffic disruption during upgrade'))
    lines.append(txt_row('SAN analytics   = MDS 9700 feature; per-flow FC telemetry for performance'))
    lines.append(txt_row('DCNM            = Data Center Network Manager; manages MDS zone and firmware'))
    lines.append(txt_row('FCoE            = Fibre Channel over Ethernet; FC on 10/25GbE via DCB/FIP'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-arch-how', 'docs/san/cisco/mds/architecture/how-it-works/index.md', 'Cisco MDS How It Works')
def _cisco_mds_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('MDS operation: HBA FLOGI → Name Server → zoning lookup → PLOGI → I/O flow.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'FC Fabric Login Flow'), bMid(L2, R2, 'VSAN & Zone Enforcement'))))
    lines.append(R(merge(bMid(L1, R1, '1. HBA powers on: FLOGI send'), bMid(L2, R2, 'Zone lookup on PLOGI'))))
    lines.append(R(merge(bMid(L1, R1, '2. MDS assigns FCID (24-bit)'), bMid(L2, R2, 'Deny if not in same zone'))))
    lines.append(R(merge(bMid(L1, R1, '3. Registered in Name Server'), bMid(L2, R2, 'Hard zoning: hardware ACL'))))
    lines.append(R(merge(bMid(L1, R1, '4. Query GPN_ID for targets'), bMid(L2, R2, 'VSAN segmentation: no leak'))))
    lines.append(R(merge(bMid(L1, R1, '5. PLOGI to target FCID'), bMid(L2, R2, 'CFS propagates zone across'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('FLOGI registers HBA; zone is enforced at PLOGI; CFS keeps zones consistent.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ISL & FSPF Routing'), bMid(L2, R2, 'SAN Analytics (MDS 9700)'))))
    lines.append(R(merge(bMid(L1, R1, 'ISL E_Port forms on boot'), bMid(L2, R2, 'Per-flow telemetry: FC'))))
    lines.append(R(merge(bMid(L1, R1, 'FSPF: link state LSR flood'), bMid(L2, R2, 'Initiator/target pair IOPS'))))
    lines.append(R(merge(bMid(L1, R1, 'Shortest path: hop + cost'), bMid(L2, R2, 'Latency histogram per ITL'))))
    lines.append(R(merge(bMid(L1, R1, 'PortChannel: LACP-like hash'), bMid(L2, R2, 'Export to Kafka / Elasticsearch'))))
    lines.append(R(merge(bMid(L1, R1, 'BB credits: per-port control'), bMid(L2, R2, 'Bottleneck ITL detection'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS director chassis · supervisor module · line card blades · SFP transceivers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FLOGI           = Fabric Login; HBA sends FLOGI to get assigned an FCID'))
    lines.append(txt_row('FCID            = Fibre Channel ID; 24-bit address assigned by fabric to each port'))
    lines.append(txt_row('Name Server     = MDS Name Server; database of all device logins (FCID → WWN)'))
    lines.append(txt_row('GPN_ID          = Get Port Name by ID; query Name Server for target WWN list'))
    lines.append(txt_row('PLOGI           = Port Login; initiator to target; MDS enforces zone at this step'))
    lines.append(txt_row('Hard zoning     = zone enforcement in hardware ASIC; cannot be bypassed by software'))
    lines.append(txt_row('CFS             = Cisco Fabric Services; zones propagated to all switches in fabric'))
    lines.append(txt_row('FSPF            = link-state routing; each switch floods LSR with link costs'))
    lines.append(txt_row('PortChannel     = ISL aggregation; frames hashed by source/dest FCID pair'))
    lines.append(txt_row('BB credits      = Buffer-to-Buffer; receiver grants credits; no credit = pause'))
    lines.append(txt_row('SAN analytics   = MDS 9700 ASIC feature; captures per-ITL IOPS and latency'))
    lines.append(txt_row('ITL             = Initiator-Target-LUN; FC I/O flow identifier for analytics'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-arch-int', 'docs/san/cisco/mds/architecture/integrations/index.md', 'Cisco MDS Integrations')
def _cisco_mds_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('MDS integrations: DCNM, Cisco ISE, SIEM, storage arrays, VMware vSphere, automation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Management Integrations'), bMid(L2, R2, 'Security Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'DCNM: zone + firmware mgmt'), bMid(L2, R2, 'ISE: TACACS+/RADIUS auth'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMP v3: NMS polling'), bMid(L2, R2, 'Syslog: SIEM forwarding'))))
    lines.append(R(merge(bMid(L1, R1, 'NETCONF/gRPC: automation'), bMid(L2, R2, 'DH-CHAP: switch-to-switch'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP: time sync all events'), bMid(L2, R2, 'AES-256: link encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'DNS: hostname resolution'), bMid(L2, R2, 'SNMPv3 auth+privacy'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('DCNM manages zones; ISE provides TACACS+; SIEM gets syslog for security events.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Storage & Compute Connect'), bMid(L2, R2, 'Automation Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'NetApp ONTAP: FC LUN target'), bMid(L2, R2, 'Ansible: cisco.nxos'))))
    lines.append(R(merge(bMid(L1, R1, 'Pure FlashArray: FC target'), bMid(L2, R2, 'Terraform: DCNM provider'))))
    lines.append(R(merge(bMid(L1, R1, 'Dell PowerStore: FC target'), bMid(L2, R2, 'Python: NX-API / RESTCONF'))))
    lines.append(R(merge(bMid(L1, R1, 'VMware vSphere: VMFS LUNs'), bMid(L2, R2, 'GitOps: zone as code'))))
    lines.append(R(merge(bMid(L1, R1, 'IBM mainframe: FICON zoning'), bMid(L2, R2, 'ServiceNow: CMDB CI sync'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS switch chassis · FC cables · management Ethernet · Cisco ISE appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('DCNM            = Data Center Network Manager; zones, firmware, topology for MDS'))
    lines.append(txt_row('ISE             = Cisco Identity Services Engine; TACACS+ and RADIUS source'))
    lines.append(txt_row('TACACS+         = centralised CLI auth; every MDS command logged with username'))
    lines.append(txt_row('NETCONF         = XML-based configuration protocol; supported on MDS NX-OS'))
    lines.append(txt_row('gRPC            = modern API transport; MDS telemetry streaming protocol'))
    lines.append(txt_row('DH-CHAP         = Diffie-Hellman CHAP; ISL authentication between switches'))
    lines.append(txt_row('AES-256 link    = optional MDS port-level encryption; requires AES license'))
    lines.append(txt_row('NX-API          = NX-OS REST-like API; JSON over HTTP for automation'))
    lines.append(txt_row('RESTCONF        = YANG-based configuration protocol; RFC 8040'))
    lines.append(txt_row('cisco.nxos      = Ansible Galaxy collection for MDS and Nexus NX-OS automation'))
    lines.append(txt_row('FICON           = IBM mainframe FC I/O protocol; requires FICON zone on MDS'))
    lines.append(txt_row('VMFS            = VMware File System; FC LUN presented to ESXi as datastore'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-arch-design', 'docs/san/cisco/mds/architecture/design-standards/index.md', 'Cisco MDS Design Standards')
def _cisco_mds_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('MDS design principles: dual-fabric A/B, VSAN per workload, PortChannel ISLs, ISSU.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric Design'), bMid(L2, R2, 'VSAN Design'))))
    lines.append(R(merge(bMid(L1, R1, 'Dual fabric A and B always'), bMid(L2, R2, 'One VSAN per workload type'))))
    lines.append(R(merge(bMid(L1, R1, 'No single switch failure impact'), bMid(L2, R2, 'VSAN 1 never used: reserved'))))
    lines.append(R(merge(bMid(L1, R1, 'ISL PortChannel: min 2 ports'), bMid(L2, R2, 'Prod/dev/test separate VSAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Over-subscription: 7:1 max'), bMid(L2, R2, 'VSAN QoS: priority per VSAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Directors: 9706/9710/9718'), bMid(L2, R2, 'FCoE: separate VSAN'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Dual fabric is non-negotiable; VSAN per workload prevents blast-radius cross-talk.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Zone Design'), bMid(L2, R2, 'Operational Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'WWN zoning: not port zoning'), bMid(L2, R2, 'ISSU upgrade: all upgrades'))))
    lines.append(R(merge(bMid(L1, R1, 'Single initiator per zone'), bMid(L2, R2, 'TACACS+ via ISE: mandatory'))))
    lines.append(R(merge(bMid(L1, R1, 'Alias: device name not WWN'), bMid(L2, R2, 'NX-OS: < 2 versions lag'))))
    lines.append(R(merge(bMid(L1, R1, 'Default deny: no open zones'), bMid(L2, R2, 'SNMPv3 only: disable v1/v2'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone set: one per VSAN'), bMid(L2, R2, 'Backup: config + zone daily'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS director pair (A+B) · dual supervisor per director · SFP transceivers · FC cables'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Dual fabric     = two independent FC fabrics; every host and array dual-homed'))
    lines.append(txt_row('VSAN            = Virtual SAN; one VSAN per workload (prod/dev/test separate)'))
    lines.append(txt_row('VSAN 1          = default VSAN; avoid using it; reserved for management'))
    lines.append(txt_row('PortChannel ISL = bundled ISLs; PortChannel1 is recommended minimum 2 links'))
    lines.append(txt_row('7:1             = recommended over-subscription ratio for FC storage traffic'))
    lines.append(txt_row('WWN zoning      = zone by HBA World Wide Name; survives port changes'))
    lines.append(txt_row('Single initiator= one HBA per zone; prevents initiator-to-initiator traffic'))
    lines.append(txt_row('Device alias    = human-readable name for WWN; managed via CFS distribution'))
    lines.append(txt_row('Default deny    = no zone = no communication; strict zone policy'))
    lines.append(txt_row('ISSU            = In-Service Software Upgrade; required for all NX-OS upgrades'))
    lines.append(txt_row('TACACS+ via ISE = Cisco ISE provides TACACS+ for all MDS admin auth'))
    lines.append(txt_row('Zone set        = one active zone set per VSAN at a time; backup sets inactive'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-ops-procedures', 'docs/san/cisco/mds/operations/procedures/index.md', 'Cisco MDS Operations Procedures')
def _cisco_mds_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — Operations Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('MDS day-2 operations: zone changes, VSAN management, firmware ISSU, health checks.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Zone Change Procedure'), bMid(L2, R2, 'VSAN Management'))))
    lines.append(R(merge(bMid(L1, R1, '1. Create device alias in CFS'), bMid(L2, R2, 'Create VSAN: vsan database'))))
    lines.append(R(merge(bMid(L1, R1, '2. Create zone with alias'), bMid(L2, R2, 'Add port to VSAN: vsan-m'))))
    lines.append(R(merge(bMid(L1, R1, '3. Add zone to zone set'), bMid(L2, R2, 'ISL trunk: trunk allowed'))))
    lines.append(R(merge(bMid(L1, R1, '4. zoneset activate vsan ID'), bMid(L2, R2, 'CFS commit: zone propagate'))))
    lines.append(R(merge(bMid(L1, R1, '5. Verify: show zone active'), bMid(L2, R2, 'Verify: show vsan'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Zone changes via DCNM preferred; CFS propagates zone set to all fabric switches.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Firmware ISSU Procedure'), bMid(L2, R2, 'Health Monitoring Routine'))))
    lines.append(R(merge(bMid(L1, R1, '1. copy bootflash: NX-OS'), bMid(L2, R2, 'Daily: show system health'))))
    lines.append(R(merge(bMid(L1, R1, '2. install all nxos <image>'), bMid(L2, R2, 'Weekly: port error report'))))
    lines.append(R(merge(bMid(L1, R1, '3. ISSU: standby sup first'), bMid(L2, R2, 'Monthly: ISL utilisation'))))
    lines.append(R(merge(bMid(L1, R1, '4. show version: verify'), bMid(L2, R2, 'Quarterly: zone audit'))))
    lines.append(R(merge(bMid(L1, R1, '5. copy run start: save'), bMid(L2, R2, 'Annual: fabric review'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS director chassis · supervisor modules · line card blades · SFP transceivers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Device alias    = named WWN; managed via CFS to all switches simultaneously'))
    lines.append(txt_row('zoneset activate= NX-OS; activates zone set in specified VSAN'))
    lines.append(txt_row('show zone active= NX-OS; verifies active zone set and member list in VSAN'))
    lines.append(txt_row('CFS             = Cisco Fabric Services; distributes device aliases and zones'))
    lines.append(txt_row('vsan database   = NX-OS mode for VSAN creation and management'))
    lines.append(txt_row('trunk allowed   = ISL VSAN list; controls which VSANs travel over ISL'))
    lines.append(txt_row('ISSU            = In-Service Software Upgrade; standby sup upgraded first'))
    lines.append(txt_row('install all     = NX-OS ISSU trigger command; activates new image non-disruptively'))
    lines.append(txt_row('copy run start  = saves running config to startup-config; prevents config loss'))
    lines.append(txt_row('show system health= MDS overall health; checks all modules, fans, PSUs'))
    lines.append(txt_row('Port error report= weekly show interface fc counters; CRC and discard checks'))
    lines.append(txt_row('Zone audit      = quarterly review: remove stale aliases and unused zones'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-ops-backup', 'docs/san/cisco/mds/operations/backup-restore/index.md', 'Cisco MDS Backup Restore')
def _cisco_mds_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — Backup and Restore'))
    lines.append(txt_row())
    lines.append(txt_row('MDS backup: running-config, zone set, startup-config to SCP/TFTP; restore sequence.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Configuration Backup'), bMid(L2, R2, 'Zone Database Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'copy run scp://server/path'), bMid(L2, R2, 'show zone status VSAN'))))
    lines.append(R(merge(bMid(L1, R1, 'copy startup scp://server'), bMid(L2, R2, 'copy run scp: zone backup'))))
    lines.append(R(merge(bMid(L1, R1, 'DCNM: archive config auto'), bMid(L2, R2, 'Zone set export: text file'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: nightly via DCNM'), bMid(L2, R2, 'Pre-change snapshot always'))))
    lines.append(R(merge(bMid(L1, R1, 'Retention: 30 days minimum'), bMid(L2, R2, 'CFS: verify zone sync'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Config backup and zone snapshot before every change; DCNM automates nightly.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Config Restore Procedure'), bMid(L2, R2, 'Zone Restore Procedure'))))
    lines.append(R(merge(bMid(L1, R1, '1. copy scp: startup-config'), bMid(L2, R2, '1. Enter zone config mode'))))
    lines.append(R(merge(bMid(L1, R1, '2. reload: apply startup'), bMid(L2, R2, '2. Import zone set file'))))
    lines.append(R(merge(bMid(L1, R1, '3. Verify: show run diff'), bMid(L2, R2, '3. zoneset activate VSAN'))))
    lines.append(R(merge(bMid(L1, R1, '4. Check: show interface fc'), bMid(L2, R2, '4. Verify: show zone active'))))
    lines.append(R(merge(bMid(L1, R1, '5. Test: host I/O access'), bMid(L2, R2, '5. CFS commit: propagate'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS switch chassis · management Ethernet · SCP/TFTP backup server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('copy run scp    = NX-OS; copies running config to SCP destination server'))
    lines.append(txt_row('startup-config  = config loaded on boot; always save running to startup'))
    lines.append(txt_row('copy run start  = NX-OS; saves running config to startup; required after change'))
    lines.append(txt_row('DCNM archive    = DCNM automatically archives per-switch config on schedule'))
    lines.append(txt_row('Zone set export = show zone all export; text file backup of zone database'))
    lines.append(txt_row('CFS             = Cisco Fabric Services; verify zone sync: show cfs merge status'))
    lines.append(txt_row('reload          = switch reload; applies startup-config after restore'))
    lines.append(txt_row('show run diff   = compare restored config to expected baseline'))
    lines.append(txt_row('zoneset activate= activates the imported zone set in specified VSAN'))
    lines.append(txt_row('show zone active= verify zone members are correct after restore'))
    lines.append(txt_row('CFS commit      = CFS zone database push to all fabric switches'))
    lines.append(txt_row('Pre-change snap = always capture zone set before making any zone changes'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-ops-health', 'docs/san/cisco/mds/operations/health-checks/index.md', 'Cisco MDS Health Checks')
def _cisco_mds_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('MDS health: show system, show interface, VSAN state, ISL utilisation, zone sync.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Hardware Health'), bMid(L2, R2, 'Fabric Connectivity Health'))))
    lines.append(R(merge(bMid(L1, R1, 'show system health: all OK'), bMid(L2, R2, 'show vsan: all active'))))
    lines.append(R(merge(bMid(L1, R1, 'show environment: temp/PSU'), bMid(L2, R2, 'show interface trunk: ISL'))))
    lines.append(R(merge(bMid(L1, R1, 'show module: all online'), bMid(L2, R2, 'show port-channel: member'))))
    lines.append(R(merge(bMid(L1, R1, 'show version: correct NX-OS'), bMid(L2, R2, 'show flogi database: count'))))
    lines.append(R(merge(bMid(L1, R1, 'show redundancy: sup active'), bMid(L2, R2, 'ISL util < 70% sustained'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('show system health and show environment cover hardware; VSAN/ISL cover fabric.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Port & Zone Health'), bMid(L2, R2, 'Performance Health'))))
    lines.append(R(merge(bMid(L1, R1, 'show interface fc: no errors'), bMid(L2, R2, 'show analytics ITL flow'))))
    lines.append(R(merge(bMid(L1, R1, 'CRC errors: 0 per day target'), bMid(L2, R2, 'show interface counter'))))
    lines.append(R(merge(bMid(L1, R1, 'show zone active: matches'), bMid(L2, R2, 'BB credits: no starvation'))))
    lines.append(R(merge(bMid(L1, R1, 'show device-alias: no stale'), bMid(L2, R2, 'SFP optical: > -3 dBm'))))
    lines.append(R(merge(bMid(L1, R1, 'CFS: zone in sync on all sw'), bMid(L2, R2, 'Latency < 1ms per ITL'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS director chassis · supervisor module · line card blades · SFP transceivers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('show system health= NX-OS; overall switch health including modules and fabric'))
    lines.append(txt_row('show environment = NX-OS; temperature, fan RPM, and PSU voltage readings'))
    lines.append(txt_row('show module      = NX-OS; line card / supervisor status and operational state'))
    lines.append(txt_row('show redundancy  = supervisor HA state; active + standby both must be present'))
    lines.append(txt_row('show flogi database= FC login database; count should match expected device list'))
    lines.append(txt_row('show interface fc= per-port counters: CRC, loss-of-sync, credit starvation'))
    lines.append(txt_row('show zone active = active zone set members per VSAN; verify correct aliases'))
    lines.append(txt_row('show device-alias= CFS-distributed device alias database; check for orphans'))
    lines.append(txt_row('CRC errors       = Cyclic Redundancy Check; non-zero = bad SFP or cable'))
    lines.append(txt_row('BB credits       = Buffer-to-Buffer credits; zero = port paused; check starvation'))
    lines.append(txt_row('SFP optical      = signal power in dBm; < -3 dBm indicates degraded transceiver'))
    lines.append(txt_row('show analytics   = MDS 9700 ITL flow analytics: IOPS, throughput, latency'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-ops-install', 'docs/san/cisco/mds/operations/install-upgrade/index.md', 'Cisco MDS Install Upgrade')
def _cisco_mds_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('MDS initial setup: rack, cable, NX-OS boot, initial config; ISSU upgrade procedure.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Initial Setup'), bMid(L2, R2, 'NX-OS Initial Configuration'))))
    lines.append(R(merge(bMid(L1, R1, '1. Rack and cable switch'), bMid(L2, R2, '1. Set hostname + IP mgmt'))))
    lines.append(R(merge(bMid(L1, R1, '2. Console: 9600 baud 8N1'), bMid(L2, R2, '2. Configure NTP servers'))))
    lines.append(R(merge(bMid(L1, R1, '3. Power on: boot sequence'), bMid(L2, R2, '3. Set admin password'))))
    lines.append(R(merge(bMid(L1, R1, '4. Initial config wizard'), bMid(L2, R2, '4. Configure TACACS+ ISE'))))
    lines.append(R(merge(bMid(L1, R1, '5. Set management IP + SSH'), bMid(L2, R2, '5. Add to DCNM fabric'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Console access required for initial setup; TACACS+ and NTP before adding to fabric.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ISSU Upgrade Procedure'), bMid(L2, R2, 'Post-Upgrade Validation'))))
    lines.append(R(merge(bMid(L1, R1, '1. Backup config + zone set'), bMid(L2, R2, '1. show version: new NX-OS'))))
    lines.append(R(merge(bMid(L1, R1, '2. Copy NX-OS to bootflash'), bMid(L2, R2, '2. show system health: OK'))))
    lines.append(R(merge(bMid(L1, R1, '3. show install all impact'), bMid(L2, R2, '3. show interface: no errors'))))
    lines.append(R(merge(bMid(L1, R1, '4. install all nxos <image>'), bMid(L2, R2, '4. Host I/O: verify access'))))
    lines.append(R(merge(bMid(L1, R1, '5. copy run start after'), bMid(L2, R2, '5. DCNM: verify version'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS director chassis · console cable · management Ethernet · SFP transceivers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ISSU            = In-Service Software Upgrade; NX-OS upgrade without traffic drop'))
    lines.append(txt_row('show install all impact= previews ISSU upgrade impact; shows module reloads'))
    lines.append(txt_row('install all     = ISSU trigger; upgrades standby supervisor first then failover'))
    lines.append(txt_row('bootflash       = switch internal flash storage; holds NX-OS images'))
    lines.append(txt_row('copy run start  = saves running config to startup; required after every change'))
    lines.append(txt_row('Console         = serial connection; 9600 baud 8N1; required for initial setup'))
    lines.append(txt_row('Initial config wizard= first-boot setup; sets admin password and IP'))
    lines.append(txt_row('TACACS+         = configure before adding to fabric; ISE must be reachable'))
    lines.append(txt_row('NTP             = configure before DCNM discovery; event timestamps must sync'))
    lines.append(txt_row('DCNM            = add switch to DCNM after SSH is configured; enables zone mgmt'))
    lines.append(txt_row('show version    = verify NX-OS version after ISSU upgrade completes'))
    lines.append(txt_row('show system health= post-upgrade health check; all modules should be online'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-ops-scripts', 'docs/san/cisco/mds/operations/scripts/index.md', 'Cisco MDS Operations Scripts')
def _cisco_mds_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — Operations Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('MDS scripting: NX-API, Ansible cisco.nxos, Python NETCONF, zone automation, reports.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'NX-API Scripting'), bMid(L2, R2, 'Zone Automation'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /ins json CLI exec'), bMid(L2, R2, 'Ansible: cisco.nxos.nxos_vsan'))))
    lines.append(R(merge(bMid(L1, R1, 'Auth: admin:pass base64'), bMid(L2, R2, 'Python: NETCONF ncclient'))))
    lines.append(R(merge(bMid(L1, R1, 'show commands via REST'), bMid(L2, R2, 'Batch zone from CSV'))))
    lines.append(R(merge(bMid(L1, R1, 'Exec zone config commands'), bMid(L2, R2, 'Validate: show zone active'))))
    lines.append(R(merge(bMid(L1, R1, 'Config push via JSON body'), bMid(L2, R2, 'Device alias bulk create'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('NX-API and Ansible cisco.nxos automate MDS zones; NETCONF for config as code.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Reporting Scripts'), bMid(L2, R2, 'Maintenance Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Port utilisation: weekly CSV'), bMid(L2, R2, 'Config backup: SCP nightly'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone audit: stale aliases'), bMid(L2, R2, 'Zone snapshot pre-change'))))
    lines.append(R(merge(bMid(L1, R1, 'SFP power: inventory script'), bMid(L2, R2, 'NX-OS ver check script'))))
    lines.append(R(merge(bMid(L1, R1, 'FLOGI count: device report'), bMid(L2, R2, 'Stale alias cleanup'))))
    lines.append(R(merge(bMid(L1, R1, 'VSAN member inventory'), bMid(L2, R2, 'Port error daily report'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS switch · NX-API port 443 · management Ethernet · automation Linux host'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('NX-API          = NX-OS REST-like API; JSON over HTTP/HTTPS; /ins endpoint'))
    lines.append(txt_row('cisco.nxos      = Ansible Galaxy collection for MDS/Nexus NX-OS automation'))
    lines.append(txt_row('nxos_vsan       = Ansible module; create, modify, and delete VSANs on MDS'))
    lines.append(txt_row('ncclient        = Python NETCONF library; send XML RPC to NX-OS NETCONF server'))
    lines.append(txt_row('show zone active= NX-OS CLI; post-change validation of zone set members'))
    lines.append(txt_row('Device alias    = human-readable WWN label; managed via CFS distribution'))
    lines.append(txt_row('CSV batch       = bulk zone creation from spreadsheet; script loops per row'))
    lines.append(txt_row('SFP power script= parse show interface transceiver; export to monitoring'))
    lines.append(txt_row('FLOGI count     = number of devices logged into fabric; trending report'))
    lines.append(txt_row('Config backup   = copy run scp:// nightly; store in version control'))
    lines.append(txt_row('Stale alias     = alias with no active FLOGI; identify and remove quarterly'))
    lines.append(txt_row('Port error daily= parse show interface fc counters; alert on CRC increase'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-ops-cli', 'docs/san/cisco/mds/operations/cli-reference/index.md', 'Cisco MDS CLI Reference')
def _cisco_mds_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('MDS NX-OS CLI: fabric commands, zone commands, port commands, diagnostics.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric & VSAN Commands'), bMid(L2, R2, 'Zone Commands'))))
    lines.append(R(merge(bMid(L1, R1, 'show flogi database'), bMid(L2, R2, 'show zone active vsan <n>'))))
    lines.append(R(merge(bMid(L1, R1, 'show vsan: all states'), bMid(L2, R2, 'zone name <n> vsan <id>'))))
    lines.append(R(merge(bMid(L1, R1, 'show fcns database vsan'), bMid(L2, R2, 'zoneset name <n> vsan <id>'))))
    lines.append(R(merge(bMid(L1, R1, 'show fcdomain: domain IDs'), bMid(L2, R2, 'zoneset activate name <n>'))))
    lines.append(R(merge(bMid(L1, R1, 'show topology: ISL map'), bMid(L2, R2, 'show device-alias database'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('show flogi and show zone are the two most-used daily operational commands.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Port & Interface Commands'), bMid(L2, R2, 'Diagnostic & Support'))))
    lines.append(R(merge(bMid(L1, R1, 'show interface fc1/1'), bMid(L2, R2, 'show system health'))))
    lines.append(R(merge(bMid(L1, R1, 'show interface trunk: ISLs'), bMid(L2, R2, 'show environment'))))
    lines.append(R(merge(bMid(L1, R1, 'show port-channel summary'), bMid(L2, R2, 'show module all'))))
    lines.append(R(merge(bMid(L1, R1, 'shut / no shut fc1/1'), bMid(L2, R2, 'show tech-support: TAC'))))
    lines.append(R(merge(bMid(L1, R1, 'show interface transceiver'), bMid(L2, R2, 'debug zone basic-er'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS director chassis · supervisor module · line card blades · management Ethernet'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('show flogi database= FC fabric login database; shows all device logins'))
    lines.append(txt_row('show vsan        = VSAN states; all should show active'))
    lines.append(txt_row('show fcns database= FC Name Server database; registered devices in VSAN'))
    lines.append(txt_row('show fcdomain    = domain ID assignment; shows principal switch'))
    lines.append(txt_row('show topology    = ISL map showing connected switches and port numbers'))
    lines.append(txt_row('show zone active = active zone set members and zone names per VSAN'))
    lines.append(txt_row('device-alias     = WWN alias; CFS-distributed across fabric'))
    lines.append(txt_row('zoneset activate = activates named zone set in specified VSAN'))
    lines.append(txt_row('show interface fc= per-port FC counters: CRC, credit, throughput'))
    lines.append(txt_row('show interface trunk= ISL trunk status and allowed VSAN list'))
    lines.append(txt_row('show transceiver = SFP optical power level and signal status'))
    lines.append(txt_row('show tech-support= full diagnostic bundle for Cisco TAC escalation'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-ops-common', 'docs/san/cisco/mds/operations/common-issues/index.md', 'Cisco MDS Common Issues')
def _cisco_mds_ops_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS 9000 — Common Operational Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common MDS issues: HBA not logging in, ISL bounce, zone conflict, CRC errors, credits.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'HBA & Login Issues'), bMid(L2, R2, 'ISL & Fabric Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'No FLOGI: check port state'), bMid(L2, R2, 'ISL bounce: SFP or cable'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone not allowing PLOGI'), bMid(L2, R2, 'ISL down: speed mismatch'))))
    lines.append(R(merge(bMid(L1, R1, 'Wrong VSAN: check trunk'), bMid(L2, R2, 'VSAN isolated: check ISL'))))
    lines.append(R(merge(bMid(L1, R1, 'Alias not in zone member'), bMid(L2, R2, 'Domain conflict: renumber'))))
    lines.append(R(merge(bMid(L1, R1, 'Port disabled: no shut fc'), bMid(L2, R2, 'CFS merge fail: zone conf'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Zone and VSAN are first checks for HBA login issues; ISL = SFP and cable check.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Performance Issues'), bMid(L2, R2, 'Firmware & Config Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'CRC errors: replace SFP'), bMid(L2, R2, 'NX-OS mismatch on fabric'))))
    lines.append(R(merge(bMid(L1, R1, 'BB credit starvation: check'), bMid(L2, R2, 'Config not saved: copy run'))))
    lines.append(R(merge(bMid(L1, R1, 'ISL util > 70%: add ISLs'), bMid(L2, R2, 'License missing: show lic'))))
    lines.append(R(merge(bMid(L1, R1, 'Latency spike: SAN analytics'), bMid(L2, R2, 'ISSU fail: check compat'))))
    lines.append(R(merge(bMid(L1, R1, 'Queue depth: host HBA tune'), bMid(L2, R2, 'Rollback: prior bootflash'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS switch chassis · SFP transceivers · FC cables · host HBAs · storage arrays'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FLOGI           = Fabric Login; HBA must FLOGI before data I/O is possible'))
    lines.append(txt_row('PLOGI           = Port Login; blocked by zone policy if HBA not in same zone'))
    lines.append(txt_row('VSAN trunk      = ISL must allow VSAN for HBA to appear in correct segment'))
    lines.append(txt_row('CFS merge fail  = zone database conflict between two switches; must resolve'))
    lines.append(txt_row('Domain conflict = two switches with same FC domain ID; isolate and renumber'))
    lines.append(txt_row('CRC errors      = Cyclic Redundancy Check; indicates bad SFP or dirty fiber'))
    lines.append(txt_row('BB credits      = Buffer-to-Buffer; zero credits = port paused; check starvation'))
    lines.append(txt_row('SAN analytics   = MDS 9700 per-ITL latency histogram; identify slow target'))
    lines.append(txt_row('show lic        = show license; verify ENTERPRISE_PKG or SAN_ANALYTICS_PKG'))
    lines.append(txt_row('ISSU compat     = ISSU requires NX-OS version compatibility check'))
    lines.append(txt_row('bootflash       = switch flash; previous NX-OS image kept for rollback'))
    lines.append(txt_row('copy run start  = saves running config; loss of unsaved changes on reload'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-sec-access', 'docs/san/cisco/mds/security/access-control/index.md', 'Cisco MDS — Security Access Control')
def _cisco_mds_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS — Security Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('Role-based access control for MDS fabric using local and AAA-backed user accounts.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Local User Accounts'), bMid(L2, R2, 'AAA Authentication'))))
    lines.append(R(merge(bMid(L1, R1, 'Built-in roles: admin, network-admin'), bMid(L2, R2, 'TACACS+: centralized auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom roles: granular command sets'), bMid(L2, R2, 'RADIUS: fallback option'))))
    lines.append(R(merge(bMid(L1, R1, 'Password policy: min length, aging'), bMid(L2, R2, 'LDAP: directory integration'))))
    lines.append(R(merge(bMid(L1, R1, 'Account lockout: failed attempts'), bMid(L2, R2, 'Server groups: priority order'))))
    lines.append(R(merge(bMid(L1, R1, 'SSH key-based login support'), bMid(L2, R2, 'Local fallback if AAA down'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('RBAC model enforced: user role determines CLI command access scope'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Role Assignments'), bMid(L2, R2, 'VSAN Access Control'))))
    lines.append(R(merge(bMid(L1, R1, 'Map users to predefined roles'), bMid(L2, R2, 'VSAN admin: per-fabric scope'))))
    lines.append(R(merge(bMid(L1, R1, 'Role inheritance: none (explicit)'), bMid(L2, R2, 'Zoning auth: FC-SP frame auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit: role change logging'), bMid(L2, R2, 'Port security: WWN allow-list'))))
    lines.append(R(merge(bMid(L1, R1, 'Show users: current sessions'), bMid(L2, R2, 'SNMPv3 with auth+privacy'))))
    lines.append(R(merge(bMid(L1, R1, 'Terminal session timeout config'), bMid(L2, R2, 'No SNMP v1/v2 in production'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS chassis · supervisor modules · AAA servers (TACACS+/RADIUS) · management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC           = Role-Based Access Control; maps users to permitted CLI commands'))
    lines.append(txt_row('TACACS+        = Terminal Access Controller Access Control System Plus; centralized AAA'))
    lines.append(txt_row('RADIUS         = Remote Authentication Dial-In User Service; alternative AAA protocol'))
    lines.append(txt_row('AAA            = Authentication, Authorization, Accounting; security framework'))
    lines.append(txt_row('FC-SP          = Fibre Channel Security Protocol; switch-to-switch frame authentication'))
    lines.append(txt_row('Port Security  = Feature restricting which WWNs can log into a given FC port'))
    lines.append(txt_row('SNMPv3         = SNMP version 3 with user-based security model; supports auth+encryption'))
    lines.append(txt_row('WWN            = World Wide Name; 64-bit unique identifier for FC devices'))
    lines.append(txt_row('VSAN           = Virtual SAN; logical fabric partition with independent access controls'))
    lines.append(txt_row('Server group   = Ordered list of AAA servers tried in sequence for authentication'))
    lines.append(txt_row('Local fallback = If all AAA servers unreachable, switch authenticates from local DB'))
    lines.append(txt_row('Account lockout= Security policy disabling login after N consecutive failed attempts'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-sec-auth', 'docs/san/cisco/mds/security/authentication/index.md', 'Cisco MDS — Security Authentication')
def _cisco_mds_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS — Security Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('Multi-layer authentication covering management plane, fabric login, and data-plane security.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Management Auth'), bMid(L2, R2, 'Fabric Auth (FC-SP)'))))
    lines.append(R(merge(bMid(L1, R1, 'SSH: key exchange + cipher'), bMid(L2, R2, 'DHCHAP: switch-to-switch auth'))))
    lines.append(R(merge(bMid(L1, R1, 'HTTPS: TLS 1.2+ for DCNM/GUI'), bMid(L2, R2, 'DHCHAP group: DH key strength'))))
    lines.append(R(merge(bMid(L1, R1, 'Console: local auth + timeout'), bMid(L2, R2, 'Hash algorithm: MD5 / SHA-1'))))
    lines.append(R(merge(bMid(L1, R1, 'AAA login: TACACS+ first'), bMid(L2, R2, 'Password db: local or RADIUS'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA via TACACS+ server side'), bMid(L2, R2, 'Per-VSAN DHCHAP enable flag'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Management auth and FC-SP fabric auth operate independently on the same switch'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Session Security'), bMid(L2, R2, 'Certificate Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Idle timeout: auto-disconnect'), bMid(L2, R2, 'PKI: local CA or external CA'))))
    lines.append(R(merge(bMid(L1, R1, 'Max sessions: limit per user'), bMid(L2, R2, 'Trustpoint: CA anchor config'))))
    lines.append(R(merge(bMid(L1, R1, 'Login banner: legal notice'), bMid(L2, R2, 'Cert enrollment: SCEP or manual'))))
    lines.append(R(merge(bMid(L1, R1, 'Exec timeout: per line config'), bMid(L2, R2, 'CRL: revocation list check'))))
    lines.append(R(merge(bMid(L1, R1, 'Logging: auth success/failure'), bMid(L2, R2, 'OCSP: online status check'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS supervisor · TACACS+/RADIUS server · CA server · management Ethernet port'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('DHCHAP         = Diffie-Hellman Challenge Handshake Authentication Protocol; FC-SP method'))
    lines.append(txt_row('FC-SP          = Fibre Channel Security Protocol; authenticates switches at FLOGI'))
    lines.append(txt_row('TACACS+        = AAA protocol; separates auth, authz, accounting for per-command logging'))
    lines.append(txt_row('SCEP           = Simple Certificate Enrollment Protocol; automates cert requests to CA'))
    lines.append(txt_row('Trustpoint     = Named CA anchor in NX-OS/MDS; used to validate server certificates'))
    lines.append(txt_row('CRL            = Certificate Revocation List; list of invalidated certs to reject'))
    lines.append(txt_row('OCSP           = Online Certificate Status Protocol; real-time cert validity check'))
    lines.append(txt_row('PKI            = Public Key Infrastructure; framework managing digital certificates'))
    lines.append(txt_row('MFA            = Multi-Factor Authentication; adds OTP/push beyond password'))
    lines.append(txt_row('SSH key        = Public-key authentication; eliminates password for admin sessions'))
    lines.append(txt_row('Login banner   = Legal warning displayed before credential prompt'))
    lines.append(txt_row('FLOGI          = Fabric Login; N_Port to switch handshake where FC-SP auth occurs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-sec-enc', 'docs/san/cisco/mds/security/encryption/index.md', 'Cisco MDS — Security Encryption')
def _cisco_mds_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS — Security Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('Management-plane TLS and FC-SP fabric encryption protecting MDS switch communications.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Management Encryption'), bMid(L2, R2, 'Fabric Encryption (FC-SP-2)'))))
    lines.append(R(merge(bMid(L1, R1, 'SSH: AES-128/256-CTR ciphers'), bMid(L2, R2, 'FC-SP-2: AES-256-GCM frames'))))
    lines.append(R(merge(bMid(L1, R1, 'HTTPS: TLS 1.2 minimum'), bMid(L2, R2, 'IKE: key exchange between ISLs'))))
    lines.append(R(merge(bMid(L1, R1, 'SNMP: v3 authPriv (AES-128)'), bMid(L2, R2, 'Per-ISL encryption enable'))))
    lines.append(R(merge(bMid(L1, R1, 'Syslog: TLS transport option'), bMid(L2, R2, 'Rekey interval configurable'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable weak ciphers: RC4/DES'), bMid(L2, R2, 'GCM: integrity + encryption'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Management TLS protects CLI/API; FC-SP-2 protects ISL data in transit'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Key Management'), bMid(L2, R2, 'Compliance Posture'))))
    lines.append(R(merge(bMid(L1, R1, 'Local key store on supervisor'), bMid(L2, R2, 'FIPS 140-2 mode available'))))
    lines.append(R(merge(bMid(L1, R1, 'KMS: external key server option'), bMid(L2, R2, 'Common Criteria validation'))))
    lines.append(R(merge(bMid(L1, R1, 'Key rotation: scheduled rekey'), bMid(L2, R2, 'Audit: cipher negotiation log'))))
    lines.append(R(merge(bMid(L1, R1, 'PKI trustpoint for cert storage'), bMid(L2, R2, 'No plaintext mgmt protocols'))))
    lines.append(R(merge(bMid(L1, R1, 'Entropy: hardware RNG on ASIC'), bMid(L2, R2, 'Annual cipher review policy'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS supervisor ASIC (hardware RNG) · ISL fiber links · management Ethernet · KMS server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FC-SP-2        = Fibre Channel Security Protocol v2; adds ISL frame encryption'))
    lines.append(txt_row('GCM            = Galois/Counter Mode; AES cipher mode providing auth + encryption'))
    lines.append(txt_row('IKE            = Internet Key Exchange; negotiates session keys for FC-SP-2'))
    lines.append(txt_row('ISL            = Inter-Switch Link; E_Port connection between two MDS switches'))
    lines.append(txt_row('FIPS 140-2     = US federal standard for cryptographic module security'))
    lines.append(txt_row('KMS            = Key Management Server; centralizes key lifecycle for encryption'))
    lines.append(txt_row('authPriv       = SNMPv3 security level: authentication + privacy (encryption)'))
    lines.append(txt_row('Trustpoint     = Named PKI anchor; stores CA cert and associated key material'))
    lines.append(txt_row('Rekey interval = How often session encryption keys are rotated to limit exposure'))
    lines.append(txt_row('Hardware RNG   = Crypto-grade random number generator built into ASIC'))
    lines.append(txt_row('Common Criteria= International security evaluation standard (ISO/IEC 15408)'))
    lines.append(txt_row('TLS            = Transport Layer Security; encrypts management-plane sessions'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-sec-hard', 'docs/san/cisco/mds/security/hardening/index.md', 'Cisco MDS — Security Hardening')
def _cisco_mds_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS — Security Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('Baseline hardening checklist: disable unused services, enforce encrypted protocols, RBAC.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service Hardening'), bMid(L2, R2, 'Network Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable Telnet: SSH only'), bMid(L2, R2, 'Mgmt ACL: restrict source IPs'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable HTTP: HTTPS only'), bMid(L2, R2, 'OOB management: dedicated VLAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable SNMPv1/v2: v3 only'), bMid(L2, R2, 'No in-band management'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable unused features (FCIP)'), bMid(L2, R2, 'NTP auth: MD5 key required'))))
    lines.append(R(merge(bMid(L1, R1, 'Enable FIPS mode if required'), bMid(L2, R2, 'Syslog: encrypted TLS remote'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Disable cleartext protocols first; then restrict source access; then enable logging'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric Hardening'), bMid(L2, R2, 'Audit and Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Port security: WWN allow-list'), bMid(L2, R2, 'Syslog: auth events to SIEM'))))
    lines.append(R(merge(bMid(L1, R1, 'FC-SP: ISL authentication on'), bMid(L2, R2, 'TACACS+ accounting: all cmds'))))
    lines.append(R(merge(bMid(L1, R1, 'DPVM: dynamic port VSAN map'), bMid(L2, R2, 'Config diff: track changes'))))
    lines.append(R(merge(bMid(L1, R1, 'SAN zoning: single-initiator'), bMid(L2, R2, 'Baseline: show running-config'))))
    lines.append(R(merge(bMid(L1, R1, 'E_Port isolation on mismatch'), bMid(L2, R2, 'Annual access review policy'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS chassis · OOB management Ethernet · TACACS+/SIEM server · NTP server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FIPS mode      = Federal Information Processing Standard; disables non-compliant algos'))
    lines.append(txt_row('OOB management = Out-of-Band; dedicated management network isolated from data path'))
    lines.append(txt_row('DPVM           = Dynamic Port VSAN Membership; assigns VSAN based on WWN at login'))
    lines.append(txt_row('E_Port isolation= Quarantining a trunk ISL due to fabric-parameter mismatch'))
    lines.append(txt_row('Port security  = Locks a switch port to allow only whitelisted WWNs to log in'))
    lines.append(txt_row('FC-SP          = Fibre Channel Security Protocol; authenticates ISL neighbors'))
    lines.append(txt_row('FCIP           = Fibre Channel over IP; WAN extension feature; disable if unused'))
    lines.append(txt_row('Single-initiator= Zoning best practice: each zone has exactly one host HBA'))
    lines.append(txt_row('TACACS+ accounting= Records every command executed; stored centrally for audit'))
    lines.append(txt_row('Config baseline= Saved known-good running-config snapshot for change detection'))
    lines.append(txt_row('NTP auth       = MD5-keyed authentication of NTP packets to prevent time spoofing'))
    lines.append(txt_row('SIEM           = Security Information and Event Management; aggregates log analysis'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-trouble-common', 'docs/san/cisco/mds/troubleshooting/common-issues/index.md', 'Cisco MDS — Troubleshooting Common Issues')
def _cisco_mds_trouble_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS — Troubleshooting Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Most frequent MDS fabric issues: FLOGI failures, E_Port isolation, zoning errors.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Login Failures'), bMid(L2, R2, 'ISL / E_Port Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'FLOGI rejected: port VSAN mismatch'), bMid(L2, R2, 'E_Port isolated: domain ID clash'))))
    lines.append(R(merge(bMid(L1, R1, 'PLOGI fail: zoning not configured'), bMid(L2, R2, 'ISL down: SFP incompatibility'))))
    lines.append(R(merge(bMid(L1, R1, 'HBA offline: SFP link fault'), bMid(L2, R2, 'Trunk mismatch: VSAN list diff'))))
    lines.append(R(merge(bMid(L1, R1, 'FDISC: NPV mode login fail'), bMid(L2, R2, 'Segmented fabric: FSPF cost'))))
    lines.append(R(merge(bMid(L1, R1, 'Show flogi database to verify'), bMid(L2, R2, 'Show interface fc state'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Login errors require FLOGI/PLOGI trace; ISL errors need domain/VSAN alignment check'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Zoning Issues'), bMid(L2, R2, 'Performance Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone not active: pending commit'), bMid(L2, R2, 'High BB_Credit pressure'))))
    lines.append(R(merge(bMid(L1, R1, 'WWN not in zone: PLOGI denied'), bMid(L2, R2, 'CRC errors: cable or SFP bad'))))
    lines.append(R(merge(bMid(L1, R1, 'Zone merge conflict: mismatch'), bMid(L2, R2, 'Congestion: slow-drain device'))))
    lines.append(R(merge(bMid(L1, R1, 'Default zone deny: block all'), bMid(L2, R2, 'IOCTL timeout: queue depth'))))
    lines.append(R(merge(bMid(L1, R1, 'Show zone active to verify'), bMid(L2, R2, 'Show interface counters'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS line cards · SFP transceivers · ISL fiber · HBA in server · storage array ports'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FLOGI          = Fabric Login; N_Port to switch handshake to join the fabric'))
    lines.append(txt_row('PLOGI          = Port Login; N_Port to N_Port session establishment through fabric'))
    lines.append(txt_row('FDISC          = Fabric Discover; VN_Port login in NPIV/NPV environments'))
    lines.append(txt_row('E_Port         = Expansion Port; ISL port mode between two switches'))
    lines.append(txt_row('E_Port isolated= Admin-isolated due to domain ID or parameter conflict'))
    lines.append(txt_row('Domain ID      = Unique 1-239 identifier for each switch in a fabric'))
    lines.append(txt_row('BB_Credit      = Buffer-to-Buffer Credit; flow control units for FC link'))
    lines.append(txt_row('Slow-drain     = Device accepting frames slowly; causes backpressure upstream'))
    lines.append(txt_row('Zone merge     = Process of combining zone databases when two fabrics connect'))
    lines.append(txt_row('Default zone   = Policy for devices not in any explicit zone: deny or permit'))
    lines.append(txt_row('FSPF           = Fabric Shortest Path First; routing protocol determining ISL paths'))
    lines.append(txt_row('CRC error      = Frame checksum failure; indicates physical layer problem'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-trouble-diag', 'docs/san/cisco/mds/troubleshooting/diagnostics/index.md', 'Cisco MDS — Troubleshooting Diagnostics')
def _cisco_mds_trouble_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS — Troubleshooting Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('Diagnostic toolset: show commands, SPAN, FC Ping/Traceroute, and tech-support bundles.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Show Command Toolkit'), bMid(L2, R2, 'FC Ping and Traceroute'))))
    lines.append(R(merge(bMid(L1, R1, 'show flogi database: logins'), bMid(L2, R2, 'fcping: N_Port reachability'))))
    lines.append(R(merge(bMid(L1, R1, 'show zone active: zone state'), bMid(L2, R2, 'fctrace: path hop-by-hop'))))
    lines.append(R(merge(bMid(L1, R1, 'show interface fc: counters'), bMid(L2, R2, 'FC loopback: port self-test'))))
    lines.append(R(merge(bMid(L1, R1, 'show topology: fabric map'), bMid(L2, R2, 'DCNM: topology view'))))
    lines.append(R(merge(bMid(L1, R1, 'show hardware: module status'), bMid(L2, R2, 'Ethanalyzer: mgmt capture'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Show commands give state snapshots; FC ping/trace verify end-to-end path connectivity'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SPAN and Capture'), bMid(L2, R2, 'Log Collection'))))
    lines.append(R(merge(bMid(L1, R1, 'FC SPAN: mirror FC traffic'), bMid(L2, R2, 'Tech-support: full bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'SPAN dest: analyzer port'), bMid(L2, R2, 'show logging: syslog buffer'))))
    lines.append(R(merge(bMid(L1, R1, 'RSPAN: remote SPAN over IP'), bMid(L2, R2, 'Event history: per-module'))))
    lines.append(R(merge(bMid(L1, R1, 'Capture with Wireshark via tap'), bMid(L2, R2, 'Core dump: supervisor crash'))))
    lines.append(R(merge(bMid(L1, R1, 'SPAN ACL: filter traffic'), bMid(L2, R2, 'TAC upload: encrypted bundle'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS supervisor · FC analyzer port · management Ethernet · syslog/DCNM server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FC SPAN        = Fibre Channel Switched Port Analyzer; mirrors selected FC traffic'))
    lines.append(txt_row('RSPAN          = Remote SPAN; forwards mirrored frames to remote analyzer over IP'))
    lines.append(txt_row('fcping         = FC-layer reachability test using ECHO Extended Link Service'))
    lines.append(txt_row('fctrace        = FC-layer traceroute; maps path from source to destination N_Port'))
    lines.append(txt_row('Ethanalyzer    = Cisco tool capturing management-plane Ethernet packets on supervisor'))
    lines.append(txt_row('tech-support   = Comprehensive diagnostic bundle; includes logs, configs, counters'))
    lines.append(txt_row('Event history  = Per-process ring buffer of internal events; survives minor faults'))
    lines.append(txt_row('Core dump      = Memory snapshot taken when a process crashes; aids TAC analysis'))
    lines.append(txt_row('TAC            = Technical Assistance Center; Cisco support team'))
    lines.append(txt_row('SPAN ACL       = Filter applied to SPAN session to capture only matching traffic'))
    lines.append(txt_row('show topology  = CLI command displaying fabric-wide switch and ISL map'))
    lines.append(txt_row('FC loopback    = Hardware self-test looping frames back at the port for validation'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-mds-trouble-esc', 'docs/san/cisco/mds/troubleshooting/escalation/index.md', 'Cisco MDS — Troubleshooting Escalation')
def _cisco_mds_trouble_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco MDS — Troubleshooting Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('Escalation path for MDS issues: internal triage → Cisco TAC → hardware RMA process.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Internal Triage (L1/L2)'), bMid(L2, R2, 'Cisco TAC Escalation (L3)'))))
    lines.append(R(merge(bMid(L1, R1, 'Confirm scope: single or fabric'), bMid(L2, R2, 'Open SR: severity 1-4'))))
    lines.append(R(merge(bMid(L1, R1, 'Collect: show tech-support'), bMid(L2, R2, 'Attach tech-support bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'Check recent changes: config'), bMid(L2, R2, 'TAC remote: Cisco WebEx'))))
    lines.append(R(merge(bMid(L1, R1, 'Check Cisco advisories: PSIRT'), bMid(L2, R2, 'ISSU patch if bug confirmed'))))
    lines.append(R(merge(bMid(L1, R1, 'Isolate: disable suspect port'), bMid(L2, R2, 'Hardware RMA if ASIC/SFP'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Internal triage captures state; TAC escalation requires SR + bundle within 30 min'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Criteria'), bMid(L2, R2, 'Recovery Actions'))))
    lines.append(R(merge(bMid(L1, R1, 'Sev 1: production I/O impacted'), bMid(L2, R2, 'ISSU: non-disruptive upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Sev 2: degraded redundancy'), bMid(L2, R2, 'Reload module: line card'))))
    lines.append(R(merge(bMid(L1, R1, 'Sev 3: intermittent errors'), bMid(L2, R2, 'SFP swap: hot-plug capable'))))
    lines.append(R(merge(bMid(L1, R1, 'Sev 4: config question'), bMid(L2, R2, 'Zone rollback: saved config'))))
    lines.append(R(merge(bMid(L1, R1, 'Always log start/end actions'), bMid(L2, R2, 'Post-mortem: RCA document'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS chassis · SFP transceivers · ISL fiber · RMA spare parts · management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SR             = Service Request; Cisco TAC case identifier'))
    lines.append(txt_row('TAC            = Technical Assistance Center; Cisco support organization'))
    lines.append(txt_row('PSIRT          = Product Security Incident Response Team; Cisco security advisories'))
    lines.append(txt_row('ISSU           = In-Service Software Upgrade; NX-OS/MDS upgrade without reboot'))
    lines.append(txt_row('RMA            = Return Merchandise Authorization; defective hardware replacement'))
    lines.append(txt_row('Severity 1     = Production outage; Cisco commits to 1-hour response SLA'))
    lines.append(txt_row('tech-support   = All-in-one diagnostic bundle uploaded to Cisco CX Cloud'))
    lines.append(txt_row('RCA            = Root Cause Analysis; post-incident document identifying root failure'))
    lines.append(txt_row('Zone rollback  = Reverting to a previously saved zoneset configuration'))
    lines.append(txt_row('Module reload  = Restarting a line card without rebooting the chassis'))
    lines.append(txt_row('Hot-plug SFP   = Transceiver replaceable while port is active (no chassis power-off)'))
    lines.append(txt_row('Cisco WebEx    = Collaboration tool used for TAC remote-assist sessions'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-arch', 'docs/san/cisco/nexus-dashboard/architecture/index.md', 'Cisco Nexus Dashboard — Architecture Overview')
def _cisco_nd_arch():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Architecture Overview'))
    lines.append(txt_row())
    lines.append(txt_row('Clustered platform hosting NDFC, NDI, and NDO as microservice apps on Kubernetes.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Architecture'), bMid(L2, R2, 'Hosted Applications'))))
    lines.append(R(merge(bMid(L1, R1, 'Primary: 3-node minimum'), bMid(L2, R2, 'NDFC: SAN/LAN fabric control'))))
    lines.append(R(merge(bMid(L1, R1, 'Worker nodes: scale capacity'), bMid(L2, R2, 'NDI: network insights/assurance'))))
    lines.append(R(merge(bMid(L1, R1, 'Kubernetes: container runtime'), bMid(L2, R2, 'NDO: multi-site orchestrator'))))
    lines.append(R(merge(bMid(L1, R1, 'etcd: distributed state store'), bMid(L2, R2, 'Apps deployed as Helm charts'))))
    lines.append(R(merge(bMid(L1, R1, 'Storage: Ceph or external NFS'), bMid(L2, R2, 'Per-app RBAC isolation'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('ND cluster provides platform; apps (NDFC/NDI/NDO) run independently on top'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Interfaces'), bMid(L2, R2, 'HA and Resilience'))))
    lines.append(R(merge(bMid(L1, R1, 'Management: OOB Ethernet'), bMid(L2, R2, 'Quorum: 2 of 3 nodes up'))))
    lines.append(R(merge(bMid(L1, R1, 'Data: in-band fabric VLAN'), bMid(L2, R2, 'App restart: K8s self-heal'))))
    lines.append(R(merge(bMid(L1, R1, 'VIP: cluster virtual IP'), bMid(L2, R2, 'Node failure: auto rebalance'))))
    lines.append(R(merge(bMid(L1, R1, 'App port: HTTPS 443'), bMid(L2, R2, 'Backup: schedule to remote'))))
    lines.append(R(merge(bMid(L1, R1, 'Inter-node: cluster fabric'), bMid(L2, R2, 'Upgrade: rolling node-by-node'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('UCS/virtual servers (3+ nodes) · management switch · ToR switches · NFS/Ceph storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('NDFC           = Nexus Dashboard Fabric Controller; manages SAN and LAN fabrics'))
    lines.append(txt_row('NDI            = Nexus Dashboard Insights; assurance and telemetry analytics'))
    lines.append(txt_row('NDO            = Nexus Dashboard Orchestrator; multi-site ACI policy orchestration'))
    lines.append(txt_row('Kubernetes     = Container orchestration platform underlying ND cluster'))
    lines.append(txt_row('etcd           = Distributed key-value store used by Kubernetes for cluster state'))
    lines.append(txt_row('Ceph           = Distributed storage system providing persistent volumes to apps'))
    lines.append(txt_row('VIP            = Virtual IP; single cluster entry point for management access'))
    lines.append(txt_row('Quorum         = Minimum node count (2 of 3) for cluster to remain operational'))
    lines.append(txt_row('Helm chart     = Kubernetes application packaging format used by ND apps'))
    lines.append(txt_row('OOB management = Out-of-Band network; separate from fabric data path'))
    lines.append(txt_row('Worker node    = Additional ND node added beyond 3 primaries for scale'))
    lines.append(txt_row('Rolling upgrade= Upgrade one node at a time to maintain cluster availability'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-arch-how', 'docs/san/cisco/nexus-dashboard/architecture/how-it-works/index.md', 'Cisco Nexus Dashboard — How It Works')
def _cisco_nd_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('ND cluster discovers fabric sites, streams telemetry, and orchestrates multi-site policy.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Site Onboarding'), bMid(L2, R2, 'Telemetry Pipeline'))))
    lines.append(R(merge(bMid(L1, R1, 'Add APIC/NDFC/switches'), bMid(L2, R2, 'gRPC streaming from switches'))))
    lines.append(R(merge(bMid(L1, R1, 'Credentials: REST API auth'), bMid(L2, R2, 'NDI: flow, latency, anomaly'))))
    lines.append(R(merge(bMid(L1, R1, 'Site health: continuous poll'), bMid(L2, R2, 'Kafka bus: event routing'))))
    lines.append(R(merge(bMid(L1, R1, 'Reachability: ICMP + REST'), bMid(L2, R2, 'Elasticsearch: query store'))))
    lines.append(R(merge(bMid(L1, R1, 'Discovered: fabric topology'), bMid(L2, R2, 'Retention: configurable days'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Sites added to ND; apps query ND APIs to retrieve topology and telemetry data'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Policy Orchestration (NDO)'), bMid(L2, R2, 'App Interactions'))))
    lines.append(R(merge(bMid(L1, R1, 'Template: define EPGs/BDs'), bMid(L2, R2, 'NDFC: SAN zone push via REST'))))
    lines.append(R(merge(bMid(L1, R1, 'Deploy: push to remote APIC'), bMid(L2, R2, 'NDI: anomaly alert webhooks'))))
    lines.append(R(merge(bMid(L1, R1, 'Delta: only changed objects'), bMid(L2, R2, 'NDO: ACI multi-site sync'))))
    lines.append(R(merge(bMid(L1, R1, 'Rollback: prior template ver'), bMid(L2, R2, 'Shared services: SSO/RBAC'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit: deploy history log'), bMid(L2, R2, 'API gateway: single endpoint'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster nodes · fabric switches (Nexus/MDS) · APIC cluster · management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('gRPC           = Google Remote Procedure Call; used for high-speed telemetry streaming'))
    lines.append(txt_row('Kafka          = Distributed event streaming platform; routes telemetry within ND'))
    lines.append(txt_row('Elasticsearch  = Search/analytics engine storing historical telemetry for NDI'))
    lines.append(txt_row('APIC           = Application Policy Infrastructure Controller; ACI fabric controller'))
    lines.append(txt_row('EPG            = Endpoint Group; ACI policy construct grouping VMs or physical hosts'))
    lines.append(txt_row('BD             = Bridge Domain; Layer 2 forwarding domain in ACI'))
    lines.append(txt_row('NDO template   = Policy definition object deployed to one or more APIC sites'))
    lines.append(txt_row('Delta deploy   = Only objects that changed since last deploy are pushed to APIC'))
    lines.append(txt_row('Rollback       = Revert site config to a previous NDO template version'))
    lines.append(txt_row('SSO            = Single Sign-On; shared auth across NDFC, NDI, NDO apps'))
    lines.append(txt_row('REST API       = HTTP-based interface used by ND to communicate with fabric sites'))
    lines.append(txt_row('API gateway    = Single HTTPS endpoint routing requests to correct ND app'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-arch-int', 'docs/san/cisco/nexus-dashboard/architecture/integrations/index.md', 'Cisco Nexus Dashboard — Architecture Integrations')
def _cisco_nd_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('ND integrates with identity providers, SIEM, monitoring tools, and cloud platforms.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity Integrations'), bMid(L2, R2, 'Monitoring Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP: user/group sync'), bMid(L2, R2, 'Syslog: event forwarding'))))
    lines.append(R(merge(bMid(L1, R1, 'RADIUS: AAA auth'), bMid(L2, R2, 'SNMP: trap generation'))))
    lines.append(R(merge(bMid(L1, R1, 'TACACS+: per-cmd accounting'), bMid(L2, R2, 'Webhook: alert delivery'))))
    lines.append(R(merge(bMid(L1, R1, 'SAML 2.0: SSO with IdP'), bMid(L2, R2, 'Email: SMTP notification'))))
    lines.append(R(merge(bMid(L1, R1, 'Cisco ISE: device posture'), bMid(L2, R2, 'Splunk/SIEM: syslog TLS'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('IdP and AAA integrate at cluster level; monitoring integrations are per-app'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cloud Integrations'), bMid(L2, R2, 'Cisco Ecosystem'))))
    lines.append(R(merge(bMid(L1, R1, 'Intersight: infra management'), bMid(L2, R2, 'APIC: ACI policy source'))))
    lines.append(R(merge(bMid(L1, R1, 'AWS/Azure: cloud site add'), bMid(L2, R2, 'DCNM/NDFC: SAN/LAN fabric'))))
    lines.append(R(merge(bMid(L1, R1, 'VMware vCenter: VM aware'), bMid(L2, R2, 'Tetration/Secure Workload'))))
    lines.append(R(merge(bMid(L1, R1, 'Terraform: infra-as-code API'), bMid(L2, R2, 'ThousandEyes: WAN assurance'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API: programmable mgmt'), bMid(L2, R2, 'AppDynamics: app telemetry'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster · IdP/AAA server · SIEM · Intersight · cloud connectors · APIC cluster'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SAML 2.0       = Security Assertion Markup Language; federated SSO protocol'))
    lines.append(txt_row('Intersight     = Cisco cloud management SaaS for UCS and HCI infrastructure'))
    lines.append(txt_row('Tetration      = Cisco workload security analytics (now Secure Workload)'))
    lines.append(txt_row('ThousandEyes   = Cisco network intelligence platform for WAN path monitoring'))
    lines.append(txt_row('AppDynamics    = Cisco APM platform; correlates app and network performance'))
    lines.append(txt_row('ISE            = Identity Services Engine; network access policy and posture'))
    lines.append(txt_row('REST API       = Representational State Transfer API; ND primary programmability'))
    lines.append(txt_row('Terraform      = IaC tool; Cisco ND provider available for automation'))
    lines.append(txt_row('APIC           = Application Policy Infrastructure Controller; manages ACI fabric'))
    lines.append(txt_row('Webhook        = HTTP callback delivering alert payload to external systems'))
    lines.append(txt_row('Syslog TLS     = Encrypted syslog transport using TLS to SIEM'))
    lines.append(txt_row('VM-aware       = ND correlates network paths with vCenter VM identifiers'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-ops-backup', 'docs/san/cisco/nexus-dashboard/operations/backup-restore/index.md', 'Cisco Nexus Dashboard — Operations Backup Restore')
def _cisco_nd_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Operations Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('Cluster configuration backup to remote storage; restore via UI or CLI for DR recovery.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Backup Configuration'), bMid(L2, R2, 'Backup Scope'))))
    lines.append(R(merge(bMid(L1, R1, 'Remote: SCP or NFS target'), bMid(L2, R2, 'Cluster config: all node data'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: daily/weekly cron'), bMid(L2, R2, 'App data: NDFC/NDI/NDO'))))
    lines.append(R(merge(bMid(L1, R1, 'Encryption: AES-256 at rest'), bMid(L2, R2, 'Secrets: encrypted in backup'))))
    lines.append(R(merge(bMid(L1, R1, 'Retention: keep N backups'), bMid(L2, R2, 'Sites: site credentials incl.'))))
    lines.append(R(merge(bMid(L1, R1, 'Alert: backup success/fail'), bMid(L2, R2, 'Certificates: not included'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Schedule backup before any upgrade; verify remote target is writable'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Restore Process'), bMid(L2, R2, 'Disaster Recovery'))))
    lines.append(R(merge(bMid(L1, R1, 'Bootstrap new cluster first'), bMid(L2, R2, 'DR: rebuild cluster nodes'))))
    lines.append(R(merge(bMid(L1, R1, 'Upload backup file via UI'), bMid(L2, R2, 'Same software version req.'))))
    lines.append(R(merge(bMid(L1, R1, 'Validate: checksum verify'), bMid(L2, R2, 'IP/hostnames must match'))))
    lines.append(R(merge(bMid(L1, R1, 'Restore: node-by-node apply'), bMid(L2, R2, 'Certs re-issued after restore'))))
    lines.append(R(merge(bMid(L1, R1, 'Post-restore: verify sites'), bMid(L2, R2, 'RTO: ~2-4 hrs typical'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster nodes · remote SCP/NFS server · management network · spare hardware for DR'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SCP            = Secure Copy Protocol; encrypted file transfer to remote backup target'))
    lines.append(txt_row('NFS            = Network File System; shared storage mount for backup destination'))
    lines.append(txt_row('AES-256        = Advanced Encryption Standard 256-bit; encrypts backup archive'))
    lines.append(txt_row('Bootstrap      = Initial cluster bring-up before restoring configuration'))
    lines.append(txt_row('Checksum       = SHA hash validating backup file integrity before restore'))
    lines.append(txt_row('RTO            = Recovery Time Objective; target time to restore service'))
    lines.append(txt_row('DR             = Disaster Recovery; rebuilding ND cluster at alternate site'))
    lines.append(txt_row('Secrets        = Passwords and API keys stored encrypted within backup bundle'))
    lines.append(txt_row('Retention      = Policy defining how many backup files are kept before purging'))
    lines.append(txt_row('Site credentials= Per-site username/password ND uses to reach APIC/switches'))
    lines.append(txt_row('Certs re-issued= SSL certificates are regenerated fresh on restore; not restored'))
    lines.append(txt_row('Version match  = Restore requires identical ND software version as backup source'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-ops-cli', 'docs/san/cisco/nexus-dashboard/operations/cli-reference/index.md', 'Cisco Nexus Dashboard — Operations CLI Reference')
def _cisco_nd_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Operations CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('ND CLI accessed via SSH to node IP; used for low-level cluster operations and recovery.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Management CLI'), bMid(L2, R2, 'Service Management CLI'))))
    lines.append(R(merge(bMid(L1, R1, 'acs health: cluster status'), bMid(L2, R2, 'acs pods: list all pods'))))
    lines.append(R(merge(bMid(L1, R1, 'acs version: software version'), bMid(L2, R2, 'acs logs: container logs'))))
    lines.append(R(merge(bMid(L1, R1, 'acs cluster node: node info'), bMid(L2, R2, 'acs restart: service restart'))))
    lines.append(R(merge(bMid(L1, R1, 'acs network: interface info'), bMid(L2, R2, 'kubectl: direct K8s access'))))
    lines.append(R(merge(bMid(L1, R1, 'acs backup: trigger backup'), bMid(L2, R2, 'systemctl: OS service mgmt'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('ACS commands are ND-specific wrappers; kubectl gives raw Kubernetes access'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Diagnostic CLI'), bMid(L2, R2, 'REST API Alternative'))))
    lines.append(R(merge(bMid(L1, R1, 'acs techsupport: bundle'), bMid(L2, R2, 'GET /api/v1/version'))))
    lines.append(R(merge(bMid(L1, R1, 'ping / traceroute: net test'), bMid(L2, R2, 'GET /api/v1/cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'netstat: port listeners'), bMid(L2, R2, 'POST /api/v1/backup'))))
    lines.append(R(merge(bMid(L1, R1, 'df / top: resource usage'), bMid(L2, R2, 'API token: Bearer auth'))))
    lines.append(R(merge(bMid(L1, R1, 'journalctl: systemd logs'), bMid(L2, R2, 'Swagger UI: /apidocs'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster nodes (SSH access) · management Ethernet · OOB jump host'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ACS            = Application Centric Stack; ND-native CLI toolset for cluster ops'))
    lines.append(txt_row('kubectl        = Kubernetes CLI; direct control of pods, deployments, namespaces'))
    lines.append(txt_row('acs health     = Shows cluster quorum, node state, and service health summary'))
    lines.append(txt_row('acs techsupport= Generates diagnostic bundle equivalent to GUI tech-support'))
    lines.append(txt_row('systemctl      = Linux systemd service manager; controls OS-level ND services'))
    lines.append(txt_row('journalctl     = Linux systemd log viewer; queries node-level service logs'))
    lines.append(txt_row('Swagger UI     = Interactive REST API documentation hosted at /apidocs on ND'))
    lines.append(txt_row('Bearer auth    = HTTP Authorization header with JWT token for REST API calls'))
    lines.append(txt_row('netstat        = Network statistics; shows open ports and active connections'))
    lines.append(txt_row('Pod            = Kubernetes workload unit; each ND microservice runs in a pod'))
    lines.append(txt_row('Namespace      = Kubernetes logical partition isolating app resources'))
    lines.append(txt_row('REST API       = Preferred programmatic interface; CLI used for break-glass ops'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-ops-common', 'docs/san/cisco/nexus-dashboard/operations/common-issues/index.md', 'Cisco Nexus Dashboard — Operations Common Issues')
def _cisco_nd_ops_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Operations Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Frequent ND operational issues: cluster quorum loss, app failures, site disconnects.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Issues'), bMid(L2, R2, 'App Failures'))))
    lines.append(R(merge(bMid(L1, R1, 'Quorum lost: 2 nodes down'), bMid(L2, R2, 'NDFC pod crash-looping'))))
    lines.append(R(merge(bMid(L1, R1, 'etcd split-brain: net partition'), bMid(L2, R2, 'NDI no telemetry: gRPC down'))))
    lines.append(R(merge(bMid(L1, R1, 'Node offline: NIC/cable fault'), bMid(L2, R2, 'NDO deploy stuck: APIC busy'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk full: log or data volume'), bMid(L2, R2, 'OOM: pod evicted by K8s'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP drift: cert validation fail'), bMid(L2, R2, 'App upgrade failed: retry'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Cluster health checked first; then app-level pod logs for targeted troubleshooting'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Site Connectivity Issues'), bMid(L2, R2, 'Resolution Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Site unreachable: REST timeout'), bMid(L2, R2, 'acs health: cluster state'))))
    lines.append(R(merge(bMid(L1, R1, 'Cred expired: 401 from APIC'), bMid(L2, R2, 'acs logs: pod error messages'))))
    lines.append(R(merge(bMid(L1, R1, 'SSL cert expired: handshake'), bMid(L2, R2, 'kubectl describe pod detail'))))
    lines.append(R(merge(bMid(L1, R1, 'Firewall: port 443 blocked'), bMid(L2, R2, 'Renew cert or rotate creds'))))
    lines.append(R(merge(bMid(L1, R1, 'Version mismatch: app incompat'), bMid(L2, R2, 'TAC: if quorum unrecoverable'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster nodes · management switches · APIC cluster · NTP server · firewall'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Quorum         = Minimum node count for cluster consensus; loss stops all writes'))
    lines.append(txt_row('etcd           = K8s state store; split-brain means two halves disagree on state'))
    lines.append(txt_row('Split-brain    = Network partition causing cluster halves to diverge independently'))
    lines.append(txt_row('Crash-loop     = Pod repeatedly starting and failing; check logs for root cause'))
    lines.append(txt_row('OOM            = Out Of Memory; Kubernetes evicts pod when node memory exhausted'))
    lines.append(txt_row('gRPC           = Streaming protocol; NDI telemetry stops if gRPC session drops'))
    lines.append(txt_row('NDO deploy     = Pushing policy templates to remote APIC; can time out if APIC busy'))
    lines.append(txt_row('NTP drift      = Time skew between nodes breaks TLS cert validation'))
    lines.append(txt_row('401 error      = HTTP Unauthorized; credentials rejected by APIC REST API'))
    lines.append(txt_row('Version mismatch= ND app version incompatible with connected fabric controller'))
    lines.append(txt_row('kubectl describe= Kubernetes command showing pod events and failure reason'))
    lines.append(txt_row('TAC            = Cisco Technical Assistance Center; escalate unrecoverable faults'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-ops-health', 'docs/san/cisco/nexus-dashboard/operations/health-checks/index.md', 'Cisco Nexus Dashboard — Operations Health Checks')
def _cisco_nd_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Operations Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('Routine health verification covering cluster nodes, hosted apps, and connected sites.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Health Checks'), bMid(L2, R2, 'App Health Checks'))))
    lines.append(R(merge(bMid(L1, R1, 'acs health: all nodes green'), bMid(L2, R2, 'NDFC: SAN services running'))))
    lines.append(R(merge(bMid(L1, R1, 'Node CPU/memory < 70%'), bMid(L2, R2, 'NDI: telemetry collection on'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk usage < 80% on all vols'), bMid(L2, R2, 'NDO: site sync status OK'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP: all nodes synced < 1s'), bMid(L2, R2, 'Pods: all Running, none Error'))))
    lines.append(R(merge(bMid(L1, R1, 'etcd: leader elected + healthy'), bMid(L2, R2, 'App version: check for updates'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Cluster health verified before app health; failing node impacts all apps'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Site Connectivity Checks'), bMid(L2, R2, 'Security Health Checks'))))
    lines.append(R(merge(bMid(L1, R1, 'All sites: Connected status'), bMid(L2, R2, 'SSL certs: expiry > 30 days'))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric site: APIC version OK'), bMid(L2, R2, 'AAA servers: reachable'))))
    lines.append(R(merge(bMid(L1, R1, 'Telemetry: data flowing NDI'), bMid(L2, R2, 'RBAC: review user access'))))
    lines.append(R(merge(bMid(L1, R1, 'Latency: < 150ms to site'), bMid(L2, R2, 'Audit log: no anomalies'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup: last success < 24h'), bMid(L2, R2, 'Backup: encryption verified'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster nodes · management switch · NTP server · APIC · AAA server · backup target'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('acs health     = ND CLI command showing cluster node and service health summary'))
    lines.append(txt_row('etcd leader    = Elected node managing all etcd writes; loss blocks cluster updates'))
    lines.append(txt_row('NTP sync       = All nodes must agree on time within 1 second for TLS to work'))
    lines.append(txt_row('Pod state      = Kubernetes pod lifecycle: Pending → Running → Error/CrashLoopBackOff'))
    lines.append(txt_row('NDO site sync  = Verification that template state matches deployed APIC config'))
    lines.append(txt_row('NDI telemetry  = Streaming flow and latency data from switches to NDI analytics'))
    lines.append(txt_row('SSL expiry     = TLS cert expiration causing connection failures if not renewed'))
    lines.append(txt_row('AAA reachable  = RADIUS/TACACS+ server responds; local fallback active if not'))
    lines.append(txt_row('Audit log      = Records of all user actions and API calls for compliance review'))
    lines.append(txt_row('Disk usage     = Storage consumed on each ND node; Elasticsearch fills fast'))
    lines.append(txt_row('Latency 150ms  = Recommended maximum RTT between ND cluster and remote site'))
    lines.append(txt_row('Backup success = Verification that scheduled backup completed and is retrievable'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-ops-install', 'docs/san/cisco/nexus-dashboard/operations/install-upgrade/index.md', 'Cisco Nexus Dashboard — Operations Install Upgrade')
def _cisco_nd_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Operations Install & Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('ND cluster initial build and rolling upgrade process with pre/post validation steps.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Initial Install'), bMid(L2, R2, 'Prerequisites'))))
    lines.append(R(merge(bMid(L1, R1, 'Deploy OVA/ISO: 3 node min'), bMid(L2, R2, 'Hardware: 16 vCPU/64GB RAM'))))
    lines.append(R(merge(bMid(L1, R1, 'Bootstrap: node 1 as primary'), bMid(L2, R2, 'Storage: 500GB min per node'))))
    lines.append(R(merge(bMid(L1, R1, 'Join: nodes 2+3 to cluster'), bMid(L2, R2, 'Network: OOB + data VLANs'))))
    lines.append(R(merge(bMid(L1, R1, 'Configure: IP, NTP, DNS'), bMid(L2, R2, 'NTP: synced before install'))))
    lines.append(R(merge(bMid(L1, R1, 'Install apps: NDFC/NDI/NDO'), bMid(L2, R2, 'Cisco CCO: download images'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Bootstrap node 1 first; other nodes join via cluster join token; apps installed last'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Process'), bMid(L2, R2, 'Post-Upgrade Validation'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup: before upgrade'), bMid(L2, R2, 'acs health: all nodes green'))))
    lines.append(R(merge(bMid(L1, R1, 'Upload image: UI or CLI'), bMid(L2, R2, 'Apps: verify running'))))
    lines.append(R(merge(bMid(L1, R1, 'Rolling: one node at a time'), bMid(L2, R2, 'Sites: all connected'))))
    lines.append(R(merge(bMid(L1, R1, 'Duration: ~45 min/node'), bMid(L2, R2, 'Telemetry: flowing to NDI'))))
    lines.append(R(merge(bMid(L1, R1, 'Apps auto-upgrade post-cluster'), bMid(L2, R2, 'Rollback: restore backup'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND nodes (UCS/VM) · management switch · NTP/DNS server · CCO download server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OVA            = Open Virtualization Appliance; VMware VM image format for ND'))
    lines.append(txt_row('ISO            = Disk image for bare-metal ND node installation'))
    lines.append(txt_row('Bootstrap      = First-node initialization creating the cluster with initial config'))
    lines.append(txt_row('Cluster join token= One-time secret additional nodes use to securely join cluster'))
    lines.append(txt_row('Rolling upgrade= ND upgrades one node at a time; cluster stays available throughout'))
    lines.append(txt_row('CCO            = Cisco Connection Online; software download portal'))
    lines.append(txt_row('App auto-upgrade= After cluster upgrade, apps detect new platform and self-upgrade'))
    lines.append(txt_row('OOB VLAN       = Management VLAN on dedicated out-of-band network'))
    lines.append(txt_row('Data VLAN      = In-band network VLAN used for site-to-ND app communication'))
    lines.append(txt_row('NTP pre-sync   = NTP must be configured and synced before cluster forms'))
    lines.append(txt_row('acs health     = Validates all nodes report green status after upgrade completes'))
    lines.append(txt_row('Rollback       = Only via backup restore; no in-place cluster downgrade supported'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-ops-scripts', 'docs/san/cisco/nexus-dashboard/operations/scripts/index.md', 'Cisco Nexus Dashboard — Operations Scripts')
def _cisco_nd_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Operations Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('Automation scripts for ND backup, health reporting, site management, and upgrades.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'REST API Scripting'), bMid(L2, R2, 'Common Script Tasks'))))
    lines.append(R(merge(bMid(L1, R1, 'Auth: POST /api/v1/auth'), bMid(L2, R2, 'Backup trigger: scheduled'))))
    lines.append(R(merge(bMid(L1, R1, 'Bearer token: reuse 60 min'), bMid(L2, R2, 'Health report: node + pods'))))
    lines.append(R(merge(bMid(L1, R1, 'Python requests / curl'), bMid(L2, R2, 'Site status: all connected'))))
    lines.append(R(merge(bMid(L1, R1, 'Ansible: Cisco ND modules'), bMid(L2, R2, 'Cert expiry: alert < 30d'))))
    lines.append(R(merge(bMid(L1, R1, 'Terraform: ND provider'), bMid(L2, R2, 'Disk usage: alert > 80%'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('All scripts authenticate via REST API token; Ansible modules wrap the same endpoints'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Ansible Automation'), bMid(L2, R2, 'Script Best Practices'))))
    lines.append(R(merge(bMid(L1, R1, 'Collection: cisco.nd'), bMid(L2, R2, 'Store creds: Vault/secrets'))))
    lines.append(R(merge(bMid(L1, R1, 'nd_site: manage sites'), bMid(L2, R2, 'Idempotent: check before set'))))
    lines.append(R(merge(bMid(L1, R1, 'nd_backup: trigger backup'), bMid(L2, R2, 'Logging: timestamp each run'))))
    lines.append(R(merge(bMid(L1, R1, 'nd_version: query version'), bMid(L2, R2, 'Error handling: retry logic'))))
    lines.append(R(merge(bMid(L1, R1, 'nd_policy: deploy templates'), bMid(L2, R2, 'Schedule: cron or Ansible AWX'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster · automation server (Ansible/AWX) · secrets vault · management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('cisco.nd       = Ansible Galaxy collection providing ND-specific modules'))
    lines.append(txt_row('Bearer token   = JWT returned by ND auth endpoint; passed in Authorization header'))
    lines.append(txt_row('Idempotent     = Script produces same result whether run once or multiple times'))
    lines.append(txt_row('AWX            = Ansible Tower open-source; schedules and tracks playbook runs'))
    lines.append(txt_row('Terraform ND   = HashiCorp provider allowing IaC management of ND resources'))
    lines.append(txt_row('Vault          = HashiCorp secrets manager; stores API credentials securely'))
    lines.append(txt_row('nd_site        = Ansible module managing ND site onboarding/removal'))
    lines.append(txt_row('nd_backup      = Ansible module triggering and verifying ND configuration backup'))
    lines.append(txt_row('REST endpoint  = /api/v1/* paths; full CRUD for all ND resources'))
    lines.append(txt_row('Token TTL      = ND tokens expire after 60 minutes; scripts must re-authenticate'))
    lines.append(txt_row('Retry logic    = Script re-attempts failed API calls with backoff before alerting'))
    lines.append(txt_row('Cert expiry check= Script querying ND cert store and alerting when < 30 days remain'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-sec-access', 'docs/san/cisco/nexus-dashboard/security/access-control/index.md', 'Cisco Nexus Dashboard — Security Access Control')
def _cisco_nd_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Security Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC model with local and AAA-backed users; per-app roles scoped to tenant or site.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'User Management'), bMid(L2, R2, 'Role Model'))))
    lines.append(R(merge(bMid(L1, R1, 'Local users: ND-native DB'), bMid(L2, R2, 'Admin: full cluster access'))))
    lines.append(R(merge(bMid(L1, R1, 'Remote: LDAP/RADIUS/TACACS+'), bMid(L2, R2, 'Operator: read + limited write'))))
    lines.append(R(merge(bMid(L1, R1, 'Groups: mapped to ND roles'), bMid(L2, R2, 'Read-only: view only'))))
    lines.append(R(merge(bMid(L1, R1, 'Password policy: enforce cmplx'), bMid(L2, R2, 'App roles: per NDFC/NDI/NDO'))))
    lines.append(R(merge(bMid(L1, R1, 'Session timeout: configurable'), bMid(L2, R2, 'Site scope: per-site access'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Roles assigned at cluster level; app-specific roles further restrict within each app'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'API Access Control'), bMid(L2, R2, 'Audit'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API: Bearer token auth'), bMid(L2, R2, 'Login events: success/fail'))))
    lines.append(R(merge(bMid(L1, R1, 'Token TTL: 60 min default'), bMid(L2, R2, 'Config changes: who+what'))))
    lines.append(R(merge(bMid(L1, R1, 'Service accounts: dedicated'), bMid(L2, R2, 'API calls: logged per user'))))
    lines.append(R(merge(bMid(L1, R1, 'IP allowlist: restrict mgmt'), bMid(L2, R2, 'Export: syslog to SIEM'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA: via SAML IdP only'), bMid(L2, R2, 'Retention: 90-day default'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster · LDAP/RADIUS/TACACS+ server · SAML IdP · SIEM · management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC           = Role-Based Access Control; maps users/groups to permitted actions'))
    lines.append(txt_row('LDAP group map = Mapping LDAP group DN to an ND role for automatic assignment'))
    lines.append(txt_row('App role       = Role scoped to a specific ND app (NDFC/NDI/NDO) not cluster-wide'))
    lines.append(txt_row('Site scope     = Restricting a user to only manage specific onboarded sites'))
    lines.append(txt_row('Service account= Dedicated ND user for automation; not used for human login'))
    lines.append(txt_row('IP allowlist   = Network ACL restricting management access to known source IPs'))
    lines.append(txt_row('MFA            = Multi-Factor Auth; enforced by SAML IdP (not natively by ND)'))
    lines.append(txt_row('Token TTL      = JWT lifetime; default 60 min; reduce for higher security posture'))
    lines.append(txt_row('Password complexity= Minimum length, upper/lower/digit/special char requirements'))
    lines.append(txt_row('Session timeout= Idle period after which UI session is automatically terminated'))
    lines.append(txt_row('SIEM export    = Forwarding ND audit logs via syslog TLS to Splunk or similar'))
    lines.append(txt_row('Audit retention= How long ND retains access logs before purging (default 90 days)'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-sec-auth', 'docs/san/cisco/nexus-dashboard/security/authentication/index.md', 'Cisco Nexus Dashboard — Security Authentication')
def _cisco_nd_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Security Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('ND supports local, LDAP, RADIUS, TACACS+, and SAML 2.0 authentication providers.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Local Authentication'), bMid(L2, R2, 'Remote Authentication'))))
    lines.append(R(merge(bMid(L1, R1, 'Built-in user DB on cluster'), bMid(L2, R2, 'RADIUS: PAP/CHAP auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Bcrypt password hashing'), bMid(L2, R2, 'TACACS+: per-cmd accounting'))))
    lines.append(R(merge(bMid(L1, R1, 'Min 8 chars + complexity'), bMid(L2, R2, 'LDAP: bind DN + search base'))))
    lines.append(R(merge(bMid(L1, R1, 'Account lockout: 5 attempts'), bMid(L2, R2, 'SAML 2.0: IdP-initiated SSO'))))
    lines.append(R(merge(bMid(L1, R1, 'Local fallback if remote down'), bMid(L2, R2, 'Priority: order of providers'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Remote providers tried in priority order; local fallback activates if all unreachable'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SAML SSO Flow'), bMid(L2, R2, 'Session Management'))))
    lines.append(R(merge(bMid(L1, R1, 'SP-initiated: ND redirects'), bMid(L2, R2, 'JWT: signed bearer token'))))
    lines.append(R(merge(bMid(L1, R1, 'Assertion: groups → ND roles'), bMid(L2, R2, 'Token TTL: 60 min default'))))
    lines.append(R(merge(bMid(L1, R1, 'Signing cert: IdP public key'), bMid(L2, R2, 'Refresh: re-auth required'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA enforced at IdP layer'), bMid(L2, R2, 'Concurrent sessions: allowed'))))
    lines.append(R(merge(bMid(L1, R1, 'Metadata URL: auto-import'), bMid(L2, R2, 'Idle timeout: UI logout'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster · RADIUS/TACACS+ server · LDAP/AD server · SAML IdP · management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SAML 2.0       = XML-based SSO standard; ND acts as Service Provider'))
    lines.append(txt_row('IdP            = Identity Provider; issues SAML assertions (e.g. Okta, Azure AD)'))
    lines.append(txt_row('SP-initiated   = User clicks ND login, is redirected to IdP for authentication'))
    lines.append(txt_row('SAML assertion = XML document from IdP containing user identity and group claims'))
    lines.append(txt_row('Bcrypt         = Adaptive password hashing algorithm; resistant to brute-force'))
    lines.append(txt_row('Bind DN        = LDAP distinguished name used by ND to query the directory'))
    lines.append(txt_row('Search base    = LDAP OU from which ND searches for user and group objects'))
    lines.append(txt_row('JWT            = JSON Web Token; signed session credential returned after auth'))
    lines.append(txt_row('Account lockout= Disables login after 5 consecutive failed authentication attempts'))
    lines.append(txt_row('PAP            = Password Authentication Protocol; sends password in clear over TLS'))
    lines.append(txt_row('Local fallback = Admin-account local auth if all remote servers are unreachable'))
    lines.append(txt_row('Metadata URL   = SAML IdP endpoint exposing signing cert and SSO URL automatically'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-sec-enc', 'docs/san/cisco/nexus-dashboard/security/encryption/index.md', 'Cisco Nexus Dashboard — Security Encryption')
def _cisco_nd_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Security Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('TLS for all management interfaces; AES-256 for backup data and secrets at rest.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'In-Transit Encryption'), bMid(L2, R2, 'At-Rest Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'HTTPS: TLS 1.2+ on port 443'), bMid(L2, R2, 'Backup: AES-256-GCM'))))
    lines.append(R(merge(bMid(L1, R1, 'Inter-node: mTLS cluster bus'), bMid(L2, R2, 'Secrets: etcd encrypted'))))
    lines.append(R(merge(bMid(L1, R1, 'Syslog: TLS transport opt.'), bMid(L2, R2, 'Passwords: bcrypt hashed'))))
    lines.append(R(merge(bMid(L1, R1, 'API: TLS cert validation'), bMid(L2, R2, 'Keys: stored in K8s secret'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable TLS 1.0/1.1 + RC4'), bMid(L2, R2, 'Disk: OS-level encryption opt'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('All external traffic TLS 1.2+; inter-node cluster traffic uses mutual TLS'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Management'), bMid(L2, R2, 'Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Default: self-signed on init'), bMid(L2, R2, 'FIPS 140-2 mode: optional'))))
    lines.append(R(merge(bMid(L1, R1, 'Replace: upload CA-signed cert'), bMid(L2, R2, 'Cipher suite: AES-GCM pref.'))))
    lines.append(R(merge(bMid(L1, R1, 'SAN: cluster VIP + hostnames'), bMid(L2, R2, 'TLS 1.3: supported on newer'))))
    lines.append(R(merge(bMid(L1, R1, 'Expiry alert: UI + syslog'), bMid(L2, R2, 'Audit: TLS handshake errors'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-renew: not built-in'), bMid(L2, R2, 'Annual cipher review policy'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster nodes · CA server · management switch · backup storage target'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('mTLS           = Mutual TLS; both client and server present certificates'))
    lines.append(txt_row('AES-256-GCM    = Symmetric cipher providing confidentiality + integrity for backups'))
    lines.append(txt_row('etcd encrypted = Kubernetes encrypts secret objects in etcd using AES-CBC/GCM'))
    lines.append(txt_row('K8s secret     = Kubernetes object storing sensitive data (keys, tokens, passwords)'))
    lines.append(txt_row('FIPS 140-2     = US federal crypto module standard; disables non-compliant algos'))
    lines.append(txt_row('SAN cert       = TLS cert with Subject Alternative Names for VIP and all node FQDNs'))
    lines.append(txt_row('Self-signed    = Default ND cert; must be replaced with CA-signed for production'))
    lines.append(txt_row('Bcrypt         = One-way hash for passwords; not reversible even with DB access'))
    lines.append(txt_row('TLS 1.3        = Latest TLS version; eliminates weak handshake options'))
    lines.append(txt_row('Cipher suite   = Negotiated algorithm set: key exchange + auth + encryption + hash'))
    lines.append(txt_row('Auto-renew     = ND does not auto-renew certs; monitor expiry and replace manually'))
    lines.append(txt_row('Disk encryption= OS-level feature (LUKS) optional on bare-metal ND deployments'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-sec-hard', 'docs/san/cisco/nexus-dashboard/security/hardening/index.md', 'Cisco Nexus Dashboard — Security Hardening')
def _cisco_nd_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Security Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('Hardening checklist: replace default certs, restrict access, enable AAA, audit logging.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Platform Hardening'), bMid(L2, R2, 'Network Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Replace self-signed cert'), bMid(L2, R2, 'IP allowlist: mgmt source'))))
    lines.append(R(merge(bMid(L1, R1, 'Enable SAML/LDAP: no local'), bMid(L2, R2, 'OOB mgmt: dedicated VLAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable default admin: rename'), bMid(L2, R2, 'Firewall: port 443 only'))))
    lines.append(R(merge(bMid(L1, R1, 'Password policy: max strength'), bMid(L2, R2, 'NTP auth: keyed NTP'))))
    lines.append(R(merge(bMid(L1, R1, 'Session timeout: 15 min idle'), bMid(L2, R2, 'Syslog TLS: to SIEM'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Replace certs and enable AAA first; then restrict network access; then audit'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'App-Level Hardening'), bMid(L2, R2, 'Ongoing Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'NDFC: disable unused features'), bMid(L2, R2, 'Quarterly access review'))))
    lines.append(R(merge(bMid(L1, R1, 'NDO: limit deploy approvers'), bMid(L2, R2, 'Cert expiry: monitor < 30d'))))
    lines.append(R(merge(bMid(L1, R1, 'NDI: restrict telemetry read'), bMid(L2, R2, 'Patch: apply within 30 days'))))
    lines.append(R(merge(bMid(L1, R1, 'API: service accounts only'), bMid(L2, R2, 'PSIRT: subscribe advisories'))))
    lines.append(R(merge(bMid(L1, R1, 'Minimal roles: least privilege'), bMid(L2, R2, 'Backup: verify monthly'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster · CA server · SAML IdP · SIEM · NTP server · OOB management switch'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Self-signed cert= Default ND cert; must be replaced with CA-signed before production'))
    lines.append(txt_row('IP allowlist   = Network-level restriction on which source IPs can reach port 443'))
    lines.append(txt_row('OOB VLAN       = Dedicated out-of-band management network isolated from data path'))
    lines.append(txt_row('PSIRT          = Cisco Product Security Incident Response Team; publishes CVEs'))
    lines.append(txt_row('Least privilege= Each user/service account has only the minimum required permissions'))
    lines.append(txt_row('Session timeout= Idle UI session automatically terminated after inactivity period'))
    lines.append(txt_row('NTP auth       = Keyed NTP ensuring time sync from trusted server only'))
    lines.append(txt_row('Service account= Dedicated ND user for automation; separate from human accounts'))
    lines.append(txt_row('Deploy approver= NDO role permitted to push templates to production APIC sites'))
    lines.append(txt_row('Access review  = Periodic audit of all user accounts and role assignments'))
    lines.append(txt_row('Patch window   = Defined maintenance period for applying ND software updates'))
    lines.append(txt_row('Syslog TLS     = Encrypted syslog stream forwarding audit events to SIEM'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-trouble-common', 'docs/san/cisco/nexus-dashboard/troubleshooting/common-issues/index.md', 'Cisco Nexus Dashboard — Troubleshooting Common Issues')
def _cisco_nd_trouble_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Troubleshooting Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Most frequent ND issues: cluster quorum, app failures, site disconnects, auth errors.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Problems'), bMid(L2, R2, 'Authentication Failures'))))
    lines.append(R(merge(bMid(L1, R1, 'Node unreachable: NIC/cable'), bMid(L2, R2, 'Login fail: AAA unreachable'))))
    lines.append(R(merge(bMid(L1, R1, 'Quorum lost: 2+ nodes down'), bMid(L2, R2, 'SAML error: cert mismatch'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk full: Elasticsearch log'), bMid(L2, R2, 'Token expired: re-auth API'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP drift: TLS cert failure'), bMid(L2, R2, 'LDAP: bind DN wrong'))))
    lines.append(R(merge(bMid(L1, R1, 'etcd crash: restore backup'), bMid(L2, R2, '401 REST: creds rotated'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Check acs health first; auth issues need AAA server reachability confirmed'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Site and App Issues'), bMid(L2, R2, 'Resolution Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Site offline: REST timeout'), bMid(L2, R2, 'acs health: check nodes'))))
    lines.append(R(merge(bMid(L1, R1, 'NDFC: pod crash-looping'), bMid(L2, R2, 'acs logs <app>: pod errors'))))
    lines.append(R(merge(bMid(L1, R1, 'NDI: no telemetry data'), bMid(L2, R2, 'Renew cert or fix NTP'))))
    lines.append(R(merge(bMid(L1, R1, 'NDO: deploy stuck/timeout'), bMid(L2, R2, 'Restart app: acs restart'))))
    lines.append(R(merge(bMid(L1, R1, 'SSL cert expired: 503 error'), bMid(L2, R2, 'TAC: quorum unrecoverable'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster nodes · management switch · NTP · AAA server · APIC · firewall'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('acs health     = ND CLI command; shows cluster node and service health at a glance'))
    lines.append(txt_row('Quorum         = Requires 2 of 3 nodes; loss makes cluster read-only'))
    lines.append(txt_row('etcd crash     = State-store failure; requires cluster restore from backup'))
    lines.append(txt_row('Disk full      = Elasticsearch retains telemetry; purge old data or expand volume'))
    lines.append(txt_row('NTP drift      = Clock skew breaks TLS validation and JWT expiry calculations'))
    lines.append(txt_row('Crash-loop     = Pod restarting repeatedly; acs logs shows root cause'))
    lines.append(txt_row('503 error      = HTTP Service Unavailable; typically expired TLS cert on ND'))
    lines.append(txt_row('401 error      = HTTP Unauthorized; API credentials rotated but not updated in ND'))
    lines.append(txt_row('Bind DN        = LDAP distinguished name ND uses to connect; fails if password changed'))
    lines.append(txt_row('SAML cert mismatch= IdP signing cert changed but not updated in ND SP config'))
    lines.append(txt_row('acs restart    = ND CLI command to restart a specific app service gracefully'))
    lines.append(txt_row('TAC            = Cisco TAC; escalate cluster quorum loss or etcd corruption'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-trouble-diag', 'docs/san/cisco/nexus-dashboard/troubleshooting/diagnostics/index.md', 'Cisco Nexus Dashboard — Troubleshooting Diagnostics')
def _cisco_nd_trouble_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Troubleshooting Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('ND diagnostic tools: acs CLI, pod logs, tech-support bundle, and REST API queries.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Diagnostics'), bMid(L2, R2, 'App Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'acs health: node summary'), bMid(L2, R2, 'acs logs <app>: pod logs'))))
    lines.append(R(merge(bMid(L1, R1, 'acs cluster node: node detail'), bMid(L2, R2, 'kubectl describe pod: events'))))
    lines.append(R(merge(bMid(L1, R1, 'acs network: interface check'), bMid(L2, R2, 'kubectl get pods -A: all pods'))))
    lines.append(R(merge(bMid(L1, R1, 'df -h: disk usage per volume'), bMid(L2, R2, 'App UI: built-in health page'))))
    lines.append(R(merge(bMid(L1, R1, 'top: CPU/memory per process'), bMid(L2, R2, 'REST: GET /api/v1/faults'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Start with acs health for cluster state; then kubectl/acs logs for app root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Tech-Support Collection'), bMid(L2, R2, 'Network Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'acs techsupport: full bundle'), bMid(L2, R2, 'ping: node to node'))))
    lines.append(R(merge(bMid(L1, R1, 'GUI: Admin → Tech Support'), bMid(L2, R2, 'curl -k: REST endpoint test'))))
    lines.append(R(merge(bMid(L1, R1, 'Includes: logs, configs, DB'), bMid(L2, R2, 'netstat: port listeners'))))
    lines.append(R(merge(bMid(L1, R1, 'Upload: Cisco CX Cloud TAC'), bMid(L2, R2, 'traceroute: path to site'))))
    lines.append(R(merge(bMid(L1, R1, 'Size: 1-5 GB typical'), bMid(L2, R2, 'nslookup: DNS resolution'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster nodes · management switch · DNS server · TAC upload target (CX Cloud)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('acs health     = Cluster-wide health summary: nodes, quorum, disk, NTP status'))
    lines.append(txt_row('acs logs       = Streams log output from a named ND application pod'))
    lines.append(txt_row('kubectl        = Kubernetes CLI; describes pods, deployments, events in detail'))
    lines.append(txt_row('acs techsupport= Generates comprehensive diagnostic archive for TAC analysis'))
    lines.append(txt_row('CX Cloud       = Cisco customer experience portal; TAC case file upload target'))
    lines.append(txt_row('GET /api/v1/faults= REST endpoint listing active fault objects on the cluster'))
    lines.append(txt_row('kubectl describe= Shows pod spec, status, and recent events (OOM, image pull errors)'))
    lines.append(txt_row('df -h          = Linux command showing disk usage per mounted volume'))
    lines.append(txt_row('curl -k        = Test HTTPS endpoint without cert validation; verify REST response'))
    lines.append(txt_row('Crash-loop     = Pod state where container repeatedly exits; root cause in logs'))
    lines.append(txt_row('nslookup       = Verify ND can resolve site hostnames and AAA server FQDNs'))
    lines.append(txt_row('Tech-support   = All-in-one bundle; includes etcd snapshot, pod logs, cluster state'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('cisco-nd-trouble-esc', 'docs/san/cisco/nexus-dashboard/troubleshooting/escalation/index.md', 'Cisco Nexus Dashboard — Troubleshooting Escalation')
def _cisco_nd_trouble_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Cisco Nexus Dashboard — Troubleshooting Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('Escalation path for ND: internal triage → Cisco TAC → cluster restore or rebuild.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Internal Triage (L1/L2)'), bMid(L2, R2, 'Cisco TAC (L3)'))))
    lines.append(R(merge(bMid(L1, R1, 'Confirm impact: cluster/app'), bMid(L2, R2, 'Open SR: severity 1-4'))))
    lines.append(R(merge(bMid(L1, R1, 'Collect: acs techsupport'), bMid(L2, R2, 'Upload bundle to CX Cloud'))))
    lines.append(R(merge(bMid(L1, R1, 'Check: recent config changes'), bMid(L2, R2, 'TAC WebEx: remote session'))))
    lines.append(R(merge(bMid(L1, R1, 'Check: Cisco PSIRT advisories'), bMid(L2, R2, 'Patch or restore if directed'))))
    lines.append(R(merge(bMid(L1, R1, 'Try: acs restart failing app'), bMid(L2, R2, 'Rebuild cluster: last resort'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Collect tech-support before any restart; TAC needs state data from failure moment'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Criteria'), bMid(L2, R2, 'Recovery Actions'))))
    lines.append(R(merge(bMid(L1, R1, 'Sev 1: all apps unavailable'), bMid(L2, R2, 'App restart: acs restart'))))
    lines.append(R(merge(bMid(L1, R1, 'Sev 2: one app failed'), bMid(L2, R2, 'Backup restore: full cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'Sev 3: degraded telemetry'), bMid(L2, R2, 'Node replace: rejoin cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'Sev 4: config question'), bMid(L2, R2, 'Rebuild: deploy + restore'))))
    lines.append(R(merge(bMid(L1, R1, 'Always document timeline'), bMid(L2, R2, 'Post-mortem: RCA document'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ND cluster nodes · backup storage · management network · spare node for rebuild'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SR             = Service Request; Cisco TAC case number'))
    lines.append(txt_row('TAC            = Technical Assistance Center; Cisco L3 support'))
    lines.append(txt_row('CX Cloud       = Cisco portal for SR management and tech-support file upload'))
    lines.append(txt_row('PSIRT          = Cisco security advisory team; check for relevant CVEs first'))
    lines.append(txt_row('acs restart    = Gracefully restarts a named ND app without rebooting the node'))
    lines.append(txt_row('Backup restore = Full cluster config recovery from most recent scheduled backup'))
    lines.append(txt_row('Node replace   = Remove failed node, add new node, rejoin cluster automatically'))
    lines.append(txt_row('Rebuild        = Deploy fresh cluster and restore from backup; last-resort recovery'))
    lines.append(txt_row('Severity 1     = Production down; Cisco SLA: 1-hour initial response'))
    lines.append(txt_row('RCA            = Root Cause Analysis; post-incident document for future prevention'))
    lines.append(txt_row('Timeline       = Chronological log of symptoms, actions, and outcomes for TAC'))
    lines.append(txt_row('Tech-support   = Collected before any recovery action; preserves failure state'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
