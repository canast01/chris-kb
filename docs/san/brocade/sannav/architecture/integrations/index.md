# SANnav — Integrations


<div class="kb-summary">
> Part of the [SANnav](../../index.md) reference.
</div>

---

## Overview

SANnav integrates with external systems for authentication, alerting, monitoring, and host visibility. This page covers each integration, the configuration steps, and the operational implications.

---

## 1. Active Directory / LDAP

SANnav supports LDAP and LDAPS for user authentication and group-based role assignment. LDAP integration is configured under **Administration > Server Settings > LDAP**.

### Configuration

| Field | Value / Example |
|---|---|
| Server type | Active Directory or OpenLDAP |
| Server address | `ldap.corp.example.com` or IP |
| Port | 636 (LDAPS) — 389 only if LDAPS not available |
| Base DN | `DC=corp,DC=example,DC=com` |
| Bind DN | `CN=sannav-svc,OU=Service Accounts,DC=corp,DC=example,DC=com` |
| Bind password | Service account password |
| User search base | `OU=SAN-Users,DC=corp,DC=example,DC=com` |
| User search filter | `(sAMAccountName={0})` |
| Group search base | `OU=SAN-Groups,DC=corp,DC=example,DC=com` |
| Group member attribute | `member` |

### Role Mapping

Map LDAP groups to SANnav roles under **Administration > LDAP > Role Mapping**:

| AD Group | SANnav Role |
|---|---|
| `GRP-SANnav-Admins` | SAN Admin |
| `GRP-SANnav-Operators` | SAN Operator |
| `GRP-SANnav-ReadOnly` | SAN Viewer |

### Test the LDAP Connection

Navigate to **Administration > Server Settings > LDAP** and click **Test Connection**. SANnav will attempt a bind with the configured service account and return a success or error message. If the test fails, verify:
- DNS resolution of the LDAP server from SANnav
- LDAPS certificate trust (import the CA certificate if using self-signed)
- Service account bind permissions

---

## 2. SMTP / Email Alerts

SANnav sends alert notifications via email. Configure under **Administration > Server Settings > SMTP**:

| Field | Value |
|---|---|
| SMTP server | `smtp.corp.example.com` |
| Port | 587 (STARTTLS) or 25 |
| Authentication | Username/password (if relay requires auth) |
| From address | `sannav-alerts@corp.example.com` |
| TLS | Enabled (STARTTLS or SMTPS) |

Alert recipients and notification rules are configured separately under **Administration > Alert Policies**. Associate email recipients with policy rules to control which severity levels trigger emails.

---

## 3. SNMP Trap Forwarding

SANnav can forward SNMP traps to upstream NMS or SIEM platforms. Configure under **Administration > Alert Policies > Trap Forwarding**:

| Field | Value |
|---|---|
| Trap receiver IP | NMS / SIEM management IP |
| Port | 162/UDP |
| SNMP version | v2c or v3 |
| Community / credentials | Match NMS configuration |
| Trap filter | All events, or filter by severity |

SANnav forwards traps using its own Broadcom MIB definitions. Load the SANnav MIB files into the NMS to decode trap OIDs correctly. MIB files are downloadable from the SANnav UI under **Administration > Downloads**.

---

## 4. Syslog Integration

SANnav appliance OS logs and application event logs can be forwarded to a syslog server (SIEM). Configure syslog on the SANnav appliance CLI:

```bash
# SSH to SANnav appliance
ssh admin@sannav-mgmt.corp.example.com

# Edit rsyslog configuration
sudo vi /etc/rsyslog.d/sannav-forward.conf

# Add:
*.* @10.10.3.50:514        # UDP syslog
# or
*.* @@10.10.3.50:514       # TCP syslog (more reliable)

# Restart rsyslog
sudo systemctl restart rsyslog

# Verify forwarding
logger -t sannav-test "Test syslog message from SANnav"
# Check SIEM for the test message
```
┌──────────────────────────────────── Brocade SANnav — Integrations ────────────────────────────────────┐
│                                                                                                       │
│  SANnav integrates with SIEM, TACACS+, SNMP NMS, REST automation, and NTP/SMTP.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Identity & Auth Integrations         │  │           Monitoring Integrations           │   │
│   │           TACACS+: admin user auth           │  │          SNMP trap to NMS (HPE/IBM)         │   │
│   │          LDAP: group-based role map          │  │        syslog to SIEM (Splunk/QRadar)       │   │
│   │         RADIUS: fallback auth option         │  │         Email: SMTP alert forwarding        │   │
│   │            SSO: SAML 2.0 support             │  │           Webhook: REST event push          │   │
│   │        Local accounts: fallback only         │  │           Grafana: API data source          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Auth integrations centralise login; monitoring integrations feed SIEM and NMS.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Automation Integrations            │  │         Infrastructure Integrations         │   │
│   │           REST API: token + HTTPS            │  │          NTP: time sync for events          │   │
│   │          Ansible: SANnav collection          │  │         DNS: switch hostname resolve        │   │
│   │          Terraform: SANnav provider          │  │           NFS: backup destination           │   │
│   │           ServiceNow: CMDB CI sync           │  │           SCP: supportsave upload           │   │
│   │           Python requests library            │  │           vSphere: OVA VM hosting           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM on vSphere · management Ethernet · TACACS+/LDAP server · NFS backup share                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TACACS+         = Terminal Access Controller; centralised admin auth for SANnav GUI                  │
│  LDAP            = Lightweight Directory Access Protocol; AD group-to-role mapping                    │
│  SAML 2.0        = Security Assertion Markup Language; SSO federation for SANnav                      │
│  REST API        = SANnav northbound API; JSON/HTTPS; token-based authentication                      │
│  SNMP trap       = SANnav forwards MAPS/fabric events to NMS via SNMP v2c/v3                          │
│  Webhook         = HTTP POST to external system on SANnav event trigger                               │
│  Ansible collection= Broadcom-published Ansible modules for SANnav automation                         │
│  ServiceNow CMDB = CI records for fabric switches auto-synced from SANnav inventory                   │
│  NFS backup      = SANnav config/database backup to NFS share; scheduled daily                        │
│  NTP             = Network Time Protocol; critical for correlated event timestamps                    │
│  OVA             = Open Virtual Appliance; SANnav delivered as vSphere OVA template                   │
│  SCP             = Secure Copy; used for supportsave upload and firmware transfers                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Useful API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/rest/login` | Obtain session token |
| DELETE | `/rest/logout` | Invalidate session token |
| GET | `/rest/resourcegroups/all/switches` | List all managed switches |
| GET | `/rest/resourcegroups/all/fabrics` | List all fabrics |
| GET | `/rest/resourcegroups/{id}/events` | Get events for resource group |
| GET | `/rest/resourcegroups/all/ports` | List all ports with state |
| GET | `/rest/license` | License status |
| POST | `/rest/resourcegroups/all/switches/{switchId}/firmwareupgrade` | Trigger firmware upgrade |

API documentation (Swagger UI) is available at: `https://<sannav-ip>/rest/swagger-ui.html`

---

## 7. SANnav Global View Integration

If SANnav Global View is deployed, each Management Portal must be registered with Global View. Register under **Administration > Global View** in the Management Portal UI.

| Field | Value |
|---|---|
| Global View URL | `https://sannav-gv.corp.example.com` |
| Username | Global View admin account |
| Password | Admin password |

After registration, the portal sends health summaries and event data to Global View. The portal continues to operate independently if Global View connectivity is lost.
