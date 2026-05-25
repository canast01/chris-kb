# vSAN — Authentication

vSAN does not have its own authentication system. All access to vSAN management functions is authenticated through vCenter Server, which in turn delegates identity verification to the vSphere SSO domain and configured identity sources.

---

## Authentication Stack

```text
User / Automation Client
        │
        ▼
vCenter Server (HTTPS/443)
        │
        ▼
vSphere SSO (Platform Services Controller embedded in VCSA)
        │
        ├── vsphere.local (built-in SSO domain)
        └── External Identity Source
                ├── Active Directory (LDAP / Integrated Windows Auth)
                └── OpenLDAP
```

```mermaid
sequenceDiagram
    participant client as User / Automation
    participant vc as vCenter (HTTPS/443)
    participant sso as vSphere SSO
    participant ad as Active Directory (LDAP/636)

    client->>vc: Login request
    vc->>sso: Authenticate user
    sso->>ad: LDAP bind + user lookup
    ad-->>sso: User attributes & groups
    sso-->>vc: SAML token (signed)
    vc-->>client: Session established

    Note over client,ad: vSAN operations then checked\nagainst vCenter RBAC at cluster scope
```

vSAN-specific operations — creating disk groups, modifying storage policies, enabling encryption — all require authentication to vCenter. No separate vSAN credentials exist.

---

## Identity Sources

### vSphere SSO Built-in Domain (vsphere.local)

The embedded SSO domain (`vsphere.local`) exists by default on every VCSA deployment. It contains:

- `administrator@vsphere.local` — the initial super-administrator account.
- Service accounts used by vSphere internal components.

**Use of `vsphere.local` accounts in production:**

- `administrator@vsphere.local` should be used only for break-glass access and initial configuration.
- All routine vSAN administration should use named accounts from an external identity source.
- Create a minimum set of service accounts in `vsphere.local` for automation that cannot use AD (e.g., monitoring agents, backup integration).

### Active Directory Integration

Integrate vCenter SSO with Active Directory to allow domain users to authenticate against vCenter.

**Configure AD identity source:**

vSphere Client → vCenter → Administration → Single Sign-On → Configuration → Identity Sources → Add

| Field | Value |
|---|---|
| Identity Source Type | Active Directory (Integrated Windows Authentication) or Active Directory as LDAP Server |
| Domain Name | `example.com` |
| Base DN for users | `OU=vSphere Admins,DC=example,DC=com` |
| Base DN for groups | `OU=vSphere Groups,DC=example,DC=com` |
| Domain alias | `EXAMPLE` |

**Integrated Windows Authentication** (recommended): Uses the machine account of the VCSA joined to the domain. Requires VCSA to be domain-joined.

**LDAP bind account** (alternative): Uses a dedicated service account with read-only access to the AD directory.

```bash
# Join VCSA to Active Directory domain (from VCSA shell)
/opt/likewise/bin/domainjoin-cli join example.com Administrator
# Reboot VCSA after domain join
reboot
```

**Post-join verification:**

```bash
/opt/likewise/bin/lwsm status
# lsass service should be running
```

**Add AD groups to vCenter permissions after joining:**

vSphere Client → vCenter → Permissions → Add → select identity source → search AD group → assign role

### Multi-Factor Authentication

vCenter SSO supports SAML-based MFA through external identity providers:

- **ADFS with MFA policies:** Configure AD FS as a SAML 2.0 identity provider in vCenter SSO.
- **Okta / Azure AD (Entra ID):** Configure as SAML IdP — supported from vSphere 7.0 U2 onward.
- **RSA SecurID:** Available as a Smart Card / CAC integration or via ADFS relay.

**Configure external IdP (vSphere 7.0+):**

vSphere Client → vCenter → Administration → Single Sign-On → Configuration → Identity Provider → Change to ADFS / external

Note: When an external IdP is configured, the vsphere.local domain remains available for break-glass access via the direct SSO login page at `https://vcenter/ui/`.

---

## Service Accounts

### Principles

- Use dedicated service accounts for each integration (backup, monitoring, automation).
- Assign the minimum required vCenter role to each service account.
- Do not share service account credentials between systems.
- Rotate service account passwords on a defined schedule (90 days recommended, or per policy).
- Store credentials in a secrets manager (HashiCorp Vault, CyberArk, Azure Key Vault) rather than configuration files.

### Recommended Service Accounts

| Account | Purpose | Required Role |
|---|---|---|
| `svc-veeam-vcenter` | Veeam backup integration | Veeam-defined custom role (backup operator) |
| `svc-aria-vcenter` | Aria Operations monitoring | Read Only + vSAN performance access |
| `svc-ansible-vcenter` | Ansible automation | Custom role with required task permissions |
| `svc-vlcm-agent` | vLCM hardware manager | Administrator (restricted to cluster scope) |

### Create a Least-Privilege Monitoring Account

