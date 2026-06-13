---
tags:
  - dell
  - troubleshooting
---
# FOD — Common Issues


<div class="kb-summary">
Common FOD activation errors, feature entitlement failures, and troubleshooting unlicensed features.
</div>

```text
┌────────────────────────────────────── Dell FoD — Common Issues ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Common FoD issues: key rejection, feature mismatch, portal problems, and audit gaps      │   │
│   │     Key rejection: #1 issue is SN mismatch; verify SN in array GUI before contacting Dell     │   │
│   │      Feature mismatch: key unlocks different feature than expected; check key description     │   │
│   │      Audit gap: keys applied without CMDB update; discovered in quarterly reconciliation      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify issue → check event log error → verify SN/FW/scope → fix or escalate → document           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Key Problems        │  │       Feature Problems      │  │       Process Problems      │   │
│   │         SN mismatch         │  │        Wrong feature        │  │        No CMDB entry        │   │
│   │       Corrupt download      │  │          FW too old         │  │         No CR raised        │   │
│   │       Wrong model key       │  │       Bundle mismatch       │  │        Lost key file        │   │
│   │       Already applied       │  │        Feature hidden       │  │        Vault not used       │   │
│   │         Account link        │  │        Reboot needed        │  │          Audit gap          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Prevention: always confirm SN from array GUI, verify FW, and use key inventory before apply        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issue       │    Root Cause    │     Diagnostic    │    Resolution    │    Prevention    │   │
│   │   Key rejected   │   SN mismatch    │    Array GUI SN   │   Re-download    │ Confirm SN first │   │
│   │  Wrong feature   │   Scope error    │   Key desc. text  │ Buy correct key  │  Read key desc.  │   │
│   │    FW too old    │  Prereq not met  │     FW version    │  Upgrade first   │   Check compat   │   │
│   │  No CMDB entry   │   Process skip   │   CMDB vs array   │   Update CMDB    │  CR as reminder  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: chassis SN label is authoritative; array GUI SN must match; check both if uncertain      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SN mismatch    = Most common FoD failure; key cryptographically bound to different SN              │
│    Corrupt download = Incomplete .lic; browser cache or network issue; clear cache and re-download    │
│    Wrong model key = FoD keys are model-specific; a PowerMax key will not import on Unity XT          │
│    Already applied = Same key imported twice; array event log shows duplicate; harmless warning       │
│    Account link   = FoD key not visible in portal because SN not linked to support account            │
│    Wrong feature  = Purchased key for Feature A but needed Feature B; verify before checkout          │
│    FW too old     = Most FoD features require minimum firmware; run compatibility check first         │
│    Bundle mismatch = Key enables a feature bundle but not all features in bundle apply to model       │
│    Feature hidden = Feature activated but UI element hidden; check Settings > Features for status     │
│    Reboot needed  = Some FoD features (rare) require array restart; check release notes               │
│    No CMDB entry  = Engineer applied key but skipped CMDB update; found at quarterly audit            │
│    Vault not used = .lic file stored in email or share; security gap; move to vault immediately       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [Flex on Demand](../../index.md) reference.

---

| Symptom | Likely Cause | Action |
|---|---|---|
| Unexpected burst charges on FOD bill | Workload spike or snapshot/backup growth pushed usage above committed baseline | Review CloudIQ capacity trend for the billing period; identify the growth driver; adjust committed baseline if sustained |
| CloudIQ reports no telemetry for a FOD-enrolled system | Secure Connect Gateway offline or CloudIQ agent not running | Check SCG appliance health; verify outbound HTTPS connectivity to Dell CloudIQ endpoints |
| FOD capacity ceiling reached (no more burst available) | All pre-installed burst capacity is consumed | Contact Dell account team to install additional physical capacity under the FOD agreement |
| Committed baseline appears incorrect in APEX Console | Baseline was set at contract time and workload changed | Submit a baseline adjustment request through APEX Console or Dell account team |

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
