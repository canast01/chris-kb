---
tags:
  - netapp
  - security
---
# SnapCenter — Authentication


<div class="kb-summary">
Part of the [SnapCenter Security](index.md) reference.

*Applies to: SnapCenter 5.x*
</div>
```text
┌───────────────────────────────── NetApp SnapCenter — Authentication ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        SnapCenter authentication: local accounts, LDAP/AD, RADIUS, and SAML SSO options       │   │
│   │        MFA: time-based OTP or hardware token required for all privileged admin accounts       │   │
│   │         Service accounts: dedicated accounts for automation; API tokens/keys preferred        │   │
│   │       Session: idle timeout enforced; concurrent session limits for admin role accounts       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Login → authenticate LDAP/SAML/local → MFA → authorise role → session                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Server           │  │          Windows VM         │  │       Central control       │   │
│   │           Plug-in           │  │          Host agent         │  │        App-consistent       │   │
│   │            Policy           │  │       Schedule/retain       │  │         Backup rule         │   │
│   │        Resource group       │  │       Grouped targets       │  │        Shared policy        │   │
│   │           Recovery          │  │       Volume/LUN/file       │  │       Granular restore      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Method      │     Use case     │  Config location  │       MFA        │     Priority     │   │
│   │     LDAP/AD      │  Staff accounts  │   Auth settings   │     Required     │     Primary      │   │
│   │     SAML SSO     │    Federated     │    SSO settings   │   IdP-enforced   │    Preferred     │   │
│   │      Local       │   Break-glass    │    Local users    │     Required     │  Emergency only  │   │
│   │    API token     │    Automation    │  Service account  │   N/A (token)    │    Automation    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SnapCenter Server (Windows) · ONTAP clusters · plug-in hosts · application servers       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapCenter         = NetApp backup orchestration; coordinates app-consistent snapshots via plug-ins│
│    Plug-in            = host-side agent; quiesces application before snapshot: SQL, Oracle, VMware    │
│    Resource group     = set of resources sharing a backup policy and schedule in SnapCenter           │
│    Policy             = SnapCenter object defining snapshot frequency, retention, and replication t...│
│    App-consistent     = snapshot taken after DB quiesce; guarantees crash-consistent recovery         │
│    Clone lifecycle    = SnapCenter clone: create from snapshot, provision to host, then delete        │
│    FlexClone          = underlying ONTAP technology; SnapCenter clone maps to an ONTAP FlexClone      │
│    Vault policy       = SnapCenter policy that also replicates snapshots to SnapVault destination     │
│    Mirror policy      = SnapCenter policy that replicates snapshots via SnapMirror to DR cluster      │
│    RBAC               = SnapCenter role-based access; Admin, Backup Operator, Restore Operator roles  │
│    SMF                = SnapCenter MySQL database storing job history, policies, and resource configs │
│    SnapCenter API     = REST API on port 8143; full feature coverage for automation workflows         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Authentication Methods

SnapCenter supports three authentication methods for the GUI and API:

| Method | Description | Recommended For |
|---|---|---|
| Local accounts | Accounts managed within the SnapCenter database | Break-glass admin account only |
| Active Directory accounts | Domain accounts authenticated via AD; groups supported | All operational users |
| SAML 2.0 / MFA | IdP-integrated SSO with MFA; SnapCenter 6.0+ | Production deployments with IdP available |

The default `admin` account is a local account created at installation. Change its password immediately post-install and store in a secrets vault. For day-to-day operations, use AD accounts or SAML SSO.

---

## Active Directory Integration

SnapCenter integrates with Active Directory for user authentication and group-based RBAC. Configure AD integration in Settings → Global Settings → Active Directory.

```powershell
# Connect to SnapCenter via PowerShell
Open-SmConnection -SMSbaseurl https://snapcenter.example.com

# Add an AD user with a specific SnapCenter role
Add-SmUser -UserName "CORP\jsmith" -RoleName "Application Backup and Clone Admin"

# Add an AD group (all group members inherit the role)
Add-SmUser -UserName "CORP\SnapCenter-Admins" -RoleName "SnapCenter Admin"
Add-SmUser -UserName "CORP\DBA-Team" -RoleName "Application Backup and Clone Admin"
Add-SmUser -UserName "CORP\Backup-Viewers" -RoleName "Backup and Clone Viewer"

# List all users and their assigned roles
Get-SmUser | Select-Object UserName, RoleName, IsActive

# Remove an AD user from SnapCenter
Remove-SmUser -UserName "CORP\jsmith"
```

### AD Authentication Troubleshooting

```powershell
# Verify the AD domain is reachable from the SnapCenter Server
# (run on the SnapCenter Server Windows host)
Test-ComputerSecureChannel -Server corp.example.com -Verbose

# Test AD user authentication
Test-Path "AD:CN=jsmith,OU=Users,DC=corp,DC=example,DC=com"

# Check SnapCenter logs for AD authentication errors
# Log location on SnapCenter Server:
# C:\Program Files\NetApp\SnapCenter\SnapCenter Web App\log\
# Look for LDAP or Kerberos errors
```

---

## SAML 2.0 / MFA Integration (SnapCenter 6.0+)

SAML 2.0 SSO integration delegates authentication to an external IdP (Active Directory Federation Services, Okta, Azure AD, or any SAML 2.0-compliant IdP). Users authenticate to SnapCenter using their IdP credentials, enabling MFA enforcement at the IdP level.

### Configure SAML in SnapCenter

1. Navigate to **Settings → Global Settings → Authentication**
2. Select **SAML Authentication** and click **Configure**
3. Download the SnapCenter service provider metadata XML
4. Register SnapCenter as a SAML application in your IdP using the SP metadata
5. Copy the IdP metadata URL or XML from the IdP into SnapCenter
6. Save and test a SAML login

### ADFS Configuration Steps

```powershell
# On the ADFS server — add SnapCenter as a Relying Party Trust
# (requires ADFS admin access)

