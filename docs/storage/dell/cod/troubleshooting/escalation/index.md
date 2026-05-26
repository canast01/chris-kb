# COD — Escalation

```
┌──────────────────────────────────────── Dell CoD — Escalation ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CoD escalation: when self-service resolution fails, escalate to Dell licensing or TAC     │   │
│   │   Dell Licensing team: for key purchase issues, duplicate keys, SN re-binding, wrong account  │   │
│   │   Dell TAC: for capacity not appearing after valid key applied; firmware or hardware faults   │   │
│   │   Account team: for budget or contract issues affecting CoD entitlements or key availability  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Self-service fails → open SR with error detail → licensing or TAC → account team if contract       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Licensing Team       │  │           Dell TAC          │  │         Account Team        │   │
│   │         Key re-issue        │  │        Firmware issue       │  │       Contract dispute      │   │
│   │        SN re-binding        │  │        Hardware fault       │  │      Entitlement query      │   │
│   │        Account merge        │  │      Capacity conflict      │  │        Pricing review       │   │
│   │        Duplicate key        │  │       License conflict      │  │       Key pre-purchase      │   │
│   │        Order history        │  │       Event log review      │  │       Exec escalation       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Collect: array SN, key file, event log, firmware version, and licensing portal screenshots         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Issue Type    │   Escalate To    │    Info Needed    │       SLA        │     Contact      │   │
│   │   Key rejected   │  Dell Licensing  │   SN + key file   │    1 biz day     │ Licensing portal │   │
│   │   No capacity    │     Dell TAC     │    FW ver + log   │    4h P2 SLA     │ support.dell.com │   │
│   │  Contract issue  │   Account team   │    Contract ID    │    1 biz day     │     Dell rep     │   │
│   │  Exec escalate   │   Account exec   │     SR number     │     Same day     │   Account team   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: gather chassis label SN photo; compare to key file and portal record before calling      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Licensing team = Dell internal team managing CoD keys, SN binding, and licensing portal accounts   │
│    SN re-binding  = Dell process to re-issue a key for a replacement array serial number              │
│    Account merge  = Consolidating two Dell support accounts that each hold CoD keys for same site     │
│    Duplicate key  = Same key applied twice or purchased twice; licensing team resolves                │
│    Dell TAC       = Technical Assistance Center; handles firmware, hardware, and capacity issues      │
│    License conflict = Two active keys for same pool; TAC can resolve with Dell backend licensing      │
│    Event log      = Array management event log showing exact error text from key rejection            │
│    Contract ID    = Dell contract reference number; needed for entitlement and pricing disputes       │
│    P2 SLA         = Dell TAC 4-hour response for degraded production; CoD failure may qualify         │
│    Account exec   = Dell account executive; involved for contract disputes or exec escalations        │
│    Entitlement    = Right to activate CoD based on support contract; account team verifies            │
│    SR number      = Service Request number; track and share when calling Dell escalation contacts     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [COD](../../index.md) reference.

---

## Support Portal

Open a Dell support case at [https://www.dell.com/support](https://www.dell.com/support). For COD license issues, select the affected PowerMax array as the primary product and specify COD / licensing as the impacted component.

## Information to Collect

Before opening a case:

- Array SID: `symcfg list`
- Current license state: `symlicense -sid <SID> list`
- Full error from failed license install: `symlicense -sid <SID> install -file <file> 2>&1`
- License file (do not share publicly — attach securely to the case)
- Unisphere version and SCG connectivity status

## Escalation Path

1. Open a standard support case via Dell support portal
2. If the activation is time-critical (emergency capacity event), request **Priority 1** escalation and contact your Dell account team directly to expedite
3. For license file re-issuance issues (wrong SID), the Dell License Management team handles this separately from standard support — your account team can connect you directly
