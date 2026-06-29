---
tags:
  - security
  - vmware
  - vsphere-replication
---
# vSphere Replication — Authentication

<div class="kb-summary">
Authentication reference covering VRA Registered with vCenter SSO, Site Pairing Authentication (Certificate-Based), VRA Admin Account, REST API Authentication, vCenter Certificate Replacement Impact and 3 more sections.

*Applies to: vSphere Replication 8.x*
</div>
![vSphere Replication — Authentication](../../../../assets/virtualization-vmware-vsphere-replication-security-authentic.svg)

  VR Authentication Architecture

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`SSL certificate verification failed: certificate has expired`** — Regenerate the SSL certificates on both vSphere Replication servers and re-pair the sites.
    **`Thumbprint mismatch detected between sites`** — Verify network connectivity between replication servers and ensure both are running the same vSphere Replication version before refreshing thumbprints.
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


```text title="Expected output"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcwOTMxNjgwMCwiZXhwIjoxNzA5MzIwNDAwfQ.kX9mPq2rL8vN5oW3jQ6sT1uY4zX7aB9cD2eF5gH8iJ0

{
  "replications": [
    {
      "id": "replication-001",
      "sourceVm": "prod-db-01.example.local",
      "targetSite": "london-dr",
      "status": "ACTIVE",
      "rpo": 300,
      "lastSync": "2024-03-01T14:32:15Z"
    },
    {
      "id": "replication-002",
      "sourceVm": "prod-web-02.example.local",
      "targetSite": "london-dr",
      "status": "ACTIVE",
      "rpo": 600,
      "lastSync": "2024-03-01T14:28:42Z"
    }
  ],
  "totalCount": 2
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in example, but verify `-sk` flags are both included).
    **`KeyError: 'token'`** — Verify the authentication credentials are correct and the VRA server is responding with a valid JSON token object; check server logs for authentication failures.
    **`curl: (7) Failed to connect to vra-london.example.local port 443: Connection refused`** — Confirm the VRA hostname is resolvable and the API service is running on the target host using `curl -v` for detailed connection diagnostics.
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

- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements

## See also

- [vSphere Replication — Access Control](../access-control/)
- [vSphere Replication — Hardening](../hardening/)
