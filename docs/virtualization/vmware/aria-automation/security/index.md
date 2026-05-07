# Aria Automation — Security
## RBAC Model

Aria Automation uses a **project-based access control** model. All resource provisioning is scoped to a project.

### Project-Level Roles

| Role | Permissions |
|---|---|
| **Owner** | Full control over the project — manage members, cloud zones, quotas, and all deployments |
| **Member** | Can request from catalog and manage own deployments within the project |
| **Viewer** | Read-only access to deployments and catalog items in the project |

### Organisation-Level Roles

| Role | Permissions |
|---|---|
| **Administrator** | Full platform access — all projects, all infrastructure, all administration |
| **Member** | Can access projects they are assigned to |

### Custom Roles

Custom roles with fine-grained permissions are managed through **Workspace ONE Access** (vIDM). Define custom role definitions in Workspace ONE Access and map them to Aria Automation projects.

---

## Secrets and Encrypted Properties

- Use **Encrypted Property Groups** for sensitive values (passwords, API tokens) in blueprints. Values are stored encrypted and are not exposed in deployment event logs.
- For enterprise-grade secrets management, integrate with **HashiCorp Vault** — Aria Automation retrieves secrets at deployment time via Vault's API. See [Integration](../integration/) for configuration steps.
- Avoid embedding plaintext secrets in Cloud Templates. Use property binding or Vault references.

---

## TLS Certificate Management

- Aria Automation ships with self-signed certificates — replace these with certificates signed by your internal or public CA before production use.
- Replace certificates via Aria Suite Lifecycle Manager (Locker) or via `vracli certificate import` on the appliance.
- Certificate renewals should be tracked in the LCM Locker and scheduled before expiry.

---

## API Token Rotation

- Aria Automation REST API access uses bearer tokens obtained from Workspace ONE Access.
- Service accounts used for API automation should have tokens with defined expiry.
- Rotate service account passwords on a schedule (quarterly minimum); update cloud account credentials in Aria Automation after rotation.

---

## Audit Logging

- All user actions (login, deployment create/delete, blueprint publish, admin changes) are recorded in the Aria Automation audit log.
- Access audit logs from the Aria Automation admin UI: **Administration > Audit Log**.
- Export audit logs for SIEM integration by querying the Aria Automation audit REST API endpoint.

---

## Hardening Checklist

- [ ] Replace self-signed TLS certificates with CA-signed certificates.
- [ ] Restrict Aria Automation management access to admin subnets (firewall rules).
- [ ] Remove or disable default/demo user accounts.
- [ ] Configure LDAP/AD integration via Workspace ONE Access — do not use local accounts for production.
- [ ] Apply least-privilege project roles — do not assign all users as Organisation Administrators.
- [ ] Use Encrypted Property Groups or Vault for all secrets in blueprints.
- [ ] Enable audit logging and forward to SIEM.
- [ ] Review and rotate integration service account passwords quarterly.
- [ ] Review cloud account and integration endpoint permissions — apply least-privilege.
- [ ] Apply Broadcom security advisories and patches within the defined patching window.
