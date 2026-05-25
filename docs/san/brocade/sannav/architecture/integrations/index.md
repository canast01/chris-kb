# SANnav — Integrations

> Part of the [SANnav](../../index.md) reference.

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

---

## 5. VMware vCenter Integration

SANnav can connect to VMware vCenter to import ESXi host information, enabling correlation between host WWNs and VM names in the SANnav topology view.

Configure under **Administration > Third-Party Integrations > VMware vCenter**:

| Field | Value |
|---|---|
| vCenter FQDN | `vcenter.corp.example.com` |
| Port | 443 |
| Username | Read-only vCenter service account |
| Password | Service account password |

After successful connection, SANnav displays the ESXi hostname and VM names alongside the HBA WWN in the device inventory and topology view. This integration does not modify any vCenter configuration.

---

## 6. REST API

SANnav exposes a full REST API allowing external systems to query inventory, trigger operations, and receive event data.

### Authentication

```bash
# Obtain a bearer token (session token)
curl -sk -X POST https://sannav.corp.example.com/rest/login \
  -H "Content-Type: application/json" \
  -d '{"credentials":{"loginName":"admin","password":"<password>"}}'

# Response includes: { "authToken": "<token>" }

# Use the token in subsequent requests
curl -sk https://sannav.corp.example.com/rest/resourcegroups/all/switches \
  -H "Authorization: Bearer <token>" | python3 -m json.tool
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
