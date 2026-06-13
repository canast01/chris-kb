---
tags:
  - dell
  - security
---
# CloudIQ — Hardening


<div class="kb-summary">
Hardening reference covering Audit Log, Security Baseline.

*Applies to: CloudIQ*
</div>

```text
┌────────────────────────────────────── Dell CloudIQ — Hardening ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      CloudIQ hardening: harden the SCG VM, portal configuration, and network architecture     │   │
│   │   SCG hardening: disable SSH after initial config, update firmware, restrict management VLAN  │   │
│   │  Portal hardening: enforce MFA, set session timeout 30 min, IP allowlist, disable stale accts │   │
│   │      Network hardening: outbound-only from SCG, IDS on management segment, proxy logging      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Deploy SCG → harden VM → harden portal config → enforce network controls → monitor                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        SCG Hardening        │  │       Portal Hardening      │  │      Network Hardening      │   │
│   │         Disable SSH         │  │         Enforce MFA         │  │        Outbound-only        │   │
│   │        Mgmt VLAN only       │  │        Session 30 min       │  │       No inbound ports      │   │
│   │       Update firmware       │  │         IP allowlist        │  │        Proxy logging        │   │
│   │           TLS only          │  │     Disable stale accts     │  │        IDS on segment       │   │
│   │       Snapshot SCG VM       │  │       Audit log review      │  │      Alert on SCG down      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SCG on isolated management VLAN; allow only TCP 443 outbound to cloudiq.dell.com                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Control      │      Setting      │     Standard     │      Owner       │   │
│   │      SCG VM      │   Disable SSH    │After initial setup│      CIS L1      │    Infra team    │   │
│   │      Portal      │   Enforce MFA    │  Org-wide policy  │   NIST 800-63    │   Storage lead   │   │
│   │     Network      │  Outbound-only   │  443 egress only  │    Sec policy    │   Network team   │   │
│   │    Monitoring    │  Alert SCG down  │   CloudIQ + SIEM  │      SOC 2       │     Ops team     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SCG management VLAN isolated from production data VLANs and user workstations            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SSH disable    = After initial SCG configuration, disable SSH; use SCG web UI for management       │
│    Mgmt VLAN      = Dedicated VLAN for storage management IPs; SCG only on this VLAN                  │
│    Outbound-only  = SCG firewall rule: allow TCP 443 egress to cloudiq.dell.com; deny all inbound     │
│    Firmware update = Apply SCG firmware updates within 30 days of release via CloudIQ portal          │
│    IP allowlist   = Restrict CloudIQ portal login to corporate egress IPs; blocks home/VPN bypass     │
│    Session timeout = Portal auto-logout after 30 min idle; recommended for all environments           │
│    Stale account  = Accounts inactive 90 days auto-disabled; reviewed quarterly by storage lead       │
│    IDS on segment = Intrusion Detection System monitoring management VLAN for anomalous traffic       │
│    Proxy logging  = Log all SCG proxy traffic to detect data exfiltration or C2 activity              │
│    Snapshot SCG   = VM snapshot before SCG firmware updates; rollback if update fails                 │
│    CIS L1         = Center for Internet Security Level 1 baseline; applied to SCG VM OS               │
│    Alert SCG down = CloudIQ and SIEM alert when SCG telemetry stops; indicates connectivity loss      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [CloudIQ](../index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Audit Log

CloudIQ logs all user actions and API calls in a tamper-evident audit log. Access the audit log under **Admin > Audit Log** in the CloudIQ portal.

Audit events include:

- User logins and logouts (including source IP)
- Changes to notification rules, user roles, and API credentials
- API calls made by integration accounts
- System registration and deregistration events

The audit log can be filtered by date, user, and event type and exported as CSV for SIEM ingestion. Integrate with your SIEM (Splunk, Microsoft Sentinel, etc.) by periodically exporting the audit log via the CloudIQ API or by configuring a scheduled export.

Retain audit log exports for a minimum of 90 days in accordance with your organisation's security policy.

## Security Baseline

- Enforce MFA for all non-federated Dell accounts with CloudIQ access
- Configure SSO/federation via Azure AD or Okta where a corporate IdP is available
- Restrict CloudIQ Admin role to named individuals only
- Use a dedicated API service account per integration — do not share credentials between integrations
- Rotate API client secrets every 90 days and store in a secrets vault
- Review the audit log monthly for unexpected API access or configuration changes
