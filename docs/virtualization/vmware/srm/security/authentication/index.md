# SRM — Authentication


<div class="kb-summary">
Authentication reference covering Site Pairing Authentication (Certificate-Based), SRA Authentication to Storage Array, REST API Authentication, vSphere Replication Authentication, Break-Glass Access to SRM and 1 more sections.
</div>

  SRM Authentication Chain
```text
┌───────────────────────────────────── VMware SRM — Authentication ─────────────────────────────────────┐
│                                                                                                       │
│  SRM uses vCenter SSO for user authentication; site pair uses TLS certificates                        │
│  for inter-site trust; SRM REST API uses bearer tokens.                                               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             User Authentication              │  │               Site Pair Trust               │   │
│   │           vCenter SSO: all logins            │  │              TLS cert exchange              │   │
│   │            AD groups: role-mapped            │  │            Self-signed or CA cert           │   │
│   │             SAML token from SSO              │  │             Trust on first pair             │   │
│   │         MFA: via vCenter SSO policy          │  │           Re-pair if cert changes           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  User auth is entirely vCenter SSO; site trust is certificate-based TLS.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                REST API Auth                 │  │            Certificate Management           │   │
│   │             POST /api/rest/login             │  │         SRM cert: Windows cert store        │   │
│   │          Bearer token: short-lived           │  │           Replace via IIS bindings          │   │
│   │            Basic auth: automation            │  │              TLS 1.2+ enforced              │   │
│   │         Refresh: re-login on expiry          │  │            Re-pair: cert rotation           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AD must be reachable from both SRM Servers on management network; cert must be                       │
│  trusted by remote SRM Server for site pair to establish.                                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vCenter SSO   = SRM delegates all user auth to vCenter SSO                                           │
│  SAML token    = SSO assertion; used for SRM session                                                  │
│  Bearer token  = REST API token; short-lived JWT                                                      │
│  Site pair TLS = mutual TLS between the two SRM Servers                                               │
│  Trust-on-pair = exchange certs when creating site pair                                               │
│  Re-pair       = required if SRM cert is replaced                                                     │
│  IIS binding   = SRM Server binds TLS cert via Windows IIS                                            │
│  TLS 1.2+      = minimum for site pair and REST API                                                   │
│  Basic auth    = REST API; base64 user:pass; use only over TLS                                        │
│  MFA           = enforced at vCenter SSO layer; applies to SRM                                        │
│  AD reachable  = SSO requires AD for group membership lookup                                          │
│  Cert rotation = requires re-pair; plan maintenance window                                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── VMware SRM — Authentication ─────────────────────────────────────┐
│                                                                                                       │
│  SRM uses vCenter SSO for user authentication; site pair uses TLS certificates                        │
│  for inter-site trust; SRM REST API uses bearer tokens.                                               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             User Authentication              │  │               Site Pair Trust               │   │
│   │           vCenter SSO: all logins            │  │              TLS cert exchange              │   │
│   │            AD groups: role-mapped            │  │            Self-signed or CA cert           │   │
│   │             SAML token from SSO              │  │             Trust on first pair             │   │
│   │         MFA: via vCenter SSO policy          │  │           Re-pair if cert changes           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  User auth is entirely vCenter SSO; site trust is certificate-based TLS.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                REST API Auth                 │  │            Certificate Management           │   │
│   │             POST /api/rest/login             │  │         SRM cert: Windows cert store        │   │
│   │          Bearer token: short-lived           │  │           Replace via IIS bindings          │   │
│   │            Basic auth: automation            │  │              TLS 1.2+ enforced              │   │
│   │         Refresh: re-login on expiry          │  │            Re-pair: cert rotation           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AD must be reachable from both SRM Servers on management network; cert must be                       │
│  trusted by remote SRM Server for site pair to establish.                                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vCenter SSO   = SRM delegates all user auth to vCenter SSO                                           │
│  SAML token    = SSO assertion; used for SRM session                                                  │
│  Bearer token  = REST API token; short-lived JWT                                                      │
│  Site pair TLS = mutual TLS between the two SRM Servers                                               │
│  Trust-on-pair = exchange certs when creating site pair                                               │
│  Re-pair       = required if SRM cert is replaced                                                     │
│  IIS binding   = SRM Server binds TLS cert via Windows IIS                                            │
│  TLS 1.2+      = minimum for site pair and REST API                                                   │
│  Basic auth    = REST API; base64 user:pass; use only over TLS                                        │
│  MFA           = enforced at vCenter SSO layer; applies to SRM                                        │
│  AD reachable  = SSO requires AD for group membership lookup                                          │
│  Cert rotation = requires re-pair; plan maintenance window                                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── VMware SRM — Authentication ─────────────────────────────────────┐
│                                                                                                       │
│  SRM uses vCenter SSO for user authentication; site pair uses TLS certificates                        │
│  for inter-site trust; SRM REST API uses bearer tokens.                                               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             User Authentication              │  │               Site Pair Trust               │   │
│   │           vCenter SSO: all logins            │  │              TLS cert exchange              │   │
│   │            AD groups: role-mapped            │  │            Self-signed or CA cert           │   │
│   │             SAML token from SSO              │  │             Trust on first pair             │   │
│   │         MFA: via vCenter SSO policy          │  │           Re-pair if cert changes           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  User auth is entirely vCenter SSO; site trust is certificate-based TLS.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                REST API Auth                 │  │            Certificate Management           │   │
│   │             POST /api/rest/login             │  │         SRM cert: Windows cert store        │   │
│   │          Bearer token: short-lived           │  │           Replace via IIS bindings          │   │
│   │            Basic auth: automation            │  │              TLS 1.2+ enforced              │   │
│   │         Refresh: re-login on expiry          │  │            Re-pair: cert rotation           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AD must be reachable from both SRM Servers on management network; cert must be                       │
│  trusted by remote SRM Server for site pair to establish.                                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vCenter SSO   = SRM delegates all user auth to vCenter SSO                                           │
│  SAML token    = SSO assertion; used for SRM session                                                  │
│  Bearer token  = REST API token; short-lived JWT                                                      │
│  Site pair TLS = mutual TLS between the two SRM Servers                                               │
│  Trust-on-pair = exchange certs when creating site pair                                               │
│  Re-pair       = required if SRM cert is replaced                                                     │
│  IIS binding   = SRM Server binds TLS cert via Windows IIS                                            │
│  TLS 1.2+      = minimum for site pair and REST API                                                   │
│  Basic auth    = REST API; base64 user:pass; use only over TLS                                        │
│  MFA           = enforced at vCenter SSO layer; applies to SRM                                        │
│  AD reachable  = SSO requires AD for group membership lookup                                          │
│  Cert rotation = requires re-pair; plan maintenance window                                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

The certificate thumbprint is permanently stored — if either site's certificate is replaced, the pairing must be re-established or the new thumbprint accepted.

### Re-establishing Pairing After Cert Rotation

```text
Site Recovery → Site Pair → [pair] → Edit
  Update thumbprints if cert changed
  OR: delete and re-create site pair
