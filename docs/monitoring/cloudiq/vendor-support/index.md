# CloudIQ Vendor Support


<div class="kb-summary">
CloudIQ Vendor Support reference.
</div>

```
┌────────────────────────────────────── CloudIQ — Vendor Support ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Support Model — Dell Technologies GSS                             │   │
│   │          CloudIQ included with ProSupport or ProSupport Plus on eligible Dell arrays          │   │
│   │             Open case: support.dell.com — provide array serial + CloudIQ org name             │   │
│   │                Severity 1: production storage down + CloudIQ data gap > 1 hour                │   │
│   │             Telemetry issues: Dell GSS can view telemetry logs from cloud backend             │   │
│   │                 Feature requests: submit via cloudiq.dell.com > Feedback link                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Dell cloud hosted · support portal at support.dell.com · 24x7 for Sev-1                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ProSupport = Dell hardware support tier; required for CloudIQ inclusion                              │
│  ProSupport Plus = Premium support tier with predictive analytics and proactive support               │
│  GSS = Global Support Services; Dell tier-1 technical support organisation                            │
│  Array serial = Hardware identifier required for support case; found on array bezel or UI             │
│  CloudIQ org name = Organisation display name from cloudiq.dell.com account settings                  │
│  Telemetry log = Backend log of push attempts; Dell GSS can access internally                         │
│  Data gap = Period where CloudIQ received no telemetry; shown as gap in time-series                   │
│  Severity 1 = Critical support priority; 24x7 response; production impacted                           │
│  Feature request = Submitted via UI feedback; reviewed by CloudIQ product team                        │
│  Release notes = CloudIQ changelog; SaaS platform updated by Dell without customer action             │
│  MyService360 = Dell customer portal showing entitlements, cases, and assets                          │
│  ProSupport expiry = CloudIQ access may be affected if ProSupport lapses on array                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── CloudIQ — Vendor Support ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Support Model — Dell Technologies GSS                             │   │
│   │          CloudIQ included with ProSupport or ProSupport Plus on eligible Dell arrays          │   │
│   │             Open case: support.dell.com — provide array serial + CloudIQ org name             │   │
│   │                Severity 1: production storage down + CloudIQ data gap > 1 hour                │   │
│   │             Telemetry issues: Dell GSS can view telemetry logs from cloud backend             │   │
│   │                 Feature requests: submit via cloudiq.dell.com > Feedback link                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Dell cloud hosted · support portal at support.dell.com · 24x7 for Sev-1                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ProSupport = Dell hardware support tier; required for CloudIQ inclusion                              │
│  ProSupport Plus = Premium support tier with predictive analytics and proactive support               │
│  GSS = Global Support Services; Dell tier-1 technical support organisation                            │
│  Array serial = Hardware identifier required for support case; found on array bezel or UI             │
│  CloudIQ org name = Organisation display name from cloudiq.dell.com account settings                  │
│  Telemetry log = Backend log of push attempts; Dell GSS can access internally                         │
│  Data gap = Period where CloudIQ received no telemetry; shown as gap in time-series                   │
│  Severity 1 = Critical support priority; 24x7 response; production impacted                           │
│  Feature request = Submitted via UI feedback; reviewed by CloudIQ product team                        │
│  Release notes = CloudIQ changelog; SaaS platform updated by Dell without customer action             │
│  MyService360 = Dell customer portal showing entitlements, cases, and assets                          │
│  ProSupport expiry = CloudIQ access may be affected if ProSupport lapses on array                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Dell support is accessed via the Dell support portal. CloudIQ and SCG issues are raised as service requests (SRs) under the relevant platform contract. Diagnostic bundles from SCG can be collected from the SCG admin UI and attached to the SR.

**Information to collect before opening a case:**

- Platform type and serial number
- SCG version (from SCG admin UI)
- CloudIQ API client ID (if API-related)
- Error message or symptom description and timeline
- SCG diagnostic bundle

| Resource | Detail |
|---|---|
| Support portal | dell.com/support |
| SR creation | Via Dell support portal or CloudIQ dashboard |
| SCG diagnostic bundle | SCG admin UI > Support > Collect Diagnostics |
| ProSupport tiers | Basic, ProSupport, ProSupport Plus (check contract) |
