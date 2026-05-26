# Aria Ops for Networks — Security

┌────────────────────────────────────── Aria Networks — Security ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  AD/LDAP auth for user access; data source service accounts for NSX/vCenter/switch collection │   │
│   │   API key management for REST API access; SNMP v3 credentials for physical switch collection  │   │
│   │   REST API over TLS; role-based access for data visibility; SAML support for SSO integration  │   │
│   │   Roles: Admin (full), Member (view), Auditor (read-only); scoped to data source visibility   │   │
│   │      Credential rotation policy for data source service accounts; API key TTL enforcement     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates platform access · RBAC limits data visibility                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │         AD/LDAP auth        │  │         Admin: full         │  │         REST API TLS        │   │
│   │         Local admin         │  │         Member: view        │  │        Collector TLS        │   │
│   │      Data src svc acct      │  │        Auditor: read        │  │         Data at rest        │   │
│   │         API key mgmt        │  │       Data src access       │  │          Cert mgmt          │   │
│   │         SAML support        │  │         Report share        │  │         SNMP v3 auth        │   │
│   │          Role-based         │  │          Alert mgmt         │  │         Pwd storage         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth controls user access · RBAC scopes data visibility · TLS and SNMP v3 protect data in transit  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   AD/LDAP auth   │    Admin role    │      REST TLS     │  Cred rotation   │    Event log     │   │
│   │     API keys     │   Member role    │   Collector TLS   │     SNMP v3      │   Data src log   │   │
│   │  Data src accts  │   Auditor role   │     Data encr     │  Cert rotation   │   Alert audit    │   │
│   │   SAML support   │   Report share   │    Pwd storage    │   API key TTL    │  Config changes  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · AD/LDAP · CA infrastructure             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AD/LDAP           = Active Directory or LDAP integration for user authentication to Aria Networks    │
│  API key           = Authentication token for REST API access; scoped to user role; subject to TTL    │
│  Data source credential = Service account used by Aria Networks to connect to NSX, vCenter, or        │
│  SNMP v3           = SNMPv3 credentials for physical switch collection; provides authentication and   │
│  Service account   = Dedicated non-interactive account used for data source authentication and        │
│  Admin role        = Full access role in Aria Networks; can configure data sources, users, and all    │
│  Member role       = Standard access role; can view topology, run queries, and use path trace features│
│  Auditor role      = Read-only role; can view all data and reports but cannot make configuration      │
│  TLS encryption    = Transport Layer Security enforced on all REST API and Collector-to-Platform      │
│  Certificate management = Platform and Collector TLS cert lifecycle including rotation and CA trust   │
│  Credential rotation = Periodic renewal of data source service account passwords and API keys per     │
│  Role-based access = RBAC model limiting which data sources and features each user role can access    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌────────────────────────────────────── Aria Networks — Security ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  AD/LDAP auth for user access; data source service accounts for NSX/vCenter/switch collection │   │
│   │   API key management for REST API access; SNMP v3 credentials for physical switch collection  │   │
│   │   REST API over TLS; role-based access for data visibility; SAML support for SSO integration  │   │
│   │   Roles: Admin (full), Member (view), Auditor (read-only); scoped to data source visibility   │   │
│   │      Credential rotation policy for data source service accounts; API key TTL enforcement     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates platform access · RBAC limits data visibility                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │         AD/LDAP auth        │  │         Admin: full         │  │         REST API TLS        │   │
│   │         Local admin         │  │         Member: view        │  │        Collector TLS        │   │
│   │      Data src svc acct      │  │        Auditor: read        │  │         Data at rest        │   │
│   │         API key mgmt        │  │       Data src access       │  │          Cert mgmt          │   │
│   │         SAML support        │  │         Report share        │  │         SNMP v3 auth        │   │
│   │          Role-based         │  │          Alert mgmt         │  │         Pwd storage         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth controls user access · RBAC scopes data visibility · TLS and SNMP v3 protect data in transit  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   AD/LDAP auth   │    Admin role    │      REST TLS     │  Cred rotation   │    Event log     │   │
│   │     API keys     │   Member role    │   Collector TLS   │     SNMP v3      │   Data src log   │   │
│   │  Data src accts  │   Auditor role   │     Data encr     │  Cert rotation   │   Alert audit    │   │
│   │   SAML support   │   Report share   │    Pwd storage    │   API key TTL    │  Config changes  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · AD/LDAP · CA infrastructure             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AD/LDAP           = Active Directory or LDAP integration for user authentication to Aria Networks    │
│  API key           = Authentication token for REST API access; scoped to user role; subject to TTL    │
│  Data source credential = Service account used by Aria Networks to connect to NSX, vCenter, or        │
│  SNMP v3           = SNMPv3 credentials for physical switch collection; provides authentication and   │
│  Service account   = Dedicated non-interactive account used for data source authentication and        │
│  Admin role        = Full access role in Aria Networks; can configure data sources, users, and all    │
│  Member role       = Standard access role; can view topology, run queries, and use path trace features│
│  Auditor role      = Read-only role; can view all data and reports but cannot make configuration      │
│  TLS encryption    = Transport Layer Security enforced on all REST API and Collector-to-Platform      │
│  Certificate management = Platform and Collector TLS cert lifecycle including rotation and CA trust   │
│  Credential rotation = Periodic renewal of data source service account passwords and API keys per     │
│  Role-based access = RBAC model limiting which data sources and features each user role can access    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, LDAP, local accounts, and identity sources.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data encryption and certificate management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
