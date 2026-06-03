```bash
# Via REST API
TOKEN=$(curl -sk -X POST https://nd-dc1.corp.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"userName":"admin","userPasswd":"<pass>","domain":"local"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk -X POST https://nd-dc1.corp.example.com/nexus/api/v1/users \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "svc-monitor",
    "password": "<strong-password>",
    "firstName": "Service",
    "lastName": "Monitor",
    "email": "san-team@corp.example.com",
    "roles": [{"name": "Viewer", "sites": [{"name": "DC1-SAN"}, {"name": "DC2-SAN"}]}]
  }' | python3 -m json.tool
```

```text
┌─────────────────────────── Cisco Nexus Dashboard — Security Access Control ───────────────────────────┐
│                                                                                                       │
│  RBAC model with local and AAA-backed users; per-app roles scoped to tenant or site.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               User Management                │  │                  Role Model                 │   │
│   │          Local users: ND-native DB           │  │          Admin: full cluster access         │   │
│   │         Remote: LDAP/RADIUS/TACACS+          │  │        Operator: read + limited write       │   │
│   │          Groups: mapped to ND roles          │  │             Read-only: view only            │   │
│   │        Password policy: enforce cmplx        │  │         App roles: per NDFC/NDI/NDO         │   │
│   │        Session timeout: configurable         │  │         Site scope: per-site access         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Roles assigned at cluster level; app-specific roles further restrict within each app                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              API Access Control              │  │                    Audit                    │   │
│   │         REST API: Bearer token auth          │  │          Login events: success/fail         │   │
│   │          Token TTL: 60 min default           │  │           Config changes: who+what          │   │
│   │         Service accounts: dedicated          │  │          API calls: logged per user         │   │
│   │         IP allowlist: restrict mgmt          │  │            Export: syslog to SIEM           │   │
│   │            MFA: via SAML IdP only            │  │          Retention: 90-day default          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster · LDAP/RADIUS/TACACS+ server · SAML IdP · SIEM · management network                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RBAC           = Role-Based Access Control; maps users/groups to permitted actions                   │
│  LDAP group map = Mapping LDAP group DN to an ND role for automatic assignment                        │
│  App role       = Role scoped to a specific ND app (NDFC/NDI/NDO) not cluster-wide                    │
│  Site scope     = Restricting a user to only manage specific onboarded sites                          │
│  Service account= Dedicated ND user for automation; not used for human login                          │
│  IP allowlist   = Network ACL restricting management access to known source IPs                       │
│  MFA            = Multi-Factor Auth; enforced by SAML IdP (not natively by ND)                        │
│  Token TTL      = JWT lifetime; default 60 min; reduce for higher security posture                    │
│  Password complexity= Minimum length, upper/lower/digit/special char requirements                     │
│  Session timeout= Idle period after which UI session is automatically terminated                      │
│  SIEM export    = Forwarding ND audit logs via syslog TLS to Splunk or similar                        │
│  Audit retention= How long ND retains access logs before purging (default 90 days)                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
