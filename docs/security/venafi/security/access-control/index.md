# Venafi — Access Control


<div class="kb-summary">
> Part of the [Venafi](../../index.md) reference. Least-privilege role assignment must be enforced, with service account permissions scoped to specific policy folders only. Separation of duties separates CA trust anchor management from day-to-day certificate operations.
</div>

> Part of the [Venafi](../../index.md) reference.

Least-privilege role assignment must be enforced, with service account permissions scoped to specific policy folders only. Separation of duties separates CA trust anchor management from day-to-day certificate operations.

---

## RBAC Roles

| Role | Capabilities | Typical Assignees |
|---|---|---|
| **Policy Master** | Create and modify CA configurations, define certificate policies, manage policy folder hierarchy, assign permissions to other roles, import and trust CA certificates | PKI team leads, security architects |
| **Certificate Manager** | Request, renew, revoke, and retire certificates within assigned policy folders; manage CSRs; trigger manual validation; push certificates to target systems | PKI operations, platform engineers managing certificate lifecycle |
| **Certificate Approver** | Review and approve or reject pending certificate requests; cannot request or revoke directly | Security team, compliance officers |
| **Viewer** | Read-only access to certificate inventory, expiry status, and policy configuration; cannot request, approve, or modify anything | Audit staff, monitoring tool service accounts, helpdesk |

## Policy Folder Permission Model

Venafi TPP permissions are scoped to **policy folders** — the organizational unit that defines certificate issuance rules for a given domain or team.

| Concept | Detail |
|---|---|
| **Inheritance** | Permissions granted at a parent folder automatically propagate to all sub-folders unless explicitly overridden at the child level. |
| **Scoping** | Assign Certificate Manager or Approver roles at the lowest folder that covers the team's scope — never grant permissions at the root policy folder unless required. |
| **Isolation** | Separate policy folders per environment (production, non-production) and per business unit. Cross-folder access requires explicit justification and Policy Master approval. |
| **CA binding** | Each policy folder binds to one or more CA templates. A Certificate Manager cannot request from a CA template outside their assigned folder's binding. |

**Recommended folder structure:**

```text
Policy/
├── Production/
│   ├── Internal-PKI/
│   └── Public-CA/
└── Non-Production/
    ├── Dev/
    └── Test/
```

## Service Account Configuration

Minimum TPP permissions required for each integration type:

| Integration | Required Role | Folder Scope | Notes |
|---|---|---|---|
| **CertBot** | Certificate Manager | Target policy folders only | Needs request, renew, revoke. Grant no access to CA configuration folders. |
| **Venafi PKI Secrets Engine (Vault)** | Certificate Manager | Folders bound to Vault-issued certificates | The Vault plugin authenticates via a dedicated service account token. Rotate the token every 90 days. |
| **REST API apps (custom integrations)** | Viewer or Certificate Manager | Narrowest folder covering the app's certificates | Grant Viewer if the app only reads certificate metadata. Grant Certificate Manager only if the app must trigger renewals. |
| **Monitoring / SIEM** | Viewer | Root (read-only audit use) | Monitoring tools need read access to expiry data only. Restrict to Viewer to prevent accidental changes. |

Service accounts must:

- Be named to identify the owning system (e.g., `svc-vault-pki`, `svc-certbot-prod`)
- Never share credentials with human user accounts
- Use API key authentication rather than password-based authentication where supported

## API Key Permission Scopes

| Capability | API Key Can Do | API Key Cannot Do |
|---|---|---|
| Certificate lifecycle | Request, renew, revoke within authorized policy folders | Modify policy folder permissions or CA trust configuration |
| Certificate retrieval | Download issued certificate and private key (if key generation is server-side) | Access certificates outside the key's authorized folder scope |
| Reporting | Query certificate inventory and expiry data | Export CA private keys or trust anchor material |
| Approvals | Submit requests for approval | Self-approve requests (Approver role required separately) |

API keys are scoped to the permissions of the TPP user account that generated them — a Viewer account's API key cannot perform Certificate Manager actions regardless of how the key is configured.

## Quarterly Access Review Procedure

1. Export the full user and service account list from TPP: **Configuration** → **Users and Groups** → export to CSV.
2. Compare against the HR leavers report and contractor roster for the quarter.
3. For each account, confirm:
   - The account is still associated with an active staff member or running system.
   - The assigned role matches the current job function or integration requirement.
   - Policy folder scope is no broader than needed.
4. Revoke or disable accounts with no activity in the past 90 days.
5. Escalate any account with Policy Master access that is not documented in the PKI RACI.
6. Record findings and sign-off in the quarterly PKI access review document in the CMDB.
