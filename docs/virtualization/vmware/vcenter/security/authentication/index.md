---
tags:
  - security
  - vcenter
  - vmware
  - vsphere-8
---
# vCenter Security — Authentication


<div class="kb-summary">
Authentication reference covering SSO Security, TLS Configuration, Certificates to Track, Certificate Replacement Process, Validation After Replacement and 5 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌─────────────────────────────────── vCenter Server — Authentication ───────────────────────────────────┐
│                                                                                                       │
│  vCenter authentication is handled by the embedded SSO service; it validates                          │
│  credentials against identity sources and issues SAML tokens for session access.                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Authentication Flow              │  │                 MFA Options                 │   │
│   │         User → vSphere Client login          │  │               Smart card / CAC              │   │
│   │          SSO validates credentials           │  │              RSA SecurID token              │   │
│   │          SAML token issued (8h TTL)          │  │              RADIUS integration             │   │
│   │           Token used for API calls           │  │             Duo via RADIUS proxy            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SSO token TTL is 8h; re-login required; API calls use bearer token from POST /api/session.           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Session Management              │  │               Lockout Policies              │   │
│   │           Max concurrent sessions            │  │              5 failed → lockout             │   │
│   │          Idle timeout: configurable          │  │           Lockout duration: 5 min           │   │
│   │        Force re-auth on privilege op         │  │              Unlock: SSO admin              │   │
│   │        API session token: short-lived        │  │            Alert on failed logins           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SSO service runs on VCSA; AD/LDAP identity source must be reachable from                             │
│  management network on port 389 (LDAP) or 636 (LDAPS).                                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SSO          = Single Sign-On; built into VCSA; core auth service                                    │
│  SAML token   = XML security assertion; vCenter uses this internally                                  │
│  SAML TTL     = 8 hours default; configurable in SSO configuration                                    │
│  Smart card   = PIV/CAC certificate-based login; requires vCenter config                              │
│  RSA SecurID  = one-time password hardware token; RADIUS integration                                  │
│  RADIUS       = Remote Authentication Dial-In User Service; MFA backend                               │
│  Duo          = MFA provider; integrates via RADIUS proxy to vCenter                                  │
│  Lockout      = SSO account temporarily blocked after failed attempts                                 │
│  Idle timeout = browser session closes after inactivity period                                        │
│  POST /api/session= REST API login; returns bearer token in response                                  │
│  LDAPS        = LDAP over TLS/SSL; port 636; required for AD in vcenter 8+                            │
│  AD identity  = Active Directory added as SSO identity source                                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## TLS Configuration

vCenter enforces TLS 1.2 minimum by default (vSphere 7.0+). TLS 1.0 and 1.1 are disabled.

### Certificate Modes

| Mode | Description | When to Use |
|---|---|---|
| VMCA (default) | vCenter acts as CA; signs all vCenter/host certs | Lab, small deployments |
| Custom CA | Enterprise CA signs all certs; VMCA subordinate to enterprise CA | Enterprise/compliance |
| Hybrid | VMCA for machine SSL; custom CA for solution user certs | Transitional |
| External CA — all custom | All certs replaced with enterprise CA-signed certs | Strict compliance |

### Certificate Replacement — Machine SSL (VCSA)

```bash
# On VCSA shell
/usr/lib/vmware-vmca/bin/certificate-manager
# Option 1: Generate CSR signed by external CA
# Option 5: Replace machine SSL certificate
```

Replacement requires vCenter services restart. Plan a maintenance window.

### Certificate Monitoring

```powershell
# PowerCLI — check vCenter endpoint certificate expiry
$req = [Net.HttpWebRequest]::Create("https://<vcenter>")
$req.GetResponse() | Out-Null
$cert = $req.ServicePoint.Certificate
[DateTime]::Parse($cert.GetExpirationDateString())
```

```bash
# Check certificate expiry from outside VCSA
echo | openssl s_client -connect <vcenter-fqdn>:443 -servername <vcenter-fqdn> 2>/dev/null \
  | openssl x509 -noout -dates

# List certificates in VECS store on VCSA (SSH)
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT --text \
  | grep -E "Alias|Not After"
```

## Certificates to Track

