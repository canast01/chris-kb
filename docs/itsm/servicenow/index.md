# ServiceNow

<div class="kb-summary">
ServiceNow knowledge base covering multi-instance SaaS architecture, ITSM/CMDB processes, MID Server integration, security, and troubleshooting.
</div>

```text
┌─────────────────────────────────── ServiceNow — Platform Overview ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                ServiceNow — SaaS ITSM Platform                                │   │
│   │           Delivery model: SaaS multi-instance; each customer gets dedicated instance          │   │
│   │                 Core processes: Incident, Problem, Change, Request, CMDB, ITOM                │   │
│   │            MID Server: on-prem Java agent; bridges ServiceNow to internal networks            │   │
│   │              Platform: Now Platform; GlideScript (server-side JS); Flow Designer              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    ServiceNow is the SaaS ITSM hub linking operations, development, and users                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │        SaaS instance        │  │       MID Server mgmt       │  │        SAML/OAuth SSO       │   │
│   │          MID Server         │  │        Health checks        │  │          ACL/roles          │   │
│   │       Integration Hub       │  │        Backup/restore       │  │          Encryption         │   │
│   │           REST API          │  │           Scripts           │  │          Hardening          │   │
│   │        Flow Designer        │  │          Procedures         │  │          Audit log          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS data centres · MID Server VM on-prem · SMTP relay · LDAP/IdP                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Incident     = unplanned service disruption; goal is restore service (ITIL)                          │
│  Problem      = root cause investigation of one or more incidents                                     │
│  Change       = controlled modification to IT environment; CAB approval flow                          │
│  CMDB         = Configuration Management Database; asset and relationship registry                    │
│  ITOM         = IT Operations Management; discovery, event management, health                         │
│  MID Server   = Management/Instrumentation/Discovery; on-prem Java agent for SNOW                     │
│  GlideScript  = ServiceNow server-side JavaScript runtime (Rhino engine)                              │
│  Flow Designer = low-code workflow automation; replaces legacy Orchestration                          │
│  Integration Hub = pre-built REST/SOAP connectors and flow steps                                      │
│  SLA          = Service Level Agreement; time targets for incident resolution                         │
│  CAB          = Change Advisory Board; approves standard and major changes                            │
│  Instance     = dedicated ServiceNow tenant; prod/dev/test each separate                              │
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
  <span>Incident, change, request, and work note procedures.</span>
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
