# Confluence

<div class="kb-summary">
Confluence knowledge base covering Data Center cluster architecture, space and page management, authentication, and troubleshooting.
</div>

```
┌───────────────────────────────── Confluence — Wiki Platform Overview ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                           Atlassian Confluence — Data Center Edition                          │   │
│   │         Enterprise wiki: Spaces → Pages → Page Tree with inline comments and versions         │   │
│   │              App tier: Tomcat on port 8090 (HTTP) / 443 (HTTPS via reverse proxy)             │   │
│   │           Data tier: PostgreSQL or Oracle DB + shared NFS home (attachments/indexes)          │   │
│   │           Search: Lucene index rebuilt from DB on demand; re-index from admin panel           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Confluence tiers span web, application, database, and shared storage layers                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      Tomcat app server      │  │      Install / Upgrade      │  │     LDAP user directory     │   │
│   │      PostgreSQL DB tier     │  │      Backup and restore     │  │        SAML SSO / MFA       │   │
│   │       NFS shared home       │  │        Health checks        │  │      Space permissions      │   │
│   │     Lucene search index     │  │        CLI reference        │  │      TLS / HTTPS config     │   │
│   │      REST API · Macros      │  │     Scripts · Procedures    │  │       Hardening guide       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere VMs: app nodes · DB VM (PostgreSQL) · NFS fileserver for shared home · Load balancer         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Space        = top-level container for pages; can be personal, project, or team scoped               │
│  Page tree    = hierarchical page structure within a space; parent/child relationships                │
│  Macro        = dynamic content block (e.g. Table of Contents, Include Page, Status)                  │
│  Shared home  = NFS mount shared by all DC nodes; stores attachments and search index                 │
│  Lucene       = embedded full-text index; must be rebuilt after DB restores                           │
│  JDBC         = Java Database Connectivity; Confluence connects to DB via JDBC URL                    │
│  DC node      = one Confluence app server in a Data Center cluster behind a load balancer             │
│  Hazelcast    = in-memory data grid; Confluence DC uses it for cache clustering                       │
│  SAML         = Security Assertion Markup Language; Confluence delegates auth to IdP                  │
│  XML backup   = Confluence site export (Admin > Backup); not for large prod restores                  │
│  Atlassian DC = Data Center licensing tier; supports clustering and high availability                 │
│  REST API     = Confluence v2 REST API; spaces/pages/content endpoints on port 8090                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────── Confluence — Wiki Platform Overview ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                           Atlassian Confluence — Data Center Edition                          │   │
│   │         Enterprise wiki: Spaces → Pages → Page Tree with inline comments and versions         │   │
│   │              App tier: Tomcat on port 8090 (HTTP) / 443 (HTTPS via reverse proxy)             │   │
│   │           Data tier: PostgreSQL or Oracle DB + shared NFS home (attachments/indexes)          │   │
│   │           Search: Lucene index rebuilt from DB on demand; re-index from admin panel           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Confluence tiers span web, application, database, and shared storage layers                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      Tomcat app server      │  │      Install / Upgrade      │  │     LDAP user directory     │   │
│   │      PostgreSQL DB tier     │  │      Backup and restore     │  │        SAML SSO / MFA       │   │
│   │       NFS shared home       │  │        Health checks        │  │      Space permissions      │   │
│   │     Lucene search index     │  │        CLI reference        │  │      TLS / HTTPS config     │   │
│   │      REST API · Macros      │  │     Scripts · Procedures    │  │       Hardening guide       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere VMs: app nodes · DB VM (PostgreSQL) · NFS fileserver for shared home · Load balancer         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Space        = top-level container for pages; can be personal, project, or team scoped               │
│  Page tree    = hierarchical page structure within a space; parent/child relationships                │
│  Macro        = dynamic content block (e.g. Table of Contents, Include Page, Status)                  │
│  Shared home  = NFS mount shared by all DC nodes; stores attachments and search index                 │
│  Lucene       = embedded full-text index; must be rebuilt after DB restores                           │
│  JDBC         = Java Database Connectivity; Confluence connects to DB via JDBC URL                    │
│  DC node      = one Confluence app server in a Data Center cluster behind a load balancer             │
│  Hazelcast    = in-memory data grid; Confluence DC uses it for cache clustering                       │
│  SAML         = Security Assertion Markup Language; Confluence delegates auth to IdP                  │
│  XML backup   = Confluence site export (Admin > Backup); not for large prod restores                  │
│  Atlassian DC = Data Center licensing tier; supports clustering and high availability                 │
│  REST API     = Confluence v2 REST API; spaces/pages/content endpoints on port 8090                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Page management, search, templates, and maintenance.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, permissions, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
