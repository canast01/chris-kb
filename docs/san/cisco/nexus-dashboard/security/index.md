# Nexus Dashboard — Security

┌────────────────────────────────── Cisco Nexus Dashboard — Security ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       ND security: RBAC roles, AAA via RADIUS/TACACS+/SAML, TLS certs, network segments       │   │
│   │         RBAC: site-admin, tenant-admin, operator, viewer; roles scoped per site/tenant        │   │
│   │            AAA: RADIUS, TACACS+, or SAML (SSO); local admin fallback always enabled           │   │
│   │        Network: OOB restricted to admin; Data VLAN to fabric only; no cross-VLAN access       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    AAA login → RBAC role → site/tenant scope → resource access → audit log                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │         Certificates        │  │         Audit / Acct        │   │
│   │          RBAC roles         │  │        ND UI TLS cert       │  │         User actions        │   │
│   │         RADIUS auth         │  │        App TLS certs        │  │         Login events        │   │
│   │         TACACS+ auth        │  │        CA-signed req.       │  │        Config changes       │   │
│   │           SAML/SSO          │  │         Cert renewal        │  │        Syslog export        │   │
│   │        Local fallback       │  │       Cipher restrict       │  │         Audit review        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Restrict ND OOB access to jump host / VPN only; never expose ND UI to public internet              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │    Mechanism     │     ND UI path    │      Verify      │      Notes       │   │
│   │       Auth       │   RADIUS/SAML    │     Admin>AAA     │    Login test    │   Local backup   │   │
│   │      AuthZ       │    RBAC role     │    Admin>Roles    │   Feature test   │     Per site     │   │
│   │       TLS        │  CA-signed cert  │   Admin>Security  │   Browser lock   │   Annual renew   │   │
│   │      Audit       │    Event log     │    Admin>Events   │   Log complete   │   Export SIEM    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: RADIUS/TACACS+/IdP on OOB management · cert private key in secrets vault                 │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RBAC           = Role-Based Access Control; roles in ND are scoped to site and tenant              │
│    site-admin     = Full access to a specific site; cannot modify ND cluster config                   │
│    tenant-admin   = Full access within a tenant (ACI); cannot access other tenants                    │
│    SAML           = Security Assertion Markup Language; used for SSO with corporate IdP               │
│    IdP            = Identity Provider (e.g. Okta, AD FS); issues SAML assertions to ND                │
│    Local fallback = ND admin account active even if AAA server unreachable; keep enabled              │
│    TLS cert       = ND HTTPS certificate; use CA-signed for browser trust and API clients             │
│    Cipher restrict = Disable TLS 1.0/1.1 and weak ciphers on ND; enforce TLS 1.2+                     │
│    OOB restrict   = Limit management network access to bastion hosts or VPN gateway only              │
│    Data VLAN      = Fabric-facing VLAN for telemetry; restrict to switch management subnets           │
│    Audit log      = ND logs every user action (login, config change) with user and timestamp          │
│    Syslog export  = Forward ND audit and system logs to centralised SIEM for retention                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
