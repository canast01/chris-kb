# Nexus Dashboard — Integrations

```bash
# List installed services on Nexus Dashboard
curl -sk -X GET \
  "https://nexus-dashboard.example.com/nexus/infra/api/v1/apps" \
  -H "Authorization: Bearer <token>" \
  | jq '.data[] | {name, version, status}'

# Trigger service installation from a local image
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v1/apps/install" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@nd-insights-4.2.1.tar.gz"
```

```text
┌─────────────────────────────────── Nexus Dashboard — Integrations ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Fabric Sources                │               Management Targets               │   │
│   │             ACI multi-site APIC              │           Cisco TAC Smart Call Home            │   │
│   │               NX-OS DCNM/NDFC                │            ServiceNow CMDB + events            │   │
│   │             HyperFlex Intersight             │           PagerDuty on-call routing            │   │
│   │                SD-WAN vManage                │             Splunk / Elastic SIEM              │   │
│   │             Kubernetes (ND Apps)             │              Webex Teams / Slack               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ND data network to fabrics · ND management to cloud SaaS targets · TCP 443 outbound                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Multi-site APIC = Multiple ACI fabrics each with their own APIC registered in ND                     │
│  Smart Call Home = Cisco TAC automatic support case from ND critical events                           │
│  CMDB = ServiceNow Configuration Management DB; ND updates CIs from fabric inventory                  │
│  HyperFlex = Cisco HCI; managed via Intersight; ND can pull cluster health                            │
│  SD-WAN vManage = Cisco SD-WAN controller; ND integration for WAN edge visibility                     │
│  ND Apps = NDI, NDFC, NDO run as Kubernetes apps inside ND cluster                                    │
│  Webex Teams = Cisco collaboration; NDI posts events to room via webhook                              │
│  Splunk / Elastic = SIEM platforms receiving ND syslog or HEC event streams                           │
│  PagerDuty = On-call routing; ND sends events via Events API v2                                       │
│  Cisco TAC = Technical Assistance Centre; Smart Call Home auto-opens cases                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
