# Aria Operations Security

```text
┌───────────────────────────────────── Aria Operations — Security ──────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Authentication & Access            │  │               Network Security              │   │
│   │             Local admin account              │  │              HTTPS only TCP 443             │   │
│   │              vIDM SSO optional               │  │             Firewall: mgmt VLAN             │   │
│   │             LDAP/AD integration              │  │              No direct internet             │   │
│   │             RBAC: role → object              │  │             Cluster TCP 443/6061            │   │
│   │            Least-privilege roles             │  │              TLS 1.2+ enforced              │   │
│   │              Audit log in vROps              │  │             Cert replace via UI             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Hardening follows VMware STIG; custom cert replaces self-signed; credential vault for adapters     │
│                                                                                                       │
│                                                  ▼                                                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Credential Management             │  │                  Hardening                  │   │
│   │             Adapter credentials              │  │             VMware STIG applied             │   │
│   │               Stored encrypted               │  │           Disable SSH post-config           │   │
│   │               Rotate on breach               │  │              Root pw complexity             │   │
│   │               Service accounts               │  │                NTP configured               │   │
│   │             Minimum permissions              │  │                Syslog to SIEM               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Credentials stored encrypted in Aria Ops internal DB · audit log in /var/log/vmware/vcops            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vIDM = VMware Identity Manager; enables SAML SSO for Aria Ops UI login                               │
│  RBAC = Role-Based Access Control; permissions defined per role and scoped to object groups           │
│  Credential = Stored adapter username/password; encrypted at rest in Aria Ops DB                      │
│  Service account = Dedicated low-privilege vCenter user for Aria Ops adapter authentication           │
│  Read-only role = vCenter role with Browse Datastore and Read-Only granted; sufficient for adapter    │
│  STIG = Security Technical Implementation Guide; VMware-published hardening baseline                  │
│  Audit log = Record of user logins, role changes, and configuration modifications                     │
│  TLS 1.2 = Minimum TLS version enforced for all Aria Ops API and UI connections                       │
│  Custom cert = CA-signed certificate replacing self-signed; applied via Admin UI HTTPS settings       │
│  Cluster port 6061 = Internal Aria Ops cluster communication port; restricted to cluster subnet       │
│  Syslog forwarding = Shipping Aria Ops audit events to external SIEM (Splunk, Elastic)                │
│  SSH disable = SSH access to appliance disabled post-deployment except during maintenance             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Aria Operations uses vCenter SSO as the identity provider, allowing centralised user management and avoiding local account sprawl. RBAC is enforced through built-in roles: Admin, Content Admin, PowerUser, and ReadOnly — role assignments should follow least-privilege principles. All management access is HTTPS-only; HTTP is disabled. API tokens should be rotated on a defined schedule (minimum every 90 days). Node OS hardening follows the VMware STIG baseline. Admin actions are captured in the audit log accessible under Admin > Audit Log.

| Role | Capabilities |
|---|---|
| Admin | Full platform administration |
| Content Admin | Manage policies, dashboards, reports |
| PowerUser | Create and edit dashboards, views |
| ReadOnly | View dashboards and alerts only |

- vCenter SSO integration for authentication
- HTTPS-only access (port 443); HTTP redirected
- API token rotation policy: every 90 days
- Node OS hardening: VMware STIG baseline
- Audit log: Admin > Audit Log (retain 12 months minimum)
