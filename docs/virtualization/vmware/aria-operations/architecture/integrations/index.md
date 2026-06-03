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
