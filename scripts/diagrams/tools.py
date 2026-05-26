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


# ── Confluence Security ───────────────────────────────────────────────────────

@kb_diagram('tools-confluence-sec', 'docs/tools/confluence/security/index.md', 'Confluence security overview')
def tools_confluence_sec():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Security Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Confluence Security Domains')))
    lines.append(R(bMid(3, 99, 'Authentication: LDAP/AD sync + SAML SSO (Okta/ADFS) + local fallback accounts')))
    lines.append(R(bMid(3, 99, 'Authorisation: Space permissions + page restrictions + global group roles')))
    lines.append(R(bMid(3, 99, 'Encryption: TLS 1.2+ in transit; DB and NFS encryption at rest recommended')))
    lines.append(R(bMid(3, 99, 'Hardening: disable anonymous access, restrict admin IPs, apply security advisories')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Three security domains — identity, access, and transport — protect Confluence data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Authentication'), bMid(B2_L, B2_R, 'Access Control'), bMid(B3_L, B3_R, 'Encryption'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP/AD user sync'), bMid(B2_L, B2_R, 'Space permissions'), bMid(B3_L, B3_R, 'TLS 1.2+ HTTPS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML SSO via IdP'), bMid(B2_L, B2_R, 'Page restrictions'), bMid(B3_L, B3_R, 'DB encrypt at rest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA at IdP layer'), bMid(B2_L, B2_R, 'Group-based roles'), bMid(B3_L, B3_R, 'NFS encrypt at rest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Session management'), bMid(B2_L, B2_R, 'Admin-only IP ACL'), bMid(B3_L, B3_R, 'Key management'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PAT for API auth'), bMid(B2_L, B2_R, 'Anon access: off'), bMid(B3_L, B3_R, 'Cert rotation'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('LDAP/AD servers · IdP (Okta/ADFS) · reverse proxy (TLS termination) · DB VM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Space permission = per-space ACL: View, Add Pages, Add Comments, Admin; set per group/user'))
    lines.append(txt_row('Page restriction = overrides space perms; locks a page to specific users/groups for view/edit'))
    lines.append(txt_row('Anonymous access = global setting; disable to force login for all Confluence content'))
    lines.append(txt_row('SAML SSO        = Confluence as SP; IdP issues assertions; no password stored in Confluence'))
    lines.append(txt_row('LDAP sync       = Confluence polls AD/LDAP on schedule; imports users and group memberships'))
    lines.append(txt_row('PAT             = Personal Access Token; recommended for REST API; scoped, revocable'))
    lines.append(txt_row('Session timeout = Admin > Security Configuration; idle session expiry duration'))
    lines.append(txt_row('IP ACL          = Admin panel restrict to known corporate IP ranges for /admin endpoints'))
    lines.append(txt_row('TLS termination = reverse proxy (nginx/Apache/F5) handles TLS; Tomcat sees plain HTTP'))
    lines.append(txt_row('MFA             = enforced at IdP; Confluence trusts IdP assertion without re-checking'))
    lines.append(txt_row('Security advisory = Atlassian publishes CVEs; apply via version upgrade or patch'))
    lines.append(txt_row('Audit log       = Admin > Audit Log; tracks permission changes and admin actions'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-sec-enc', 'docs/tools/confluence/security/encryption/index.md', 'Confluence encryption')
def tools_confluence_sec_enc():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Confluence Encryption — In Transit and At Rest')))
    lines.append(R(bMid(3, 99, 'In transit: TLS 1.2+ via reverse proxy (nginx/Apache/F5); Tomcat on plain HTTP internally')))
    lines.append(R(bMid(3, 99, 'At rest: DB encryption via PostgreSQL TDE or OS-level dm-crypt/LUKS on DB volume')))
    lines.append(R(bMid(3, 99, 'NFS: encrypt NFS datastore at hypervisor or storage array level for attachments')))
    lines.append(R(bMid(3, 99, 'Secrets: DB password in confluence.cfg.xml; use vault or encrypted env vars')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Encryption must cover every data path: browser, app-to-DB, and storage volumes'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'In Transit'), bMid(B2_L, B2_R, 'At Rest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS 1.2+ at LB/proxy'), bMid(B2_L, B2_R, 'DB: dm-crypt/LUKS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HTTP internally only'), bMid(B2_L, B2_R, 'NFS: storage encrypt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP: LDAPS/StartTLS'), bMid(B2_L, B2_R, 'Backup files: GPG'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB: SSL JDBC param'), bMid(B2_L, B2_R, 'VM disk: vSphere encrypt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cert: 2048-bit RSA+'), bMid(B2_L, B2_R, 'Vault: secret mgmt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HSTS header: enabled'), bMid(B2_L, B2_R, 'Key rotation: annual'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Reverse proxy VM · Confluence app VMs · PostgreSQL VM with encrypted disk · NFS datastore'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TLS 1.2+     = Transport Layer Security; minimum version 1.2; prefer 1.3 for new deployments'))
    lines.append(txt_row('HSTS         = HTTP Strict Transport Security; forces HTTPS for all subsequent browser requests'))
    lines.append(txt_row('LDAPS        = LDAP over SSL (port 636); encrypts directory sync traffic'))
    lines.append(txt_row('SSL JDBC     = sslmode=require in JDBC URL; encrypts app-to-DB connection'))
    lines.append(txt_row('dm-crypt     = Linux kernel disk encryption; LUKS format; transparent to application'))
    lines.append(txt_row('LUKS         = Linux Unified Key Setup; standard for Linux full-disk encryption'))
    lines.append(txt_row('GPG          = GNU Privacy Guard; used to encrypt backup tar archives'))
    lines.append(txt_row('vSphere encrypt = VM encryption at hypervisor level using vSphere Native Key Provider'))
    lines.append(txt_row('Vault        = HashiCorp Vault or equivalent; stores DB passwords and API keys securely'))
    lines.append(txt_row('TDE          = Transparent Data Encryption; PostgreSQL enterprise extension or pgcrypto'))
    lines.append(txt_row('Key rotation = replacing encryption keys annually; requires planned maintenance window'))
    lines.append(txt_row('cert         = X.509 certificate; signed by internal CA or public CA (Let\'s Encrypt)'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-sec-hard', 'docs/tools/confluence/security/hardening/index.md', 'Confluence hardening')
def tools_confluence_sec_hard():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Confluence Hardening Guide')))
    lines.append(R(bMid(L, RR, 'Disable anonymous access and guest users in global permissions')))
    lines.append(R(bMid(L, RR, 'Restrict /admin path to corp IP ranges via reverse proxy or WAF rules')))
    lines.append(R(bMid(L, RR, 'Apply all Atlassian security advisories; keep within n-1 version')))
    lines.append(R(bMid(L, RR, 'Remove default admin account; use named accounts with MFA via IdP')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Hardening reduces the attack surface across network, application, and OS layers'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Application Hardening'), bMid(B2_L, B2_R, 'OS/Network Hardening'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Disable anon access'), bMid(B2_L, B2_R, 'Firewall: allow 443 only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Remove default admin'), bMid(B2_L, B2_R, 'SSH key auth only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Enforce strong passwords'), bMid(B2_L, B2_R, 'SELinux/AppArmor on'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Audit log enabled'), bMid(B2_L, B2_R, 'Minimal OS packages'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Plugin allow-list'), bMid(B2_L, B2_R, 'Regular OS patching'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Headers: CSP/HSTS/X-Frame'), bMid(B2_L, B2_R, 'WAF rules for /admin'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Reverse proxy (WAF) · Confluence VMs with SELinux · DB VM · firewall segmentation'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Anonymous access = global toggle; disable to require login for all page views'))
    lines.append(txt_row('CSP              = Content Security Policy header; prevents XSS by restricting script sources'))
    lines.append(txt_row('X-Frame-Options  = HTTP header preventing clickjacking via iframe embedding'))
    lines.append(txt_row('WAF              = Web Application Firewall; inspects HTTP and blocks malicious requests'))
    lines.append(txt_row('Plugin allow-list = restrict UPM to approved Marketplace apps; block unsigned plugins'))
    lines.append(txt_row('Audit log        = Confluence Admin > Audit Log; records admin actions and permission changes'))
    lines.append(txt_row('SELinux          = mandatory access control on RHEL/CentOS; enforcing mode recommended'))
    lines.append(txt_row('AppArmor         = MAC on Debian/Ubuntu; profile-based confinement for Tomcat process'))
    lines.append(txt_row('n-1 version      = stay within one major version behind latest; apply critical patches same-day'))
    lines.append(txt_row('Default admin    = built-in admin account in fresh installs; rename and rotate password'))
    lines.append(txt_row('SSH key auth     = disable password SSH; require public key for all admin access'))
    lines.append(txt_row('MFA              = enforced at IdP; admins must pass MFA before receiving SAML assertion'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-sec-access', 'docs/tools/confluence/security/access-control/index.md', 'Confluence access control')
def tools_confluence_sec_access():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Confluence Access Control Hierarchy')))
    lines.append(R(bMid(3, 99, 'Global permissions → Space permissions → Page restrictions (most specific wins)')))
    lines.append(R(bMid(3, 99, 'Groups managed in LDAP/AD; sync to Confluence; assign to spaces not individuals')))
    lines.append(R(bMid(3, 99, 'Page restrictions override space-level view/edit rights for sensitive content')))
    lines.append(R(bMid(3, 99, 'Admin role: Confluence Administrators group; limit to 2-3 named accounts')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Access control layers from global to page; most restrictive setting wins'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Global Permissions'), bMid(B2_L, B2_R, 'Space Permissions'), bMid(B3_L, B3_R, 'Page Restrictions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Can use Confluence'), bMid(B2_L, B2_R, 'View space'), bMid(B3_L, B3_R, 'View only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create spaces'), bMid(B2_L, B2_R, 'Add/edit pages'), bMid(B3_L, B3_R, 'Edit only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Manage users'), bMid(B2_L, B2_R, 'Add attachments'), bMid(B3_L, B3_R, 'View+Edit combo'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'System admin'), bMid(B2_L, B2_R, 'Space admin'), bMid(B3_L, B3_R, 'Inheritable'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Confluence admin'), bMid(B2_L, B2_R, 'Export/import'), bMid(B3_L, B3_R, 'Child pages apply'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('LDAP/AD for group source · Confluence DB stores permission ACLs · IdP for auth'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Global permission = instance-wide rights; set via Admin > Global Permissions'))
    lines.append(txt_row('Space permission  = per-space ACL; View/AddPages/AddComments/Admin; assign to groups'))
    lines.append(txt_row('Page restriction  = per-page ACL; overrides space for that page and optionally children'))
    lines.append(txt_row('Inheritance       = page restrictions can cascade to child pages if set during creation'))
    lines.append(txt_row('Group assignment  = best practice is to assign permissions to LDAP groups, not individuals'))
    lines.append(txt_row('Space admin       = can manage space members and page tree; cannot change global settings'))
    lines.append(txt_row('System admin      = full Confluence access including server config and mail settings'))
    lines.append(txt_row('Confluence admin  = application-level admin; can manage users, plugins, and permissions'))
    lines.append(txt_row('Anonymous access  = global toggle for unauthenticated users; default OFF in enterprise'))
    lines.append(txt_row('Can use Confluence = base permission; must be granted for any user to log in'))
    lines.append(txt_row('LDAP group sync   = groups from AD mapped to Confluence groups; updated on each poll'))
    lines.append(txt_row('Audit trail       = Admin > Audit Log records all permission changes with timestamp'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-sec-auth', 'docs/tools/confluence/security/authentication/index.md', 'Confluence authentication')
def tools_confluence_sec_auth():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Confluence Authentication Methods')))
    lines.append(R(bMid(3, 99, 'LDAP: user/group sync from AD/OpenLDAP; Confluence handles credential bind')))
    lines.append(R(bMid(3, 99, 'SAML SSO: Confluence as SP; IdP (Okta/ADFS) issues signed assertion; no password stored')))
    lines.append(R(bMid(3, 99, 'Crowd: Atlassian SSO server; centralized auth across Confluence, Jira, Bitbucket')))
    lines.append(R(bMid(3, 99, 'PAT: Personal Access Token; HTTP Bearer header; scoped; revocable via profile')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Multiple auth methods serve different user types; SSO preferred for all human login'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Human Auth Methods'), bMid(B2_L, B2_R, 'Service/API Auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML 2.0 SSO (primary)'), bMid(B2_L, B2_R, 'PAT: Bearer token'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP bind fallback'), bMid(B2_L, B2_R, 'Basic auth (legacy)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Crowd SSO (DC option)'), bMid(B2_L, B2_R, 'OAuth app link'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA at IdP layer'), bMid(B2_L, B2_R, 'Service account'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Session: 30 min idle'), bMid(B2_L, B2_R, 'API rate limiting'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local account: break-glass'), bMid(B2_L, B2_R, 'Scope: read/write'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('LDAP/AD DCs · IdP (Okta/ADFS) with HA · Crowd server (if used) · Confluence app VMs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SAML 2.0     = federated SSO standard; Confluence validates IdP-signed XML assertion'))
    lines.append(txt_row('LDAP bind    = Confluence authenticates user by binding to LDAP with their credentials'))
    lines.append(txt_row('Crowd        = Atlassian identity server; issues Crowd SSO token shared across products'))
    lines.append(txt_row('PAT          = Personal Access Token; created in Confluence profile; used as Bearer token'))
    lines.append(txt_row('Basic auth   = Base64-encoded user:pass in Authorization header; deprecated; use PAT'))
    lines.append(txt_row('OAuth app link = OAuth 1.0a/2.0 trust between Confluence and Jira for macros/API'))
    lines.append(txt_row('Break-glass  = local admin account used when IdP/LDAP is unavailable'))
    lines.append(txt_row('Session timeout = idle session expiry; set in Admin > Security Configuration'))
    lines.append(txt_row('MFA          = second factor enforced at IdP; Confluence receives only the SAML assertion'))
    lines.append(txt_row('Service account = dedicated LDAP account for automation; PAT preferred for API'))
    lines.append(txt_row('Rate limiting = Confluence REST API: no native limit; rely on reverse proxy throttling'))
    lines.append(txt_row('Assertion    = SAML XML document signed by IdP containing user identity and attributes'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Confluence Troubleshooting ────────────────────────────────────────────────

@kb_diagram('tools-confluence-trouble', 'docs/tools/confluence/troubleshooting/index.md', 'Confluence troubleshooting overview')
def tools_confluence_trouble():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Troubleshooting Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Confluence Troubleshooting Framework')))
    lines.append(R(bMid(3, 99, 'Triage by symptom: slow, down, data issue, auth failure, or search broken')))
    lines.append(R(bMid(3, 99, 'First check: GET /status, heap usage, catalina.out, and DB connectivity')))
    lines.append(R(bMid(3, 99, 'Escalate to Atlassian Support with support-zip; include thread dump + heap dump')))
    lines.append(R(bMid(3, 99, 'Known issues: check Atlassian JIRA (bugs.atlassian.com) before opening ticket')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Structured triage prevents escalating issues that can be resolved at Tier 1'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Diagnostics'), bMid(B2_L, B2_R, 'Common Issues'), bMid(B3_L, B3_R, 'Escalation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'GET /status check'), bMid(B2_L, B2_R, 'OOM / heap full'), bMid(B3_L, B3_R, 'Atlassian Support'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Thread dump'), bMid(B2_L, B2_R, 'Slow page loads'), bMid(B3_L, B3_R, 'support-zip bundle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Heap dump (OOM)'), bMid(B2_L, B2_R, 'Search broken'), bMid(B3_L, B3_R, 'Thread dump req'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB query analysis'), bMid(B2_L, B2_R, 'Auth failures'), bMid(B3_L, B3_R, 'bugs.atlassian.com'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Log analysis'), bMid(B2_L, B2_R, 'NFS mount lost'), bMid(B3_L, B3_R, 'Hotfix / patch'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Confluence VMs · PostgreSQL · NFS · monitoring system (Prometheus/Zabbix) · log aggregator'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GET /status    = HTTP health endpoint; returns JSON with RUNNING or error state'))
    lines.append(txt_row('Thread dump    = JVM stack snapshot; generated with kill -3 <pid> or via Admin > Logging'))
    lines.append(txt_row('Heap dump      = JVM memory snapshot; triggered by OOM or via jmap; analysed with MAT'))
    lines.append(txt_row('support-zip    = Admin > Troubleshooting > Create Support Zip; includes logs and config'))
    lines.append(txt_row('OOM            = OutOfMemoryError; heap exhausted; Confluence crash; increase -Xmx'))
    lines.append(txt_row('Reindex        = rebuild Lucene index from DB; fixes stale or missing search results'))
    lines.append(txt_row('catalina.out   = Tomcat stdout log; CONFLUENCE_INSTALL/logs/catalina.out'))
    lines.append(txt_row('NFS mount lost = CONFLUENCE_HOME unmounted; attachments return 404; remount NFS'))
    lines.append(txt_row('MAT            = Eclipse Memory Analyser Tool; analyses heap dumps for leak suspects'))
    lines.append(txt_row('DB query       = slow queries visible in pg_stat_activity; check with pg_stat_statements'))
    lines.append(txt_row('bugs.atlassian.com = Atlassian public issue tracker; check for known bugs first'))
    lines.append(txt_row('Hotfix         = Atlassian-provided patch JAR for critical CVEs between releases'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-trouble-diag', 'docs/tools/confluence/troubleshooting/diagnostics/index.md', 'Confluence diagnostics')
def tools_confluence_trouble_diag():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Confluence Diagnostic Runbook')))
    lines.append(R(bMid(L, RR, 'Step 1: curl -s http://localhost:8090/status — confirms app is RUNNING')))
    lines.append(R(bMid(L, RR, 'Step 2: grep -i "ERROR|OOM|Exception" catalina.out | tail -100')))
    lines.append(R(bMid(L, RR, 'Step 3: psql -U confluence -c "SELECT count(*) FROM content;" — DB alive')))
    lines.append(R(bMid(L, RR, 'Step 4: df -h $CONFLUENCE_HOME — check disk; ls $CONFLUENCE_HOME/attachments')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Run diagnostic steps in order; stop at first anomaly and remediate before continuing'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Application Diagnostics'), bMid(B2_L, B2_R, 'Infrastructure Diag'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'curl /status endpoint'), bMid(B2_L, B2_R, 'df -h home dir'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'grep catalina.out'), bMid(B2_L, B2_R, 'mount | grep nfs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Thread dump: kill -3'), bMid(B2_L, B2_R, 'pg_stat_activity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Heap: jmap -histo'), bMid(B2_L, B2_R, 'netstat / ss ports'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Admin > System Info'), bMid(B2_L, B2_R, 'top / free -h'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'support-zip export'), bMid(B2_L, B2_R, 'journalctl -u confluence'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SSH access to Confluence VMs · PostgreSQL admin access · NFS mount visibility'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('kill -3 PID    = sends SIGQUIT to JVM; prints thread dump to catalina.out'))
    lines.append(txt_row('jmap -histo    = prints histogram of JVM heap object counts by class'))
    lines.append(txt_row('pg_stat_activity = PostgreSQL view of active queries; find long-running DB queries'))
    lines.append(txt_row('catalina.out   = Tomcat stdout; primary log for startup errors and exceptions'))
    lines.append(txt_row('atlassian-confluence.log = application log; verbose errors and warning messages'))
    lines.append(txt_row('support-zip    = Admin > Troubleshooting > Create Support Zip; bundles all logs'))
    lines.append(txt_row('top            = real-time process view; check CPU and memory for java process'))
    lines.append(txt_row('netstat / ss   = list open ports; confirm 8090 and 8091 are listening'))
    lines.append(txt_row('mount          = list mounted filesystems; confirm NFS home is mounted correctly'))
    lines.append(txt_row('journalctl     = systemd log reader; useful if Confluence runs as a systemd service'))
    lines.append(txt_row('free -h        = show available system memory; check if OS swapping under pressure'))
    lines.append(txt_row('df -h          = disk usage; alert if CONFLUENCE_HOME volume >80% full'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-trouble-esc', 'docs/tools/confluence/troubleshooting/escalation/index.md', 'Confluence escalation')
def tools_confluence_trouble_esc():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Escalation Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Confluence Escalation Tiers')))
    lines.append(R(bMid(3, 99, 'Tier 1: Ops team — restart, reindex, check logs, restore from backup')))
    lines.append(R(bMid(3, 99, 'Tier 2: Senior engineer — JVM tuning, DB query analysis, plugin conflicts')))
    lines.append(R(bMid(3, 99, 'Tier 3: Atlassian Support — open ticket with support-zip; attach thread/heap dump')))
    lines.append(R(bMid(3, 99, 'Tier 4: Atlassian escalation — P1 production down; 24x7 critical support SLA')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Escalation criteria: T1 > 30 min no resolution; T2 > 2 hr; T3 > 4 hr production down'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Escalation Criteria'), bMid(B2_L, B2_R, 'Artifacts to Gather'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service down > 30 min'), bMid(B2_L, B2_R, 'support-zip bundle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Data loss suspected'), bMid(B2_L, B2_R, 'Thread dumps x3'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Security incident'), bMid(B2_L, B2_R, 'Heap dump (OOM)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Repeated OOM crash'), bMid(B2_L, B2_R, 'catalina.out tail'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Corruption suspected'), bMid(B2_L, B2_R, 'DB slow query log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Plugin breaks upgrade'), bMid(B2_L, B2_R, 'Version + patch info'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Confluence VMs · PostgreSQL DB · monitoring/alerting · Atlassian Support portal'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('support-zip    = Admin > Troubleshooting > Create Support Zip; logs, config, thread dumps'))
    lines.append(txt_row('Thread dump    = JVM thread snapshot; take 3 dumps 10 seconds apart for deadlock analysis'))
    lines.append(txt_row('Heap dump      = full JVM memory capture; large file; required for OOM analysis'))
    lines.append(txt_row('P1 incident    = production service down; page on-call immediately; escalate within 30 min'))
    lines.append(txt_row('Atlassian Support = support.atlassian.com; requires valid license; submit with support-zip'))
    lines.append(txt_row('Atlassian escalation = request via account team; for critical production outages'))
    lines.append(txt_row('DB slow query  = pg_stat_statements or log_min_duration_statement=1000ms in postgresql.conf'))
    lines.append(txt_row('Plugin conflict = disable plugins one-by-one in safe mode to isolate culprit'))
    lines.append(txt_row('Safe mode      = Confluence starts without any user-installed plugins for diagnostics'))
    lines.append(txt_row('Corruption     = DB or index inconsistency; run reindex; compare DB row counts'))
    lines.append(txt_row('Data loss      = page versions allow recovery; check DB for deleted content'))
    lines.append(txt_row('SLA            = Atlassian support SLA: P1 1hr response, P2 4hr, P3/P4 next business day'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-trouble-common', 'docs/tools/confluence/troubleshooting/common-issues/index.md', 'Confluence common issues')
def tools_confluence_trouble_common():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Common Issues'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Confluence Frequent Issue Patterns')))
    lines.append(R(bMid(3, 99, 'OOM crash: heap too small; increase -Xmx; check for memory-leaking plugins')))
    lines.append(R(bMid(3, 99, 'Slow pages: DB slow queries or GC pressure; check pg_stat_activity and GC log')))
    lines.append(R(bMid(3, 99, 'Search broken: Lucene index stale; trigger full reindex from Admin > Content Indexing')))
    lines.append(R(bMid(3, 99, 'Auth fails: LDAP sync failure or SAML cert expired; check directory config')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Most Confluence issues fall into four categories: memory, performance, search, auth'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Issue'), bMid(B2_L, B2_R, 'Resolution'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OOM / crash'), bMid(B2_L, B2_R, 'Increase -Xmx; check plugins'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Slow page loads'), bMid(B2_L, B2_R, 'DB index; tune GC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Search missing pages'), bMid(B2_L, B2_R, 'Full reindex from admin'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML login fails'), bMid(B2_L, B2_R, 'Check IdP cert expiry'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Attachments 404'), bMid(B2_L, B2_R, 'Remount NFS home dir'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB connection errors'), bMid(B2_L, B2_R, 'Increase pool size'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Confluence VMs · PostgreSQL · NFS home · IdP (Okta/ADFS) · load balancer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('-Xmx         = JVM max heap; set in setenv.sh; increase if OOM crashes occur frequently'))
    lines.append(txt_row('GC pressure  = garbage collection running too frequently; indicates heap too small'))
    lines.append(txt_row('Reindex      = Admin > Content Indexing > Rebuild Index; fixes stale Lucene search'))
    lines.append(txt_row('SAML cert    = IdP signing cert; expires on a schedule; update in SAML config'))
    lines.append(txt_row('NFS remount  = umount then mount; or systemctl restart nfs-client.target'))
    lines.append(txt_row('DB pool      = JDBC connection pool; increase maxPoolSize in dbconfig.xml'))
    lines.append(txt_row('GC log       = JVM GC log; enable with -Xlog:gc* in JVM args; shows pause durations'))
    lines.append(txt_row('Plugin leak  = some Confluence plugins have memory leaks; disable to test'))
    lines.append(txt_row('LDAP sync    = Admin > User Management > User Directories; trigger manual sync'))
    lines.append(txt_row('pg_stat_activity = PostgreSQL view; shows running queries; find slow or blocked queries'))
    lines.append(txt_row('Content index = Lucene index managed by Confluence; stored in CONFLUENCE_HOME/index'))
    lines.append(txt_row('Attachment 404 = attachment served from NFS; NFS unavailable = 404 for all attachments'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Confluence Operations (remaining) ─────────────────────────────────────────

@kb_diagram('tools-confluence-ops-procedures', 'docs/tools/confluence/operations/procedures/index.md', 'Confluence operations procedures')
def tools_confluence_ops_procedures():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Operations Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Confluence Standard Operating Procedures')))
    lines.append(R(bMid(3, 99, 'Planned restart: drain LB → stop Confluence → maintenance → start → add to LB')))
    lines.append(R(bMid(3, 99, 'Space archival: export as XML → disable space → move to archive space')))
    lines.append(R(bMid(3, 99, 'User offboard: deactivate LDAP account → remove group memberships → audit log')))
    lines.append(R(bMid(3, 99, 'Plugin update: test in staging → UPM update in prod → verify functionality')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  SOPs reduce error rates and ensure consistent execution of routine operations'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Maintenance SOPs'), bMid(B2_L, B2_R, 'Content SOPs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Planned restart SOP'), bMid(B2_L, B2_R, 'Space archival SOP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Plugin update SOP'), bMid(B2_L, B2_R, 'User offboard SOP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB maintenance SOP'), bMid(B2_L, B2_R, 'Content migration SOP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Upgrade SOP'), bMid(B2_L, B2_R, 'Audit log review SOP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup verify SOP'), bMid(B2_L, B2_R, 'Permission review SOP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Reindex SOP'), bMid(B2_L, B2_R, 'GDPR deletion SOP'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Confluence VMs · LB for draining · PostgreSQL · NFS · UPM for plugins'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LB drain       = remove node from load balancer pool before maintenance; in-flight reqs complete'))
    lines.append(txt_row('UPM            = Universal Plugin Manager; Admin > Manage Apps for add-on updates'))
    lines.append(txt_row('Space archival = export space as XML; disable space; accessible via search but read-only'))
    lines.append(txt_row('User offboard  = deactivate in LDAP; Confluence sync picks up deactivation within poll interval'))
    lines.append(txt_row('DB maintenance = VACUUM ANALYZE in PostgreSQL; run during low-traffic windows'))
    lines.append(txt_row('GDPR deletion  = remove personal data; Confluence has no native right-to-erasure tool'))
    lines.append(txt_row('Content migrate = use Confluence space import/export to move content between instances'))
    lines.append(txt_row('Permission review = quarterly review of space admin list and global permission groups'))
    lines.append(txt_row('Audit log review = Admin > Audit Log; monthly review of privilege escalation events'))
    lines.append(txt_row('Upgrade SOP    = snapshot VMs → backup DB → run installer → verify → cutover'))
    lines.append(txt_row('Reindex SOP    = Admin > Content Indexing > Rebuild; during off-peak; takes 30+ min for large'))
    lines.append(txt_row('VACUUM ANALYZE = PostgreSQL command; reclaims storage and updates query planner statistics'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-ops-install', 'docs/tools/confluence/operations/install-upgrade/index.md', 'Confluence install and upgrade')
def tools_confluence_ops_install():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Confluence — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Confluence Installation and Upgrade Procedure')))
    lines.append(R(bMid(3, 99, 'Install: JDK 11/17 → download installer → set CONFLUENCE_HOME → run setup wizard')))
    lines.append(R(bMid(3, 99, 'DB: create PostgreSQL DB and role → set in setup wizard → apply license key')))
    lines.append(R(bMid(3, 99, 'Upgrade: backup DB + home → stop → run new installer → start → verify → test')))
    lines.append(R(bMid(3, 99, 'DC node add: install on new VM → point to same DB + NFS → join cluster auto')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Always test upgrade in staging environment before production; keep snapshot for rollback'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fresh Install Steps'), bMid(B2_L, B2_R, 'Upgrade Steps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Install JDK 11/17'), bMid(B2_L, B2_R, 'Snapshot VM + DB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Download installer'), bMid(B2_L, B2_R, 'pg_dump backup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Set CONFLUENCE_HOME'), bMid(B2_L, B2_R, 'Stop all nodes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create PostgreSQL DB'), bMid(B2_L, B2_R, 'Run new installer'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Run setup wizard'), bMid(B2_L, B2_R, 'Start and verify'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Apply license key'), bMid(B2_L, B2_R, 'Test key functions'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Fresh VM (RHEL/CentOS) · PostgreSQL VM · NFS datastore · load balancer for DC'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CONFLUENCE_HOME = data directory; set as env var or in confluence-init.properties'))
    lines.append(txt_row('JDK 11/17    = Confluence 8.x supports JDK 11 and 17; JDK 21 for Confluence 9.x'))
    lines.append(txt_row('Setup wizard = browser-based initial config: DB, license, admin account, space'))
    lines.append(txt_row('License key  = Atlassian data center or server license; apply in setup or Admin panel'))
    lines.append(txt_row('pg_dump      = PostgreSQL backup utility; always backup before any upgrade'))
    lines.append(txt_row('Installer    = Atlassian-provided .bin file for Linux; chmod +x and run as root'))
    lines.append(txt_row('DC cluster   = second node auto-joins when pointed at same DB and NFS home'))
    lines.append(txt_row('Snapshot     = VM snapshot before upgrade; revert if upgrade fails'))
    lines.append(txt_row('Version check = Confluence upgrade path; some versions require intermediate upgrade steps'))
    lines.append(txt_row('setenv.sh    = JVM argument config; in CONFLUENCE_INSTALL/bin/; set -Xmx here'))
    lines.append(txt_row('Plugin compat = check app compatibility on upgrade; UPM shows incompatible plugins'))
    lines.append(txt_row('Rollback     = revert VM snapshot or restore DB dump; re-run previous installer'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-confluence-ops-scripts', 'docs/tools/confluence/operations/scripts/index.md', 'Confluence operations scripts')
def tools_confluence_ops_scripts():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Confluence — Operations Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Confluence Operational Script Reference')))
    lines.append(R(bMid(L, RR, 'backup.sh: pg_dump → tar CONFLUENCE_HOME/attachments → gpg encrypt → push to S3')))
    lines.append(R(bMid(L, RR, 'reindex.sh: curl REST API to trigger reindex; poll until complete')))
    lines.append(R(bMid(L, RR, 'health-check.sh: curl /status; check disk, heap via JMX, DB conn test')))
    lines.append(R(bMid(L, RR, 'space-export.sh: REST API POST to /export-space; download exported ZIP')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Confluence app VMs · PostgreSQL DB · NFS home · S3 or NFS backup target'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('backup.sh      = shell script: pg_dump + tar home + gpg + s3 copy; run via cron'))
    lines.append(txt_row('reindex.sh     = REST call to trigger reindex: POST /rest/api/index/reindexAll'))
    lines.append(txt_row('health-check.sh = curl /status + df + JMX heap query + psql connection check'))
    lines.append(txt_row('space-export.sh = Confluence REST space export; useful for archival or migration'))
    lines.append(txt_row('pg_dump        = PostgreSQL utility; creates database backup file'))
    lines.append(txt_row('gpg encrypt    = GPG symmetric or asymmetric encryption of backup archives'))
    lines.append(txt_row('s3 copy        = aws s3 cp to push backup to S3 bucket with lifecycle policy'))
    lines.append(txt_row('JMX            = Java Management Extensions; expose heap/thread metrics for scripts'))
    lines.append(txt_row('cron           = schedule backup.sh and health-check.sh at required intervals'))
    lines.append(txt_row('REST auth      = scripts use PAT in Authorization: Bearer header for API calls'))
    lines.append(txt_row('Space export   = produces a ZIP archive; importable to another Confluence instance'))
    lines.append(txt_row('Poll loop      = reindex.sh polls /rest/api/index/reindexAll until status=DONE'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Jira ─────────────────────────────────────────────────────────────────────

@kb_diagram('tools-jira', 'docs/tools/jira/index.md', 'Jira platform overview')
def tools_jira():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Platform Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Atlassian Jira — Issue and Project Tracking')))
    lines.append(R(bMid(3, 99, 'Projects: Software (Scrum/Kanban), Business, Service Management project types')))
    lines.append(R(bMid(3, 99, 'App tier: Tomcat on port 8080; behind reverse proxy on 443; JVM heap 4-8 GB')))
    lines.append(R(bMid(3, 99, 'Data tier: PostgreSQL or Oracle DB; Lucene search index on shared NFS home')))
    lines.append(R(bMid(3, 99, 'Integrations: Confluence app link, Bitbucket, CI/CD webhooks, REST API v3')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Jira is the central issue registry linking development, operations, and support'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Architecture'), bMid(B2_L, B2_R, 'Operations'), bMid(B3_L, B3_R, 'Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tomcat app tier'), bMid(B2_L, B2_R, 'Install/Upgrade'), bMid(B3_L, B3_R, 'LDAP/SAML auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PostgreSQL DB'), bMid(B2_L, B2_R, 'Backup/Restore'), bMid(B3_L, B3_R, 'Permission schemes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Lucene search'), bMid(B2_L, B2_R, 'Health checks'), bMid(B3_L, B3_R, 'TLS encryption'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'REST API v3'), bMid(B2_L, B2_R, 'Scripts'), bMid(B3_L, B3_R, 'Hardening guide'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Integrations'), bMid(B2_L, B2_R, 'CLI reference'), bMid(B3_L, B3_R, 'Access control'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere VMs for app nodes · PostgreSQL DB VM · NFS shared home · load balancer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Project      = Jira container for issues; has type (Software/Business/SM), key, and scheme'))
    lines.append(txt_row('Issue        = unit of work: Bug, Story, Task, Epic, Sub-task; tracked across workflow'))
    lines.append(txt_row('JQL          = Jira Query Language; SQL-like filter syntax (project = TEAM AND status = Open)'))
    lines.append(txt_row('Workflow     = state machine for issues; Statuses and Transitions defined per project'))
    lines.append(txt_row('Screen       = field layout shown on create/edit/view; configured per issue type'))
    lines.append(txt_row('Permission scheme = project-level ACL; maps project roles to operations (create, edit, etc.)'))
    lines.append(txt_row('Notification scheme = email rules for issue events; per project configuration'))
    lines.append(txt_row('Component    = sub-category within a project; assigned to issues for grouping'))
    lines.append(txt_row('Sprint       = Scrum time-box; issues committed to a 1-4 week iteration'))
    lines.append(txt_row('Kanban board = continuous flow board; WIP limits; no fixed sprint iterations'))
    lines.append(txt_row('Epic         = large user story grouping multiple stories; tracked across sprints'))
    lines.append(txt_row('Velocity     = average story points completed per sprint; sprint planning metric'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-arch', 'docs/tools/jira/architecture/index.md', 'Jira architecture overview')
def tools_jira_arch():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Architecture Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Data Center Architecture')))
    lines.append(R(bMid(3, 99, 'Load balancer → multiple Tomcat app nodes → shared PostgreSQL DB + NFS home')))
    lines.append(R(bMid(3, 99, 'Shared home: stores Lucene index, attachments, plugins, and avatars on NFS')))
    lines.append(R(bMid(3, 99, 'Ehcache clustering: Jira DC uses distributed Ehcache for cache across nodes')))
    lines.append(R(bMid(3, 99, 'Job scheduling: Jira DC uses cluster-aware scheduler to prevent duplicate jobs')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Jira architecture mirrors Confluence DC: stateless app nodes sharing DB and NFS'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Application Tier'), bMid(B2_L, B2_R, 'Data Tier'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tomcat: 8 vCPU/16 GB'), bMid(B2_L, B2_R, 'PostgreSQL primary'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'JVM heap: 4-8 GB'), bMid(B2_L, B2_R, 'Streaming replica'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Ehcache: distributed'), bMid(B2_L, B2_R, 'NFS shared home'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'REST API: port 8080'), bMid(B2_L, B2_R, 'Lucene index on NFS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Scheduler: DC-aware'), bMid(B2_L, B2_R, 'JDBC: jira DB user'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LB: sticky sessions'), bMid(B2_L, B2_R, 'pg_dump nightly'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('2+ app VMs · DB VM with SSD · NFS datastore · L4/L7 load balancer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Ehcache      = distributed Java cache library; Jira DC uses it for issue and user caching'))
    lines.append(txt_row('Shared home  = JIRA_HOME on NFS; same path on all nodes; holds index and attachments'))
    lines.append(txt_row('Tomcat       = Java servlet container; Jira runs as a WAR on Tomcat listening port 8080'))
    lines.append(txt_row('DC scheduler = Jira cluster-aware job scheduler; only one node runs each scheduled task'))
    lines.append(txt_row('JDBC pool    = connection pool; Jira uses HikariCP; tune maxPoolSize for concurrent users'))
    lines.append(txt_row('Lucene       = embedded search; index on NFS; rebuilt after restore or corruption'))
    lines.append(txt_row('Sticky session = LB routes user to same node; avoids Ehcache cache miss cost'))
    lines.append(txt_row('Streaming replica = PostgreSQL WAL replica; provides read scale and failover target'))
    lines.append(txt_row('pg_dump      = PostgreSQL backup; schedule nightly with custom format for fast restore'))
    lines.append(txt_row('NFS mount    = JIRA_HOME on NFS; must be available before Jira starts'))
    lines.append(txt_row('LB           = load balancer; HAProxy, nginx, or F5; handles TLS termination'))
    lines.append(txt_row('JVM heap     = -Xmx in setenv.sh; 4 GB minimum, 8 GB for large instances'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-arch-how', 'docs/tools/jira/architecture/how-it-works/index.md', 'Jira how it works')
def tools_jira_arch_how():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Request and Data Flow')))
    lines.append(R(bMid(3, 99, 'Browser → LB → Tomcat (Jira app) → DB read/write; attachments via NFS')))
    lines.append(R(bMid(3, 99, 'Issue create: HTTP POST → workflow engine → DB insert → Lucene index update')))
    lines.append(R(bMid(3, 99, 'JQL search: parse query → Lucene search → fetch issue data from DB → render')))
    lines.append(R(bMid(3, 99, 'Notifications: issue event → notification scheme → email via SMTP relay')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Jira processes issue events synchronously; indexing and notifications are async'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HTTP Flow'), bMid(B2_L, B2_R, 'Workflow Engine'), bMid(B3_L, B3_R, 'Search Flow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Browser → LB'), bMid(B2_L, B2_R, 'Transition trigger'), bMid(B3_L, B3_R, 'JQL parse'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LB → Tomcat'), bMid(B2_L, B2_R, 'Condition check'), bMid(B3_L, B3_R, 'Lucene query'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Auth check'), bMid(B2_L, B2_R, 'Validator run'), bMid(B3_L, B3_R, 'Fetch from DB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB query/write'), bMid(B2_L, B2_R, 'Post function'), bMid(B3_L, B3_R, 'Permission filter'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Lucene index'), bMid(B2_L, B2_R, 'Status update'), bMid(B3_L, B3_R, 'Response render'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Notify via SMTP'), bMid(B2_L, B2_R, 'Assign / comment'), bMid(B3_L, B3_R, 'Pagination'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Tomcat JVM VMs · PostgreSQL VM · NFS home · SMTP relay for notifications'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Workflow engine = Jira state machine; processes transitions, conditions, validators, post functions'))
    lines.append(txt_row('Transition      = workflow step moving issue from one status to another'))
    lines.append(txt_row('Condition       = rule checked before transition is allowed (e.g. user must be assignee)'))
    lines.append(txt_row('Validator       = checks field values before transition executes'))
    lines.append(txt_row('Post function   = action executed after transition (e.g. assign to role, fire webhook)'))
    lines.append(txt_row('JQL             = Jira Query Language; parsed to Lucene query for issue search'))
    lines.append(txt_row('Lucene index    = inverted index of issue fields; stored on NFS shared home'))
    lines.append(txt_row('Permission filter = search results filtered by current user project/issue permissions'))
    lines.append(txt_row('Notification scheme = defines which events trigger email and to which recipients'))
    lines.append(txt_row('SMTP relay      = outgoing mail server; Jira sends notifications via configured relay'))
    lines.append(txt_row('Ehcache         = distributed cache; stores resolved permissions and issue data'))
    lines.append(txt_row('Attachment      = file stored on NFS under JIRA_HOME/data/attachments'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-arch-int', 'docs/tools/jira/architecture/integrations/index.md', 'Jira integrations')
def tools_jira_arch_int():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Integration Landscape')))
    lines.append(R(bMid(3, 99, 'Atlassian: Confluence app link, Bitbucket branch/PR linking, Bamboo builds')))
    lines.append(R(bMid(3, 99, 'Auth: LDAP user/group sync + SAML SSO via Okta/ADFS + Crowd optional')))
    lines.append(R(bMid(3, 99, 'REST API v3: issues, projects, boards, sprints, comments, attachments')))
    lines.append(R(bMid(3, 99, 'Webhooks: HTTP POST on issue created/updated/deleted to CI/CD and ITSM')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Jira acts as the integration hub connecting dev tools, auth, and ticketing systems'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Directory & Auth'), bMid(B2_L, B2_R, 'Dev Toolchain'), bMid(B3_L, B3_R, 'External Systems'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP/AD sync'), bMid(B2_L, B2_R, 'Confluence app link'), bMid(B3_L, B3_R, 'REST API'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML SSO: Okta/ADFS'), bMid(B2_L, B2_R, 'Bitbucket branches'), bMid(B3_L, B3_R, 'Webhooks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Crowd SSO (optional)'), bMid(B2_L, B2_R, 'Bamboo CI results'), bMid(B3_L, B3_R, 'ServiceNow link'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA at IdP layer'), bMid(B2_L, B2_R, 'Jenkins webhooks'), bMid(B3_L, B3_R, 'Slack notifs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local fallback accts'), bMid(B2_L, B2_R, 'GitHub PR links'), bMid(B3_L, B3_R, 'Email SMTP'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('LDAP/AD DCs · IdP (Okta/ADFS) · Bitbucket/GitHub servers · SMTP relay'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('App link     = Atlassian trusted relationship; enables cross-product OAuth and macros'))
    lines.append(txt_row('Bitbucket link = Jira shows branch and PR status from linked Bitbucket/GitHub repos'))
    lines.append(txt_row('Bamboo link  = Jira shows CI build results on issues linked to Bamboo build plans'))
    lines.append(txt_row('LDAP sync    = Jira polls LDAP/AD on schedule; imports users and group memberships'))
    lines.append(txt_row('Webhook      = Jira POST to external URL on issue event; configure in Admin > Webhooks'))
    lines.append(txt_row('REST API v3  = Jira REST API; /rest/api/3/ prefix; JSON; PAT or OAuth2 auth'))
    lines.append(txt_row('ServiceNow   = Jira-to-SNOW integration via webhook or REST for incident/change sync'))
    lines.append(txt_row('Slack        = Jira for Slack app; posts issue updates to channels via webhook'))
    lines.append(txt_row('SMTP         = outbound email for notifications; configure in Admin > Outgoing Mail'))
    lines.append(txt_row('OAuth        = app link OAuth 1.0a/2.0 for trusted cross-product API requests'))
    lines.append(txt_row('PAT          = Personal Access Token; preferred for REST API scripting'))
    lines.append(txt_row('Crowd        = optional Atlassian SSO server; centralized auth if not using SAML'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-arch-design', 'docs/tools/jira/architecture/design-standards/index.md', 'Jira design standards')
def tools_jira_arch_design():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Design and Sizing Standards')))
    lines.append(R(bMid(3, 99, 'App node: min 8 vCPU / 16 GB RAM; JVM heap 4-8 GB set in setenv.sh')))
    lines.append(R(bMid(3, 99, 'DB: 4 vCPU / 8 GB RAM; SSD storage; tune autovacuum and work_mem')))
    lines.append(R(bMid(3, 99, 'NFS: shared home for index/attachments; 10 GbE, low latency (<1 ms)')))
    lines.append(R(bMid(3, 99, 'Project naming: PROJ-KEY in CAPS (max 10 chars); descriptive display name')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Standards enforce consistent sizing, naming, and topology across environments'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Infrastructure Standards'), bMid(B2_L, B2_R, 'Configuration Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App: 8 vCPU/16 GB'), bMid(B2_L, B2_R, 'JVM: -Xms2g -Xmx8g'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB: 4 vCPU/8 GB SSD'), bMid(B2_L, B2_R, 'DB pool: max 60'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NFS: 10 Gbps low latency'), bMid(B2_L, B2_R, 'Tomcat: 150 threads'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LB: sticky sessions'), bMid(B2_L, B2_R, 'Scheduler: cluster-aware'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Replica: streaming repl'), bMid(B2_L, B2_R, 'Backup: nightly pg_dump'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DR: off-site NFS copy'), bMid(B2_L, B2_R, 'Retention: 30-day'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere HA cluster · SSD datastores · 10 GbE NFS segment · dedicated DB VLAN'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('-Xmx         = JVM max heap; set in JIRA_INSTALL/bin/setenv.sh'))
    lines.append(txt_row('autovacuum   = PostgreSQL background vacuum; critical for Jira schema with high write rate'))
    lines.append(txt_row('work_mem     = PostgreSQL per-sort memory; increase for complex JQL aggregation queries'))
    lines.append(txt_row('Project key  = 2-10 uppercase chars; unique ID prefix for all issues (e.g. OPS-1234)'))
    lines.append(txt_row('DB pool      = HikariCP in Jira; maxPoolSize in dbconfig.xml; match DB max_connections'))
    lines.append(txt_row('NFS latency  = shared home I/O latency directly affects Lucene indexing performance'))
    lines.append(txt_row('Retention    = 30-day backup minimum; adjust per compliance requirement'))
    lines.append(txt_row('Streaming repl = PostgreSQL WAL replica for HA failover and read offloading'))
    lines.append(txt_row('Sticky session = LB routes same user to same node; minimizes cache miss overhead'))
    lines.append(txt_row('DC-aware sched = only one Jira node runs each scheduled task at a time'))
    lines.append(txt_row('JIRA_HOME    = data directory; set in jira-application.properties; NFS mount path'))
    lines.append(txt_row('Tomcat threads = max concurrent HTTP handlers; set connector maxThreads in server.xml'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-ops', 'docs/tools/jira/operations/index.md', 'Jira operations overview')
def tools_jira_ops():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Operations Overview'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Daily Checks'), bMid(B2_L, B2_R, 'Weekly Tasks'), bMid(B3_L, B3_R, 'Monthly Tasks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service status'), bMid(B2_L, B2_R, 'Backup verify'), bMid(B3_L, B3_R, 'License audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Heap usage'), bMid(B2_L, B2_R, 'User audit'), bMid(B3_L, B3_R, 'Plugin updates'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Disk usage'), bMid(B2_L, B2_R, 'Index health'), bMid(B3_L, B3_R, 'Performance review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert triage'), bMid(B2_L, B2_R, 'Check logs'), bMid(B3_L, B3_R, 'Security review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Jira app VMs · PostgreSQL DB VM · NFS shared home · monitoring system'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Service status = Jira running state; check via curl http://localhost:8080/status'))
    lines.append(txt_row('Heap usage     = JVM memory; check Admin > System Info or JMX; alert >80%'))
    lines.append(txt_row('Disk usage     = monitor JIRA_HOME volume; alert at 80%; attachments grow fast'))
    lines.append(txt_row('Index health   = Lucene index consistency; reindex if search returns stale results'))
    lines.append(txt_row('License audit  = active user count vs licensed seats; Admin > License Details'))
    lines.append(txt_row('Plugin updates = Admin > Manage Apps; update via UPM; test in staging first'))
    lines.append(txt_row('User audit     = review inactive users and orphan group memberships weekly'))
    lines.append(txt_row('Backup verify  = confirm pg_dump completed; check JIRA_HOME/export for recent files'))
    lines.append(txt_row('Performance review = monthly GC log analysis and slow query identification'))
    lines.append(txt_row('Security review = permission scheme audit and admin account review monthly'))
    lines.append(txt_row('UPM            = Universal Plugin Manager; built-in app management in Jira admin'))
    lines.append(txt_row('Alert triage   = review monitoring alerts for Jira service, DB, and NFS health'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-ops-procedures', 'docs/tools/jira/operations/procedures/index.md', 'Jira operations procedures')
def tools_jira_ops_procedures():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Operations Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Standard Operating Procedures')))
    lines.append(R(bMid(3, 99, 'Planned restart: drain LB → stop Jira → maintenance → start → add to LB')))
    lines.append(R(bMid(3, 99, 'Project archival: close all issues → archive project → restrict permissions')))
    lines.append(R(bMid(3, 99, 'User offboard: deactivate LDAP account → remove from project roles → audit')))
    lines.append(R(bMid(3, 99, 'Reindex: Admin > System > Indexing; full reindex during off-peak window')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  SOPs standardise Jira operations and reduce human error in routine tasks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Maintenance SOPs'), bMid(B2_L, B2_R, 'Project/User SOPs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Planned restart SOP'), bMid(B2_L, B2_R, 'Project archival SOP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Plugin update SOP'), bMid(B2_L, B2_R, 'User offboard SOP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB maintenance SOP'), bMid(B2_L, B2_R, 'Permission review SOP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Upgrade SOP'), bMid(B2_L, B2_R, 'Audit log review SOP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup verify SOP'), bMid(B2_L, B2_R, 'GDPR deletion SOP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Reindex SOP'), bMid(B2_L, B2_R, 'Field config review SOP'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Jira app VMs · LB for draining · PostgreSQL DB · NFS · UPM for plugin management'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LB drain       = remove node from LB before work; prevents requests during maintenance'))
    lines.append(txt_row('Project archival = mark project archived; issues read-only; frees active board space'))
    lines.append(txt_row('Reindex SOP    = Admin > System > Indexing > Full Re-Index; takes 30+ min for large DB'))
    lines.append(txt_row('User offboard  = deactivate in LDAP; Jira sync deactivates account on next poll'))
    lines.append(txt_row('Permission review = quarterly audit of project permission schemes and role members'))
    lines.append(txt_row('GDPR deletion  = anonymize user data via Admin > User Management > Anonymize User'))
    lines.append(txt_row('Audit log      = Admin > Audit Log; tracks config and permission changes'))
    lines.append(txt_row('Field config   = Jira field configuration schemes; review for unused custom fields'))
    lines.append(txt_row('DB maintenance = VACUUM ANALYZE public; run in PostgreSQL during low-traffic window'))
    lines.append(txt_row('Plugin update  = UPM > Manage Apps > Update; test in staging before production'))
    lines.append(txt_row('Upgrade SOP    = snapshot VM → backup DB → run installer → verify → restore if fail'))
    lines.append(txt_row('Backup verify  = check pg_dump file exists and is non-zero size after cron run'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-ops-backup', 'docs/tools/jira/operations/backup-restore/index.md', 'Jira backup and restore')
def tools_jira_ops_backup():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Backup and Restore'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Backup and Restore Strategy')))
    lines.append(R(bMid(3, 99, 'Backup: pg_dump nightly + tar JIRA_HOME/data/attachments + push off-site')))
    lines.append(R(bMid(3, 99, 'Restore: stop Jira → restore DB → restore home → start Jira → reindex')))
    lines.append(R(bMid(3, 99, 'XML backup: Admin > Backup System; not for production restores; content only')))
    lines.append(R(bMid(3, 99, 'RTO target: 4 hours; RPO target: 24 hours (nightly backup interval)')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Always restore DB before home directory; reindex after any restore'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup Strategy'), bMid(B2_L, B2_R, 'Restore Procedure'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB: pg_dump nightly'), bMid(B2_L, B2_R, 'Stop Jira service'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Home: tar nightly'), bMid(B2_L, B2_R, 'Drop + recreate DB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Off-site: S3 copy'), bMid(B2_L, B2_R, 'pg_restore dump'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify backup daily'), bMid(B2_L, B2_R, 'Restore home dir'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'XML: weekly (small)'), bMid(B2_L, B2_R, 'Start Jira'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test restore: quarterly'), bMid(B2_L, B2_R, 'Trigger full reindex'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Jira app VMs · PostgreSQL DB with SSD · NFS/SAN for JIRA_HOME · S3 off-site storage'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('pg_dump      = PostgreSQL backup; use --format=custom for parallel pg_restore'))
    lines.append(txt_row('pg_restore   = restore custom-format pg_dump; use -j for parallel job count'))
    lines.append(txt_row('JIRA_HOME    = Jira data directory; contains attachments, indexes, plugins, and config'))
    lines.append(txt_row('XML backup   = Jira built-in export; useful for small instances or content migration only'))
    lines.append(txt_row('Off-site     = backup copy to secondary site or S3; required for DR compliance'))
    lines.append(txt_row('Reindex      = always reindex after restore; DB and index must be in sync'))
    lines.append(txt_row('RTO          = Recovery Time Objective; target restore completion time'))
    lines.append(txt_row('RPO          = Recovery Point Objective; maximum acceptable data loss'))
    lines.append(txt_row('Quarterly test = restore to isolated test environment; verify data integrity'))
    lines.append(txt_row('Tar archive  = tar -czf jira_home_$(date +%Y%m%d).tar.gz JIRA_HOME/'))
    lines.append(txt_row('Drop+recreate = DROP DATABASE jira; CREATE DATABASE jira; before pg_restore'))
    lines.append(txt_row('Verify       = compare row counts: SELECT count(*) FROM jiraissue;'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-ops-health', 'docs/tools/jira/operations/health-checks/index.md', 'Jira health checks')
def tools_jira_ops_health():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Health Checks'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Application Health'), bMid(B2_L, B2_R, 'Infrastructure Health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'GET /status → RUNNING'), bMid(B2_L, B2_R, 'DB connectivity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Heap usage < 80%'), bMid(B2_L, B2_R, 'Disk < 80%'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No OOM in logs'), bMid(B2_L, B2_R, 'NFS mount active'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Lucene index OK'), bMid(B2_L, B2_R, 'Backup completed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Background jobs OK'), bMid(B2_L, B2_R, 'SMTP reachable'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Jira app VMs · PostgreSQL DB · NFS shared home · SMTP relay'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GET /status    = curl http://localhost:8080/status; returns RUNNING or error'))
    lines.append(txt_row('Heap check     = Admin > System Info > JVM Memory Usage; alert if >80%'))
    lines.append(txt_row('Lucene index   = Admin > System > Indexing; shows index size and last update time'))
    lines.append(txt_row('Background jobs = Admin > Scheduled Jobs; verify last-run time and error count'))
    lines.append(txt_row('DB check       = psql -U jira -c "SELECT 1;" to confirm connectivity'))
    lines.append(txt_row('Disk check     = df -h JIRA_HOME; alert at 80%; attachments fill disk gradually'))
    lines.append(txt_row('NFS check      = mount | grep nfs; ls JIRA_HOME/data/attachments'))
    lines.append(txt_row('SMTP check     = Admin > Outgoing Mail > Send Test Email'))
    lines.append(txt_row('Backup check   = verify pg_dump file timestamp and non-zero size'))
    lines.append(txt_row('OOM check      = grep OutOfMemoryError catalina.out; OOM indicates heap too small'))
    lines.append(txt_row('Scheduled jobs = Jira runs DB clean-up, indexing, and mail jobs on schedule'))
    lines.append(txt_row('JMX            = expose JVM metrics; scrape with Prometheus JMX exporter'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-ops-install', 'docs/tools/jira/operations/install-upgrade/index.md', 'Jira install and upgrade')
def tools_jira_ops_install():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Installation and Upgrade Procedure')))
    lines.append(R(bMid(3, 99, 'Install: JDK 11/17 → download installer → set JIRA_HOME → run setup wizard')))
    lines.append(R(bMid(3, 99, 'DB: PostgreSQL 14+ → create DB/role → configure via setup wizard')))
    lines.append(R(bMid(3, 99, 'Upgrade: snapshot → pg_dump → stop → new installer → start → verify')))
    lines.append(R(bMid(3, 99, 'DC node add: install on new VM → same DB + NFS JIRA_HOME → cluster joins')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Snapshot VMs and backup DB before every upgrade; prepare rollback plan'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fresh Install Steps'), bMid(B2_L, B2_R, 'Upgrade Steps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Install JDK 11/17'), bMid(B2_L, B2_R, 'Snapshot VM + DB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Download Jira .bin'), bMid(B2_L, B2_R, 'pg_dump backup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Set JIRA_HOME env'), bMid(B2_L, B2_R, 'Stop all nodes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create PostgreSQL DB'), bMid(B2_L, B2_R, 'Run new installer'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Run setup wizard'), bMid(B2_L, B2_R, 'Start and verify'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Apply license key'), bMid(B2_L, B2_R, 'Test key workflows'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Fresh VM (RHEL/CentOS) · PostgreSQL VM · NFS for shared home · load balancer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('JIRA_HOME    = data directory; set in jira-application.properties; NFS mount for DC'))
    lines.append(txt_row('JDK 11/17    = Jira 9.x supports JDK 11 and 17; check Jira version compatibility matrix'))
    lines.append(txt_row('Setup wizard = browser-based config: DB, license, admin account, project template'))
    lines.append(txt_row('License key  = Atlassian Jira DC or Server license; apply in setup or Admin panel'))
    lines.append(txt_row('Installer    = Atlassian-provided .bin for Linux; chmod +x; run as root'))
    lines.append(txt_row('Snapshot     = VM snapshot before upgrade; revert if upgrade fails'))
    lines.append(txt_row('Plugin compat = check app compatibility before upgrade; UPM shows incompatible apps'))
    lines.append(txt_row('setenv.sh    = JVM flags; JIRA_INSTALL/bin/setenv.sh; set -Xmx here'))
    lines.append(txt_row('Rollback     = revert VM snapshot; restore pg_dump; restart previous version'))
    lines.append(txt_row('Upgrade path = some Jira versions require intermediate upgrade steps; check docs'))
    lines.append(txt_row('DC cluster   = additional node joins when same DB and NFS home configured'))
    lines.append(txt_row('PostgreSQL 14 = minimum recommended for Jira 9.x; check matrix for exact version'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-ops-scripts', 'docs/tools/jira/operations/scripts/index.md', 'Jira operations scripts')
def tools_jira_ops_scripts():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Jira — Operations Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Jira Operational Script Reference')))
    lines.append(R(bMid(L, RR, 'backup.sh: pg_dump jira → tar JIRA_HOME/data/attachments → push to S3')))
    lines.append(R(bMid(L, RR, 'reindex.sh: POST /rest/api/2/reindex → poll /rest/api/2/reindex until COMPLETE')))
    lines.append(R(bMid(L, RR, 'health-check.sh: curl /status, heap via JMX, DB conn, disk check')))
    lines.append(R(bMid(L, RR, 'user-deactivate.sh: REST PUT /rest/api/2/user?username=X → active: false')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Jira app VMs · PostgreSQL DB · NFS for JIRA_HOME · S3 backup target'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('backup.sh      = nightly cron: pg_dump + tar attachments + s3 cp off-site'))
    lines.append(txt_row('reindex.sh     = triggers Jira REST reindex; polls until COMPLETE state'))
    lines.append(txt_row('health-check.sh = checks Jira status endpoint, JVM heap, DB, disk, and NFS'))
    lines.append(txt_row('user-deactivate = REST API to deactivate user; used in offboarding automation'))
    lines.append(txt_row('pg_dump        = PostgreSQL utility; custom format dump for parallel restore'))
    lines.append(txt_row('s3 cp          = AWS CLI upload to S3; add --sse for server-side encryption'))
    lines.append(txt_row('JMX            = Java Management Extensions; Jira exposes heap via JMX beans'))
    lines.append(txt_row('REST auth      = scripts use PAT in Authorization: Bearer header'))
    lines.append(txt_row('cron           = schedule backup.sh and health-check.sh via crontab'))
    lines.append(txt_row('/rest/api/2    = Jira REST API v2; still widely used; v3 for cloud'))
    lines.append(txt_row('Reindex poll   = GET /rest/api/2/reindex → check currentProgress and type'))
    lines.append(txt_row('Attachment tar = tar -czf; compress JIRA_HOME/data/attachments/'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-ops-cli', 'docs/tools/jira/operations/cli-reference/index.md', 'Jira CLI reference')
def tools_jira_ops_cli():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    lines = []
    lines.append(title_border(W2, 'Jira — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Jira Admin CLI — run on server as jira OS user')))
    lines.append(R(bMid(L, RR, './start-jira.sh / ./stop-jira.sh — start/stop Jira application server')))
    lines.append(R(bMid(L, RR, 'curl http://localhost:8080/status — returns JSON with state field')))
    lines.append(R(bMid(L, RR, 'psql -U jira jira -c "SELECT count(*) FROM jiraissue;" — count issues')))
    lines.append(R(bMid(L, RR, 'pg_dump -Fc -U jira jira -f /backup/jira_$(date +%Y%m%d).dump')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SSH to Jira server · run as jira OS user · DB on PostgreSQL VM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('start-jira.sh  = JIRA_INSTALL/bin/start-jira.sh; starts Tomcat JVM process'))
    lines.append(txt_row('stop-jira.sh   = graceful shutdown; waits for active requests to complete'))
    lines.append(txt_row('GET /status    = REST endpoint; returns state: RUNNING, STARTING, STOPPING, ERROR'))
    lines.append(txt_row('jiraissue table = PostgreSQL table containing all Jira issues'))
    lines.append(txt_row('pg_dump -Fc    = custom format dump; required for parallel pg_restore -j'))
    lines.append(txt_row('kill -3 PID    = SIGQUIT to JVM; thread dump printed to catalina.out'))
    lines.append(txt_row('JIRA_INSTALL   = installation directory; contains bin/, conf/, atlassian-jira/'))
    lines.append(txt_row('JIRA_HOME      = data directory; attachments/, indexes/, plugins/, log/'))
    lines.append(txt_row('catalina.out   = Tomcat stdout; JIRA_INSTALL/logs/catalina.out'))
    lines.append(txt_row('atlassian-jira.log = Jira application log; JIRA_HOME/log/atlassian-jira.log'))
    lines.append(txt_row('jira-application.properties = JIRA_HOME config; sets jira.home and cluster config'))
    lines.append(txt_row('dbconfig.xml   = JIRA_HOME; JDBC connection settings; edit to change DB params'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-sec', 'docs/tools/jira/security/index.md', 'Jira security overview')
def tools_jira_sec():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Security Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Security Domains')))
    lines.append(R(bMid(3, 99, 'Authentication: LDAP/SAML SSO; PAT for API; local break-glass accounts')))
    lines.append(R(bMid(3, 99, 'Authorisation: global perms → permission schemes → issue security schemes')))
    lines.append(R(bMid(3, 99, 'Encryption: TLS 1.2+ in transit; DB and JIRA_HOME encrypt at rest')))
    lines.append(R(bMid(3, 99, 'Hardening: disable anonymous access, restrict admin path, apply advisories')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Jira security follows same principles as Confluence: identity, access, transport'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Authentication'), bMid(B2_L, B2_R, 'Access Control'), bMid(B3_L, B3_R, 'Encryption'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP/AD sync'), bMid(B2_L, B2_R, 'Global permissions'), bMid(B3_L, B3_R, 'TLS 1.2+ HTTPS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML SSO via IdP'), bMid(B2_L, B2_R, 'Permission scheme'), bMid(B3_L, B3_R, 'DB encrypt at rest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA at IdP layer'), bMid(B2_L, B2_R, 'Issue security'), bMid(B3_L, B3_R, 'NFS encrypt at rest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PAT for API'), bMid(B2_L, B2_R, 'Admin IP ACL'), bMid(B3_L, B3_R, 'Key management'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local break-glass'), bMid(B2_L, B2_R, 'Anon access: off'), bMid(B3_L, B3_R, 'Cert rotation'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('LDAP/AD · IdP (Okta/ADFS) · reverse proxy for TLS · DB VM with encrypted disk'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Permission scheme = project-level ACL; maps operations to project roles/groups'))
    lines.append(txt_row('Issue security scheme = per-issue visibility restriction; hides issues from non-members'))
    lines.append(txt_row('Global permission = instance-wide right: Administer Jira, Create Projects, Browse Users'))
    lines.append(txt_row('Anonymous access = Admin > Global Permissions; remove "Any logged in user" for browse'))
    lines.append(txt_row('SAML SSO        = Jira as SP; IdP provides signed assertion; no password in Jira'))
    lines.append(txt_row('PAT             = Personal Access Token; Admin > Profile > PATs; use as Bearer token'))
    lines.append(txt_row('IP ACL          = restrict /admin and /secure/admin to corporate IP ranges via proxy'))
    lines.append(txt_row('Issue security  = security level scheme; assign issues to a level; control visibility'))
    lines.append(txt_row('TLS termination = reverse proxy (nginx/F5); Tomcat sees plain HTTP on port 8080'))
    lines.append(txt_row('MFA             = enforced at IdP; Jira trusts SAML assertion without re-checking'))
    lines.append(txt_row('Audit log       = Admin > Audit Log; records admin and permission events'))
    lines.append(txt_row('Security advisory = Atlassian PSIRT publishes CVEs; patch within SLA window'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-sec-enc', 'docs/tools/jira/security/encryption/index.md', 'Jira encryption')
def tools_jira_sec_enc():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Encryption — In Transit and At Rest')))
    lines.append(R(bMid(3, 99, 'In transit: TLS 1.2+ via reverse proxy; Tomcat internal HTTP only')))
    lines.append(R(bMid(3, 99, 'At rest: DB encryption with dm-crypt/LUKS or PostgreSQL TDE extension')))
    lines.append(R(bMid(3, 99, 'JIRA_HOME: NFS datastore encrypted at storage or hypervisor level')))
    lines.append(R(bMid(3, 99, 'Secrets: DB password in dbconfig.xml; store in Vault or encrypted env')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Every data path must be encrypted: browser, app-to-DB, and storage volumes'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'In Transit'), bMid(B2_L, B2_R, 'At Rest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS 1.2+ at LB/proxy'), bMid(B2_L, B2_R, 'DB: dm-crypt/LUKS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HTTP Tomcat internal'), bMid(B2_L, B2_R, 'NFS: storage encrypt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP: LDAPS port 636'), bMid(B2_L, B2_R, 'Backup: GPG encrypt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB: SSL JDBC sslmode'), bMid(B2_L, B2_R, 'VM: vSphere encrypt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HSTS: enabled at proxy'), bMid(B2_L, B2_R, 'Vault: secret store'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cert: RSA 2048 min'), bMid(B2_L, B2_R, 'Key rotation: annual'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Reverse proxy VM · Jira app VMs · PostgreSQL VM encrypted disk · NFS datastore'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TLS 1.2+     = minimum TLS version; disable TLS 1.0/1.1 at proxy level'))
    lines.append(txt_row('HSTS         = Strict-Transport-Security header; forces HTTPS after first visit'))
    lines.append(txt_row('LDAPS        = LDAP over SSL port 636; encrypts directory sync'))
    lines.append(txt_row('SSL JDBC     = sslmode=require in dbconfig.xml JDBC URL'))
    lines.append(txt_row('dm-crypt     = Linux kernel encryption; LUKS partition on DB data volume'))
    lines.append(txt_row('LUKS         = Linux Unified Key Setup; standard partition encryption'))
    lines.append(txt_row('GPG backup   = gpg --symmetric backup.tar.gz; passphrase stored in Vault'))
    lines.append(txt_row('vSphere encrypt = VM-level encryption using vSphere Native Key Provider'))
    lines.append(txt_row('Vault        = HashiCorp Vault; stores dbconfig.xml DB password'))
    lines.append(txt_row('dbconfig.xml = Jira DB connection config; in JIRA_HOME; contains JDBC URL'))
    lines.append(txt_row('Key rotation = annual encryption key change; planned maintenance window'))
    lines.append(txt_row('TDE          = Transparent Data Encryption at PostgreSQL level (pgcrypto)'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-sec-hard', 'docs/tools/jira/security/hardening/index.md', 'Jira hardening')
def tools_jira_sec_hard():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Hardening Guide')))
    lines.append(R(bMid(3, 99, 'Disable public sign-up and anonymous access in global permissions')))
    lines.append(R(bMid(3, 99, 'Restrict /secure/admin to corporate IP ranges via reverse proxy/WAF')))
    lines.append(R(bMid(3, 99, 'Apply Atlassian security advisories; stay within n-1 version')))
    lines.append(R(bMid(3, 99, 'Remove default admin account; named accounts with MFA via SAML IdP')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Hardening reduces attack surface at network, application, and OS layers'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Application Hardening'), bMid(B2_L, B2_R, 'OS/Network Hardening'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Disable anon access'), bMid(B2_L, B2_R, 'Firewall: 443 only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Remove default admin'), bMid(B2_L, B2_R, 'SSH key auth only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Disable public signup'), bMid(B2_L, B2_R, 'SELinux enforcing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Enable audit log'), bMid(B2_L, B2_R, 'Minimal OS packages'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Plugin allow-list'), bMid(B2_L, B2_R, 'OS patch schedule'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Security headers'), bMid(B2_L, B2_R, 'WAF for /admin path'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('WAF/reverse proxy · Jira VMs with SELinux · DB VM · firewall segmentation'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Public sign-up   = Admin > Global Permissions; remove Anyone can sign up'))
    lines.append(txt_row('Anonymous access = Admin > Global Permissions; remove Browse Projects for Anyone'))
    lines.append(txt_row('Security headers = CSP, X-Frame-Options, X-Content-Type-Options at proxy'))
    lines.append(txt_row('Plugin allow-list = Admin > Manage Apps; disable unsigned / unapproved plugins'))
    lines.append(txt_row('Audit log        = Admin > Audit Log; enable for all admin and config changes'))
    lines.append(txt_row('WAF              = Web Application Firewall; restrict /secure/admin to corp IPs'))
    lines.append(txt_row('SELinux          = enforcing mode on RHEL/CentOS; confines Tomcat process'))
    lines.append(txt_row('SSH key auth     = disable password SSH login on Jira server OS'))
    lines.append(txt_row('n-1 version      = stay one version behind latest max; patch critical CVEs'))
    lines.append(txt_row('Default admin    = rename or delete; create named admin accounts'))
    lines.append(txt_row('CSP              = Content-Security-Policy header; prevents cross-site scripting'))
    lines.append(txt_row('MFA              = multi-factor auth enforced at IdP; Jira trusts SAML assertion'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-sec-access', 'docs/tools/jira/security/access-control/index.md', 'Jira access control')
def tools_jira_sec_access():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Access Control Hierarchy')))
    lines.append(R(bMid(3, 99, 'Global perms → Permission scheme → Issue security scheme (most specific wins)')))
    lines.append(R(bMid(3, 99, 'Groups from LDAP/AD; assign groups to project roles; roles to permission schemes')))
    lines.append(R(bMid(3, 99, 'Issue security: hides individual issues from users without assigned security level')))
    lines.append(R(bMid(3, 99, 'Jira Admins group: limit to 2-3 named accounts; never use for day-to-day work')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Layers: global → project scheme → issue security; LDAP groups feed project roles'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Global Perms'), bMid(B2_L, B2_R, 'Project Perms'), bMid(B3_L, B3_R, 'Issue Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Administer Jira'), bMid(B2_L, B2_R, 'Browse project'), bMid(B3_L, B3_R, 'Security levels'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create projects'), bMid(B2_L, B2_R, 'Create issues'), bMid(B3_L, B3_R, 'Assign to issue'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Browse users'), bMid(B2_L, B2_R, 'Edit issues'), bMid(B3_L, B3_R, 'Default level'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Manage groups'), bMid(B2_L, B2_R, 'Admin project'), bMid(B3_L, B3_R, 'Restricted level'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP group sync'), bMid(B2_L, B2_R, 'Role members'), bMid(B3_L, B3_R, 'Inherited child'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('LDAP/AD for group source · Jira DB stores permission ACLs · IdP for auth'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Global permission = instance-wide; Administer Jira, Create Projects, Browse Users'))
    lines.append(txt_row('Permission scheme = project permission template; assign to one or many projects'))
    lines.append(txt_row('Issue security    = fine-grained visibility; can hide issues even within same project'))
    lines.append(txt_row('Project role      = named membership group per project (e.g. Developers, Reporters)'))
    lines.append(txt_row('Role member       = user or group assigned to a role in a specific project'))
    lines.append(txt_row('LDAP group sync   = groups imported from AD; assign to project roles'))
    lines.append(txt_row('Security level    = named tier within issue security scheme; assigned per issue'))
    lines.append(txt_row('Browse project    = minimum permission to see a project and its issues'))
    lines.append(txt_row('Admin project     = can manage project settings, components, versions'))
    lines.append(txt_row('Administer Jira   = full admin rights; can create schemes, users, and projects'))
    lines.append(txt_row('Issue inherit     = issue security can be inherited from parent issue'))
    lines.append(txt_row('Audit log         = Admin > Audit Log; records permission and scheme changes'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-sec-auth', 'docs/tools/jira/security/authentication/index.md', 'Jira authentication')
def tools_jira_sec_auth():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Authentication Methods')))
    lines.append(R(bMid(3, 99, 'LDAP: user/group sync from AD; Jira binds with user credentials for login')))
    lines.append(R(bMid(3, 99, 'SAML SSO: Jira as SP; Okta/ADFS as IdP; signed assertion; no password stored')))
    lines.append(R(bMid(3, 99, 'PAT: Personal Access Token; HTTP Bearer; profile-managed; revocable')))
    lines.append(R(bMid(3, 99, 'Crowd: optional Atlassian SSO; centralises auth across DC products')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  SSO preferred for humans; PAT for automation; local break-glass for emergencies'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Human Auth'), bMid(B2_L, B2_R, 'Service/API Auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML 2.0 SSO (primary)'), bMid(B2_L, B2_R, 'PAT: Bearer token'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP bind fallback'), bMid(B2_L, B2_R, 'Basic auth (legacy)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Crowd SSO (optional)'), bMid(B2_L, B2_R, 'OAuth app link'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA at IdP layer'), bMid(B2_L, B2_R, 'Service account'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Session: 30 min idle'), bMid(B2_L, B2_R, 'API rate: via proxy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local: break-glass'), bMid(B2_L, B2_R, 'Scope: read/write'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('LDAP/AD DCs · IdP (Okta/ADFS) with HA · Crowd server (optional) · Jira app VMs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SAML 2.0     = federated SSO; Jira validates signed IdP XML assertion'))
    lines.append(txt_row('LDAP bind    = Jira binds to LDAP with user creds; auth happens at directory'))
    lines.append(txt_row('PAT          = Personal Access Token; Jira Profile > Personal Access Tokens'))
    lines.append(txt_row('Basic auth   = base64 user:pass; deprecated; disable in favour of PAT'))
    lines.append(txt_row('Crowd        = Atlassian SSO; issues Crowd token accepted by all linked products'))
    lines.append(txt_row('OAuth app link = OAuth 1.0a/2.0 for trusted Jira-to-Confluence API calls'))
    lines.append(txt_row('Break-glass  = local admin; used when LDAP/IdP is unreachable'))
    lines.append(txt_row('Session      = idle timeout; Admin > Security > Session Configuration'))
    lines.append(txt_row('MFA          = enforced at IdP; Jira trusts SAML assertion without extra factor'))
    lines.append(txt_row('Service account = dedicated LDAP user for automation; prefer PAT instead'))
    lines.append(txt_row('Rate limiting = no native Jira rate limit; implement at reverse proxy (nginx)'))
    lines.append(txt_row('Assertion    = SAML XML signed by IdP; contains user attributes and groups'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Jira Troubleshooting ─────────────────────────────────────────────────────

@kb_diagram('tools-jira-trouble', 'docs/tools/jira/troubleshooting/index.md', 'Jira troubleshooting overview')
def tools_jira_trouble():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Troubleshooting Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Troubleshooting Framework')))
    lines.append(R(bMid(3, 99, 'Triage by symptom: slow, down, search broken, workflow stuck, auth fail')))
    lines.append(R(bMid(3, 99, 'First check: GET /status, heap usage, catalina.out, and DB connectivity')))
    lines.append(R(bMid(3, 99, 'Escalate to Atlassian Support with support-zip; attach thread + heap dumps')))
    lines.append(R(bMid(3, 99, 'Known issues: search jira.atlassian.com before opening support ticket')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Systematic triage reduces mean time to resolution for common Jira issues'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Diagnostics'), bMid(B2_L, B2_R, 'Common Issues'), bMid(B3_L, B3_R, 'Escalation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'GET /status check'), bMid(B2_L, B2_R, 'OOM / heap full'), bMid(B3_L, B3_R, 'Atlassian Support'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Thread dump'), bMid(B2_L, B2_R, 'Slow page loads'), bMid(B3_L, B3_R, 'support-zip bundle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Heap dump (OOM)'), bMid(B2_L, B2_R, 'Search broken'), bMid(B3_L, B3_R, 'Thread dump x3'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DB query analysis'), bMid(B2_L, B2_R, 'Workflow stuck'), bMid(B3_L, B3_R, 'jira.atlassian.com'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Log analysis'), bMid(B2_L, B2_R, 'Auth failures'), bMid(B3_L, B3_R, 'Hotfix / patch'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Jira VMs · PostgreSQL · NFS · monitoring (Prometheus/Zabbix) · log aggregator'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('support-zip    = Admin > System > Troubleshooting > Create Support Zip'))
    lines.append(txt_row('Thread dump    = kill -3 <pid>; take 3 at 10-second intervals for deadlock analysis'))
    lines.append(txt_row('Heap dump      = jmap -dump:format=b,file=jira.hprof <pid>; analyse with MAT'))
    lines.append(txt_row('Workflow stuck = issue cannot transition; check conditions/validators in workflow'))
    lines.append(txt_row('OOM            = OutOfMemoryError; increase -Xmx in setenv.sh'))
    lines.append(txt_row('Reindex        = Admin > System > Indexing > Full Re-Index; fixes stale search'))
    lines.append(txt_row('catalina.out   = primary startup and exception log; check first on any issue'))
    lines.append(txt_row('pg_stat_activity = PostgreSQL active queries; find long-running blocking queries'))
    lines.append(txt_row('MAT            = Eclipse Memory Analyser Tool; heap dump analysis'))
    lines.append(txt_row('Safe mode      = start Jira without plugins; diagnose plugin-related issues'))
    lines.append(txt_row('jira.atlassian.com = Atlassian public bug tracker for known Jira issues'))
    lines.append(txt_row('Hotfix         = patch JAR from Atlassian for critical CVEs between releases'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-trouble-diag', 'docs/tools/jira/troubleshooting/diagnostics/index.md', 'Jira diagnostics')
def tools_jira_trouble_diag():
    R, txt_row = make_helpers(W2)
    L, RR = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(L, RR)))
    lines.append(R(bMid(L, RR, 'Jira Diagnostic Runbook')))
    lines.append(R(bMid(L, RR, 'Step 1: curl -s http://localhost:8080/status — confirm state is RUNNING')))
    lines.append(R(bMid(L, RR, 'Step 2: grep -i "ERROR|OOM|Exception" catalina.out | tail -100')))
    lines.append(R(bMid(L, RR, 'Step 3: psql -U jira -c "SELECT count(*) FROM jiraissue;" — DB alive')))
    lines.append(R(bMid(L, RR, 'Step 4: df -h $JIRA_HOME — check disk; ls $JIRA_HOME/data/attachments')))
    lines.append(R(bBot(L, RR)))
    lines.append(txt_row())
    lines.append(txt_row('  Stop at first anomaly and remediate before continuing to next diagnostic step'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Application Diagnostics'), bMid(B2_L, B2_R, 'Infrastructure Diag'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'curl /status endpoint'), bMid(B2_L, B2_R, 'df -h JIRA_HOME'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'grep catalina.out'), bMid(B2_L, B2_R, 'mount | grep nfs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Thread dump: kill -3'), bMid(B2_L, B2_R, 'pg_stat_activity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Heap: jmap -histo'), bMid(B2_L, B2_R, 'netstat open ports'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Admin > System Info'), bMid(B2_L, B2_R, 'top / free -h'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'support-zip export'), bMid(B2_L, B2_R, 'journalctl -u jira'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SSH to Jira VMs · PostgreSQL admin access · NFS mount visibility'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('kill -3 PID    = sends SIGQUIT to JVM; thread dump printed to catalina.out'))
    lines.append(txt_row('jmap -histo    = histogram of JVM heap; lists top objects by class name'))
    lines.append(txt_row('pg_stat_activity = PostgreSQL running queries; find blocking and long-running SQL'))
    lines.append(txt_row('catalina.out   = Tomcat stdout log; JIRA_INSTALL/logs/catalina.out'))
    lines.append(txt_row('atlassian-jira.log = Jira application log; JIRA_HOME/log/atlassian-jira.log'))
    lines.append(txt_row('support-zip    = Admin > System > Troubleshooting; bundles logs and thread dumps'))
    lines.append(txt_row('top            = real-time process monitor; watch java process CPU and memory'))
    lines.append(txt_row('netstat        = open port check; confirm 8080 (Jira) and 5432 (PG) listening'))
    lines.append(txt_row('mount          = list mounted filesystems; verify NFS home mount present'))
    lines.append(txt_row('journalctl     = systemd log reader; use if Jira runs as systemd service'))
    lines.append(txt_row('free -h        = system memory; check if OS is swapping under memory pressure'))
    lines.append(txt_row('df -h          = disk usage; alert if JIRA_HOME volume exceeds 80% full'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-trouble-esc', 'docs/tools/jira/troubleshooting/escalation/index.md', 'Jira escalation')
def tools_jira_trouble_esc():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Escalation Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Escalation Tiers')))
    lines.append(R(bMid(3, 99, 'Tier 1: Ops — restart, reindex, check logs, restore from backup')))
    lines.append(R(bMid(3, 99, 'Tier 2: Senior engineer — JVM tuning, DB query analysis, plugin isolation')))
    lines.append(R(bMid(3, 99, 'Tier 3: Atlassian Support — ticket with support-zip; thread + heap dumps')))
    lines.append(R(bMid(3, 99, 'Tier 4: Atlassian escalation — P1 production down; 24x7 critical SLA')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Escalate: T1 > 30 min no resolution; T2 > 2 hr; T3 > 4 hr production down'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Escalation Criteria'), bMid(B2_L, B2_R, 'Artifacts to Gather'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service down >30 min'), bMid(B2_L, B2_R, 'support-zip bundle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Data loss suspected'), bMid(B2_L, B2_R, 'Thread dumps x3'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Security incident'), bMid(B2_L, B2_R, 'Heap dump (OOM)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Repeated OOM crash'), bMid(B2_L, B2_R, 'catalina.out tail'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Corruption suspected'), bMid(B2_L, B2_R, 'DB slow query log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Plugin breaks upgrade'), bMid(B2_L, B2_R, 'Version + patch info'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Jira VMs · PostgreSQL DB · monitoring/alerting · Atlassian Support portal'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('support-zip    = Admin > System > Troubleshooting > Create Support Zip'))
    lines.append(txt_row('Thread dump    = 3 dumps 10 seconds apart; detect deadlocks in worker threads'))
    lines.append(txt_row('Heap dump      = full JVM memory; jmap -dump:format=b,file=jira.hprof <pid>'))
    lines.append(txt_row('P1 incident    = production down; page on-call; escalate within 30 minutes'))
    lines.append(txt_row('Atlassian Support = support.atlassian.com; valid license required'))
    lines.append(txt_row('Safe mode      = start without plugins; -Djira.startup.options=safe-mode'))
    lines.append(txt_row('Plugin isolate = disable plugins one by one until issue resolves'))
    lines.append(txt_row('DB slow query  = set log_min_duration_statement=1000 in postgresql.conf'))
    lines.append(txt_row('Corruption     = DB row count vs index count mismatch; reindex if different'))
    lines.append(txt_row('Data loss      = check jiraissue table; deleted issues have DELETED status'))
    lines.append(txt_row('SLA            = P1 1hr response, P2 4hr, P3/P4 next business day'))
    lines.append(txt_row('Critical escalation = request via Atlassian account team for P1 outages'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-jira-trouble-common', 'docs/tools/jira/troubleshooting/common-issues/index.md', 'Jira common issues')
def tools_jira_trouble_common():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'Jira — Common Issues'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Jira Frequent Issue Patterns')))
    lines.append(R(bMid(3, 99, 'OOM crash: heap too small; increase -Xmx in setenv.sh; check for plugin leaks')))
    lines.append(R(bMid(3, 99, 'Slow issues: DB slow queries or GC pressure; check pg_stat_activity + GC log')))
    lines.append(R(bMid(3, 99, 'Search broken: Lucene index stale; trigger full reindex from Admin > Indexing')))
    lines.append(R(bMid(3, 99, 'Workflow stuck: check conditions/validators; view workflow in project settings')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Most Jira issues: memory, performance, search, workflow, or authentication'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Issue'), bMid(B2_L, B2_R, 'Resolution'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OOM / crash'), bMid(B2_L, B2_R, 'Increase -Xmx; check plugins'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Slow page loads'), bMid(B2_L, B2_R, 'DB index; tune GC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Search stale'), bMid(B2_L, B2_R, 'Full reindex from admin'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Workflow stuck'), bMid(B2_L, B2_R, 'Check conditions/validators'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML login fails'), bMid(B2_L, B2_R, 'Check IdP cert expiry'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Attachments 404'), bMid(B2_L, B2_R, 'Remount NFS JIRA_HOME'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Jira VMs · PostgreSQL · NFS home · IdP (Okta/ADFS) · load balancer'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('-Xmx         = JVM max heap; set in JIRA_INSTALL/bin/setenv.sh'))
    lines.append(txt_row('GC pressure  = excessive garbage collection; heap too small; increase -Xmx'))
    lines.append(txt_row('Full reindex = Admin > System > Indexing > Full Re-Index; fixes search issues'))
    lines.append(txt_row('Condition    = workflow transition prerequisite; check in Project > Workflows'))
    lines.append(txt_row('Validator    = field check before transition; fix fields or disable validator'))
    lines.append(txt_row('SAML cert    = IdP signing certificate; expires on schedule; update in SAML config'))
    lines.append(txt_row('NFS remount  = umount && mount JIRA_HOME; or restart nfs-client.target'))
    lines.append(txt_row('DB index     = PostgreSQL indexes on jiraissue; check with EXPLAIN ANALYZE'))
    lines.append(txt_row('Plugin leak  = disable suspect plugin to confirm memory leak'))
    lines.append(txt_row('LDAP sync    = Admin > User Management > User Directories > Synchronise'))
    lines.append(txt_row('Indexing     = Admin > System > Indexing; check index status and last run time'))
    lines.append(txt_row('GC log       = enable -Xlog:gc* in JVM_SUPPORT_RECOMMENDED_ARGS for analysis'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── ServiceNow ────────────────────────────────────────────────────────────────

@kb_diagram('tools-snow', 'docs/tools/servicenow/index.md', 'ServiceNow platform overview')
def tools_snow():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'ServiceNow — Platform Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'ServiceNow — SaaS ITSM Platform')))
    lines.append(R(bMid(3, 99, 'Delivery model: SaaS multi-instance; each customer gets dedicated instance')))
    lines.append(R(bMid(3, 99, 'Core processes: Incident, Problem, Change, Request, CMDB, ITOM')))
    lines.append(R(bMid(3, 99, 'MID Server: on-prem Java agent; bridges ServiceNow to internal networks')))
    lines.append(R(bMid(3, 99, 'Platform: Now Platform; GlideScript (server-side JS); Flow Designer')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  ServiceNow is the SaaS ITSM hub linking operations, development, and users'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Architecture'), bMid(B2_L, B2_R, 'Operations'), bMid(B3_L, B3_R, 'Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SaaS instance'), bMid(B2_L, B2_R, 'MID Server mgmt'), bMid(B3_L, B3_R, 'SAML/OAuth SSO'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MID Server'), bMid(B2_L, B2_R, 'Health checks'), bMid(B3_L, B3_R, 'ACL/roles'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Integration Hub'), bMid(B2_L, B2_R, 'Backup/restore'), bMid(B3_L, B3_R, 'Encryption'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'REST API'), bMid(B2_L, B2_R, 'Scripts'), bMid(B3_L, B3_R, 'Hardening'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Flow Designer'), bMid(B2_L, B2_R, 'Procedures'), bMid(B3_L, B3_R, 'Audit log'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ServiceNow SaaS data centres · MID Server VM on-prem · SMTP relay · LDAP/IdP'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Incident     = unplanned service disruption; goal is restore service (ITIL)'))
    lines.append(txt_row('Problem      = root cause investigation of one or more incidents'))
    lines.append(txt_row('Change       = controlled modification to IT environment; CAB approval flow'))
    lines.append(txt_row('CMDB         = Configuration Management Database; asset and relationship registry'))
    lines.append(txt_row('ITOM         = IT Operations Management; discovery, event management, health'))
    lines.append(txt_row('MID Server   = Management/Instrumentation/Discovery; on-prem Java agent for SNOW'))
    lines.append(txt_row('GlideScript  = ServiceNow server-side JavaScript runtime (Rhino engine)'))
    lines.append(txt_row('Flow Designer = low-code workflow automation; replaces legacy Orchestration'))
    lines.append(txt_row('Integration Hub = pre-built REST/SOAP connectors and flow steps'))
    lines.append(txt_row('SLA          = Service Level Agreement; time targets for incident resolution'))
    lines.append(txt_row('CAB          = Change Advisory Board; approves standard and major changes'))
    lines.append(txt_row('Instance     = dedicated ServiceNow tenant; prod/dev/test each separate'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-snow-arch', 'docs/tools/servicenow/architecture/index.md', 'ServiceNow architecture overview')
def tools_snow_arch():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'ServiceNow — Architecture Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'ServiceNow Architecture')))
    lines.append(R(bMid(3, 99, 'SaaS: customer instance on ServiceNow cloud; no on-prem app servers')))
    lines.append(R(bMid(3, 99, 'MID Server: on-prem JVM agent; polls ServiceNow ECC Queue for work items')))
    lines.append(R(bMid(3, 99, 'Data: proprietary Glide DB (MySQL-based); accessed via GlideRecord API')))
    lines.append(R(bMid(3, 99, 'API: REST Table API + Scripted REST API; HTTPS to instance.service-now.com')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  ServiceNow is SaaS; the only on-prem component is the optional MID Server'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cloud (ServiceNow SaaS)'), bMid(B2_L, B2_R, 'On-Prem (Customer)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Now Platform runtime'), bMid(B2_L, B2_R, 'MID Server JVM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Glide DB (MySQL)'), bMid(B2_L, B2_R, 'MID polls ECC Queue'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'REST Table API'), bMid(B2_L, B2_R, 'Discovery probes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Flow Designer'), bMid(B2_L, B2_R, 'JDBC/SNMP probes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Integration Hub'), bMid(B2_L, B2_R, 'Firewall: outbound 443'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'GlideScript runtime'), bMid(B2_L, B2_R, 'No inbound ports'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ServiceNow data centres (customer-invisible) · MID Server VM on-prem · outbound firewall'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Now Platform  = ServiceNow application runtime; hosts all ITSM apps'))
    lines.append(txt_row('Glide DB      = ServiceNow proprietary DB layer; built on MySQL; accessed via GlideRecord'))
    lines.append(txt_row('GlideRecord   = server-side JS API for DB CRUD; used in Business Rules and Scripts'))
    lines.append(txt_row('ECC Queue     = External Communication Channel; MID Server polls for work items'))
    lines.append(txt_row('MID Server    = on-prem Java agent; runs discovery, orchestration, and event probes'))
    lines.append(txt_row('Table API     = /api/now/table/{tableName}; REST CRUD for any ServiceNow table'))
    lines.append(txt_row('Flow Designer = drag-drop workflow builder; uses Actions and Triggers'))
    lines.append(txt_row('Integration Hub = connector library for Flow Designer; REST, JDBC, LDAP steps'))
    lines.append(txt_row('Discovery     = ITOM module; auto-populates CMDB by probing network devices'))
    lines.append(txt_row('Outbound only = MID Server initiates connection to ServiceNow; no inbound'))
    lines.append(txt_row('Instance URL  = https://customer.service-now.com; unique per customer tenant'))
    lines.append(txt_row('Prod/dev/test = separate ServiceNow instances; clone prod to dev for testing'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-snow-arch-how', 'docs/tools/servicenow/architecture/how-it-works/index.md', 'ServiceNow how it works')
def tools_snow_arch_how():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'ServiceNow — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'ServiceNow Request and Automation Flow')))
    lines.append(R(bMid(3, 99, 'User/API → HTTPS → Now Platform → GlideDB; Business Rules fire on record change')))
    lines.append(R(bMid(3, 99, 'Incident: create → categorise → assign → resolve → close (ITIL workflow)')))
    lines.append(R(bMid(3, 99, 'MID Server: ECC Queue poll → probe execution → result posted back to SNOW')))
    lines.append(R(bMid(3, 99, 'Flow Designer: trigger (table record event) → actions → integrations')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  ServiceNow processes three parallel flows: ITSM, automation, and discovery'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ITSM Flow'), bMid(B2_L, B2_R, 'Automation Flow'), bMid(B3_L, B3_R, 'Discovery Flow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'User submits ticket'), bMid(B2_L, B2_R, 'Flow trigger fires'), bMid(B3_L, B3_R, 'Schedule runs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Business Rule runs'), bMid(B2_L, B2_R, 'Actions execute'), bMid(B3_L, B3_R, 'ECC Queue item'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Assignment rule'), bMid(B2_L, B2_R, 'REST call out'), bMid(B3_L, B3_R, 'MID probe runs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SLA clock starts'), bMid(B2_L, B2_R, 'Response parsed'), bMid(B3_L, B3_R, 'Result posted'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Notification sent'), bMid(B2_L, B2_R, 'Record updated'), bMid(B3_L, B3_R, 'CMDB updated'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Resolve / close'), bMid(B2_L, B2_R, 'Log entry written'), bMid(B3_L, B3_R, 'CI discovered'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ServiceNow cloud infra · MID Server VM on-prem · SMTP relay · LDAP/AD DCs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Business Rule = server-side GlideScript triggered on DB insert/update/delete/query'))
    lines.append(txt_row('Assignment rule = auto-assigns incident to group based on category/subcategory'))
    lines.append(txt_row('SLA clock    = ServiceNow tracks breach time against SLA definition'))
    lines.append(txt_row('Flow trigger  = event that starts a Flow Designer flow (e.g. record insert)'))
    lines.append(txt_row('Action        = Flow Designer step: REST call, approval, sub-flow, script'))
    lines.append(txt_row('ECC Queue     = ServiceNow table; MID Server polls for probe/sensor commands'))
    lines.append(txt_row('Discovery probe = MID Server script that probes target IP for CI data'))
    lines.append(txt_row('CI            = Configuration Item; managed in CMDB (server, app, service, etc.)'))
    lines.append(txt_row('GlideRecord   = JS API for DB access: gr.addQuery(); gr.query(); gr.next()'))
    lines.append(txt_row('Notification  = email/SMS/push triggered by SNOW event or Business Rule'))
    lines.append(txt_row('Resolve       = final active state before Close; SLA stops on resolve'))
    lines.append(txt_row('CMDB update   = Discovery writes CI attributes to CMDB after probe results'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-snow-arch-int', 'docs/tools/servicenow/architecture/integrations/index.md', 'ServiceNow integrations')
def tools_snow_arch_int():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    M3 = (B3_L + B3_R) // 2
    lines = []
    lines.append(title_border(W2, 'ServiceNow — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'ServiceNow Integration Landscape')))
    lines.append(R(bMid(3, 99, 'Auth: SAML SSO (Okta/ADFS); MFA at IdP; LDAP user provisioning')))
    lines.append(R(bMid(3, 99, 'ITSM integrations: Jira (sync), PagerDuty (alert), Slack (notify)')))
    lines.append(R(bMid(3, 99, 'Monitoring: Zabbix/Prometheus/Datadog → SNOW event via REST or MID probe')))
    lines.append(R(bMid(3, 99, 'REST Table API: create/update incidents from external systems via HTTPS')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  ServiceNow sits at the integration centre of ops tooling ecosystem'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identity & Auth'), bMid(B2_L, B2_R, 'Dev & ITSM Tools'), bMid(B3_L, B3_R, 'Monitoring'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML SSO (Okta/ADFS)'), bMid(B2_L, B2_R, 'Jira: issue sync'), bMid(B3_L, B3_R, 'Zabbix alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP provisioning'), bMid(B2_L, B2_R, 'PagerDuty: escalate'), bMid(B3_L, B3_R, 'Prometheus events'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA via IdP'), bMid(B2_L, B2_R, 'Slack: notify'), bMid(B3_L, B3_R, 'Datadog events'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OAuth 2.0 API auth'), bMid(B2_L, B2_R, 'Confluence: KB link'), bMid(B3_L, B3_R, 'SNMP traps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Basic auth (legacy)'), bMid(B2_L, B2_R, 'Bitbucket PRs'), bMid(B3_L, B3_R, 'Syslog ingest'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('IdP (Okta/ADFS) · LDAP/AD · MID Server VM · SMTP relay · network connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SAML SSO     = ServiceNow supports SAML 2.0; configure under System Properties > SSO'))
    lines.append(txt_row('LDAP provisioning = ServiceNow LDAP integration creates/updates users from AD'))
    lines.append(txt_row('Table API    = REST endpoint for CRUD on any table; used by external integrations'))
    lines.append(txt_row('Jira sync    = Jira issues linked to SNOW changes via webhook or REST'))
    lines.append(txt_row('PagerDuty    = incident alert routing; SNOW triggers PagerDuty via REST outbound'))
    lines.append(txt_row('Slack        = SNOW sends notifications to Slack channels via Integration Hub'))
    lines.append(txt_row('OAuth 2.0    = recommended API auth method; create OAuth app under System OAuth'))
    lines.append(txt_row('SNMP trap    = network device alert; received by MID Server or event connector'))
    lines.append(txt_row('Syslog       = log stream from servers; parsed by SNOW event connector'))
    lines.append(txt_row('MID probe    = MID Server sensor that polls target systems for monitoring data'))
    lines.append(txt_row('Event connector = SNOW module that receives external events and creates incidents'))
    lines.append(txt_row('Integration Hub = pre-built action library for REST, JDBC, LDAP flow steps'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-snow-arch-design', 'docs/tools/servicenow/architecture/design-standards/index.md', 'ServiceNow design standards')
def tools_snow_arch_design():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    lines = []
    lines.append(title_border(W2, 'ServiceNow — Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'ServiceNow Design and Configuration Standards')))
    lines.append(R(bMid(3, 99, 'MID Server: min 4 vCPU / 8 GB RAM; Windows or Linux; n+1 for HA')))
    lines.append(R(bMid(3, 99, 'Instance: prod/test/dev; clone prod to test monthly for regression testing')))
    lines.append(R(bMid(3, 99, 'Script standards: always use GlideRecord; avoid cross-scope scripting')))
    lines.append(R(bMid(3, 99, 'Change management: all SNOW config changes via Update Set; tracked in source')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  SNOW design standards govern MID sizing, scripting, and config management'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MID Server Standards'), bMid(B2_L, B2_R, 'Platform Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Min 4 vCPU/8 GB'), bMid(B2_L, B2_R, 'Update Sets for changes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'n+1 MID redundancy'), bMid(B2_L, B2_R, 'Scripting: GlideRecord'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Outbound 443 only'), bMid(B2_L, B2_R, 'No cross-scope scripts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dedicated MID per env'), bMid(B2_L, B2_R, 'Test in sub-prod first'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'JVM: 4 GB heap min'), bMid(B2_L, B2_R, 'CMDB: CI naming std'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OS patching schedule'), bMid(B2_L, B2_R, 'SLA definition review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MID Server VMs (prod/test/dev) · firewall allowing outbound 443 only'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Update Set    = container for SNOW config changes; migrate via XML export/import'))
    lines.append(txt_row('GlideRecord   = SNOW server-side API; always preferred over raw SQL or direct DB'))
    lines.append(txt_row('Cross-scope   = accessing data from different application scope; use public APIs'))
    lines.append(txt_row('MID HA        = n+1 MID Servers; SNOW auto-fails over to available MID'))
    lines.append(txt_row('Clone         = copy prod data to test/dev; Admin > System Clone > Clone Instance'))
    lines.append(txt_row('CI naming     = consistent CMDB naming: hostname in lowercase, FQDN preferred'))
    lines.append(txt_row('SLA definition = Agreement + SLA Definition + Workflow; reviewed quarterly'))
    lines.append(txt_row('Dedicated MID = separate MID Server per environment (prod/test) to avoid confusion'))
    lines.append(txt_row('JVM heap      = set in JAVA_OPTS in MID Server wrapper.conf; min 4 GB for prod'))
    lines.append(txt_row('Script scope  = ServiceNow app scope isolation; prevents cross-app data access'))
    lines.append(txt_row('Sub-prod test = always test Update Sets in test before applying to prod'))
    lines.append(txt_row('Outbound 443  = MID Server only needs outbound HTTPS to *.service-now.com'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('tools-snow-ops', 'docs/tools/servicenow/operations/index.md', 'ServiceNow operations overview')
def tools_snow_ops():
    R, txt_row = make_helpers(W2)
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    lines = []
    lines.append(title_border(W2, 'ServiceNow — Operations Overview'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Daily Checks'), bMid(B2_L, B2_R, 'Weekly Tasks'), bMid(B3_L, B3_R, 'Monthly Tasks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MID Server status'), bMid(B2_L, B2_R, 'SLA compliance'), bMid(B3_L, B3_R, 'Instance health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Incident backlog'), bMid(B2_L, B2_R, 'User audit'), bMid(B3_L, B3_R, 'CMDB accuracy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Failed jobs check'), bMid(B2_L, B2_R, 'Flow error review'), bMid(B3_L, B3_R, 'Update Set review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert triage'), bMid(B2_L, B2_R, 'CMDB drift check'), bMid(B3_L, B3_R, 'Security review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ServiceNow SaaS cloud · MID Server VMs on-prem · monitoring for MID health'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('MID Server status = check via Admin > MID Servers; state should be Up'))
    lines.append(txt_row('Incident backlog = open incidents exceeding SLA; review daily for P1/P2'))
    lines.append(txt_row('Failed jobs = System > Scheduled Jobs; check for last-run errors'))
    lines.append(txt_row('SLA compliance = reports showing on-time resolution vs SLA targets'))
    lines.append(txt_row('Flow error = Flow Designer > Executions; check failed flow instances'))
    lines.append(txt_row('CMDB drift = CIs that were discovered but not matched; orphan records'))
    lines.append(txt_row('CMDB accuracy = percentage of CIs with complete and correct attribute data'))
    lines.append(txt_row('Update Set review = monthly review of pending Update Sets across instances'))
    lines.append(txt_row('Instance health = ServiceNow HI (Hi.service-now.com) for instance stats'))
    lines.append(txt_row('User audit = review inactive users and over-privileged role assignments'))
    lines.append(txt_row('Security review = monthly review of ACLs and admin role membership'))
    lines.append(txt_row('Alert triage = ServiceNow ITOM events; confirm actionable vs noise'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
