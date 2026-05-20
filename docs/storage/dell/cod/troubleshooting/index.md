# COD — Troubleshooting


```
┌───────────────────────────────────── Dell CoD — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ CoD troubleshooting: key application failures, capacity not appearing, licensing portal issues│   │
│   │    Key failure: invalid key, wrong serial, expired — verify SN and re-download from portal    │   │
│   │     Capacity not visible: key applied but pool not expanded — check firmware compatibility    │   │
│   │     Portal issues: login failures, key not found — verify support account and entitlements    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom identified → verify key SN match → re-download if needed → escalate to Dell if stuck       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Key Issues         │  │       Capacity Issues       │  │        Portal Issues        │   │
│   │      Invalid key error      │  │      Pool not expanded      │  │        Login failure        │   │
│   │         Wrong serial        │  │       Firmware compat       │  │        Key not found        │   │
│   │         Expired key         │  │        Partial unlock       │  │        No entitlement       │   │
│   │       File corruption       │  │      Capacity mismatch      │  │         Account link        │   │
│   │        Duplicate key        │  │       License conflict      │  │        Browser issue        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    First step: verify array serial number matches the SN in the CoD key file exactly                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │      Cause       │       Check       │       Fix        │   Escalate If    │   │
│   │   Invalid key    │     Wrong SN     │   SN in key file  │   Re-download    │  After 2 tries   │   │
│   │   No expansion   │   Firmware old   │   Firmware ver.   │  Upgrade array   │   Dell TAC SR    │   │
│   │   Portal login   │  Account issue   │   Support acct.   │  Account reset   │   Dell support   │   │
│   │  Key not found   │  Wrong account   │   Order history   │    Link accts    │  Dell licensing  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: verify array SN on chassis label or via array GUI before contacting Dell support         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Invalid key error = Array rejects key file; usually SN mismatch or corrupted download              │
│    SN mismatch    = CoD key file is bound to a different array serial number than the target          │
│    Expired key    = Rare; CoD keys typically do not expire but check key file metadata                │
│    File corruption = Download interrupted; re-download from portal; verify checksum if provided       │
│    Firmware compat = CoD key requires minimum array firmware version; check release notes             │
│    Partial unlock = Only some pools unlocked; check key scope matches intended pools                  │
│    Capacity mismatch = Unlocked capacity differs from purchased amount; raise SR with Dell            │
│    License conflict = Two keys for same pool applied; array shows conflict; contact Dell licensing    │
│    No entitlement = Dell support account not linked to the service tag; contact Dell licensing team   │
│    Account link   = Link service tag to Dell support account via support.dell.com portal              │
│    Order history  = Check purchase history in licensing portal to locate previously bought keys       │
│    Dell licensing = Dell licensing team reachable via support portal or account team for key issues   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
