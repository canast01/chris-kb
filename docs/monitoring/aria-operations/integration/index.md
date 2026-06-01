# Aria Operations Integration

<div class="kb-summary">
Aria Operations Integration reference covering Overview, vCenter Integration, Slack / Teams Webhooks, Aria Logs Integration, Third-Party Management Pack Summary and 1 more sections.
</div>

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
```
┌─────────────────────────────────── Aria Operations — Integrations ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Core Platform Integrations                                  │   │
│   │            vCenter: primary data source — inventory, metrics, events, tags, alarms            │   │
│   │            NSX: network topology, logical switches, edges, DFW rules, and BGP state           │   │
│   │              vSAN: cluster health, capacity, performance, and disk group metrics              │   │
│   │              Aria Automation: request lifecycle, deployment state, and cost data              │   │
│   │               Aria Logs: log-based alerts forwarded to Aria Ops as notifications              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Adapters connect Aria Ops to external systems; each adapter has its own credential and schedule    │
│                                                                                                       │
│                                                  ▼                                                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Infrastructure Adapters            │  │             ITSM / Notification             │   │
│   │             Dell EMC: PowerStore             │  │            ServiceNow: CMDB sync            │   │
│   │           Pure Storage FlashArray            │  │              SMTP: email alerts             │   │
│   │             NetApp ONTAP adapter             │  │              SNMP trap outbound             │   │
│   │              Cisco UCS adapter               │  │             Slack/Teams webhook             │   │
│   │               AWS/Azure cloud                │  │              PagerDuty REST API             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Adapter processes run inside Aria Ops master node · outbound plugins use TCP 443/25/162              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Adapter = PAK-based plugin that collects data from a specific source (storage, cloud, network)       │
│  PAK file = Plugin/adapter package distributed by VMware or partner; installed via Solutions UI       │
│  Credential = Stored username/password or token used by adapter to authenticate to source             │
│  Collection interval = Frequency at which adapter queries source; typically 5 minutes                 │
│  Outbound plugin = Connector for sending alert notifications (SMTP, SNMP, REST, webhook)              │
│  CMDB sync = Pushing Aria Ops object inventory into ServiceNow CMDB via adapter                       │
│  Tag propagation = vSphere tags imported by vCenter adapter and applied to Aria Ops objects           │
│  Cloud account = AWS/Azure subscription registered in Aria Ops for cross-cloud visibility             │
│  REST adapter = Generic HTTP adapter for any REST API source not covered by a PAK                     │
│  Webhook = HTTP POST payload sent by outbound plugin when alert fires                                 │
│  SNMP trap = UDP notification sent to network management system on alert condition                    │
│  Alert notification = Outbound message triggered when alert changes state (firing or resolved)        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

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
