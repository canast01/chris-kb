# Nexus Dashboard — Integrations (Monitoring)

<div class="kb-summary">
Nexus Dashboard integrates with ACI APIC, NX-OS fabrics, and MDS SAN switches via its hosted applications (NDFC, NDI, NDO). External integrations cover LDAP, TACACS+, syslog, and the Nexus Dashboard REST API.
</div>

```text
┌───────────────────────────── Nexus Dashboard — Architecture Integrations ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Fabric Inputs                 │              Notification Outputs              │   │
│   │              ACI: APIC REST API              │                   Email SMTP                   │   │
│   │             NX-OS: MDT gRPC/SSH              │               ServiceNow webhook               │   │
│   │            Cisco Intersight (HX)             │               PagerDuty webhook                │   │
│   │            Crosswork Network Ctrl            │              Webex Teams webhook               │   │
│   │             Third-party RESTCONF             │                 Syslog to SIEM                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ND data network → fabrics · ND management → ITSM/email · gRPC TCP 9339 for MDT                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  APIC REST API = NDI polls APIC at TCP 443 for ACI fabric inventory and events                        │
│  MDT gRPC = NX-OS switches stream telemetry to ND data IP TCP 9339                                    │
│  SSH = NDFC uses SSH TCP 22 to NX-OS switches for config and inventory                                │
│  Intersight = Cisco cloud management; HyperFlex cluster data fed to ND                                │
│  Crosswork = Cisco network controller; can forward telemetry to ND                                    │
│  RESTCONF = Standard REST API on NX-OS; used for config and state queries                             │
│  ServiceNow = NDI events forwarded as incidents via REST webhook                                      │
│  PagerDuty = On-call routing for critical NDI fabric events                                           │
│  Webex Teams = Cisco collaboration; NDI events posted to space via webhook                            │
│  Syslog = NDI events forwarded to SIEM for security correlation                                       │
│  TCP 9339 = gRPC port for MDT streaming from NX-OS to ND                                              │
│  SMTP = Email notification for NDI events; configured in ND admin settings                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
