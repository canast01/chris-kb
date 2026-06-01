# Nexus Dashboard — Integrations


<div class="kb-summary">
> Part of the [Nexus Dashboard](../../index.md) reference.
</div>

---

## Overview

Nexus Dashboard integrates with external identity providers, monitoring systems, Cisco cloud services, and third-party platforms. This page covers each integration, the configuration steps, and operational notes.

---

## 1. Active Directory / LDAP

Nexus Dashboard uses a centralized identity service (Keycloak) that supports LDAP, Active Directory, SAML 2.0, and local accounts.

### LDAP Configuration

Navigate to **Admin Console > Security > Authentication > Login Domains > Add**:

| Field | Value / Example |
|---|---|
| Domain name | `CORP-AD` |
| Type | Active Directory or OpenLDAP |
| Server | `ldap.corp.example.com` |
| Port | 636 (LDAPS) |
| Base DN | `DC=corp,DC=example,DC=com` |
| Bind DN | `CN=nd-svc,OU=Service Accounts,DC=corp,DC=example,DC=com` |
| Bind password | Service account password |
| User attribute | `sAMAccountName` |
| Group search base | `OU=ND-Groups,DC=corp,DC=example,DC=com` |
| Group attribute | `member` |

After saving, map AD groups to ND roles under **Security > Roles**:

| AD Group | ND Role |
|---|---|
| `GRP-ND-Admins` | Admin |
| `GRP-ND-Operators` | Operator |
| `GRP-ND-ReadOnly` | Viewer |
| `GRP-NDFC-SAN-Admins` | NDFC Network Admin (site-scoped) |

Test LDAP authentication from the login page using an AD credential before retiring local accounts.

---

## 2. TACACS+

Nexus Dashboard supports TACACS+ as an external authentication provider, which is common in Cisco environments using Cisco ISE.

Configure under **Admin Console > Security > Authentication > Login Domains > Add > TACACS+**:

| Field | Value |
|---|---|
| Server 1 | `10.10.1.10` |
| Server 2 | `10.10.1.11` |
| Port | 49 |
| Shared key | Stored in vault |
| Role mapping | Via TACACS+ AV-pair or default role |

TACACS+ role assignment can be done by:
- **AV-pair**: the TACACS+ server returns `cisco-av-pair=shell:nd-role=Admin` in the authorization response
- **Default role**: all TACACS+ users receive a configured default role (less granular, not recommended for production)

---

## 3. SAML 2.0 / SSO

Nexus Dashboard supports SAML 2.0 for single sign-on, integrating with identity providers such as Microsoft ADFS, Okta, or Ping Identity.

Configure under **Admin Console > Security > Authentication > Login Domains > Add > SAML**:

1. Download the ND SAML Service Provider metadata from the ND UI.
2. Import this metadata into your IdP as a new application.
3. Configure the IdP to return a `Role` attribute in the SAML assertion.
4. In ND, map IdP role attribute values to ND roles.
5. Set the login domain as the default or leave it as a secondary option alongside local accounts.

SAML SSO removes the need for users to maintain separate ND passwords. Users are redirected to the corporate IdP login page and returned to ND after successful authentication.

---

## 4. Cisco Intersight Integration

