---
tags:
  - aria-automation
  - security
  - vmware
description: "Authentication reference covering Authentication Architecture, Active Directory Integration via VIDM, API Authentication, API Service Account, Session and..."
---
# Aria Automation — Authentication

<div class="kb-summary">
Authentication reference covering Authentication Architecture, Active Directory Integration via VIDM, API Authentication, API Service Account, Session and Token Policies and 2 more sections.

*Applies to: Aria Automation 8.x*
</div>
![Aria Automation — Authentication](../../../../../assets/virtualization-vmware-aria-automation-security-authenticatio.svg)

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Authentication Architecture

Aria Automation delegates all authentication to **Workspace ONE Access (VIDM)**. There is no standalone AD/LDAP connector in Aria Automation itself — VIDM acts as the identity broker between Aria Automation and Active Directory.

**Acquire a token (AD user):**

```bash
TOKEN=$(curl -sk -X POST \
  "https://vra-prod-01.example.local/csp/gateway/am/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc.vra@corp.local","password":"<password>","domain":"corp.local"}' | \
  jq -r '.token')
```


```text title="Expected output"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdmMudnJhQGNvcnAubG9jYWwiLCJpc3MiOiJjc3AtZ2F0ZXdheSIsImV4cCI6MTcwOTMxNjgwMCwiaWF0IjoxNzA5MzAwNDAwLCJqdGkiOiI0ZjU2YTdjMi1lZTM5LTQyYzAtOWY3ZC1hYzU4ZjM5ZDJlNDMifQ.kX9mZ2pL5qR8vN3wY7jK4hB6cD9eF2gT1sU5xW8yZ0a
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl (already present) or import the CA certificate into your system trust store with `update-ca-certificates`. |
    | `jq: error (at <stdin>:1): Cannot index null with string "token"` | Verify credentials are correct and the CSP gateway is responding; check the actual response with `curl -sk ... | jq '.'` to see the error message. |
    | `command not found: jq` | Install jq with `apt-get install jq` (Debian/Ubuntu) or `yum install jq` (RHEL/CentOS). |
**Token validity:** 8 hours by default. For long-running scripts, implement token refresh logic:

```bash
# Refresh token before expiry (every 7 hours)
TOKEN=$(curl -sk -X POST \
  "https://vra-prod-01.example.local/csp/gateway/am/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc-vra-api","password":"<password>","domain":"System Domain"}' | \
  jq -r '.token')
```


```text title="Expected output"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdmMtdnJhLWFwaSIsImlhdCI6MTcwOTMxMjAwMCwiZXhwIjoxNzA5MzMzNjAwLCJpc3MiOiJodHRwczovL3ZyYS1wcm9kLTAxLmV4YW1wbGUubG9jYWwifQ.kR9mN2pQxL8vZ5jW3tY6aB4cD7eF9gH0iJ1kL2mN3oP
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl (already present) or import the vRA certificate into your system CA bundle with `curl-config --ca-bundle`. |
    | `jq: parse error: Cannot index string with string "token"` | Verify the API response is valid JSON and the login credentials are correct; check vRA gateway logs with `tail -f /var/log/vra/gateway.log`. |
    | `command not found: jq` | Install jq with `apt-get install jq` (Debian/Ubuntu) or `yum install jq` (RHEL/CentOS). |
---

## API Service Account

Create a dedicated local account for API access rather than using the platform `admin` account:

1. Log in to VIDM with admin credentials
2. **VIDM console → Users & Groups → Users → Add User**
3. Create user `svc-vra-api` in the **System Domain**
4. Set a strong password; store in enterprise vault
5. Assign the minimum required Aria Automation role in **Identity & Access Management → Aria Automation → Role Assignments**

---

## Session and Token Policies

| Setting | Default | Configuration |
|---|---|---|
| API token lifetime | 8 hours | VIDM console → Identity & Access Management → Policies |
| UI session timeout | 8 hours | VIDM console → Policies → Session Policies |
| AD group sync interval | 60 minutes | VIDM → Directories → edit directory |
| MFA enforcement | Via VIDM access policies | VIDM console → Policies → Access Policies → add MFA step |
| Failed login lockout | 5 attempts (VIDM default) | VIDM console → Policies → Password Policies |

---

## Certificate Trust for API Clients

Aria Automation uses TLS for all API endpoints. Clients must trust the CA that signed the Aria Automation certificate:

```bash
# Add Aria Automation CA to the OS trust store on a Linux client
cp internal-ca.pem /usr/local/share/ca-certificates/internal-ca.crt
update-ca-certificates   # Debian/Ubuntu

# Python clients
import requests
requests.get("https://vra-prod-01.example.local/iaas/api/zones",
             headers={"Authorization": f"Bearer {token}"},
             verify="/etc/ssl/certs/ca-certificates.crt")
```

```text title="Expected output"
cp: cannot stat 'internal-ca.pem': No such file or directory
(Assuming file exists, cp completes silently)
Updating certificates in /etc/ssl/certs...
rehash: warning: skipping ca-certificates.crt, it is not a certificate or crl
Processing triggers for ca-certificates (20230311) ...
update-ca-certificates: 1 added, 0 removed; 0 removed unlisted.
(Python script runs silently if successful; returns HTTP 200 response with zone data)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cp: cannot stat 'internal-ca.pem': No such file or directory` | Verify the CA certificate file path is correct and exists in the current working directory, or provide the full absolute path. |
    | `requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]` | Run `update-ca-certificates` with sudo and ensure the certificate was copied to `/usr/local/share/ca-certificates/` with a `.crt` extension before updating. |
    | `requests.exceptions.ConnectionError: HTTPSConnectionPool(host='vra-prod-01.example.local')` | Verify the Aria Automation hostname resolves correctly and is reachable from the client, and confirm the token has not expired. |
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements

## See also

- [Aria Automation — Access Control](../access-control/)
- [Aria Automation — Hardening](../hardening/)
