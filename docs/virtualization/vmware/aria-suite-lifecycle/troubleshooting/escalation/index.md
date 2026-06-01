# Aria Suite Lifecycle — Escalation

```text
  LCM Escalation Path
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Collect upfront (avoids data-request delay)            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ vracli support-bundle   │ LCM + product versions        │    │
│  │ Request ID (if upgrade) │ Upgrade log (/vrlcm/upgrade/) │    │
│  │ openssl x509 output     │ Timeline: last good → failure  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                  │                                              │
│                  ▼                                              │
│  Step 2: Severity Assessment                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ S1: prod env down, no workaround → open SR + call NOW    │   │
│  │ S2: major feature unavailable → open SR (urgent)         │   │
│  │ S3: partial degradation, workaround → normal SR          │   │
│  │ S4: question / how-to → normal SR / KB search            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                  │                                              │
│                  ▼                                              │
│  Step 3: Escalation Triggers                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ S1 unresolved > 2h → Critical Escalation Team            │   │
│  │ Recurring / SLA breach → TAM engagement                  │   │
│  │ Do NOT power cycle partial-upgrade VMs without SR OK     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```
┌────────────────────────────────────── Aria Suite LCM Escalation ──────────────────────────────────────┐
│                                                                                                       │
│  Escalation with logscraper bundle, SR process, and TAM engagement for LCM.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │              SR Severity Levels             │   │
│   │             LCM UI inaccessible              │  │          P1: LCM down or data loss          │   │
│   │            All products degraded             │  │           P2: deploy/upgrade fails          │   │
│   │           Upgrade fails and stuck            │  │          P3: cert or feature issue          │   │
│   │          Cert expiry causing outage          │  │            P4: question / how-to            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Identify severity; run logscraper; open SR with bundle; call TAM for P1.                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SR Process                  │  │                TAM Engagement               │   │
│   │          1. Run logscraper + bundle          │  │             Call TAM for P1 now             │   │
│   │          2. Open GSS SR + severity           │  │           TAM escalates internally          │   │
│   │         3. Attach bundle + timeline          │  │              Bridge call for P1             │   │
│   │            4. Follow GSS guidance            │  │           Provide change log + env          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM; logscraper via LCM UI; GSS portal for SR; TAM for P1/P2 escalation                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Logscraper          = LCM tool collecting logs from all products; mandatory for SR                   │
│  Support Bundle      = LCM-level log archive from lcm-support.sh or VAMI                              │
│  GSS                 = Global Support Services; Broadcom support portal                               │
│  SR                  = Support Request; opened with severity and bundle attached                      │
│  P1 Severity         = LCM or product fully down; 24/7 response; bridge call                          │
│  P2 Severity         = Deploy/upgrade failure; priority business-hours response                       │
│  P3 Severity         = Cert or feature issue; standard SLA                                            │
│  TAM                 = Technical Account Manager; escalation for P1/P2                                │
│  Bridge Call         = Live call with GSS + TAM + customer for P1 resolution                          │
│  Change Log          = Recent changes provided to GSS for root cause analysis                         │
│  Environment Details = LCM environment config; share with GSS for context                             │
│  RCA                 = Root Cause Analysis document issued after P1 resolution                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

**Log bundle (required for all SRs):**

```bash
# Generate support bundle from LCM appliance SSH
ssh admin@lcm-prod-01.example.local
vracli support-bundle generate

# Bundle location — typically /data/support-bundles/<timestamp>.tar.gz
ls -lh /data/support-bundles/
```

The bundle includes: LCM application logs, service logs, deployment history, Locker metadata (no passwords), system diagnostics, and recent request audit trail.

**Additional data for specific issues:**

| Issue Type | Additional Data |
|---|---|
| Upgrade failure | Request ID from LCM UI; upgrade-specific log from `/var/log/vmware/vrlcm/upgrade/` |
| VIDM/authentication failure | VIDM appliance log bundle; browser HAR file of the failed login flow |
| Certificate failure | `openssl x509 -text` output for the failing certificate; trust chain verification output |
| UI issue | Browser console errors (F12 → Console); browser HAR file of the failing page load |
| Network/connectivity issue | `traceroute`, `curl -v` output between LCM and affected endpoint |

---

## SR Handoff Checklist

Before handing an SR to the next shift or to a specialist:

- [ ] SR number documented in the incident ticket
- [ ] Support bundle uploaded to the SR (confirm upload complete in the portal)
- [ ] Exact LCM version and affected product versions noted
- [ ] Timeline of events: last known good state → first observed failure → actions taken
- [ ] Any commands run on the LCM appliance or product VMs documented
- [ ] Current state of the product VMs (powered on/off, snapshot present/absent)
- [ ] Broadcom support contact name and case manager noted

---

## VMware by Broadcom Knowledge Base

Before opening an SR, search the Broadcom knowledge base for known issues:

- Search: `site:kb.vmware.com aria suite lifecycle <error message>`
- LCM release notes list known issues for each version — review before upgrades
- The VMware by Broadcom communities forum often has workarounds for common LCM errors

**Useful KB categories for LCM:**
- Upgrade failures: search `vRealize Suite Lifecycle upgrade fails`
- Certificate errors: search `LCM locker certificate import`
- VIDM integration: search `LCM identity manager`
