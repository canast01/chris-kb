---
tags:
  - pure
  - security
---
# Pure Storage Evergreen Security


<div class="kb-summary">
Pure Storage Evergreen Security reference covering Hardening Checklist, RBAC, Encryption, Audit Logging, Subscription Security.
</div>

Evergreen Security Controls
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Same FlashArray/FlashBlade security model applies                                                    │
│  ├── AES-256 encryption at rest (always-on SEDs)                                                      │
│  ├── TLS for all management + replication traffic                                                     │
│  ├── RBAC: array_admin / storage_admin / ops / readonly                                               │
│  ├── SafeMode snapshots (Pure Support required to delete)                                             │
│  └── AD/LDAP/SAML SSO for human admin auth                                                            │
├──────────────────────────────────────────────────────────┤
│  Evergreen-specific controls                                                                          │
│  ├── Rotate API tokens every 90 days                                                                  │
│  ├── Phone-home always active (contractual)                                                           │
│  └── Controller refresh: drives sanitised before return                                               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Hardening Checklist

- Enforce TLS 1.2 or higher for all management access (GUI, REST API); confirm HTTP redirect is disabled
- Disable unused host protocols — if the array serves only iSCSI hosts, disable FC initiator support in the Purity configuration
- Rotate API tokens for all service accounts on a defined schedule (90 days recommended); revoke immediately on staff departure
- Disable or remove unused local accounts; all operational access should use named accounts or SAML/SSO integration where supported
- Restrict management network access to a dedicated out-of-band management VLAN; do not expose the management interface on the data network
- Enable SafeMode for protection groups on all Tier-1 production arrays — SafeMode requires a second-factor confirmation from Pure Support before snapshots can be destroyed, protecting against ransomware
- Confirm Pure1 phonehome is active — phonehome enables proactive monitoring and is required for the security patch delivery model under Evergreen
- Review local user accounts quarterly and remove any accounts no longer associated with active staff or service accounts

## RBAC

Purity//FA uses built-in role-based access control. All user access should be assigned the minimum role required for the task.

| Role | Permissions | Use Case |
|---|---|---|
| `array_admin` | Full access: system configuration, user management, protocol, and hardware settings | Array administrators; restrict to named individuals only |
| `storage_admin` | Manage volumes, hosts, protection groups, and snapshots; cannot modify system or user configuration | Storage operations team; backup and automation service accounts |
| `ops_admin` | Read access plus alert acknowledgement; cannot modify configuration | Operations centre staff; monitoring tools |
| `readonly` | Read-only view of all configuration and status | Auditors, capacity planners, CMDB integrations |

Configure SSO/SAML integration to map IdP groups to Purity roles. This enforces MFA through the IdP, enables central access revocation, and provides a consolidated audit trail.

```bash
# List all local user accounts and assigned roles
pureuser list

# List API tokens
pureuser apitoken list
```

## Encryption

**Data at Rest**

All data written to FlashArray DirectFlash Modules is encrypted using XTS-AES-256. Encryption is always on and cannot be disabled. Drive retirement and replacement trigger cryptographic erasure by destroying the per-drive encryption key — no physical destruction is required for data sanitisation.

**Data in Flight**

All management plane traffic (GUI, REST API) uses TLS 1.2 or higher. Host data plane encryption depends on protocol:

- **NVMe/TCP** — IPsec can be applied at the network layer for in-flight encryption
- **iSCSI** — CHAP authentication is configurable; transport-layer encryption is handled at the network level (IPsec/MACsec)
- **FC / NVMe-FC** — encryption at the SAN fabric layer (MACsec on FC switches) if required

**Key Management Options**

| Option | Description |
|---|---|
| Internal key management | Default; encryption keys managed within the array; no external dependency |
| External KMIP | Integrate with an external Key Management Interoperability Protocol (KMIP) server (e.g., Thales, HashiCorp Vault) for centralised key management and separation of duties |

Configure KMIP integration via **Settings > Security > Key Management** in the Purity GUI.

## Audit Logging

Purity//FA records an audit log entry for every administrative action — GUI, CLI, or REST API — including username, source IP, timestamp, and the specific operation performed.

Forward audit logs to a SIEM or centralised syslog server:

```bash
# Add a syslog destination (UDP)
purearray syslog add --uri udp://siem:514

# Add a syslog destination (TLS-encrypted)
purearray syslog add --uri tls://siem:6514

# List configured syslog destinations
purearray syslog list
```

Ensure logs are forwarded off-array. An attacker with array admin access could not modify forwarded syslog entries, but could clear the local audit log. Off-array log retention is essential for forensic integrity.

## Subscription Security

Under the Evergreen subscription model, Pure manages several security functions that would otherwise fall to the customer:

- **Hardware firmware** — Pure manages and applies drive and controller firmware updates as part of Purity software upgrades; customers do not need to track or apply firmware independently
- **Security patches** — Purity OS security patches are delivered through standard Purity software upgrades; the Evergreen subscription includes all software upgrades, so staying on a current Purity version is the primary security posture control
- **Controller refresh** — the Ever Modern refresh replaces controller hardware before it reaches end of vendor support, eliminating the security risk of running unsupported hardware
- **Phonehome monitoring** — Pure1 continuously monitors array health and can detect anomalous behaviour (unexpected snapshot deletion, alert spikes) that may indicate a security incident

---

Review the Pure Security Advisories page (https://support.purestorage.com/) regularly and apply Purity upgrades promptly when a security advisory is issued.