# 1. In ADFS Management, right-click "Relying Party Trusts" → Add Relying Party Trust
# 2. Select "Import data about the relying party from a file"
# 3. Upload the SnapCenter SP metadata XML downloaded from SnapCenter

# After adding the Relying Party Trust, configure claim rules to pass
# the UPN or SAMAccountName attribute as the NameID claim

# Example claim rule (Issuance Transform Rules):
# Rule type: Send LDAP Attributes as Claims
# Attribute store: Active Directory
# LDAP Attribute: User-Principal-Name
# Outgoing Claim Type: Name ID
```

### SAML Operational Notes

- After SAML is enabled, the local `admin` account retains password-based access as a fallback — this is the break-glass account
- User roles in SnapCenter are still assigned via `Add-SmUser` even when SAML is the authentication method — the IdP handles authentication, SnapCenter handles authorisation
- If the IdP is unavailable, SAML authentication fails; users must use the local `admin` break-glass account until the IdP is restored

---

## Service Account Authentication — ONTAP

SnapCenter connects to ONTAP storage systems using credentials stored in the SnapCenter Credential Store. These credentials are used for all API calls to create snapshots, manage SnapMirror, and access LUN mappings.

### Credential Store Management

```powershell
# Add ONTAP credentials to the SnapCenter Credential Store
Add-SmCredential \
    -Name "ontap-svc-snapcenter" \
    -AuthMode UseWindowsCredentials:$false \
    -UserName svc-snapcenter \
    -Password (ConvertTo-SecureString "password" -AsPlainText -Force)

# List all credentials stored in SnapCenter
Get-SmCredential | Select-Object Name, UserName, AuthMode

# Update a credential (e.g., after password rotation)
Set-SmCredential \
    -Name "ontap-svc-snapcenter" \
    -Password (ConvertTo-SecureString "new-password" -AsPlainText -Force)
```

### Best Practices for ONTAP Service Account

- Use a dedicated ONTAP account (`svc-snapcenter`) with a custom least-privilege RBAC role — see the [Access Control](access-control/index.md) page for the recommended ONTAP role definition
- Do not use personal admin accounts or the built-in `admin` account for ONTAP connections in SnapCenter
- Rotate the ONTAP service account password at least annually or when personnel change; update the credential in SnapCenter Credential Store after each rotation
- If the ONTAP account is an AD-integrated ONTAP account, ensure the AD account follows the same lifecycle as the SnapCenter SAML accounts

---

## Plugin Host Authentication

SnapCenter agents on protected hosts authenticate using OS-level credentials stored in the SnapCenter Credential Store. The SnapCenter Server pushes plugin installers and executes pre/post scripts on the host using these credentials.

```powershell
# Add Windows host credentials
Add-SmCredential \
    -Name "win-host-admin" \
    -AuthMode UseWindowsCredentials \
    -UserName "CORP\snapcenter-svc" \
    -Password (ConvertTo-SecureString "password" -AsPlainText -Force)

# Add Linux host credentials (used for Oracle, SAP HANA, UNIX plugin hosts)
Add-SmCredential \
    -Name "linux-host-root" \
    -AuthMode UseSudoCredentials \
    -UserName root \
    -Password (ConvertTo-SecureString "password" -AsPlainText -Force)

# Assign credentials to a host when adding it to SnapCenter
Add-SmHost \
    -HostName dbhost01.corp.example.com \
    -HostType Windows \
    -Credential "win-host-admin" \
    -PluginCode SCW
```

### Linux Host sudo Configuration

For Linux plugin hosts, the SnapCenter agent typically runs as a non-root user with sudo access for specific commands. Configure `/etc/sudoers` on each Linux plugin host:

```bash
# /etc/sudoers — allow the SnapCenter plugin user to run required commands without a password prompt
# Add this entry using visudo — do not edit /etc/sudoers directly

snapcenter ALL=(ALL) NOPASSWD: /bin/mount, /bin/umount, /sbin/multipath, \
    /sbin/fdisk, /usr/sbin/dmsetup, /opt/NetApp/snapcenter/spl/bin/*

# Verify the sudoers entry is valid
sudo -l -U snapcenter
```

---

## Session and Token Management

SnapCenter REST API authentication uses tokens with a configurable session lifetime. Tokens expire after inactivity to limit the exposure window.

```bash
# Obtain an API token
curl -sk -X POST "https://snapcenter.example.com/api/4.9/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
        "UserOperationContext": {
            "User": {
                "Name": "admin",
                "Passphrase": "<password>",
                "Rolename": "SnapCenter Admin"
            }
        }
    }' | python3 -m json.tool
# Returns: { "Token": "..." }

# Use the token in subsequent API calls
TOKEN="<token-from-login>"
curl -sk -X GET "https://snapcenter.example.com/api/4.9/resourcegroups" \
    -H "token: $TOKEN" | python3 -m json.tool

# Logout — invalidate the token
curl -sk -X POST "https://snapcenter.example.com/api/4.9/auth/logout" \
    -H "token: $TOKEN"
```

For automation scripts, always log out at the end of the script to invalidate the token. Do not hardcode credentials in scripts — retrieve them from a secrets vault at runtime.
---

## Related Reference

- [Standard LDAP Integration](../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements

---

## See also

- [Snapcenter — Access Control](access-control/)
- [Snapcenter — Hardening](hardening/)
- [Snapcenter — Encryption](encryption/)
