# Aria Operations Integration
## Overview

Aria Operations ingests telemetry from VMware infrastructure and third-party platforms via management packs (adapters). Outbound integrations route alerts and reports to ITSM, notification, and log platforms.

## vCenter Integration

The vCenter adapter is the primary collection source and is configured during initial deployment.

```text
Admin > Solutions > VMware vCenter > Configure
- Hostname / IP: vCenter FQDN
- Credential: read-only svc-ariaops service account
- Collection interval: 5 minutes (default)
- Advanced: enable object tagging collection for custom group membership
```

Verify the adapter is in **Collecting** state. If it shows **No Data**, check the credential and network connectivity on port TCP 443.

## NSX Integration

The NSX management pack extends visibility to NSX-T overlays, logical routers, transport nodes, and edge clusters.

```text
Admin > Solutions > VMware NSX-T Adapter > Configure
- NSX Manager FQDN / IP
- Credential: read-only NSX service account
```

Key objects collected: Logical Routers, Transport Nodes, Edge Clusters, Tier-0/Tier-1 Gateways.

## vSAN Integration

vSAN monitoring is included in the vCenter adapter — enable vSAN collection in the adapter advanced settings. Metrics include disk group latency, resync throughput, capacity per datastore cluster, and component health.

## Storage Adapter Integrations

| Adapter | Configuration Location | Key Metrics |
|---|---|---|
| Pure Storage Management Pack | Admin > Solutions > Pure Storage | Array latency, IOPS, capacity per volume |
| Dell EMC MP (PowerStore/PowerMax) | Admin > Solutions > Dell EMC | Array health, LUN latency, capacity |
| NetApp MP | Admin > Solutions > NetApp | Volume latency, aggregate capacity |

All storage adapters require a service account on the array with read-only API access.

## ServiceNow Integration (Outbound Alerts)

Aria Operations can create ServiceNow incidents automatically via the outbound alert notification plugin.

```text
Admin > Alerts > Notification Plugins > Add ServiceNow Plugin
- ServiceNow instance URL
- Username / password (or OAuth token)
- Map alert severity to incident priority
- Assign to: storage / infra assignment group
```

Test the integration using the **Test Notification** button after saving.

## Slack / Teams Webhooks

```text
Admin > Alerts > Notification Plugins > Add Webhook Plugin
- Webhook URL: <Teams/Slack incoming webhook URL>
- Alert filter: severity = Critical or Immediate
- Payload template: include alert name, object, and description
```

Separate plugins are recommended per team channel for targeted routing.

## Aria Logs Integration

Aria Logs (log analytics) integrates bidirectionally — Aria Operations can launch log search in context from an alert, and Aria Logs can trigger alerts back into Aria Operations.

```text
Admin > Global Settings > Log Integration
- Enable Aria Logs integration
- Provide Aria Logs FQDN
```

## Third-Party Management Pack Summary

| Integration | Type | Purpose |
|---|---|---|
| vCenter Adapter | Inbound | VM, host, cluster, datastore metrics |
| NSX-T Management Pack | Inbound | Network overlay visibility |
| vSAN (via vCenter) | Inbound | vSAN capacity and performance |
| Pure Storage MP | Inbound | Array performance and capacity |
| Dell EMC MP | Inbound | Dell storage metrics |
| NetApp MP | Inbound | NetApp storage metrics |
| ServiceNow Plugin | Outbound | Alert-to-incident ticketing |
| Slack / Teams Webhook | Outbound | Critical alert notifications |
| Aria Logs | Bidirectional | Log correlation with performance data |

## Credential Management

All adapter credentials should use dedicated service accounts with read-only permissions. Store credentials in the team secrets manager, not in the Aria Operations credential store alone. Rotate adapter service account passwords on the standard 12-month schedule and update credentials under:

```text
Admin > Credentials > [Select Credential] > Edit
```
