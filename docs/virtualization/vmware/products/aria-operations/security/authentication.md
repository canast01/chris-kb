---
tags:
  - aria-operations
  - security
  - vmware
description: "Authentication reference covering Authentication Sources, Configuring Active Directory / LDAP, LDAP Group Import and Role Assignment, Workspace ONE Access..."
---
# Aria Operations — Authentication

<div class="kb-summary">
Authentication reference covering Authentication Sources, Configuring Active Directory / LDAP, LDAP Group Import and Role Assignment, Workspace ONE Access (VIDM) / SAML Integration, API Authentication and 3 more sections.

*Applies to: Aria Ops 8.x*
</div>
![Aria Operations — Authentication](../../../../../assets/virtualization-vmware-aria-operations-security-authenticatio.svg)

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Authentication Sources

Aria Operations supports multiple authentication sources. Users can authenticate against any configured source.

| Source | Type | Use Case |
|---|---|---|
| **Local** | Built-in user accounts | Break-glass admin, lab environments |
| **Active Directory** | LDAP/LDAPS | Primary enterprise authentication |
| **OpenLDAP** | LDAP | Non-AD LDAP directories |
| **Workspace ONE Access (VIDM)** | SAML 2.0 | SSO integration with LCM-deployed environments |

---

## Configuring Active Directory / LDAP

**Via UI:**

Expected result: "Connection successful — X users found."

---

## LDAP Group Import and Role Assignment

After adding the AD source, import groups to assign roles:

```text
Administration → Access Control → User Groups → Import Groups from Source
```

Search for the group name (e.g., `GG-VROPS-Admins`) → select → Import.

Assign a role to the imported group:

```text
Administration → Access Control → User Groups → select group → Assign Role → select role
```

| AD Group | Aria Operations Role |
|---|---|
| `GG-VROPS-Admins` | Administrator |
| `GG-VROPS-ContentAdmins` | Content Admin |
| `GG-VROPS-Operators` | Operator |
| `GG-VROPS-ReadOnly` | Read Only |

---

## Workspace ONE Access (VIDM) / SAML Integration

When Aria Operations is deployed and managed by LCM, VIDM is automatically registered as the SSO provider. For standalone deployments:

```text
Administration → Global Settings → Authentication → Enable SSO → Configure VIDM
```

Provide:
- VIDM FQDN
- Admin credentials for VIDM registration

After configuration, the Aria Operations login page shows "Log in with VMware Identity Manager." AD users authenticated via VIDM can be assigned Aria Operations roles by importing VIDM groups.

---

## API Authentication

The Aria Operations REST API supports two authentication methods:

**Token-based (preferred):**

```bash
# Acquire a token — valid for 30 minutes
TOKEN=$(curl -sk -X POST \
  "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","authSource":"Local"}' | \
  jq -r '.token')

# Use token in subsequent API calls
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/adapterkinds"
```


```text title="Expected output"
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcwOTMxNjgwMCwiZXhwIjoxNzA5MzE4NjAwfQ.x7kL9mN2pQrS4tUvWxYzAbCdEfGhIjKlMnOpQrStUv"}
{
  "adapterKinds": [
    {
      "key": "VMWARE",
      "name": "VMware vSphere Adapter",
      "version": "8.10.2",
      "resourceKinds": ["VirtualMachine", "HostSystem", "Datastore"]
    },
    {
      "key": "KUBERNETES",
      "name": "Kubernetes Adapter",
      "version": "8.10.1",
      "resourceKinds": ["Pod", "Node", "Service"]
    },
    {
      "key": "CUSTOM_REST",
      "name": "Custom REST Adapter",
      "version": "8.9.5",
      "resourceKinds": ["CustomResource"]
    }
  ],
  "pageInfo": {
    "pageSize": 10,
    "totalCount": 3
  }
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip certificate verification (already present in example, but ensure it's not removed).
    **`jq: parse error: Cannot index string with string "token"`** — Verify the authentication response is valid JSON and credentials are correct; check that the API endpoint and password are accurate.
    **`curl: (401) Unauthorized`** — Ensure the token variable is properly set by running `echo $TOKEN` to verify it's not empty, and confirm the token hasn't expired (tokens are valid for 30 minutes).
**Basic authentication (scripts and monitoring):**

```bash
curl -sk -u 'admin:<password>' \
  "https://vrops-prod-01.example.local/suite-api/api/alertdefinitions" | jq '.'
