# COD — Procedures

```
┌────────────────────────────────── Dell CoD — Operational Procedures ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ CoD procedures: capacity review, key purchase, key application, and post-expansion validation │   │
│   │    Capacity review: monthly CloudIQ review of used vs dark capacity; update growth forecast   │   │
│   │    Key purchase: raise CR, get approval, purchase from licensing portal, store key securely   │   │
│   │  Key application: apply key in array GUI or CLI within approved change window; verify result  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Capacity alert → CR raised → key purchased → key applied in window → verified → CMDB updated       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Capacity Review       │  │         Key Purchase        │  │       Key Application       │   │
│   │        CloudIQ review       │  │           Raise CR          │  │        Log into array       │   │
│   │      Dark cap remaining     │  │         Get approval        │  │       Import key file       │   │
│   │         Growth trend        │  │      Order from portal      │  │        Confirm unlock       │   │
│   │       Forecast trigger      │  │         Download key        │  │         Update CMDB         │   │
│   │         Update plan         │  │        Store in vault       │  │           Close CR          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key application is zero-downtime; hosts see expanded capacity within seconds of key apply          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Phase       │    Procedure     │        Tool       │      Owner       │     Duration     │   │
│   │      Review      │ Capacity report  │      CloudIQ      │   Storage ops    │      30 min      │   │
│   │     Purchase     │  Buy + download  │  Licensing portal │   Storage lead   │     1-5 days     │   │
│   │      Apply       │ Import key file  │   Array GUI/CLI   │   Storage eng.   │     < 5 min      │   │
│   │     Validate     │ Verify capacity  │     Array GUI     │   Storage eng.   │      10 min      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: apply key during business hours; downtime not required but have rollback plan ready      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CR             = Change Request in ITSM; required before any CoD key purchase or application       │
│    Approval       = Finance and storage lead sign-off on CoD key cost before purchase                 │
│    Import key file = Array management UI: Settings > License > Import; paste or upload key file       │
│    Confirm unlock = Check array pool view: dark capacity should now show as available                 │
│    CMDB update    = Record new licensed capacity per pool in the Configuration Management Database    │
│    Close CR       = Mark Change Request resolved after CMDB updated and capacity verified             │
│    Vault store    = Save key file to HashiCorp Vault or secure share immediately after download       │
│    Zero-downtime  = CoD key apply does not interrupt I/O; hosts continue without interruption         │
│    Growth trend   = Monthly CloudIQ capacity chart showing rate of consumption vs projection          │
│    Forecast trigger = Projected date when dark capacity exhausted; triggers pre-purchase action       │
│    Dark cap remaining = Current unactivated CoD capacity still available before next key needed       │
│    Lead time plan = Ensuring key is purchased and ready before capacity threshold is actually hit     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [COD](../../index.md) reference.

---

## COD Activation Procedure

1. Confirm the COD activation is required and the change ticket is approved
2. Log in to Unisphere and navigate to Settings > License > Capacity on Demand
3. Submit the activation request specifying the number of additional TB required
4. Monitor the activation status in Unisphere — expect propagation within 10-15 minutes
5. Validate the new capacity is visible via SYMCLI:
   ```bash
   symcfg -sid <sid> show -capacity -gb
   symlmf -sid <sid> list
   ```
6. Confirm the new capacity is available to the SRP and workloads are not impacted
7. Update the change ticket with the post-activation capacity figures

## Incident Triage

**On alert or issue:**
1. Log in to Unisphere or connect via SYMCLI to identify the exact utilization and licensing state
2. Check SYMCLI event log for any licensing-related errors: `symelog -sid <sid> list -type license`
3. Confirm the COD activation request was submitted via the correct channel (Unisphere > Settings > License > Activate Capacity)
4. If activation is rejected, verify the Dell account is current and the COD entitlement has not expired
5. Open a Dell support case if the activation cannot proceed through Unisphere

| Symptom | Likely Cause | Action |
|---|---|---|
| Unexpected capacity consumption spike | Workload growth or new provisioning without capacity planning | Run `symcfg -sid <sid> list -srp -detail`, identify which SRP/SG consumed capacity, review provisioning activity |
| COD activation rejected in Unisphere | Entitlement expired or account issue | Check license entitlement via `symlmf -sid <sid> list`, contact Dell account team |
| Licensing error in SYMCLI | Expired or invalid license file | Run `symlmf -sid <sid> list` to show license state, check expiry, open Dell support case |
| COD capacity not visible after activation | Activation not yet propagated | Wait up to 15 minutes, then re-run `symcfg -sid <sid> show -capacity -gb` |
| Unisphere cannot reach Dell licensing backend | Proxy or firewall blocking outbound HTTPS | Check SCG connectivity, verify proxy settings in Unisphere |
