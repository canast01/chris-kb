---
tags:
  - pure
  - security
---
# FlashArray — Hardening


<div class="kb-summary">
Hardening reference covering Hardening Checklist, Step-by-Step Controls, Post-Hardening Verification.

*Applies to: FlashArray Purity 6.x*
</div>
```text
┌──────────────────────────────── Pure FlashArray — Security Hardening ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FlashArray hardening: disable unused protocols, enforce encryption, restrict access      │   │
│   │         Network: dedicated storage VLAN; restrict management access to jump hosts only        │   │
│   │        Auth: disable default accounts; enforce password complexity and rotation policy        │   │
│   │         Audit: forward syslog to SIEM; alert on privilege escalation and failed logins        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Baseline config → disable unused → enforce MFA → enable logging → audit                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │         Controllers         │  │        Active-active        │  │           No SPOF           │   │
│   │            Drives           │  │         DirectFlash         │  │         NVMe native         │   │
│   │           Volumes           │  │       Thin provisioned      │  │        Instant clone        │   │
│   │        ActiveCluster        │  │       Sync replication      │  │           Zero RPO          │   │
│   │           SafeMode          │  │       Immutable snaps       │  │      Ransomware resist      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Area       │     Control      │      Standard     │      Verify      │    Frequency     │   │
│   │     Accounts     │ Disable defaults │  No default creds │   Login audit    │      Deploy      │   │
│   │    Protocols     │  Disable unused  │   TLS 1.2+ only   │    Port scan     │     Monthly      │   │
│   │       MFA        │ Enforce all admi │   TOTP/hardware   │    Auth logs     │    Continuous    │   │
│   │     Logging      │ SIEM forwarding  │  All admin events │   SIEM alerts    │      Daily       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FlashArray//X or //C controllers · DirectFlash NVMe modules · 25/100 GbE / 32Gb FC       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FlashArray         = Pure all-NVMe block/file array; inline dedup and compression always enabled   │
│    DirectFlash        = Pure proprietary NVMe modules; direct flash access without SAS translation    │
│    ActiveCluster      = synchronous active-active stretch cluster; hosts see a single namespace       │
│    ActiveDR           = asynchronous replication to DR site; recovery point objective in seconds      │
│    SafeMode           = admin-locked immutable snapshots; cannot be deleted even by array administr...│
│    Protection group   = set of volumes and hosts sharing a snapshot and replication schedule          │
│    purefa CLI         = REST CLI tool for FlashArray; purefa CLI connects via REST API key            │
│    purearray          = purectl CLI command: purearray list and purearray show monitoring             │
│    Volume tag         = user-defined key-value label on volumes for policy and reporting purposes     │
│    Host group         = logical collection of hosts sharing volume access via a host group object     │
│    Inline dedup       = content-based deduplication performed inline before data is written to flash  │
│    Evergreen          = Pure architecture; controllers upgrade non-disruptively, shelves remain in ...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
FlashArray Hardening Sequence
  1. Change defaults ──► rename/vault pureuser, create named admins
  2. Configure AD/LDAP ──► group-to-role mapping
  3. Enable SAML SSO ──► MFA enforced at IdP level
  4. Restrict mgmt network ──► dedicated VLAN, firewall ACL
  5. Install CA-signed TLS cert ──► replace self-signed
  6. Disable unused protocols ──► FC/iSCSI only what is needed
  7. Configure SNMPv3 ──► disable legacy SNMP versions
  8. Enable SafeMode ──► Pure Support required to destroy snaps
  9. Verify encryption at rest ──► purearray list --encryption
 10. Configure TLS syslog ──► forward audit log to SIEM
 11. Set idle timeout ──► purearray setattr --idle-timeout 15
```

This page covers the ordered hardening steps to apply on every new FlashArray before it enters production, along with the rationale and CLI commands for each control. Apply these steps after initial network and identity configuration and before connecting any production hosts.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Hardening Checklist

Work through these steps in order. Each control builds on the previous ones.

