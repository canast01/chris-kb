---
tags:
  - troubleshooting
  - evergreen-one
  - pure-storage
  - known-issues
---
# Pure Storage Evergreen//One — Known Issues and Error Codes

<div class="kb-summary">
Evergreen//One is Pure Storage's STaaS offering — on-premises Pure hardware managed by Pure. Operational issues are handled by Pure support directly. This page covers tenant-side issues such as capacity overages and connectivity requirements.

*Applies to: Evergreen//One STaaS*
</div>

```text
┌───────────────────────────────────────── Pure Evergreen//ONE ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Evergreen//ONE: Storage as a Service subscription delivered on Pure FlashArray/FlashBlade   │   │
│   │                        Protocols: FC · iSCSI · NVMe-oF · NFS · SMB · S3                       │   │
│   │                              Management: Pure1 / Purity REST API                              │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Hardware          │  │         On-prem Pure        │  │          Pure-owned         │   │
│   │           Billing           │  │        Committed TiB        │  │         Monthly sub.        │   │
│   │           Refresh           │  │        Non-disruptive       │  │        Pure delivers        │   │
│   │          Management         │  │          Pure1 SaaS         │  │         AI analytics        │   │
│   │           Support           │  │        24x7 proactive       │  │          AI-driven          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │      Pure1       │   SaaS portal    │       HTTPS       │     SSO/SAML     │   AI analytics   │   │
│   │    FlashArray    │    Block/file    │    FC/iSCSI/NFS   │  CHAP/Kerberos   │     All-NVMe     │   │
│   │    FlashBlade    │   File/object    │     NFS/SMB/S3    │   Kerberos/IAM   │   Parallel I/O   │   │
│   │  ActiveCluster   │ Sync replication │    Internal RPC   │   Certificate    │     Zero RPO     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Pure FlashArray or FlashBlade on-prem (Pure-owned) · Pure1 cloud · WAN to Pure           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Evergreen//ONE     = Pure STaaS; Pure-owned hardware on customer premises with subscription billi  │
│    Pure1              = Pure Storage cloud management portal; AI-based analytics and capacity planni  │
│    Non-disruptive upgrade = hardware upgrade without host I/O interruption; Pure handles logistics    │
│    Committed TiB      = minimum subscribed capacity; billed monthly regardless of actual usage        │
│    Burst capacity     = additional capacity above commitment; no pre-ordering; billed as consumed     │
│    Hardware refresh   = Pure delivers and installs new controllers and shelves on 3-year cadence      │
│    Purity//FA         = FlashArray OS; unified block and file with NVMe-native architecture           │
│    Purity//FB         = FlashBlade OS; object and file storage with massive parallel throughput       │
│    AI copilot         = Pure1 AI feature; recommends workload placement and anomaly remediation       │
│    TaaS               = Technology as a Service; hardware ownership stays with Pure throughout subsc  │
│    ActiveCluster      = sync stretch replication included; ActiveDR async replication optional        │
│    SAML SSO           = Pure1 supports SAML 2.0; identity provider integrates with corporate IdP      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- For hardware faults or array operational issues, contact **Pure Storage support directly** — the array is Pure-managed under Evergreen//One.
- Tenant responsibilities: maintain network connectivity (TCP 443 to pure1.purestorage.com), manage data access credentials, and track consumed capacity vs. committed tier.

## Connectivity and Metering

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Pure reports `Array offline` for Evergreen//One array | Any | TCP 443 to pure1.purestorage.com blocked by tenant firewall | Open TCP 443 outbound from array management IP; Evergreen//One SLA requires continuous connectivity | N/A |
| Capacity overage notification despite low usage | Any | Thin provisioning and snapshot reserve counted toward consumed | Review effective capacity in Pure1 portal; contact Pure for tier adjustment | N/A |

## See also

- [Pure Storage FlashArray — Known Issues](../../flasharray/troubleshooting/known-issues/)
- [Pure Storage FlashBlade — Known Issues](../../flashblade/troubleshooting/known-issues/)
- [Pure1 — Known Issues](../../pure1/troubleshooting/known-issues/)
