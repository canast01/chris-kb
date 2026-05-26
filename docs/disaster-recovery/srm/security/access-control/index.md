# SRM Security — Access Control

## vCenter RBAC for DR Operators

Define a dedicated `DR-Operator` role in vCenter with only the privileges required for SRM operations:

```yaml
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
