---
tags:
  - pure
  - security
---
# FlashBlade — Hardening


<div class="kb-summary">
Hardening reference covering Hardening Checklist, Step-by-Step Controls, Post-Hardening Verification.

*Applies to: FlashBlade Purity//FB 4.x*
</div>
```text
┌──────────────────────────────── Pure FlashBlade — Security Hardening ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FlashBlade hardening: disable unused protocols, enforce encryption, restrict access      │   │
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
│   │            Blades           │  │           NVMe+CPU          │  │         Parallel I/O        │   │
│   │             File            │  │           NFS/SMB           │  │        Scale-out NAS        │   │
│   │            Object           │  │           S3/Swift          │  │         Bucket store        │   │
│   │         Replication         │  │            Async            │  │          DR/backup          │   │
│   │           SafeMode          │  │         Locked snaps        │  │      Ransomware resist      │   │
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
│    Physical: FlashBlade//S or //E chassis · storage blades · 100 GbE network · Pure1 SaaS             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FlashBlade         = Pure massively parallel all-flash NAS and object platform; single namespace   │
│    Blade              = individual storage module in FlashBlade chassis; NVMe and CPU per blade       │
│    File system        = FlashBlade NFS/SMB export namespace; up to 4 PiB per file system              │
│    Object store       = S3-compatible bucket store on FlashBlade; versioning and lifecycle rules      │
│    purefb CLI         = REST CLI client for FlashBlade: purefb fs list, purefb array show commands    │
│    Replication        = async file or object replication between FlashBlade systems for DR            │
│    SafeMode           = admin-locked snapshots; protected from deletion even by local array admin     │
│    S3 multitenancy    = per-bucket policy and IAM-style access control for object storage             │
│    NFS Kerberos       = FlashBlade NFS supports krb5, krb5i, and krb5p security flavours              │
│    SMB multichannel   = FlashBlade uses SMB multichannel for improved Windows client performance      │
│    Inline compression = always-on data reduction; typically 2-10x for unstructured data               │
│    ActiveScale        = enterprise geo-distribution and erasure coding for large object workloads     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
FlashBlade Hardening Sequence
  1. Default credentials ──► rename/vault admin account
  2. Configure AD ──► SMB auth + admin group-to-role mapping
  3. Enable SAML SSO ──► MFA for GUI access
  4. Restrict mgmt network ──► dedicated VLAN + ACL
  5. Install CA-signed TLS cert ──► replace self-signed
  6. NFS export policy ──► restrict to specific client CIDRs
  7. SMB share ACLs ──► AD group-based permissions
  8. S3 access keys ──► one key per workload, rotate 90 days
  9. Disable unused protocols ──► only NFS/SMB/S3 as required
 10. Configure TLS syslog ──► forward audit to SIEM
 11. Enable Pure1 phone-home ──► required for proactive support
```

> Part of the [FlashBlade Security](index.md) reference.

---

This page covers the ordered hardening steps to apply on every new FlashBlade before it enters production. Apply these steps after initial network and identity configuration and before connecting production NFS, SMB, or S3 clients.

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
| 2 | Configure AD/LDAP authentication and map groups to Purity roles | | |
| 3 | Enforce MFA via SAML SSO | | |
| 4 | Restrict management network access to dedicated management VLAN | | |
| 5 | Install a CA-signed TLS certificate on the management interface | | |
| 6 | Disable unused data protocols | | |
| 7 | Configure SNMPv3 and remove any legacy SNMP communities | | |
| 8 | Enable SafeMode snapshots | | |
| 9 | Verify encryption at rest is active | | |
| 10 | Restrict NFS exports to specific client IP ranges | | |
| 11 | Review and restrict S3 bucket policies | | |
| 12 | Configure syslog/audit forwarding to SIEM | | |
| 13 | Set session idle timeout | | |
| 14 | Audit and disable unused API tokens | | |
| 15 | Configure SMTP with TLS for alert emails | | |

---

## Step-by-Step Controls

### 1. Change Default Credentials and Create Named Admin Accounts

