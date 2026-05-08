# FOD — Integrations

> Part of the [Flex on Demand](../../) reference.

---

| Integration | Notes |
|---|---|
| CloudIQ | Metering telemetry pipeline; capacity trends drive billing; SCG must stay connected |
| Secure Connect Gateway (SCG) | Forwards capacity telemetry from the array to CloudIQ; SCG outage causes telemetry gaps |
| Dell APEX Console | Billing and consumption reporting; committed baseline adjustments |
| Unisphere REST API | Capacity queries (`/system_capacity`, `/srp`) for burst monitoring |
| SYMCLI | Local capacity and license queries for PowerMax/VMAX arrays |
| Finance / chargeback tools | Automated monthly usage export via CloudIQ API for internal reporting |
