# Active Directory

Active Directory operational notes and deep-dive references.

## Kerberos Authentication Flow

```
  Client                  KDC (DC)                  Application Server
    │                        │                               │
    │── AS-REQ (username) ──►│                               │
    │   (pre-auth: enc TS)   │                               │
    │◄── AS-REP (TGT) ───────│                               │
    │    enc with krbtgt key  │                               │
    │                        │                               │
    │── TGS-REQ (TGT) ──────►│                               │
    │   (request: service SPN)│                               │
    │◄── TGS-REP (ST) ───────│                               │
    │    enc with svc key     │                               │
    │                        │                               │
    │── AP-REQ (ST + auth) ──────────────────────────────►  │
    │   (mutual auth option)  │                               │
    │◄── AP-REP ─────────────────────────────────────────── │
    │                        │                               │
    │           [Session established — Kerberos ticket valid]│
    │                        │                               │
    │── Resource Access ─────────────────────────────────►  │
    │◄── Response ────────────────────────────────────────── │
```

## LDAP Bind Flow

```
  Client                         Active Directory (LDAP)
    │                                      │
    │── TCP SYN ──────────────────────────►│  (port 389 / 636)
    │◄── TCP SYN-ACK ─────────────────────│
    │── LDAP Bind Request (DN + password) ►│
    │◄── Bind Response (success / error) ──│
    │                                      │
    │── Search Request (filter + scope) ──►│
    │◄── Search Entries ───────────────────│
    │◄── Search Done ──────────────────────│
    │                                      │
    │── Unbind ───────────────────────────►│
    │── TCP FIN ──────────────────────────►│
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>HA topology, components, connectivity, and sizing.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Naming conventions, build baseline, and configuration checklist.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Command reference by category with syntax and examples.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for daily checks, health, incident triage, and validation.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>VMware, backup tools, monitoring, authentication, and API integration.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span></a>
<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Opening a case, information to collect, support portal, and SLA tiers.</span></a>
</div>

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="domain-controllers/">
  <strong>Domain Controllers</strong>
  <span>Domain Controllers notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="dns-dependency/">
  <strong>DNS Dependency</strong>
  <span>DNS Dependency notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="groups/">
  <strong>Groups</strong>
  <span>Groups notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="gpos/">
  <strong>GPOs</strong>
  <span>GPOs notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="ldap/">
  <strong>LDAP</strong>
  <span>LDAP notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Troubleshooting notes, checks, commands, troubleshooting, and validation.</span>
</a>

</div>