The factory default `pureuser` account credentials are documented in the array's initial setup guide and may be known to anyone who has been involved in the physical installation. Change the password immediately and create named accounts for the storage team.

```bash
# Change pureuser password to a strong randomly-generated credential (20+ characters)
purefb admin update --name pureuser --password
# Enter the new password at the prompt

# Create named admin accounts for the storage team
purefb admin create --name s.jones --role array_admin
purefb admin create --name p.smith --role storage_admin
purefb admin create --name svc-monitoring --role readonly

# Create a break-glass account
purefb admin create --name break-glass --role array_admin

# Set passwords for named accounts
purefb admin update --name s.jones --password
purefb admin update --name p.smith --password
```

Store the break-glass and pureuser credentials in the organisation's PAM vault (CyberArk, HashiCorp Vault) with access restricted to the on-call escalation procedure. Document the vault path in the array's CMDB record.

---

### 2. Configure AD/LDAP Authentication

After AD integration, individual named local accounts can be removed for human admin access — role assignment comes from AD group membership.

```bash
# Configure AD directory service
purefb directory-service update \
    --enabled true \
    --uri "ldaps://dc01.example.com" \
    --base-dn "DC=example,DC=com" \
    --bind-user "CN=svc-pure-bind,OU=ServiceAccounts,DC=example,DC=com" \
    --bind-password "<bind_password>"

# Test the connection
purefb directory-service test

# Map AD groups to Purity roles
purefb admin add-group \
    --name "CN=pure-fb-admins,OU=Groups,DC=example,DC=com" \
    --role array_admin

purefb admin add-group \
    --name "CN=pure-storage-ops,OU=Groups,DC=example,DC=com" \
    --role storage_admin

purefb admin add-group \
    --name "CN=pure-readonly,OU=Groups,DC=example,DC=com" \
    --role readonly
```

Validate: log out and log back in with a domain account in each role group to confirm access works before removing individual local accounts.

---

### 3. Enforce MFA via SAML SSO

SAML SSO delegates authentication to an enterprise IdP (Okta, Azure AD, ADFS) that enforces MFA. This is the preferred mechanism for production FlashBlade arrays where compliance requires MFA for privileged access.

Configure SSO via the Purity//FB GUI: **Settings > Access > Single Sign-On**. See [Authentication](authentication/index.md) for full SAML configuration steps.

```bash
# Verify SSO status after configuration
purefb array list --sso
```

If SAML is not feasible in the short term, compensate with:
- Named account controls and PAM vault for credential management
- Network-level restriction (step 4) to limit the attack surface
- SIEM alerting for failed login attempts

---

### 4. Restrict Management Network Access

FlashBlade does not provide built-in IP-based ACLs for the management plane. Implement network controls at the infrastructure layer:

| Control | Implementation |
|---|---|
| Dedicated management VLAN | Place the management interface on a separate VLAN from all data VLANs |
| Firewall ACL | Allow TCP 22 (SSH) and TCP 443 (HTTPS/REST API) only from admin jump hosts and monitoring systems; deny all other sources |
| Jump host requirement | Require all admin access through a bastion host with MFA; the FlashBlade management IP should not be reachable from general-purpose workstations |
| No direct internet access | Management interface must not be directly internet-reachable; Pure1 phone-home uses outbound HTTPS only |

Verify the management interface VLAN assignment and confirm the management IP is not routable from untrusted networks. Document the allowed source ranges in the firewall change record.

---

### 5. Install a CA-Signed TLS Certificate

The factory default is a self-signed certificate that generates browser warnings and prevents proper certificate pinning in automation tools.

```bash
# View the current certificate — confirm it is self-signed
purefb array list --certificate

# Install a CA-signed certificate (PEM format: certificate + intermediates + key)
purefb array update --certificate /path/to/combined.pem

# Verify the new certificate is active
purefb array list --certificate
```

Requirements:
- RSA 4096 or ECDSA P-256 key
- SAN must include the array management IP and/or FQDN
- Certificate must be trusted by the browsers and automation tools that access the array
- Set a calendar reminder 30 days before expiry for renewal

---

