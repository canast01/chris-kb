# VMware Cloud Foundation Security

> Part of the [VCF](../) reference.

---
## Hardening Checklist

- [ ] All default passwords rotated via SDDC Manager Password Management at first use
- [ ] Password rotation schedule configured to 90 days (or per policy)
- [ ] SDDC Manager RBAC roles mapped to AD groups — no shared local accounts for day-to-day operations
- [ ] Local `admin` and `vcf` accounts locked after initial deployment; passwords stored in vault
- [ ] TLS 1.2 minimum enforced on all VCF component endpoints (verify via SDDC Manager Security UI)
- [ ] Certificates for all components replaced with CA-signed certificates via SDDC Manager Certificate Management
- [ ] Syslog forwarding to SIEM configured under Administration → Syslog
- [ ] Network access to SDDC Manager UI (TCP 443) restricted to management jump-host CIDR via firewall
- [ ] vSAN data-at-rest encryption enabled for workload domains handling sensitive data
- [ ] SDDC Manager audit logs reviewed monthly for privilege escalation or unexpected API activity

---

## RBAC — SDDC Manager Roles

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

## Certificate Management

All VCF component certificates are managed through SDDC Manager's Certificate Management workflow. Do not replace certificates directly through component UIs (vCenter VAMI, NSX Manager) — SDDC Manager will lose track of the state.

```
SDDC Manager → Security → Certificate Management
```

**Replacement procedure:**

1. Generate CSR in SDDC Manager for the target component
2. Submit CSR to internal CA and receive the signed certificate + CA chain
3. Import the signed cert and chain back into SDDC Manager
4. SDDC Manager installs the certificate on the component and restarts affected services

**Check certificate expiry from the appliance:**

```bash
# SDDC Manager certificate
openssl s_client -connect <sddc-manager-ip>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates

# NSX Manager certificate
openssl s_client -connect <nsx-mgr-ip>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates

# vCenter certificate
openssl s_client -connect <vcenter-fqdn>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates
```

**Lead times:**

| Timeline | Action |
|---|---|
| 60 days | Plan renewal — raise change ticket |
| 30 days | Schedule maintenance window |
| 7 days | Treat as P2 — renew immediately |

---

## Password Management

```
SDDC Manager → Security → Password Management
```

- View current password state for all managed accounts
- Rotate individual accounts or schedule bulk rotation
- Password rotation log shows last rotated timestamp per account

**Break-glass rotation procedure (manual):**

1. Retrieve the break-glass account password from the enterprise vault
2. Rotate the password in SDDC Manager → Password Management
3. Update the vault entry with the new password immediately
4. Log the rotation in the change management system

---

## Audit Logging and SIEM Forwarding

```
SDDC Manager → Administration → Syslog → Add Syslog Server
```

- Protocol: TLS recommended for production (port 6514); UDP/TCP 514 also supported
- Test: perform a UI action after configuring and verify the event appears in the SIEM

**SDDC Manager audit log locations (SSH access):**

```bash
/var/log/vmware/vcf/sddc-manager/sddc-manager.log   # API and UI actions
/var/log/vmware/vcf/lcm/lcm.log                     # Lifecycle operations
/var/log/vmware/vcf/domainmanager/domainmanager.log  # Domain management events
```

---

## Network Access Controls

Firewall rules for SDDC Manager management plane:

| Source | Destination | Port | Purpose |
|---|---|---|---|
| Management jump-host CIDR | SDDC Manager IP | TCP 443 | SDDC Manager UI/API |
| SDDC Manager | vCenter IPs | TCP 443 | Component management |
| SDDC Manager | NSX Manager IPs | TCP 443 | NSX API |
| SDDC Manager | ESXi management IPs | TCP 443, 902 | Host management |
| SDDC Manager | SIEM IP | UDP/TCP 514 or TLS 6514 | Syslog |

Block direct access from workstation VLANs to SDDC Manager — all access goes through the management jump host.

---

## vSAN Encryption

For workload domains handling sensitive data:

1. Deploy and configure a KMS (Key Management Server) — SDDC Manager supports vSphere native KMS.
2. In vCenter for the workload domain: Cluster → Configure → vSAN → Services → Data-at-Rest Encryption → Enable.
3. Define a key rotation schedule (annual minimum or per policy) and document the rotation procedure.
4. Ensure the KMS is highly available — KMS loss makes the vSAN datastore inaccessible.

Key rotation is performed through vCenter → vSAN → Key Management → Rotate Keys. This is a live operation and does not require downtime.
