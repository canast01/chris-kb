# Aria Operations — Security

## RBAC Roles

| Role | Permissions |
|------|------------|
| Administrator | Full access — manage users, adapters, system settings |
| Content Admin | Manage dashboards, views, reports, alerts, policies |
| Operator | Acknowledge/cancel alerts, run actions; no admin access |
| Read Only | View dashboards, alerts, and metrics; no changes |

Roles are assigned in **Administration > Access Control > User Accounts** or via imported AD/LDAP groups.

---

## Local Admin Account Hardening

- Change the default `admin` password immediately after deployment.
- Use a strong passphrase (minimum 16 characters, mixed case, numbers, symbols).
- Restrict local admin use — prefer AD group-based RBAC for day-to-day access.
- Store the admin credential in a secrets vault or password manager.

---

## TLS Certificate Replacement

Aria Operations ships with a self-signed certificate. Replace with a CA-signed certificate for production.

### Via UI

```
Administration > Certificates > Replace Certificate
```

Upload:
- Certificate (PEM)
- Private key (PEM, no passphrase)
- CA chain / intermediate (PEM)

### Via CLI

```bash
ssh admin@<aria-ops-primary-fqdn>

# Import certificate
vracli certificate import \
  --cert /tmp/aria-ops.crt \
  --key /tmp/aria-ops.key \
  --ca /tmp/ca-chain.crt

# Verify certificate
vracli certificate show
```

> After certificate replacement, all nodes must be updated — the LCM or in-product wizard handles cluster-wide propagation.

---

## LDAP / Active Directory Authentication

See [Integration](../integration/) for full LDAP configuration steps.

**Best practices:**

- Use a dedicated read-only service account for LDAP bind.
- Map specific AD groups to roles — avoid broad group mappings.
- Set the session timeout: **Administration > Global Settings > Session Timeout**.

---

## Audit Logging

Aria Operations writes audit events (login, logout, configuration changes, alert actions) to internal logs and optionally to syslog.

### Enable syslog forwarding

```
Administration > Outbound Settings > Add Plugin > Syslog
```

| Field | Value |
|-------|-------|
| Host | `siem.domain.local` |
| Port | 514 (UDP) or 6514 (TLS) |
| Protocol | UDP / TCP / TLS |

Audit log path on appliance:

```bash
/storage/log/audit/
```

---

## Hardening Checklist

- [ ] Default admin password changed
- [ ] CA-signed TLS certificate installed
- [ ] LDAP/AD authentication configured and tested
- [ ] Local accounts minimised — only break-glass admin kept local
- [ ] Role assignments reviewed — least privilege applied
- [ ] Session timeout configured (recommended: 30 minutes)
- [ ] Syslog/audit forwarding to SIEM enabled
- [ ] Unused adapters/accounts removed
- [ ] Snapshots disabled for production cluster nodes (performance impact)
- [ ] vCenter service account uses minimum required permissions

---

## Compliance Notes

- Aria Operations itself does not enforce compliance frameworks but can monitor compliance of infrastructure objects via **Compliance Benchmarks** (PCI-DSS, HIPAA, CIS).
- Navigate to **Environment > Compliance** to view and run compliance workloads.

---

## Related Sections

- [Integration](../integration/) — LDAP and AD setup
- [Operations](../operations/) — certificate renewal workflow
- [Vendor Support](../vendor-support/) — opening security-related cases