| # | Control | Status | Notes |
|---|---|---|---|
| 1 | Change default credentials and create named admin accounts | | |
| 2 | Configure AD/LDAP authentication | | |
| 3 | Enforce MFA via SAML SSO | | |
| 4 | Restrict management network access | | |
| 5 | Install a CA-signed TLS certificate | | |
| 6 | Disable unused protocols | | |
| 7 | Configure SNMPv3 and disable legacy SNMP | | |
| 8 | Enable SafeMode snapshots | | |
| 9 | Verify encryption at rest | | |
| 10 | Verify replication TLS | | |
| 11 | Configure syslog/audit forwarding to SIEM | | |
| 12 | Set session idle timeout | | |
| 13 | Audit and disable unused API tokens | | |
| 14 | Configure SMTP with TLS for alert emails | | |

---

## Step-by-Step Controls

### 1. Change Default Credentials and Create Named Admin Accounts

The factory default `pureuser` account uses a password printed on the array chassis label. This password is shared knowledge by anyone who has physically accessed the array.

```bash
# Change pureuser password to a strong randomly-generated credential
pureadmin setattr pureuser --password
# Enter a 20+ character random password at the prompt

# Create named admin accounts for the storage team
pureadmin create --role array_admin s.jones
pureadmin create --role storage_admin p.smith
pureadmin create --role ops_admin oncall-storage

# Set passwords for named accounts
pureadmin setattr s.jones --password
pureadmin setattr p.smith --password
pureadmin setattr oncall-storage --password
```

Store the `pureuser` credentials in the organisation's PAM vault (CyberArk, HashiCorp Vault, etc.) with access restricted to the on-call and emergency procedures. Document the vault path in the array's CMDB record.

---

### 2. Configure AD/LDAP Authentication

After AD integration, individual named local accounts can be removed for human admin access — role assignment comes from AD group membership.

```bash
# Join to Active Directory
puredirectoryservice setattr \
    --base-dn "DC=example,DC=com" \
    --bind-user "svc-pure-bind" \
    --bind-password "<password>" \
    --domain "example.com" \
    --uri "ldaps://dc01.example.com"

# Test the connection
pureds check

# Map AD groups to Purity roles
pureadmin setattr --role array_admin \
    --group "CN=pure-array-admins,OU=Groups,DC=example,DC=com"

pureadmin setattr --role storage_admin \
    --group "CN=pure-storage-admins,OU=Groups,DC=example,DC=com"

pureadmin setattr --role ops_admin \
    --group "CN=pure-ops,OU=Groups,DC=example,DC=com"

pureadmin setattr --role readonly \
    --group "CN=pure-readonly,OU=Groups,DC=example,DC=com"
```

Validate: log out and log back in with a domain account in each role group to confirm access works before removing or downgrading local accounts.

---

### 3. Enforce MFA via SAML SSO

SAML SSO delegates authentication to an enterprise IdP (Okta, Azure AD, ADFS) that enforces MFA. This is the preferred mechanism for production arrays where compliance requires MFA for privileged access.

```bash
# Enable SSO (after configuring SAML in the IdP and Purity GUI)
pureadmin global enable --single-sign-on

# Verify SSO is enabled
pureadmin global list
```

See the [Authentication](authentication/index.md) page for full SAML configuration steps. SAML integration requires Purity//FA 6.0 or later.

If SAML is not feasible in the short term, compensate with:
- Named account controls and PAM vault for credential management
- Network-level restriction (step 4) to limit the attack surface
- Audit log alerting for failed login attempts

---

### 4. Restrict Management Network Access

FlashArray does not provide built-in IP-based ACLs for the management plane. Implement network controls to protect the management interface:

| Control | Implementation |
|---|---|
| Dedicated management VLAN | Place management interface on a separate VLAN from data traffic |
| Firewall ACL | Allow TCP 22 (SSH) and TCP 443 (HTTPS/REST API) only from admin jump hosts and monitoring systems; deny all other sources |
| Jump host requirement | Require all admin access through a bastion host; the jump host should enforce MFA |
| No direct internet access | Management interface must not be directly internet-reachable; Pure1 phone-home uses outbound HTTPS only |

Verify the management interface is on the correct VLAN and the IP is not routable from untrusted networks. Document the allowed source ranges in the firewall change record.

