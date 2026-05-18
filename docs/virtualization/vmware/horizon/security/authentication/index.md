# Horizon — Authentication

```
  Authentication Flow
┌────────────┐    ┌──────────────┐    ┌─────────────────────────────┐
│  User      │    │  Workspace   │    │  Connection Server          │
│            │───►│  ONE / vIDM  │───►│  ┌─────────────────────┐    │
│  1. Login  │    │  (SAML IdP)  │    │  │ AD Kerberos / NTLM  │    │
│            │    │  ┌─────────┐ │    │  │ RADIUS (2FA)        │    │
│            │    │  │ MFA /   │ │    │  │ Smart Card (PIV/CAC) │   │
│            │    │  │ FIDO2 / │ │    │  └─────────────────────┘    │
│            │    │  │ LDAP    │ │    │                             │
│            │    │  └─────────┘ │    │  True SSO (cert issued)     │
└────────────┘    └──────────────┘    │  ┌─────────────────────┐   │
                                      │  │ Enrollment Server   │   │
                                      │  │ → short-lived cert  │   │
                                      │  │ → Windows login     │   │
                                      │  └─────────────────────┘   │
                                      └─────────────────────────────┘
```

---

## Primary Authentication: Active Directory

Connection Server authenticates users against AD. The Connection Server must be domain-joined:

```powershell
# Verify domain membership on Connection Server
(Get-WmiObject Win32_ComputerSystem).Domain
# Should return corp.local
```

Configure AD domains in Horizon:
```
Horizon Console → Settings → Servers → Domains
  All trusted domains should appear automatically
  If not: Add Domain → enter domain name and service account credentials
```

---

## Two-Factor Authentication (RADIUS / RSA SecurID)

```
Horizon Console → Settings → Servers → Connection Servers → [CS] → Edit → Authentication
  2-Factor Authentication: RADIUS
  Authentication Module: RadiusAuthModule
  Hostname: radius.corp.local
  Port: 1812
  Shared Secret: <radius secret>
  Username Hint: Use UPN (user@corp.local) or sAMAccountName
```

For RSA SecurID (hardware token):
```
  2-Factor Authentication: SecurID
  Load RSA sdconf.rec (downloaded from RSA Authentication Manager)
```

---

## SAML Authentication (Workspace ONE / vIDM)

SAML enables IdP-initiated SSO — users authenticate to Workspace ONE/vIDM and are passed to Horizon:

```
Horizon Console → Settings → Servers → Connection Servers → [CS] → Edit → Authentication
  Delegation of Authentication to VMware Identity Manager: Allowed or Required
  vIDM URL: https://vidm.corp.local
  Token TTL: 300 seconds
```

SAML is required for:
- Passwordless authentication
- Biometric (FIDO2) authentication via vIDM
- True SSO (certificate-based silent desktop login)

---

## Smart Card / Certificate Authentication

```
Horizon Console → Settings → Servers → Connection Servers → [CS] → Edit → Authentication
  Smart Card Authentication: Required or Optional
  Certificate Revocation: Use CRL / OCSP (recommended)
  Certificate Revocation URL: http://pki.corp.local/crl/corp-ca.crl
```

Smart card authentication works with CAC, PIV, and software certificates. The client OS must have the certificate in the user's personal certificate store.

---

## True SSO

True SSO eliminates the password prompt for desktop login after initial UAG authentication:

```
Requirements:
  - Microsoft Enterprise CA
  - Enrollment Server role (installed on same or separate Windows Server)
  - SAML authentication configured
  - Certificate template: Horizon Enrollment (key usage: Digital Signature, Key Encipherment)

Horizon Console → Settings → True SSO
  Enable True SSO
  Enrollment Server: <FQDN of Enrollment Server>
  Template: Horizon
```

When enabled: user authenticates once at UAG (AD/SAML/RADIUS), receives short-lived cert, desktop logs in automatically.

---

## Unauthenticated Access (Kiosk Mode)

For kiosk/shared terminals with no personal authentication:

```
Horizon Console → Settings → Servers → Connection Servers → [CS] → Edit → Authentication
  Allow Unauthenticated Access: Enabled
```

Assign kiosk desktops to a dedicated pool with restricted internet access and no persistent profiles.

---

## Session Timeout and Reauthentication

```
Horizon Console → Settings → Global Settings → General
  Session Timeout: 600 minutes (10 hours — adjust per policy)
  Disconnected Session Timeout: 60 minutes (log off disconnected sessions)
  Reauthentication on Reconnect: Enabled (require new auth after disconnect)
```

For high-security environments: set Reauthentication = Always and reduce timeout to 4 hours.

---

## UAG Identity Bridging

UAG can perform identity bridging for applications that require Kerberos authentication internally when users are authenticating externally via SAML:

```
UAG Admin UI → Edge Service Settings → Horizon → Advanced
  Identity Bridging: Enable
  Principal Name: UPN (user@corp.local)
```

This allows external SAML-authenticated users to transparently access Kerberos-protected intranet applications through the desktop.
