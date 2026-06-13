---
tags:
  - security
  - vmware
  - vsan
  - vsphere-8
---
# vSAN — Authentication


<div class="kb-summary">
vSAN does not have its own authentication system. All access to vSAN management functions is authenticated through vCenter Server, which in turn delegates identity verification to the vSphere SSO domain and configured identity sources.

*Applies to: vSAN 7.x / 8.x*
</div>

---

## Authentication Stack

```text
┌──────────────────────────────────────── vSAN — Authentication ────────────────────────────────────────┐
│                                                                                                       │
│  vSAN cluster nodes authenticate each other using the ESXi host SSL certificates;                     │
│  management authentication uses vCenter SSO.                                                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Cluster Node Auth               │  │               Management Auth               │   │
│   │            ESXi SSL cert: node ID            │  │           vCenter SSO: all logins           │   │
│   │         Cluster UUID: shared secret          │  │           SAML token for API calls          │   │
│   │        Host join: vCenter issues UUID        │  │            AD groups: role-mapped           │   │
│   │       RDT: Reliable Datagram Transport       │  │           MFA: per vCenter policy           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Cluster node trust uses ESXi certs; management trust uses vCenter SSO tokens.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              KMS Authentication              │  │           Certificate Requirements          │   │
│   │          KMS: client cert per ESXi           │  │           Host cert: auto-renewed           │   │
│   │             KMIP mutual TLS auth             │  │            VMCA: signs host certs           │   │
│   │         KMS cluster: redundant pair          │  │           Custom CA: replace VMCA           │   │
│   │         Key retrieval: power-on path         │  │           Expiry: monitor >30 days          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  KMS server must be reachable from each ESXi host on management network port 5696;                    │
│  KMS cluster ensures HA key retrieval for encrypted vSAN.                                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cluster UUID  = unique identifier shared across all vSAN cluster nodes                               │
│  RDT           = Reliable Datagram Transport; vSAN inter-host protocol                                │
│  KMIP          = Key Management Interoperability Protocol; port 5696                                  │
│  KMS           = Key Management Server; holds encryption keys                                         │
│  Mutual TLS    = both client and server present certs; bidirectional auth                             │
│  VMCA          = vSphere Certificate Authority; signs host machine certs                              │
│  Host cert     = SSL cert on each ESXi host; auto-renewed by VMCA                                     │
│  Custom CA     = replace VMCA with enterprise PKI for compliance                                      │
│  SAML token    = SSO assertion; used for vCenter API auth                                             │
│  KMS cluster   = HA pair of KMS nodes; both must be reachable                                         │
│  Key retrieval = power-on of encrypted VM triggers KMS request                                        │
│  AD groups     = Active Directory groups mapped to vCenter RBAC roles                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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

**Post-join verification:**

```bash
/opt/likewise/bin/lwsm status
# lsass service should be running
```

**Add AD groups to vCenter permissions after joining:**

vSphere Client → vCenter → Permissions → Add → select identity source → search AD group → assign role

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
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
