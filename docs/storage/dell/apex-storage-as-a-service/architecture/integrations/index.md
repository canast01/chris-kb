# APEX Storage as a Service — Integrations

> Part of the [APEX Storage as a Service](../../) reference.

---

| Integration | Notes |
|---|---|
| APEX Console | Primary management interface for subscriptions, billing, capacity requests, and support cases |
| APEX REST API | `https://api.dell.com` — programmatic access to systems, subscriptions, capacity, and metrics |
| CloudIQ | Health scoring and alerting for APEX systems; APEX systems appear in CloudIQ by underlying hardware model |
| Secure Connect Gateway (SCG) | Telemetry pipeline from on-premises hardware to CloudIQ and Dell support |
| Dell field service | Hardware replacement and capacity additions are Dell-managed via APEX Console service requests |

## Notes on APEX Management Boundaries

| Task | Interface |
|---|---|
| Order / provision new APEX system | APEX Console (console.dell.com) |
| Resize contracted capacity | APEX Console → Subscription → Modify |
| Create / delete volumes | APEX Console or APEX Block API |
| Monitor health and alerts | CloudIQ (console.dell.com/cloudiq) |
| View billing / consumption | APEX Console → Billing or Subscription API |
| Performance metrics | APEX Block API or CloudIQ API |
| Firmware upgrades | Dell-managed (SaaS — no customer action required) |
| Hardware replacement | Dell field service — no customer CLI |
