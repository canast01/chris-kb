---
tags:
  - dell
  - security
---
# APEX Storage as a Service — Hardening


<div class="kb-summary">
Hardening reference covering Hardening Checklist, Network Requirements Summary.
</div>

```text
┌──────────────────────────────── Dell Apex STaaS — Security Hardening ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Apex hardening: disable unused protocols, isolate storage VLAN, enforce TLS, audit      │   │
│   │     Network: storage traffic on dedicated VLAN; no routing between storage and user VLANs     │   │
│   │         Protocols: disable Telnet, NFS AUTH_SYS for sensitive data, unused iSCSI ports        │   │
│   │      Firmware: Dell manages array firmware; customer must not block SupportAssist access      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Baseline → disable unused protocols → network isolation → audit config → review quarterly          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Protocol          │  │           Network           │  │           Firmware          │   │
│   │        Disable Telnet       │  │         Storage VLAN        │  │         Dell managed        │   │
│   │       Enforce TLS 1.2+      │  │         No user VLAN        │  │          SCG allows         │   │
│   │        CHAP on iSCSI        │  │        iSCSI VLAN ACL       │  │         Auto patches        │   │
│   │        Limit NFS ver.       │  │        FC zone tight        │  │         CVE tracking        │   │
│   │         Disable HTTP        │  │         OOB separate        │  │        Audit firmware       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Dell firmware updates are automatic via SupportAssist; never block SCG egress to Dell              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Hardening     │      Action      │       Verify      │   Risk if skip   │      Notes       │   │
│   │   VLAN isolate   │  Dedicated VLAN  │   No cross-ping   │   Lateral move   │  ACL on switch   │   │
│   │       CHAP       │ Enable per host  │    CHAP active    │   Unauth iSCSI   │  Bidirectional   │   │
│   │   TLS enforce    │ Disable TLS<1.2  │    sslyze test    │   Weak cipher    │    Portal/API    │   │
│   │    FC zoning     │ Single init/tgt  │     show zone     │   Broad access   │  One zone/pair   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: switch VLAN ACLs · FC fabric binding + port security · iSCSI ACL on switches             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Storage VLAN   = Dedicated VLAN carrying only iSCSI or NFS; ACL blocks all other hosts             │
│    OOB separate   = Array management (iDRAC) on separate management VLAN; not in storage VLAN         │
│    FC zone tight  = One zone per initiator-target pair; not broad zones spanning all targets          │
│    TLS 1.2+       = Apex Console only accepts TLS 1.2 and 1.3; disable older cipher suites            │
│    Telnet         = Cleartext protocol; ensure disabled on all Apex Console endpoints                 │
│    HTTP disable   = Force HTTPS redirect on Apex Console; HTTP should return 301                      │
│    CVE tracking   = Dell publishes DSA (Dell Security Advisories); subscribe and track                │
│    SCG egress     = Allow outbound HTTPS from SCG VM to Dell cloud for SupportAssist                  │
│    Lateral move   = If storage VLAN is flat, compromise of one host risks all volumes                 │
│    iSCSI VLAN ACL = Switch ACL permitting only registered host IPs to reach array iSCSI ports         │
│    DSA            = Dell Security Advisory; CVE notifications for Dell product vulnerabilities        │
│    Audit config   = Monthly review of VLAN, zone, and CHAP settings for drift                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [APEX Storage as a Service](../../index.md) reference.

---

## Hardening Checklist

| Control | Standard | Action |
|---|---|---|
| **SCG software version** | Current GA release | Update the SCG appliance whenever Dell releases a new version. Outdated SCG versions may break telemetry delivery and SupportAssist connectivity, causing metering gaps that require manual correction. Check the SCG admin console for available updates at least monthly. |
| **SCG redundancy** | Two SCG appliances per site | Deploy two SCG appliances and register each monitored array to both. A single SCG is a metering and support single point of failure. Both appliances should be on separate physical hosts to survive a host-level failure. |
| **SCG network isolation** | Management VLAN only | Place SCG appliances on the storage management VLAN. Block access from general server VLANs. The SCG requires outbound HTTPS (443) to Dell cloud endpoints only — no inbound connections are required from external networks. |
| **SCG outbound allowlist** | Dell cloud endpoints only | Permit SCG outbound TCP 443 to `esrs.dell.com`, `cloudiq.dell.com`, and `api.dell.com` (or the regional equivalents listed in the SCG deployment guide). Deny all other outbound destinations at the perimeter firewall. |
| **API credential rotation** | Every 90 days | Rotate all APEX API client secrets on a 90-day cycle. Automate rotation where possible. Store credentials in a secrets vault — never in config files or version control. |
| **MFA enforcement** | Enforced for all human users | Enable MFA on all Dell account users with APEX Console access. This is configured under account identity settings and applies to all users in the tenancy. Emergency break-glass accounts are exempt but must be logged and reviewed monthly. |
| **IP allowlisting** | Corporate egress IPs only | Restrict APEX Console access to known corporate egress IP ranges or VPN exit nodes under account security settings. Review and prune stale CIDRs quarterly. |
| **Audit log review** | Monthly | Review the APEX Console audit log monthly for unexpected access, failed authentication attempts, unscheduled configuration changes, and unexpected SCG registration or deregistration events. |
| **SCG TLS validation** | Certificate pinning enabled | Do not deploy a TLS-inspecting proxy between the SCG and Dell cloud endpoints. Certificate pinning on the SCG will reject inspected connections, silently breaking telemetry delivery. Use a split-tunnel or allowlist exemption for SCG traffic. |
| **Named service accounts per integration** | One account per consuming system | Create a dedicated APEX API service account for each consuming system (monitoring tool, CMDB, automation pipeline). Assign the Viewer role unless write access is explicitly required. Never share credentials between integrations. |
| **Access review cadence** | Quarterly | Review all APEX Console user roles and service accounts on a quarterly basis. Revoke access for departed staff and contractors immediately; recertify remaining accounts annually at minimum. Document the review outcome in the CMDB. |
| **Platform-level encryption** | Enabled at deployment | Verify that Dell-managed encryption is enabled on all APEX storage pools. Confirm encryption status is visible in the APEX Console under the storage pool details view. Do not disable encryption for performance testing without a formal change record. |

## Network Requirements Summary

| Destination | Port | Direction | Purpose |
|---|---|---|---|
| `esrs.dell.com` | TCP 443 | Outbound from SCG | Secure Connect Gateway telemetry upload |
| `cloudiq.dell.com` | TCP 443 | Outbound from SCG | CloudIQ metric ingestion |
| `api.dell.com` | TCP 443 | Outbound from management hosts | APEX API access |
| Array management interface | TCP 443 / 8443 | SCG to array | Array registration and metric collection |
| SCG admin console | TCP 443 | Management hosts to SCG | SCG configuration and update management |

All other inbound connections to the SCG should be denied by default. SCG appliances do not require inbound access from the internet.
