# FOD — Backup & Restore

```
┌──────────────────────────────────── Dell FoD — Backup and Restore ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FoD backup: protect license key files and array configuration for restore scenarios      │   │
│   │      Key backup: store .lic files in vault; keys always re-downloadable from Dell portal      │   │
│   │       Config backup: export array license list before and after each FoD key application      │   │
│   │         Restore: re-apply key from portal if array replaced or controller swap occurs         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Apply key → export license config → store in vault → portal re-download available if needed        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Key Backup         │  │        Config Backup        │  │           Restore           │   │
│   │        Vault storage        │  │       Pre-apply export      │  │         Re-download         │   │
│   │         Portal re-DL        │  │      Post-apply export      │  │         Re-apply key        │   │
│   │       Encrypted share       │  │         Diff verify         │  │          Ctrl swap          │   │
│   │        Key inventory        │  │          CMDB entry         │  │        Array replace        │   │
│   │        Version track        │  │        Change record        │  │        Verify feature       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    FoD keys tied to array SN; controller swap on same chassis does not require new key                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │     Trigger      │        Tool       │      Owner       │    Retention     │   │
│   │    Key backup    │  After purchase  │   Vault + portal  │   Storage eng.   │    Permanent     │   │
│   │  Config export   │ Before/after key │     Array GUI     │   Storage eng.   │    1 year min    │   │
│   │    Key re-DL     │  Array replace   │  Licensing portal │   Storage eng.   │    On-demand     │   │
│   │  Verify feature  │  After restore   │     Array GUI     │   Storage eng.   │   Per restore    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: .lic files stored in HashiCorp Vault or CyberArk; do not store in plain-text repos       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Key vault      = Secure secret manager (HashiCorp Vault, CyberArk) for .lic file storage           │
│    Portal re-DL   = FoD keys always re-downloadable from Dell Licensing Portal by order/SN            │
│    Pre-apply export = Array license list snapshot before key; used as rollback reference              │
│    Post-apply export = Array license list after key; diff confirms expected feature activated         │
│    Diff verify    = Compare pre/post config exports; only new FoD feature should appear               │
│    Controller swap = Replacing failed controller in same chassis; SN unchanged; key still valid       │
│    Array replace  = Entire chassis replaced; new SN issued; request key re-issue from Dell            │
│    Key re-issue   = Dell Licensing team re-binds purchased FoD to new SN after array replace          │
│    Key inventory  = Master document tracking every FoD key: SN, feature, file name, vault path        │
│    Version track  = Each key application logged in inventory with version/date for audit trail        │
│    CMDB entry     = Configuration record updated with new active features post-apply                  │
│    Encrypted share = Secondary backup of .lic files on encrypted file server alongside vault          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [Flex on Demand](../../index.md) reference.

---

FOD does not manage data backup directly. Key items to protect:

- **FOD license files**: store downloaded license key files in a secure, backed-up location.
- **Monthly usage reports**: export and retain monthly consumption reports from the APEX Console for billing reconciliation and dispute resolution.
- **Contracted baseline documentation**: retain records of the contracted base and burst ceiling values, contract dates, and any baseline adjustment requests.
