# FOD — Integrations

```
┌──────────────────────────────── Dell FoD — Architecture Integrations ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    FoD integrates with Dell Licensing Portal, array management systems, and ITSM workflows    │   │
│   │     Licensing Portal: purchase, download, and track FoD keys; tied to support account + SN    │   │
│   │     Array management: Unisphere, PowerStore Manager, or CLI applies key; feature activates    │   │
│   │       ITSM integration: FoD key application triggers CR; webhook closes CR on completion      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Purchase portal → download key → ITSM CR → apply via array GUI → CMDB updated → CR closed          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Licensing Portal      │  │       Array Management      │  │         ITSM / CMDB         │   │
│   │         Buy FoD key         │  │        PowerStore Mgr       │  │       CR pre-approval       │   │
│   │        Download .lic        │  │          Unisphere          │  │        Webhook close        │   │
│   │        Order history        │  │         Isilon/OneFS        │  │         CMDB update         │   │
│   │          SN binding         │  │          Array CLI          │  │         Audit trail         │   │
│   │       License history       │  │        Instant effect       │  │        Inventory doc        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    CloudIQ shows active FoD features per array in Health > Features view (select models)              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      System      │     Function     │      Protocol     │       Auth       │      Notes       │   │
│   │ Licensing portal │   Key purchase   │       HTTPS       │     Dell SSO     │licensing.dell.com│   │
│   │  PowerStore Mgr  │    Key apply     │     HTTPS REST    │    Local/LDAP    │    Per array     │   │
│   │       ITSM       │  Change control  │    API/webhook    │  Service token   │ Pre-approved CR  │   │
│   │       CMDB       │ Feature tracking │        API        │   Svc account    │Updated post-apply│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FoD key applied to array controller; no network path to licensing portal required        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Licensing portal = Dell portal for FoD key purchase, download, and history tracking                │
│    PowerStore Mgr = PowerStore Manager web UI; Settings > Licenses to import FoD key                  │
│    Unisphere      = Web UI for PowerMax and Unity; Administration > License to apply FoD key          │
│    Isilon / OneFS = PowerScale (formerly Isilon) uses OneFS CLI for FoD key application               │
│    Array CLI      = Fall-back method for FoD application if GUI is unavailable                        │
│    ITSM webhook   = ITSM auto-closes the CR when FoD application succeeds (optional integration)      │
│    Audit trail    = ITSM CR + array event log provide complete audit of feature activation            │
│    CMDB update    = After key apply, update CMDB record for the array with new feature list           │
│    Inventory doc  = Key inventory spreadsheet updated with feature, SN, date applied, applied by      │
│    SN binding     = Each FoD key is cryptographically bound to one array serial number                │
│    Order history  = All FoD purchases in licensing portal; re-download any key by order number        │
│    CR pre-approval = Standing change request for FoD activation; avoids delay in urgent situations    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Flex on Demand](../../index.md) reference.

---

| Integration | Notes |
|---|---|
| CloudIQ | Metering telemetry pipeline; capacity trends drive billing; SCG must stay connected |
| Secure Connect Gateway (SCG) | Forwards capacity telemetry from the array to CloudIQ; SCG outage causes telemetry gaps |
| Dell APEX Console | Billing and consumption reporting; committed baseline adjustments |
| Unisphere REST API | Capacity queries (`/system_capacity`, `/srp`) for burst monitoring |
| SYMCLI | Local capacity and license queries for PowerMax/VMAX arrays |
| Finance / chargeback tools | Automated monthly usage export via CloudIQ API for internal reporting |
