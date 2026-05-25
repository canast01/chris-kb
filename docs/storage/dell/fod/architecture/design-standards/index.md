# FOD — Standards

```
┌────────────────────────────── Dell FoD — Architecture Design Standards ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    FoD design standards: key inventory, firmware prereqs, change control, and CMDB hygiene    │   │
│   │        Pre-apply standard: verify minimum firmware version before applying any FoD key        │   │
│   │    Inventory standard: all purchased FoD keys documented in key inventory with SN and date    │   │
│   │     Change control: all FoD key applications require approved CR; tested in non-prod first    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Plan feature need → verify prereqs → raise CR → purchase key → apply in window → update CMDB       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Key Standards        │  │      Firmware Standards     │  │      Process Standards      │   │
│   │        Vault storage        │  │     Min FW before apply     │  │         CR required         │   │
│   │      Key inventory doc      │  │     Compat matrix check     │  │        Non-prod test        │   │
│   │         SN tracking         │  │       DDOS / PMAS ver       │  │         CMDB update         │   │
│   │       Bundle awareness      │  │       Pre-upgrade plan      │  │       Quarterly audit       │   │
│   │      Portal re-download     │  │        Release notes        │  │        Naming scheme        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Naming: FoD keys stored as <ARRAYNAME>-<FEATURE>-<DATE>.lic in secure vault                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Standard     │   Requirement    │       Reason      │    Reference     │      Owner       │   │
│   │    Key vault     │  Store all keys  │   Recovery/audit  │    Sec policy    │   Storage lead   │   │
│   │    FW prereq     │Check before apply│   Avoid failure   │  Release notes   │   Storage eng.   │   │
│   │   CR required    │  ITSM CR raised  │   Change control  │   ITSM policy    │   Storage lead   │   │
│   │   CMDB update    │   After apply    │      Accuracy     │  CMDB standard   │     Ops team     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FoD modifies array firmware feature flags; no hardware change; instant and reversible    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Key inventory  = Spreadsheet or CMDB entry tracking all FoD keys: SN, feature, applied date        │
│    Vault storage  = FoD .lic files stored in HashiCorp Vault or encrypted file share                  │
│    Min FW         = Each FoD key requires minimum array firmware; check before applying key           │
│    Compat matrix  = Dell support matrix showing which FoD keys work with which firmware versions      │
│    PMAS           = PowerMax Array Software; Hypermax OS version on PowerMax arrays                   │
│    Non-prod test  = Apply FoD in test/dev array first; validate feature behavior before production    │
│    CR required    = Change Request; prevents unauthorized feature activation in production arrays     │
│    Bundle awareness = Some FoD keys activate multiple features; understand full scope before applying │
│    Portal re-download = All FoD keys re-downloadable from Dell Licensing Portal by SN and order       │
│    Quarterly audit = Review all FoD keys applied per array; confirm CMDB matches array license list   │
│    Naming scheme  = Consistent file name for FoD keys in vault; aids search and audit                 │
│    Release notes  = Dell FoD release notes list firmware prereqs and feature activation behavior      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Flex on Demand](../../index.md) reference.

---

## Upgrade Notes

| Step | Action |
|---|---|
| 1 | FOD billing is unaffected by firmware upgrades, but confirm CloudIQ telemetry resumes promptly after any maintenance that takes the array offline |
| 2 | After adding physical burst capacity under a FOD agreement, confirm CloudIQ reflects the new total installed capacity |
| 3 | If the array is migrated or replaced, work with Dell to transfer the FOD contract to the new system SID |

## Design Standards

- Monitor CloudIQ capacity trends weekly so burst events are visible before the end-of-month bill
- Deploy two SCG appliances for redundancy — a single SCG failure silently causes telemetry gaps that complicate billing disputes
- Automate monthly usage extraction via CloudIQ API and feed into a finance reporting system
- Set the committed baseline conservatively at contract start; adjust upward at renewal
- Review monthly metered usage report from CloudIQ or APEX Console and compare to contracted baseline
