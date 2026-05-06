# CyberArk Integration

CyberArk integrates with AD, MFA, ticketing, VMware, Linux, and automation tooling to enforce privileged access controls across all platforms. AD group membership drives safe entitlements without requiring manual PVWA user management.

---

## Integration Overview

| Integration | Method | Notes |
|---|---|---|
| Active Directory (LDAP) | LDAP bind from PVWA | User authentication and group-based safe membership |
| MFA (RSA / Duo) | RADIUS from PVWA | Enforced at logon; configured in PVWA Authentication settings |
| Syslog / SIEM (Splunk) | Syslog from Vault and PVWA | Vault audit events forwarded to Splunk |
| ServiceNow | REST API ticket validation | Dual-control requests validated against open change/ticket |
| vCenter | CyberArk vCenter plugin / CPM platform | vCenter accounts managed; rotation via CPM |
| Linux SSH | PSMP or CPM SSH key rotation | Root and privileged Linux accounts managed |
| Ansible | `cyberark.pas` Ansible collection | Retrieve credentials at playbook runtime |
| Terraform | CyberArk Terraform provider | Manage safes, accounts, platforms as code |
| CyberArk EPM | Agent on endpoints | Least-privilege for workstations; integrated with PAM |

---

## Active Directory / LDAP Integration

PVWA authenticates users against AD and uses AD group membership to determine safe access.

Configuration in PVWA (Administration > LDAP Integration):

```
LDAP Host:   ldaps://dc01.corp.example.com:636
Base DN:     DC=corp,DC=example,DC=com
Bind DN:     CN=svc-cyberark-ldap,OU=Service Accounts,OU=Managed,DC=corp,DC=example,DC=com
Bind Pwd:    <managed by CyberArk itself in the Vault>
```

AD groups mapped to Vault access:
- `GG_CyberArk_Auditors` → Auditors role (read-only access to all safes)
- `GG_CyberArk_SafeOwners` → Safe Owner role (manage assigned safes)
- `GG_CyberArk_VaultAdmins` → Vault Admins (full administrative rights)

```powershell
# Test LDAPS connectivity from PVWA server
Test-NetConnection -ComputerName dc01.corp.example.com -Port 636

# Verify LDAP bind and group membership query
$ldap = New-Object DirectoryServices.DirectoryEntry(
    "LDAP://dc01.corp.example.com:636",
    "svc-cyberark-ldap@corp.example.com",
    "password"
)
$ldap.Path
```

---

## MFA Integration (Duo / RSA)

PVWA supports RADIUS-based MFA enforcement at logon. All privileged user logons require MFA.

PVWA RADIUS configuration (Administration > Authentication Methods > RADIUS):
- RADIUS server: `duo-proxy.corp.example.com` port 1812
- Shared secret: stored in CyberArk safe `CyberArk-Platform-Accounts`
- Timeout: 60 seconds
- Retries: 2

For Duo Security, the Duo Authentication Proxy must be deployed on-premises and configured with the PVWA's RADIUS secret.

---

## VMware vCenter Integration

CyberArk manages vCenter service accounts and administrator credentials via the VMware vSphere plugin for CPM.

1. Install the vSphere CPM plugin on the CPM server (from CyberArk Marketplace).
2. Create a Platform in PVWA for `VMware-vCenter` using the plugin.
3. Onboard vCenter accounts to the appropriate safe.
4. CPM will rotate the password and update vCenter via the vSphere API.

```powershell
# Onboard a vCenter account
Add-PASAccount `
    -userName "svc-cyberark-vcenter" `
    -address  "vcenter01.corp.example.com" `
    -accountName "vcenter01-svc-cyberark" `
    -platformID "VMware-vCenter" `
    -SafeName "VMware-vCenter-Accounts" `
    -secret (ConvertTo-SecureString "InitialPassword!" -AsPlainText -Force) `
    -automaticManagementEnabled $true
```

Session recording for vCenter: PSM for Web is used to proxy browser-based vSphere Client sessions. No credential is exposed to the user.

---

## Linux SSH Key Rotation

CyberArk manages SSH private keys for privileged Linux accounts. CPM rotates keys by generating a new key pair, placing the public key on the target host, and storing the private key in the Vault.

1. Deploy the SSH Key Manager CPM plugin.
2. Create a platform for `Unix-SSH-Key` in PVWA.
3. Onboard the account with `sshKey` secret type.
4. CPM connects via SSH (as the account itself or via sudo) to rotate the `authorized_keys` entry.

```bash
# Verify CyberArk public key is in place after rotation
grep "CyberArk" /home/root/.ssh/authorized_keys

# Ensure sshd allows key-based auth and CyberArk's CPM source IP
cat /etc/ssh/sshd_config | grep -E "AuthorizedKeysFile|PubkeyAuthentication"
```

---

## Ansible Integration

The `cyberark.pas` Ansible collection retrieves credentials from the Vault at playbook runtime. No secrets are stored in Ansible inventory, vars files, or Ansible Tower/AWX credentials for managed accounts.

```yaml
# playbook example: retrieve a password at runtime
- name: Retrieve DB password from CyberArk
  cyberark.pas.cyberark_credential:
    api_base_url: "https://pvwa.corp.example.com"
    app_id: "Ansible-Automation"
    query: "Safe=APP-DB01-Accounts;Folder=Root;Object=db01-svc-app01"
    connection_timeout: 30
  register: cyberark_result
  no_log: true

- name: Use the retrieved credential
  community.mysql.mysql_db:
    login_user: "svc-app01"
    login_password: "{{ cyberark_result.result.Content }}"
    name: appdb
    state: present
```

The Ansible `app_id` must be defined in CyberArk Application Access Manager (AAM) with the Ansible Tower/AWX host IP as an allowed machine.

---

## Terraform Integration

```hcl
# Retrieve a CyberArk secret in Terraform
provider "cyberark" {
  tenant    = "corp"
  client_id = var.cyberark_client_id
  client_secret = var.cyberark_client_secret
}

data "cyberark_secret" "db_password" {
  name     = "db01-svc-app01"
  safe_name = "APP-DB01-Accounts"
}

resource "aws_db_instance" "app_db" {
  password = data.cyberark_secret.db_password.value
  # other config...
}
```

---

## SIEM (Splunk) Integration

The Vault and PVWA forward audit events to Splunk via syslog.

Vault syslog configuration (`DBPARM.ini` on Vault server):

```ini
[SYSLOG]
SyslogServerIP     = 10.10.10.200
SyslogServerPort   = 514
SyslogServerProtocol = UDP
SyslogTranslatorFile = Syslog.xsl
```

Key audit event types to monitor in Splunk:
- `CPM Password Change` — credential rotation events
- `Get Password` — credential retrievals (who accessed what)
- `PSM Session Start/End` — privileged session tracking
- `Safe Member Added/Removed` — entitlement changes
- `Logon/Logoff` — PVWA authentication events
