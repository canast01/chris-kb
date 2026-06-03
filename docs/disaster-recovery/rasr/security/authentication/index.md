# RASR — Authentication


<div class="kb-summary">
Authentication controls for Dell Rapid Array Snapshot Recovery operations, recovery media access, and management interfaces.
</div>

## Overview

RASR (Rapid Array Snapshot Recovery) recovery operations involve several authentication boundaries that must be controlled:

- **Dell EMC storage management interfaces** — the array management plane where RASR policies are configured.
- **Recovery media and bootable environments** — access to RASR recovery USBs and PXE-boot environments.
- **Recovery session authentication** — verifying the identity of operators initiating a recovery.
- **Target system access** — authentication on the recovered system post-restore.

## Storage Array Management Authentication

RASR is managed through the Dell EMC array management interface (Unisphere, iDRAC, or OpenManage). All access to these interfaces must require strong authentication.

### Unisphere for Unity / PowerStore

```yaml
Authentication requirements:
- Minimum: local accounts with strong passwords (20+ character)
- Preferred: LDAP/AD integration with role-based access
- Required for recovery operators: "Recovery Manager" or equivalent role
- MFA: Enable for all management plane access where supported
```text
┌──────────────────────────────────────── RASR — Authentication ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 RASR — Authentication Methods                                 │   │
│   │         Vault operator role; 2-person integrity for unlock; AD integration for PPDM UI        │   │
│   │               Management UI: HTTPS on 443 (PPDM REST API) — browser-based login               │   │
│   │               API: bearer token or service account; rotate credentials quarterly              │   │
│   │                 Inter-component: certificate-based mutual TLS between engines                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Human Access                 │  │                Machine Access               │   │
│   │            AD / LDAP integration             │  │               Service account               │   │
│   │              SAML SSO optional               │  │               API key / token               │   │
│   │                 MFA via IdP                  │  │               Certificate auth              │   │
│   │            Session timeout 15 min            │  │              Rotate every 90 d              │   │
│   │              Audit login events              │  │             Vault-stored secrets            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Recovery Media Authentication

RASR recovery media (USB drives, ISO images, PXE boot images) must be protected from unauthorised use. An attacker with access to recovery media can potentially restore systems to a compromised state or access snapshot data.

### Physical Media Controls

| Control | Implementation |
|---|---|
| Recovery USB inventory | Serial number tracked in CMDB; checked out via change management |
| Physical storage | Recovery USB drives stored in locked cabinet with key log |
| USB labelling | Clearly labelled with system/environment scope and creation date |
| Media access log | Sign-out sheet or electronic access log (who, when, why) |
| Media destruction | Cryptographic wipe (3-pass DoD or shred) before disposal |

### BIOS/UEFI Boot Authentication

Recovery from bootable RASR media requires BIOS/UEFI boot. Protect this path:

```yaml
BIOS/UEFI hardening:
- Set UEFI administrator password to prevent boot order changes
- Restrict boot order to internal drive; allow USB/PXE only when authorised
- Enable Secure Boot (verify recovery media is Secure Boot compatible)
- Log BIOS access attempts via iDRAC
- Require iDRAC credentials to enable one-time boot to USB/PXE
```

```bash
# Racadm — configure one-time boot to virtual media (requires authentication)
racadm set iDRAC.ServerBoot.BootOnce 1
racadm set iDRAC.ServerBoot.FirstBootDevice VCD-DVD

# This requires valid iDRAC credentials — prevents unauthorised recovery boot
```

## Recovery Session Authentication

When a RASR recovery is initiated, the process must require multi-party authentication for production systems.

### Four-Eyes / Dual-Control Procedure

```text
Recovery authorisation workflow:
1. Recovery requester raises a change record (ServiceNow / Jira)
2. Change is approved by the system owner or DR manager
3. Recovery is initiated by a separate operator (not the requester)
4. Both parties authenticate to the array management plane during the session
5. Recovery actions are logged (see audit/hardening page)
```

### Service Account for Automated RASR Operations

```yaml
Automated RASR tasks (e.g., scheduled snapshot validation) use dedicated service accounts:
- One service account per environment (prod, UAT, DR)
- Minimum privilege: snapshot read and recovery initiation only
- Password stored in a privileged access management (PAM) vault (CyberArk / HashiCorp Vault)
- No interactive login permitted (shell: /sbin/nologin on Linux management hosts)
- Credentials rotated every 90 days
```

```bash
# Example: Store RASR service account credentials in HashiCorp Vault
vault kv put secret/rasr/prod \
  username="svc-rasr-prod" \
  password="$(openssl rand -base64 32)"

# Retrieve at runtime (never in scripts or config files)
RASR_PASSWORD=$(vault kv get -field=password secret/rasr/prod)
```

## Post-Recovery System Authentication

After a RASR recovery completes, verify the recovered system's authentication configuration before returning it to production.

```bash
# Linux — verify SSH host keys have been regenerated (not restored from snapshot)
ls -la /etc/ssh/ssh_host_*
# If keys are identical to the pre-restore state, regenerate:
rm /etc/ssh/ssh_host_*
ssh-keygen -A
systemctl restart sshd

# Verify SSSD is connected to AD after restore
systemctl status sssd
realm list
id domain_admin_user@corp.local

# Reset cached Kerberos tickets
kdestroy -A   # Clear all credential caches

# Verify no local accounts were added during the rollback period that need review
awk -F: '$3 >= 1000 { print $1, $3 }' /etc/passwd
lastlog | grep -v "Never logged in"
```

```powershell
# Windows — verify AD domain secure channel after restore
Test-ComputerSecureChannel
# If broken:
Test-ComputerSecureChannel -Repair -Credential (Get-Credential)

# Check local administrator account status post-restore
Get-LocalUser | Select-Object Name, Enabled, LastLogon

# Verify LAPS has rotated the local admin password post-recovery
Get-LapsADPassword -Identity $env:COMPUTERNAME -AsPlainText

# Clear cached credentials
cmdkey /list
cmdkey /delete:targetname
```

## Authentication Audit Checklist

| Check | Verification |
|---|---|
| Array management uses AD auth | `uemcli /sys/auth/ldap show` returns active config |
| iDRAC default creds changed | Login with default `root/calvin` fails |
| iDRAC uses AD groups | LDAP roles assigned, test login with AD account |
| Recovery USB sign-out logged | Physical log reviewed at end of each recovery |
| Change record approved before recovery | Change ticket in "Approved" state prior to action |
| Service account in PAM vault | CyberArk / Vault shows current svc-rasr account |
| SSH host keys regenerated post-restore | `ssh-keyscan` from monitoring host shows changed key |
| AD secure channel intact | `Test-ComputerSecureChannel` returns True |

## Quick Reference

| Topic | Action / Tool |
|---|---|
| Array management auth | Unisphere LDAP settings; `uemcli /sys/auth/ldap show` |
| iDRAC AD integration | `racadm set iDRAC.ActiveDirectory.Enable 1` |
| iDRAC session timeout | `racadm set iDRAC.WebServer.Timeout 900` |
| One-time boot via iDRAC | `racadm set iDRAC.ServerBoot.BootOnce 1` |
| PAM vault for service accounts | CyberArk Safe or HashiCorp Vault |
| Post-restore SSH keys | `rm /etc/ssh/ssh_host_* && ssh-keygen -A` |
| Post-restore AD channel | `Test-ComputerSecureChannel -Repair` |
| LAPS post-restore | `Get-LapsADPassword -Identity <computer>` |
---

## Related Reference

- [Standard LDAP Integration](../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
