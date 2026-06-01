# Business Impact Assessment


<div class="kb-summary">
Business Impact Assessment reference covering Overview, Impact Dimensions, User Impact Categories, SLA Breach Assessment, Affected Services Inventory and 1 more sections.
</div>
```
┌──────────────────────────── Project Management Incident Management Impact ────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Incident Management: Project Management Incident Management Impact platform          │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │          Management: Project Management Incident Management Impact management console         │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Project Management Incident Management Impact infrastructure · management network · mon  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Incident Management = Project Management Incident Management Impact platform overview and core co  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Overview

A business impact assessment during an incident quantifies who is affected, which business processes are disrupted, what the financial and reputational exposure is, and whether SLA commitments are at risk. This assessment drives priority setting, escalation decisions, and stakeholder communication.

---

## Impact Dimensions

Assess impact across four dimensions simultaneously.

| Dimension      | Questions to Answer                                              |
|----------------|------------------------------------------------------------------|
| User count     | How many users are affected? Internal only or external/customers? |
| Service scope  | Which specific services or features are unavailable?            |
| Business process | Which business workflows are blocked or degraded?              |
| Data risk      | Is there any risk of data loss, corruption, or exposure?        |

Complete this assessment within 15 minutes of incident declaration for P1s.

---

## User Impact Categories

| Category              | Definition                                         | Priority Indicator |
|-----------------------|----------------------------------------------------|--------------------|
| All external users    | Full customer-facing outage                        | P1 automatic       |
| Subset of customers   | Geographic, tier, or feature-based outage          | P1 or P2           |
| All internal users    | Full internal service outage (e.g., VPN, email)    | P1 or P2           |
| Specific teams only   | Isolated to one department or function             | P2 or P3           |
| Single user           | Individual fault, no wider impact                  | P3 or P4           |

---

## SLA Breach Assessment

Check SLA status early — a P2 becomes a P1 if you are 30 minutes away from an SLA breach.

- [ ] Identify which SLAs apply to affected services
- [ ] Calculate time elapsed since incident start
- [ ] Determine time remaining before SLA breach (if any)
- [ ] If breach is within 30 minutes, escalate priority and notify account/customer success team
- [ ] Document SLA breach or near-miss in the incident ticket for reporting

| SLA Metric            | Contracted Target | Current Status        |
|-----------------------|-------------------|-----------------------|
| Availability (monthly)| 99.9%             | (calculate from uptime)|
| Response time P1      | 15 minutes        | (from alert to response)|
| Resolution time P1    | 4 hours           | (from alert to resolved)|

---

## Affected Services Inventory

During the incident, maintain a live list of affected services. Update it as scope becomes clearer.

- [ ] Primary service confirmed affected
- [ ] Dependencies of the primary service assessed
- [ ] Services that depend on the primary service assessed
- [ ] Third-party integrations assessed
- [ ] Internal tools that rely on the affected service assessed

Record the list in the incident ticket. Use the CMDB CI relationships view to speed up the dependency sweep.

---

## Financial and Reputational Exposure

For major incidents, estimating financial impact helps leadership make resource decisions.

- **Revenue impact** — if the service is revenue-generating, estimate lost transactions per hour
- **Contractual penalties** — check customer contracts for SLA penalty clauses
- **Reputational risk** — is this incident publicly visible? Are customers posting on social media?
- **Regulatory exposure** — does the incident involve personal data (GDPR, HIPAA)?

If any regulatory exposure is identified, notify the Legal and Compliance team immediately — do not wait for the incident to be resolved.
