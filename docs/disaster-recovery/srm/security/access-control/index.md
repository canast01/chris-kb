# SRM Security — Access Control

## vCenter RBAC for DR Operators

Define a dedicated `DR-Operator` role in vCenter with only the privileges required for SRM operations:

```
Privileges to include:
  Site Recovery Manager:
    - Site Recovery.Manage
    - Site Recovery.Test
    - Site Recovery.Recovery
  Datastore:
    - Datastore.AllocateSpace
  Network:
    - Network.Assign (for network customisation)
  Virtual Machine:
    - Virtual Machine.Provisioning.* (for recovery)
```

Assign the role at the SRM inventory root — do not grant broad vCenter Admin privileges to DR operators.

---

## SRM RBAC Roles by Function

SRM operations require different privilege combinations depending on the DR workflow. Apply least-privilege per team function.

| SRM Function | Required vCenter Privileges | Required SRM Privileges | Assign To |
|---|---|---|---|
| View protection groups / plans | Read-only on vCenter objects | Site Recovery.View | DR-Read role |
| Run DR **test** (non-disruptive) | VM power on/off, datastore read | Site Recovery.Test | DR-Operator role |
| Execute **recovery** (planned / unplanned) | VM provision, datastore alloc, network assign | Site Recovery.Recovery | DR-Recovery role |
| **Re-protect** (reverse replication post-failover) | Storage policy, replication config | Site Recovery.Manage | DR-Admin role |
| **Failback** (return to primary site) | All of the above + primary site vCenter perms | Site Recovery.Manage | DR-Admin role |
| Manage protection groups (create/edit) | Datastore, replication group config | Site Recovery.Manage | DR-Admin role |
| Modify recovery plans | Recovery plan edit | Site Recovery.Manage | DR-Admin role |

> Create separate AD security groups for each role tier. Avoid assigning the DR-Admin role to operational staff — require approval workflow for recovery plan modifications.

---

## Protection Group and Recovery Plan Permissions

Access to create versus execute SRM objects is deliberately separated.

### Protection Groups

| Action | Who Can Perform | Permission Scope |
|---|---|---|
| Create / modify protection group | DR-Admin only | Site Recovery.Manage on protected site inventory |
| View protection group status | DR-Operator, DR-Read | Site Recovery.View |
| Add/remove VMs from group | DR-Admin only | Site Recovery.Manage + VM inventory rights |
| Delete protection group | DR-Admin only | Site Recovery.Manage |

### Recovery Plans

| Action | Who Can Perform | Permission Scope |
|---|---|---|
| Create / modify recovery plan | DR-Admin only | Site Recovery.Manage on recovery site SRM |
| Execute Test (cleanup included) | DR-Operator | Site Recovery.Test |
| Execute Planned Migration | DR-Recovery | Site Recovery.Recovery |
| Execute Emergency Recovery | DR-Recovery | Site Recovery.Recovery |
| Re-protect after recovery | DR-Admin | Site Recovery.Manage |
| Cancel in-progress recovery | DR-Admin | Site Recovery.Manage |

> Recovery plan execution is logged and non-reversible mid-stream. Require a change ticket and secondary approval before granting DR-Recovery role access outside of declared DR events.

---

## SRM REST API Authentication

SRM 8.x exposes a REST API for automation (port 443, path `/api`).

### Authentication Methods

| Method | Description | Use Case |
|---|---|---|
| vCenter SSO (session token) | Authenticate to vCenter SSO; use session cookie with SRM API | Interactive tooling, ad-hoc scripts |
| Local SRM account | SRM-local user in the SRM appliance management UI | Break-glass access when SSO is unavailable |
| Service account (SSO) | Dedicated AD/SSO service account with DR-Operator or DR-Admin role | CI/CD pipelines, orchestration tools |

### Obtain an API Session Token

```bash
# Authenticate to vCenter SSO and get a session token
curl -s -k -X POST "https://<vcenter>/rest/com/vmware/cis/session" \
  -u "administrator@vsphere.local:<password>" \
  | jq -r '.value'

# Use the session token with the SRM API
curl -s -k -X GET "https://<srm-server>/api/protection-groups" \
  -H "vmware-api-session-id: <session_token>"
```

### Local SRM Account (Break-Glass)

Access local SRM accounts at `https://<srm-appliance>:5480` (VAMI). Use only when vCenter SSO is unavailable. Rotate the local admin password after each use and store in a sealed break-glass envelope or PAM vault.

---

## Audit: Where SRM Logs DR Operations

SRM records all operations in multiple locations. Use these for compliance, change auditing, and post-DR review.

### Audit Log Locations

| Log Source | Location / Access Method | What It Records |
|---|---|---|
| SRM Events | vCenter UI → Site Recovery → Events tab | All SRM operations: plan runs, test start/end, errors |
| vCenter Tasks | vCenter UI → Tasks — filter by SRM task type | Task completion, duration, initiating user |
| Recovery History | SRM UI → Recovery Plans → select plan → History | Per-plan execution records with timestamps and outcomes |
| SRM appliance syslog | `/var/log/vmware/dr/` on SRM appliance (SSH) | Detailed server-side logs for troubleshooting |
| vCenter Audit Log | vCenter UI → Administration → Events → export | Includes RBAC changes affecting SRM roles |

### Key Commands for Log Review

```bash
# SSH to SRM appliance (admin or root)
ssh admin@<srm-appliance>

# View live SRM server log
tail -f /var/log/vmware/dr/dr.log

# Search for recovery plan execution events
grep -i "recovery plan\|RECOVERY_STARTED\|RECOVERY_COMPLETE\|RECOVERY_FAILED" \
  /var/log/vmware/dr/dr.log

# Search for authentication events (login/logout, permission denied)
grep -i "authentication\|login\|permission denied\|unauthorized" \
  /var/log/vmware/dr/dr.log | tail -50
```

### Exporting Recovery History for Compliance

In the SRM UI: **Recovery Plans** → select plan → **History** → **Export** — produces a CSV with plan name, start time, end time, result, and initiating user. Retain exports for audit evidence per your retention policy (typically 1–3 years for DR events).
