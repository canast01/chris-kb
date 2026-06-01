# COD — Backup & Restore


<div class="kb-summary">
COD — Backup & Restore reference.
</div>

```
┌──────────────────────────────────── Dell CoD — Backup and Restore ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    CoD backup/restore: protect CoD key files and array configuration for recovery scenarios   │   │
│   │ Key backup: store CoD key files in secure vault and Dell licensing portal (re-download avail) │   │
│   │       Array config backup: export array config before and after each CoD key application      │   │
│   │     Restore: re-apply key from licensing portal if array is replaced or controller swapped    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Apply key → export array config → store key in vault → re-download from portal if lost             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Key Backup         │  │        Config Backup        │  │           Restore           │   │
│   │        Vault storage        │  │       Pre-apply export      │  │       Re-download key       │   │
│   │      Portal re-download     │  │      Post-apply export      │  │      Re-apply to array      │   │
│   │      Secure file share      │  │        SRE diff check       │  │       Controller swap       │   │
│   │      Key inventory doc      │  │        Change record        │  │        Array replace        │   │
│   │       Version tracking      │  │          CMDB entry         │  │       Verify capacity       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    CoD keys are tied to array serial number; key must be re-downloaded and re-applied on replacement  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │     Trigger      │        Tool       │      Owner       │    Retention     │   │
│   │    Key backup    │  After purchase  │   Vault + portal  │   Storage eng.   │    Permanent     │   │
│   │  Config export   │ Before/after key │     Array GUI     │   Storage eng.   │    1 year min    │   │
│   │ Key re-download  │  Array replace   │  Licensing portal │   Storage eng.   │    On-demand     │   │
│   │  Verify unlock   │  After restore   │     Array GUI     │   Storage eng.   │   Per restore    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: CoD key is a signed license file; store in HashiCorp Vault or equivalent secure store    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Key vault      = Secure secret store (HashiCorp Vault, CyberArk) holding CoD license files         │
│    Portal re-download = CoD keys always re-downloadable from Dell Licensing Portal by serial number   │
│    Pre-apply export = Array config backup taken before key application; baseline for comparison       │
│    Post-apply export = Array config after key applied; diff confirms expected capacity change         │
│    Controller swap = Replacing failed array controller; key must be re-applied after new controller   │
│    Array replace  = Entire array chassis swap (rare); new SN issued; new CoD key required             │
│    Key inventory  = Document tracking all purchased CoD keys per array: SN, capacity, applied date    │
│    SRE diff check = Comparing pre/post config exports to confirm only expected changes were made      │
│    CMDB entry     = Configuration Management Database updated with new licensed capacity post-apply   │
│    Version tracking = Key inventory tracks each key version as capacity is unlocked over time         │
│    Secure file share = Encrypted file store as secondary backup for key files alongside vault         │
│    Verify capacity = Post-restore check in array management that all expected pools are visible       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────── Dell CoD — Backup and Restore ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    CoD backup/restore: protect CoD key files and array configuration for recovery scenarios   │   │
│   │ Key backup: store CoD key files in secure vault and Dell licensing portal (re-download avail) │   │
│   │       Array config backup: export array config before and after each CoD key application      │   │
│   │     Restore: re-apply key from licensing portal if array is replaced or controller swapped    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Apply key → export array config → store key in vault → re-download from portal if lost             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Key Backup         │  │        Config Backup        │  │           Restore           │   │
│   │        Vault storage        │  │       Pre-apply export      │  │       Re-download key       │   │
│   │      Portal re-download     │  │      Post-apply export      │  │      Re-apply to array      │   │
│   │      Secure file share      │  │        SRE diff check       │  │       Controller swap       │   │
│   │      Key inventory doc      │  │        Change record        │  │        Array replace        │   │
│   │       Version tracking      │  │          CMDB entry         │  │       Verify capacity       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    CoD keys are tied to array serial number; key must be re-downloaded and re-applied on replacement  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │     Trigger      │        Tool       │      Owner       │    Retention     │   │
│   │    Key backup    │  After purchase  │   Vault + portal  │   Storage eng.   │    Permanent     │   │
│   │  Config export   │ Before/after key │     Array GUI     │   Storage eng.   │    1 year min    │   │
│   │ Key re-download  │  Array replace   │  Licensing portal │   Storage eng.   │    On-demand     │   │
│   │  Verify unlock   │  After restore   │     Array GUI     │   Storage eng.   │   Per restore    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: CoD key is a signed license file; store in HashiCorp Vault or equivalent secure store    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Key vault      = Secure secret store (HashiCorp Vault, CyberArk) holding CoD license files         │
│    Portal re-download = CoD keys always re-downloadable from Dell Licensing Portal by serial number   │
│    Pre-apply export = Array config backup taken before key application; baseline for comparison       │
│    Post-apply export = Array config after key applied; diff confirms expected capacity change         │
│    Controller swap = Replacing failed array controller; key must be re-applied after new controller   │
│    Array replace  = Entire array chassis swap (rare); new SN issued; new CoD key required             │
│    Key inventory  = Document tracking all purchased CoD keys per array: SN, capacity, applied date    │
│    SRE diff check = Comparing pre/post config exports to confirm only expected changes were made      │
│    CMDB entry     = Configuration Management Database updated with new licensed capacity post-apply   │
│    Version tracking = Key inventory tracks each key version as capacity is unlocked over time         │
│    Secure file share = Encrypted file store as secondary backup for key files alongside vault         │
│    Verify capacity = Post-restore check in array management that all expected pools are visible       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [COD](../../index.md) reference.

---

COD does not manage data backup directly. Key items to protect:

- **COD license files**: store downloaded license key files (`.xml`/`.dat`) in a secure, backed-up location — a secrets vault or a protected network share accessible only to storage admins. Lost license files require re-issuance from the Dell License Portal, which can cause delays during emergency activations.
- **COD inventory record**: maintain and back up the COD inventory tracking spreadsheet or CMDB records for each array including SID, activation dates, and headroom.
- **SYMCLI audit log exports**: periodically export `symaudit -sid <SID> list` output to a file and retain for compliance purposes.
