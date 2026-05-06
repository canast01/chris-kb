# Aria Operations — Integration

## vCenter Adapter (Primary Integration)

The vCenter / SDDC adapter is the core integration and is added during initial setup.

**Service account requirements:**

| Permission | Minimum Role |
|-----------|-------------|
| Read inventory (hosts, VMs, clusters) | Read-Only |
| Execute remediation actions (VM power, resize) | Virtual Machine Power User |
| Full operations (recommended) | Administrator |

**Add or verify via UI:**

```
Administration > Solutions > vCenter Adapter
```

---

## NSX Adapter

Monitors NSX-T logical topology, transport nodes, and control plane health.

**Requirements:**
- NSX Manager FQDN/IP
- NSX service account with read-only Enterprise Admin or Auditor role

**Configure:**

```
Administration > Solutions > NSX-T Adapter > Add Instance
```

---

## Active Directory / LDAP Authentication

```
Administration > Access Control > Authentication Sources > Add Source
```

| Field | Value |
|-------|-------|
| Type | Active Directory / OpenLDAP |
| Host | `ldap://dc01.domain.local` |
| Bind DN | `CN=aria-bind,OU=Service Accounts,DC=domain,DC=local` |
| Base DN | `DC=domain,DC=local` |
| User attribute | `sAMAccountName` |
| Group search | `OU=Groups,DC=domain,DC=local` |

After adding the source, map AD groups to Aria Operations roles in **Access Control > Roles**.

---

## SMTP (Alert Email)

```
Administration > Outbound Settings > Add Plugin > SMTP
```

| Field | Value |
|-------|-------|
| SMTP Host | `smtp.domain.local` |
| Port | 25 or 587 (TLS) |
| Sender | `aria-ops@domain.local` |
| Auth | Optional (if relay requires it) |

Assign SMTP to notification rules: **Alerts > Notifications > Add Rule**

---

## ServiceNow ITSM Integration

Requires the **ServiceNow Notification Plugin** (available in the Aria Operations Marketplace or bundled).

```
Administration > Outbound Settings > Add Plugin > ServiceNow
```

| Field | Value |
|-------|-------|
| ServiceNow URL | `https://<instance>.service-now.com` |
| Username | ITSM integration user |
| Table | `incident` |
| Assignment Group | As configured in ServiceNow |

Trigger: Add a notification rule targeting critical alerts → ServiceNow plugin action.

---

## Webhook / Generic REST Actions

For custom integrations (Slack, Teams, custom ITSM):

```
Administration > Outbound Settings > Add Plugin > REST Notification Plugin
```

Configure endpoint URL, method (POST), and body template using Aria Operations alert tokens.

---

## Aria Operations for Logs (Alert Forwarding)

Forward Aria Operations alerts to Aria Operations for Logs for correlation:

```
Administration > Solutions > Log Insight Adapter
```

Requires: Aria Operations for Logs FQDN, admin credentials.

---

## Related Sections

- [Security](../security/) — RBAC and authentication
- [Operations](../operations/) — adapter health monitoring
- [Troubleshooting](../troubleshooting/) — adapter collection errors
