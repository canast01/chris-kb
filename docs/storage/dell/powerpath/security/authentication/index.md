# PowerPath — Authentication

## Overview

```mermaid
graph TD
    adminUser(["Storage Admin\nor Automation Account"])

    subgraph "Linux Host"
        ssh["SSH (key-based auth)\nPAM / SSSD → AD"]
        sudo["sudo → /usr/sbin/powermt\n(sudoers.d/powerpath)"]
        svcAccount["Service Account\n(restricted sudo — display only)"]
        ssh --> sudo
        ssh --> svcAccount
    end

    subgraph "Windows Host"
        winAuth["Windows Auth\n(Kerberos / NTLM)"]
        localAdm["Local Administrators group\n(required for powermt)"]
        jea["JEA Role Capability\n(optional: limit to display commands)"]
        winAuth --> localAdm
        localAdm --> jea
    end

    adminUser --> ssh
    adminUser --> winAuth
    sudo -->|"powermt set / save / config"| ppCLI["powermt CLI"]
    svcAccount -->|"powermt display only"| ppCLI
    jea -->|"constrained commands"| ppCLI
```

PowerPath does not implement its own authentication system. There is no PowerPath-native login, user database, or session management. Access to `powermt` CLI commands is controlled entirely by the host operating system's authentication and authorisation mechanisms.

This design means PowerPath security is inherited from the host OS security posture. Any account with sufficient OS privilege can run any `powermt` command — there is no additional PowerPath credential check.

---

## Linux Authentication

On Linux, all `powermt` commands that modify configuration require root privileges. Read-only display commands (`powermt display`) may or may not require root depending on the PowerPath version and kernel configuration.

### Root Access

The simplest and least secure model: operations staff SSH to the host as root and run `powermt` directly. Acceptable only in environments with full SSH key control and no shared root passwords.

```bash
# Direct root access
ssh root@db-prod-01
powermt display dev=all
powermt set policy=CLAROpt class=all
powermt save
```

### Sudo-Based Access (Recommended)

