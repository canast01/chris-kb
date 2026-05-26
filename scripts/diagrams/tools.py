"""
Tools (Confluence, Git, Jira, ServiceNow) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

# ── Tools Root ────────────────────────────────────────────────────────────────

@kb_diagram(
    'tools-root',
    'docs/tools/index.md',
    'Tools Platform Overview — Confluence, Git, Jira, ServiceNow',
)
def tools_root():
    """Tools Platform Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    B3_L, B3_R = 3, 50
    B4_L, B4_R = 53, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Tools Platform Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Enterprise Tools Platform')))
    lines.append(R(bMid(IV_L, IV_R, 'Collaboration, version control, issue tracking, and ITSM services')))
    lines.append(R(bMid(IV_L, IV_R, 'Atlassian DC stack: Confluence + Jira on PostgreSQL, shared NFS home, Tomcat app tier')))
    lines.append(R(bMid(IV_L, IV_R, 'Git: distributed VCS hosted on GitHub/GitLab/Bitbucket with SSH and HTTPS access')))
    lines.append(R(bMid(IV_L, IV_R, 'ServiceNow: SaaS ITSM — Incident, Change, CMDB, ITOM with MID Server on-prem link')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Four tools cover the full DevOps lifecycle from code to production to incident'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Confluence'),
        bMid(B2_L, B2_R, 'Git'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Team wiki and knowledge base'),
        bMid(B2_L, B2_R, 'Distributed version control'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Spaces · Pages · Templates'),
        bMid(B2_L, B2_R, 'Branches · Commits · Tags'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Macros · Page tree · REST API'),
        bMid(B2_L, B2_R, 'Pull requests · Hooks · LFS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP / SAML SSO auth'),
        bMid(B2_L, B2_R, 'SSH keys / PAT auth'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Lucene search · XML backup'),
        bMid(B2_L, B2_R, 'GitHub · GitLab · Bitbucket'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B3_L, B3_R), bTop(B4_L, B4_R))))
    lines.append(R(merge(
        bMid(B3_L, B3_R, 'Jira'),
        bMid(B4_L, B4_R, 'ServiceNow'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, 'Issue and project tracking'),
        bMid(B4_L, B4_R, 'SaaS ITSM platform'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, 'Scrum · Kanban · JQL'),
        bMid(B4_L, B4_R, 'Incident · Change · CMDB'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, 'Epics · Stories · Sprints'),
        bMid(B4_L, B4_R, 'MID Server: on-prem bridge'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, 'Workflows · Screens · Fields'),
        bMid(B4_L, B4_R, 'Integration Hub REST flows'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, 'REST API v3 · Webhooks'),
        bMid(B4_L, B4_R, 'SAML SSO · GlideScript'),
    )))
    lines.append(R(merge(bBot(B3_L, B3_R), bBot(B4_L, B4_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Atlassian DC on vSphere VMs · NFS shared home · PostgreSQL DB VMs · ServiceNow MID Server VM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Confluence   = Atlassian wiki platform; Data Center edition on Tomcat + PostgreSQL/Oracle'))
    lines.append(txt_row('Jira         = Atlassian issue tracker; Scrum/Kanban/SM projects with JQL query language'))
    lines.append(txt_row('Git          = distributed VCS; every clone is a full repo with local commit history'))
    lines.append(txt_row('ServiceNow   = SaaS ITSM; Incident, Problem, Change, Request, CMDB on Now Platform'))
    lines.append(txt_row('MID Server   = Management/Instrumentation/Discovery; on-prem Java agent for ServiceNow'))
    lines.append(txt_row('LDAP         = Lightweight Directory Access Protocol; centralised user auth directory'))
    lines.append(txt_row('SAML SSO     = Security Assertion Markup Language; federated single sign-on standard'))
    lines.append(txt_row('PAT          = Personal Access Token; scoped credential replacing password for Git/API'))
    lines.append(txt_row('JQL          = Jira Query Language; SQL-like syntax for filtering and searching issues'))
    lines.append(txt_row('Lucene       = Apache full-text search engine embedded in Confluence and Jira'))
    lines.append(txt_row('Tomcat       = Apache Tomcat; Java servlet container hosting Confluence/Jira web apps'))
    lines.append(txt_row('Integration  = ServiceNow Integration Hub; low-code REST/SOAP/scripted integrations'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Confluence ────────────────────────────────────────────────────────────────

@kb_diagram(
    'tools-confluence',
    'docs/tools/confluence/index.md',
    'Confluence Overview — wiki platform, Data Center components, auth, backup',
)
def tools_confluence():
    """Confluence Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Confluence — Wiki Platform Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Atlassian Confluence — Data Center Edition')))
    lines.append(R(bMid(IV_L, IV_R, 'Enterprise wiki: Spaces → Pages → Page Tree with inline comments and versions')))
    lines.append(R(bMid(IV_L, IV_R, 'App tier: Tomcat on port 8090 (HTTP) / 443 (HTTPS via reverse proxy)')))
    lines.append(R(bMid(IV_L, IV_R, 'Data tier: PostgreSQL or Oracle DB + shared NFS home (attachments/indexes)')))
    lines.append(R(bMid(IV_L, IV_R, 'Search: Lucene index rebuilt from DB on demand; re-index from admin panel')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Confluence tiers span web, application, database, and shared storage layers'))
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
        bMid(B1_L, B1_R, 'Tomcat app server'),
        bMid(B2_L, B2_R, 'Install / Upgrade'),
        bMid(B3_L, B3_R, 'LDAP user directory'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'PostgreSQL DB tier'),
        bMid(B2_L, B2_R, 'Backup and restore'),
        bMid(B3_L, B3_R, 'SAML SSO / MFA'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NFS shared home'),
        bMid(B2_L, B2_R, 'Health checks'),
        bMid(B3_L, B3_R, 'Space permissions'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Lucene search index'),
        bMid(B2_L, B2_R, 'CLI reference'),
        bMid(B3_L, B3_R, 'TLS / HTTPS config'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'REST API · Macros'),
        bMid(B2_L, B2_R, 'Scripts · Procedures'),
        bMid(B3_L, B3_R, 'Hardening guide'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere VMs: app nodes · DB VM (PostgreSQL) · NFS fileserver for shared home · Load balancer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Space        = top-level container for pages; can be personal, project, or team scoped'))
    lines.append(txt_row('Page tree    = hierarchical page structure within a space; parent/child relationships'))
    lines.append(txt_row('Macro        = dynamic content block (e.g. Table of Contents, Include Page, Status)'))
    lines.append(txt_row('Shared home  = NFS mount shared by all DC nodes; stores attachments and search index'))
    lines.append(txt_row('Lucene       = embedded full-text index; must be rebuilt after DB restores'))
    lines.append(txt_row('JDBC         = Java Database Connectivity; Confluence connects to DB via JDBC URL'))
    lines.append(txt_row('DC node      = one Confluence app server in a Data Center cluster behind a load balancer'))
    lines.append(txt_row('Hazelcast    = in-memory data grid; Confluence DC uses it for cache clustering'))
    lines.append(txt_row('SAML         = Security Assertion Markup Language; Confluence delegates auth to IdP'))
    lines.append(txt_row('XML backup   = Confluence site export (Admin > Backup); not for large prod restores'))
    lines.append(txt_row('Atlassian DC = Data Center licensing tier; supports clustering and high availability'))
    lines.append(txt_row('REST API     = Confluence v2 REST API; spaces/pages/content endpoints on port 8090'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'tools-confluence-architecture',
    'docs/tools/confluence/architecture/index.md',
    'Confluence Architecture Overview — tiers, clustering, data flow',
)
def tools_confluence_architecture():
    """Confluence Architecture Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Confluence — Architecture Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Confluence Data Center Architecture')))
    lines.append(R(bMid(IV_L, IV_R, 'Load balancer → multiple Tomcat app nodes → shared PostgreSQL DB + NFS home')))
    lines.append(R(bMid(IV_L, IV_R, 'Each node is stateless for HTTP; shared NFS provides attachments and Lucene index')))
    lines.append(R(bMid(IV_L, IV_R, 'Hazelcast cluster: in-memory cache synchronisation across all app nodes')))
    lines.append(R(bMid(IV_L, IV_R, 'Synchrony: collaborative editing service co-located or standalone on port 8091')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  App nodes scale horizontally; DB and NFS are the single-source-of-truth tiers'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Application Tier'),
        bMid(B2_L, B2_R, 'Data Tier'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Tomcat JVM: heap 4-8 GB'),
        bMid(B2_L, B2_R, 'PostgreSQL 14+ primary'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Hazelcast: node discovery'),
        bMid(B2_L, B2_R, 'DB replica for read scale'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Synchrony: collab edits'),
        bMid(B2_L, B2_R, 'NFS shared home mount'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Lucene: local index copy'),
        bMid(B2_L, B2_R, 'Attachments on NFS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'REST API endpoint: 8090'),
        bMid(B2_L, B2_R, 'JDBC: confluence user'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Session: Hazelcast-backed'),
        bMid(B2_L, B2_R, 'DB backup: pg_dump nightly'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Application tier is horizontally scalable; data tier requires HA at DB and NFS level'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Design Standards', 'Integrations', 'Ports', 'Protocols'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Request lifecycle', 'Node sizing guide', 'LDAP/SAML IdP', '8090 HTTP app', 'AJP / HTTP/S'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Search indexing', 'DB schema design', 'Jira app link', '5432 PostgreSQL', 'JDBC TCP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Collab editing', 'NFS sizing', 'CI/CD webhooks', '8091 Synchrony', 'WebSocket'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cache sync flow', 'HA topology', 'REST API clients', '443 HTTPS LB', 'TLS 1.2+'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('2+ vSphere VMs per app node · DB VM with SSD storage · NFS datastore · L4 load balancer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Hazelcast    = distributed in-memory data grid; Confluence uses it for session + cache sync'))
    lines.append(txt_row('Synchrony    = real-time collaborative editing service bundled with Confluence DC'))
    lines.append(txt_row('AJP          = Apache JServ Protocol; Tomcat connector for Apache httpd reverse proxy'))
    lines.append(txt_row('JDBC         = Java Database Connectivity; connection pool managed by Confluence'))
    lines.append(txt_row('Lucene       = Apache search library; Confluence maintains local index per node'))
    lines.append(txt_row('NFS          = Network File System; shared home for attachments across DC nodes'))
    lines.append(txt_row('pg_dump      = PostgreSQL native backup utility; produces SQL or custom-format dump'))
    lines.append(txt_row('JVM heap     = memory allocated to Confluence JVM; set in setenv.sh (recommended 4-8 GB)'))
    lines.append(txt_row('DC node      = single Confluence app server instance in a clustered DC deployment'))
    lines.append(txt_row('Load balancer= L4/L7 device distributing HTTP requests across Confluence app nodes'))
    lines.append(txt_row('Shared home  = confluence.home path mounted from NFS; same path on all nodes'))
    lines.append(txt_row('App link     = Atlassian application link connecting Confluence to Jira for auth/data'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'tools-confluence-arch-how-it-works',
    'docs/tools/confluence/architecture/how-it-works/index.md',
    'Confluence How It Works — request lifecycle, search, collaborative editing',
)
def tools_confluence_arch_how_it_works():
    """Confluence How It Works — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    PD1, PD2, PD3 = 26, 51, 76

    lines = []
    lines.append(title_border(W2, 'Confluence — How It Works'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Confluence Request and Data Flow')))
    lines.append(R(bMid(IV_L, IV_R, 'Browser → LB → Tomcat (Confluence app) → DB read/write + NFS attachment I/O')))
    lines.append(R(bMid(IV_L, IV_R, 'Page render: Velocity templates transform wiki markup to HTML on each request')))
    lines.append(R(bMid(IV_L, IV_R, 'Search: Lucene index on NFS; rebuilt with full re-index from Admin > Content Indexing')))
    lines.append(R(bMid(IV_L, IV_R, 'Collab editing: Synchrony service (port 8091) manages OT over WebSocket')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Confluence processes three parallel flows: HTTP, search indexing, and collaborative edits'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HTTP Request Flow'),
        bMid(B2_L, B2_R, 'Search Flow'),
        bMid(B3_L, B3_R, 'Collab Edit Flow'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Browser → HTTPS LB'),
        bMid(B2_L, B2_R, 'Create/edit triggers'),
        bMid(B3_L, B3_R, 'User opens editor'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LB → Tomcat node'),
        bMid(B2_L, B2_R, 'Lucene index update'),
        bMid(B3_L, B3_R, 'WebSocket → Synchrony'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Auth: session/SAML'),
        bMid(B2_L, B2_R, 'Async indexing queue'),
        bMid(B3_L, B3_R, 'OT conflict resolve'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DB query via JDBC'),
        bMid(B2_L, B2_R, 'Shared index on NFS'),
        bMid(B3_L, B3_R, 'DB draft save'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NFS: attachments'),
        bMid(B2_L, B2_R, 'Per-node cache warm'),
        bMid(B3_L, B3_R, 'Publish: DB commit'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Velocity → HTML resp'),
        bMid(B2_L, B2_R, 'Re-index: admin UI'),
        bMid(B3_L, B3_R, 'Version stored in DB'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  All three flows converge on the shared PostgreSQL DB as the authoritative data store'))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Tomcat JVM VMs · PostgreSQL VM with fast SSD · NFS datastore · network load balancer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Velocity     = Apache Velocity; Java template engine used to render Confluence HTML pages'))
    lines.append(txt_row('OT           = Operational Transformation; algorithm resolving concurrent edit conflicts'))
    lines.append(txt_row('Synchrony    = Confluence collab editing service; manages document state via WebSocket'))
    lines.append(txt_row('Lucene index = inverted index of page content; enables fast full-text search'))
    lines.append(txt_row('Re-index     = full rebuild of Lucene index from DB; needed after restore or corruption'))
    lines.append(txt_row('JDBC pool    = connection pool (HikariCP) managed by Confluence for DB access'))
    lines.append(txt_row('SAML         = Confluence delegates authentication to IdP (Okta/AD FS/Ping) via SAML 2.0'))
    lines.append(txt_row('NFS mount    = shared home directory; same path on every DC node for attachment access'))
    lines.append(txt_row('Draft        = Synchrony saves drafts to DB before publish to avoid data loss'))
    lines.append(txt_row('Page version = every save increments version counter; prior versions retained in DB'))
    lines.append(txt_row('Attachment   = binary file stored on NFS under confluence.home/attachments'))
    lines.append(txt_row('LB session   = load balancer uses sticky sessions or shared Hazelcast session store'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'tools-confluence-arch-design',
    'docs/tools/confluence/architecture/design-standards/index.md',
    'Confluence Design Standards — sizing, HA topology, naming, retention',
)
def tools_confluence_arch_design():
    """Confluence Design Standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Confluence — Design Standards'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Confluence Design and Sizing Standards')))
    lines.append(R(bMid(IV_L, IV_R, 'Node sizing: min 8 vCPU / 16 GB RAM per app node; JVM heap 4-6 GB (-Xmx)')))
    lines.append(R(bMid(IV_L, IV_R, 'DB sizing: 4 vCPU / 8 GB RAM; SSD storage; autovacuum tuned for Confluence')))
    lines.append(R(bMid(IV_L, IV_R, 'NFS sizing: 500 GB starting point; monitor confluence.home/attachments growth')))
    lines.append(R(bMid(IV_L, IV_R, 'HA topology: 2+ app nodes behind LB with sticky sessions; PostgreSQL streaming replica')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Design standards define the minimum viable and production-grade deployment topologies'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Infrastructure Standards'),
        bMid(B2_L, B2_R, 'Configuration Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'App node: 8 vCPU / 16 GB'),
        bMid(B2_L, B2_R, 'JVM: -Xms2g -Xmx6g'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DB: 4 vCPU / 8 GB SSD'),
        bMid(B2_L, B2_R, 'DB pool: max 60 conns'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NFS: 10 Gbps, low latency'),
        bMid(B2_L, B2_R, 'Tomcat: max threads 200'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LB: sticky session rules'),
        bMid(B2_L, B2_R, 'Scheduler: cluster-aware'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Replica: streaming repl'),
        bMid(B2_L, B2_R, 'Backup: nightly pg_dump'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DR: cross-site NFS sync'),
        bMid(B2_L, B2_R, 'Retention: 30-day backup'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere HA cluster · SSD-backed datastores · 10 GbE NFS network · dedicated DB VLAN'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('-Xmx         = JVM max heap flag; set in setenv.sh; controls Confluence memory ceiling'))
    lines.append(txt_row('Sticky session = LB routes same user to same node; needed for non-Hazelcast session stores'))
    lines.append(txt_row('autovacuum   = PostgreSQL background process; reclaims dead row storage (critical for Jira/Confluence)'))
    lines.append(txt_row('Streaming replica = PostgreSQL standby receiving WAL stream for hot-standby reads and failover'))
    lines.append(txt_row('DB pool      = JDBC connection pool; Confluence default uses c3p0; tune maxPoolSize'))
    lines.append(txt_row('Tomcat threads = max simultaneous HTTP request handlers; tune based on concurrent users'))
    lines.append(txt_row('Scheduler    = Confluence background job scheduler; DC-aware to avoid duplicate execution'))
    lines.append(txt_row('pg_dump      = PostgreSQL dump tool; use --format=custom for parallel restore with pg_restore'))
    lines.append(txt_row('NFS latency  = shared home latency directly impacts Confluence page render time'))
    lines.append(txt_row('Attachment   = binary stored in NFS; large attachments slow backup and NFS throughput'))
    lines.append(txt_row('Cluster node = each Confluence instance in DC must share the same DB URL and home path'))
    lines.append(txt_row('WAL          = Write-Ahead Log; PostgreSQL durability mechanism, source for replication'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'tools-confluence-arch-integrations',
    'docs/tools/confluence/architecture/integrations/index.md',
    'Confluence Integrations — Jira app links, LDAP, SAML, REST API, webhooks',
)
def tools_confluence_arch_integrations():
    """Confluence Integrations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2

    lines = []
    lines.append(title_border(W2, 'Confluence — Architecture Integrations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Confluence Integration Landscape')))
    lines.append(R(bMid(IV_L, IV_R, 'Atlassian application links: Confluence ↔ Jira for cross-product macro rendering')))
    lines.append(R(bMid(IV_L, IV_R, 'Directory: LDAP/AD user sync; SAML SSO via Okta/AD FS/Ping IdP')))
    lines.append(R(bMid(IV_L, IV_R, 'REST API: v2 endpoints for spaces, pages, content; PAT or Basic auth')))
    lines.append(R(bMid(IV_L, IV_R, 'Webhooks: HTTP POST events on page create/update/delete to external systems')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Integrations connect Confluence outward to auth, issue tracking, and automation systems'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Directory & Auth'),
        bMid(B2_L, B2_R, 'Atlassian Ecosystem'),
        bMid(B3_L, B3_R, 'External Systems'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP: user/group sync'),
        bMid(B2_L, B2_R, 'Jira: app link OAuth'),
        bMid(B3_L, B3_R, 'REST API: automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SAML SSO: Okta/ADFS'),
        bMid(B2_L, B2_R, 'Jira macro: issue list'),
        bMid(B3_L, B3_R, 'Webhooks: CI/CD events'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Crowd: SSO for DC'),
        bMid(B2_L, B2_R, 'Bamboo: build results'),
        bMid(B3_L, B3_R, 'Slack: notifications'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'MFA: TOTP via Okta'),
        bMid(B2_L, B2_R, 'Bitbucket: code macro'),
        bMid(B3_L, B3_R, 'Email: SMTP alerts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Local accounts: fallback'),
        bMid(B2_L, B2_R, 'Atlassian Access: audit'),
        bMid(B3_L, B3_R, 'PDF export: server-side'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('LDAP/AD DC servers · IdP (Okta/AD FS) · SMTP relay · network connectivity to Jira/Bitbucket'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('App link     = Atlassian trusted relationship between two products enabling OAuth and macros'))
    lines.append(txt_row('Crowd        = Atlassian SSO server; centralises auth for Confluence, Jira, Bitbucket'))
    lines.append(txt_row('SAML SSO     = Confluence acts as Service Provider; IdP handles credential validation'))
    lines.append(txt_row('LDAP sync    = Confluence polls LDAP on a schedule to import users and group memberships'))
    lines.append(txt_row('Webhook      = outbound HTTP POST triggered by Confluence page events'))
    lines.append(txt_row('Jira macro   = {jira} macro embeds live issue data from linked Jira instance'))
    lines.append(txt_row('PAT          = Personal Access Token; recommended over Basic auth for REST API access'))
    lines.append(txt_row('Atlassian Access = cloud governance layer for audit log, mobile policies, user provisioning'))
    lines.append(txt_row('PDF export   = Confluence server-side render; requires matching CSS for accurate output'))
    lines.append(txt_row('SMTP relay   = outbound mail for page notifications, comment alerts, admin emails'))
    lines.append(txt_row('OAuth        = app link uses OAuth 1.0a or OAuth 2.0 for cross-product API trust'))
    lines.append(txt_row('MFA          = multi-factor auth enforced at IdP level (Okta/ADFS); Confluence trusts IdP'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Confluence remaining pages ────────────────────────────────────────────────

W2 = 103

@kb_diagram('tools-confluence-ops', 'docs/tools/confluence/operations/index.md', 'Confluence operations overview')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'Confluence — Operations Overview'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Daily Checks'), bMid(B2_L, B2_R, 'Weekly Tasks'), bMid(B3_L, B3_R, 'Monthly Tasks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service status'), bMid(B2_L, B2_R, 'Space health'), bMid(B3_L, B3_R, 'License audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup verify'), bMid(B2_L, B2_R, 'User audit'), bMid(B3_L, B3_R, 'Plugin updates'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Disk usage'), bMid(B2_L, B2_R, 'Check logs'), bMid(B3_L, B3_R, 'Performance review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert triage'), bMid(B2_L, B2_R, 'Reindex if slow'), bMid(B3_L, B3_R, 'Security review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Confluence server/DC VMs · PostgreSQL or Oracle DB · file system for attachments'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Service status = Confluence app server running; check via systemctl or process monitor'))
    lines.append(txt_row('Backup verify = Confirm backup job completed; test restore quarterly'))
    lines.append(txt_row('Disk usage = Monitor home directory and attachments; alert at 80%'))
    lines.append(txt_row('Reindex = Rebuilding Confluence search index; needed after bulk import or corruption'))
    lines.append(txt_row('Plugin = Confluence app/add-on; update via UPM (Universal Plugin Manager)'))
    lines.append(txt_row('UPM = Universal Plugin Manager; Confluence built-in app marketplace management'))
    lines.append(txt_row('Space = Confluence top-level container for pages; each team typically has a space'))
    lines.append(txt_row('License audit = Verifying active user count against licensed seats'))
    lines.append(txt_row('PostgreSQL = Recommended database for Confluence Server/DC deployments'))
    lines.append(txt_row('Home directory = CONFLUENCE_HOME; stores attachments, backups, and indexes'))
    lines.append(txt_row('Performance review = Monthly check of heap usage, GC pauses, and page load times'))
    lines.append(txt_row('Security review = Monthly check of admin accounts, anonymous access, and HTTPS config'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-ops-backup', 'docs/tools/confluence/operations/backup-restore/index.md', 'Confluence backup and restore')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Confluence — Backup and Restore'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup Strategy'), bMid(B2_L, B2_R, 'Restore Procedure'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB dump nightly'), bMid(B2_L, B2_R, 'Stop Confluence'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Home dir snapshot'), bMid(B2_L, B2_R, 'Restore DB first'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'XML backup (weekly)'), bMid(B2_L, B2_R, 'Restore home dir'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify daily'), bMid(B2_L, B2_R, 'Start Confluence'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Off-site copy'), bMid(B2_L, B2_R, 'Verify via UI'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Confluence server · PostgreSQL DB · CONFLUENCE_HOME on NFS or SAN · backup to NFS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('XML backup = Confluence built-in export; content only; portable but slow for large instances'))
    lines.append(txt_row('DB dump = pg_dump for PostgreSQL; fastest and most reliable backup method'))
    lines.append(txt_row('CONFLUENCE_HOME = File system directory containing attachments, config, and indexes'))
    lines.append(txt_row('Home dir snapshot = Filesystem or VM snapshot of CONFLUENCE_HOME for quick restore'))
    lines.append(txt_row('Restore order = Always restore DB before restoring home directory'))
    lines.append(txt_row('Verify restore = Log in, check recent pages and attachments exist after restore'))
    lines.append(txt_row('Off-site copy = Backup archive copied to secondary location or object store'))
    lines.append(txt_row('Quarterly test = Full restore to test environment quarterly to verify recoverability'))
    lines.append(txt_row('RTO = Recovery Time Objective; target time from failure to restored service'))
    lines.append(txt_row('RPO = Recovery Point Objective; maximum acceptable data loss in time'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-ops-cli', 'docs/tools/confluence/operations/cli-reference/index.md', 'Confluence CLI reference')
def _():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Confluence — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Confluence admin CLI — run on server as confluence OS user')))
    lines.append(R(bMid(L, RR, './start-confluence.sh / ./stop-confluence.sh — start/stop application')))
    lines.append(R(bMid(L, RR, './confluence.sh status — show running/stopped state and PID')))
    lines.append(R(bMid(L, RR, 'Confluence REST API: GET /rest/api/space — list all spaces')))
    lines.append(R(bMid(L, RR, 'Confluence REST API: GET /rest/api/content?type=page — search content')))
    lines.append(R(bMid(L, RR, 'pg_dump -U confluence confluence > backup.sql — PostgreSQL backup')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('SSH to Confluence server · commands run as confluence OS user · DB on separate host'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('start-confluence.sh = Script in CONFLUENCE_INSTALL/bin/ to start the app server'))
    lines.append(txt_row('stop-confluence.sh = Graceful shutdown; waits for active sessions to complete'))
    lines.append(txt_row('REST API = Confluence programmatic interface at /rest/api; auth: Basic or OAuth'))
    lines.append(txt_row('Space REST = GET /rest/api/space returns all spaces with key, name, and type'))
    lines.append(txt_row('Content REST = GET /rest/api/content; supports CQL query for filtering'))
    lines.append(txt_row('CQL = Confluence Query Language; structured search (type=page AND space=TEAM)'))
    lines.append(txt_row('pg_dump = PostgreSQL backup utility; creates SQL dump of Confluence DB'))
    lines.append(txt_row('CONFLUENCE_INSTALL = Installation directory; contains bin/, conf/, and lib/'))
    lines.append(txt_row('CONFLUENCE_HOME = Data directory; contains attachments, indexes, and backups'))
    lines.append(txt_row('Log files = CONFLUENCE_HOME/logs/atlassian-confluence.log for app events'))
    lines.append(txt_row('catalina.out = Tomcat log; CONFLUENCE_INSTALL/logs/catalina.out'))
    lines.append(txt_row('Heap dump = -XX:+HeapDumpOnOutOfMemoryError in JVM_SUPPORT_RECOMMENDED_ARGS'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-ops-health', 'docs/tools/confluence/operations/health-checks/index.md', 'Confluence health checks')
def _():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    lines = []
    lines.append(title_border(W2, 'Confluence — Health Checks'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Application Health'), bMid(B2_L, B2_R, 'Infrastructure Health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'GET /status → OK'), bMid(B2_L, B2_R, 'DB connection'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Heap usage < 80%'), bMid(B2_L, B2_R, 'Disk < 80%'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Thread count normal'), bMid(B2_L, B2_R, 'NFS mount check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No OOM in logs'), bMid(B2_L, B2_R, 'Backup completed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Search index OK'), bMid(B2_L, B2_R, 'SMTP test'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Confluence server · PostgreSQL · NFS for home dir · SMTP relay · load balancer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GET /status = Confluence health endpoint; returns RUNNING or error state'))
    lines.append(txt_row('Heap usage = JVM heap percentage; >80% risks OOM; check via Admin > System Info'))
    lines.append(txt_row('OOM = OutOfMemoryError; kills Confluence if heap exhausted; check catalina.out'))
    lines.append(txt_row('Thread count = Active HTTP threads; high count indicates slow requests backing up'))
    lines.append(txt_row('Search index = Lucene index in CONFLUENCE_HOME/index; trigger reindex if stale'))
    lines.append(txt_row('DB connection = Confluence checks DB pool; if exhausted, pages fail to load'))
    lines.append(txt_row('NFS mount = CONFLUENCE_HOME on NFS; if unmounted, attachments return 404'))
    lines.append(txt_row('SMTP test = Send test email from Admin > Mail Servers; confirms notifications work'))
    lines.append(txt_row('Backup completed = Check CONFLUENCE_HOME/backups/ for fresh archive'))
    lines.append(txt_row('System Info = Admin > System Information; shows memory, JVM version, and config'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