### 6. Disable Unused Data Protocols

Reduce the attack surface by disabling protocols that are not in use.

```bash
# Check which protocols are currently enabled on each filesystem
purefb filesystem list
# Review the 'nfs_v3', 'nfs_v4_1', and 'smb' columns

# Disable NFSv3 on a filesystem that only serves NFSv4.1 clients
purefb filesystem update \
    --name prod-ml-training-data \
    --nfs-v3-enabled false

# Disable SMB on a filesystem that is NFS-only
purefb filesystem update \
    --name prod-nfs-only \
    --smb-enabled false

# Disable S3 object store at the array level if it is not in use
# (done via the Purity//FB GUI under Settings > Array > Object Store)
```

---

### 7. Configure SNMPv3 and Disable Legacy SNMP

If SNMP monitoring is required, use SNMPv3 with `authPriv` security level (authentication + encryption). Never use SNMPv1 or SNMPv2c — they transmit credentials in plaintext.

```bash
# Check existing SNMP configuration
purefb snmp list

# Remove any existing SNMPv1 or SNMPv2c community strings
purefb snmp delete <community_name>

# Create an SNMPv3 monitoring user
purefb snmp create \
    --version v3 \
    --auth-protocol SHA \
    --auth-passphrase "<auth_pass_20_chars>" \
    --privacy-protocol AES \
    --privacy-passphrase "<priv_pass_20_chars>" \
    svc-snmp-monitor

# Configure an SNMPv3 trap destination
purefb snmp-manager create \
    --version v3 \
    --community svc-snmp-monitor \
    --host <nms_ip> \
    nms-trap-v3

# Verify — only v3 entries should be present
purefb snmp list
purefb snmp-manager list
```

---

### 8. Enable SafeMode Snapshots

SafeMode makes snapshot schedules and retention policies immutable — no local admin can delete a protected snapshot until its retention window expires. This prevents ransomware from destroying backup copies even if admin credentials are compromised.

**How to enable:** Contact Pure Storage Support. SafeMode requires Pure Support involvement to activate and cannot be enabled from the CLI alone.

Before enabling SafeMode:
- [ ] Confirm all production snapshot schedules are correct — retention windows, frequency, and replication targets
- [ ] Confirm the Purity eradication timer (default 24 hours) is set appropriately
- [ ] Brief the storage team: deleting SafeMode-protected snapshots requires Pure Support involvement

```bash
# Verify SafeMode status after enablement by Pure Support
purefb array list --safemode
```

---

### 9. Verify Encryption at Rest

Encryption at rest (XTS-AES-256) is always on and cannot be disabled. Verify it is active after initial setup:

```bash
# Verify encryption status
purefb array list --encryption

# Confirm all drives are self-encrypting
purefb drive list
# Look for encryption_enabled in the output
```

No configuration is required — encryption is hardware-enforced by the NVMe drives. If FIPS 140-2 compliance is required for the encryption implementation, confirm with the Pure account team that the installed hardware meets FIPS requirements.

---

### 10. Restrict NFS Exports to Specific Client IP Ranges

Avoid wildcard `*` NFS export rules in production. Restrict each filesystem's NFS export to the specific client subnets that require access.

```bash
# Restrict a production filesystem to the GPU cluster subnet only
purefb filesystem update \
    --name prod-ml-training-data \
    --nfs-rules "10.0.1.0/24(rw,root_squash)"

# Backup filesystem — restricted to the backup server only
purefb filesystem update \
    --name prod-veeam-daily \
    --nfs-rules "10.0.10.50/32(rw,no_root_squash)"

# Verify export rules for all filesystems — look for wildcard (*) entries
purefb filesystem list
```

**Use `root_squash` by default.** Only set `no_root_squash` for filesystems where the backup tool or application explicitly requires root access (Veeam NFS repositories, Kubernetes persistent volumes requiring root ownership).

---

### 11. Review and Restrict S3 Bucket Policies

Avoid wildcard principal grants on production S3 buckets. Apply bucket policies to explicitly enumerate allowed users and operations.

