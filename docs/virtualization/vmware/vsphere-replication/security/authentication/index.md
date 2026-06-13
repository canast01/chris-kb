---
tags:
  - security
  - vmware
  - vsphere-replication
---
# vSphere Replication — Authentication


<div class="kb-summary">
Authentication reference covering VRA Registered with vCenter SSO, Site Pairing Authentication (Certificate-Based), VRA Admin Account, REST API Authentication, vCenter Certificate Replacement Impact and 3 more sections.
</div>

  VR Authentication Architecture
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  User / Script            vCenter SSO           VRA                                                   │
│  ┌──────────────┐         ┌──────────────┐      ┌─────────┐                                           │
│  │ vCenter UI / │────────►│  SSO session │─────►│ VR feat.│                                           │
│  │ PowerCLI     │         │  (no separate│      │ via VC  │                                           │
│  └──────────────┘         │   VR login)  │      └─────────┘                                           │
│                           └──────────────┘                                                            │
│                                                                                                       │
│  Site Pairing (cert-based)                                                                            │
│  ┌──────────────────────────────────────────────────────┐                                             │
│  │ VRA Site A cert thumbprint ──► accepted at Site B    │                                             │
│  │ VRA Site B cert thumbprint ──► accepted at Site A    │                                             │
│  │ Refresh thumbprints after any cert replacement       │                                             │
│  └──────────────────────────────────────────────────────┘                                             │
│                                                                                                       │
│  REST API: POST /api/rest/vr/authentication/token                                                     │
│  Token TTL: 300 seconds                                                                               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## VRA Registered with vCenter SSO

VRA authenticates to vCenter using vCenter SSO credentials provided during initial registration. End-users authenticate to VR features through vCenter — no separate VR login.

```yaml
VRA VAMI → Configuration → vCenter Server
  vCenter: vcenter-london.example.local
  Username: administrator@vsphere.local
  Password: <password>
  → Register
```

If vCenter SSO credentials change, update VRA registration with new credentials.

---

## Site Pairing Authentication (Certificate-Based)

VRA appliances authenticate to each other using their SSL certificates. When pairing sites:

```text
vCenter → Site Recovery → New Site Pair
  → Presents remote VRA certificate thumbprint for acceptance
  Accept thumbprint → stored in local vCenter database
```

If either VRA certificate is replaced after pairing, the pairing must be updated:

```bash
Site Recovery → Sites → [pair] → Edit → Refresh Thumbprints
# OR: delete and re-create the site pair
```

---

## VRA Admin Account

The VRA VAMI admin account is local to the appliance, separate from vCenter SSO:

```text
VRA VAMI (https://vra-london.example.local:5480)
  Username: admin
  Password: set during OVA deployment

Change password:
  VAMI → Administration → Change Admin Password
```

---

## REST API Authentication

```bash
# Get session token
curl -sk -X POST \
  "https://vra-london.example.local/api/rest/vr/authentication/token" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "<password>"}' | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['token'])"

# Token usage
curl -sk -H "Authorization: Bearer <token>" \
  "https://vra-london.example.local/api/rest/vr/replications"
```

Token TTL: default 300 seconds — request a new token for longer-running scripts.

---

## vCenter Certificate Replacement Impact

When vCenter's SSL certificate is replaced:
- VRA must re-register with vCenter to accept the new certificate:
```text
  VRA VAMI → Configuration → vCenter Server → Reconnect or Re-register
  ```
- Site pairing thumbprints should be verified:
  ```text
  Site Recovery → Sites → [pair] → verify Connected status
  ```

---

## ESXi hbrsvc Authentication

The ESXi replication service (hbrsvc) authenticates to the target VRA to establish replication sessions. This authentication is managed automatically by vSphere — no manual credential configuration is needed. It uses certificates managed by vCenter.

---

## Session Security

| Setting | Default | Notes |
|---|---|---|
| VRA VAMI session timeout | 30 minutes | Cannot be configured |
| REST API token TTL | 300 seconds | Request new token for long-running scripts |
| VRA SSH login | Key or password | Restrict to key-based only (see Hardening) |
---

## Related Reference

- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
