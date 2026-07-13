---
tags:
  - aria-networks
  - security
  - vmware
description: "Authentication reference covering Authentication Methods, Local Authentication, SAML / VMware Identity Manager, API Token Authentication, Session..."
---
# Aria Operations for Networks — Authentication

<div class="kb-summary">
Authentication reference covering Authentication Methods, Local Authentication, SAML / VMware Identity Manager, API Token Authentication, Session Management and 3 more sections.

*Applies to: Aria Networks 6.x*
</div>
![Aria Operations for Networks — Authentication](../../../../../assets/virtualization-vmware-aria-operations-for-networks-security-.svg)

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Authentication Methods

| Method | Description | Use Case |
|---|---|---|
| Local | Built-in admin@local | Initial setup, break-glass |
| LDAP / AD | AD group-to-role mapping | Standard enterprise |
| SAML / vIDM | Workspace ONE SSO | SSO environments |
| API Token | Bearer token for REST API | Automation, monitoring |

---

## Local Authentication

Default credential after OVA deployment: `admin@local` — password set during OVA wizard.

Password policy (Settings → Security):
- Minimum length: 12+ characters (increase from default 8)
- Complexity: uppercase, lowercase, number, special character
- Lockout: 5 failed attempts → 30-minute lockout

Change password:

Attribute mapping in vIDM:
- NameID → user email
- Groups attribute → AD groups synced to vIDM (map to vRNI roles)

---

## API Token Authentication

Create long-lived tokens in UI (Settings → API Tokens → Generate Token). Store in secrets manager — never hard-code.

```bash
# Session token (short-lived — for interactive scripting)
TOKEN=$(curl -sk -X POST \
  https://vrni.example.local/api/ni/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<pass>","domain":{"domain_type":"LOCAL"}}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")

# Use token
curl -sk -H "Authorization: NetworkInsight $TOKEN" \
  "https://vrni.example.local/api/ni/data-sources/vcenters"
```


```text title="Expected output"
{"data":[{"id":"datasource-1","name":"vcenter-prod-01.corp.local","ip_address":"10.42.15.88","version":"7.0.3","status":"ACTIVE","last_collection":"2024-01-15T14:32:18Z"},{"id":"datasource-2","name":"vcenter-dr-02.corp.local","ip_address":"10.42.15.89","version":"7.0.3","status":"ACTIVE","last_collection":"2024-01-15T14:31:45Z"},{"id":"datasource-3","name":"vcenter-test-03.corp.local","ip_address":"10.42.15.90","version":"6.7.0","status":"INACTIVE","last_collection":"2024-01-10T09:22:10Z"}],"count":3}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl to skip certificate verification (already present in example, but ensure both curl commands include it). |
    | `{"error":"Invalid credentials","status":401}` | Verify the username, password, and domain type match the configured authentication backend in Aria Operations for Networks. |
    | `{"error":"Token expired","status":401}` | Regenerate the token as it has exceeded its TTL; for production use, implement token refresh logic or use API keys instead of session tokens. |
---

## Session Management

| Setting | Default | Recommended |
|---|---|---|
| Idle session timeout | 30 minutes | 15 minutes |
| Failed login lockout | 5 attempts | 5 attempts |
| Lockout duration | 30 minutes | 30 minutes |

Configure: Settings → Security → Session Timeout.

---

## LDAP Certificate Trust (LDAPS)

If using LDAPS (port 636), the LDAP CA certificate must be trusted by the Platform VM:

```bash
# SSH to Platform VM
ssh ubuntu@vrni.example.local

# Install CA certificate
sudo cp /tmp/corp-root-ca.crt /usr/local/share/ca-certificates/corp-root-ca.crt
sudo update-ca-certificates

# Restart vRNI after cert trust update
sudo systemctl restart hms
```


```text title="Expected output"
ubuntu@vrni.example.local's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-42-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

Last login: Mon Jan 15 14:32:18 2024 from 192.168.1.50
ubuntu@vrni:~$ sudo cp /tmp/corp-root-ca.crt /usr/local/share/ca-certificates/corp-root-ca.crt
ubuntu@vrni:~$ sudo update-ca-certificates
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; 5 kept from previous state.
Processing triggers for ca-certificates (20230311ubuntu0.20.04.1) ...
ubuntu@vrni:~$ sudo systemctl restart hms
ubuntu@vrni:~$
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cp: cannot stat '/tmp/corp-root-ca.crt': No such file or directory` | Verify the CA certificate file exists on the Platform VM or upload it first using `scp ubuntu@vrni.example.local:/path/to/cert`. |
    | `update-ca-certificates: command not found` | Install the ca-certificates package with `sudo apt-get install ca-certificates`. |
    | `Failed to restart hms: Unit hms.service not found.` | Verify the correct service name with `sudo systemctl list-units --type=service | grep -i hms` and use the actual service name. |
---

## Token Rotation Policy

| Token Type | Expiry | Rotation |
|---|---|---|
| Session tokens (API login) | 24 hours | Auto-expire |
| Long-lived API tokens | 90–365 days | Calendar reminder, revoke old on renewal |
| Service account tokens | 365 days | Rotate when personnel changes |

Review active tokens quarterly (Settings → API Tokens) and revoke any with no recent activity.
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements

## See also

- [Aria Operations for Networks — Access Control](../access-control/)
- [vRNI Security Hardening](../hardening/)
