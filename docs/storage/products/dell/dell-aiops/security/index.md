---
tags:
  - dell
  - security
description: "Dell AIOps Security reference covering Access Control (RBAC), SSO Integration, Audit Logging, Data Sovereignty, Network Security and 1 more sections."
---
# Dell AIOps Security

<div class="kb-summary">
Dell AIOps Security reference covering Access Control (RBAC), SSO Integration, Audit Logging, Data Sovereignty, Network Security and 1 more sections.

*Applies to: Dell AIOps*
</div>

```d2
direction: down

external: External / Untrusted {shape: rectangle}
access_control_rbac: "Access Control (RBAC)" {shape: rectangle}
sso_integration: "SSO Integration" {shape: rectangle}
data_sovereignty: "Data Sovereignty" {shape: rectangle}
network_security: "Network Security" {shape: rectangle}
security_hardening_checklist: "Security Hardening Checklist" {shape: rectangle}
core: "Dell AIOps Core" {shape: hexagon}

external -> access_control_rbac: traffic in
access_control_rbac -> sso_integration
sso_integration -> data_sovereignty
data_sovereignty -> network_security
network_security -> security_hardening_checklist
security_hardening_checklist -> core: secured path
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Access Control (RBAC)

Dell AIOps access control inherits from CloudIQ RBAC. Roles are assigned per user in the CloudIQ portal.

| Role | Capabilities |
|---|---|
| Admin | Full access: recommendations, configuration, notification rules, user management, API client management |
| Viewer | Read-only access to recommendations, anomalies, health data, and capacity trends |

User management: **CloudIQ portal > Settings > User Management**

Apply the principle of least privilege. Operations staff reviewing dashboards and recommendations should be Viewers. Admins should be limited to designated platform administrators.

## SSO Integration

Dell AIOps authentication is handled through CloudIQ SSO, which supports SAML 2.0 integration with enterprise IdPs.

Key events to review in audit log:
- User login/logout (especially failed logins or logins from unexpected locations)
- API client creation, modification, and secret rotation
- Notification rule changes
- Recommendation acknowledgement and dismissal

**Retention**: Export audit logs monthly to SIEM for long-term retention beyond CloudIQ's on-platform retention window.

## Data Sovereignty

AIOps telemetry is processed entirely in Dell's cloud infrastructure.

| Consideration | Detail |
|---|---|
| Data type | Storage performance metrics, capacity data, hardware health — not customer data or PII |
| Processing location | Dell cloud (confirm EU region for GDPR compliance if required) |
| Retention in Dell cloud | Per Dell's data retention policy — review Dell's privacy documentation |
| Local SCG buffer | SCG stores a short-term telemetry buffer on disk — ensure SCG VM disk is on an encrypted datastore |

## Network Security

| Control | Implementation |
|---|---|
| SCG egress | TCP 443 outbound only to Dell cloud endpoints; no inbound rules required |
| SCG management UI access | Restrict to ops management subnet via firewall rule (TCP 9443) |
| Array credentials on SCG | Use dedicated read-only service accounts per array; store in SCG credential store |

## Security Hardening Checklist

- [ ] SSO enabled; local accounts disabled for non-break-glass users
- [ ] Admin role limited to designated platform administrators
- [ ] API clients scoped to minimum required permissions
- [ ] API secrets stored in secrets manager; not in scripts or repos
- [ ] API secret rotation on 90-day schedule; rotation dates tracked
- [ ] SCG management UI access restricted to ops subnet
- [ ] SCG VM disk on encrypted datastore
- [ ] NTP configured on SCG (prevents certificate validation failures)
- [ ] Audit log exported to SIEM monthly
- [ ] Annual review of user accounts — remove stale accounts
