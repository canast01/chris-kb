# FOD — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Escalation Path.
</div>

```
┌──────────────────────────────────────── Dell FoD — Escalation ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   FoD escalation: when self-service fails, escalate to Dell licensing, TAC, or account team   │   │
│   │    Dell licensing: key re-issue for array replacement, SN re-binding, duplicate resolution    │   │
│   │      Dell TAC: feature not activating after valid key; firmware issues; event log errors      │   │
│   │         Account team: contract/entitlement disputes; key not tied to support contract         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Self-service fails → collect diagnostics → open Dell SR → licensing or TAC → account team          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Licensing Team       │  │           Dell TAC          │  │         Account Team        │   │
│   │         Key re-issue        │  │       Feature inactive      │  │         Entitlement         │   │
│   │        SN re-binding        │  │         Firmware bug        │  │        Contract query       │   │
│   │        Duplicate key        │  │       License conflict      │  │           Pricing           │   │
│   │        Account merge        │  │       Event log error       │  │       Exec escalation       │   │
│   │        Order history        │  │        Bundle partial       │  │         Account link        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Collect before escalating: array SN, .lic file, event log, firmware version, order number          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Issue Type    │   Escalate To    │    Info Needed    │       SLA        │     Contact      │   │
│   │   Key rejected   │  Dell Licensing  │   SN + key file   │    1 biz day     │ Licensing portal │   │
│   │ Feature inactive │     Dell TAC     │   FW + event log  │    4h P2 SLA     │ support.dell.com │   │
│   │  Contract issue  │   Account team   │    Contract ID    │    1 biz day     │     Dell rep     │   │
│   │  Exec escalate   │   Account exec   │     SR number     │     Same day     │   Account team   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: collect chassis SN label photo; compare to portal before opening any escalation          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dell Licensing = Dell team managing FoD key purchase, SN binding, and re-issue processes           │
│    SN re-binding  = Re-issuing FoD key for a replacement array with new serial number                 │
│    Account merge  = Consolidating two Dell portal accounts that each hold keys for same array         │
│    Duplicate key  = Same key applied twice or purchased twice; licensing team resolves billing        │
│    Dell TAC       = Technical Assistance Center; handles firmware and feature activation issues       │
│    Bundle partial = Some features in a bundle not activating; TAC debugs feature flag state           │
│    License conflict = Two conflicting FoD features applied; TAC resolves with Dell backend            │
│    Event log      = Array event log showing exact error code and text from failed key import          │
│    Order number   = Dell purchase order number; required for licensing team to locate key history     │
│    P2 SLA         = 4-hour TAC response; FoD failure blocking production may qualify                  │
│    Account exec   = Dell account executive; involved for contract disputes or exec escalation         │
│    SR number      = Service Request tracking number; always reference when following up               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [Flex on Demand](../../index.md) reference.

---

## Support Portal

Open a Dell support case at [https://www.dell.com/support](https://www.dell.com/support). For FOD billing and metering issues, select the affected array as the primary product and specify Flex on Demand / APEX billing as the impacted component.

## Escalation Path

1. For billing discrepancies or metering disputes, contact your **Dell account team** first — these are often resolved without a formal support case
2. For technical issues (SCG connectivity, capacity not reflecting correctly), open a standard support case
3. For contract baseline adjustments, submit a request through the **APEX Console → Subscription → Modify** or via your account team
