# Aria Operations — Integration


<div class="kb-summary">
Integration reference covering NSX Adapter, Active Directory / LDAP Authentication, SMTP (Alert Email), ServiceNow ITSM Integration, Webhook / Generic REST Actions and 2 more sections.
</div>

Aria Operations — Adapter and Outbound Integration Map
```text
┌─────────────────────────────────────────────────────┐
│  Data Sources (Inbound Adapters)                                                                      │
│                                                                                                       │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐                                                   │
│  │ vCenter  │  │  NSX-T   │  │  Storage           │                                                   │
│  │ Adapter  │  │ Adapter  │  │  (Pure, NetApp,    │                                                   │
│  │          │  │          │  │   vSAN built-in)   │                                                   │
│  │ read-only│  │ auditor  │  │                    │                                                   │
│  │ min. role│  │ role min.│  │                    │                                                   │
│  └────┬─────┘  └────┬─────┘  └─────────┬──────────┘                                                   │
│       └─────────────┴──────────────────┘                                                              │
│                          │                                                                            │
└──────────────────────────┼──────────────────────────┘
```
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
                           │ outbound notifications
          ┌────────────────┼──────────────────────┐
          ▼                ▼                      ▼
```text
┌──────────────┐  ┌──────────────┐  ┌────────────────┐
│  SMTP        │  │  ServiceNow  │  │  Webhook / REST                                                   │
│  (email      │  │  (ITSM       │  │  (Slack, Teams,                                                   │
│   alerts)    │  │   incidents) │  │   custom ITSM)                                                    │
└──────────────┘  └──────────────┘  └────────────────┘
```
          │
          ▼
```text
```
┌─────────────────────────────────────────────────────┐
│  Aria Ops for Logs (Log Insight Adapter)                                                              │
│  forwards alerts for log correlation                                                                  │
└─────────────────────────────────────────────────────┘
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

---

## Active Directory / LDAP Authentication

```text
Administration > Access Control > Authentication Sources > Add Source
```

| Field | Value |
|-------|-------|
| Type | Active Directory / OpenLDAP |
| Host | `ldap://dc01.domain.local` |
| Bind DN | `CN=aria-bind,OU=Service Accounts,DC=domain,DC=local` |
| Base DN | `DC=domain,DC=local` |
| User attribute | `sAMAccountName` |
| Group search | `OU=Groups,DC=domain,DC=local` |

After adding the source, map AD groups to Aria Operations roles in **Access Control > Roles**.

---

## SMTP (Alert Email)

```text
Administration > Outbound Settings > Add Plugin > SMTP
```

| Field | Value |
|-------|-------|
| SMTP Host | `smtp.domain.local` |
| Port | 25 or 587 (TLS) |
| Sender | `aria-ops@domain.local` |
| Auth | Optional (if relay requires it) |

Assign SMTP to notification rules: **Alerts > Notifications > Add Rule**

---

## ServiceNow ITSM Integration

Requires the **ServiceNow Notification Plugin** (available in the Aria Operations Marketplace or bundled).

```text
Administration > Outbound Settings > Add Plugin > ServiceNow
```

| Field | Value |
|-------|-------|
| ServiceNow URL | `https://<instance>.service-now.com` |
| Username | ITSM integration user |
| Table | `incident` |
| Assignment Group | As configured in ServiceNow |

Trigger: Add a notification rule targeting critical alerts → ServiceNow plugin action.

---

## Webhook / Generic REST Actions

For custom integrations (Slack, Teams, custom ITSM):

```text
Administration > Outbound Settings > Add Plugin > REST Notification Plugin
```

Configure endpoint URL, method (POST), and body template using Aria Operations alert tokens.

---

## Aria Operations for Logs (Alert Forwarding)

Forward Aria Operations alerts to Aria Operations for Logs for correlation:

```text
Administration > Solutions > Log Insight Adapter
```

Requires: Aria Operations for Logs FQDN, admin credentials.

---

## Related Sections

- [Security](../../security/index.md) — RBAC and authentication
- [Operations](../../operations/index.md) — adapter health monitoring
- [Troubleshooting](../../troubleshooting/index.md) — adapter collection errors
