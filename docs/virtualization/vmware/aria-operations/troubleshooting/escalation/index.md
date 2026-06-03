# Aria Operations — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Support Bundle Collection, Information to Collect Before Opening a Case, SLA Tiers, Escalation Path and 2 more sections.
</div>

## Support Portal

**Broadcom Support Portal:** [https://support.broadcom.com](https://support.broadcom.com)

Log in with your Broadcom Customer Connect account. Aria Operations (formerly vRealize Operations) cases are filed under the **VMware Cloud Foundation** or **Aria** product category.

---

## Support Bundle Collection

Always attach a support bundle when opening a case.

### Via UI

```text
┌───────────────────────────────────── Aria Operations Escalation ──────────────────────────────────────┐
│                                                                                                       │
│  SR process, P1/P2 severity definitions, and TAM engagement for Aria Operations.                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │              SR Severity Levels             │   │
│   │           vROps UI completely down           │  │         P1: monitoring down/no data         │   │
│   │          All adapters disconnected           │  │          P2: major adapter failure          │   │
│   │             Cluster node offline             │  │          P3: feature broken or slow         │   │
│   │          Upgrade fails or corrupts           │  │            P4: question / how-to            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Identify severity; open SR with bundle; engage TAM for P1/P2 platform outages.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SR Process                  │  │                TAM Engagement               │   │
│   │          1. Generate support bundle          │  │         Call TAM for P1 immediately         │   │
│   │          2. Open GSS SR + severity           │  │         TAM escalates to engineering        │   │
│   │         3. Attach bundle + timeline          │  │           Join bridge call for P1           │   │
│   │            4. Follow GSS guidance            │  │          Provide change log to TAM          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster; support bundle from SSH or VAMI; GSS portal for SR submission                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Support Bundle      = Log archive; always attach to SR before GSS can assist                         │
│  GSS                 = Global Support Services; Broadcom support portal                               │
│  SR                  = Support Request; tracks issue from open to resolution                          │
│  P1 Severity         = Production monitoring down; 24/7 response; bridge call                         │
│  P2 Severity         = Major degradation; priority business-hours response                            │
│  P3 Severity         = Feature broken; standard SLA response                                          │
│  TAM                 = Technical Account Manager; internal escalation path                            │
│  Bridge Call         = Live conference call for P1; GSS + TAM + customer                              │
│  Change Log          = Timeline of recent changes; critical for root cause analysis                   │
│  Engineering Escalation= GSS routes SR to product engineering for complex bugs                        │
│  RCA                 = Root Cause Analysis; document issued after P1 resolution                       │
│  Upgrade Corruption  = Data or config damaged by failed upgrade; always P1/P2                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── Aria Operations Escalation ──────────────────────────────────────┐
│                                                                                                       │
│  SR process, P1/P2 severity definitions, and TAM engagement for Aria Operations.                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │              SR Severity Levels             │   │
│   │           vROps UI completely down           │  │         P1: monitoring down/no data         │   │
│   │          All adapters disconnected           │  │          P2: major adapter failure          │   │
│   │             Cluster node offline             │  │          P3: feature broken or slow         │   │
│   │          Upgrade fails or corrupts           │  │            P4: question / how-to            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Identify severity; open SR with bundle; engage TAM for P1/P2 platform outages.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SR Process                  │  │                TAM Engagement               │   │
│   │          1. Generate support bundle          │  │         Call TAM for P1 immediately         │   │
│   │          2. Open GSS SR + severity           │  │         TAM escalates to engineering        │   │
│   │         3. Attach bundle + timeline          │  │           Join bridge call for P1           │   │
│   │            4. Follow GSS guidance            │  │          Provide change log to TAM          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster; support bundle from SSH or VAMI; GSS portal for SR submission                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Support Bundle      = Log archive; always attach to SR before GSS can assist                         │
│  GSS                 = Global Support Services; Broadcom support portal                               │
│  SR                  = Support Request; tracks issue from open to resolution                          │
│  P1 Severity         = Production monitoring down; 24/7 response; bridge call                         │
│  P2 Severity         = Major degradation; priority business-hours response                            │
│  P3 Severity         = Feature broken; standard SLA response                                          │
│  TAM                 = Technical Account Manager; internal escalation path                            │
│  Bridge Call         = Live conference call for P1; GSS + TAM + customer                              │
│  Change Log          = Timeline of recent changes; critical for root cause analysis                   │
│  Engineering Escalation= GSS routes SR to product engineering for complex bugs                        │
│  RCA                 = Root Cause Analysis; document issued after P1 resolution                       │
│  Upgrade Corruption  = Data or config damaged by failed upgrade; always P1/P2                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Information to Collect Before Opening a Case

| Item | Where to Find |
|------|--------------|
| Product version | Administration > About |
| Cluster topology (nodes, roles) | Administration > Cluster Management |
| Affected adapter / resource | Administration > Solutions |
| Symptom description and timeline | Incident notes |
| Active alerts / error messages | Screenshots or alert export |
| Support bundle | Generated above |
| vSphere / NSX version interop | Check interop matrix |

---

## SLA Tiers

| Priority | Description | Initial Response |
|----------|-------------|-----------------|
| P1 — Critical | Production down, full outage | 30 minutes |
| P2 — High | Significant degradation, workaround available | 4 hours |
| P3 — Medium | Partial impact, non-urgent | Next business day |
| P4 — Low | General question, enhancement request | Next business day |

---

## Escalation Path

1. Open case via Broadcom Support Portal with all information collected above.
2. If no response within SLA: use portal escalation button or call support line.
3. For P1: request **duty manager escalation** via phone.
4. Engage internal VMware/Broadcom TAM (Technical Account Manager) if available.

---

## Useful Links

| Resource | URL |
|----------|-----|
| Broadcom Support Portal | https://support.broadcom.com |
| Aria Operations Documentation | https://docs.vmware.com/en/VMware-Aria-Operations/ |
| VMware Interoperability Matrix | https://interopmatrix.vmware.com/ |
| Broadcom Lifecycle Policy | https://support.broadcom.com/lifecycle-management |
| Broadcom Knowledge Base | https://kb.vmware.com |

---

## Related Sections

- [Operations](../../operations/index.md) — support bundle generation
- [Diagnostics](../diagnostics/index.md) — pre-case diagnostics
- [Install & Upgrade](../../operations/install-upgrade/index.md) — version and EOL information
