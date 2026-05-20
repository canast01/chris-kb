# COD — Integrations

```
┌──────────────────────────────── Dell CoD — Architecture Integrations ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    CoD integrates with Dell Licensing Portal, array management, CloudIQ, and ITSM workflows   │   │
│   │ Licensing Portal: purchase and download CoD keys; linked to Dell support account and array SN │   │
│   │     Array management: Unisphere, PMAX GUI, or CLI applies key and activates dark capacity     │   │
│   │  CloudIQ integration: monitors used vs CoD capacity; alerts when threshold triggers next key  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Purchase key → download from portal → apply via array GUI or CLI → CloudIQ confirms unlock         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Licensing Portal      │  │       Array Management      │  │          Monitoring         │   │
│   │         Buy CoD key         │  │      Unisphere for PMax     │  │        CloudIQ alerts       │   │
│   │      Download key file      │  │           VMAX Mgr          │  │      Capacity forecast      │   │
│   │      Serial number tie      │  │       Unity Unisphere       │  │        SCG telemetry        │   │
│   │       License history       │  │       Array CLI apply       │  │         ITSM ticket         │   │
│   │         Account link        │  │        Instant effect       │  │         Email alert         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    ITSM integration: CoD key purchase triggers change request; applied in approved change window      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      System      │     Function     │      Protocol     │       Auth       │      Notes       │   │
│   │ Licensing portal │   Key purchase   │       HTTPS       │     Dell SSO     │licensing.dell.com│   │
│   │    Unisphere     │    Key apply     │     HTTPS REST    │    Local/LDAP    │ Per array model  │   │
│   │     CloudIQ      │  Usage monitor   │     HTTPS/SCG     │      OAuth2      │ Alerts ops team  │   │
│   │       ITSM       │  Change control  │    API/webhook    │  Service token   │ Pre-approved CR  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: CoD key is a signed file applied to array controller; hardware enforced at firmware      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Licensing portal = Dell online portal for purchasing, downloading, and tracking CoD license keys   │
│    SN tie         = Each CoD key is cryptographically bound to a specific array serial number         │
│    Unisphere      = Dell web-based management UI for PowerMax, VMAX, and Unity arrays                 │
│    Key apply      = Importing the CoD license file into array management software to unlock capacity  │
│    Instant effect = Capacity visible and usable within seconds; no array reboot required              │
│    CloudIQ alert  = Triggered at configurable threshold (e.g. 80%) of current CoD capacity            │
│    ITSM ticket    = Change request created before key purchase and application for audit trail        │
│    License history = Dell portal retains all purchased keys per serial; re-download if needed         │
│    SCG telemetry  = Used capacity metrics flow via SCG to CloudIQ for monitoring                      │
│    Pre-approved CR = Standing change request for CoD activation to avoid delay at capacity trigger    │
│    Account link   = Dell support account linked to licensing portal; required for key purchase        │
│    Webhook        = CloudIQ posts alert to ITSM webhook on threshold breach for auto-ticket creation  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [COD](../../) reference.

---

| Integration | Notes |
|---|---|
| Unisphere for PowerMax | Primary GUI for COD activation and license status; also exposes REST API for capacity queries |
| SYMCLI / Solutions Enabler | Command-line interface for license inspection, COD activation, and capacity discovery |
| Dell License Management Portal | Source of COD license key files; SID-tied entitlements managed here |
| CloudIQ | Provides capacity forecasting; shows active vs. total installed capacity and COD headroom |
| CMDB / change management | COD activations must be recorded as changes; CMDB updated after each activation |