```powershell
Connect-VIServer <vcenter>

# Create a read-only role with vSAN performance access
$permissions = @(
    "System.Anonymous", "System.Read", "System.View",
    "Global.VCServer",
    "Performance.ModifyIntervals",
    "VirtualMachine.State.CreateSnapshot"  # required for Veeam-style tools
)

New-VIRole -Name "vSAN-Monitor-RO" -Privilege (Get-VIPrivilege -Id $permissions)

# Assign the role to the monitoring service account on the cluster
$principal = "EXAMPLE\svc-aria-vcenter"
Set-VIPermission -Entity (Get-Cluster "VSAN-LON-01") `
                 -Principal $principal `
                 -Role "vSAN-Monitor-RO" `
                 -Propagate $true
```

---

## Session and Token Management

### vCenter Session Tokens

vCenter issues session tokens after successful SSO authentication. Default session settings:

| Setting | Default | Recommendation |
|---|---|---|
| Session timeout | 30 minutes (inactivity) | Keep at 30 minutes or reduce to 15 minutes for privileged roles |
| Max login attempts before lockout | Not limited by default | Set via SSO policy — recommend 5 attempts |
| Lockout duration | N/A (not set) | Configure 15-minute lockout after 5 failures |

**Configure SSO lockout policy:**

vSphere Client → vCenter → Administration → Single Sign-On → Configuration → Local Accounts → Lockout Policy

| Field | Recommended Value |
|---|---|
| Maximum number of failed login attempts | 5 |
| Time interval between failures (seconds) | 180 |
| Unlock time (seconds) | 900 (15 minutes) |

### API Tokens and Automation

For automation with PowerCLI or REST API, use session tokens rather than embedding credentials in scripts:

```powershell
# Request a session token (avoids passing credentials in each call)
Connect-VIServer <vcenter> -Credential (Get-Credential)
$session = $global:DefaultVIServer.SessionId

# Use the session token in API calls
# PowerCLI maintains the session automatically during the script run
Disconnect-VIServer -Confirm:$false
```

For REST API automation:

```bash
# Authenticate and get a session token
TOKEN=$(curl -s -u "administrator@vsphere.local:password" \
    -X POST "https://vcenter/api/session" \
    -k | tr -d '"')

# Use the token in subsequent calls
curl -s -H "vmware-api-session-id: $TOKEN" \
    "https://vcenter/api/vcenter/cluster" -k | jq '.'

# Terminate the session when done
curl -s -H "vmware-api-session-id: $TOKEN" \
    -X DELETE "https://vcenter/api/session" -k
```

---

## ESXi Host Authentication

### SSH Access

SSH to ESXi hosts is disabled by default and should remain disabled in production. Enable only when required for maintenance, then disable again.

```bash
# Enable SSH from ESXi shell (local console)
esxcli system maintenanceMode set --enable true  # if host needs to be in MM first
vim-cmd hostsvc/enable_ssh
vim-cmd hostsvc/start_ssh

# Disable SSH after maintenance
vim-cmd hostsvc/stop_ssh
vim-cmd hostsvc/disable_ssh
```

**Or from vCenter UI:**
Host → Configure → Services → SSH → Start / Stop

### Root Password Management

- The ESXi root password should be managed through vCenter host profiles or a configuration management tool.
- Rotate root passwords on a schedule (90 days).
- Store root credentials in a privileged access management (PAM) system.
- Consider disabling direct root login via SSH and using named admin accounts with `su` — supported from ESXi 8.0.

### Active Directory for ESXi Host Access

ESXi hosts can be joined to Active Directory, allowing domain users to authenticate to the ESXi shell and DCUI.

```bash
# Join ESXi host to AD from ESXi shell
esxcli system settings advanced set \
    -o /Config/HostAgent/plugins/hostsvc/esxAdminsGroup \
    -s "vSphere Admins"

# Join host to domain via vCenter
# vSphere Client → Host → Configure → System → Authentication Services → Join Domain
```

When joined to AD, members of the `ESX Admins` group (or the configured group) receive Administrator access to the ESXi host.

---

## Certificate-Based Authentication

### vSAN and VMCA

vCenter's VMware Certificate Authority (VMCA) issues certificates to all ESXi hosts during cluster onboarding. These certificates authenticate host-to-host vSAN communications (CMMDS cluster membership protocol).

Verify certificate status:

```bash
# Check host certificate
esxcli system certificate info list

# Check VMCA certificate chain
/usr/lib/vmware/vmca/bin/certool --status
```

**Custom CA certificates:** Replace VMCA-issued certificates with certificates from an enterprise CA (Microsoft CA, HashiCorp Vault PKI) if your security policy requires it. vSAN continues to function after certificate replacement — vCenter orchestrates the replacement rolling.

vSphere Client → vCenter → Administration → Certificate Management → Replace VMCA Root Certificate

### TLS Configuration

vSAN management traffic between vCenter and ESXi hosts uses TLS 1.2 minimum. TLS 1.0 and 1.1 are disabled by default from vSphere 7.0 onward.

Verify TLS settings on VCSA:

```bash
# On VCSA shell
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT
```

Configure minimum TLS version in vCenter:
vSphere Client → vCenter → Configure → Advanced Settings → `config.tls.minVersion` = `TLSv1.2`
