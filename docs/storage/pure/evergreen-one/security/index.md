# Pure Storage Evergreen//One Security


<div class="kb-summary">
Pure Storage Evergreen//One Security reference covering Hardening Checklist, RBAC, Encryption, Audit Logging, Subscription Security — Pure-Managed Responsibilities.
</div>

```text
  Pure Security Architecture

  ┌─────────────────────────────────────────────────┐
  │  FlashArray / FlashBlade                        │
  │                                                 │
  │  Encryption                                     │
  │  ├─ Data at rest: XTS-AES-256 (always on)       │
  │  ├─ Data in flight: TLS 1.2+ (management)       │
  │  └─ Drive erasure: cryptographic key destroy    │
  │                                                 │
  │  RBAC                                           │
  │  ├─ array_admin ──► full system access          │
  │  ├─ storage_admin ──► volumes / snapshots       │
  │  ├─ ops_admin ──► read + alert ack              │
  │  └─ readonly ──► auditors / CMDB                │
  │                                                 │
  │  Audit Logging                                  │
  │  └─ Every admin action ──► syslog ──► SIEM      │
  │     (customer AND Pure Support actions logged)  │
  │                                                 │
  │  SafeMode                                       │
  │  └─ Snapshot destroy requires Pure Support ─►   │
  │     Protection against ransomware               │
  └─────────────────────────────────────────────────┘
  SSO/SAML ──► IdP MFA enforced for all interactive login
```

## Hardening Checklist

- Enforce TLS 1.2 or higher for all management access; confirm HTTP redirect is disabled on all array management interfaces
- Disable unused host protocols (FC, iSCSI, NVMe variants) — configure only the protocols required for connected hosts
- Rotate API tokens for all customer-managed service accounts on a defined schedule (90 days); revoke immediately on staff departure
- Restrict management network access to a dedicated out-of-band management VLAN; do not expose the management interface on the data network
- Enable SafeMode for all Tier-1 protection groups — SafeMode requires Pure Support involvement before snapshots can be destroyed, protecting against ransomware lateral movement
- Confirm Pure1 phonehome is always active — phonehome is the channel through which Pure delivers proactive security response and is required for SLA monitoring
- Review customer-managed local accounts in Purity quarterly; remove accounts no longer associated with active personnel
- Confirm SSO/SAML integration is configured for all interactive user access to enforce MFA through the identity provider

## RBAC

Purity uses built-in role-based access control. For Evergreen//One, Pure's support and operations engineers also have privileged access to the arrays under the service agreement. Customer RBAC should be managed independently for customer-side operational accounts.

| Role | Permissions | Use Case |
|---|---|---|
| `array_admin` | Full access: system, user, and protocol configuration | Array administrators; restrict to named individuals; Pure Support uses this role for managed operations |
| `storage_admin` | Manage volumes, hosts, protection groups, snapshots; no system or user config | Storage operations team; backup and automation service accounts |
| `ops_admin` | Read access plus alert acknowledgement | Operations centre monitoring staff |
| `readonly` | Read-only view of all configuration and status | Auditors, billing validators, CMDB integrations |

```bash
# List local user accounts and roles
pureuser list

# List API tokens (customer-managed accounts)
pureuser apitoken list
```

Configure SAML/SSO in the Purity GUI to enforce IdP-managed MFA for all interactive access. This ensures that even if a local account is compromised, interactive login requires a second factor controlled by the IdP.

## Encryption

**Data at Rest**

All data on FlashArray DirectFlash Modules is encrypted with XTS-AES-256. Encryption is always enabled and cannot be disabled. When Pure replaces a drive, cryptographic erasure is performed by destroying the per-drive key — no physical destruction is needed for data sanitisation. Pure provides erasure certificates on request.

**Data in Flight**

All management plane traffic uses TLS 1.2 or higher. Host data plane encryption options:

- **NVMe/TCP** — IPsec at the network layer for in-flight encryption
- **iSCSI** — CHAP authentication; transport encryption via network-layer IPsec or MACsec
- **FC / NVMe-FC** — MACsec at the SAN fabric layer if required

**Key Management**

| Option | Description |
|---|---|
| Internal key management | Default; keys managed within the array |
| External KMIP | Integration with a KMIP-compliant key manager (e.g., Thales, HashiCorp Vault) for centralised key control and separation of duties |

For Evergreen//One, Pure manages the encryption infrastructure as part of the service. Confirm with the Pure account team whether external KMIP integration requires a service agreement amendment.

## Audit Logging

Purity records an audit log entry for every administrative action — by both customer accounts and Pure Support accounts — including username, source IP, timestamp, and operation performed.

Forward audit logs to a customer-managed SIEM:

```bash
# Add syslog destination (UDP)
purearray syslog add --uri udp://siem:514

# Add syslog destination (TLS-encrypted)
purearray syslog add --uri tls://siem:6514

# List configured syslog destinations
purearray syslog list
```

Because Pure Support engineers access the arrays as part of the managed service, off-array audit log retention is especially important for Evergreen//One — it provides the customer with an independent record of all operations performed on customer data, including by Pure staff.

## Subscription Security — Pure-Managed Responsibilities

Evergreen//One shifts several security functions from the customer to Pure:

- **Hardware firmware** — Pure manages all drive and controller firmware; customers never need to apply firmware updates
- **Purity OS security patches** — Pure delivers security patches through scheduled Purity upgrades; critical advisories trigger out-of-cycle patching with advance customer notification
- **Drive retirement and erasure** — Pure performs cryptographic erasure on all drives removed from the service, and provides erasure certificates on request — this satisfies data destruction requirements for regulated environments
- **Proactive monitoring** — Pure1 AIOps continuously monitors array health; anomalous snapshot deletion spikes or alert patterns can be flagged proactively, providing an early indicator of ransomware or insider threat activity

Review the Pure Security Advisories page (https://support.purestorage.com/Security_Advisories) for awareness of disclosed vulnerabilities. Pure will contact customers directly for any advisory requiring action on the managed service, but tracking advisories independently is recommended for compliance documentation.
