# Pure1 Security
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

```text
Pure1 > Administration > Single Sign-On > Configure
- IdP metadata URL or XML upload
- Attribute mapping:
  - email → user account
  - role claim → Admin or Read-only (via IdP group claim)
- Enable SCIM for automatic user provisioning/deprovisioning
```
┌────────────────────────────────────────── Pure1 — Security ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Access Control                │  │                Data Security                │   │
│   │             SSO / local account              │  │              TLS 1.2 phonehome              │   │
│   │              MFA on Pure1 login              │  │              Encrypted at rest              │   │
│   │              RBAC: Admin/Viewer              │  │                Telemetry only               │   │
│   │               API RSA key auth               │  │                No data access               │   │
│   │             Annual access review             │  │                 SOC2 Type II                │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Data in Pure cloud datacentres · tenant isolation · SOC2 Type II · no customer data                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SSO = Single Sign-On; Pure1 supports SAML 2.0 for corporate IdP integration                          │
│  MFA = Multi-factor authentication for Pure1 UI login                                                 │
│  RBAC = Admin (full) vs Viewer (read-only) per Pure1 org                                              │
│  RSA key auth = Pure1 API uses RSA-signed JWT; no shared secret                                       │
│  TLS 1.2 = Phonehome and API connections encrypted in transit                                         │
│  Telemetry only = Pure1 receives metrics and events; no customer data or files                        │
│  No data access = Pure Storage cannot access stored customer data via Pure1                           │
│  Encrypted at rest = Telemetry data encrypted in Pure cloud storage                                   │
│  SOC2 Type II = Pure Storage annual security audit; covers data handling                              │
│  Tenant isolation = Each customer org data separated in multi-tenant cloud                            │
│  Annual review = Yearly audit of Pure1 users; remove stale accounts and roles                         │
│  API key rotation = RSA key pair rotated annually per security policy                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

### Secure Key Storage

```bash
# Never store the private key in plain text in scripts or repos
# Load from secrets manager at runtime:

import boto3  # example using AWS Secrets Manager

def get_pure1_private_key() -> str:
    client = boto3.client("secretsmanager", region_name="eu-west-1")
    secret = client.get_secret_value(SecretId="pure1/api-private-key")
    return secret["SecretString"]
```

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
