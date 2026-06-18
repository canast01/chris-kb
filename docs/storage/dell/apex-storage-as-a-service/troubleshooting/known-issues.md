---
tags:
  - troubleshooting
  - apex
  - dell
  - known-issues
---
# Dell APEX Storage as a Service — Known Issues and Error Codes

<div class="kb-summary">
Dell APEX Storage is a Dell-managed STaaS offering. Hardware operational issues are handled by Dell directly. This page covers tenant-side issues such as portal access, data access, and connectivity requirements.

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


## Before you begin

- For hardware faults or array failures, contact **Dell APEX support** — Dell manages the hardware lifecycle.
- Tenant responsibilities: maintain TCP 443 outbound to `apex.dell.com` and `cloudiq.dell.com`, and manage data access credentials.

## Portal and Management

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| APEX portal shows `Array offline` | APEX | TCP 443 blocked from array management IP to apex.dell.com | Open outbound 443 from array management network; check `status.dell.com` for outage | N/A |
| `Order not visible` in APEX portal after purchase | APEX | Order provisioning takes 24–72 hours after contract execution | Wait 72 hours; contact Dell APEX support if still missing | N/A |

## Data Access

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Storage not accessible after APEX delivery | APEX | Host zoning or masking not configured by customer | Configure FC zoning or iSCSI connectivity per underlying array type | N/A |

## See also

- [Dell APEX — Common Issues](common-issues/)
- [Dell PowerStore — Known Issues](../../powerstore/troubleshooting/known-issues.md)
- [Dell CloudIQ — Known Issues](../../cloudiq/troubleshooting/known-issues.md)
