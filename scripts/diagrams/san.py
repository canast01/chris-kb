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
