# Keystone — Integrations

> Part of the [Keystone Architecture](../index.md) reference.

---

## ActiveIQ Digital Advisor

BlueXP / ActiveIQ Digital Advisor is the primary portal for Keystone capacity visibility and subscription management. Log in at [https://activeiq.netapp.com](https://activeiq.netapp.com) using your NetApp SSO credentials. The Keystone dashboard displays:

- Committed vs. consumed capacity per service tier
- Burst usage and remaining burst headroom
- SLA compliance status (availability, latency, IOPS/TB)
- Monthly consumption trends and true-up projections

Access is provisioned by the Keystone Success Manager at subscription onboarding. Request additional user access via the KSM or the support portal.

## Keystone Collector

The Keystone Collector is a VM agent deployed on-premises that collects consumption data from ONTAP clusters and StorageGRID systems in the Keystone subscription.

- Runs as a Linux service (`keystone-collector`); requires outbound HTTPS on port 443 to `keystone.netapp.com`
- No inbound ports required — the Collector is outbound only
- Communicates with ONTAP via the cluster management LIF using ONTAP REST API
- Update the Collector when NetApp releases new versions to maintain telemetry continuity

Collector configuration is managed via a terminal UI (TUI) accessible on the Collector VM console.

## REST API

Keystone exposes a REST API for programmatic consumption reporting and subscription visibility. Use for custom dashboards, ServiceNow integration, or automated capacity reports.

```
# List subscriptions
GET /api/keystone/v1/subscriptions

# Get consumption for a specific subscription
GET /api/keystone/v1/subscriptions/{id}/consumption

# Get service level details
GET /api/keystone/v1/subscriptions/{id}/service-levels
```

Authenticate via ActiveIQ API tokens generated in the BlueXP portal. Tokens are scoped to the customer account and expire on a configurable schedule.

## ITSM Integration

Integrate Keystone consumption data with ServiceNow CMDB or similar ITSM platforms for:

- Asset and capacity records that reflect actual Keystone-managed hardware
- Monthly consumption report import for chargeback automation
- Alert generation from BlueXP webhooks to trigger ServiceNow incidents on capacity threshold breaches

Use the Keystone REST API to pull monthly consumption reports and push them to ServiceNow via its REST API or integration hub.

## CloudOps Integration

For hybrid cloud strategies, Keystone Flex extends the subscription model to Cloud Volumes ONTAP (CVO) instances in AWS, Azure, or GCP. A unified Keystone subscription can cover both on-premises Keystone STaaS and cloud CVO capacity under the same committed/burst billing model, with a single BlueXP dashboard view of total consumption across on-premises and cloud.
