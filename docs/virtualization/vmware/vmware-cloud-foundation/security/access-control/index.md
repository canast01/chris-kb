# VCF — Access Control


<div class="kb-summary">
Access Control reference covering Credential Rotation, Quarterly Access Review Checklist.
</div>

VCF RBAC Model — Role Assignment Flow
```text
┌─────────────────────────────────────────────────────┐
│  Active Directory                                                                                     │
│  ┌──────────────────────────────────────────────┐                                                     │
│  │  GG-VCF-Admins · GG-VCF-Operators · ...     │                                                      │
│  └──────────────────────────────────────────────┘                                                     │
└───────────────────────┬─────────────────────────────┘
```
```
┌────────────────────────────── VMware Cloud Foundation — Access Control ───────────────────────────────┐
│                                                                                                       │
│  VCF access control spans SDDC Manager (admin/operator/viewer roles), vCenter RBAC                    │
│  per domain, NSX RBAC, and credential management for all service accounts.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              SDDC Manager Roles              │  │               Per-Domain RBAC               │   │
│   │             Admin: full control              │  │           Each domain: own vCenter          │   │
│   │       Operator: manage but not config        │  │             AD groups per domain            │   │
│   │         Viewer: read-only dashboard          │  │            NSX: per-domain roles            │   │
│   │           SSO: AD-integrated login           │  │            No cross-domain access           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SDDC Manager roles control VCF platform ops; domain RBAC controls workload access.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Credential Management             │  │              Audit & Compliance             │   │
│   │          SDDC Mgr: rotate passwords          │  │           Log: all SDDC Mgr events          │   │
│   │          Service accounts: managed           │  │           Review admin list qtrly           │   │
│   │         Break-glass: local SSO admin         │  │           Alert: failed login SIEM          │   │
│   │         Vault integration: optional          │  │           SDDC Mgr audit log: API           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SDDC Manager runs on management domain; AD must be reachable on management network                   │
│  for identity-based login; all SDDC Mgr operations are logged.                                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager Admin= full platform control; assign to minimal staff                                   │
│  Operator role= manage domains/clusters; cannot change VCF config                                     │
│  Viewer role   = read-only; safe for monitoring teams                                                 │
│  AD integration= SDDC Mgr authenticates against AD via LDAP                                           │
│  Break-glass   = local admin account; used when AD is unreachable                                     │
│  Credential rotation= SDDC Mgr rotates service account passwords automatically                        │
│  Vault integration= optional HashiCorp Vault for credential storage                                   │
│  SIEM          = receives SDDC Mgr syslog and vCenter events                                          │
│  Audit API     = SDDC Mgr REST API /v1/audit-events endpoint                                          │
│  Quarterly review= verify admin role assignments across all domains                                   │
│  No cross-domain= workload domain RBAC is isolated per domain                                         │
│  Service accounts= SDDC Mgr manages all component service credentials                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Credential Rotation (all via SDDC Manager — never manually):
```text
```
```
┌─────────────────────────────────────────────────────┐
│  SDDC Manager → Security → Credentials → Rotate                                                       │
│  ESXi root · vCenter SSO admin · NSX admin                                                            │
│  SDDC Manager admin · vSAN iSCSI accounts                                                             │
│  Schedule: every 90 days (or per policy)                                                              │
└─────────────────────────────────────────────────────┘
```text
┌────────────────────────────── VMware Cloud Foundation — Access Control ───────────────────────────────┐
│                                                                                                       │
│  VCF access control spans SDDC Manager (admin/operator/viewer roles), vCenter RBAC                    │
│  per domain, NSX RBAC, and credential management for all service accounts.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              SDDC Manager Roles              │  │               Per-Domain RBAC               │   │
│   │             Admin: full control              │  │           Each domain: own vCenter          │   │
│   │       Operator: manage but not config        │  │             AD groups per domain            │   │
│   │         Viewer: read-only dashboard          │  │            NSX: per-domain roles            │   │
│   │           SSO: AD-integrated login           │  │            No cross-domain access           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SDDC Manager roles control VCF platform ops; domain RBAC controls workload access.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Credential Management             │  │              Audit & Compliance             │   │
│   │          SDDC Mgr: rotate passwords          │  │           Log: all SDDC Mgr events          │   │
│   │          Service accounts: managed           │  │           Review admin list qtrly           │   │
│   │         Break-glass: local SSO admin         │  │           Alert: failed login SIEM          │   │
│   │         Vault integration: optional          │  │           SDDC Mgr audit log: API           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SDDC Manager runs on management domain; AD must be reachable on management network                   │
│  for identity-based login; all SDDC Mgr operations are logged.                                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager Admin= full platform control; assign to minimal staff                                   │
│  Operator role= manage domains/clusters; cannot change VCF config                                     │
│  Viewer role   = read-only; safe for monitoring teams                                                 │
│  AD integration= SDDC Mgr authenticates against AD via LDAP                                           │
│  Break-glass   = local admin account; used when AD is unreachable                                     │
│  Credential rotation= SDDC Mgr rotates service account passwords automatically                        │
│  Vault integration= optional HashiCorp Vault for credential storage                                   │
│  SIEM          = receives SDDC Mgr syslog and vCenter events                                          │
│  Audit API     = SDDC Mgr REST API /v1/audit-events endpoint                                          │
│  Quarterly review= verify admin role assignments across all domains                                   │
│  No cross-domain= workload domain RBAC is isolated per domain                                         │
│  Service accounts= SDDC Mgr manages all component service credentials                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
