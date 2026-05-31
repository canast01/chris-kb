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
## Fabric Integrations (via Hosted Applications)

| Application | Integration Target | Protocol | Purpose |
|---|---|---|---|
| NDFC (SAN mode) | Cisco MDS switches | SSH + SNMP v3 | Zoning, fabric discovery, health |
| NDFC (LAN mode) | NX-OS Nexus switches | SSH + SNMP v3 | VXLAN fabric provisioning, topology |
| NDI | ACI APIC / NX-OS | Telemetry streaming (gRPC) | Flow analysis, anomaly detection |
| NDO | ACI APIC (multi-site) | HTTPS REST | Policy orchestration across sites |

## Authentication Integrations

| Method | Use Case | Configuration Path |
|---|---|---|
| LDAP / Active Directory | User authentication | ND Admin → Authentication → Remote |
| TACACS+ | Network device AAA | NDFC → Admin → AAA |
| Local | Break-glass only | Local admin account; stored in CyberArk |

## Syslog and SNMP

| Integration | Direction | Configuration |
|---|---|---|
| Syslog (RFC 5424) | Outbound → SIEM | ND Admin → System Settings → Syslog |
| SNMP v3 trap receiver | Outbound → NMS | ND Admin → System Settings → SNMP |

## REST API

```bash
# Authenticate
curl -k -X POST https://nd.corp.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"userName":"admin","userPasswd":"<pass>","domain":"DefaultAuth"}'

# List fabric sites (NDFC)
curl -k -H "Cookie: AuthCookie=<token>" \
  https://nd.corp.example.com/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics

# List MDS switches managed by NDFC (SAN)
curl -k -H "Cookie: AuthCookie=<token>" \
  https://nd.corp.example.com/appcenter/cisco/ndfc/api/v1/san/fabrics
```
