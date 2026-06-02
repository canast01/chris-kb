# Cisco DCNM — Integrations


<div class="kb-summary">
> Part of the [Cisco DCNM](../../index.md) reference.
</div>

---

## Overview

DCNM integrates with external authentication, alerting, and monitoring systems. This page covers the configuration of each integration.

---

## 1. LDAP / Active Directory

DCNM supports LDAP and LDAPS for user authentication. Configure under **Administration > Security > Authentication > LDAP**.

| Parameter | Value |
|---|---|
| Server type | MS Active Directory or OpenLDAP |
| Server address | `ldap.corp.example.com` |
| Port | 636 (LDAPS) |
| Base DN | `DC=corp,DC=example,DC=com` |
| Bind DN | `CN=dcnm-svc,OU=Service Accounts,DC=corp,DC=example,DC=com` |
| Bind password | Service account password |
| User attribute | `sAMAccountName` |
| Group base | `OU=DCNM-Groups,DC=corp,DC=example,DC=com` |

**LDAP Group Role Mapping** — configure under **Administration > Security > Roles > LDAP Role Mapping**:

| AD Group | DCNM Role |
|---|---|
| `GRP-DCNM-Admins` | Admin |
| `GRP-DCNM-NetworkAdmin` | Network Admin |
| `GRP-DCNM-Operators` | Operator |
| `GRP-DCNM-ReadOnly` | Network Operator |

After saving, test by logging in with an AD user in one of the mapped groups.

---

## 2. SNMP Trap Forwarding

DCNM can forward SNMP traps to an NMS or SIEM. Configure under **Administration > Event Settings > SNMP Trap Forwarding**:

| Setting | Value |
|---|---|
| Trap receiver IP | `10.10.3.50` (NMS server) |
| Port | 162/UDP |
| SNMP version | v2c or v3 |
| Community / credentials | Match NMS configuration |
| Event filter | All, or filter by severity (WARNING and above recommended) |

DCNM uses its own CISCO-DCNM-MIB. Load the MIB files into your NMS to decode trap OIDs. MIBs are available at `https://software.cisco.com/download/home` under DCNM software.

---

## 3. Email Notifications

Configure under **Administration > Event Settings > Mail Setup**:

| Setting | Value |
|---|---|
| SMTP server | `smtp.corp.example.com` |
| Port | 25 or 587 |
| From | `dcnm-alerts@corp.example.com` |
| Auth | Username/password if relay requires auth |

Configure notification rules under **Administration > Event Settings > Notification Rules**:
- Severity: Critical, Warning, or All
- Destination: email address
- Scope: all fabrics or specific fabric

---

## 4. Syslog Integration

DCNM generates its own syslog from application events and can forward to a SIEM:

```bash
# On DCNM appliance
ssh root@dcnm-mgmt.corp.example.com

# Configure syslog forwarding (rsyslog)
cat >> /etc/rsyslog.d/dcnm-forward.conf << 'EOF'
# Forward DCNM application logs to SIEM
local0.* @10.10.3.50:514
*.err @@10.10.3.50:514
EOF

systemctl restart rsyslog
logger -p local0.info -t dcnm "Test message"
# Verify arrival at SIEM
```
```
┌────────────────────────────────────── Cisco DCNM — Integrations ──────────────────────────────────────┐
│                                                                                                       │
│  DCNM integrates with Cisco ISE, SIEM, REST automation, CMDB, and NTP/SMTP.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Identity & Auth Integrations         │  │           Monitoring Integrations           │   │
│   │          Cisco ISE: TACACS+/RADIUS           │  │       SNMP trap to NMS (CW/Solarwinds)      │   │
│   │          LDAP: AD group-to-role map          │  │          Syslog: SIEM Splunk/QRadar         │   │
│   │         RADIUS: fallback auth method         │  │             Email: SMTP alerting            │   │
│   │        Local accounts: emergency only        │  │           REST webhook: event push          │   │
│   │            SSO: SAML 2.0 via IdP             │  │          Grafana: REST data source          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  ISE provides centralised TACACS+; SIEM integrations forward all events for correlation.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Automation Integrations            │  │         Infrastructure Integrations         │   │
│   │           REST API: token + HTTPS            │  │        NTP: time sync for all events        │   │
│   │        Ansible: cisco.dcnm collection        │  │         DNS: switch name resolution         │   │
│   │           Terraform: DCNM provider           │  │          NFS: config backup target          │   │
│   │          ServiceNow: CMDB CI update          │  │         SCP: config archive transfer        │   │
│   │           Python requests library            │  │           vSphere: OVA VM platform          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM VM · management Ethernet · Cisco ISE appliance · NFS backup share                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cisco ISE       = Identity Services Engine; TACACS+ + RADIUS for Cisco devices                       │
│  TACACS+         = Terminal Access Controller; centralised CLI + GUI auth for DCNM                    │
│  LDAP            = Lightweight Directory Access Protocol; AD group to DCNM role map                   │
│  SAML 2.0        = Security Assertion Markup Language; SSO federation for DCNM GUI                    │
│  REST API        = DCNM northbound API; JSON/HTTPS with token authentication                          │
│  cisco.dcnm      = Ansible Galaxy collection; modules for DCNM automation                             │
│  Terraform       = HashiCorp IaC; DCNM provider for zone and VLAN provisioning                        │
│  ServiceNow CMDB = CI records for MDS switches auto-synced from DCNM inventory                        │
│  SNMP trap       = DCNM forwards MDS health events to NMS (CiscoWorks/SolarWinds)                     │
│  Syslog          = DCNM forwards audit and health events to SIEM for correlation                      │
│  NFS backup      = DCNM config/DB backup to NFS; scheduled nightly                                    │
│  NTP             = Network Time Protocol; required for correlated event timestamps                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Key API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/rest/logon` | Authenticate and get session |
| POST | `/rest/logout` | End session |
| GET | `/rest/inventory/switches` | List all switches |
| GET | `/rest/inventory/switches/{serialNumber}` | Switch detail |
| GET | `/rest/san/fabric` | List fabrics |
| GET | `/rest/san/vsan` | List VSANs |
| GET | `/rest/san/zoning` | Zoning information |
| POST | `/rest/san/zoning` | Create/modify zones |
| GET | `/rest/events/allevents` | Retrieve events |
| GET | `/rest/fm/image` | List firmware images |

API documentation: `https://dcnm.corp.example.com/api-docs`

---

## 6. vCenter Integration

DCNM can query VMware vCenter to correlate host WWNs with VM and host names:

1. Navigate to **Administration > VMware vCenter**.
2. Enter vCenter FQDN, port (443), username (read-only service account), and password.
3. Click **Test Connection**, then **Save**.

After connection, DCNM displays the ESXi hostname next to HBA WWNs in the End Devices view (**SAN > End Devices**), improving topology readability.

---

## 7. Nexus Dashboard Integration (DCNM 11.5+)

DCNM 11.5 introduced the ability to register with a Nexus Dashboard instance for federated visibility:

1. In DCNM: **Administration > Settings > Nexus Dashboard**.
2. Enter Nexus Dashboard cluster IP and admin credentials.
3. Click **Register**.

This allows DCNM fabric data to appear in Nexus Dashboard Insights dashboards. Full migration to NDFC is a separate process.
