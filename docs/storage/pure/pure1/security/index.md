---
tags:
  - pure
  - security
---
# Pure1 Security

<div class="kb-summary">
Pure1 Security reference covering Access Control (RBAC), SSO Configuration (SAML 2.0), Authentication Flow (RSA Key), Audit Logging, Data Security and 1 more sections.

*Applies to: Pure1*
</div>

```d2
direction: down

external: External / Untrusted {shape: rectangle}
access_control_rbac: "Access Control (RBAC)" {shape: rectangle}
sso_configuration_saml_20: "SSO Configuration (SAML 2.0)" {shape: rectangle}
authentication_flow_rsa_key: "Authentication Flow (RSA Key)" {shape: rectangle}
audit_logging: "Audit Logging" {shape: rectangle}
data_security: "Data Security" {shape: rectangle}
security_hardening_checklist: "Security Hardening Checklist" {shape: rectangle}
core: "Pure1 Core" {shape: hexagon}

external -> access_control_rbac: traffic in
access_control_rbac -> sso_configuration_saml_20
sso_configuration_saml_20 -> authentication_flow_rsa_key
authentication_flow_rsa_key -> audit_logging
audit_logging -> data_security
data_security -> security_hardening_checklist
security_hardening_checklist -> core: secured path
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Access Control (RBAC)

Pure1 uses role-based access control managed in the Pure1 portal. Assign the minimum required role to each user.

| Role | Capabilities |
|---|---|
| Admin | Full access: configuration, notifications, user management, API registration |
| Read-only | View fleet data, health, capacity, alerts — no configuration changes |

User management: **Pure1 portal > Administration > User Management**

Operations staff monitoring dashboards should have the Read-only role. Admin access is limited to designated Pure1 platform administrators.

## SSO Configuration (SAML 2.0)

Pure1 supports SAML 2.0 SSO and SCIM provisioning from enterprise IdPs (Okta, Azure AD, ADFS).

## Authentication Flow (RSA Key)

Pure1 REST API v1 uses a JWT signed with the RSA private key for authentication.

```python
import jwt, time, uuid, requests
from cryptography.hazmat.primitives import serialization

def get_pure1_token(client_id: str, key_id: str, private_key_pem: str) -> str:
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(), password=None
    )
    payload = {
        "iss": client_id,
        "sub": client_id,
        "aud": "pure1:auth:mfa",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "jti": str(uuid.uuid4())
    }
    id_token = jwt.encode(payload, private_key, algorithm="RS256",
                          headers={"kid": key_id})
    resp = requests.post("https://api.pure1.purestorage.com/oauth2/1.0/token",
                         data={"grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                               "subject_token": id_token,
                               "subject_token_type": "urn:ietf:params:oauth:token-type:json_web_token"})
    resp.raise_for_status()
    return resp.json()["access_token"]
```

## Audit Logging

Pure1 logs all admin actions in an audit trail.

```text
Pure1 > Administration > Audit Log
- Filter by user, date, or action type
- Export to CSV for SIEM ingestion
```

Key events to monitor:
- User logins (especially from unexpected locations)
- API key creation and rotation
- Notification rule changes
- Admin role changes

Export audit logs monthly to SIEM for long-term retention.

## Data Security

| Consideration | Detail |
|---|---|
| Telemetry data type | Performance metrics, capacity data, component health — no workload data or customer content |
| Data isolation | Telemetry scoped per customer tenant in Pure Storage cloud |
| Array write-back | None — Pure1 is read-only; it cannot modify array configuration |
| Transmission security | TLS 1.2+ for all API calls and telemetry upload |

## Security Hardening Checklist

- [ ] SSO enabled; local accounts disabled for non-break-glass users
- [ ] Admin role limited to designated platform administrators
- [ ] One API service account per consuming system; read-only scope
- [ ] Private keys stored in secrets manager; not in filesystem or code repositories
- [ ] API key rotation on annual schedule; rotation dates tracked
- [ ] Audit log exported to SIEM monthly
- [ ] SCIM provisioning enabled for automatic account lifecycle management
- [ ] Annual user account review — remove or reassign accounts for departed staff