```bash
# List all S3 buckets and their current access policies
purefb bucket list
purefb bucket access-policy list

# Apply a restrictive bucket policy — allow only named users to access the bucket
purefb bucket access-policy update \
    --name prod-analytics-raw \
    --policy '{"Version":"2012-10-17","Statement":[
      {"Effect":"Allow","Principal":{"AWS":["arn:aws:iam:::user/svc-analytics/ml-platform"]},
       "Action":["s3:GetObject","s3:PutObject","s3:ListBucket"],
       "Resource":["arn:aws:s3:::prod-analytics-raw/*","arn:aws:s3:::prod-analytics-raw"]}
    ]}'
```

Verify no buckets have public access policies (`"Principal": "*"`). Any such policy on a production bucket should be treated as a security incident.

---

### 12. Configure Syslog/Audit Forwarding to SIEM

Forward audit logs to an external SIEM immediately so the log record is preserved off-array and cannot be tampered with.

```bash
# TLS syslog (preferred for integrity and confidentiality)
purefb syslog create --uri tls://siem.example.com:6514 siem-tls

# UDP syslog (fallback only)
purefb syslog create --uri udp://siem.example.com:514 siem-udp

# List configured syslog destinations
purefb syslog list
```

Verify delivery by checking the SIEM for log events from the FlashBlade management IP. Configure SIEM alerts for:
- Multiple failed login attempts from the same source IP
- API token creation or deletion outside business hours
- Filesystem permission or export rule changes
- Snapshot eradication events
- SafeMode modification attempts

---

### 13. Set Session Idle Timeout

Unattended CLI or GUI sessions with admin privileges are a security risk. Set the session idle timeout to 15 minutes.

```bash
# Set session idle timeout (minutes)
purefb array update --idle-timeout 15

# Verify
purefb array list --idle-timeout
```

This applies to both SSH (CLI) and HTTPS (GUI) sessions.

---

### 14. Audit and Disable Unused API Tokens

Service account API tokens with no expiry represent permanent credentials. Audit them at initial setup and at least quarterly.

```bash
# List all admin accounts and their API token status
purefb admin apitoken list

# Revoke a token for an account that no longer needs API access
purefb admin apitoken delete --name svc-old-integration

# Delete an account that no longer exists
purefb admin delete --name svc-decommissioned
```

---

### 15. Configure SMTP with TLS for Alert Emails

Alert emails contain operational data about the array. Use STARTTLS or SMTPS.

```bash
# Configure SMTP relay with TLS
purefb smtp update \
    --relay-host smtp.example.com \
    --relay-host-port 587 \
    --sender-domain example.com

# Add alert notification recipients
purefb alert-watcher create --email storage-team@example.com storage-team
purefb alert-watcher create --email oncall@example.com oncall

# Verify SMTP configuration
purefb smtp list

# Send a test alert to confirm delivery
purefb alert-watcher test storage-team
```

---

## Post-Hardening Verification

Run these commands after completing all hardening steps to confirm the configuration is correct:

```bash
# Array identity and status
purefb array list

# Confirm no alerts from hardening changes
purefb alert list

# Confirm AD/LDAP directory service is active
purefb directory-service list
purefb directory-service test

# Confirm syslog destinations are configured
purefb syslog list

# Confirm SNMP is v3 only — no v1/v2c communities
purefb snmp list

# Confirm NFS exports do not use wildcard source
purefb filesystem list
# Visually confirm no '*' in export rules

# Confirm SafeMode status
purefb array list --safemode

# Confirm encryption is active
purefb array list --encryption

# Confirm admin accounts and roles
purefb admin list

# Confirm API token inventory
purefb admin apitoken list

# Confirm audit log — review recent hardening actions
purefb audit list | head -30
```

Document the completion date, the engineer who performed the hardening, and the Purity//FB version at time of hardening in the array's CMDB record. Schedule a re-review at the next major Purity upgrade or 12 months, whichever comes first.

---

## See also

- [FlashBlade — Authentication](authentication/)
- [FlashBlade — Access Control](access-control/)
- [FlashBlade — Encryption](encryption/)
