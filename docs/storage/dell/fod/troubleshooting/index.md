# FOD — Troubleshooting


```text
┌───────────────────────────────────── Dell FoD — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       FoD troubleshooting: key rejection, feature not activating, portal access failures      │   │
│   │      Key rejection: SN mismatch, wrong key scope, corrupt file — re-download from portal      │   │
│   │    Feature not active: firmware prereq not met, bundle partially applied, license conflict    │   │
│   │       Portal issues: account MFA locked, key not in order history, account link missing       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom → check array event log → verify SN and FW → re-download if needed → Dell SR               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Key Issues         │  │        Feature Issues       │  │        Portal Issues        │   │
│   │       Rejection error       │  │        Not activating       │  │        Login failure        │   │
│   │         SN mismatch         │  │        FW prereq fail       │  │        Key not found        │   │
│   │         Wrong scope         │  │        Partial bundle       │  │        No entitlement       │   │
│   │         Corrupt file        │  │       License conflict      │  │         Account link        │   │
│   │       Already applied       │  │      Wrong array model      │  │          MFA locked         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Collect: array SN, event log error text, firmware version, and portal order screenshot             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │      Cause       │       Check       │       Fix        │   Escalate If    │   │
│   │   Key rejected   │   SN mismatch    │    Array GUI SN   │   Re-download    │  After 2 tries   │   │
│   │    Not active    │    FW prereq     │   Firmware ver.   │  Upgrade array   │   Dell TAC SR    │   │
│   │   Portal login   │    MFA locked    │    Dell account   │  Account reset   │   Dell support   │   │
│   │   Key missing    │  Wrong account   │   Order history   │  Link accounts   │  Dell licensing  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: confirm SN from chassis label; do not rely on documentation which may be outdated        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Rejection error = Array event log shows specific error code; note exact text for Dell TAC          │
│    SN mismatch    = Key file SN differs from array SN; most common FoD failure; re-download           │
│    Wrong scope    = Key unlocks different feature or tier than intended; verify before purchase       │
│    Corrupt file   = Download interrupted; browser saved incomplete .lic; re-download via HTTPS        │
│    FW prereq fail = Array firmware below minimum required for feature; upgrade before applying        │
│    Partial bundle = Bundle key partially active; some features of bundle blocked by FW prereq         │
│    License conflict = Two keys conflict on same feature; contact Dell TAC; do not apply more keys     │
│    Wrong array model = FoD key model-specific; a Unity key will not apply to a PowerStore             │
│    Already applied = Duplicate key import attempt; array shows duplicate; harmless but contact Dell   │
│    No entitlement = Support contract not linked to SN; contact Dell licensing team to link            │
│    Account link   = Link service tag to Dell support account via support.dell.com portal              │
│    MFA locked     = Too many failed MFA attempts; Dell support can unlock the portal account          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌───────────────────────────────────── Dell FoD — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       FoD troubleshooting: key rejection, feature not activating, portal access failures      │   │
│   │      Key rejection: SN mismatch, wrong key scope, corrupt file — re-download from portal      │   │
│   │    Feature not active: firmware prereq not met, bundle partially applied, license conflict    │   │
│   │       Portal issues: account MFA locked, key not in order history, account link missing       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom → check array event log → verify SN and FW → re-download if needed → Dell SR               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Key Issues         │  │        Feature Issues       │  │        Portal Issues        │   │
│   │       Rejection error       │  │        Not activating       │  │        Login failure        │   │
│   │         SN mismatch         │  │        FW prereq fail       │  │        Key not found        │   │
│   │         Wrong scope         │  │        Partial bundle       │  │        No entitlement       │   │
│   │         Corrupt file        │  │       License conflict      │  │         Account link        │   │
│   │       Already applied       │  │      Wrong array model      │  │          MFA locked         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Collect: array SN, event log error text, firmware version, and portal order screenshot             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │      Cause       │       Check       │       Fix        │   Escalate If    │   │
│   │   Key rejected   │   SN mismatch    │    Array GUI SN   │   Re-download    │  After 2 tries   │   │
│   │    Not active    │    FW prereq     │   Firmware ver.   │  Upgrade array   │   Dell TAC SR    │   │
│   │   Portal login   │    MFA locked    │    Dell account   │  Account reset   │   Dell support   │   │
│   │   Key missing    │  Wrong account   │   Order history   │  Link accounts   │  Dell licensing  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: confirm SN from chassis label; do not rely on documentation which may be outdated        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Rejection error = Array event log shows specific error code; note exact text for Dell TAC          │
│    SN mismatch    = Key file SN differs from array SN; most common FoD failure; re-download           │
│    Wrong scope    = Key unlocks different feature or tier than intended; verify before purchase       │
│    Corrupt file   = Download interrupted; browser saved incomplete .lic; re-download via HTTPS        │
│    FW prereq fail = Array firmware below minimum required for feature; upgrade before applying        │
│    Partial bundle = Bundle key partially active; some features of bundle blocked by FW prereq         │
│    License conflict = Two keys conflict on same feature; contact Dell TAC; do not apply more keys     │
│    Wrong array model = FoD key model-specific; a Unity key will not apply to a PowerStore             │
│    Already applied = Duplicate key import attempt; array shows duplicate; harmless but contact Dell   │
│    No entitlement = Support contract not linked to SN; contact Dell licensing team to link            │
│    Account link   = Link service tag to Dell support account via support.dell.com portal              │
│    MFA locked     = Too many failed MFA attempts; Dell support can unlock the portal account          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌───────────────────────────────────── Dell FoD — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       FoD troubleshooting: key rejection, feature not activating, portal access failures      │   │
│   │      Key rejection: SN mismatch, wrong key scope, corrupt file — re-download from portal      │   │
│   │    Feature not active: firmware prereq not met, bundle partially applied, license conflict    │   │
│   │       Portal issues: account MFA locked, key not in order history, account link missing       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom → check array event log → verify SN and FW → re-download if needed → Dell SR               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Key Issues         │  │        Feature Issues       │  │        Portal Issues        │   │
│   │       Rejection error       │  │        Not activating       │  │        Login failure        │   │
│   │         SN mismatch         │  │        FW prereq fail       │  │        Key not found        │   │
│   │         Wrong scope         │  │        Partial bundle       │  │        No entitlement       │   │
│   │         Corrupt file        │  │       License conflict      │  │         Account link        │   │
│   │       Already applied       │  │      Wrong array model      │  │          MFA locked         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Collect: array SN, event log error text, firmware version, and portal order screenshot             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │      Cause       │       Check       │       Fix        │   Escalate If    │   │
│   │   Key rejected   │   SN mismatch    │    Array GUI SN   │   Re-download    │  After 2 tries   │   │
│   │    Not active    │    FW prereq     │   Firmware ver.   │  Upgrade array   │   Dell TAC SR    │   │
│   │   Portal login   │    MFA locked    │    Dell account   │  Account reset   │   Dell support   │   │
│   │   Key missing    │  Wrong account   │   Order history   │  Link accounts   │  Dell licensing  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: confirm SN from chassis label; do not rely on documentation which may be outdated        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Rejection error = Array event log shows specific error code; note exact text for Dell TAC          │
│    SN mismatch    = Key file SN differs from array SN; most common FoD failure; re-download           │
│    Wrong scope    = Key unlocks different feature or tier than intended; verify before purchase       │
│    Corrupt file   = Download interrupted; browser saved incomplete .lic; re-download via HTTPS        │
│    FW prereq fail = Array firmware below minimum required for feature; upgrade before applying        │
│    Partial bundle = Bundle key partially active; some features of bundle blocked by FW prereq         │
│    License conflict = Two keys conflict on same feature; contact Dell TAC; do not apply more keys     │
│    Wrong array model = FoD key model-specific; a Unity key will not apply to a PowerStore             │
│    Already applied = Duplicate key import attempt; array shows duplicate; harmless but contact Dell   │
│    No entitlement = Support contract not linked to SN; contact Dell licensing team to link            │
│    Account link   = Link service tag to Dell support account via support.dell.com portal              │
│    MFA locked     = Too many failed MFA attempts; Dell support can unlock the portal account          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
