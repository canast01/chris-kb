# Aria Operations Integrations

```text
┌──────────────────────────────────── Aria Operations Integrations ─────────────────────────────────────┐
│                                                                                                       │
│  vCenter, NSX, vRLI, ITSM, and cloud endpoint integrations for Aria Operations.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           VMware Platform Sources            │  │            Log & Network Sources            │   │
│   │         vCenter: VMs/hosts/clusters          │  │            vRLI: log correlation            │   │
│   │            vSAN: storage metrics             │  │          NSX: overlay + DFW metrics         │   │
│   │           vRNI: network flow data            │  │             SD-WAN: edge metrics            │   │
│   │           LCM: product health feed           │  │          Horizon: VDI session data          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  VMware sources provide metrics; ITSM and cloud consume or extend vROps data.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             ITSM & Notification              │  │              Cloud Integrations             │   │
│   │          ServiceNow: alert webhook           │  │           AWS: EC2/RDS/ELB metrics          │   │
│   │           Slack/Teams: chat alert            │  │             Azure: VM + storage             │   │
│   │           Email: SMTP notification           │  │             GCP: Compute Engine             │   │
│   │           PagerDuty: on-call alert           │  │          Cloud: read-only IAM role          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster on vSphere; management packs per source; outbound HTTPS for cloud/ITSM                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Management Pack     = vROps plugin adding adapters, dashboards, alerts for a product                 │
│  vCenter Adapter     = Built-in; collects all vSphere metrics without extra pack                      │
│  vRLI Integration    = Log Insight alert events appear in vROps for correlation                       │
│  NSX Management Pack = Adds DFW rule, segment, edge gateway metrics to vROps                          │
│  vRNI Integration    = Network flow metrics pushed from vRNI to vROps via REST                        │
│  ServiceNow Webhook  = Outbound HTTP POST from vROps alert to ServiceNow intake                       │
│  PagerDuty           = On-call routing; vROps sends alert via REST or email                           │
│  Cloud Adapter       = vROps plugin collecting EC2/Azure/GCP metrics via cloud API                    │
│  IAM Role            = Read-only cloud role granting vROps access to cloud metrics                    │
│  LCM Integration     = LCM health events visible in vROps product health dashboard                    │
│  Horizon Pack        = Management pack for VMware Horizon VDI session and pool data                   │
│  Notification Rule   = vROps config routing alert to a specific outbound channel                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────┐  ┌──────────────┐  ┌────────────────┐
│  SMTP        │  │  ServiceNow  │  │  Webhook / REST                                                   │
│  (email      │  │  (ITSM       │  │  (Slack, Teams,                                                   │
│   alerts)    │  │   incidents) │  │   custom ITSM)                                                    │
└──────────────┘  └──────────────┘  └────────────────┘
```
```text
┌─────────────────────────────────────────────────────┐
│  Aria Ops for Logs (Log Insight Adapter)                                                              │
│  forwards alerts for log correlation                                                                  │
└─────────────────────────────────────────────────────┘
```

```powershell
┌──────────────────────────────────── Aria Operations Integrations ─────────────────────────────────────┐
│                                                                                                       │
│  vCenter, NSX, vRLI, ITSM, and cloud endpoint integrations for Aria Operations.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           VMware Platform Sources            │  │            Log & Network Sources            │   │
│   │         vCenter: VMs/hosts/clusters          │  │            vRLI: log correlation            │   │
│   │            vSAN: storage metrics             │  │          NSX: overlay + DFW metrics         │   │
│   │           vRNI: network flow data            │  │             SD-WAN: edge metrics            │   │
│   │           LCM: product health feed           │  │          Horizon: VDI session data          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  VMware sources provide metrics; ITSM and cloud consume or extend vROps data.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             ITSM & Notification              │  │              Cloud Integrations             │   │
│   │          ServiceNow: alert webhook           │  │           AWS: EC2/RDS/ELB metrics          │   │
│   │           Slack/Teams: chat alert            │  │             Azure: VM + storage             │   │
│   │           Email: SMTP notification           │  │             GCP: Compute Engine             │   │
│   │           PagerDuty: on-call alert           │  │          Cloud: read-only IAM role          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster on vSphere; management packs per source; outbound HTTPS for cloud/ITSM                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Management Pack     = vROps plugin adding adapters, dashboards, alerts for a product                 │
│  vCenter Adapter     = Built-in; collects all vSphere metrics without extra pack                      │
│  vRLI Integration    = Log Insight alert events appear in vROps for correlation                       │
│  NSX Management Pack = Adds DFW rule, segment, edge gateway metrics to vROps                          │
│  vRNI Integration    = Network flow metrics pushed from vRNI to vROps via REST                        │
│  ServiceNow Webhook  = Outbound HTTP POST from vROps alert to ServiceNow intake                       │
│  PagerDuty           = On-call routing; vROps sends alert via REST or email                           │
│  Cloud Adapter       = vROps plugin collecting EC2/Azure/GCP metrics via cloud API                    │
│  IAM Role            = Read-only cloud role granting vROps access to cloud metrics                    │
│  LCM Integration     = LCM health events visible in vROps product health dashboard                    │
│  Horizon Pack        = Management pack for VMware Horizon VDI session and pool data                   │
│  Notification Rule   = vROps config routing alert to a specific outbound channel                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
Administration > Access Control > Authentication Sources > Add Source
```
```text
Administration > Outbound Settings > Add Plugin > SMTP
```
```text
Administration > Outbound Settings > Add Plugin > ServiceNow
```
```text
Administration > Outbound Settings > Add Plugin > REST Notification Plugin
```
```text
Administration > Solutions > Log Insight Adapter
```

## Overview

Aria Operations ingests telemetry from VMware infrastructure and third-party platforms via management packs (adapters). Outbound integrations route alerts and reports to ITSM, notification, and log platforms.

## vCenter Integration

The vCenter adapter is the primary collection source and is configured during initial deployment.

```text
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
Separate plugins are recommended per team channel for targeted routing.
```

## Aria Logs Integration

Aria Logs (log analytics) integrates bidirectionally — Aria Operations can launch log search in context from an alert, and Aria Logs can trigger alerts back into Aria Operations.

Admin > Global Settings > Log Integration
- Enable Aria Logs integration
- Provide Aria Logs FQDN

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

Admin > Credentials > [Select Credential] > Edit
