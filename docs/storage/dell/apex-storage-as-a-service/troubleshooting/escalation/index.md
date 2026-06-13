---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# APEX Storage as a Service — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Escalation Path.
</div>

```text
┌──────────────────────────────────── Dell Apex STaaS — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Apex escalation: severity triage, SR creation, log collection, TAC engagement         │   │
│   │           P1 (production down): call Dell immediately + open SR; 4-hour response SLA          │   │
│   │       P2 (degraded): open SR online; 8-hour response; attach multipath and CloudIQ logs       │   │
│   │             Collect before calling: host OS logs, CloudIQ bundle, SCG diagnostics             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Triage severity → collect logs → open SR → Dell responds → RCA → preventive action                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Severity          │  │       What to Collect       │  │          SR Process         │   │
│   │        P1: prod down        │  │        multipath -ll        │  │       Apex Console SR       │   │
│   │         P2: degraded        │  │        CloudIQ bundle       │  │        Phone + online       │   │
│   │         P3: limited         │  │        dmesg / syslog       │  │        Online SR only       │   │
│   │         P4: question        │  │        SCG diagnostic       │  │        Community/chat       │   │
│   │         Escalate P1         │  │        CloudIQ events       │  │       Manager escalate      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Always note time of issue, affected volumes, and host count when opening SR                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Severity     │     Criteria     │    SLA respond    │     Contact      │    Escalation    │   │
│   │        P1        │    Prod down     │      4 hours      │    Phone + SR    │   Exec if >4h    │   │
│   │        P2        │     Degraded     │      8 hours      │    SR + phone    │    Mgr if >8h    │   │
│   │        P3        │   Limited imp.   │   Next bus. day   │    SR online     │    SR comment    │   │
│   │        P4        │     Question     │    Best effort    │   Portal/chat    │   None needed    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: collect cable/SFP photos for P1 hardware failures · note rack location                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    P1 severity    = Production storage completely unavailable; call Dell 24x7 phone line              │
│    P2 severity    = Production degraded (slow, one path lost); open SR + follow up by phone           │
│    P3 severity    = Non-production or isolated issue; online SR; next business day response           │
│    P4 severity    = General question or feature request; community or chat; no SLA                    │
│    CloudIQ bundle = Downloadable diagnostic package from CloudIQ; attach to SR                        │
│    SCG diagnostic = SCG built-in log collection; download from SCG web UI                             │
│    dmesg          = Linux kernel ring buffer; shows SCSI errors, path events, I/O failures            │
│    syslog         = System log; contains iSCSI daemon, multipath, and storage driver events           │
│    Manager escalate = Requesting Dell TAC manager involvement if SLA is not being met                 │
│    RCA            = Root Cause Analysis; Dell provides written cause and prevention plan              │
│    Exec escalation = For P1 unresolved >4h; request to Dell account team for exec attention           │
│    SR number      = Service Request ticket; record and share with all team members involved           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [APEX Storage as a Service](../../index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Support Portal

Open a support case via the APEX Console (APEX Console → Support → New Case) or at [https://www.dell.com/support](https://www.dell.com/support). Dell is responsible for infrastructure remediation under the APEX STaaS agreement.

## Escalation Path

1. For SLA-impacting issues (system offline, performance below committed SLA), open a **P1 support case** via APEX Console immediately
2. Contact your **Dell account team** to escalate if the issue is not resolved within the contracted response time
3. For billing or contractual disputes, engage your Dell account team directly — these are typically not resolved through standard support cases
4. Check [https://www.dell.com/support/incidents-outages](https://www.dell.com/support/incidents-outages) for any announced APEX service incidents before escalating

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
