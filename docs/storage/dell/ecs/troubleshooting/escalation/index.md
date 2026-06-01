# Dell ECS — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation Path.
</div>
```
┌──────────────────────────────────────── Dell ECS — Escalation ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        ECS escalation: severity triage, vendor support contact, and required artifacts        │   │
│   │         L1: basic checks, restart services; L2: log analysis, config review, vendor SR        │   │
│   │        Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours       │   │
│   │         Before escalating: collect support bundle, event timeline, and change history         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Detect issue → triage severity → collect artifacts → open SR → update                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Node            │  │        x86 appliance        │  │        Shared-nothing       │   │
│   │         Storage pool        │  │          Node group         │  │        Erasure coded        │   │
│   │             VDC             │  │          Virtual DC         │  │        Per-site unit        │   │
│   │          Rep. group         │  │          Multi-VDC          │  │        Geo redundancy       │   │
│   │            Bucket           │  │       Object container      │  │        S3/Swift/Blob        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Severity     │     Criteria     │   Response time   │      Owner       │    Vendor SLA    │   │
│   │        P1        │ Production down  │     Immediate     │   On-call + L2   │    1 hr 24x7     │   │
│   │        P2        │  Major degraded  │       1 hour      │   L2 engineer    │   4 hr biz hrs   │   │
│   │        P3        │  Minor degraded  │      4 hours      │   L2 engineer    │   8 hr biz hrs   │   │
│   │        P4        │    No impact     │    Next biz day   │    L1 support    │    2 biz days    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ECS appliance nodes · 10/25 GbE backend network · commodity SAS drives                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ECS                = Elastic Cloud Storage; Dell S3-compatible object store for unstructured data  │
│    VDC                = Virtual Data Center; group of ECS nodes at a single geographic site           │
│    Storage pool       = collection of nodes within a VDC; defines the erasure coding domain           │
│    Replication group  = links VDCs for geo-redundant object storage; 3-way replication                │
│    Bucket             = top-level S3 namespace; equivalent to S3 bucket or Azure container            │
│    Erasure coding     = data protection scheme; default 12+4 provides 4-drive fault tolerance         │
│    Namespace          = tenant-level isolation; multiple tenants share a single ECS cluster           │
│    CAS                = Content Addressed Storage; fixed-content object storage with WORM support     │
│    Replication factor = number of VDC copies; 3-way geo-replication for maximum durability            │
│    Atmos API          = legacy Dell Atmos-compatible API; supported for migration from Atmos systems  │
│    HDFS connector     = ECS Hadoop connector; ECS appears as HDFS namespace for analytics jobs        │
│    Quota              = per-namespace or per-bucket storage quota; enforced as hard or soft limit     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Support Portal

Dell EMC Support: [https://www.dell.com/support](https://www.dell.com/support)

- Log in with your MyDell account linked to your support contract
- Navigate to **Cases** to open a new case or view existing cases
- Navigate to **Contracts & Warranties** to verify ECS support entitlement

## Opening a Case

1. Confirm the ECS system is registered under your support contract in the Dell Support portal
2. Collect the information listed below before opening the case
3. Go to [https://www.dell.com/support](https://www.dell.com/support) → **Contact Support** → **Create Service Request**
4. Select product: **Dell EMC ECS** (Enterprise Content Storage)
5. Set severity:
   - **Severity 1** — production cluster down or data inaccessible
   - **Severity 2** — degraded cluster (nodes down, replication stopped) but data accessible
   - **Severity 3** — non-critical functional issue or question
   - **Severity 4** — general enquiry or low-impact issue
6. Attach the support bundle (ECS Portal → Support → Collect Logs) to the case immediately
7. Note the case number and communicate it to the on-call team

## Information to Collect

```bash
# ECS software version
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/version" | python3 -m json.tool

# Node list and health status
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/nodes" | python3 -m json.tool

# Active alerts
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/alerts" | python3 -m json.tool

# VDC capacity
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/capacity" | python3 -m json.tool

# Replication group status (geo deployments)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/data-service/vpools" | python3 -m json.tool

# Namespace and bucket affected by the issue
ecscli namespace list
ecscli bucket get --namespace <namespace> --name <bucket>
```

Also provide:
- ECS Portal → Support → Collect Logs (per-node support bundle — mandatory for Severity 1/2 cases)
- VDC topology diagram (number of sites, nodes per VDC, replication group configuration)
- Approximate time the issue started
- Description of any recent changes (upgrades, replication group changes, network/firewall changes, new bucket or namespace creation)
- Error messages from the ECS Portal and from the S3/API client side

## SLA Tiers

| Severity | Description | Initial Response Target | Update Frequency |
|---|---|---|---|
| Severity 1 | Production cluster down / data inaccessible | 30 minutes | Every 2 hours until resolved |
| Severity 2 | Degraded cluster / significant impact | 2 hours | Every 4 hours |
| Severity 3 | Non-critical issue / minor impact | Next business day | As updated |
| Severity 4 | General question / low impact | 2 business days | As updated |

Response times are governed by your specific Dell support contract tier (Basic, ProSupport, ProSupport Plus, or Mission Critical). Verify your entitlement in the Support portal before assuming the above defaults.

## Escalation Path

1. **Case update**: Add a comment to the open case requesting escalation if progress is insufficient
2. **Account Team**: Contact your Dell account manager or technical account manager (TAM) to escalate a Sev1/Sev2 case that is not progressing
3. **Mission Critical escalation**: If you have a ProSupport Mission Critical contract, call the dedicated Mission Critical support line for immediate engineer engagement
4. **Executive escalation**: If the account team is unresponsive, request escalation through your Dell sales representative to Dell EMC Services management