```

---

## SRA Authentication to Storage Array

SRAs authenticate to storage arrays using credentials stored in SRM:

```text
Site Recovery → Storage → Array Pairs → [pair] → Adapter Configuration
  FlashArray: management IP + API token (preferred over username/password)
  Other arrays: management IP + username/password
```

Credentials are encrypted at rest using SRM's internal encryption. Rotate on a schedule:
1. Create new credential on the array
2. Update in SRM adapter configuration
3. Delete old credential on array

---

## REST API Authentication

SRM REST API uses vCenter session tokens:

```bash
# Step 1: Get vCenter session token
TOKEN=$(curl -sk -X POST \
  "https://vcenter-protected.example.local/rest/com/vmware/cis/session" \
  -u "administrator@vsphere.local:<password>" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['value'])")

# Step 2: Use token for SRM API calls
curl -sk -H "vmware-api-session-id: $TOKEN" \
  "https://vcenter-protected.example.local/api/vcenter/dr/recovery/plans"
```

---

## vSphere Replication Authentication

VRA appliances authenticate to each other and to vCenter using certificates. The VRA registers with vCenter using vCenter SSO credentials provided during initial configuration.

If vCenter certificate is replaced, re-register VRA:
```text
VRA VAMI (https://vra-protected.example.local:5480)
  Configuration → vCenter Server → Reconfigure
  Re-enter vCenter credentials
```

---

## Break-Glass Access to SRM

If vCenter SSO is unavailable, SRM cannot authenticate users. SRM is not operational without vCenter.

Recovery procedure: restore vCenter first, then SRM reconnects automatically. This is why vCenter must be included in DR plans — it is a dependency of SRM itself.
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
