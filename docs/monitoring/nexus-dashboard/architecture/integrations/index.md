# Nexus Dashboard — Integrations (Monitoring)

<div class="kb-summary">
Nexus Dashboard integrates with ACI APIC, NX-OS fabrics, and MDS SAN switches via its hosted applications (NDFC, NDI, NDO). External integrations cover LDAP, TACACS+, syslog, and the Nexus Dashboard REST API.
</div>

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
```