| Certificate | Location | Risk if Expired |
|---|---|---|
| vCenter Machine SSL | VAMI → Certificate Management | Browser warnings, API failures |
| VMCA Root Certificate | VAMI → Certificate Management | Breaks all VMCA-issued certs |
| STS Certificate | vSphere Client → SSO → Certificates | Login failures platform-wide |
| Solution User Certificates | VAMI → Certificate Management | Service-to-service auth failures |

## Certificate Replacement Process

```mermaid
graph LR
    id1["Identify expiring cert\n(VAMI / openssl check)"]
    id2["Confirm vCenter\nbackup is current"]
    id3["Schedule maintenance\nwindow"]
    id4["Replace via\ncertificate-manager"]
    id5["Restart affected\nservices"]
    id6["Validate browser,\nSSO, integrations"]

    id1 --> id2 --> id3 --> id4 --> id5 --> id6

    classDef step fill:#2563eb,stroke:#1d4ed8,color:#fff
    class id1,id2,id3,id4,id5,id6 step
```

1. Identify the certificate and replacement method (VMCA, custom CA, or self-signed)
2. Confirm backup of vCenter is current
3. Schedule a maintenance window
4. Replace the certificate using the appropriate method
5. Restart affected services
6. Validate all integrations and logins

## Validation After Replacement

- Browser access to vCenter confirmed with no certificate warning
- All ESXi hosts Connected
- SSO login working for both local and AD accounts
- Aria, NSX, and backup integrations confirmed working

## Emergency Escalation

If certificate expiry causes a login or service failure:
- Check if the local administrator account (`administrator@vsphere.local`) still works
- Engage VMware support if SSO or STS cannot be recovered in place

---

## SAML Federation (External IdP)

vCenter can act as a SAML service provider for an external IdP such as ADFS, Okta, or Azure AD. This enables MFA enforcement at the IdP level without requiring MFA on every VCSA individually.

Configure at **Administration → Single Sign On → Configuration → Identity Provider → Set up SAML Service Provider**.

### ADFS Configuration (High Level)

1. Export the vCenter SAML metadata from **SSO → Configuration → SAML Service Provider → Download Service Provider Metadata**
2. In ADFS: Add a new Relying Party Trust using the metadata file
3. Add claim rules: `UPN → NameID`, `Token-Groups (unqualified names) → Group`
4. In vCenter: Set the IdP metadata URL (your ADFS federation metadata endpoint)
5. Test login: users should be redirected to ADFS login page and returned to vSphere Client with their AD group memberships

After federation is configured, grant permissions to AD groups (not individual users) in vCenter. The group SID comparison is done via the SAML assertion attributes.

---

## vCenter Enhanced Linked Mode (ELM)

Enhanced Linked Mode connects multiple vCenter instances to a shared SSO domain, providing single-pane-of-glass management across sites.

| Feature | Linked Mode |
|---|---|
| Single login | Yes — authenticate once, manage all vCenters |
| Shared roles | Yes — roles defined on one vCenter are visible on others |
| Shared permissions | Partially — global permissions apply to all; local permissions are per-vCenter |
| Shared inventory | Yes — view VMs and hosts across all vCenters |
| vMotion across vCenters | Yes — cross-vCenter vMotion supported (requires same SSO domain) |

```powershell
# Connect to multiple vCenters simultaneously
Connect-VIServer -Server vcenter-lon.example.local, vcenter-ams.example.local

# List all VMs across both vCenters
Get-VM | Select-Object Name, @{N="vCenter";E={$_.Uid.Split(':')[0]}}, PowerState

# Disconnect all
Disconnect-VIServer * -Confirm:$false
```

---

## Unlocking Accounts

### Unlock administrator@vsphere.local

```bash
# SSH to VCSA
/usr/lib/vmware-vmafd/bin/dir-cli user unlock \
    --account administrator \
    --domain vsphere.local \
    --password <current-password>

# If the password is also lost, reset via VCSA console (single-user mode)
# See VMware KB 2069041 for the reset procedure
```

### Unlock an AD Account (from vCenter)

AD account lockouts caused by vCenter (e.g. cached wrong password in identity source):
1. Check if the bind account password has changed — update in **SSO → Identity Sources → Edit**
2. Unlock the AD account from Active Directory Users and Computers or PowerShell:
   ```powershell
   # On a domain controller
   Unlock-ADAccount -Identity jsmith
   ```
3. Restart `vmware-sts-idmd` service to clear any cached authentication state:
   ```bash
   service-control --restart vmware-sts-idmd
   ```
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
