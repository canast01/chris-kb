# VCF — Access Control

```
VCF RBAC Model — Role Assignment Flow
┌─────────────────────────────────────────────────────┐
│  Active Directory                                   │
│  ┌──────────────────────────────────────────────┐   │
│  │  GG-VCF-Admins · GG-VCF-Operators · ...     │    │
│  └──────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────┘
                        │ AD groups mapped to roles
          ┌─────────────┼──────────────┐
          ▼             ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
│ SDDC Manager │ │ NSX Manager  │ │ vCenter Server    │
│              │ │              │ │ (per domain)      │
│ ADMIN        │ │ Enterprise   │ │ Administrator     │
│ OPERATOR     │ │   Admin      │ │ ReadOnly          │
│ VIEWER       │ │ Network Eng  │ │ CloudAdmin (VVF)  │
│              │ │ Security Eng │ │                   │
│              │ │ Auditor      │ │ Apply at lowest   │
│              │ │              │ │ inventory level   │
└──────────────┘ └──────────────┘ └──────────────────┘

Credential Rotation (all via SDDC Manager — never manually):
┌─────────────────────────────────────────────────────┐
│  SDDC Manager → Security → Credentials → Rotate     │
│  ESXi root · vCenter SSO admin · NSX admin          │
│  SDDC Manager admin · vSAN iSCSI accounts           │
│  Schedule: every 90 days (or per policy)            │
└─────────────────────────────────────────────────────┘
```

> Part of the [VMware Cloud Foundation](../../) reference.

---

## SDDC Manager Roles

| Role | Access |
|---|---|
| ADMIN | Full access — lifecycle, security, credential rotation |
| OPERATOR | Day-to-day operations — health, tasks, monitoring; no credential access |
| VIEWER | Read-only dashboards and health views |

**Assign roles to AD groups:**

1. SDDC Manager → Administration → Single Sign-On → add Active Directory identity source
2. Administration → Users and Groups → assign roles to AD groups
3. Remove direct user-level assignments — group-based assignment is auditable and survives staff changes

---

## NSX Manager Roles

| Role | Capabilities | Typical Assignees |
|---|---|---|
| **Enterprise Admin** | Full NSX configuration — logical switching, routing, micro-segmentation, load balancing, gateway firewall, certificate management, user management | Network architects, NSX platform owners |
| **Network Engineer** | Configure and manage logical switches, routers, and load balancers; cannot modify security policy or manage users | Network operations team |
| **Security Engineer** | Create and modify distributed firewall rules, security groups, and gateway firewall policies; cannot modify network topology | Security team, firewall engineers |
| **Auditor** | Read-only access to all NSX configuration and logs; cannot make any changes | Compliance, audit staff, monitoring service accounts |

NSX roles are assigned in NSX Manager under **System → User Management → Roles**. In a VCF environment, NSX Manager user management should be configured to use the same AD identity source as SDDC Manager to ensure consistent group-based access.

---

## vCenter Server Roles in VCF Context

In a VCF-managed deployment, vCenter permissions are managed through SDDC Manager rather than directly in the vCenter UI. This ensures that VCF lifecycle operations retain the permissions they require.

| Principle | Detail |
|---|---|
| **VCF service account** | SDDC Manager creates and manages a service account in each vCenter. Do not modify or disable this account — VCF lifecycle tasks (upgrades, expansions) depend on it. |
| **Human user access** | Grant human users access to vCenter via AD group membership in vCenter → Administration → Global Permissions. Use built-in roles (Administrator, Read-Only, Virtual Machine User) or custom roles with least privilege. |
| **Role scope** | Apply roles at the lowest inventory level possible (VM folder, cluster, or datacenter object) rather than at the global level. Global permissions propagate to all vCenter objects and should be reserved for platform admins. |
| **No local vCenter accounts** | In a VCF environment, disable local vCenter accounts (other than the built-in `administrator@vsphere.local` break-glass account). All access should flow through the AD identity source. |

---

## API Service Account Guidance

SDDC Manager exposes a REST API used by automation pipelines, CMDB integrations, and monitoring tools.

| Use Case | Recommended Role | Authentication Method |
|---|---|---|
| Read-only monitoring (health, inventory queries) | VIEWER | API token (Bearer) — generate under My Account in SDDC Manager |
| Automation pipelines (deploy workload domains, expand clusters) | OPERATOR or ADMIN depending on operations required | API token with short expiry; rotate on each pipeline run via CI/CD secrets manager |
| CMDB or asset discovery | VIEWER | Long-lived API token stored in secrets vault; rotate every 90 days |

**Obtaining an API token:**

```bash
# Authenticate and retrieve a session token
curl -sk -X POST https://<sddc-manager-fqdn>/v1/tokens \
  -H "Content-Type: application/json" \
  -d '{"username":"svc-automation@vsphere.local","password":"<password>"}' \
  | jq -r '.accessToken'
```

Use the returned `accessToken` as a Bearer token in subsequent API calls:

```bash
curl -sk https://<sddc-manager-fqdn>/v1/hosts \
  -H "Authorization: Bearer <accessToken>"
```

API tokens expire after 24 hours by default. For automation pipelines, authenticate at the start of each run rather than caching tokens across runs.

---

## Credential Rotation

VCF manages credentials for all components in the SDDC stack (vCenter, NSX, ESXi, SDDC Manager itself). Use the built-in rotation workflow rather than changing passwords manually in individual products.

**Rotate credentials via SDDC Manager:**

1. SDDC Manager → Security → Credentials
2. Select the component and credential type (SSH, API, or SSO)
3. Click **Rotate** and confirm — SDDC Manager orchestrates the change across all dependent components
4. Verify the rotation task completes without errors in the Tasks view

**Rotate all passwords on a schedule:**

- ESXi root passwords: every 90 days
- vCenter SSO `administrator@vsphere.local`: every 90 days
- NSX admin password: every 90 days
- SDDC Manager admin password: every 90 days

Do not rotate credentials manually in vCenter or NSX for components managed by VCF — out-of-band changes break the credential store and cause lifecycle task failures.

---

## Quarterly Access Review Checklist

| Step | Action |
|---|---|
| 1. Export SDDC Manager user list | Administration → Users and Groups → note all accounts and assigned roles |
| 2. Export NSX Manager user list | System → User Management → Principal Identity and Roles |
| 3. Export vCenter Global Permissions | Administration → Global Permissions → export or screenshot |
| 4. Cross-reference with HR leavers | Revoke access for any account belonging to a departed employee or contractor |
| 5. Validate AD group membership | Confirm each AD group used for VCF access has correct, current members |
| 6. Review service accounts | Confirm each service account is still associated with a running integration; disable unused accounts |
| 7. Confirm break-glass account status | Verify `administrator@vsphere.local` password is current, stored in the vault, and access was not used outside a declared incident |
| 8. Document and sign off | Record review completion in the CMDB change record; obtain sign-off from the platform owner |