---

### 5. Install a CA-Signed TLS Certificate

The factory default is a self-signed certificate that generates browser warnings and prevents proper certificate pinning in automation tools.

```bash
# View the current certificate (confirm it is currently self-signed)
purearray list --ssl-certificate

# Install a CA-signed certificate (PEM format: cert + intermediates + key combined)
purearray setattr --tls-certificate /path/to/combined.pem

# Verify the new certificate is active
purearray list --ssl-certificate
```

Requirements:
- RSA 4096 or ECDSA P-256 key
- SAN must include the array management IP and/or FQDN
- Certificate must be trusted by the browsers and automation tools that access the array
- Set a calendar reminder 30 days before expiry for renewal

---

### 6. Disable Unused Protocols

Reduce the attack surface by disabling protocols that are not in use.

```bash
# Check which protocols are currently enabled
purenetwork list
pureport list
```

**If iSCSI is not in use (FC-only environment):**

Disable iSCSI interfaces at the network level — set the iSCSI interface IP to `0.0.0.0` or down the interface via `purenetwork setattr`. Coordinate with Pure Support before disabling any interface if unsure.

**If SNMP is not required:**

Do not configure SNMP at all — Purity only enables SNMP if an SNMP community or trap destination is configured. If SNMP was previously configured for a legacy integration:

```bash
# List SNMP configuration
puresnmp list
puresnmptrap list

# Remove legacy SNMPv1/v2c communities if present
puresnmp delete <community_name>
```

**SSH access:**

SSH to the management interface is enabled by default and required for Purity CLI access. Do not disable SSH — restrict access at the network layer instead (step 4).

---

### 7. Configure SNMPv3 and Disable Legacy SNMP

If SNMP monitoring is required, use SNMPv3 with `authPriv` security level only (authentication + encryption). Never use SNMPv1 or SNMPv2c — they transmit community strings in plaintext and provide no access control.

```bash
# Configure SNMPv3 monitoring user
puresnmp create \
    --version v3 \
    --auth-protocol SHA \
    --auth-passphrase "<auth_pass_20_chars>" \
    --privacy-protocol AES \
    --privacy-passphrase "<priv_pass_20_chars>" \
    --user svc-snmp-monitor \
    monitoring-v3

# Configure SNMPv3 trap destination
puresnmptrap create \
    --version v3 \
    --auth-protocol SHA \
    --auth-passphrase "<auth_pass_20_chars>" \
    --privacy-protocol AES \
    --privacy-passphrase "<priv_pass_20_chars>" \
    --user svc-snmp-monitor \
    --host <nms_ip> \
    nms-trap-v3

# Verify
puresnmp list
puresnmptrap list
```

Ensure no SNMPv1 or v2c communities exist: `puresnmp list` should show only v3 entries.

---

### 8. Enable SafeMode Snapshots

SafeMode makes protection group snapshot schedules and snapshot retention policies immutable. No local admin (including `array_admin`) can delete a locked snapshot or modify its retention until the retention window expires. This prevents ransomware attacks from destroying backups even if admin credentials are compromised.

**How to enable:** Contact Pure Storage Support. SafeMode requires a dual-approval process — it cannot be activated from the array CLI alone. Engagement with a Pure Support engineer is required.

Before enabling SafeMode:
- [ ] Confirm all production protection group schedules are correct — retention windows, frequency, and replication targets
- [ ] Confirm the Purity eradication timer (default 24 hours for destroyed volumes) is set appropriately — SafeMode can extend this
- [ ] Brief the storage team: once SafeMode is enabled, snapshot deletion operations require Pure Support involvement

```bash
# Verify SafeMode status (after enablement)
purearray list --safemode
```

---

### 9. Verify Encryption at Rest

Encryption at rest is always-on and requires no configuration. Verify it is active after initial setup:

```bash
# Verify encryption is active
purearray list --encryption

# Verify all drives are SEDs (self-encrypting drives)
puredrive list --spec
# Look for 'encryption_enabled: true' or equivalent in the output
```

If KMIP external key management is required, configure it now. See [Encryption](encryption/index.md) for the full KMIP configuration procedure.

