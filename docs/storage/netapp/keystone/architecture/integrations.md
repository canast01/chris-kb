---
tags:
  - architecture
  - netapp
---
# Keystone — Integrations


<div class="kb-summary">
Integrations reference covering ActiveIQ Digital Advisor, Keystone Collector, REST API, ITSM Integration, CloudOps Integration.

*Applies to: Keystone STaaS*
</div>

```text
┌───────────────────────────── NetApp Keystone — Architecture Integrations ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Keystone integrations: Active IQ, BlueXP, Ansible ONTAP, ServiceNow, Prometheus        │   │
│   │         BlueXP: unified cloud manager; controls Keystone ordering and capacity changes        │   │
│   │          Ansible NetApp collection: automates SVM, volume, LUN provisioning on ONTAP          │   │
│   │          Prometheus exporter: exposes ONTAP perf metrics; Grafana dashboards for ops          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    ONTAP REST API <- Ansible/Terraform/BlueXP; ONTAP -> Prometheus -> Grafana -> alerts               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Cloud Integrations     │  │          Automation         │  │          Monitoring         │   │
│   │         Active IQ DA        │  │        Ansible netapp       │  │          Prometheus         │   │
│   │        BlueXP portal        │  │       Terraform ONTAP       │  │        Grafana boards       │   │
│   │         Keystone UI         │  │        REST API calls       │  │          SNMP traps         │   │
│   │         AutoSupport         │  │          ServiceNow         │  │          EMS alerts         │   │
│   │          SR portal          │  │          Python SDK         │  │        Syslog export        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    ONTAP REST API is the integration backbone; all modern tools use JSON/HTTPS                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Tool       │     Use Case     │      Protocol     │       Auth       │      Notes       │   │
│   │      BlueXP      │  Capacity order  │       HTTPS       │      OAuth2      │   NetApp cloud   │   │
│   │     Ansible      │   Provisioning   │     REST/ZAPI     │    Basic/cert    │    na_ontap_*    │   │
│   │    Prometheus    │   Perf metrics   │    HTTP scrape    │    None/token    │  ONTAP exporter  │   │
│   │    ServiceNow    │   ITSM tickets   │    REST webhook   │      OAuth       │   EMS -> SNOW    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Ansible controller VM · Prometheus server · Grafana in mgmt network                      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    BlueXP           = NetApp cloud manager; unified UI for on-prem and cloud storage                  │
│    Ansible na_ontap = NetApp Ansible collection; 200+ modules for ONTAP automation                    │
│    Terraform ONTAP  = NetApp provider for Terraform; declarative ONTAP provisioning                   │
│    Prometheus       = Time-series metrics DB; scrapes ONTAP exporter endpoint                         │
│    EMS              = Event Management System; ONTAP event log and alert engine                       │
│    SNMP trap        = UDP event notification; ONTAP -> monitoring system                              │
│    AutoSupport      = ONTAP built-in support telemetry; HTTPS to support.netapp.com                   │
│    ServiceNow       = ITSM platform; EMS webhooks create incident tickets                             │
│    Python SDK       = netapp-lib / ontap-rest-python; scripting ONTAP REST API                        │
│    Syslog           = ONTAP EMS forwarded to syslog server (Splunk, Graylog, etc.)                    │
│    OAuth2           = Token-based auth for BlueXP and modern REST API clients                         │
│    ZAPI             = Legacy XML-based ONTAP API; deprecated from ONTAP 9.13 onward                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