Nexus Dashboard can connect to Cisco Intersight (Cisco's cloud management platform) for:
- Centralized visibility across ND clusters and ACI fabrics
- Firmware advisory notifications
- NDFC fabric health surfaced in Intersight dashboards

Configure under **Admin Console > Infrastructure > Intersight > Connect**:

1. Generate a claim code from the ND UI.
2. Log into `intersight.com`, navigate to **Devices**, and claim the ND cluster using the code.
3. After claiming, the ND cluster appears in Intersight as a managed device.
4. Intersight can then pull health and inventory from the ND cluster.

Intersight connectivity requires outbound HTTPS (port 443) from the ND management network to `api.intersight.com`.

---

## 5. Email / SMTP Alerts

Configure email notification delivery under **Admin Console > System > Mail Configuration**:

| Field | Value |
|---|---|
| SMTP server | `smtp.corp.example.com` |
| Port | 587 (STARTTLS) or 25 |
| From address | `nexus-dashboard@corp.example.com` |
| Authentication | Username/password if relay requires auth |
| TLS | STARTTLS or SMTPS |

Alert rules and email recipients are configured per application (NDFC and NDI have their own alert notification settings). The SMTP relay setting is shared at the platform level.

---

## 6. Syslog Forwarding

Forward ND platform and application logs to a SIEM:

```bash
# SSH to any ND cluster node
ssh ndadmin@nd-node1.corp.example.com

# Configure syslog forwarding via ND CLI
acs system syslog add --server 10.10.3.50 --port 514 --protocol udp

# Verify
acs system syslog show
```
```
┌────────────────────────── Cisco Nexus Dashboard — Architecture Integrations ──────────────────────────┐
│                                                                                                       │
│  ND integrates with identity providers, SIEM, monitoring tools, and cloud platforms.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Identity Integrations             │  │           Monitoring Integrations           │   │
│   │            LDAP: user/group sync             │  │           Syslog: event forwarding          │   │
│   │               RADIUS: AAA auth               │  │            SNMP: trap generation            │   │
│   │         TACACS+: per-cmd accounting          │  │           Webhook: alert delivery           │   │
│   │            SAML 2.0: SSO with IdP            │  │           Email: SMTP notification          │   │
│   │          Cisco ISE: device posture           │  │           Splunk/SIEM: syslog TLS           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  IdP and AAA integrate at cluster level; monitoring integrations are per-app                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Cloud Integrations              │  │               Cisco Ecosystem               │   │
│   │         Intersight: infra management         │  │           APIC: ACI policy source           │   │
│   │          AWS/Azure: cloud site add           │  │          DCNM/NDFC: SAN/LAN fabric          │   │
│   │           VMware vCenter: VM aware           │  │          Tetration/Secure Workload          │   │
│   │         Terraform: infra-as-code API         │  │         ThousandEyes: WAN assurance         │   │
│   │         REST API: programmable mgmt          │  │          AppDynamics: app telemetry         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster · IdP/AAA server · SIEM · Intersight · cloud connectors · APIC cluster                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SAML 2.0       = Security Assertion Markup Language; federated SSO protocol                          │
│  Intersight     = Cisco cloud management SaaS for UCS and HCI infrastructure                          │
│  Tetration      = Cisco workload security analytics (now Secure Workload)                             │
│  ThousandEyes   = Cisco network intelligence platform for WAN path monitoring                         │
│  AppDynamics    = Cisco APM platform; correlates app and network performance                          │
│  ISE            = Identity Services Engine; network access policy and posture                         │
│  REST API       = Representational State Transfer API; ND primary programmability                     │
│  Terraform      = IaC tool; Cisco ND provider available for automation                                │
│  APIC           = Application Policy Infrastructure Controller; manages ACI fabric                    │
│  Webhook        = HTTP callback delivering alert payload to external systems                          │
│  Syslog TLS     = Encrypted syslog transport using TLS to SIEM                                        │
│  VM-aware       = ND correlates network paths with vCenter VM identifiers                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

### Key Platform API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | Authenticate and obtain token |
| GET | `/nexus/api/v1/sites` | List registered sites (fabrics) |
| GET | `/nexus/api/v1/nodes` | List cluster nodes and health |
| GET | `/nexus/api/v1/apps` | List installed applications |
| GET | `/nexus/api/v1/users` | List user accounts |
| POST | `/nexus/api/v1/backups` | Trigger a backup |
| GET | `/nexus/api/v1/backups` | List available backups |

NDFC API: accessible at `https://<nd-ip>/appcenter/cisco/ndfc/api/v1/`
NDI API: accessible at `https://<nd-ip>/appcenter/cisco/ndinsight/api/v1/`

Full API documentation (Swagger UI): `https://<nd-ip>/apidocs`

---

## 8. NDFC Integration with Cisco UCS (Compute)

NDFC can pull UCS server and HBA information from Cisco UCS Manager (UCSM) or UCS Central:

1. Navigate to **NDFC > Fabric > Settings > Compute**.
2. Add a UCS Manager instance:
   - UCSM IP / FQDN
   - Read-only service account credentials
3. After connection, NDFC correlates UCS server service profiles with fabric-connected HBA WWNs, enriching the End Device view with server identity information.

This integration is read-only; NDFC does not modify UCS configuration.

---

## 9. VMware vCenter Integration

NDFC integrates with VMware vCenter to correlate ESXi host HBA WWNs with VM and host names:

Navigate to **NDFC > Fabric > Settings > vCenter**:
- vCenter FQDN
- Port: 443
- Username: read-only vCenter service account
- Password

After connection, NDFC's End Device view displays ESXi hostnames and VM names alongside HBA WWNs. The integration is read-only from the NDFC side.

---

## 10. Multi-Site Connectivity (VPN / Dark Fibre)

When managing multiple data centre sites from a single ND cluster, sites connect to ND via:
- **Direct routed connectivity** (if sites share a routed network) — simplest option
- **VPN** — ND can be configured with IPsec connectivity between cluster and remote sites
- **Express Connect** (AWS deployments) — for cloud-connected remote sites

Configure site connectivity under **Admin Console > Infrastructure > Connectivity**. Each remote site's management network must be reachable from the ND data network (`data0` interface).
