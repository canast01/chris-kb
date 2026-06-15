---
tags:
  - apex
  - dell
  - storage-as-a-service
  - networking
  - firewall
  - ports
---
# Dell APEX Storage as a Service — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell APEX Storage as a Service (STaaS). APEX Storage deploys Dell hardware on-premises managed through Dell's cloud portal. The underlying storage protocols are identical to the array type deployed (PowerStore, PowerFlex, etc.).

*Applies to: Dell APEX Block Storage / File Storage / Object Storage*
</div>

```text
┌─────────────────────────────────────────── Dell Apex STaaS ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     Apex STaaS: cloud-managed on-prem storage subscription                    │   │
│   │                               Protocols: iSCSI · FC · NFS · SMB                               │   │
│   │                                    Management: Apex Console                                   │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Owner            │   │
│   │           Hardware          │  │       NVMe/SAS arrays       │  │             Dell            │   │
│   │          Management         │  │         Apex Console        │  │           Customer          │   │
│   │          Monitoring         │  │         CloudIQ/SCG         │  │            Shared           │   │
│   │           Billing           │  │       Committed+burst       │  │         Dell billing        │   │
│   │           Network           │  │        iSCSI VLAN/FC        │  │           Customer          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Function     │      Protocol     │       Auth       │      Notes       │   │
│   │      Arrays      │  Block/File/NFS  │    iSCSI/FC/NFS   │  CHAP/Kerberos   │     On-prem      │   │
│   │   Apex Console   │  Provision/bill  │     HTTPS REST    │     SAML SSO     │   SaaS portal    │   │
│   │       SCG        │ Telemetry relay  │       HTTPS       │   Certificate    │     Local VM     │   │
│   │     CloudIQ      │ AIOps analytics  │       HTTPS       │      OAuth2      │       SaaS       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell array hardware on-premises · customer iSCSI VLAN / FC fabric · Apex Console SaaS    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Apex STaaS         = on-prem Dell storage consumed as a cloud service with subscription billing    │
│    Apex Console       = cloud portal; provision volumes, view usage, and raise support requests       │
│    Committed base     = minimum contracted capacity tier; billed monthly regardless of actual use     │
│    Burst capacity     = pre-installed unlocked storage above committed; billed when consumed          │
│    SCG                = Secure Connect Gateway; relays array telemetry to CloudIQ for analysis        │
│    CloudIQ            = Dell AIOps SaaS; health scores, capacity forecasts, firmware advisories       │
│    NVMe tier          = all-flash performance tier; sub-millisecond latency for database workloads    │
│    Capacity tier      = SAS/NL-SAS lower cost tier; suited to bulk storage and backup targets         │
│    iSCSI CHAP         = Challenge Handshake Auth Protocol; authenticates iSCSI initiators to array    │
│    FC port sec.       = FC fabric binding and port security; restricts which HBAs can log in          │
│    vVols              = Virtual Volumes; per-VM storage objects exposed via VASA provider to vCenter  │
│    OOB mgmt           = out-of-band management network for direct array controller access             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## APEX Cloud Management (Outbound — Required)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | APEX array management IP | apex.dell.com, cloudiq.dell.com, esrs.dell.com | APEX portal connectivity, CloudIQ telemetry, ESRS support, automated updates |

## Data Access Protocols (Same as Underlying Array)

APEX Storage uses the same data access ports as the underlying array type:

| Array Type | Relevant Ports Page |
|---|---|
| APEX Block Storage (PowerStore-based) | [Dell PowerStore — Ports](../../powerstore/architecture/ports/) |
| APEX Block Storage (PowerFlex-based) | iSCSI 3260, NVMe-oF 4420 |
| APEX File Storage (PowerScale-based) | [Dell PowerScale — Ports](../../powerscale/architecture/ports/) |
| APEX Object Storage (ECS-based) | [Dell ECS — Ports](../../ecs/architecture/ports/) |

## Admin Access to APEX Portal (SaaS)

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | apex.dell.com | Admin browser access to APEX order management and monitoring |

## Firewall Summary

| From | To | Ports | Notes |
|---|---|---|---|
| APEX array mgmt IP | apex.dell.com, cloudiq.dell.com | 443 | Required for APEX management — must be open |
| Data protocol hosts | APEX array data IPs | Varies by type | Same as underlying array ports |

## See also

- [Dell APEX — Architecture](how-it-works/)
- [Dell CloudIQ — Ports](../../cloudiq/architecture/ports/)
- [Dell PowerStore — Ports](../../powerstore/architecture/ports/)
