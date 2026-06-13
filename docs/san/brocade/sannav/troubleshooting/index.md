---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
---
# SANnav — Troubleshooting


<div class="kb-summary">
Diagnosing SANnav connectivity issues, fabric discovery failures, certificate errors, and alert configuration problems.
</div>

```text
┌────────────────────────────────────── SANnav — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     SANnav troubleshooting: connectivity, data quality, authentication, and service health    │   │
│   │        UI/access: login failure, session expiry, certificate error, LDAP not reachable        │   │
│   │     Discovery: switch unreachable, SNMP timeout, wrong credentials, FabricOS incompatible     │   │
│   │          Escalation: collect /var/log/sannav/ log bundle; open Broadcom support case          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    UI/access issues → discovery problems → data quality → SANnav service → escalation                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         UI / Access         │  │          Discovery          │  │          Escalation         │   │
│   │        Login failure        │  │        Switch offline       │  │         Collect logs        │   │
│   │       Session expired       │  │         SNMP timeout        │  │          DB backup          │   │
│   │          Cert error         │  │        Auth mismatch        │  │         Broadcom TAC        │   │
│   │         LDAP timeout        │  │          FW too old         │  │        Syslog review        │   │
│   │       Blank dashboard       │  │          Data gaps          │  │       Service restart       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Restart SANnav services via systemctl before opening a support case                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │   First check    │   Log to review   │       Fix        │    Escalation    │   │
│   │   Login fails    │ LDAP reachable?  │     sannav.log    │   LDAP restart   │   Broadcom TAC   │   │
│   │  Switch offline  │ Ping switch mgmt │   discovery.log   │  Re-add switch   │   TAC + creds    │   │
│   │     Data gap     │Poll interval OK? │    polling.log    │  Manual refresh  │  TAC if persist  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: management network path · SANnav VM CPU/RAM health · switch SSH reachability             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    sannav.log    = Main SANnav application log; in /var/log/sannav/ on the SANnav VM                  │
│    discovery.log = Discovery engine log; shows switch reachability and poll failures                  │
│    polling.log   = Counter collection log; shows which polls succeeded or timed out                   │
│    Service restart = systemctl restart sannav; clears transient service issues                        │
│    DB backup     = Take SANnav DB backup before any upgrade or troubleshooting attempt                │
│    Log bundle    = Admin > Support > Download Logs; zip of all SANnav logs for TAC                    │
│    Cert error    = HTTPS cert expired or self-signed; renew via Admin > Certificates                  │
│    LDAP timeout  = SANnav cannot reach LDAP server; check network path and LDAP URL                   │
│    Data gap      = Performance counter missing for a time period; usually poll failure                │
│    FW too old    = Switch FabricOS below minimum SANnav supported version                             │
│    Broadcom TAC  = Technical Assistance Centre for Brocade/SANnav support cases                       │
│    Blank dash    = Dashboard shows no data; check SANnav services and DB health first                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known problems, symptoms, and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to Broadcom TAC with the right data.</span>
</a>

</div>