---

### 10. Verify Replication TLS

Inter-array replication uses TLS by default. Verify the connection is established and encrypted:

```bash
# List connected remote arrays and their connection status
purearray list --connection

# Verify replication protection groups have active targets
purepgroup list --replication
```

If the array is not yet connected to a remote array, this step is deferred until replication is configured.

---

### 11. Configure Syslog/Audit Forwarding to SIEM

Local audit logs can potentially be modified by a compromised `array_admin` account. Forward all logs to an external SIEM immediately so the log record is preserved off-array.

```bash
# Configure TLS syslog to SIEM (preferred — use TCP TLS for integrity)
puresyslog create --uri tls://<siem_ip>:6514 siem-tls

# UDP syslog (fallback only — not recommended for audit purposes)
puresyslog create --uri udp://<siem_ip>:514 siem-udp

# List configured syslog destinations
puresyslog list
```

Verify syslog delivery by checking the SIEM for log events from the array management IP. Generate a test event:

```bash
# Generate a test audit event (e.g., run a read-only command)
purearray list
# Check the SIEM for the corresponding audit log entry within 60 seconds
```

Configure SIEM alerts for:
- Multiple failed login attempts from the same source IP (brute force indicator)
- API token creation or deletion by non-standard accounts
- Protection group schedule modifications
- Volume or snapshot eradication events
- SafeMode-related audit entries

---

### 12. Set Session Idle Timeout

Unattended CLI or GUI sessions with admin-level privileges are a security risk. Set the idle timeout to 15 minutes.

```bash
# Set CLI/GUI session idle timeout (in minutes)
purearray setattr --idle-timeout 15

# Verify
purearray list --idle-timeout
```

This applies to both SSH (CLI) and HTTPS (GUI) sessions. A session that has been idle for 15 minutes will require re-authentication.

---

### 13. Audit and Disable Unused API Tokens

Service account API tokens that are unused represent permanent credentials with no expiry. Audit them after initial setup and at least quarterly.

```bash
# List all accounts and their API token status
pureadmin list --api-token

# Identify the last-used timestamp for each token
pureadmin list --api-token --expose
# Compare 'last_used' timestamp against expected usage pattern

# Revoke a token that is no longer needed (without deleting the account)
pureadmin delete svc-old --api-token

# Delete an account and its token if the integration no longer exists
pureadmin delete svc-decommissioned
```

Establish a quarterly review process:
1. Export the API token inventory to a ticket or spreadsheet
2. Confirm each token is actively used by an integration
3. Revoke tokens that cannot be accounted for

---

### 14. Configure SMTP with TLS for Alert Emails

Alert emails contain operational data about the array. Use STARTTLS or SMTPS to protect them in transit.

```bash
# Configure SMTP relay with TLS
puresmtp create \
    --username "pure-alerts@example.com" \
    --password "<smtp_password>" \
    --relay-host "smtp.example.com" \
    --relay-host-port 587 \
    --sender-domain "example.com" \
    default

# Add alert notification recipients
purealert create --email storage-team@example.com storage-team
purealert create --email oncall@example.com oncall

# Verify SMTP configuration
puresmtp list

# Send a test alert to confirm delivery
purealert test storage-team
```

---

## Post-Hardening Verification

Run the following checks after completing all hardening steps:

```bash
# Confirm array name, version, and general status
purearray list

# Confirm no critical alerts from hardening changes
purealert list

# Confirm AD authentication is working
pureds check
pureds list

# Confirm TLS certificate is from a CA (not self-signed)
purearray list --ssl-certificate

# Confirm SNMPv3 is the only SNMP configuration
puresnmp list

# Confirm syslog destinations are active
puresyslog list

# Confirm session timeout is set
purearray list --idle-timeout

# Confirm SafeMode status
purearray list --safemode

# Confirm encryption is active
purearray list --encryption

# Audit log: confirm recent hardening actions are captured
pureaudit list --sort time- | head -30
```

Document the completion date, the engineer who performed the hardening, and the Purity version at time of hardening in the array's CMDB record. Schedule a re-review at the next major Purity upgrade or 12 months, whichever comes first.