The recommended model for Linux: create a named storage administration account and grant it sudo access only to specific `powermt` commands. This provides auditability (sudo logs the caller's real username) while restricting blast radius.

**Sudoers configuration for a storage admin account:**

```bash
# /etc/sudoers.d/powerpath
# Storage admin — full powermt access
svc-storage ALL=(root) NOPASSWD: /usr/sbin/powermt
```

This grants the `svc-storage` account the ability to run any `powermt` subcommand. If tighter restriction is needed, specify individual commands:

```bash
# /etc/sudoers.d/powerpath-monitoring
# Read-only monitoring account — display and registration check only
svc-monitoring ALL=(root) NOPASSWD: \
    /usr/sbin/powermt display dev=all, \
    /usr/sbin/powermt display ports class=all, \
    /usr/sbin/powermt display options, \
    /usr/sbin/powermt check_registration, \
    /usr/sbin/powermt version
```

Validate the sudoers file syntax before applying:

```bash
visudo -c -f /etc/sudoers.d/powerpath-monitoring
```

### PAM Integration

PowerPath itself does not integrate with PAM. Host SSH authentication via PAM (including LDAP, Active Directory via SSSD, or MFA via PAM RADIUS) applies normally — PAM controls who can log into the host; once logged in, sudo controls what they can run.

For environments with Active Directory integration on Linux:

```bash
# Confirm the storage admin AD group resolves on the host
id svc-storage
getent group storage-admins

# Grant the AD group sudo access to powermt
# /etc/sudoers.d/powerpath-ad
%storage-admins ALL=(root) NOPASSWD: /usr/sbin/powermt
```

### SSH Key Management

Hosts running PowerPath should enforce SSH key authentication and disable password-based SSH login for root:

```bash
# /etc/ssh/sshd_config
PermitRootLogin prohibit-password
PasswordAuthentication no
```

This ensures that interactive root access requires a managed SSH key, reducing the risk of credential-based attacks on hosts with privileged PowerPath access.

---

## Windows Authentication

On Windows Server, PowerPath installs as a system service and filter driver. The `powermt` command requires Local Administrator rights. There is no finer-grained Windows permission model for PowerPath — it is binary: Local Administrator or no access.

### Local Administrator Groups

```powershell
# Confirm account is in the local Administrators group
Get-LocalGroupMember -Group "Administrators"

# Add a service account to local Administrators (requires existing admin rights)
Add-LocalGroupMember -Group "Administrators" -Member "DOMAIN\svc-storage"
```

### Windows Remote Management (WinRM)

For remote PowerPath management on Windows, WinRM with constrained language mode or PowerShell JEA (Just Enough Administration) can be configured to restrict which `powermt` commands a delegated account can run remotely:

```powershell
# Example JEA configuration — restrict to display commands only
# In a JEA role capability file (.psrc):
VisibleExternalCommands = 'powermt display dev=all', 'powermt check_registration'
```

### Active Directory Integration

Windows Server hosts joined to Active Directory authenticate via Kerberos. Grant the relevant AD security group Local Administrator membership on PowerPath hosts via Group Policy:

```text
Computer Configuration > Policies > Windows Settings >
Security Settings > Restricted Groups >
Add DOMAIN\Storage-Admins to local Administrators
```

---

## AIX Authentication

On IBM AIX, `powermt` requires root access. AIX RBAC (Role-Based Access Control) can be used to grant the `powermt` command to a non-root user:

```bash
# Create a custom role for PowerPath operations
mkrole rolelist=powerpath_admin

# Assign the powermt binary to the role
# Edit /etc/security/roles to include command access

# Assign the role to a user
chuser roles=powerpath_admin storage_admin_user
```

For most AIX environments, the simpler approach is a named shared account in the `system` group that is permitted to run `powermt`, with sudo configured via the IBM AIX sudo package.

---

## Automation and Service Accounts

When PowerPath monitoring or automation scripts run `powermt` commands, use a dedicated service account rather than a shared root password or personal admin account.

Principles for automation service accounts:

1. **Least privilege**: Grant only the `powermt` subcommands the automation actually needs. Monitoring scripts typically need only `display` and `check_registration` — not `set`, `save`, or `config`.
2. **No interactive login**: Disable interactive shell login for the service account; only sudo-based command execution should be permitted.
3. **SSH key authentication**: Use a unique, passphrase-protected SSH key for each automation system. Rotate annually.
4. **Audit trail**: Ensure all `powermt` commands run by the service account are logged via sudo (`/var/log/secure` on RHEL/OEL, `/var/log/auth.log` on Debian/Ubuntu).

```bash
# Example: monitoring service account with restricted sudo
# /etc/sudoers.d/powerpath-svc-monitor

Defaults:svc-monitor !requiretty
svc-monitor ALL=(root) NOPASSWD: /usr/sbin/powermt display dev=all
svc-monitor ALL=(root) NOPASSWD: /usr/sbin/powermt display ports class=all
svc-monitor ALL=(root) NOPASSWD: /usr/sbin/powermt check_registration
svc-monitor ALL=(root) NOPASSWD: /usr/sbin/powermt display options
```

---

## Audit Trail

PowerPath does not write its own audit log. Administrative actions (`powermt set`, `powermt save`, `powermt config`, `powermt remove`) are only traceable through:

- **sudo logs** (Linux): `/var/log/secure` or `/var/log/auth.log` — records who ran which `powermt` command via sudo, including timestamp and originating user
- **Shell history**: If admins run `powermt` as root, the command will appear in the root shell history (`/root/.bash_history`) — unreliable unless audited centrally
- **Windows Event Log**: `powermt` executions on Windows are not specifically logged by PowerPath; rely on Windows process creation auditing (Security Event ID 4688) if process-level audit is required
- **Centralised logging**: Forward sudo logs and Windows Event Log to a SIEM for retention and alerting on privileged PowerPath operations

For change management compliance, document every `powermt set` and `powermt save` operation in the associated change record, including the before/after output of `powermt display options`.

---

## PowerPath Management Suite (PPMS) Authentication

Dell PowerPath Management Suite is the optional centralised management platform for PowerPath-managed hosts. PPMS has its own authentication layer, separate from host OS authentication:

- PPMS uses local accounts and optionally integrates with LDAP/Active Directory for SSO
- Role-based access within PPMS: Administrator, Operator, and Read-Only roles map to full management, limited change, and view-only access respectively
- PPMS API access uses token-based authentication; tokens are scoped per role
- For environments using PPMS, direct `powermt` command access on individual hosts should be restricted to break-glass scenarios

Refer to the Dell PowerPath Management Suite Installation and Administration Guide for PPMS-specific authentication configuration.

---

## Quick Reference

| Platform | Authentication Mechanism | Minimum Required Privilege |
|---|---|---|
| Linux | Root or sudo | Root (or sudo to powermt) |
| Windows Server | Windows authentication | Local Administrator |
| AIX | Root or AIX RBAC | Root (or RBAC role with powermt) |
| HP-UX | Root | Root |
| Solaris | Root or RBAC | Root (or RBAC profile) |
| PowerPath/VE (ESXi) | vSphere authentication | vSphere Administrator or Storage Administrator role |
| PPMS | Local account or LDAP/AD | PPMS Administrator role |