```


```text title="Expected output"
{
  "pageInfo": {
    "pageSize": 20,
    "totalCount": 847,
    "resourceCount": 20,
    "pageNumber": 1
  },
  "links": [
    {
      "resourceType": "AlertDefinition",
      "rel": "self",
      "href": "/suite-api/api/alertdefinitions?pageSize=20&pageNumber=1"
    }
  ],
  "alertDefinitions": [
    {
      "id": "AlertDefinition-1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p",
      "name": "CPU Ready Time High",
      "adapterKindKey": "VMware",
      "resourceKindKey": "VirtualMachine",
      "severity": "CRITICAL",
      "enabled": true,
      "description": "Alert when CPU ready time exceeds threshold"
    },
    {
      "id": "AlertDefinition-2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q",
      "name": "Memory Contention",
      "adapterKindKey": "VMware",
      "resourceKindKey": "VirtualMachine",
      "severity": "WARNING",
      "enabled": true
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or import the vROps certificate into your CA bundle.
    **`jq: parse error: Invalid JSON text at line 1`** — Verify the API endpoint is correct and the vROps service is running; check with `curl -sk -u 'admin:<password>' "https://vrops-prod-01.example.local/suite-api/api/about"` first.
    **`401 Unauthorized`** — Confirm the admin password is correct and the user account has API access permissions in vROps.
For AD-authenticated API calls, include `authSource`:

```bash
TOKEN=$(curl -sk -X POST \
  "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc.vrops@corp.local","password":"<password>","authSource":"corp.local"}' | \
  jq -r '.token')
```


```text title="Expected output"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdmMudnJvcHNAY29ycC5sb2NhbCIsImlhdCI6MTcwOTMxNjgwMCwiZXhwIjoxNzA5MzIwNDAwLCJhdXRob3JpdGllcyI6WyJBRE1JTiIsIkFVVEgiXX0.a2V5LWZvci1zaWduaW5nLXRva2Vucy1oZXJlLWlzLWxvbmdlcg==
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification (already present; if error persists, verify the FQDN matches the certificate CN).
    **`jq: parse error: Cannot index null with string "token"`** — Verify credentials are correct and the authentication endpoint is accessible; check the actual response with `curl -sk ... | jq '.'` to see the error message.
    **`command not found: jq`** — Install jq with `apt-get install jq` (Debian/Ubuntu) or `yum install jq` (RHEL/CentOS).
---

## Token Expiry and Rotation

Tokens expire after 30 minutes. Scripts that run longer must re-authenticate or keep a token-renewal loop:

```bash
#!/usr/bin/env bash
# Re-authenticate function for long-running scripts
get_token() {
  curl -sk -X POST "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$VROPS_USER\",\"password\":\"$VROPS_PASS\",\"authSource\":\"Local\"}" | \
    jq -r '.token'
}

TOKEN=$(get_token)
TOKEN_AGE=0

while [[ ... ]]; do
  TOKEN_AGE=$((TOKEN_AGE + 1))
  if [[ $TOKEN_AGE -ge 25 ]]; then  # renew before 30-minute expiry
    TOKEN=$(get_token)
    TOKEN_AGE=0
  fi
  # ... script body using $TOKEN
  sleep 60
done
```


```text title="Expected output"
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwOTMxNjgwMH0.abc123def456","validity":1800,"sessionID":"550e8400-e29b-41d4-a716-446655440000"}
(no output — command completes silently)
(no output — token refresh loop running)
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl (already present) or import the vROps certificate into your system CA bundle with `update-ca-certificates`.
    **`jq: parse error: Cannot index string with string "token"`** — Verify the API endpoint is correct and the credentials in `$VROPS_USER` and `$VROPS_PASS` are set; test with `curl -sk https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire -d '{"username":"admin","password":"test","authSource":"Local"}' | jq .`
---

## Session Management

| Setting | Default | Location |
|---|---|---|
| Session timeout (UI) | 30 minutes inactivity | Global Settings → Authentication |
| Token lifetime (API) | 30 minutes | Not configurable |
| LDAP sync interval | 60 minutes | Authentication Sources → Edit → Sync Interval |
| Failed login lockout | No lockout (local) | Enforced at AD level for LDAP users |
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements

## See also

- [Aria Operations — Access Control](../access-control/)
- [Aria Operations Security Hardening](../hardening/)
